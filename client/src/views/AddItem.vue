<template>
  <item-editor :parent="$route.params.id"
               @upload="update" @right="navRight" @down="navDown" @up="navUp"/>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {ItemDetails} from '@/types/ItemDetails';
import ItemEditor from '@/components/ItemEditor.vue';

export default defineComponent({
  name: 'AddItem',
  components: {ItemEditor},
  methods: {
    async uploadItem(item: ItemDetails): Promise<string> { // Returns item key
      const response: Response = await fetch(`http://localhost:5000/item`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(item),
      });
      const json = await response.json();
      if (!response.ok) {
        throw json.error.join(' ');
      }
      this.toastSuccess();
      return json.id;
    },
    update(item: ItemDetails) {
      this.uploadItem(item)
          .then((id: string) => console.log('Submitted ' + id)) // Force a reload of the item editor
          .catch(this.toastError); // Errors reported by uploadItem
          // TODO: Handle 500 error separately when adding item
    },
    navRight(item: ItemDetails) {
      this.uploadItem(item)
          .then((id: string) => console.log('navRight ' + id))
          .catch(this.toastError);
    },
    navDown(item: ItemDetails) {
      this.uploadItem(item)
          .then((id: string) => console.log('navDown ' + id))
          .catch(this.toastError);
    },
    navUp(item: ItemDetails) {
      this.uploadItem(item)
          .then((id: string) => console.log('navUp ' + id))
          .catch(this.toastError);
    },
    toastError(error: string) {
      console.error(error);
      // TODO: Toast error
    },
    toastSuccess() {
      console.log('Added successfully :)');
      // TODO: Toast success
    },
  },
});
</script>

<style scoped lang="scss">

</style>