<template>
  <div>
    <h1>Analyse du graphe des photos</h1>
    <p>
      Tout les calculs sont fait en local, sur votre ordinateur en web assembly.
    </p>
    <div class='box stats-box'>
      <h3>Statistiques</h3>
      <ul>
        <li>Nombre de photos: {{ nbNodes }}</li>
      </ul>
    </div>
    <button @click='computeSizeInWasm'>Compute Size in wasm</button>
    <button @click='computeSizeInWasm'>Compute Size in js</button>
  </div>
</template>

<script>

export default {
  name: 'GraphAnalyzer',
  components: { },
  methods: {
    computeSizeInWasm() {
      console.log('Computing size in wasm');
      console.log(this.indexesGraph.flat());
      const graph = this.wasm.Graph.new(this.nbNodes, 5, this.indexesGraph.flat());
      const t0 = performance.now();
      console.log(graph.random_walk(100000));
      const t1 = performance.now();
      console.log("Call to doSomething took " + (t1 - t0) + " milliseconds.")
    },
    computeInJs() {
      console.log('Computing size in wasm');
      const graph = this.indexesGraph.flat();
      const t0 = performance.now();
      let current_node = Math.floor(Math.random()*this.nbNodes);
      for (let k = 0; k < 100000; k++) {
        current_node = graph[current_node*this.nbNodes + Math.floor(Math.random()*5)];
      }
      console.log(current_node);
      const t1 = performance.now();
      console.log("Call to doSomething took " + (t1 - t0) + " milliseconds.")
    },
  },
  computed: {
    nbNodes() {
      return Object.keys(this.$store.state.graph).length;
    },
    idToIndex() {
      const keys = Object.keys(this.$store.state.graph);
      const idToIndex = {};
      for (let index = 0; index < keys.length; index++) {
        idToIndex[keys[index]] = index;
      }
      return idToIndex;
    },
    indexesGraph() {
      const graph = this.$store.state.graph;
      const indexesGraph = [];
      for (let nodeId in graph) {
        const neighborsId = graph[nodeId];
        indexesGraph.push(neighborsId.map((id) => this.idToIndex[id]));
      }
      return indexesGraph;
    }
  },
  async beforeMount() {
    this.$store.dispatch('FETCH_WHOLE_GRAPH');

    this.wasm = await require('wasm-graph-analyzer');
    //this.wasm.greet();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#network {
  height: 100vh;
}
</style>
