<template>
  <div class="magic-container">
    {{ magicCurrent }}
    <div class="magic-name">
      <h4>{{ magicCurrent === null ? "" : magicCurrent.magic.name }}</h4>
      <label for="magicLevel">Lv.</label>
      <input
        type="number"
        name="magicLevel"
        v-model.number="magicLevel"
        min="1"
        max="10"
        @blur="magicLevel = Math.max(1, Math.min(10, magicLevel))"
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
            {{ buff.text }}
          </div>
          <button @click="remove(index)">x</button>
        </li>
        <li class="add-buff">
          <select v-model="newBuff">
          <option disabled value="">選択してください</option>
          <option
            v-for="(buff, index) in filteredAvailableBuffs"
            :value="buff" 
            :key="index"
          >

            {{ buff.text }}
          </option>
        </select>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>

const attrs = ["火", "水", "木", "無"];

export default {
  name: 'Magic',
  data() {
    return {
      magicLevel: 1,
      buffs: [],
      newBuff: "",
      DuoEnabled: false,
      modal: false,
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
    },
    allAvailableBuffs: {
      type: Array,
      required: true,
    }
  },
  methods: {
    remove(index) {
      this.buffs.splice(index, 1);
    }
  },
  computed: {
    magicCurrent() {
      const level = Math.max(1, Math.min(10, this.magicLevel));
      const index = Math.floor(level / 5);
      let mc = this.magic === undefined ? null :
      { 
        magic: this.magicList[this.magic[index][0]],
        text: this.magic[index][1]
      }
      if (mc !== null && mc.text.includes("UP")) {
        this.$emit('update:availableBuff', {
          text: mc.text,
          level: level
        });
      }
      return mc
    },
    DuoUsable() {
      return this.magicCurrent === null ? false : this.magicCurrent.text.includes("[DUO]")
    },

    filteredAvailableBuffs() {
      return this.allAvailableBuffs.filter(buff => buff.text);
    },
    
    BuffAttack() {
      if (this.magicCurrent === null)
        return 0;

      let totalBuff = 0;
      const current = {
        text: this.magicCurrent.text,
        level: this.magicLevel
      }

      this.buffs
      .concat(current)
      .filter(buff => buff.text.includes("ATK UP"))
      .forEach(buff => {
        if (buff.text.includes("極小")) 
          totalBuff += 0.05 + 0.005 * buff.level;
        else if (buff.text.includes("小")) 
          totalBuff += 0.1 + 0.01 * buff.level;
        else if (buff.text.includes("中")) 
          totalBuff += 0.2 + 0.015 * buff.level;
        else if (buff.text.includes("大")) 
          totalBuff += 0.5;
      })
      return this.BaseAttack * totalBuff;
    },
    BuffDamage() {
      if (this.magicCurrent === null)
        return 0;

      let totalBuff = 0;
      const current = {
        text: this.magicCurrent.text,
        level: this.magicLevel
      }

      this.buffs
      .concat(current)
      .filter(buff => buff.text.includes("ダメージ UP"))
      .forEach(buff => {
        const bonus = 
          buff.text.includes(attrs[this.magicCurrent.magic.attr] + "属性") ? 1.2 :
          buff.text.includes("属性") ? 0 : 1

        if (buff.text.includes("極小")) 
          totalBuff += (0.0125 +  0.00125 * buff.level) * bonus;
        else if (buff.text.includes("小")) 
          totalBuff += (0.025 + 0.0025 * buff.level) * bonus;
        else if (buff.text.includes("中")) 
          totalBuff += (0.05 + 0.00375 * buff.level) * bonus;
        else if (buff.text.includes("大")) 
          totalBuff += (0.125) * bonus;
      })
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
      if (this.magicCurrent !== null) {
        this.$emit('update:totalDamage', {
          damage: this.totalDamage[3],
          attr: this.magicCurrent.magic.attr
        });
      } 
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
  padding-left: 0;
}

li.selected-buffs {
  background: aqua;
  padding: 10px 20px;
  border-radius: 3px;
}

.buffs-list select {
  width: 100%;
}

.buff-name {
  display: inline-block;
}

</style>