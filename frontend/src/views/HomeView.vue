<template>
  <div>
    <!-- <p-search-header/> -->
    <p-network id='network' :nodes='nodes' :edges='edges'
      @node-selection='onNodeSelection' @edge-selection='onEdgeSelection'
      @node-double-selection='onNodeDoubleSelection' @edge-double-selection='onEdgeDoubleSelection'
      @node-deselection='onNodeDeselection'/>
    <p-picture-tools :displayed='displayed' :populationDelay='5000'
      @go-walk='goWalk()' @edit-image='editImage()' @random-image='randomImage()' @populate='populate()'/>
  </div>
</template>

<script>

import PNetwork from '../components/Network.vue';
import PSearchHeader from '../components/SearchHeader.vue';
import PPictureTools from '../components/PictureTools.vue';

export default {
  name: 'Home',
  components: { PNetwork, PSearchHeader, PPictureTools },
  data: () => ({
    selectedNode: undefined,
    displayed: ['signout', 'help', 'stats', 'random', 'populate', 'clean']
  }),
  methods: {
    onNodeSelection: function(imageId) {
      this.selectedNode = imageId
      this.displayed.push('edit');
      this.displayed.push('walk');
      this.displayed.push('share');
    },
    onNodeDeselection: function(nodeIds) {
      if (nodeIds.length === 0) return;
      if (nodeIds.indexOf(this.selectedNode) === -1) return;
      this.selectedNode = '';
      this.displayed.splice(this.displayed.indexOf('edit'), 1);
      this.displayed.splice(this.displayed.indexOf('walk'), 1);
      this.displayed.splice(this.displayed.indexOf('share'), 1);
    },
    onEdgeSelection: function(edgeId) {
      console.log('Selected edge ', edgeId);
    },
    onNodeDoubleSelection: function(imageId) {
      console.log('Db clicked on ', imageId);
      this.$store.dispatch('FETCH_NEIGHBORS', imageId);
      console.log(this.$store.getters.TAGS_NETWORK);
    },
    onEdgeDoubleSelection: function(edgeId) {
      console.log('Db clicked on ', edgeId);
    },
    goWalk: function() {
      this.$router.push({ name: 'walk', params: { pictureId: this.selectedNode }});
    },
    editImage: function() {
      this.$router.push({ name: 'edit', params: { pictureId: this.selectedNode }});
    },
    randomImage: function() {
      this.$store.dispatch('FETCH_RANDOM_PICTURE').then((node) => {
        this.$store.dispatch('FETCH_NEIGHBORS', node.id);
      });
    },
    populate: function() {
      const lessConnectedNodeId = this.$store.getters.lessConnectedPictures;
      this.$store.dispatch('FETCH_NEIGHBORS', lessConnectedNodeId);
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
  background-color: #111;
}

</style>
