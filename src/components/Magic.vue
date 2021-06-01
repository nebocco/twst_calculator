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
    <p>{{magicCurrent}}</p>
    <p>damage: {{ totalDamage }}</p>
    <div class="magic-description">
      <dl>
        <dt>説明</dt>
        <dd>{{ magicCurrent === null ? "--" : magicCurrent.magic.text }}</dd>
        <dt>追加効果</dt>
        <dd>
          {{ magicCurrent === null ? "--" : magicCurrent.text }}
          <input
            type="checkbox"
            name="DuoEnable"
            id="duo-enable"
            v-if="DuoUsable"
            v-model="DuoEnabled"
          />
        </dd>
      </dl>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Magic',
  data() {
    return {
      magicLevel: 1,
      buffs: [],
      DuoEnabled: false,
    }
  },
  props: {
    magic: {
      type: Object,
    },
    magicList: {
      type: Array,
      required: true,
    },
    BaseAttack: {
      type: Number
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
    DuoUsable() {
      return this.magicCurrent === null ? false : this.magicCurrent.text.includes("[DUO]")
    },
    BuffAttack() {
      return 0;
    },
    BuffDamage() {
      return 0;
    },
    totalDamage() {
      if(this.magicCurrent === null) {
        return 0;
      }
      const attack = this.BaseAttack + this.BuffAttack;
      const power = (this.magicCurrent.magic.power + 4) / 8 +
        (this.magicCurrent.magic.power + 2) / 80 * this.magicLevel;
      const affectedCombo = this.DuoEnabled && this.DuoUsable ? 3 : this.magicCurrent.magic.combo;
      const combo = (1 - 0.1 * (affectedCombo - 1)) * affectedCombo; 
      return [attack, power, combo, attack * power * combo];
    }
  },
  watch: {
    totalDamage() {
      this.$emit('update:totalDamage', this.totalDamage[3]);
    }
  }
}
</script>

<style scoped>
h4 {
  display: inline-block;
  margin-right: 1em;
}

dl {
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