<template>
  Item: {{ item.title }}
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {FontAwesomeIcon} from '@/plugins/font-awesome';
import {ItemDetails} from '@/types/ItemDetails';

export default defineComponent({
  name: 'EditItem',
  data() {
    return {
      item: {} as ItemDetails,
    };
  },
  // components: {
  //   FontAwesomeIcon,
  // },
  methods: {
    load() {
      fetch(`http://localhost:5000/details/${this.$route.params.id}`)
          .then(response => response.json())
          .then(data => this.item = data.item);
    },
  },
  created() {
    this.load();
  },
});
</script>

<style scoped lang="scss">

</style>