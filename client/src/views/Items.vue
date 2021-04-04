<template>
  <item-list parent="1"/>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import ItemList from '@/components/ItemList.vue';

export default defineComponent({
  components: {ItemList},
});
</script>

<style scoped lang="scss">

</style>