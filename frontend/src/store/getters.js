export default {
  TAGS_NETWORK: (state, getters) => {
    const nodes = {};
    const edges = {};

    for (let pictureId in state.tags) {
      const tags = state.tags[pictureId];
      tags.forEach((tag) => {
        if (nodes[tag] === undefined)
          nodes[tag] = { id: tag, label: tag, value: 0, shape: 'dot' };
        nodes[tag].value++;
      });

      /*for (let fromTagIndex in tags) {
        const fromTag = tags[fromTagIndex];
        for (let toTagIndex in tags) {
          const toTag = tags[toTagIndex];
          if (fromTag <= toTag) continue;

          const edgeId = fromTag + '__' + toTag;
          if (edges[edgeId] == undefined)
            edges[edgeId] = { id: edgeId, from: fromTag, to: toTag, value: 0}
          edges[edgeId].value++;
        }
      }

      for (let edge in edges) {
        //if (edge.value < 5)
          delete edges[edge.id];
      }*/
    }
    return { nodes, edges };
  }
}
