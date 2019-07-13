import {
  fetchNeigborsForPictureId,
  fetchTagsForPictureId,
  postTagsForPictureId,
  fetchAllTags,
  fetchRandomPicture
 } from '../api';

export default {
  FETCH_NEIGHBORS: ( { commit,  state, dispatch }, pictureId) => {
    return new Promise((resolve, reject) => {
      fetchNeigborsForPictureId(pictureId).then((edges) => {

        // TODO remove
        edges.forEach((edge) => {
          commit('SET_NODES', {
            nodes: [
              { id: edge.from, shape: 'image', image: 'http://localhost/thumbnails/' + edge.from + '.jpg', size:'35' }, // label: 'Image ' + edge.to,
              { id: edge.to, shape: 'image', image: 'http://localhost/thumbnails/' + edge.to + '.jpg', size:'35' }
            ]});
        });
        commit('SET_EDGES', { edges });
        resolve(edges);
      }).catch(({ code, error}) => {
        if (code == 401) dispatch('LOGOUT');
        reject(error);
      });
    });
  },
  FETCH_TAGS: ({ commit, state, dispatch }, pictureId) => {
    return new Promise((resolve, reject) => {
      fetchTagsForPictureId(pictureId)
      .then((tags) => {
        commit('SET_TAGS', { pictureId, tags });
        resolve(tags);
      }).catch(({ code, error}) => {
        if (code == 401) dispatch('LOGOUT');
        reject(error);
      });
    });
  },
  UPDATE_TAGS: ({ commit, state, dispatch }, { pictureId, tags }) => {
    return new Promise((resolve, reject) => {
      postTagsForPictureId(pictureId, tags)
      .then((tags) => {
        commit('SET_TAGS', { pictureId, tags });
        resolve(tags);
      }).catch(({ code, error }) => {
        if (code == 401) dispatch('LOGOUT');
        reject(error);
      });
    });
  },
  ADD_TAG: ({ commit, state, dispatch }, { pictureId, tag }) => {
    return new Promise((resolve, reject) => {
      commit('ADD_TAG', { pictureId, tag });
      postTagsForPictureId(pictureId, state.tags[pictureId])
      .then((tags) => {
        commit('SET_TAGS', { pictureId, tags });
        resolve(tags);
      }).catch(({ code, error }) => {
        if (code == 401) dispatch('LOGOUT');
        reject(error);
      });
    });
  },
  FETCH_OPTIONS: ({ commit, state, dispatch }) => {
    return new Promise((resolve, reject) => {
      fetchAllTags()
      .then((tags) => {
        commit('SET_OPTIONS', tags);
        resolve(tags);
      }).catch(({ code, error }) => {
        if (code == 401) dispatch('LOGOUT');
        reject(error);
      });
    });
  },
  // TODO remove
  FETCH_RANDOM_PICTURE: ({ commit, state, dispatch }) => {
    return new Promise((resolve, reject) => {
      fetchRandomPicture()
      .then((picture) => {
        const node = { id: picture.id, shape: 'image', image: 'http://localhost/thumbnails/' + picture.id + '.jpg', size: '35'};
        commit('SET_NODES', { nodes: [node] });
        resolve(nodes);
      }).catch(({ code, error }) => {
        if (code == 401) dispatch('LOGOUT');
        reject(error);
      });
    });
  }
}