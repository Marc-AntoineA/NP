<template>
  <div class='bottom-fixed-navbar'>
    <h1>Picture Tools</h1>
  </div>
</template>

<script>

export default {
  name: 'p-picture-tools'
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.bottom-fixed-navbar{
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  overflow: hidden;
  z-index: 1;
  border-top: solid black 3px;
  background-color: lightgray;
}
</style>
