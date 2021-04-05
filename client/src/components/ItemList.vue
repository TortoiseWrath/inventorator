<template>
  <ul>
    <li v-for="(item, index) in items" :key="index">
      <div class="left">
        <button v-if="item.childCount" v-show="!item.expanded" @click="item.expanded = true" class="expand">
          Expand
        </button>
        <button v-if="item.childCount" v-show="item.expanded" @click="item.expanded = false" class="collapse">
          Collapse
        </button>
        <div v-if="!item.childCount" class="spacer"/>

        <!-- TODO: Add checkboxes -->

        <div class="title">{{ item.title }}</div>
      </div>
      <div class="right">
        <div class="childCount">{{ item.childCount }}</div>

        <div class="value">{{ item.totalValue }}</div>
        <!-- TODO: Show value details on hovering value -->

        <div v-bind:class="['weight', {'warning': lt(item.weight, item.totalWeight)}]">
          {{ item.totalWeight }}
        </div>
        <!-- TODO: Show weight details on hovering weight -->

        <div v-bind:class="['volume', {'warning': lt(item.volume, item.totalVolume)}]">
          {{ item.totalVolume }}
        </div>
        <!-- TODO: Show volume details on hovering volume -->

        <!-- https://medium.com/@rmmmsy/creating-and-animating-a-modal-component-as-a-child-route-using-vue-41a275a51d0c -->
        <button class="add">Add Children</button> <!-- TODO: Add children modal -->
        <button class="edit">Edit</button> <!-- TODO: Edit item modal -->
        <button class="delete">Delete</button> <!-- TODO: Delete item -->
      </div>
      <item-list v-if="item.expanded" v-bind:parent="item.id"/>
    </li>
  </ul>
</template>

<script lang="ts">
import {defineComponent} from 'vue';

type Item = {
  title: string,
  childCount: number,
  value?: string,
  weight?: string,
  volume?: string,
  totalValue?: string,
  totalWeight?: string,
  totalVolume?: string,
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
      fetch(`http://localhost:5000/items/${this.parent}`).then(response => response.json())
          .then(data => this.items = data.items);
    },
    lt(a: string | null, b: string | null): boolean {
      return a !== null && b !== null && parseFloat(a) < parseFloat(b);
    },
  },
  created() {
    this.load();
  },
});
</script>

<style scoped lang="scss">

</style>