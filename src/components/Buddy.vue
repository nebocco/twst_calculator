<template>
  <h3>バディ</h3>
  <!-- {{ buddyEnabled }} -->
  <!-- {{ buffs }} -->
  <table class="buddy-lis">
    <tr>
      <th>キャラ</th>
      <th>効果</th>
      <th>Lv.</th>
    </tr>
    <tr
      v-for="(buddy, index) in buddiesExtended"
      :key="buddy[0]"
      :class="{ 'buddy-enabled': buddyEnabled[index] }"
    >
      <td>
        {{ buddy[0] == -1 ? "" : characterList[buddy[0]].name }}
      </td>
      <td>{{ buddy[0] == -1 ? "" : effectText[buddy[1]]}}</td>
      <td>
        <input 
          type="number" 
          min=1
          max=10
          :id="buddy[0]"
          :name="buddy[0]"
          :disabled="!buddyEnabled[index]"
          v-model.number="buddyLevel[index]"
          @input="$emit('update:buffsBuddy', buffs)"
        >
      </td>
    </tr>
  </table>
</template>

<script>
export default {
  data() {
    return {
      effectText: [
        "ATK UP（小）",
        "ATK UP（中）",
        "HP UP（小）",
        "HP UP（中）",
      ],
      buddyLevel: [1, 1, 1],
      attackBuff: [1, 1, 1],
      hpBuff: [1, 1, 1],
    }
  },
  props: {
    buddies: {
      type: Array,
      required: true
    },
    characterList: {
      type: Array,
      required: true
    },
    partyMember: {
      type: Array,
      required: true
    }
  },
  computed: {
    buddiesExtended() {
      let res = this.buddies.slice();
      for(let i=res.length; i < 3; i++) {
        res.push([-1, -1])
      }
      return res;
    },
    buffs() {
      let res = [0, 0]; // atk, hp
      this.buddies.forEach((buddy, index) => {
        if(this.buddyEnabled[index]) {
          res[Math.floor(buddy[1] / 2)] += 
            0.1 * (buddy[1] % 2 + 1) + 0.005 * (buddy[1] % 2 + 2) * this.buddyLevel[index];
        }
      });
      return res;
    },
    buddyEnabled() {
      return this.buddiesExtended.map((buddy) =>
        buddy[0] !== -1 && this.partyMember.includes(buddy[0])
      )
    },
  },
  watch: {
    buffs: {
      handler() {
        this.$emit('update:buffsBuddy', this.buffs)
      },
      deep: true
    }
  }
}
</script>

<style scoped>

th {
  color: #667;
}

tr > td {
  color: #aaa;
}

tr.buddy-enabled > td {
  font-weight: bold;
  color: #114;
}

tr > td:last-child {
  width: 20%;
}

tr > td:first-child {
  width: 30%;
}

tr, td, th {
  border: none;
  background: none;
}

td {
  border-bottom: 1px solid #ddd;
  padding: .2em 0;
}

th {
  border-bottom: 2px solid #114;
}

td > label {
  margin: 0;
}

input {
  width: 100%;
  background: #fafbfc;
}

input[disabled] {
  color: #aaa;
  background: #f2f4f6;
}

td > input {
  padding: 0.2em 0.4em;
  margin: 0;
  border: none;
  border-radius: 0;
  background: none;
  text-align: end;
}

</style>