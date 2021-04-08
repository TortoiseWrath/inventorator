<template>
  <div>
    <video autoplay disablePictureInPicture ref="video"/>
    <label v-if="videoDevices.length > 1"><span>Camera</span>
      <select v-model="videoDevice" @change="startVideo">
        <option v-for="(videoDevice, index) in videoDevices" :key="index" :value="index">
          {{ videoDevice.label }}
        </option>
      </select>
      <button @click="nextCamera">Next</button>
    </label>
    <button @click="takePhoto">Take Photo</button>
    <button @click="scanBarcode">Scan Barcode</button>
    <div ref="target"/>
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
      videoElement: {} as HTMLVideoElement,
      videoDevices: [] as MediaDeviceInfo[],
      videoDevice: 0,
    };
  },
  mounted() {
    this.videoElement = this.$refs.video as HTMLVideoElement;
    navigator.mediaDevices.enumerateDevices().then((devices) => devices.forEach((device) => {
      if (device.kind === 'videoinput') {
        this.videoDevices.push(device);
      }
    })).then(() => this.startVideo());
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
    },
    cameraShortcut: {
      type: Number,
      required: false,
    },
  },
  watch: {
    photoShortcut: function () {
      this.takePhoto();
    },
    barcodeShortcut: function () {
      this.scanBarcode();
    },
    cameraShortcut: function () {
      this.nextCamera();
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
    async readBarcode(blob: Blob) {
      try {
        const response: Response = await fetch(`http://localhost:5000/barcode`, {method: 'POST', body: blob});
        const json = await response.json();
        if (!response.ok) {
          console.error(response);
          console.error(json);
          this.toast.error(json.error.join(' '));
        } else {
          console.log(json);
          if (json.length == 0) {
            this.toast.warning('Didn\'t find a barcode');
          } else if (json.length > 1) {
            this.toast.warning('Found multiple barcodes:<br>' + json.join('<br>'));
          } else {
            this.$emit('barcode', json[0]);
          }
        }
      } catch (e) {
        console.error(e);
        this.toast.error(e.message);
      }
    },
    scanBarcode() {
      this.capturePhoto().then((blob) => this.readBarcode(blob));
    },
    startVideo() {
      navigator.mediaDevices.getUserMedia({
        video: {
          width: {ideal: 10000},
          height: {ideal: 10000},
          deviceId: this.videoDevices[this.videoDevice].deviceId,
        },
      })
          .then(stream => {
            this.videoElement.srcObject = stream;
            this.track = stream.getVideoTracks()[0];
          })
          .catch(e => console.error(e));
    },
    nextCamera() {
      if (this.videoDevice >= this.videoDevices.length - 1) {
        this.videoDevice = 0;
      } else {
        this.videoDevice++;
      }
      this.startVideo();
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

label {
  display: block;

  span {
    display: none;
  }
}
</style>