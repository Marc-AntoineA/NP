<template>
  <div>
    <p-search-header/>
    <p-network id='network' :nodes='nodes' :edges='edges'
      @node-selection='onNodeSelection' @edge-selection='onEdgeSelection'
      @node-double-selection='onNodeDoubleSelection' @edge-double-selection='onEdgeDoubleSelection'/>
    <p-picture-tools/>
  </div>
</template>

<script>

import PNetwork from '../components/Network.vue';
import PSearchHeader from '../components/SearchHeader.vue';
import PPictureTools from '../components/PictureTools.vue';

export default {
  name: 'Home',
  components: { PNetwork, PSearchHeader, PPictureTools },
  methods: {
    onSubmit() {
    }
  },
  methods: {
    onNodeSelection: function(imageId) {
      console.log('Selected node ', imageId);
    },
    onEdgeSelection: function(edgeId) {
      console.log('Selected edge ', edgeId);
    },
    onNodeDoubleSelection: function(imageId) {
      console.log('Db clicked on ', imageId);
      this.$store.dispatch('FETCH_NEIGHBORS', imageId);
    },
    onEdgeDoubleSelection: function(edgeId) {
      console.log('Db clicked on ', edgeId);
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
    this.$store.dispatch('FETCH_RANDOM_PICTURE');
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#network {
  height: 100vh;
}
</style>
