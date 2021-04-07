<template>
  <div>
    <video autoplay disablePictureInPicture ref="video"/>
    <button @click="takePhoto">Take Photo</button>
    <button @click="startScan">Scan Barcode</button>
    <div ref="target"/>
  </div>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {useToast} from 'vue-toastification';
import {BrowserMultiFormatReader, NotFoundException} from '@zxing/library';
import Result from '@zxing/library/esm/core/Result';
import Exception from '@zxing/library/esm/core/Exception';

export default defineComponent({
  name: 'Camera',
  data() {
    return {
      toast: useToast(),
      video: {} as HTMLVideoElement,
      stream: {} as MediaStream,
      scanningToast: null as string | number | null,
      scanner: new BrowserMultiFormatReader(),
    };
  },
  mounted() {
    this.video = this.$refs.video as HTMLVideoElement;
    if (navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({
        video: {
          width: {ideal: 10000},
          height: {ideal: 10000},
        },
      })
          .then(stream => {
            this.video.srcObject = stream;
            this.stream = stream;
          })
          .catch(e => console.error(e));
    }
  },
  emits: {
    photo(path: string) {
      return !!path;
    },
    barcode(value: string) {
      return new RegExp('^[0-9 ]+$').test(value);
    },
  },
  methods: {
    async capturePhoto(): Promise<Blob> {
      // TODO: Webcam fallback for Firefox
      // TODO: Use photoSettings once it's supported somewhere
      const imageCapture = new ImageCapture(this.stream.getVideoTracks()[0]);
      return imageCapture.takePhoto();
    },
    async uploadPhoto(blob: Blob) {
      try {
        const response: Response = await fetch(`http://localhost:5000/photo`, {method: 'POST', body: blob});
        const json = await response.json();
        if (!response.ok) {
          console.error(response);
          console.error(json);
          this.toast.error(json.error.join(' '));
        } else {
          console.log(`Photo uploaded to: ${json.path}`);
          this.$emit('photo', json.path);
        }
      } catch (e) {
        console.error(e);
        this.toast.error(e.message);
      }
    },
    takePhoto() {
      this.capturePhoto().then((blob) => this.uploadPhoto(blob));
    },
    startScan() {
      this.scanningToast = this.toast.info('Scanning barcode', {
        timeout: false,
        showCloseButtonOnHover: false,
        onClose: this.stopScan,
      });
      this.scanner.decodeFromStream(this.stream, this.video, this.scanCallback);
    },
    stopScan() {
      console.log('STOPPING');
      this.scanner.stopContinuousDecode();
      this.video.srcObject = this.stream;
    },
    scanCallback(result: Result, err?: Exception) {
      if (result) {
        console.log(result);
        this.toast.warning(result);
      }
      if (err) {
        if (err instanceof NotFoundException) {
          return; // Keep looking
        }
        console.error(err);
        this.toast.error(err.message);
      }
      this.stopScan();
      if (this.scanningToast != null) {
        this.toast.dismiss(this.scanningToast);
        this.scanningToast = null;
      }
    },
  },
});
</script>

<style scoped lang="scss">
video {
  width: 100%;
}

div {
  max-width: 50%;
}
</style>