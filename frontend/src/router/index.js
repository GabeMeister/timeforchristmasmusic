import Vue from 'vue';
import Router from 'vue-router';
import SongList from '@/components/SongList';
import Song from '@/components/Song';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'SongList',
      component: SongList
    },
    {
        path: '/song/:url',
        name: 'Song',
        component: Song
    }
  ]
});
