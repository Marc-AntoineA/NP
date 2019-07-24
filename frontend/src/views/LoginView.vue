<template>
  <div class='login-box'>
      <label for="username">Adresse email</label>
      <input v-model='username' type="text" placeholder="Votre addresse email" name="username" required/>

      <label for="password">Mot de passe</label>
      <input v-model='password' type="password" placeholder="Votre mot de passe" name="password" required/>

      <button type='submit' @click='onSubmit'>Me connecter</button>
  </div>
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
    onSubmit(event) {
      this.$store.dispatch('LOGIN', { username: this.username, password: this.password }).then((connected) => {
        if (!connected) return;
        this.$router.push('/');
        alert('Vous êtes désormais connecté');
      });
    }
  },
  mounted() {
    console.log(this.$store.getters.isLoggedIn);
    if (!this.$store.getters.isLoggedIn) return;
    this.$store.dispatch('LOGOUT');
    alert('Vous êtes maintenant deconnecté');
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.login-box input {
	display: block;
	width: 100%;
	margin-bottom: 10px;
}

.login-box label {
  display: block;
}

.login-box button {
  padding: 7px 13px;
  background-color: white;
  border: 2px solid #222;
  border-radius: 10%;
}

.login-box {
	max-width: 330px;
	border: 3px solid #666;
	padding: 30px;
	margin: 80px auto;
	text-align: center;
	background-color: #dedede;
	box-shadow: 4px 5px 8px #444;
}
</style>
