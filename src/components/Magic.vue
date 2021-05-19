<template>
  <div class="magic-container">
    <div class="magic-name">
      <h4>{{ magicCurrent === null ? "" : magicCurrent.magic.name }}</h4>
      <label for="magicLevel">Lv.</label>
      <input
        type="number"
        name="magicLevel"
        v-model.number="magicLevel"
        min="1"
        max="10"
        :disabled="magicCurrent === null"
      >
    </div>
    <div class="magic-description">
      <dl>
        <dt>説明</dt>
        <dd>{{ magicCurrent === null ? "--" : magicCurrent.magic.text }}</dd>
        <dt>追加効果</dt>
        <dd>{{ magicCurrent === null ? "--" : magicCurrent.text }}</dd>
      </dl>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Magic',
  data() {
    return {
      magicLevel: 1
    }
  },
  props: {
    magic: {
      type: Object,
    },
    magicList: {
      type: Array,
      required: true,
    }
  },
  computed: {
    magicCurrent() {
      return this.magic === undefined ? null :
      { 
        magic: this.magicList[this.magic[Math.floor(this.magicLevel / 5)][0]],
        text: this.magic[Math.floor(this.magicLevel / 5)][1]
      }
    },
  }
}
</script>

<style scoped>
h4 {
  display: inline-block;
  margin-right: 1em;
}

dl {
  /* width: 100%; */
  margin: 10px 0;
  display: flex;
  flex-wrap: wrap;
}

dt {
  width: 35%;
  padding: 10px;
  background-color: #DADADA;
  margin: 0 0 10px 0;
  border-top-left-radius: 3px;
  border-bottom-left-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
}

dd {
  width: 65%;
  padding: 10px;
  background-color: #F3F3F3;
  margin: 0 0 10px 0;
  border-top-right-radius: 3px;
  border-bottom-right-radius: 3px;
}

dd::before {
  content: "";
}

.magic-name {
  display: flex;
  align-items: baseline;
}

.magic-name > h4 {
  flex-grow: 1;
}

label {
  margin-right: .6em;
}

input[disabled] {
  color: #aaa;
  background: #f2f4f6;
}

input:invalid {
  border-color: red;
  background: #eecccc;
}

input:invalid::before {
  content: "0100101";
}

</style>