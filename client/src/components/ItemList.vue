<template>
  <ul>
    <li v-for="(item, index) in items" :key="index">
      <div class="left">

        <font-awesome-icon icon="caret-right" v-if="item.childCount"
                           @click="item.expanded = !item.expanded"
                           :class="item.expanded ? 'collapse' : 'expand'"/>
        <div v-if="!item.childCount" class="spacer"/>
        <!-- @todo Add hover transition to buttons -->
        <!-- @todo Add rotation transition to expand/collapse buttons -->

        <!-- @todo Add checkboxes to items list -->

        <img :src="`http://localhost:5000/photo/${item.photo}`" v-if="item.photo" :alt="item.title"/>

        <div class="title">{{ item.title }}</div>
      </div>
      <div class="right">
        <div :class="['childCount', {'decorated': item.childCount}]">{{ item.childCount }}</div>

        <div :class="['value', {'decorated': item.totalValue}]">{{ item.totalValue }}</div>
        <!-- @todo Show value details on hovering value -->

        <div :class="['weight', {'warning': lt(item.weight, item.totalWeight), 'decorated': item.weight}]">
          {{ item.weight }} <!-- @todo Add weight conversions -->
        </div>
        <!-- @todo Show weight details on hovering weight -->

        <div :class="['volume', {'warning': lt(item.volume, item.totalVolume), 'decorated': item.volume}]">
          {{ item.volume }} <!-- @todo Add volume conversions -->
        </div>
        <!-- @todo Show volume details on hovering volume -->

        <router-link :to="{ path: `/add/${item.id}`}">
          <font-awesome-icon icon="plus" class="add"/>
        </router-link>
        <router-link :to="{ path: `/item/${item.id}`}">
          <font-awesome-icon icon="pen" class="edit"/>
        </router-link>
        <font-awesome-icon icon="trash-alt" class="delete" @click="item.showModal = true"/>
        <!-- @todo Add tooltips to buttons -->
      </div>
      <item-list v-if="item.expanded != null" v-show="item.expanded" :parent="item.id"
                 @deletedChildren="(count, value) => {
                   item.childCount -= count;
                   if (item.totalValue && value) {
                     item.totalValue = (parseFloat(item.totalValue) - parseFloat(value)).toString();
                   }
                   if (!item.childCount) {
                     item.expanded = false;
                   }
                   $emit('deletedChildren', 0, value);
                 }"/>
      <!-- @todo Add transition for show/hide children -->
      <modal v-if="item.showModal" @cancel="item.showModal = false" @confirm="deleteItem(item, items, index)">
        Are you sure you want to delete
        {{
          (item.title ? item.title : 'item id ' + item.id) +
          (item.childCount ? ` and its ${item.childCount} ${item.childCount > 1 ? 'children' : 'child'}?` : '?')
        }}
      </modal>
    </li>
  </ul>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {FontAwesomeIcon} from '@/plugins/font-awesome';
import {Item} from '@/types/Item';
import Modal from '@/components/Modal.vue';
import {useToast} from 'vue-toastification';

export default defineComponent({
  name: 'ItemList',
  data() {
    return {
      items: [] as Item[],
      toast: useToast(),
    };
  },
  emits: ['deletedChildren'],
  components: {
    Modal,
    FontAwesomeIcon,
  },
  props: {
    parent: {
      type: Number,
      required: true,
    },
    expand: {
      type: Boolean,
      required: false,
    },
  },
  methods: {
    load() {
      fetch(`http://localhost:5000/items/${this.parent}`).then(response => response.json())
          .then(data => {
            this.items = data.items;
            if (this.expand && this.items[0]?.childCount) {
              this.items[0].expanded = true;
            }
          });
    },
    lt(a: string | null, b: string | null): boolean {
      return a !== null && b !== null && parseFloat(a) < parseFloat(b);
    },
    async deleteItem(item: Item, itemArray: Item[], itemIndex: number) {
      try {
        const response: Response = await fetch(`http://localhost:5000/item/${item.id}`, {method: 'DELETE'});
        const json = await response.json();
        if (!response.ok) {
          console.error(response);
          console.error(json);
          this.toast.error(json.error.join(' '));
        } else {
          item.showModal = false;
          const count = 1;
          const value = item.totalValue;
          itemArray.splice(itemIndex, 1);
          this.$emit('deletedChildren', count, value);
        }
      } catch (e) {
        console.error(e);
        this.toast.error(e.message);
      }
    },
  },
  created() {
    this.load();
  },
});
</script>

<style scoped lang="scss">
$indent: 1em;
$child-count-width: 4em;
$decimal-width: 8em;
$right-width: 6 * $indent + $child-count-width + 3 * $decimal-width;
$indent-ratio: 0.67; // Adjust to make the lines look like they line up with the arrows
// @todo Hide decimals on mobile

ul {
  list-style: none;
  display: inline-block;
  background-color: $debug-background;
  padding-left: $indent * $indent-ratio;
  width: 100%;
  max-width: 13in;
  box-sizing: border-box;

  > li {
    display: block;
    width: 100%;
    text-align: left;
    border-left: 1px solid #aaa;
    box-sizing: border-box;
    padding-left: $indent * (1 - $indent-ratio);

    &:hover {
      background-color: #aaa3;
    }

    > div {
      height: 3rem;
      vertical-align: top;
      display: inline-flex;
      align-items: center;

      div {
        margin-bottom: -.3em; // Shift text down slightly to account for space below baseline
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      > * {
        display: inline-block;
      }

      &.left {
        width: calc(100% - #{$indent} - #{$right-width});

        .expand, .collapse, div.spacer {
          width: $indent * 1.5;
          height: $indent * 1.5;
          vertical-align: middle;
          flex-shrink: 0;
        }

        .collapse {
          transform: rotate(90deg);
        }

        .expand, .collapse {
          &:hover {
            cursor: pointer;
            color: $hover;
          }
        }

        img {
          max-height: calc(100% - 0.3rem);
          margin-right: 0.3rem;
        }
      }

      &.left:hover + .right, &.right:hover {
        .add, .edit, .delete {
          opacity: 1; // @todo Add a transition to fade buttons in/out on hover
        }
      }

      &.right {
        width: $right-width;
        justify-content: flex-end;

        .add, .edit, .delete {
          height: $indent;
          margin-left: $indent;
          flex-shrink: 0;
          opacity: 0;
          color: $body;

          &:hover { // @todo Make sure hover is usable on mobile
            cursor: pointer;
            color: $hover;
          }
        }

        .delete {
          color: $danger;

          &:hover {
            color: $danger-hover;
          }
        }

        > div {
          width: $decimal-width;
          text-align: right;

          &.childCount {
            width: $child-count-width;
          }

          &.decorated {
            &.childCount::before {
              content: "+";
            }

            &.value::before {
              content: "$";
            }

            &.weight::after {
              content: " oz";
            }

            &.volume::after {
              content: " in³";
            }
          }
        }
      }
    }
  }
}
</style>