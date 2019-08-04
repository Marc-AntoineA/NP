<template>
  <div id='login-view'>
    <div class='login-box'>

        <h1>Se Connecter</h1>

        <div v-if='infoText.text' class='info-box' v-bind:class="{ 'error': infoText.type === 'error', 'success': infoText.type === 'success' }">
          {{ infoText.text }}
        </div>

        <div class='input-container'>
          <font-awesome-icon size='1x' icon="user" class='white'/>
          <input v-model='username' type="text" placeholder="Votre addresse email" name="username" required/>
        </div>

        <div class='input-container'>
          <font-awesome-icon size='1x' icon="lock" class='white'/>
          <input v-model='password' type="password" placeholder="Votre mot de passe" name="password" required/>
        </div>

        <button type='submit' @click='onSubmit' class='loaded'><span>Me connecter</span></button>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Login',
  props: {},
  data: () => ({
    username: '',
    password: '',
    loading: false,
    infoText: {
      text: '',
      type: 'error'
    }
  }),
  methods: {
    onSubmit(event) {
      if (!this.username || !this.password) {
        this.infoText.text = "Veuiller renseigner votre addresse email ainsi que votre mot de passe.";
        this.infoText.type = 'error';
        return;
      }
      this.$store.dispatch('LOGIN', { username: this.username, password: this.password }).then(() => {
        this.$router.push('/');
      }).catch((error) => {
        this.infoText.text = error;
        this.infoText.type = 'error';
      });
    }
  },
  mounted() {
    console.log(this.$store.getters.isLoggedIn);
    if (!this.$store.getters.isLoggedIn) return;
    this.$store.dispatch('LOGOUT').then(() => {
      this.infoText.text = "Vous êtes désormais déconnecté.";
      this.infoText.type = 'success';
    });
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.login-box input {
  font-size: 16px;
  color: #fff;
  line-height: 1.2;
  width: calc(100% - 30px);
  height: 45px;
  background: 0 0;
  padding: 0 5px 0 10px;
  border: none;
}

.login-box button {
  width: 100%;
  height: 50px;
  margin: 40px 0px 10px 0px;
  background: white;
  border: none;
  font-size: 16px;
  font-weight: bold;
  color: #646464;
}

.login-box span:after {
  content: '\00bb';
  position: absolute;
  opacity: 0;
  top: 0;
  right: -20px;
  transition: 0.5s;
}

.login-box span {
  cursor: pointer;
  display: inline-block;
  position: relative;
  transition: 0.5s;
}

.login-box:hover span {
  padding-right: 25px;
}

.login-box:hover span:after {
  opacity: 1;
  right: 0;
}

.login-box h1 {
  font-size: 30px;
  color: #fff;
  line-height: 1.2;
  text-align: center;
  text-transform: uppercase;
  display: block;
}

.login-box {
  width: 500px;
  border-radius: 10px;
  overflow: hidden;
  padding: 55px 55px 37px;
  background: -moz-linear-gradient(top,#00416A,#E4E5E6);
}

#login-view {
  display: -webkit-box;
  display: -webkit-flex;
  display: -moz-box;
  display: -ms-flexbox;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  position: absolute;
  width: 100vw;
  min-height: 100vh;
  background-image: url('../../public/background.png');
  z-index: 1;
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
}

#login-view::before {
    content: "";
    display: block;
    position: absolute;
    z-index: -1;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    background-color: rgba(1, 61, 100, 0.4);
}

.input-container {
  width: 100%;
  padding: 10px 4px;
  border-bottom: 3px solid white;
  margin-bottom: 5px;
}

.white {
  color: white;
}

.info-box {
  padding: 15px;
  color: white;
}

.info-box.error {
  background-color: rgba(192, 57, 43, 0.8);
}

.info-box.success {
  background-color: rgba(52,152,219, 0.8);
}
</style>
