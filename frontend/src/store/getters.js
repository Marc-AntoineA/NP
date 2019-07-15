export default {
  neighbors: (state, getters) => (pictureId) => {
    const edges = Object.values(state.edges).filter((edge) => edge.to === pictureId || edge.from === pictureId);
    return edges.map((edge) => edge.from === pictureId ? edge.to : edge.from);
  }
}
