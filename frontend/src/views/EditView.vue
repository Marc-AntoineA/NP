<template>
  <div class='background'>
    <div v-if='!loading' class='edit-view'>
      <multiselect class='black-multiselect' :value='tags' tag-placeholder='Ajouter ce tag' placeholder='Chercher ou ajouter un tag'
      :options='options' :multiple='true' :taggable='true' @tag='addTag'
      :hide-selected='true' :options-limit='5' @input='updateTags'
       />
      <img class='image-full' :src='pictureFullUrl'/>
    </div>
    <div class='gallery'>
      <button @click='loadLessTaggedPictures()'>Charger des images peu taggées</button>
      <ul>
        <li v-for='picture in lessTaggedPictures'>
          <img :src='"http://192.168.2.119/thumbnails/" + picture.id + ".jpg"'
            @click='changePicture(picture.id)'/>
        </li>
      </ul>
    </div>

    <p-picture-tools :displayed="['home', 'walk', 'signout', 'share', 'help', 'stats', 'random']"/>
  </div>
</template>

<script>

import Multiselect from 'vue-multiselect';
import PPictureTools from '../components/PictureTools.vue';

export default {
  name: 'Edit',
  props: {},
  components: {
    Multiselect, PPictureTools
  },
  data: () => ({
    loading: true,
  }),
  computed: {
    pictureId() {
      return this.$route.params.pictureId;
    },
    pictureFullUrl() {
      return 'http://localhost' + '/full/' + this.pictureId + '.jpg';
    },
    tags() {
      return this.$store.state.tags[this.pictureId];
    },
    options() {
      return this.$store.state.options;
    },
    lessTaggedPictures() {
      return this.$store.state.lessTaggedPictures;
    }
  },
  methods: {
    addTag(newTag) {
      this.$store.commit('ADD_OPTION', newTag);
      this.$store.dispatch('ADD_TAG', { pictureId: this.pictureId, tag: newTag });
    },
    updateTags(tags) {
      this.$store.dispatch('UPDATE_TAGS', { pictureId: this.pictureId, tags: tags });
    },
    loadLessTaggedPictures() {
      this.$store.dispatch('FETCH_LESS_TAGGED_PICTURES');
    },
    changePicture(pictureId) {
      this.$router.push({ name: 'edit', params: { pictureId: pictureId }});
    }
  },
  beforeRouteUpdate(to, from, next) {
    this.$store.dispatch('FETCH_TAGS', to.params.pictureId);
    next();
  },
  beforeMount() {
    let loadingOptions = true;
    let loadingTags = true;

    this.$store.dispatch('FETCH_OPTIONS', this.$route.params.pictureId).then(() => {
      loadingOptions = false;
      if (!loadingTags) this.loading = false;
    });

    this.$store.dispatch('FETCH_TAGS', this.$route.params.pictureId).then(() => {
      loadingTags = false;
      if (!loadingOptions) this.loading = false;
    });
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style scoped>
.image-full {
  max-height: 95%;
  max-width: calc(95% - 460px);
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

.edit-view {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  height: calc(100vh - 160px);
}

.black-multiselect {
  width: 400px;
}

.gallery {
  width: 100%;
  position: absolute;
  bottom: 0;
}

.gallery button {
  background: transparent;
  border: 3px solid white;
  color: #eee;
  padding: 5px;
  font-size: 14px;
  font-weight: bold;
  border-radius: 5px;
}

.gallery ul {
  overflow-x: scroll;
  display: flex;
  list-style: none;
  margin-bottom: 0px;
  /* min-height: 110px; */
}

.gallery img {
  height: 100px;
  margin: 0px 5px;
}

</style>

<style>
.black-multiselect {
    width: auto;
    margin: 20px;
}

.black-multiselect .multiselect__tag-icon::after {
  color: black;
}

.black-multiselect .multiselect__tag {
	background-color: #888;
}

.black-multiselect .multiselect__option--highlight {
  background-color: #888;
}

.black-multiselect .multiselect__option--highlight::after {
  background-color: #444;
}

.black-multiselect .multiselect__tag-icon:focus, .multiselect__tag-icon:hover {
    background: #bbb;
}

</style>
