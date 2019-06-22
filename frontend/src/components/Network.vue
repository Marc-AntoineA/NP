    <template>
    <div ref='visualization'></div>
</template>

<script>
import { DataSet, Network } from 'visjs-network';

export default {
  name: 'p-network',
  props: {
    nodes: Array,
    msg: String,
    edges: Array,
  },
  data: () => ({

  }),
  mounted() {
    // create a network
    const container = this.$refs.visualization;
    var data = {
      nodes: new DataSet(this.nodes),
      edges: new DataSet(this.edges)
    };

    const options = {
      autoResize: true,
      height: '100%',
      width: '100%',
      nodes: {
        shapeProperties: {
          useBorderWithImage:true
        }
      }
    };

    const network = new Network(container, data, options);

    const self = this;
    network.on('click', function(params) {
      const selectedNodes = params.nodes;
      const selectedEdges = params.edges;
      if (selectedNodes.length === 1) {
        self.$emit('node-selection', selectedNodes[0])
      } else if (selectedEdges.length == 1) {
        self.$emit('edge-selection', selectedEdges[0]);
      } else {
        throw new Error('Unknown click event');
      }
    });
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
