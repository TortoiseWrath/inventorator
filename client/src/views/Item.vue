<template>
  Item {{id}}
</template>

<script lang="ts">
import {defineComponent} from 'vue';

export default defineComponent({
  props: {
    parent: {
      type: Number,
      required: true,
    },
  }
});
</script>

<style scoped lang="scss">

</style>