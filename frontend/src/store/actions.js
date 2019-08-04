import {
  fetchNeigborsForPictureId,
  fetchTagsForPictureId,
  postTagsForPictureId,
  fetchAllTags,
  fetchRandomPicture,
  fetchWholeGraph,
  fetchLessTaggedPictures
 } from '../api';

export default {
  FETCH_NEIGHBORS: ( { commit,  state, dispatch, getters }, pictureId) => {
    return new Promise((resolve, reject) => {
      fetchNeigborsForPictureId(pictureId).then((edges) => {

        // TODO remove
        edges.forEach((edge) => {

          const newPictureId = edge.from === pictureId ? edge.to  : edge.from;

          commit('SET_NODES', {
            nodes: [
              { id: newPictureId, shape: 'image', image: getters.thumbnailUrl(newPictureId), size:'35', color:'#fefefe' }
            ]
          });

          commit('SET_TAGS', { pictureId: newPictureId, tags: edge.tags_new_node });
          delete edge.tags_new_node;
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
  FETCH_RANDOM_PICTURE: ({ commit, state, dispatch, getters }) => {
    return new Promise((resolve, reject) => {
      fetchRandomPicture()
      .then((picture) => {
        const tags = picture.tags;
        commit('SET_TAGS', { pictureId: picture.id, tags: tags });
        const node = { id: picture.id, shape: 'image', image: getters.thumbnailUrl(picture.id) , size: '35', color: '#fefefe'};
        commit('SET_NODES', { nodes: [node] });
        resolve(node);
      }).catch(({ code, error }) => {
        if (code == 401) dispatch('LOGOUT');
        reject(error);
      });
    });
  },
  FETCH_WHOLE_GRAPH: ({ commit, state, dispatch }) => {
    return new Promise((resolve, reject) => {
      fetchWholeGraph()
      .then((graph) => {
        commit('SET_GRAPH', graph);
        resolve();
      }).catch(({ code, error }) => {
        if (code == 401) dispatch('LOGOUT');
        reject(error);
      });
    });
  },
  LOGIN: ({ commit, state, dispatch }, { username, password }) => {
    return new Promise((resolve, reject) => {
      // todo
      const token = 'auieauie';
      localStorage.setItem('user', JSON.stringify({ username, token }));
      commit('SET_USER', { username, token });
      resolve(true);
    });
  },
  LOGOUT: ({ commit, state, dispatch }) => {
    return new Promise((resolve, reject) => {
      localStorage.removeItem('user');
      commit('REMOVE_USER');
      resolve();
    });
  },
  RESET_GRAPH: ({ commit, state, dispatch }) => {
    return new Promise((resolve, reject) => {
      commit('RESET_GRAPH')
      resolve();
    });
  },
  FETCH_LESS_TAGGED_PICTURES: ({ commit, state, dispatch }) => {
    return new Promise((resolve, reject) => {
      fetchLessTaggedPictures()
      .then((pictures) => {
        commit('SET_LESS_TAGGED_PICTURES', pictures);
        resolve();
      }).catch(({ code, error }) => {
        if (code == 401) dispatch('LOGOUT');
        reject(error);
      });
    });
  },
}
