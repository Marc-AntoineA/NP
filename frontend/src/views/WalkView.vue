<template>
  <div>
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


export default {
  name: 'Walk',
  props: {},
  components: {
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
  max-height: 60vh
}

.images-preview li {
  display: inline-block;
}

.image-thumbnail {
  height: 80px;
}

</style>
