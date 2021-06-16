<template>
  <table class="buddy-lis">
    <tr>
      <th>キャラ</th>
      <th>効果</th>
      <th>Lv.</th>
    </tr>
    <tr
      v-for="(buddy, index) in buddiesExtended"
      :key="'buddy-' + index"
      :class="{ 'buddy-enabled': buddyEnabled[index] }"
    >
      <td>
        {{ buddy[0] == -1 ? "" : characterList[buddy[0]].name }}
      </td>
      <td>
        {{ effectText[index] }}</td>
      <td>
        <input 
          type="number"
          v-model.number="buddyLevel[index]"
          min="1"
          max="10"
          :name="'buddy-' + memberIndex + index"
          :disabled="!buddyEnabled[index]"
          @input="$emit('update:buffsBuddy', buffs)"
          @focus="
            levelStash[index] = buddyLevel[index];
            buddyLevel[index] = '';
          "
          @blur="buddyLevel[index] = buddyLevel[index] === '' ? levelStash[index] : Math.min(10, Math.max(1, buddyLevel[index]))"
        >
      </td>
    </tr>
  </table>
</template>

<script>
export default {
  data() {
    return {
      effectTextBase: [
        "ATK UP（小）",
        "ATK UP（中）",
        "HP UP（小）",
        "HP UP（中）",
      ],
      buddyLevel: [1, 1, 1],
      levelStash: [1, 1, 1],
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
    },
    memberIndex: {
      type: Number,
      required: true
    }
  },
  methods: {
    clearAll() {
      this.buddyLevel = [1, 1, 1];
    },
    loadStorage(level) {
      this.buddyLevel = level;
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
          for (let i = 0; i < 4; i++) {
            res[Math.floor(i / 2)] += 
              (buddy[1] >> i & 1) == 0 ? 0 :
              0.1 * (i % 2 + 1)
              + 0.005 * ((i == 1) + 2) * this.buddyLevel[index];
          }
        }
      });
      return res;
    },
    buddyEnabled() {
      return this.buddiesExtended.map((buddy) =>
        buddy[0] !== -1 && this.partyMember.includes(buddy[0])
      )
    },
    effectText() {
      let text = this.buddiesExtended
      .map((buddy) => {
        if (buddy[0] == -1) { return ""; }
        let t = []
        for (let i = 0; i < 4; ++i) {
          if (buddy[1] >> i & 1) {
            t.push(this.effectTextBase[i])
          }
        }
        return t.join(" & ")
      })
      return text;
    }
  },
  watch: {
    buffs: {
      handler() {
        this.$emit('update:buffsBuddy', this.buffs)
      },
      deep: true
    },
    buddyLevel: {
      handler() {
        this.$emit("update:buddyLevel", this.buddyLevel);
      },
      deep: true
    }
  }
}
</script>

<style scoped>

tr, td, th {
  border: none;
  background: none;
}

th {
  color: #5b6471;
  border-bottom: 2px solid #5b6471;
}

td {
  color: #aaa;
  border-bottom: 1px solid #ddd;
  padding: .2em 0;
}

tr.buddy-enabled > td {
  font-weight: bold;
  color: #333;
}

td:first-child {
  width: 30%;
}

td:last-child {
  width: 20%;
}

label {
  margin: 0;
}

input {
  width: 100%;
  padding: 0.2em 0.4em;
  margin: 0;
  background: none;
  border: 1px solid #c5c5de;
  border-radius: 0;
  text-align: end;
}

input[disabled] {
  color: #aaa;
  background: #f2f4f6;
}

input:invalid {
  border-color: red;
  background: #eecccc;
}

</style>