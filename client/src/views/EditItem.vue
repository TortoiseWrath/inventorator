<template>
  <div class="details">
    <label class="parent"><span>Parent</span>
      <select v-model="item.parent">
        <!-- TODO: Make a hierarchical item menu -->
        <!-- TODO: Prevent moving an item to one of its own descendants -->
        <option v-for="item in allItems" :key="item.message" :value="item.id">
          {{ item.title }}
        </option>
      </select>
    </label>
    <label class="title"><span>Title</span>
      <input v-model="item.title" maxlength="255"/>
    </label>
    <label class="description"><span>Description</span>
      <textarea v-model="item.description" maxlength="65535"/>
    </label>
    <label class="acquired"><span>Acquired</span>
      <input v-model="item.acquired"/> <!-- TODO: Use date inputs in item editor -->
    </label>
    <label class="basis"><span>Cost basis</span>
      <input v-model="item.basis" maxlength="11" pattern="\d*(\.\d*)?"/>
    </label>
    <label class="value"><span>Value</span>
      <input v-model="item.value" maxlength="11" pattern="\d*(\.\d*)?"/>
      <!-- TODO: Allow arithmetic expressions in item editor -->
    </label>
    <label class="valueAsOf"><span>as of</span>
      <input v-model="item.valueAsOf"/>
    </label>
    <label class="weight"><span>Weight</span>
      <input v-model="item.weight" maxlength="11" pattern="\d*(\.\d*)?"/>
    </label>
    <fieldset class="dimensions">
      <legend>Dimensions</legend>
      <label><span>L</span>
        <input v-model="item.d1" maxlength="11" pattern="\d*(\.\d*)?"/>
      </label>
      <label><span>W</span>
        <input v-model="item.d2" maxlength="11" pattern="\d*(\.\d*)?"/>
      </label>
      <label><span>H</span>
        <input v-model="item.d3" maxlength="11" pattern="\d*(\.\d*)?"/>
      </label>
    </fieldset>
    <label class="upc"><span>UPC</span>
      <input v-model="item.upc" maxlength="255" pattern="[\d ]+"/>
      <!-- TODO: Add barcode scanner to item editor -->
    </label></div>
  <div class="buttons">
    <button @click="uploadItem()">Save</button>
    <button @click="navRight()">Add sibling</button>
    <button @click="navDown()">Add child</button>
    <button @click="navUp()">Edit parent</button>
  </div>
  <aside>
    <p>Item created: {{ item.created }}</p>
    <p>Last modified: {{ item.modified }}</p>
  </aside>
  <!-- TODO: Add photos to item editor -->
  <!-- TODO: Add links to item editor -->
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {FontAwesomeIcon} from '@/plugins/font-awesome';
import {ItemDetails} from '@/types/ItemDetails';
import {Item} from '@/types/Item';

export default defineComponent({
  name: 'EditItem',
  data() {
    return {
      item: {} as ItemDetails,
      allItems: [] as Item[],
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
      fetch('http://localhost:5000/items').then(response => response.json())
          .then(data => this.allItems = data.items);
    },
    uploadItem(): boolean {
      console.log('Submit');
      fetch(`http://localhost:5000/item/${this.item.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.item),
      }).then(response => response.json()).then(data => console.log(data));
      // TODO: handle errors when updating item
      return true;
    },
    navRight() {
      if (!this.uploadItem()) return;
      console.log('navRight');
    },
    navDown() {
      if (!this.uploadItem()) return;
      console.log('navDown');
    },
    navUp() {
      if (!this.uploadItem()) return;
      console.log('navUp');
    },
  },
  created() {
    this.load();
  },
});
</script>

<style scoped lang="scss">

</style>