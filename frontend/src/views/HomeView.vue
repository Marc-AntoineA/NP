<template>
  <div>
    <!--<h1>Home View 3</h1>-->
    <p-network id='network' :nodes='nodes' :edges='edges'
      @node-selection='onNodeSelection' @edge-selection='onEdgeSelection'/>
  </div>
</template>

<script>

import PNetwork from '../components/Network.vue';

export default {
  name: 'Home',
  components: { PNetwork },
  methods: {
    onSubmit() {
    }
  },
  methods: {
    onNodeSelection: function(nodeId) {
      console.log('Selected node ', nodeId);
    },
    onEdgeSelection: function(edgeId) {
      console.log('Selected edge ', edgeId);
    }
  },
  computed: {
    nodes: function () {
      return Object.values(this.$store.state.nodes);
    },
    edges: function() {
      return Object.values(this.$store.state.edges);
    }
  },
  beforeMount() {
    this.$store.dispatch('FETCH_NODES');
    this.$store.dispatch('FETCH_EDGES');
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#network {
  height: 100vh;
}
</style>
