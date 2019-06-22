

export default {
  FETCH_NODES: ({ commit, state, dispatch }) => {
    return new Promise((resolve, reject) => {
      const nodes = [
        { id: 1, label: 'Node 1' },
        { id: 2, label: 'Node 2' },
        { id: 3, label: 'Node 3' },
        { id: 4, label: 'Node 4' },
        { id: 5, label: 'Node 5' }
      ];
      commit('SET_NODES', { nodes });
      resolve(nodes);
    });
  },
  FETCH_EDGES: ( { commit, state, dispatch }) => {
    return new Promise((resolve, reject) => {
      const edges = [
       { id: '1_3', from: 1, to: 3 },
       { id: '1_2', from: 1, to: 2 },
       { id: '2_4', from: 2, to: 4 },
       { id: '2_5', from: 2, to: 5 },
       { id: '3_3', from: 3, to: 3 }
     ];
     commit('SET_EDGES', { edges });
     resolve(edges);
    });
  }
}
