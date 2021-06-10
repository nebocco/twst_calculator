<template>
  <header>
    <h1>
      計算機
    </h1>
    <i 
      class="far fa-question-circle"
      @click="$refs.modal.show()"
    />
  </header>
  <HelpModal ref="modal" />
</template>

<script>
import HelpModal from './HelpModal.vue';

export default {
  name: "Header",
  components: {
    HelpModal
  }
}
</script>

<style scoped>
header {
  display: flex;
  justify-content: center;
  position: relative;
}

h1 {
  margin: 0;
}

i {
  font-size: 2em;
  position: absolute;
  right: .5em;
}

i:hover {
  cursor: pointer;
  opacity: .6;
}

</style>