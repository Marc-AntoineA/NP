<template>
    <div ref='visualization'></div>
</template>

<script>
import { DataSet, Network } from 'visjs-network';

export default {
  name: 'p-network',
  props: {
    msg: String
  },
  mounted() {
    // create an array with nodes
    const nodes = new DataSet([
      { id: 1, label: 'Node 1' },
      { id: 2, label: 'Node 2' },
      { id: 3, label: 'Node 3' },
      { id: 4, label: 'Node 4' },
      { id: 5, label: 'Node 5' }
    ]);

    // create an array with edges
    const edges = new DataSet([
      { from: 1, to: 3 },
      { from: 1, to: 2 },
      { from: 2, to: 4 },
      { from: 2, to: 5 },
      { from: 3, to: 3 }
    ]);

    // create a network
    const container = this.$refs.visualization;
    var data = {
      nodes: nodes,
      edges: edges
    };

    const options = {
      toResize: true,
      height: '100%',
      width: '100%'
    };
    new Network(container, data, options);
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
