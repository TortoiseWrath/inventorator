<template>
  <ul>
    <li v-for="(item, index) in items" :key="index">
      <div class="left">

        <font-awesome-icon icon="caret-right" v-if="item.childCount"
                           @click="item.expanded = !item.expanded"
                           :class="item.expanded ? 'collapse' : 'expand'"/>
        <div v-if="!item.childCount" class="spacer"/>
        <!-- TODO: Add hover transition to buttons -->
        <!-- TODO: Add rotation transition to expand/collapse buttons -->

        <!-- TODO: Add checkboxes to items list -->
        <!-- TODO: Add photo preview to items list -->

        <div class="title">{{ item.title }}</div>
      </div>
      <div class="right">
        <div :class="['childCount', {'decorated': item.childCount}]">{{ item.childCount }}</div>

        <div :class="['value', {'decorated': item.totalValue}]">{{ item.totalValue }}</div>
        <!-- TODO: Show value details on hovering value -->

        <div :class="['weight', {'warning': lt(item.weight, item.totalWeight), 'decorated': item.weight}]">
          {{ item.weight }} <!-- TODO: Add weight conversions -->
        </div>
        <!-- TODO: Show weight details on hovering weight -->

        <div :class="['volume', {'warning': lt(item.volume, item.totalVolume), 'decorated': item.volume}]">
          {{ item.volume }} <!-- TODO: Add volume conversions -->
        </div>
        <!-- TODO: Show volume details on hovering volume -->

        <router-link :to="{ path: `/add/${item.id}`}">
          <font-awesome-icon icon="plus" class="add"/>
        </router-link>
        <router-link :to="{ path: `/item/${item.id}`}">
          <font-awesome-icon icon="pen" class="edit"/>
        </router-link>
        <font-awesome-icon icon="trash-alt" class="delete"/> <!-- TODO: Delete item modal -->
        <!-- TODO: Add tooltips to buttons -->
      </div>
      <item-list v-if="item.expanded != null" v-show="item.expanded" :parent="item.id"/>
      <!-- TODO: Add transition for show/hide children -->
    </li>
  </ul>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {FontAwesomeIcon} from '@/plugins/font-awesome';
import {Item} from '@/types/Item';
import {Decimal} from '@/types/Decimal';

export default defineComponent({
  name: 'ItemList',
  data() {
    return {
      items: [] as Item[],
    };
  },
  components: {
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
    lt(a: Decimal | null, b: Decimal | null): boolean {
      return a !== null && b !== null && a.value() < b.value();
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
$extra-width: 2 * $indent;
$right-width: 6 * $indent + $extra-width + $child-count-width + 3 * $decimal-width;
// TODO: Hide decimals on mobile

ul {
  list-style: none;
  display: inline-block;
  background-color: $debug-background;
  padding-left: $indent;
  width: 100%;
  max-width: 13in;
  box-sizing: border-box;

  > li {
    display: block;
    width: 100%;
    text-align: left;

    > div {
      height: 2rem;
      vertical-align: top;
      display: inline-flex;
      align-items: center;

      div {
        margin-bottom: -.3em; // Shift text down slightly to account for space below baseline
        overflow: hidden;
        text-overflow: ellipsis;
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
      }

      &.left:hover + .right, &.right:hover {
        .add, .edit, .delete {
          opacity: 1; // TODO: Add a transition to fade buttons in/out on hover
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

          &:hover { // TODO: Make sure hover is usable on mobile
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