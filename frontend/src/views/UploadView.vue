<template>
  <div class='background'>
    <h1>Charger de nouvelles images</h1>

    <div class='box good-practices'>
      <h2>Bonnes pratiques</h2>
      <ul>
        <li>Bien vérifer manuellement que l'image n'est pas déjà présente dans la base, à l'aide de l'affichage des images similaires</li>
        <li>Tagger immédiatement les photos - pour ce faire, il suffit d'ouvrir le menu d'édition et de charger les images les moins tagguées</li>
        <li>Ne pas mettre trop de photos d'un unique événement : une dizaine ou une vingtaine est largement suffisant</li>
        <li>Cela ne sert à rien de mettre des photos de trop bonne qualité, elles seront dans tout les cas redimensionnées</li>
      </ul>
    </div>
    <div class='box upload-form'>
      <!-- <form> -->
        <input type='file' @change='previewImage' />
        <img id="blah" :src='imageUrl' alt="your image" />
        <button @click='uploadImage()'>Uploader</button>
      <!-- </form> -->
    </div>
    <p-picture-tools :displayed="['home', 'signout']"/>
  </div>
</template>

<script>

import PPictureTools from '../components/PictureTools.vue';

export default {
  name: 'Edit',
  props: {},
  components: {
    PPictureTools
  },
  data: () => ({
    image: undefined
  }),
  computed: {
    imageUrl() {
      if (!this.image) return;
      console.log(this.image);
      return URL.createObjectURL(this.image);
    }
  },
  methods: {
    previewImage(input) {
      input = input.target;
      if (!input.files || !input.files[0])
        return;
      this.image = input.files[0];
    },
    uploadImage() {
      const data = new FormData();
      data.append('picture', this.image);
      console.log(this.image);
      console.log(data);
      this.$store.dispatch('UPLOAD_PICTURE', data);
    }
  },
  beforeRouteUpdate(to, from, next) {
    this.$store.dispatch('FETCH_TAGS', to.params.pictureId);
    next();
  },
  beforeMount() {

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
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

.box {
  color: white;
  border: 2px solid white;
  margin: 10px;
  border-radius: 11px;
  padding: 15px;
}

.upload-form img {
  max-width: 500px;
  max-height: 200px;
}
</style>
