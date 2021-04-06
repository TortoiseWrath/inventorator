<template>
  <input type="date" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)">
</template>

<script lang="ts">
import {defineComponent} from 'vue';

export default defineComponent({
  name: 'DateStringSelector',
  props: ['modelValue'],
  emits: ['update:modelValue'],
  beforeUpdate() {
    if (!this.modelValue) {
      return; // Ignore empty date
    }
    const parsedDate: string = new Date(this.modelValue).toISOString().split('T')[0];
    if (parsedDate !== this.modelValue) {
      this.$emit('update:modelValue', parsedDate);
    }
  },
});
</script>

<style scoped lang="scss">

</style>