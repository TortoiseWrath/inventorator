<template>
  <!-- TODO: Warn when navigating away from an item with unsaved changes -->
  <article @keyup="handleKeypress">
    <div class="photos">
      <camera :photoShortcut="photoShortcut" :barcodeShortcut="barcodeShortcut"
              @photo="addPhoto" @barcode="(upc) => item.upc = upc"/>
      <draggable v-model="item.photos">
        <div v-for="(path, key) in item.photos" :key="key">
          <thumbnail :path="path" :key="key"
                     @enlarge="enlargedPhoto = key" @delete="photoToDelete = key"/>
          <!-- TODO: Separate thumbnail-sized images -->
        </div>
      </draggable>
      <modal v-if="photoToDelete !== null" @cancel="photoToDelete = null" @confirm="deletePhoto">
        Are you sure you want to delete this image?
        <br>
        <img :src="`http://localhost:5000/photo/${item.photos[photoToDelete]}`"
             class="delete" alt="${item.photos[photoToDelete]}"/>
      </modal>
      <!-- TODO: Enlarged photo carousel modal -->
    </div>
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
        <input v-model="item.title" maxlength="255" ref="title"/>
      </label>
      <label class="description"><span>Description</span>
        <textarea v-model="item.description" maxlength="65535"/>
      </label>
      <label class="acquired"><span>Acquired</span>
        <date-string-selector v-model="item.acquired"/>
      </label>
      <label class="basis"><span>Cost basis</span>
        <input v-model="item.basis" maxlength="11" pattern="\d*(\.\d*)?"/>
      </label>
      <label class="value"><span>Value</span>
        <input v-model="item.value" maxlength="11" pattern="\d*(\.\d*)?"/>
        <!-- TODO: Allow arithmetic expressions in item editor -->
      </label>
      <label class="valueAsOf"><span>as of</span>
        <date-string-selector v-model="item.valueAsOf"/>
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
        <div>Volume: {{ item.d1 * item.d2 * item.d3 || '' }}</div> <!-- TODO: Use a computed property for volume -->
      </fieldset>
      <label class="upc"><span>UPC</span>
        <input v-model="item.upc" maxlength="255" pattern="[0-9 ]+"/>
        <!-- TODO: Add barcode scanner to item editor -->
      </label>
    </div>
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
  </article>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
// import {FontAwesomeIcon} from '@/plugins/font-awesome';
import {ItemDetails} from '@/types/ItemDetails';
import {Item} from '@/types/Item';
import DateStringSelector from '@/components/DateStringSelector.vue';
import Camera from '@/components/Camera.vue';
import {VueDraggableNext} from 'vue-draggable-next';
import Thumbnail from '@/components/Thumbnail.vue';
import Modal from '@/components/Modal.vue';
import {useToast} from 'vue-toastification';

export default defineComponent({
  name: 'ItemEditor',
  data() {
    return {
      item: {parent: this.parent ? parseInt(this.parent) : 2} as ItemDetails,
      allItems: [] as Item[],
      enlargedPhoto: null as number | null,
      photoToDelete: null as number | null,
      toast: useToast(),
      photoShortcut: 0, // Track how many times the photo button has been pressed. Changes -> take photo.
      barcodeShortcut: 0, // ditto
    };
  },
  components: {
    Thumbnail,
    Camera,
    // FontAwesomeIcon,
    DateStringSelector,
    draggable: VueDraggableNext,
    Modal,
  },
  props: {
    id: String,
    parent: String,
  },
  emits: {
    upload(details: ItemDetails) {
      return !!details;
    },
    right(details: ItemDetails) {
      return !!details;
    },
    down(details: ItemDetails) {
      return !!details;
    },
    up(details: ItemDetails) {
      return !!details;
    },
  },
  methods: {
    load() {
      if (this.id) {
        fetch(`http://localhost:5000/item/${this.id}`)
            .then(response => response.json())
            .then(data => this.item = data.item);
      }
      fetch('http://localhost:5000/items').then(response => response.json())
          .then(data => this.allItems = data.items);
    },
    uploadItem() {
      this.$emit('upload', this.item);
    },
    navRight() {
      this.$emit('right', this.item);
    },
    navDown() {
      this.$emit('down', this.item);
    },
    navUp() {
      this.$emit('up', this.item);
    },
    focusTitle() {
      const titleInput = this.$refs.title as HTMLInputElement;
      titleInput.focus();
    },
    addPhoto(path: string) {
      this.item.photos ??= [];
      this.item.photos.push(path);
    },
    modal(path: string) {
      console.log('Show modal for ' + path);
    },
    async deletePhoto() {
      if (this.photoToDelete === null || !this.item?.photos || !this.item.photos[this.photoToDelete]) {
        this.toast.error('Tried to delete nothing?');
        return;
      }
      try {
        const response: Response = await fetch(
            `http://localhost:5000/photo/${this.item.photos[this.photoToDelete]}`, {method: 'DELETE'});
        const json = await response.json();
        if (!response.ok) {
          console.error(response);
          console.error(json);
          this.toast.error(json.error.join(' '));
        } else {
          this.toast.info('Deleted photo', {timeout: 1000});
          this.item.photos.splice(this.photoToDelete, 1);
          this.photoToDelete = null;
        }
      } catch (e) {
        console.error(e);
        this.toast.error(e.message);
      }
    },
    handleKeypress(e: KeyboardEvent) {
      console.log(e);
      switch (e.code) {
        case 'F13':
          this.barcodeShortcut++;
          break;
        case 'F14':
          this.navUp();
          break;
        case 'F15':
          this.navDown();
          break;
        case 'F16':
          this.navRight();
          break;
        case 'F17':
          this.photoShortcut++;
          break;
      }
    },
  },
  created() {
    this.load();
  },
  mounted() {
    this.focusTitle();
  },
});
</script>

<style scoped lang="scss">
// TODO: Style the item editor
img.delete {
  max-width: calc(100vw - 5em);
  max-height: calc(100vw - 5em);
  margin-top: 1em;
}
</style>