<template>
  <div>
    <video autoplay disablePictureInPicture ref="video"/>
    <button @click="takePhoto">Take Photo</button>
    <button @click="scanBarcode">Scan Barcode</button>
    <div ref="target"/>
    <img class="barcode" ref="barcodeImage"/>
  </div>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {useToast} from 'vue-toastification';
import {BrowserMultiFormatReader, NotFoundException, Result} from '@zxing/library';

export default defineComponent({
  name: 'Camera',
  data() {
    return {
      toast: useToast(),
      track: {} as MediaStreamTrack,
      scanner: new BrowserMultiFormatReader(),
    };
  },
  mounted() {
    const video = this.$refs.video as HTMLVideoElement;
    if (navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({
        video: {
          width: {ideal: 10000},
          height: {ideal: 10000},
        },
      })
          .then(stream => {
            video.srcObject = stream;
            this.track = stream.getVideoTracks()[0];
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
  props: {
    photoShortcut: {
      type: Number,
      required: false,
    },
    barcodeShortcut: {
      type: Number,
      required: false,
    }
  },
  watch: {
    photoShortcut: function() {
      this.takePhoto();
    },
    barcodeShortcut: function() {
      this.scanBarcode();
    },
  },
  methods: {
    async capturePhoto(): Promise<Blob> {
      // @todo Webcam fallback for Firefox
      // @todo Use photoSettings once it's supported somewhere
      const imageCapture = new ImageCapture(this.track);
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
    async startScan() {
      // @todo Continuous barcode scanning
      // @todo Fix the barcode scanner
      const image: Blob = await this.capturePhoto();
      console.log(image);
      const imageElement = this.$refs.barcodeImage as HTMLImageElement;
      imageElement.src = window.URL.createObjectURL(image);
      console.log(imageElement.src);
      try {
        const result: Result = await this.scanner.decodeFromImageElement(imageElement);
        console.log(result);
        this.toast.info(result);
      } catch (err) {
        if (err instanceof NotFoundException) {
          this.toast.warning('No barcode detected', {timeout: 1000});
        } else {
          console.error(err);
          this.toast.error(err.message);
        }
      }
      // this.scanner.reset();
    },
    scanBarcode() {
      this.startScan().then();
    },
  },
});
</script>

<style scoped lang="scss">
video {
  width: 100%;
}

button {
  font: inherit;
  font-size: 110%;
  padding: 0.2em 0.5em;
  margin: 0.3em 1em;
}
</style>