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
    <!-- <p>{{magicCurrent}}</p> -->
    <p>[atk, pow, cmb, damage] : <br> {{ totalDamage }}</p>
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
    <div class="other-buffs">
      <ul class="buffs-list">
        <li
          class="selected-buffs"
          v-for="(buff, index) in buffs"
          :key=index
        >
          <div class="buff-name">
            {{ buff }}
          </div>
          <button @click="remove(index)">x</button>
        </li>
        <li class="add-buff">
          <select v-model="newBuff">
          <option disabled value="">選択してください</option>
          <option
            v-for="(buff, index) in optionBuffs" 
            :value="buff" 
            :key="index"
          >
            {{ buff }}
          </option>
        </select>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>

const optionBuffs = [
  "ATK UP（極小）",
  "ATK UP（小）",
  "ATK UP（中）",
  "ATK UP（大）",
  "ダメージ UP（極小）",
  "ダメージ UP（小）",
  "ダメージ UP（中）",
  "ダメージ UP（大）",
  // "ダメージ DOWN（小）",
  // "ダメージ DOWN（中）",
  // "ダメージ DOWN（大）",
]

export default {
  name: 'Magic',
  data() {
    return {
      magicLevel: 1,
      buffs: [],
      newBuff: "",
      DuoEnabled: false,
      modal: false,
      optionBuffs: optionBuffs,
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
    },
    affectedAttack: {
      type: Number
    }
  },
  methods: {
    remove(index) {
      this.buffs.splice(index, 1);
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
      let totalBuff = 0;
      this.buffs.forEach(buff => {
        switch(buff) {
          case "ATK UP（極小）":
            totalBuff += 0.05 + 0.005 * this.magicLevel;
            break;
          case "ATK UP（小）":
            totalBuff += 0.1 + 0.01 * this.magicLevel;
            break;
          case "ATK UP（中）":
            totalBuff += 0.2 + 0.015 * this.magicLevel;
            break;
          case "ATK UP（大）":
            assert(this.magicLevel == 10);
            totalBuff += 0.5;
            break;
        }
      })
      switch(thi.magicCurrent.text) {
        case "ATK UP（極小）":
          totalBuff += 0.05 + 0.005 * this.magicLevel;
          break;
        case "ATK UP（小）":
          totalBuff += 0.1 + 0.01 * this.magicLevel;
          break;
        case "ATK UP（中）":
          totalBuff += 0.2 + 0.015 * this.magicLevel;
          break;
        case "ATK UP（大）":
          assert(this.magicLevel == 10);
          totalBuff += 0.5;
          break;
      }
      return this.BaseAttack * totalBuff;
    },
    BuffDamage() {
      let totalBuff = 0;
      this.buffs.forEach(buff => {
        switch(buff) {
          case "ダメージ UP（極小）":
            totalBuff += 0.0125 +  0.00125 * this.magicLevel;
            break;
          case "ダメージ UP（小）":
            totalBuff += 0.025 + 0.0025 * this.magicLevel;
            break;
          case "ダメージ UP（中）":
            totalBuff += 0.05 + 0.00375 * this.magicLevel;
            break;
          case "ダメージ UP（大）":
            assert(this.magicLevel == 10);
            totalBuff += 0.15;
            break;
        }
      })
      switch(this.magicCurrent.text) {
        case "ダメージ UP（極小）":
          totalBuff += 0.0125 +  0.00125 * this.magicLevel;
          break;
        case "ダメージ UP（小）":
          totalBuff += 0.025 + 0.0025 * this.magicLevel;
          break;
        case "ダメージ UP（中）":
          totalBuff += 0.05 + 0.00375 * this.magicLevel;
          break;
        case "ダメージ UP（大）":
          assert(this.magicLevel == 10);
          totalBuff += 0.15;
          break;
      }
      return totalBuff
    },
    totalDamage() {
      if(this.magicCurrent === null) {
        return [0, 0, 0, 0];
      }
      const attack = this.affectedAttack + this.BuffAttack;
      const power = (this.magicCurrent.magic.power + 4) / 8 +
        (this.magicCurrent.magic.power + 2) / 80 * this.magicLevel + this.BuffDamage;
      const affectedCombo = this.DuoEnabled && this.DuoUsable ? 3 : this.magicCurrent.magic.combo;
      const combo = (1 - 0.1 * (affectedCombo - 1)) * affectedCombo; 
      return [attack, power, combo, attack * power * combo];
    }
  },
  watch: {
    totalDamage() {
      this.$emit('update:totalDamage', this.totalDamage[3]);
    },
    newBuff() {
      if (this.newBuff !== "") {
        this.buffs.push(this.newBuff);
        this.newBuff = "";
      } 
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

input {
  width: 20%;
  text-align: right;
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

ul.buffs-list {
  list-style: none;
}

li.selected-buffs {
  background: aqua;
  padding: 10px 20px;
  border-radius: 3px;
}

.buff-name {
  display: inline-block;
}

</style>