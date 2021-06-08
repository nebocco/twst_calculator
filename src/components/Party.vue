<template>
  <p>Total HP: {{ totalHitPoint }}</p>
  <p>Total ATK: {{ totalAttack }}</p>
  <p>attr Damage: {{ totalDamage }}</p>
  <p>total Damage: {{ vsAttrDamage }}</p>
  <!-- {{ partyDamageList }} -->
  <!-- {{ vsAttr }} -->
  <div class="vs-attr">
    <div
      class="attr-selector"
      v-for="i in 4"
      :key="i"
      :class="{ active: vsAttr === i-1}"
      @click="vsAttr = i-1"
    >
      {{ attrs[i-1] }}
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
        :characterList="staticData.characters"
        :costumeList="staticData.costumes"
        :cardList="staticData.cards"
        :magicList="staticData.magics"
        :partyMember="partyMember"
        :allAvailableBuffs="allAvailableBuffs.flat()"
        v-for="i in 5"
        :key="i"
        v-show="currentMember === i"
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

.vs-attr {
  display: flex;
  width: 30%;
  justify-content: space-between;
  align-items: center;
  margin: 20px auto;
}

.attr-selector {
  padding: 10px 15px;
  border: 2px solid black;
}

.attr-selector:hover {
  cursor: pointer;
}

.attr-selector.active {
  background-color: gray;
}

ul.tab {
  list-style: none;
  display: flex;
}

li.tab-item {
  padding: 10px 20px;
  display: block;
  border: 2px solid #eee;
  border-radius: 10px 10px 0 0;
  cursor: pointer;
}

li.is-selected {
  background-color: #eee;
}

</style>