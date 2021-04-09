<template>
  <div>
    <video autoplay disablePictureInPicture ref="video"/>
    <label v-if="state.videoDevices?.length > 1"><span>Camera</span>
      <select v-model="state.videoDevice" @change="startVideo">
        <option v-for="(videoDevice, index) in state.videoDevices" :key="index" :value="index">
          {{ videoDevice?.label }}
        </option>
      </select>
      <!--      <button @click="nextCamera">Next</button>-->
    </label>
    <button @click="takePhoto">Take Photo</button>
    <button @click="scanBarcode">Scan Barcode</button>
    <div class="timer">
      <label>Timer:
        <input v-model="timerSeconds" type="number"/>
             seconds
      </label>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {useToast} from 'vue-toastification';
import {BrowserMultiFormatReader} from '@zxing/library';
import {useState} from '@/state';

export default defineComponent({
  name: 'Camera',
  data() {
    return {
      toast: useToast(),
      track: {} as MediaStreamTrack,
      scanner: new BrowserMultiFormatReader(),
      videoElement: {} as HTMLVideoElement,
      state: useState(),
      timerSeconds: 0,
    };
  },
  mounted() {
    this.videoElement = this.$refs.video as HTMLVideoElement;
    if (!this.state.videoDevice) {
      this.state.videoDevices = [];
      this.state.videoDevice = 0;
      navigator.mediaDevices.enumerateDevices().then((devices) => devices.forEach((device) => {
        if (device.kind === 'videoinput') {
          this.state.videoDevices?.push(device);
        }
      })).then(() => this.startVideo());
    } else {
      this.startVideo();
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
      await this.timeCapture();
      const imageCapture = new ImageCapture(this.track);
      return imageCapture.takePhoto();
    },
    async timeCapture(): Promise<void> {
      if (this.timerSeconds === 0) {
        return;
      }
      return new Promise((resolve, reject) => {
        setTimeout(resolve, this.timerSeconds * 1000);
        this.toast.info('Wait for photo capture', {
          showCloseButtonOnHover: false,
          pauseOnHover: false,
          pauseOnFocusLoss: false,
          timeout: this.timerSeconds * 1000,
          onClose: () => reject(), // TODO: Catch rejected promise from canceled photo capture
        });
      });
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
      if (this.state.videoDevices === undefined || this.state.videoDevice === undefined) {
        this.toast.error('No video devices');
        return;
      }
      navigator.mediaDevices.getUserMedia({
        video: {
          width: {ideal: 10000},
          height: {ideal: 10000},
          deviceId: this.state.videoDevices[this.state.videoDevice].deviceId,
        },
      })
          .then(stream => {
            this.videoElement.srcObject = stream;
            this.track = stream.getVideoTracks()[0];
          })
          .catch(e => console.error(e));
    },
    nextCamera() {
      if (this.state.videoDevices === undefined || this.state.videoDevice === undefined) {
        return;
      }
      if (this.state.videoDevice >= this.state.videoDevices.length - 1) {
        this.state.videoDevice = 0;
      } else {
        this.state.videoDevice++;
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

div.timer input {
  width: 3em;
}
</style>