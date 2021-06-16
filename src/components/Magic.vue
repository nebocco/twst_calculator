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
        @focus="
          levelStash = magicLevel;
          magicLevel='';
        "
        @blur="magicLevel = magicLevel === '' ? levelStash : Math.min(10, Math.max(1, magicLevel))"
        :disabled="magicCurrent === null"
      />
    </div>
    <p class="damage">
      damage: 
      <span
        class="damage-number"
        :class="compatibilityTag"
      >
        {{ Math.round(attrDamage) }}
      </span>
    </p>
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
            v-if="DuoUsable"
            v-model="DuoEnabled"
          />
        </dd>
      </dl>
    </div>
    <div class="accordion">
      <div class="title" @click="openAccordion">
        <div class="title-text">
          その他のバフ ({{ buffs.length }})
        </div>
        <i class="fas fa-chevron-up" v-show="isOpen" />
        <i class="fas fa-chevron-down" v-show="!isOpen" />
      </div>
      <div class="accordion-content" v-if="isOpen">
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
              <button @click="remove(index)">
                <i class="fas fa-times" />
              </button>
            </li>
            <li class="add-buff">
              <select v-model="newBuff">
                <option disabled value="">バフを追加</option>
                <option
                  v-for="(buff, index) in filteredAvailableBuffs"
                  :value="buff" 
                  :key="index"
                >
                  {{ buff.text + "（" + buff.from + "）"}}
                </option>
              </select>
            </li>
          </ul>
        </div>
      </div>
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
      levelStash: '',
      buffs: [],
      newBuff: "",
      DuoEnabled: false,
      modal: false,
      isOpen: false,
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
    },
    memberIndex: {
      type: Number,
      required: true
    },
    magicIndex: {
      type: Number,
      required: true
    },
    vsAttr: Number
  },
  methods: {
    openAccordion() {
      this.isOpen = !this.isOpen;
    },

    remove(index) {
      this.buffs.splice(index, 1);
    },
    removeExceptUP(buff) {
      return {
        text: buff.text.split(' & ').filter(t => t.includes("UP")).join(' & '),
        level: buff.level,
        from: buff.from
      }
    },
    clearAll() {
      this.magicLevel = 1;
      this.buffs = [];
      this.newBuff = "";
      this.DuoEnabled = false;
      this.modal = false;
    },
    loadStorage(level) {
      this.magicLevel = level;
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
      return mc
    },
    DuoUsable() {
      return this.magicCurrent === null ? false : this.magicCurrent.text.includes("[DUO]")
    },

    filteredAvailableBuffs() {
      return this.allAvailableBuffs
      .filter(buff => buff.text)
      .map(buff => this.removeExceptUP(buff))
      .filter(buff => buff.text !== "")
    },
    BuffAttack() {
      if (this.magicCurrent === null)
        return 0;

      let totalBuff = 0;
      const current = this.removeExceptUP({
        text: this.magicCurrent.text,
        level: this.magicLevel
      });

      this.buffs
      .concat(current)
      .forEach(buff => {
        if (buff.text.includes("ATK UP（極小")) 
          totalBuff += 0.05 + 0.005 * buff.level;
        else if (buff.text.includes("ATK UP（小")) 
          totalBuff += 0.1 + 0.01 * buff.level;
        else if (buff.text.includes("ATK UP（中")) 
          totalBuff += 0.2 + 0.015 * buff.level;
        else if (buff.text.includes("ATK UP（大")) 
          totalBuff += 0.5;
      })
      return this.BaseAttack * totalBuff;
    },
    BuffDamage() {
      if (this.magicCurrent === null)
        return 0;

      let totalBuff = 0;
      const current = this.removeExceptUP({
        text: this.magicCurrent.text,
        level: this.magicLevel
      });

      this.buffs
      .concat(current)
      .forEach(buff => {
        const bonus = 
          buff.text.includes(attrs[this.magicCurrent.magic.attr] + "属性ダメージ UP") ? 1.2 :
          buff.text.includes("属性ダメージ UP") ? 0 : 1

        if (buff.text.includes("ダメージ UP（極小")) 
          totalBuff += (0.0125 +  0.00125 * buff.level) * bonus;
        else if (buff.text.includes("ダメージ UP（小")) 
          totalBuff += (0.025 + 0.0025 * buff.level) * bonus;
        else if (buff.text.includes("ダメージ UP（中")) 
          totalBuff += (0.05 + 0.00375 * buff.level) * bonus;
        else if (buff.text.includes("ダメージ UP（大")) 
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
    },
    attrDamage() {
      if (this.magicCurrent === null) {
        return 0;
      }
      else {
        let damage = this.totalDamage[3];
        let self_attr = this.magicCurrent.magic.attr;
        if (self_attr == 3) {
          return damage * 1.2;
        } else if (this.compatibility == 1) {
          return damage * 1.5;
        } else if (this.compatibility == -1) {
          return damage * 0.5;
        } else {
          return damage;
        }
      }
    },
    compatibility() {
      if (this.magicCurrent === null) {
        return 0;
      }
      else {
        let self_attr = this.magicCurrent.magic.attr;
        let opp_attr = this.vsAttr;
        if (self_attr == 3) {
          return 0;
        } else if ((self_attr + 2) % 3 == opp_attr) {
          return 1;
        } else if ((self_attr + 1) % 3 == opp_attr) {
          return -1;
        } else {
          return 0;
        }
      }
    },
    compatibilityTag() {
      if (this.compatibility === 1) {
        return "compatible"
      } else if (this.compatibility === -1) {
        return "incompatible"
      } else {
        return ""
      }
    },
    BuffCure() {
      if (this.magicCurrent === null) {
        return 0;
      }
      let text = this.magicCurrent.text;
      let totalBuff = 0;
      if (text.includes("HP回復（極小")) {
        totalBuff += 0.5 + 0.01 * this.magicLevel;
      } else if (text.includes("HP回復（小")) {
        totalBuff += 0.9 + 0.02 * this.magicLevel;
      } else if (text.includes("HP回復（中")) {
        totalBuff += 1.3 + 0.04 * this.magicLevel;
      } else if (text.includes("HP継続回復（中")) {
        totalBuff += 1.15 + 0.03 * this.magicLevel;
      }
      return totalBuff;
    }
  },
  watch: {
    totalDamage() {
      if (this.magicCurrent !== null) {
        this.$emit('update:totalDamage', {
          damage: this.totalDamage[3],
          attr: this.magicCurrent.magic.attr
        });
      } else {
        this.$emit('update:totalDamage', {
          damage: 0,
          attr: 0
        });
      }
    },
    newBuff() {
      if (this.newBuff !== "") {
        this.buffs.push(this.newBuff);
        this.newBuff = "";
      } 
    },
    magicLevel() {
      this.$emit("update:magicLevel", this.magicLevel);
    },
    magicCurrent() {
      console.log("update:availableBuff", this.memberIndex);
      if (this.magicCurrent !== null && this.magicCurrent.text.includes("UP")) {
        this.$emit('update:availableBuff', {
          text: this.magicCurrent.text,
          level: this.magicLevel
        });
      } else {
        this.$emit('update:availableBuff', {});
      }
    },
    BuffCure() {
      this.$emit('update:BuffCure', this.BuffCure);
    }

  }
}
</script>

<style scoped>
h4 {
  display: inline-block;
  font-size: 1.2em;
  margin: auto;
  padding: 0;
}

dl {
  margin: 10px 0;
  display: flex;
  flex-wrap: wrap;
}

dt {
  width: 35%;
  padding: 10px;
  background-color: var(--color-background-third);
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
  background-color: var(--color-background-second);
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
  margin-bottom: 0.4em;
}

.magic-name > h4 {
  flex-grow: 1;
}

label {
  margin: auto .6em auto 0;
}

input {
  width: 20%;
  margin: 0;
  border: 1px solid var(--color-border-light);
  border-radius: 0;
  text-align: end;
  display: inline;
}


input[disabled] {
  color: var(--color-letter-light);
  background: #f2f4f6;
}

input:invalid {
  border-color: red;
  background: #eecccc;
}

ul.buffs-list {
  list-style: none;
  padding-left: 0;
}

li.selected-buffs {
  border: 2px solid var(--color-border);
  border-radius: 3px;
  display: flex;
  justify-content: space-between;
}

.selected-buffs > div {
  padding: 10px 20px;

}

.selected-buffs button {
  width: 15%;
  max-width: 40px;
}

.buffs-list select {
  padding: .4em .8em;
  margin: 0;
  border: 1px solid var(--color-border-light);
  border-radius: 0;
  width: 100%;
}

.buff-name {
  display: inline-block;
}

.accordion {
  margin: -10px auto 40px;
}

.title:hover {
  opacity: .8;
  cursor: pointer;
}

.title {
  margin-bottom: 10px;
  padding: 10px;
  border-bottom: 2px solid var(--color-border);
  text-align: left;
}

.title > div {
  display: inline-block;
  font-weight: bold;
}

.title i {
  float: right;
  line-height: 1.3;
}

.content {
  padding: 0 15px;
  margin-bottom: 10px;
}

.damage-number {
  font-weight: 600;
}

.damage-number.compatible {
  color: var(--color-warn);
}

.damage-number.incompatible {
  color: var(--color-ok);
}

</style>