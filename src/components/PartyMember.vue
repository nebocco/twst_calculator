<template>
<div class="party-member">
  <h3>カード</h3>
  <div class="card-box">
    <div class="card-detail">
      <select
        name="characterName"
        v-model="Name"
        @change="fillDetails"
      >
        <option value="-1">名前</option>
        <option 
          v-for="c in filteredCharacters"
          :key="c.id"
          :value="c.id"
        >
          {{ c.name }}
        </option>
      </select>
    </div>
    <div class="card-detail">
      <select
        name="characterCostume"
        v-model="Costume"
        @change="fillDetails"
      >
        <option value="-1">コスチューム</option>
        <option 
          v-for="c in filteredCostumes"
          :key="c.id"
          :value="c.id"
        >
          {{ c.name }}
        </option>
      </select>
    </div>
  </div>
  {{ buffsBuddy }}
  <div class="status-box">
    <div class="status-each">
      <label for="hit-point">HP</label>
      <input
        type="number"
        id="hit-point"
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
        id="attack"
        v-model.number="Attack"
        min=0
        onfocus="if(this.value==0)this.value='';"
        onblur="if(this.value=='')this.value=0;"
      >
    </div>
  </div>
  <Buddy
    :buddies="Buddies"
    :characterList="characterList"
    :partyMember="partyMember"
    @update:buffsBuddy="buffsBuddy = $event"
  />
  <h3>魔法</h3>
  <Magic 
    key="magic1"
    :magic="Magics[0]"
    :magicList="magicList"
    :BaseAttack=affectedAttack
    @update:totalDamage="$emit('update:totalDamage', [0, $event])" 
  />
  <Magic
    key="magic2"
    :magic="Magics[1]"
    :magicList="magicList"
    :BaseAttack = affectedAttack
    @update:totalDamage="$emit('update:totalDamage', [1, $event])" 
  />
</div>
</template>

<script>
import Buddy from './Buddy.vue'
import Magic from './Magic.vue'

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
    }
  },
  methods: {
    fillDetails() {
      if(this.Name < 0 || this.Costume < 0) {
        return
      }
      const card = this.cardList[this.cardReverseIndex[this.Name][this.Costume]];
      this.Buddies = card.buddies;
      this.Magics = card.magics;
      this.$emit('select-card', this.Name);
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
    }
  },
  components: {
    Buddy,
    Magic
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

    affectedHitPoint() {
      return Math.floor(this.HitPoint * (1 + this.buffsBuddy[0]))
    },

    affectedAttack() {
      return Math.floor(this.Attack * (1 + this.buffsBuddy[1]))
    }
  },
  watch: {
    affectedHitPoint() {
      this.$emit('update:HP-ATK', [this.affectedHitPoint, this.affectedAttack])
    },
    affectedAttack() {
      this.$emit('update:HP-ATK', [this.affectedHitPoint, this.affectedAttack])
    }
  }
}
</script>

<style scoped>

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

.card-detail > select {
  width: 90%;
}

.card-detail > select > option:first-child {
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
  margin-right: 1em;
}

.status-each > input {
  width: 90%;
  max-width: 90%;
}

</style>