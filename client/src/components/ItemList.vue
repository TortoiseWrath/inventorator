<template>
  <ul>
    <li v-for="(item, index) in items" :key="index">
      <button v-if="item.childCount" @click="item.expanded = true">Expand</button>
      <div v-else class="spacer"/>
      <div class="title">{{ item.title }}</div>
      <div class="childCount">{{ item.childCount }}</div>
      <div class="value">{{ item.value }}</div>
      <div class="weight">{{ item.weight }}</div>
      <div class="volume">{{ item.volume }}</div>
      <button class="add">Add Children</button>
      <button class="edit">Edit</button>
      <button class="delete">Delete</button>
      <item-list v-if="item.expanded" v-bind:parent="item.id"/>
    </li>
  </ul>
</template>

<script lang="ts">
import {defineComponent} from 'vue';

type Item = {
  title: string,
  childCount: number,
  value: number,
  weight: number,
  volume: number,
  id: string,
  expanded?: boolean // null at first, then true or false later on
}

export default defineComponent({
  name: 'ItemList',
  data() {
    return {
      items: [] as Item[],
    };
  },
  props: {
    parent: {
      type: String,
      required: true,
    },
  },
  methods: {
    load() {
      fetch(`http://localhost:5000/items/${this.parent}`).then(response => response.json()).then(data => this.items = data.items);
    },
  },
  created() {
    this.load();
  },
});
</script>

<style scoped lang="scss">

</style>