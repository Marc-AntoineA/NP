<template>
  <div class='background'>
    <p-spinner class='center' :show="loading"></p-spinner>
    <div v-if='!loading' class='picture-view'>
      <div class='full-image-preview'>
        <img class='image-full' :class='{opaque: !transitionState }' :src='$store.getters.fullUrl(pictureId)'/>
        <img class='image-full' :class='{opaque: transitionState }' :src='nextPictureUrl'/>
      </div>
      <ul class='images-preview'>
        <li v-if='displayPreviews' v-for='neighborId in neighbors'>
          <img class='image-thumbnail' :src='$store.getters.thumbnailUrl(neighborId)'
            @click='selectPicture(neighborId)' :class='{opaque: !loadingPreviews }'/>
        </li>
      </ul>
    </div>

    <p-picture-tools :displayed="['home', 'random', 'populate', 'edit', 'help', 'stats', 'home', 'share', 'signout']"
      :populationDelay='10000'
      @random-image='loadRandomImage()' @populate='randomWalk()' @edit-image='editImage()'/>
    <p-list-tags :currentTags='tags' :alwaysDisplay='false'/>
  </div>
</template>

<script>
import PPictureTools from '../components/PictureTools.vue';
import PSpinner from '../components/Spinner.vue';
import PListTags from '../components/ListTags.vue';

export default {
  name: 'Walk',
  props: {},
  components: { PSpinner, PPictureTools, PListTags, },
  data: () => ({
    loading: true,
    loadingPreviews: true,
    nextPictureUrl: '',
    transitionState: false,
    displayPreviews: false
  }),
  computed: {
    pictureId() {
      return this.$route.params.pictureId;
    },
    tags() {
      return this.$store.state.tags[this.pictureId];
    },
    options() {
      return this.$store.state.options;
    },
    neighbors() {
      const neighbors = this.$store.getters.neighbors(this.pictureId);
      for (let i = neighbors.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        const temp = neighbors[i];
        neighbors[i] = neighbors[j];
        neighbors[j] = temp;
      }
      return neighbors.slice(0, 5);
    }
  },
  methods: {
    loadRandomImage() {
      this.$store.dispatch('FETCH_RANDOM_PICTURE').then((node) => {
        const pictureId = node.id;
        this.$router.push({ name: 'walk', params: { pictureId: pictureId }});
      });
    },
    randomWalk() {
      const randomPictureIndex = Math.floor(Math.random()*this.neighbors.length);
      const nodeId = this.neighbors[randomPictureIndex];
      this.$router.push({ name: 'walk', params: { pictureId: nodeId }});
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
    this.nextPictureUrl = this.$store.getters.fullUrl(to.params.pictureId);
    setTimeout(() => {
      this.$store.dispatch('FETCH_NEIGHBORS', to.params.pictureId).then(() => {
        this.displayPreviews = true;
        setTimeout(() => { this.loadingPreviews = false; }, 150);
        this.transitionState = false;
      });
      next();
    }, 200);
  },
  beforeMount() {
    this.loading = true;
    this.displayPreviews = false;
    this.loadingPreviews = true;
    this.$store.dispatch('FETCH_NEIGHBORS', this.$route.params.pictureId).then(() => {
      setTimeout(() => { this.loadingPreviews = false; }, 150);;
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
