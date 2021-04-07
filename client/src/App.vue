<template>
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
