<template>
  <item-editor :id="$route.params.id" @upload="uploadItem" @right="navRight" @down="navDown" @up="navUp"/>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {ItemDetails} from '@/types/ItemDetails';
import ItemEditor from '@/components/ItemEditor.vue';

export default defineComponent({
  name: 'EditItem',
  components: {ItemEditor},
  methods: {
    uploadItem(item: ItemDetails): boolean {
      console.log(item);
      fetch(`http://localhost:5000/item/${item.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(item),
      }).then(response => console.log(response));
      // TODO: handle errors when updating item
      return true;
    },
    navRight(item: ItemDetails) {
      if (!this.uploadItem(item)) return;
      console.log('navRight');
    },
    navDown(item: ItemDetails) {
      if (!this.uploadItem(item)) return;
      console.log('navDown');
    },
    navUp(item: ItemDetails) {
      if (!this.uploadItem(item)) return;
      console.log('navUp');
    },
  },
});
</script>

<style scoped lang="scss">

</style>