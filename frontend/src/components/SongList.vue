<template>
  <div class="song-list">
    <h1 v-text="msg"></h1>
    <router-link :to="'/song/' + song.url" v-for="song in songs" :key="song.url">
        <h2 v-text="song.name"></h2>
    </router-link>
  </div>
</template>

<script>
import Vue from 'vue';
import axios from 'axios';

export default {
  name: 'Song',
  data () {
    return {
      msg: 'Pick a Christmas Song!',
      songs: []
    }
  },
  created: function() {
      this.getSongList();
  },
  methods: {
      getSongList: function() {
          axios.get(Vue.config.baseUrl+'/songlist')
            .then(response => {
                this.songs = response.data;
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
