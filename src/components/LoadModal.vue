<template>
  <transition name="fade">
    <div
      class="modal-wrapper"
      v-show="isOpened"
      @click.self="hide"
    >
      <div class="modal-container">
        <!-- <i class="fas fa-times" @click="hide" /> -->
        <div class="modal-text">
          <div class="text">
            保存されたデータを読み込みます。
          </div>
          <select
            v-model="dataName"
            @change="fillDetails"
          >
            <option disabled value="">データを選択してください</option>
            <option 
              v-for="c, i in savedDataNames"
              :key="'data-' + i"
              :value="c"
            >
              {{ c }}
            </option>
          </select>
          <div class="button-container">
            <button @click="deleteData" class="delete"> Delete </button>
            <button @click="loadData" class="ok"> OK </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  data () {
    return {
      isOpened: false,
      dataName: ""
    }
  },

  methods: {
    show () {
      this.isOpened = true;
    },

    hide () {
      this.dataName = "";
      this.isOpened = false;
    },

    loadData() {
      if (this.dataName) {
        this.$emit("load-data", this.dataName);
      }
      this.hide();
    },

    deleteData() {
      if (!confirm("「" + this.dataName + "」を削除しますか？")) {
        return;
      }
      if (this.dataName) {
        this.$emit("delete-data", this.dataName);
      }
      this.hide();
    }
  },

  props: {
    savedDataNames: Array
  },

  watch: {
    isOpened () {
      document.body.className = this.isOpened ? 'modal-opened' : '';
    }
  }
}
</script>

<style scoped>

.modal-wrapper {
  position: fixed;
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
  background: rgba(0,0,0,.75);
  z-index: 999;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-container {
  background-color: var(--color-background);
  width: 90%;
  max-width: 900px;
  height: auto;
  border-radius: 8px;
  position: relative;
  padding-top: 2.5em;
}

.modal-container > i {
  font-size: 2em;
  display: inline-block;
  line-height: 1;
  position: absolute;
  right: .2em;
  top: .2em;
}

.modal-text {
  height: auto;
  max-height: 100%;
  width: 90%;
  margin: 0 auto;
  overflow: auto;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity .3s ease;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.text {
  text-align: left;
  margin-bottom: .8em;
}

.button-container {
  display: flex;
  width: 60%;
  justify-content: space-between;
  margin: .8em auto 1.2em;
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

button.ok {
  color: var(--color-ok);
  border: 2px solid var(--color-ok);
}

button.delete {
  color: var(--color-warn);
  border: 2px solid var(--color-warn);
}

select {
  width: 90%;
  border: none;
  border-radius: 0;
  border-bottom: var(--color-border) solid 3px;
}

</style>