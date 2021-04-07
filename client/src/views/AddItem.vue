<template>
  <item-editor :parent="$route.params.id" :key="$route.params.id + ' ' + submitted"
               @upload="update" @right="navRight" @down="navDown" @up="navUp"/>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {ItemDetails} from '@/types/ItemDetails';
import ItemEditor from '@/components/ItemEditor.vue';
import {useToast} from 'vue-toastification';

export default defineComponent({
  name: 'AddItem',
  components: {ItemEditor},
  data() {
    return {
      submitted: 0,
      toast: useToast(),
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
      this.toast.success(`Added item ${json.id}`, {timeout: 500});
      return json.id;
    },
    update(item: ItemDetails) {
      this.uploadItem(item)
          .then((id: string) => this.$router.push(`/item/${id}`))
          .catch(this.toast.error); // Errors reported by uploadItem
      // TODO: Handle 500 error separately when adding item
    },
    navRight(item: ItemDetails) {
      if (this.isEmpty(item)) {
        // Don't bother adding an empty item
        this.toast.warning('Item is empty', {timeout: 1000});
      } else {
        this.uploadItem(item)
            .then(() => this.submitted++) // Force reload -> new item, same parent
            .catch(this.toast.error);
      }
    },
    navDown(item: ItemDetails) {
      this.uploadItem(item)
          .then((id: string) => this.$router.push(`/add/${id}`))
          .catch(this.toast.error);
    },
    navUp(item: ItemDetails) {
      if (this.isEmpty(item)) {
        // Don't bother adding an empty item.
        this.toast.info('Ignoring empty item', {timeout: 500});
        this.$router.push(`/item/${item.parent}`);
      } else {
        this.uploadItem(item)
            .then(() => this.$router.push(`/item/${item.parent}`))
            .catch(this.toast.error);
      }
    },
    isEmpty(item: ItemDetails) {
      return !item.photos?.length && !item.links?.length && !item.title && !item.description && !item.upc;
    },
  },
});
</script>

<style scoped lang="scss">

</style>