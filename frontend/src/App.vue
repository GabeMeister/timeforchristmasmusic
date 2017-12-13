<template>
  <div id="app">
    <button @click="handleClick">Click Me</button>
    <router-view/>
  </div>
</template>

<script>
import Vue from 'vue';
import axios from 'axios';

export default {
  name: 'app',
  methods: {
      handleClick: function() {
        axios.get(Vue.config.baseUrl+'/songlist')
          .then(response => {
            console.log('response: ', response.data);
          })
          .catch(error => {
            console.log('error: ', error);
          });
      }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
