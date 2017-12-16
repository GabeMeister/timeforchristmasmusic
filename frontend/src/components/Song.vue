<template>
  <div class="song">
    <h1 v-text="name"></h1>
    <div v-for="line in lyrics" :key="line">
      <div v-if="line === ''">
        <br/>
      </div>
      <div v-if="line !== ''" v-text="line"></div>
    </div>
    <router-link to="/"><h2>Back to Song List</h2></router-link>
  </div>
</template>

<script>
import Vue from 'vue';
import axios from 'axios';

export default {
  name: 'Song',
  data () {
    return {
      msg: '',
      name: '',
      lyrics: ''
    }
  },
  created: function() {
    this.getSongData();
  },
  methods: {
      getSongData: function() {
        axios.get(Vue.config.baseUrl+'/song/'+this.$route.params.url)
          .then(response => {
            this.name = response.data.name;
            this.lyrics = response.data.lyrics;
            console.log('assigned lyrics: ', this.lyrics);
          })
          .catch(error => {
            console.log('error: ', error);
          });
      }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: bold;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
  text-decoration: none;
}
</style>
