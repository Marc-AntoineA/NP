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
}
