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
    <button @click='computeInJs'>Compute Size in js</button>
    <ul>
      <li v-for='(picture, index) in picturesFrequencies'>
        {{ index }} --- 
        <span>{{ picture.nbTimes }}</span>
        <img :src='"http://192.168.2.119/thumbnails/" + picture.id + ".jpg"'/>
        <a :href='"/walk/" + picture.id' target='_blank'>Walk</a>
      </li>
    </ul>
    <p-picture-tools :displayed="['home']"/>
  </div>
</template>

<script>

import PPictureTools from '../components/PictureTools.vue';

export default {
  name: 'GraphAnalyzer',
  components: { PPictureTools },
  data: () => ({
    picturesFrequencies: {
      type: Array,
      default: []
    }
  }),
  methods: {
    computeSizeInWasm() {
      console.log('Computing size in wasm');
      console.log(this.indexesGraph.flat());
      const graph = this.wasm.Graph.new(this.nbNodes, 5, this.indexesGraph.flat());
      const t0 = performance.now();
      const nbTimes_visited_nodes = graph.random_walk(10000);
      const ids = Object.keys(this.$store.state.graph);
      let nbTimes_with_image_id = ids.map((id, index) => {
        return { 'id': id, 'nbTimes': nbTimes_visited_nodes[index] };
      });
      nbTimes_with_image_id = nbTimes_with_image_id.sort((a, b) => (a.nbTimes > b.nbTimes));
      this.picturesFrequencies = nbTimes_with_image_id;
      const t1 = performance.now();
      console.log("Call to doSomething took " + (t1 - t0) + " milliseconds.")
    },
    computeInJs() {
      console.log('Computing size in js');
      const graph = this.indexesGraph.flat();
      const t0 = performance.now();
      const visited = [];
      for (let k = 0; k < this.nbNodes; k++)
        visited.push(0);

      let current_node = Math.floor(Math.random()*this.nbNodes);
      visited[current_node]++;
      for (let k = 0; k < 10000000; k++) {
        current_node = graph[current_node*5 + Math.floor(Math.random()*5)];
        visited[current_node]++;
      }
      console.log(visited);
      console.log(current_node);
      const t1 = performance.now();
      console.log("Call to js took " + (t1 - t0) + " milliseconds.")
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
