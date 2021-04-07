<template>
  <video autoplay disablePictureInPicture ref="video"/>
  <button @click="takePhoto">Take Photo</button>
  <div ref="target"></div>
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
      console.log(blob);
    },
    takePhoto() {
      this.capturePhoto().then((blob) => this.uploadPhoto(blob));
    },
  },
});
</script>

<style scoped lang="scss">

</style>