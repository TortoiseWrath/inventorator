<template>
  <item-editor :parent="$route.params.id" :key="$route.params.id + ' ' + submitted"
               @upload="update" @right="navRight" @down="navDown" @up="navUp"/>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {ItemDetails} from '@/types/ItemDetails';
import ItemEditor from '@/components/ItemEditor.vue';

export default defineComponent({
  name: 'AddItem',
  components: {ItemEditor},
  data() {
    return {
      submitted: 0,
    };
  },
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
      this.toastSuccess(`Added item ${json.id}`);
      return json.id;
    },
    update(item: ItemDetails) {
      this.uploadItem(item)
          .then((id: string) => this.$router.push(`/item/${id}`))
          .catch(this.toastError); // Errors reported by uploadItem
      // TODO: Handle 500 error separately when adding item
    },
    navRight(item: ItemDetails) {
      if (this.isEmpty(item)) {
        // Don't bother adding an empty item
        this.toastWarning('Item is empty', 2);
      } else {
        this.uploadItem(item)
            .then((id: string) => this.submitted++) // Force reload -> new item, same parent
            .catch(this.toastError);
      }
    },
    navDown(item: ItemDetails) {
      this.uploadItem(item)
          .then((id: string) => this.$router.push(`/add/${id}`))
          .catch(this.toastError);
    },
    navUp(item: ItemDetails) {
      if (this.isEmpty(item)) {
        // Don't bother adding an empty item.
        this.toastNotice('Ignoring empty item', 1);
        this.$router.push(`/item/${item.parent}`);
      } else {
        this.uploadItem(item)
            .then((id: string) => this.$router.push(`/item/${item.parent}`))
            .catch(this.toastError);
      }
    },
    toastError(message: string, duration = 5) {
      console.error(message);
      // TODO: Toast error
    },
    toastSuccess(message: string, duration = 1) {
      console.log(message);
      // TODO: Toast success
    },
    toastNotice(message: string, duration = 5) {
      console.log(message);
      // TODO: Toast notice
    },
    toastWarning(message: string, duration = 2) {
      console.warn(message);
      // TODO: Toast warning
    },
    isEmpty(item: ItemDetails) {
      return !item.photos?.length && !item.links?.length && !item.title && !item.description && !item.upc;
    },
  },
});
</script>

<style scoped lang="scss">

</style>