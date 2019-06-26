<template>
  <div class='fixed-search-header'>
    <h1>Header</h1>
  </div>
</template>

<script>

export default {
  name: 'p-search-header'
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.fixed-search-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  overflow: hidden;
  z-index: 1;
  border-bottom: solid black 3px;
  background-color: lightgray;
}
</style>
