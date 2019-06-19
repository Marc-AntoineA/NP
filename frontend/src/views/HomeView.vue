<template>
  <div>
    <!--<h1>Home View 3</h1>-->
    <p-network id='network'/>
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
  beforeMount() {
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#network {
  height: 100vh;
}
</style>
