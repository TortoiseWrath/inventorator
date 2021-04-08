<template>
  <item-editor :id="$route.params.id" :key="$route.params.id + ' ' + submitted"
               @upload="update" @right="navRight" @down="navDown" @up="navUp" @next="navNext"/>
  <section>
    <h2>Children</h2>
    <item-list :parent="parseInt($route.params.id.toString())" :key="$route.params.id"/>
  </section>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {ItemDetails} from '@/types/ItemDetails';
import ItemEditor from '@/components/ItemEditor.vue';
import {useToast} from 'vue-toastification';
import ItemList from '@/components/ItemList.vue';

export default defineComponent({
  name: 'EditItem',
  components: {ItemList, ItemEditor},
  data() {
    return {
      submitted: 0,
      toast: useToast(),
    };
  },
  methods: {
    async uploadItem(item: ItemDetails) {
      const response: Response = await fetch(`http://localhost:5000/item/${item.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(item),
      });
      if (!response.ok) {
        const json = await response.json();
        throw json.error.join(' ');
      }
      this.toast.success(`Updated item ${item.id}`, {timeout: 500});
    },
    update(item: ItemDetails) {
      this.uploadItem(item)
          .then(() => this.submitted++) // Force a reload of the item editor
          .catch(this.toast.error); // Errors reported by uploadItem
    },
    navRight(item: ItemDetails) {
      this.uploadItem(item)
          .then(() => this.$router.push(`/add/${item.parent}`))
          .catch(this.toast.error);
    },
    navDown(item: ItemDetails) {
      this.uploadItem(item)
          .then(() => this.$router.push(`/add/${item.id}`))
          .catch(this.toast.error);
    },
    navUp(item: ItemDetails) {
      if (item.parent && item.parent < 2) {
        this.toast.error('Already at root!', {timeout: 2000});
      } else {
        this.uploadItem(item)
            .then(() => this.$router.push(`/item/${item.parent}`))
            .catch(this.toast.error);
      }
    },
    navNext(item: ItemDetails) {
      fetch(`http://localhost:5000/sibling/${item.id}`)
      .then((response) => response.json())
      .then((json) => this.$router.push(`/item/${json.id}`))
      .catch(this.toast.error);
    },
  },
});
</script>

<style scoped lang="scss">
h2 {
  display: none;
}

h2 + * {
  border-top: 1px solid #ccc;
}
</style>