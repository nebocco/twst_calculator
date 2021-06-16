<template>
  <transition name="fade">
    <div
      class="modal-wrapper"
      v-show="isOpened"
      @click.self="hide"
    >
      <div id="modal" class="modal-container">
        <!-- <i class="fas fa-times" @click="hide" /> -->
        <div class="modal-text">
          <div class="text">
            保存する名前を入力してください。<br>
            すでに存在している名前を入力すると上書きされます。
          </div>
          <div class="input-container">
            <input
              type="text"
              v-model="saveName"
            >
            <button
              @click="save"
            >
              OK
            </button>
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
      saveName: ""
    }
  },

  methods: {
    show() {
      this.isOpened = true;
    },

    hide() {
      this.isOpened = false;
    },

    save() {
      if (this.saveName) {
        this.$emit('save-data', this.saveName)
      }
      this.hide();
    }
  },

  props: {
    initialName: String,
  },

  watch: {
    isOpened () {
      document.body.className = this.isOpened ? 'modal-opened' : '';
    },

    initialName() {
      this.saveName = this.initialName;
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
  padding: .8em .4em;
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

.input-container {
  display: flex;
}

.text {
  text-align: left;
  margin-bottom: .8em;
}

input {
  flex: 1;
  width: 90%;
  max-width: 90%;
  border: none;
  border-radius: 0;
  border-bottom: var(--color-border) solid 3px;
  margin: 0;
}

button {
  padding: .4em 1.2em;
  margin-left: .4em;
  font-size: 1rem;
  text-align: center;
  text-decoration: none;
  white-space: nowrap;
  color: var(--color-ok);
  border: 2px solid var(--color-ok);
  border-radius: 4px;
  box-sizing: border-box;
  cursor: pointer;
}

button:hover {
  background: var(--color-background-third);
}

</style>