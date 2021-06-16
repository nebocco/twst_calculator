<template>
  <Header />
  <Party />
  <Footer />
</template>

<script>
import Header from './components/Header.vue'
import Party from './components/Party.vue'
import Footer from './components/Footer.vue'


export default {
  name: 'App',
  data() {
    return {
    }
  },
  components: {
    Header,
    Party,
    Footer
  },
  methods: {
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: var(--color-letter);
  margin-top: 60px;
}

</style>
