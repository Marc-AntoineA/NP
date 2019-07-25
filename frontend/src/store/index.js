import Vue from 'vue';
import Vuex from 'vuex';
import actions from './actions';
import getters from './getters';
import mutations from './mutations';

Vue.use(Vuex);

export function createStore() {
  return new Vuex.Store({
    state: {
      nodes: {/* [id: String]: Process */},
      edges: {/* {from: id, to: id}*/},
      tags: {/* {id, [] }*/},
      options: [],
      graph: {},
      user: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : { usename: '', token: ''},
      lessTaggedPictures: {},
    },
    actions,
    mutations,
    getters
  });
}
