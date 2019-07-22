<template>
  <div class='bottom-fixed-navbar'>
    <ul class='tools-list'>
      <li class='tool-button tooltip' title="Retourner au graphe">
        <button @click='goHome()'><font-awesome-icon size='2x' icon="home"/></button>
      </li>
      <li class='tool-button tooltip' title="Se deconnecter">
        <button @click='signOut()'><font-awesome-icon size='2x' icon="sign-out-alt"/></button>
      </li>
      <li class='tool-button tooltip' title="Populer le graphe automatiquement">
        <button @click='populate()'><font-awesome-icon size='2x' icon="robot"/></button>
      </li>
      <li class='tool-button tooltip' title="Charger une image aléatoirement">
        <button @click='randomImage()'><font-awesome-icon size='2x' icon="dice"/></button>
      </li>
      <li class='tool-button tooltip' title="Modifier les tags de cette image">
        <button @click='editImage()'><font-awesome-icon size='2x' icon="edit"/></button>
      </li>
      <li class='tool-button tooltip' title="Ouvrir la marche aléatoire">
        <button @click='goWalk()'><font-awesome-icon size='2x' icon="hiking"/></button>
      </li>
      <li class='tool-button tooltip' title="Partager cette photo">
        <button @click='shareImage()'><font-awesome-icon size='2x' icon="share-alt"/></button>
      </li>
      <li class='tool-button tooltip' title="Une interrogation ?">
        <button @click='showHelp()'><font-awesome-icon size='2x' icon="question"/></button>
      </li>
      <li class='tool-button tooltip' title="Quelques statistiques">
        <button @click='goStatistics()'><font-awesome-icon size='2x' icon="info"/></button>
      </li>
    </ul>
  </div>
</template>

<script>

export default {
  name: 'p-picture-tools',
  methods: {
    goHome: function() {
      this.$router.push({ name: 'home' });
    },
    goWalk: function() {
      this.$emit('go-walk');
    },
    signOut: function() {
      this.$router.push({ name: 'login' });
    },
    goStatistics: function() {
      this.$router.push({ name: 'analyze' });
    },
    showHelp: function() {
      this.emit('help');
    },
    shareImage: function() {
      this.$emit('share-image');
    },
    editImage: function() {
      this.$emit('edit-image');
    },
    populate: function() {
      alert('populate');
    },
    randomImage: function() {
      this.$emit('random-image');
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.bottom-fixed-navbar{
  position: fixed;
  bottom: 15px;
  right: 15px;
  /* width: 100%; */
  overflow: hidden;
  z-index: 1;
}

button {
	border-radius: 100%;
	display: inline-block;
	height: 50px;
	width: 50px;
	background: #fefefe;
	border: none;
}

.tools-list {
  list-style: none;
}

.tool-button {
  margin-top: 10px;
  margin-bottom: 10px;
}

.tools-list {
	list-style: none;
	padding: 15px;
	margin: 0;
  width: 200px;
  text-align: right;
}

.tooltip{
    display: block;
    position: relative;
}

.tooltip:hover:after{
    background: #fefefe;
    border-radius: 5px;
    color: #111;
    content: attr(title);
    right: 61px;
    top: 10px;
    padding: 5px 15px;
    position: absolute;
    z-index: 98;
    width: auto;
    text-align:center;
    font-size: 13px;
}

.tooltip:hover::before {
	border: solid;
	border-color: transparent #fefefe;
	border-width: 7px 0px 7px 7px;
	top: 20px;
	content: "";
	right: 55px;
	position: absolute;
	z-index: 99;
}

</style>
