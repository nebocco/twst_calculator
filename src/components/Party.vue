<template>
  <p>Total HP: {{ totalHitPoint }}</p>
  <p>Total ATK: {{ totalAttack }}</p>
  <div class="party-member">
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
    <PartyMember 
      :characterList="staticData.characters"
      :costumeList="staticData.costumes"
      :cardList="staticData.cards"
      :magicList="staticData.magics"
      :partyMember="partyMember"
      v-for="i in 5"
      :key="i"
      v-show="currentMember === i"
      @select-card="partyMember[i-1] = $event"
      @update:HP-ATK="updateStatus(i-1, $event)"
    />
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
      partyAttackList: [0, 0, 0, 0, 0]
    }
  },
  components: {
    PartyMember,
  },
  methods: {
    updateStatus(index, event) {
      this.partyHitPointList[index] = event[0];
      this.partyAttackList[index] = event[1];
    }
  },
  computed: {
    totalHitPoint() {
      return this.partyHitPointList.reduce((sum, ele) => sum + ele, 0)
    },
    totalAttack() {
      return this.partyAttackList.reduce((sum, ele) => sum + ele, 0)
    }
  }
}
</script>

<style scoped>

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