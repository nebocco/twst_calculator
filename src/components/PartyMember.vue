<template>
<div class="party-member">
  <!-- <h3>カード</h3> -->
  <div class="button-container">
    <button class="red" @click="clearAll(false)">Clear</button>
    <button class="green" @click="$refs.save_modal.show()">Save</button>
    <button class="green" @click="$refs.load_modal.show()">Load</button>
    <SaveModal ref="save_modal"
      :initialName="cardDisplayName"
      @save-data="saveData($event)"
    />
    <LoadModal
      ref="load_modal"
      :savedDataNames="Object.keys(savedData)"
      @load-data="loadData($event)"
      @delete-data="$emit('delete-data', $event)"
    />
  </div>
  <div class="card-box">
    <div class="card-detail">
      <div class="select-wrap">
      <select
        name="characterName"
        v-model="Name"
        @change="fillDetails"
      >
        <option disabled value="-1">名前</option>
        <option 
          v-for="c in filteredCharacters"
          :key="'name-' + c.id"
          :value="c.id"
        >
          {{ c.name }}
        </option>
      </select>
      </div>
    </div>
    <div class="card-detail">
      <div class="select-wrap">
      <select
        name="characterCostume"
        v-model="Costume"
        @change="fillDetails"
      >
        <option disabled value="-1">コスチューム</option>
        <option 
          v-for="c in filteredCostumes"
          :key="'costume-' + c.id"
          :value="c.id"
        >
          {{ c.name }}
        </option>
      </select>
      </div>
    </div>
  </div>
  <div class="status-box">
    <div class="status-each">
      <label for="hit-point">HP</label>
      <input
        type="number"
        v-model.number="HitPoint"
        min=0
        onfocus="if(this.value==0)this.value='';"
        onblur="if(this.value=='')this.value=0;"
      >
    </div>
    <div class="status-each">
      <label for="attack">ATK</label>
      <input
        type="number"
        v-model.number="Attack"
        min=0
        onfocus="if(this.value==0)this.value='';"
        onblur="if(this.value=='')this.value=0;"
      >
    </div>
  </div>
  <h3>バディ</h3>
  <Buddy
    ref="buddy"
    :buddies="Buddies"
    :characterList="characterList"
    :partyMember="partyMember"
    :memberIndex="memberIndex"
    @update:buffsBuddy="buffsBuddy = $event"
    @update:buddyLevel="buddyLevelRef = $event"
  />
  <h3>魔法</h3>
  <Magic 
    v-for="i in 2"
    :key="'magic' + i"
    :ref="'magic' + i"
    :memberIndex="memberIndex"
    :magicIndex="i-1"
    :magic="Magics[i-1]"
    :magicList="magicList"
    :BaseAttack="Attack"
    :affectedAttack="affectedAttack"
    :allAvailableBuffs="allAvailableBuffs[i-1]"
    :vsAttr="vsAttr"
    @update:totalDamage="$emit('update:totalDamage', [i-1, $event])" 
    @update:availableBuff="updateAvailableBuff(i-1, $event)"
    @update:magicLevel="magicLevelRef[i-1] = $event"
    @update:BuffCure="updateBuffCure(i-1, $event)"
  />
</div>
</template>

<script>
import Buddy from './Buddy.vue'
import Magic from './Magic.vue'
import SaveModal from './SaveModal'
import LoadModal from './LoadModal'

