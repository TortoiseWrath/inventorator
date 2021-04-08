<template>
  <!-- @todo Add a transition to the modal -->
  <!-- @todo Add Esc and Enter keybindings -->
  <div class="container" @click.self="$emit('cancel')">
    <div class="modal">
      <div class="body">
        <slot>
          Are you sure?
        </slot>
      </div>
      <div class="buttons">
        <button class="confirm" @click="$emit('confirm')">Confirm</button>
        <button class="cancel" @click="$emit('cancel')">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent} from 'vue';

export default defineComponent({
  name: 'Modal',
  emits: ['cancel', 'confirm'],
});
</script>

<style scoped lang="scss">
div.container {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 3;
  width: 100%;
  height: 100%;
  background-color: #0003;
  display: flex;
  justify-content: center;
  align-items: center;

}

div.modal {
  background-color: #fffffff6;
  padding: 1rem;
  border-radius: 0.5rem;
  border: 1px solid $danger;
}

div.buttons {
  display: flex;
  justify-content: space-evenly;
}

button {
  margin-top: 1rem;
  font-size: 120%;
  padding: 0.2em 0.6em;

  &.confirm {
    color: $danger;
  }
}
// @todo Improve modal styling
</style>