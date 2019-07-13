<template>
  <div>
    <div v-if='!loading' class='picture-view'>
      <multiselect :value='tags' tag-placeholder='Ajouter ce tag' placeholder='Chercher ou ajouter un tag'
      :options='options' :multiple='true' :taggable='true' @tag='addTag'
      :hide-selected='true' :options-limit='5' @input='updateTags'
       />
      <img class='image-full' :src='pictureFullUrl'/>
    </div>
  </div>
</template>

<script>

import Multiselect from 'vue-multiselect';

export default {
  name: 'Edit',
  props: {},
  components: {
    Multiselect
  },
  data: () => ({
    loading: true,
  }),
  methods: {
    onSubmit() {
    }
  },
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
      console.log(this.$store.state.options);
      return this.$store.state.options;
    }
  },
  methods: {
    addTag(newTag) {
      this.$store.commit('ADD_OPTION', newTag);
      this.$store.dispatch('ADD_TAG', { pictureId: this.pictureId, tag: newTag });
    },
    updateTags(tags) {
      this.$store.dispatch('UPDATE_TAGS', { pictureId: this.pictureId, tags: tags });
    }
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
  max-height: 65vh;
  max-width: 95vw;
}
</style>
