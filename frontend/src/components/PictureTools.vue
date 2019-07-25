<template>
  <div>
    <div class='bottom-fixed-navbar'>
      <ul class='tools-list'>
        <li v-if='displayed.indexOf("home") !== -1' class='tool-button tooltip' title="Retourner au graphe">
          <button @click='goHome()'><font-awesome-icon size='2x' icon="home"/></button>
        </li>
        <li v-if='displayed.indexOf("signout") !== -1' class='tool-button tooltip' title="Se deconnecter">
          <button @click='signOut()'><font-awesome-icon size='2x' icon="sign-out-alt"/></button>
        </li>
        <li v-if='displayed.indexOf("populate") !== -1' class='tool-button tooltip' v-bind:class="{ 'automated-mode': automatedMode }"
         title="Peupler le graphe automatiquement">
          <button @click='handlePopulate()'><font-awesome-icon size='2x' icon="robot"/></button>
        </li>
        <li v-if='displayed.indexOf("random") !== -1' class='tool-button tooltip' title="Charger une image aléatoirement">
          <button @click='randomImage()'><font-awesome-icon size='2x' icon="dice"/></button>
        </li>
        <li v-if='displayed.indexOf("clean") !== -1' class='tool-button tooltip' title="Nettoyer le graphe">
          <button @click='clean()'><font-awesome-icon size='2x' icon="broom"/></button>
        </li>
        <li v-if='displayed.indexOf("edit") !== -1' class='tool-button tooltip' title="Modifier les tags de cette image">
          <button @click='editImage()'><font-awesome-icon size='2x' icon="edit"/></button>
        </li>
        <li v-if='displayed.indexOf("walk") !== -1' class='tool-button tooltip' title="Ouvrir la marche aléatoire">
          <button @click='goWalk()'><font-awesome-icon size='2x' icon="hiking"/></button>
        </li>
        <li v-if='displayed.indexOf("share") !== -1' class='tool-button tooltip' title="Partager cette photo">
          <button @click='shareImage()'><font-awesome-icon size='2x' icon="share-alt"/></button>
        </li>
        <li v-if='displayed.indexOf("help") !== -1' class='tool-button tooltip' title="Une interrogation ?">
          <button @click='showHelp()'><font-awesome-icon size='2x' icon="question"/></button>
        </li>
        <li v-if='displayed.indexOf("stats") !== -1' class='tool-button tooltip' title="Quelques statistiques">
          <button @click='goStatistics()'><font-awesome-icon size='2x' icon="info"/></button>
        </li>
      </ul>
    </div>
    <div class='progress-bar' :style='"width:" + this.automatedProgress + "%"'/>
  </div>
</template>

<script>

export default {
  name: 'p-picture-tools',
  props: {
    displayed: Array,
    populationDelay: {
      type: Number,
      default: 5000
    }
  },
  data: () => ({
    automatedMode: false,
    automatedProgress: 0
  }),
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
    handlePopulate: function() {
      this.automatedMode = !this.automatedMode;
      if (this.automatedMode)
        this.populate();
      else
        this.automatedProgress = 0;
    },
    populate: function() {
      this.automatedProgress = 1;
      this.incrProgress();
      setTimeout(() => {
        if (!this.automatedMode) return;
        this.$emit('populate');
        this.populate();
      }, this.populationDelay);
    },
    incrProgress: function() {
      if (this.automatedProgress === 0) return;
      if (this.automatedProgress >= 98) return;
      this.automatedProgress += 1;
      setTimeout(() => {
        this.incrProgress();
      }, this.populationDelay/100.);
    },
    randomImage: function() {
      this.$emit('random-image');
    },
    clean() {
      this.$store.dispatch('RESET_GRAPH').then(() => {
        this.$store.dispatch('FETCH_RANDOM_PICTURE');
      });
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

.automated-mode path {
  color: blue;
}

.progress-bar {
  height: 4px;
  background-color: white;
  margin: auto;
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  border-radius: 3px;
}

</style>
