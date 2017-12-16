<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'app'
}
</script>

<style>
html {
  height: 100%;
}

body {
  min-height: 100%;
  background-image: url("https://i.imgur.com/xK568Mx.png");
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  padding-top: 50px;
  padding-bottom: 50px;
  min-height: 100%;
}
</style>
