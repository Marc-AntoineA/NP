    <template>
    <div ref='visualization'></div>
</template>

<script>
import { DataSet, Network } from 'visjs-network';

export default {
  name: 'p-network',
  props: {
    msg: String,
    nodes: Array,
    edges: Array
  },
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

    new Network(container, data, options);
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
