export default {
  neighbors: (state, getters) => (pictureId) => {
    const edges = Object.values(state.edges).filter((edge) => edge.to === pictureId || edge.from === pictureId);
    return edges.map((edge) => edge.from === pictureId ? edge.to : edge.from);
  },
  token: (state, getters) => {
    return state.user.token;
  },
  isLoggedIn: (state, getters) => {
    return state.user.token !== '' && state.user.username !== '';
  },
  lessConnectedPictures: (state, getters) => {
    const edges = Object.values(state.edges);
    const nbNeighbors = {};
    for (let nodeId in state.nodes) {
      nbNeighbors[nodeId] = edges.reduce((acc, value) => {
        if (value.from === nodeId || value.to === nodeId)
          return acc + 1;
        return acc;
      }, 0);
    }

    const minNeighbors = Math.min(...Object.values(nbNeighbors));
    for (let nodeId in nbNeighbors) {
      if (nbNeighbors[nodeId] === minNeighbors)
        return nodeId;
    }
    return undefined;
  }
}
