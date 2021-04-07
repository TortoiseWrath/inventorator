<template>
  <div class="container">
    <img :src="`http://localhost:5000/photo/${path}`" @click="modal"/>
    <font-awesome-icon icon="times-circle" class="delete" @click="confirmDeletion"/>
  </div>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {FontAwesomeIcon} from '@/plugins/font-awesome';
import {useToast} from 'vue-toastification';

export default defineComponent({
  name: 'Thumbnail',
  emits: ['destroy', 'enlarge'],
  props: {
    path: String,
  },
  components: {
    FontAwesomeIcon,
  },
  data() {
    return {
      toast: useToast(),
      showModal: false,
    };
  },
  methods: {
    modal() {
      this.$emit('enlarge');
    },
    async deletePhoto() {
      try {
        const response: Response = await fetch(`http://localhost:5000/photo/${this.path}`, {method: 'DELETE'});
        const json = await response.json();
        if (!response.ok) {
          console.error(response);
          console.error(json);
          this.toast.error(json.error.join(' '));
        } else {
          this.$emit('destroy');
        }
      } catch (e) {
        console.error(e);
        this.toast.error(e.message);
      }
    },
    confirmDeletion() {
      this.showModal = true;
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
    // TODO: Add a transition for image delete button
  }
}
</style>