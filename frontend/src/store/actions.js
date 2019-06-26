import { fetchNeigborsForImageId } from '../api';

export default {
  FETCH_NEIGHBORS: ( { commit,  state, dispatch }, imageId) => {
    return new Promise((resolve, reject) => {
      fetchNeigborsForImageId(imageId).then((edges) => {

        // TODO remove
        edges.forEach((edge) => {
          commit('SET_NODES', {
            nodes: [
              { id: edge.from, shape: 'image', image: '/data/images_full/' + edge.from + '.jpg', size:'35' }, // label: 'Image ' + edge.to,
              { id: edge.to, shape: 'image', image: '/data/images_full/' + edge.to + '.jpg', size:'35' }
            ]});
        });
        commit('SET_EDGES', { edges });
        resolve(edges);
      }).catch(({code, error}) => {
        if (code == 401) dispatch('LOGOUT');
        reject(error);
      });
    });
  },

  // TODO remove
  FETCH_NODES: ({ commit, state, dispatch }) => {
    return new Promise((resolve, reject) => {
      const nodes = [
        { id: '1', shape: 'image', image: '/data/images_full/1.jpg' }
      ];
      commit('SET_NODES', { nodes });
      resolve(nodes);
    });
  },
  // TODO remove
  FETCH_EDGES: ( { commit, state, dispatch }) => {
    return new Promise((resolve, reject) => {
      const edges = [/*
       { id: '1_3', from: 1, to: 3 },
       { id: '1_2', from: 1, to: 2 },
       { id: '2_4', from: 2, to: 4 },
       { id: '2_5', from: 2, to: 5 },
       { id: '3_3', from: 3, to: 3 }*/
     ];
     commit('SET_EDGES', { edges });
     resolve(edges);
    });
  },

}
