<template>
  <div id="nav">
    <router-link to="/items">Items</router-link>
    |
    <router-link to="/add/2">Add Item</router-link>
  </div>
  <router-view/>
</template>

<style lang="scss">
html {
  background-color: $background;
  color: $body;
}

#app {
  font-family: Helvetica, Arial, sans-serif;
  text-align: center;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
