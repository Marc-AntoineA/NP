import Vue from 'vue';

export default {
  SET_EDGES: (state, { edges }) => {
    edges.forEach((edge) => {
      Vue.set(state.edges, edge.id, edge);
    });
  },
  SET_NODES: (state, { nodes }) => {
    nodes.forEach((node) => {
      Vue.set(state.nodes, node.id, node);
    })
  },
  SET_TAGS: (state, { tags,  pictureId }) => {
    Vue.set(state.tags, pictureId, tags);
  },
  ADD_TAG: (state, { tag, pictureId }) => {
    Vue.set(state.tags[pictureId], state.tags[pictureId].length, tag);
  },
  SET_OPTIONS: (state, tags) => {
    state.options = tags;
  },
  ADD_OPTION: (state, tag) => {
    Vue.set(state.options, state.options.length, tag);
  },
  SET_GRAPH: (state, graph) => {
    state.graph = graph;
  },
  SET_USER: (state, { username, token }) => {
    Vue.set(state.user, 'username', username);
    Vue.set(state.user, 'token', token);
  },
  REMOVE_USER: (state) => {
    Vue.set(state.user, 'username', '');
    Vue.set(state.user, 'token', '');
  },
  RESET_GRAPH: (state) => {
    state.nodes = {};
    state.edges = {};
    state.tags = {};
  },
  SET_LESS_TAGGED_PICTURES: (state, pictures) => {
    state.lessTaggedPictures = pictures;
  }
}
