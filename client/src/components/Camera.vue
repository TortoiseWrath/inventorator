<template>
  <div>
    <video autoplay disablePictureInPicture ref="video"/>
    <button @click="takePhoto">Take Photo</button>
    <div ref="target"></div>
  </div>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {useToast} from 'vue-toastification';

export default defineComponent({
  name: 'Camera',
  data() {
    return {
      toast: useToast(),
      track: {} as MediaStreamTrack,
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
    }
  },
  methods: {
    async capturePhoto(): Promise<Blob> {
      // TODO: Webcam fallback for Firefox
      // TODO: Use photoSettings once it's supported somewhere
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
      } catch (e: any) {
        console.error(e);
        this.toast.error(e.message);
      }
    },
    takePhoto() {
      this.capturePhoto().then((blob) => this.uploadPhoto(blob));
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