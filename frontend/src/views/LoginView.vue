<template>
  <h1>Login View</h1>
</template>

<script>

export default {
  name: 'Login',
  props: {},
  data: () => ({
    username: '',
    password: '',
    loading: false
  }),
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
.boxed {
  margin: 50px auto;
  border: 2px solid teal;
  background-color: #f0efef;
  width: 330px;
  box-shadow: 0px 6px 4px #004c4c;
}

.boxed img {
  width: 65%;
}
</style>
