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

    fetch('/data/database.json')
    .then((response) => response.json())
    .then((data) => {

      const nodes_list = [];
      const list_edges = [];
      for (let image_index = 0; image_index < 40; image_index++) {
        const image = data[image_index];
        const id = image.Name;
        nodes_list.push({
          id: id,
          shape: 'image',
          label: 'Image ' + id,
          image: '/data/images_full/' + id + '.jpg'
        });
        let nb = 0;
        const values = Object.values(image);
        for (let image_bis_index = image_index + 1; image_bis_index < 40; image_bis_index++) {
          const bis_image = data[image_bis_index];
          const bis_values = Object.values(bis_image);
          if (nb > 8) break;
          let count = 0;
          for (let k = 0; k < bis_values.length; k++) {
            if (bis_values[k] === '') continue;
            if (bis_values[k] === values[k]) {
              count++;
            }
            if (count > 3) {
              list_edges.push({ from: image.Name, to: bis_image.Name });
              nb++;
              break;
            }
          }
        }
      }

      const nodes = new DataSet(nodes_list);
      const edges = new DataSet(list_edges);

      // create a network
      const container = this.$refs.visualization;
      var data = {
        nodes: nodes,
        edges: edges
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
    });
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
