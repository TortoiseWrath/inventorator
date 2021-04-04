<template>
  <div>
    <button @click="ping()">{{ msg }}</button>
  </div>
</template>

<script lang="ts">
import {defineComponent} from 'vue';

export default defineComponent({
  name: 'Ping',
  data() {
    return {
      msg: 'henlo',
    };
  },
  methods: {
    ping() {
      fetch('http://localhost:5000/ping').then(response => response.json()).then(data => this.msg = data.data);
    },
  },
});
</script>

<style scoped>

</style>