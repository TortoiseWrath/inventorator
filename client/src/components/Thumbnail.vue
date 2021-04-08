<template>
  <div>
    <div class="container">
      <img :src="`http://localhost:5000/photo/${path}`" @click="$emit('enlarge')"/>
      <font-awesome-icon icon="times-circle" class="delete" @click="$emit('delete')"/>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {FontAwesomeIcon} from '@/plugins/font-awesome';

export default defineComponent({
  name: 'Thumbnail',
  emits: ['delete', 'enlarge'],
  props: {
    path: String,
  },
  components: {
    FontAwesomeIcon,
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

  &:hover {
    cursor: pointer;

    .delete {
      opacity: 0.8;
    }
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
    }
  }

  &:hover .delete {
    opacity: 0.8;
    // @todo Add a transition for image delete button
  }
}
</style>