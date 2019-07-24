<template>
  <div class='background'>
    <p-spinner class='center' :show="loading"></p-spinner>
    <div v-if='!loading' class='picture-view'>
      <div class='full-image-preview'>
        <img class='image-full' :class='{opaque: !transitionState }' :src='pictureFullUrl'/>
        <img class='image-full' :class='{opaque: transitionState }' :src='nextPictureUrl'/>
      </div>
      <ul class='images-preview'>
        <li v-if='displayPreviews' v-for='neighborId in neighbors'>
          <img class='image-thumbnail' :src='"http://localhost/thumbnails/" + neighborId + ".jpg"'
            @click='selectPicture(neighborId)' :class='{opaque: !loadingPreviews }'/>
        </li>
      </ul>
    </div>

    <p-picture-tools :displayed="['home', 'random', 'populate', 'edit', 'help', 'stats', 'home', 'share', 'signout']"
      :automatedMode='automatedMode'
      @random-image='loadRandomImage()' @populate='handleRandomWalk()' @edit-image='editImage()'/>
  </div>
</template>

<script>
import PPictureTools from '../components/PictureTools.vue';
import PSpinner from '../components/Spinner.vue';

export default {
  name: 'Walk',
  props: {},
  components: {
    PSpinner,
    PPictureTools
  },
  data: () => ({
    loading: true,
    loadingPreviews: true,
    automatedMode: false,
    nextPictureUrl: '',
    transitionState: false,
    displayPreviews: false
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
    loadRandomImage() {
      this.$store.dispatch('FETCH_RANDOM_PICTURE').then((node) => {
        const pictureId = node.id;
        this.$router.push({ name: 'walk', params: { pictureId: pictureId }});
      });
    },
    handleRandomWalk() {
      this.automatedMode = !this.automatedMode;
      if (this.automatedMode) this.randomWalk();
    },
    randomWalk() {
      setTimeout(() => {
        console.log(this.automatedMode);
        if (!this.automatedMode) return;
        const randomPictureIndex = Math.floor(Math.random()*this.neighbors.length);
        const nodeId = this.neighbors[randomPictureIndex];
          this.$router.push({ name: 'walk', params: { pictureId: nodeId }});
        this.randomWalk();
      }, 10000);
    },
    selectPicture(pictureId) {
      this.$router.push({ name: 'walk', params: { pictureId }});
    },
    editImage() {
      this.$router.push({ name: 'edit', params: { pictureId: this.pictureId }});
    }
  },
  beforeRouteUpdate(to, from, next) {
    this.transitionState = true;
    this.displayPreviews = false;
    this.loadingPreviews = true;
    this.nextPictureUrl = 'http://192.168.2.119' + '/full/' + to.params.pictureId + '.jpg';
    setTimeout(() => {
      this.$store.dispatch('FETCH_NEIGHBORS', to.params.pictureId).then(() => {
        this.displayPreviews = true;
        setTimeout(() => { this.loadingPreviews = false; }, 300);
        this.transitionState = false;
      });
      next();
    }, 400);
  },
  beforeMount() {
    this.loading = true;
    this.displayPreviews = false;
    this.loadingPreviews = true;
    this.$store.dispatch('FETCH_NEIGHBORS', this.$route.params.pictureId).then(() => {
      setTimeout(() => { this.loadingPreviews = false; }, 300);;
      this.displayPreviews = true;
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
background-color: #111;
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


.full-image-preview {
  position:relative;
  height: calc(100vh - 120px);
  width:100vw;
}

.full-image-preview img {
  position: absolute;
  left: 0;
  right: 0;
  margin: auto;
  -webkit-transition: opacity 1s ease-in-out;
  -moz-transition: opacity 1s ease-in-out;
  -o-transition: opacity 1s ease-in-out;
  transition: opacity 1s ease-in-out;
  opacity:0;
}

.images-preview img {
  -webkit-transition: opacity 2s ease-out;
  -moz-transition: opacity 2s ease-out;
  -o-transition: opacity 2s ease-out;
  transition: opacity 2s ease-out;
  opacity:0;
}

img.opaque {
  opacity: 1!important;
}

</style>
