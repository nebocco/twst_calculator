<template>
  <div class="result">
    <p>HP: {{ Math.round(totalHitPoint) }}</p>
    <!-- <p>Total ATK: {{ totalAttack }}</p> -->
    <!-- <p>attr Damage: {{ totalDamage }}</p> -->
    <p>Damage: {{ Math.round(vsAttrDamage) }}</p>
    <!-- {{ partyDamageList }} -->
    <!-- {{ vsAttr }} -->
  </div>
  <button class="clear" @click="clearAll">Clear All</button>
  <div class="vs-attr-container">
    <div class="vs-attr-text">
      相手属性：
    </div>
    <div class="vs-attr">
      <div
        class="attr-selector"
        v-for="i in 4"
        :key="i"
        :class="{ active: vsAttr === i-1 }"
        @click="vsAttr = i-1"
      >
        {{ attrs[i-1] }}
      </div>
    </div>
  </div>
  <div class="party">
    <div class="party-tab">
      <ul class="tab">
        <li 
          class="tab-item"
          v-for="i in 5"
          :key="i"
          @click="currentMember = i"
          :class="{ 'is-selected': currentMember === i }"
        >
         {{ i }}
        </li>
      </ul>
    </div>
    <div class="party-member-container">
      <PartyMember 
        class="party-member"
        v-for="i in 5"
        :key="i"
        :memberIndex="i-1"
        :ref="'member' + (i-1)"
        :characterList="staticData.characters"
        :costumeList="staticData.costumes"
        :cardList="staticData.cards"
        :magicList="staticData.magics"
        :partyMember="partyMember"
        :allAvailableBuffs="allAvailableBuffs.flat()"
        :class="{'not-selected': currentMember !== i}"
        :vsAttr="vsAttr"
        @select-card="partyMember[i-1] = $event"
        @update:HP-ATK="updateStatus(i-1, $event)"
        @update:totalDamage="updateDamage(i-1, $event)"
        @update:availableBuff="updateAvailableBuff(i-1, $event)"
      />
    </div>
  </div>
</template>

<script>
import PartyMember from './PartyMember.vue'
import staticData from '../../static/twst.json'

export default {
  name: 'Party',
  data() {
    return {
      staticData: staticData,
      currentMember: 1,
      partyMember: [-1, -1, -1, -1, -1],
      partyHitPointList: [0, 0, 0, 0, 0],
      partyAttackList: [0, 0, 0, 0, 0],
      partyDamageList: [[{}, {}], [{}, {}], [{}, {}], [{}, {}], [{}, {}]],
      allAvailableBuffs: [[{}, {}], [{}, {}], [{}, {}], [{}, {}], [{}, {}]],
      attrs: ["火", "水", "木", "無"],
      vsAttr: 3
   }
  },
  components: {
    PartyMember,
  },
  methods: {
    updateStatus(index, event) {
      this.partyHitPointList[index] = event[0];
      this.partyAttackList[index] = event[1];
    },
    updateDamage(index, event) {
      this.partyDamageList[index][event[0]] = event[1];
    },
    updateAvailableBuff(index, buffs) {
      this.allAvailableBuffs[index] = buffs
    },
    clearAll() {
      this.currentMember = 1;
      for (let i = 0; i < 5; ++i) {
        this.$refs["member" + i].clearAll();
      }
    }
  },
  computed: {
    totalHitPoint() {
      return this.partyHitPointList.reduce((sum, ele) => sum + ele, 0)
    },
    totalAttack() {
      return this.partyAttackList.reduce((sum, ele) => sum + ele, 0)
    },
    totalDamage() {
      let damage = [0, 0, 0, 0];
      this.partyDamageList.flat().forEach(dam => {
        damage[dam.attr] += dam.damage;
      })
      return damage;
    },
    vsAttrDamage() {
      let total = this.totalDamage[3] * 1.1;
      if (this.vsAttr == 3) {
        total += this.totalDamage[0]
        + this.totalDamage[1]
        + this.totalDamage[2];
      } else {
        total += this.totalDamage[this.vsAttr]
        + this.totalDamage[(this.vsAttr + 1) % 3] * 1.5
        + this.totalDamage[(this.vsAttr + 2) % 3] * 0.5;
      }
      return total;
    }
  }
}
</script>

<style scoped>

.result > p {
  font-weight: bold;
  font-size: 1.2em;
}


.vs-attr-container {
  /* width: 100%; */
  display: flex;
  justify-content: center;
  align-items: center;
}

.vs-attr-text {
  margin-right: .5em;
}

.vs-attr {
  display: flex;
  width: 60%;
  max-width: 300px;
  justify-content: space-between;
  align-items: center;
  margin: 20px 0;
}

.attr-selector {
  padding: 10px 15px;
  border: 2px solid black;
}

.attr-selector:hover {
  cursor: pointer;
}

.attr-selector.active {
  background-color: #5b6471;
  font-weight: bold;
  color: #eee;
}

.party-tab {
  display: flex;
  justify-content: center;
  width: 100%;
}

ul.tab {
  list-style: none;
  display: flex;
  justify-content: space-between;
  width: 90%;
  max-width: 400px;
  padding: 0;
  border-bottom: 5px solid #5b6471;
}

li.tab-item {
  /* margin: 0 10px; */
  padding: 10px 25px;
  display: block;
  border: 2px solid #5b6471;
  border-radius: 2px;
  cursor: pointer;
  border-bottom: none;
  box-sizing: content-box;
  font-size: 1.2em;
}

li.is-selected {
  background-color: #5b6471;
  /* border: 5px solid #5b6471; */
  color: #eee;
  font-weight: bold;
}

.party-member.not-selected {
  display: none;
}

/* @media screen and (min-width: 800px) {

.party-member-container {
  display: flex;
  justify-content: center;
  margin: 0 auto;
  overflow-x: scroll;
}

.party-member {
  margin: 0 30px;
  flex: 0 0 400px;
}

.party-member.not-selected {
  display: unset;
}

} */

</style>