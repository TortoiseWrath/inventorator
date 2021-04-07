<template>
  <div class="container">
    <img :src="`http://localhost:5000/photo/${path}`" @click="modal"/>
    <font-awesome-icon icon="times-circle" class="delete" @click="confirmAndDestroy"/>
  </div>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {FontAwesomeIcon} from '@/plugins/font-awesome';

export default defineComponent({
  name: 'Thumbnail',
  emits: ['destroy'],
  props: {
    path: String,
  },
  components: {
    FontAwesomeIcon,
  },
  methods: {
    modal() {
      console.log('modal');
    },
    destroy() {
      this.$emit('destroy');
    },
    confirmAndDestroy() {

      this.destroy();
    },
  },
});
</script>

<style scoped lang="scss">
div.container {
  display: inline-block;
  position: relative;

  img {
    max-width: 1.25in;
  }

  .delete {
    opacity: 0;
    position: absolute;
    $size: 0.2in;
    $space: 0.03in;
    width: $size;
    height: $size;
    top: $space;
    right: $space;
    color: $danger;

    &:hover {
      color: $danger-hover;
      cursor: pointer;
    }
  }

  &:hover .delete {
    opacity: 0.8;
    // TODO: Add a transition for image delete button
  }
}
</style>