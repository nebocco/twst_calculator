<template>
  <header>
    <h1>
      ツイステ計算機
    </h1>
    <i 
      class="far fa-question-circle"
      @click="$refs.help_modal.show()"
    />
  </header>
  <HelpModal ref="help_modal" />
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
  font-size: 2em;
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