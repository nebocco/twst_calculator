<template>
  <Header />
  <Party />
</template>

<script>
import Header from './components/Header.vue'
import Party from './components/Party.vue'


export default {
  name: 'App',
  data() {
    return {
    }
  },
  components: {
    Header,
    Party
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
  color: #2c3e50;
  margin-top: 60px;
}

body {
  padding: 0;
}

</style>
