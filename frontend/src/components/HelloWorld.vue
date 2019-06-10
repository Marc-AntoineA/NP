<template>
  <div class="hello">
    <h1>Tentatives</h1>
    <div ref='visualization'></div>
  </div>
</template>

<script>
import { DataSet, Network } from 'visjs-network';

export default {
  name: 'HelloWorld',
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

    const options = {};
    new Network(container, data, options);
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
