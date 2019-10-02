import {
  fetchNeigborsForPictureId,
  fetchTagsForPictureId,
  postTagsForPictureId,
  fetchAllTags,
  fetchRandomPicture,
  fetchWholeGraph,
  fetchLessTaggedPictures,
  fetchToken,
  refreshToken,
  uploadPicture
 } from '../api';

export default {
  FETCH_NEIGHBORS: ( { commit,  state, dispatch, getters }, pictureId) => {
    return new Promise((resolve, reject) => {
      fetchNeigborsForPictureId(pictureId, state.user.token).then((edges) => {
        edges.forEach((edge) => {
          const newPictureId = edge.from === pictureId ? edge.to  : edge.from;
          commit('SET_NODES', {
            nodes: [{ id: newPictureId, shape: 'image', image: getters.thumbnailUrl(newPictureId), size:'35', color:'#fefefe' }]
          });
          commit('SET_TAGS', { pictureId: newPictureId, tags: edge.tags_new_node });
          delete edge.tags_new_node;
        });
        commit('SET_EDGES', { edges });
        resolve(edges);
      }).catch(({ code, error}) => {
        if (code == 401) {
          dispatch('REFRESH_TOKEN').then(() => {
            dispatch('FETCH_NEIGHBORS', pictureId)
            .then((edges) => {
              resolve(edges);
            }).catch(({ error }) => {
              reject(error)
            });
          });
          return;
        }
        reject(error);
      });
    });
  },
  FETCH_TAGS: ({ commit, state, dispatch }, pictureId) => {
    return new Promise((resolve, reject) => {
      fetchTagsForPictureId(pictureId, state.user.token)
      .then((tags) => {
        commit('SET_TAGS', { pictureId, tags });
        resolve(tags);
      }).catch(({ code, error}) => {
        if (code == 401) {
          dispatch('REFRESH_TOKEN').then(() => {
            dispatch('FETCH_TAGS', pictureId)
            .then((tags) => resolve(tags))
            .catch(({ error }) => reject(error));
          });
          return;
        }
        reject(error);
      });
    });
  },
  UPDATE_TAGS: ({ commit, state, dispatch }, { pictureId, tags }) => {
    return new Promise((resolve, reject) => {
      postTagsForPictureId(pictureId, tags, state.user.token)
      .then((tags) => {
        commit('SET_TAGS', { pictureId, tags });
        resolve(tags);
      }).catch(({ code, error }) => {
        if (code == 401) {
          dispatch('REFRESH_TOKEN').then(() => {
            dispatch('UPDATE_TAGS', { pictureId, tags })
            .then((tags) => resolve(tags))
            .catch(({ error }) => reject(error));
          });
          return;
        }
        reject(error);
      });
    });
  },
  ADD_TAG: ({ commit, state, dispatch }, { pictureId, tag }) => {
    return new Promise((resolve, reject) => {
      commit('ADD_TAG', { pictureId, tag });
      postTagsForPictureId(pictureId, state.tags[pictureId], state.user.token)
      .then((tags) => {
        commit('SET_TAGS', { pictureId, tags });
        resolve(tags);
      }).catch(({ code, error }) => {
        if (code == 401) {
          dispatch('REFRESH_TOKEN').then(() => {
            dispatch('FETCH_TAGS', { pictureId, tag })
            .then((tags) => resolve(tags))
            .catch(({ error }) => reject(error));
          });
          return;
        }
        reject(error);
      });
    });
  },
  FETCH_OPTIONS: ({ commit, state, dispatch }) => {
    return new Promise((resolve, reject) => {
      fetchAllTags(state.user.token)
      .then((tags) => {
        commit('SET_OPTIONS', tags);
        resolve(tags);
      }).catch(({ code, error }) => {
        if (code == 401) {
          dispatch('REFRESH_TOKEN').then(() => {
            dispatch('FETCH_OPTIONS')
            .then((tags) => resolve(tags))
            .catch(({ error }) => reject(error));
          });
          return;
        }
        reject(error);
      });
    });
  },
  FETCH_RANDOM_PICTURE: ({ commit, state, dispatch, getters }) => {
    return new Promise((resolve, reject) => {
      fetchRandomPicture(state.user.token)
      .then((picture) => {
        const tags = picture.tags;
        commit('SET_TAGS', { pictureId: picture.id, tags: tags });
        const node = { id: picture.id, shape: 'image', image: getters.thumbnailUrl(picture.id) , size: '35', color: '#fefefe'};
        commit('SET_NODES', { nodes: [node] });
        resolve(node);
      }).catch(({ code, error }) => {
        if (code == 401) {
          dispatch('REFRESH_TOKEN').then(() => {
            dispatch('FETCH_RANDOM_PICTURE')
            .then((nodes) => resolve(nodes))
            .catch(({ error }) => reject(error));
          });
          return;
        }
        reject(error);
      });
    });
  },
  FETCH_WHOLE_GRAPH: ({ commit, state, dispatch }) => {
    return new Promise((resolve, reject) => {
      fetchWholeGraph(state.user.token)
      .then((graph) => {
        commit('SET_GRAPH', graph);
        resolve();
      }).catch(({ code, error }) => {
        if (code == 401) {
          dispatch('REFRESH_TOKEN').then(() => {
            dispatch('FETCH_WHOLE_GRAPH')
            .then(() => resolve())
            .catch(({ error }) => reject(error));
          });
          return;
        }
        reject(error);
      });
    });
  },
  LOGIN: ({ commit, state, dispatch }, { username, password }) => {
    return new Promise((resolve, reject) => {
      fetchToken({ username, password })
      .then((token) => {
        localStorage.setItem('user', JSON.stringify({ username, token }));
        commit('SET_USER', { username, token });
        resolve(true);
      }).catch(({ code, error }) => {
        if (code == 401) dispatch('LOGOUT');
        reject(error);
      });
    });
  },
  REFRESH_TOKEN: ({ commit, state, dispatch }) => {
    return new Promise((resolve, reject) => {
      refreshToken(state.user.token)
      .then(({ access }) => {
        commit('SET_ACCESS_TOKEN', access);
        localStorage.setItem('user', JSON.stringify(state.user));
        resolve(true);
      }).catch(({ code, error }) => {
        if (code == 401) dispatch('LOGOUT');
        reject(error);
      });
    });
  },
  LOGOUT: ({ commit, state, dispatch }) => {
    return new Promise((resolve, reject) => {
      localStorage.removeItem('user');
      commit('REMOVE_USER');
      commit('CLEAR_STATE');
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
      fetchLessTaggedPictures(state.user.token)
      .then((pictures) => {
        commit('SET_LESS_TAGGED_PICTURES', pictures);
        resolve();
      }).catch(({ code, error }) => {
        if (code == 401) {
          dispatch('REFRESH_TOKEN').then(() => {
            dispatch('FETCH_LESS_TAGGED_PICTURES')
            .then(() => resolve())
            .catch(({ error }) => reject(error));
          });
          return;
        }
        reject(error);
      });
    });
  },
  UPLOAD_PICTURE: ({ commit, state, dispatch }, picture) => {
    return new Promise((resolve, reject) => {
      uploadPicture(state.user.token, picture)
      .then(() => {
        resolve();
      }).catch(({ code, error }) => {
        if (code == 401) {
          dispatch('REFRESH_TOKEN').then(() => {
            dispatch('FETCH_LESS_TAGGED_PICTURES')
            .then(() => resolve())
            .catch(({ error }) => reject(error));
          });
          return;
        }
        reject(error);
      });
    });
  }
}
