<template>
  <div class='background'>
    <router-link class='close-button' :to="{ name: 'home'}">
      <font-awesome-icon class='close-icon' icon="times" size='2x'/>
    </router-link>
    <p-spinner class='center' :show="loading"></p-spinner>
    <div v-if='!loading' class='picture-view'>
      <img class='image-full' :src='pictureFullUrl'/>
      <ul class='images-preview'>
        <li v-if='!loadingPreviews' v-for='neighborId in neighbors'>
          <router-link :to="{ name: 'walk', params: { pictureId: neighborId }}">
            <img class='image-thumbnail' :src='"http://localhost/thumbnails/" + neighborId + ".jpg"'/>
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>

import PSpinner from '../components/Spinner.vue';

export default {
  name: 'Walk',
  props: {},
  components: {
    PSpinner
  },
  data: () => ({
    loading: true,
    loadingPreviews: true
  }),
  computed: {
    pictureId() {
      return this.$route.params.pictureId;
    },
    pictureFullUrl() {
      return 'http://192.168.2.119' + '/full/' + this.pictureId + '.jpg';
    },
    tags() {
      return this.$store.state.tags[this.pictureId];
    },
    options() {
      console.log(this.$store.state.options);
      return this.$store.state.options;
    },
    neighbors() {
      return this.$store.getters.neighbors(this.pictureId).slice(0, 5);
    }
  },
  methods: {

  },
  beforeRouteUpdate(to, from, next) {
    console.log(to);
    console.log(from);
    this.loadingPreviews = true;
    console.log(to.params.pictureId);
    this.$store.dispatch('FETCH_NEIGHBORS', to.params.pictureId).then(() => {
      this.loadingPreviews = false;

    });
    next();
  },
  beforeMount() {
    this.loading = true;
    this.loadingPreviews = true;
    this.$store.dispatch('FETCH_NEIGHBORS', this.$route.params.pictureId).then(() => {
      this.loadingPreviews = false;
      this.loading = false;
    });

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.image-full {
  max-height: calc(100vh - 120px);
  max-width: 95vw;
  margin-bottom: 5px;
}

.images-preview li {
  display: inline-block;
  margin: 0px 4px;
}

.images-preview {
  margin: 5px;
}

.image-thumbnail {
  height: 90px;
}

.background {
  height: 100vh;
  width: 100vw;
  margin: 0;
  position: absolute;
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
  background-color: black;
}

.center {
  position: absolute;
  top: 48vh;
}

.close-button {
  position: absolute;
  right: 30px;
  top: 20px;
}
</style>
