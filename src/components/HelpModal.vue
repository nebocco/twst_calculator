<template>
  <transition name="fade">
  <div
    class="modal-wrapper"
    v-show="isOpened"
    @click.self="hide"
  >
  <div id="modal" class="modal-container">
  <i class="fas fa-times" @click="hide" />
  <div class="modal-text">
    <div class="modal-head">
      <h3>使い方</h3>
    </div>
    <ol>
      <li>
        まずはメンバー５人の基本情報を入力します。
      </li>
      画像
      <li>
        有効になっているバディに色が付くので、レベルを入力します。
      </li>
      画像

      <li>
        魔法レベルを入力します。
      </li>

      画像

      <li>
        DUOの効果を有効にする場合は、チェックボックスに印を付けます。
      </li>

      画像


      <li>
        味方のバフがかかるよう設定したい場合は「その他のバフ」から追加できます。
      </li>

      画像


    </ol>
    
    <!-- <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br> -->
    <h4>注意</h4>
    <ul>
      <li>
          自身へのATK UP・ダメージ UPのみを計算対象に入れています。
      </li>
    </ul> 
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
    }
  },

  methods: {
    show () {
      this.isOpened = true;
    },

    hide () {
      this.isOpened = false;
    },
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
  background-color: white;
  width: 85%;
  max-width: 900px;
  height: 90%;
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
  width: 95%;
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

li {
  margin-top: .4rem;
  text-align: left;
}
</style>