export default {
  name: 'PartyMember',
  data() {
    return {
      Name: -1,
      Costume: -1,
      HitPoint: 0,
      Attack: 0,
      Buddies: [],
      Magics: [],
      buffsBuddy: [0, 0],
      availableBuff: [{}, {}],
      buddyLevelRef: [1, 1, 1],
      magicLevelRef: [1, 1],
      BuffCure: [0, 0],
    }
  },
  methods: {
    fillDetails() {
      if(this.Name < 0 || this.Costume < 0) {
        this.$emit('select-card', -1);
        return
      }
      const card = this.cardList[this.cardReverseIndex[this.Name][this.Costume]];
      this.Buddies = card.buddies;
      this.Magics = card.magics;
      this.$emit('select-card', this.Name);
    },
    
    updateAvailableBuff(index, buff) {
      if (this.Name < 0 || this.Costume < 0) {
        return;
      }
      if (buff.text) {
        buff.from = this.characterList[this.Name].name +
          "【" + this.costumeList[this.Costume].name + "】"
      }
      this.availableBuff[index] = buff;
      let emitBuff = this.availableBuff.map(buff => {
        if (buff.text && buff.text.includes("選択")) {
          return buff;
        } else {
          return {};
        }
      });
      this.$emit('update:availableBuff', emitBuff);
    },
    updateBuffCure(index, buff) {
      this.BuffCure[index] = buff;
      let cure = this.BuffCure[0] + this.BuffCure[1];
      this.$emit("update:Cure", cure * this.Attack);
    },
    clearAll(force) {
      if (!force && !confirm(this.memberIndex + 1 + "人目の入力を削除しますか？")) {
        return;
      }
      this.Name = -1;
      this.Costume = -1;
      this.HitPoint = 0;
      this.Attack = 0;
      this.Buddies = [];
      this.Magics = [];
      this.buffsBuddy = [0, 0];
      this.availableBuff = [{}, {}];

      this.$refs.magic1.clearAll();
      this.$refs.magic2.clearAll();
      this.$refs.buddy.clearAll();

      this.fillDetails()
    },
    unpackData(member) {
      if (!this.cardReverseIndex[member.name][member.costume] < 0) {
        return;
      }
      this.Name = member.name;
      this.Costume = member.costume;
      this.HitPoint = member.hp;
      this.Attack = member.atk;
      this.fillDetails();
      this.$refs.buddy.loadStorage(member.buddyLevel);
      this.$refs.magic1.loadStorage(member.magicLevel[0]);
      this.$refs.magic2.loadStorage(member.magicLevel[1]);
    },
    loadStorage() {
      if (localStorage.getItem('currentMembers')) {
        let members = JSON.parse(localStorage.getItem('currentMembers'));
        try {
          const member = members[this.memberIndex];
          if (member) {
            this.unpackData(member);
          }
        } catch(e) {
          members[this.memberIndex] = null;
          localStorage.setItem('currentMembers', JSON.stringify(members));
        }
      } else {
          localStorage.setItem('currentMembers', JSON.stringify([]));
      }
    },
    saveStorage() {
      let members = JSON.parse(localStorage.getItem('currentMembers'))
      members[this.memberIndex] = this.characterSaveData;
      localStorage.setItem('currentMembers', JSON.stringify(members))
    },
    loadData(savedName) {
      let data = this.savedData[savedName];
      if (data) {
        this.unpackData(data);
      }
    },
    saveData(saveName) {
      this.$emit('update:savedData', [saveName, this.characterSaveData])
    }
  },
  props: {
    characterList: {
      type: Array,
      required: true,
    },
    costumeList: {
      type: Array,
      required: true
    },
    magicList: {
      type: Array,
      required: true
    },
    cardList: {
      type: Array,
      required: true
    },
    partyMember: {
      type: Array,
      required: true
    },
    AvailableBuffs: {
      type: Array,
      required: true
    },
    memberIndex: {
      type: Number,
      required: true
    },
    vsAttr: {
      type: Number
    },
    savedData: Object,
  },
  components: {
    Buddy,
    Magic,
    SaveModal,
    LoadModal
  },
  computed: {
    filteredCharacters() {
      return this.Costume === -1 ? this.characterList :
      this.characterList.filter((c) => 
        this.cardReverseIndex[c.id][this.Costume] >= 0
      )
    },
    filteredCostumes() {
      return this.Name === -1 ? this.costumeList :
      this.costumeList.filter((c) =>
        this.cardReverseIndex[this.Name][c.id] >= 0
      )
    },

    cardReverseIndex() {
      let table = new Array(this.characterList.length);
      for(let i = 0; i < this.characterList.length; i++) {
        table[i] = new Array(this.costumeList.length).fill(-1);
      }
      this.cardList.forEach((card, index) => {
        table[card.name][card.costume] = index;
      })
      return table;
    },
    allAvailableBuffs() {
      let buff1 = this.AvailableBuffs.slice();
      let buff2 = this.AvailableBuffs.slice();
      buff1.push(this.availableBuff[1]);
      buff2.push(this.availableBuff[0]);
      return [buff1, buff2];
    },

    cardDisplayName() {
      if(this.Name < 0 || this.Costume < 0) {
        return ""
      }
      const card = this.cardList[this.cardReverseIndex[this.Name][this.Costume]];
      return this.characterList[card.name].name 
        + "【" 
        + this.costumeList[card.costume].name
        + "】"
    },

    affectedHitPoint() {
      return Math.floor(this.HitPoint * (1 + this.buffsBuddy[1]))
    },

    affectedAttack() {
      return Math.floor(this.Attack * (1 + this.buffsBuddy[0]))
    },

    characterSaveData() {
      return {
        name: this.Name,
        costume: this.Costume,
        hp: this.HitPoint,
        atk: this.Attack,
        buddyLevel: Array.from(this.buddyLevelRef),
        magicLevel: Array.from(this.magicLevelRef),
      }
    },
  },
  mounted() {
    this.loadStorage();
  },
  watch: {
    affectedHitPoint() {
      this.$emit('update:HP-ATK', [this.affectedHitPoint, this.affectedAttack])
    },
    affectedAttack() {
      this.$emit('update:HP-ATK', [this.affectedHitPoint, this.affectedAttack])
    },
    characterSaveData: {
      handler() {
        if(this.Name >= 0 && this.Costume >= 0) {
          this.saveStorage()
        }
      },
      deep: true
    }
  }
}
</script>

<style scoped>

.button-container {
  margin: 10px auto;
  display: flex;
  justify-content: center;
}

button {
  padding: .4em 1.2em;
  font-size: 1rem;
  text-align: center;
  text-decoration: none;
  white-space: nowrap;
  border-radius: 4px;
  box-sizing: border-box;
  cursor: pointer;
}

button:hover, button:focus {
  background: var(--color-background-third);
}

button.green {
  color: var(--color-ok);
  border: 2px solid var(--color-ok);
}

button.red {
  color: var(--color-warn);
  border: 2px solid var(--color-warn);
}

h3 {
  margin-top: 2rem;
}

.party-member {
  width: 90%;
  margin: 0 auto;
}

.card-box {
  display: flex;
}

.card-detail {
  flex: 1;
}

.card-detail select {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  width: 90%;
  border: none;
  border-radius: 0;
  border-bottom: var(--color-border) solid 2px;
}

.select-wrap {
  position: relative;
}

.select-wrap::after {
  position: absolute;
  font-family: "Font Awesome 5 Free";
  font-weight: 900;
  font-size: .8em;
  content: "\f078";
  right: 8%;
  top: 24%;
}

.card-detail option:disabled {
  display: none;
}

.status-box {
  display: flex;
}

.status-each {
  flex: 1;
}

.status-each > label {
  min-width: 3em;
  margin-top: .5em;
  margin-bottom: 0;
}

.status-each > input {
  width: 90%;
  max-width: 90%;
  border: none;
  border-radius: 0;
  border-bottom: var(--color-border) solid 2px;
  text-align: right;
}

.button-container {
  display: flex;
  width: 80%;
  justify-content: space-between;
  margin: .8em auto 1.2em;
}


</style>