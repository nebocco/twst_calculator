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
        カードの基本情報を入力します。
      </li>
    </ol>

    <div class="help-example help-example-1">
      <div class="card-box">
        <div class="card-detail">
          <select disabled>
            <option disabled selected value="-1">リドル</option>
          </select>
        </div>
        <div class="card-detail">
          <select disabled>
            <option disabled selected value="-1">寮服</option>
          </select>
        </div>
      </div>

      <div class="status-box">
        <div class="status-each">
          <label for="hit-point">HP</label>
          <input
            type="number"
            value="0"
            disabled
          >
        </div>
        <div class="status-each">
          <label for="attack">ATK</label>
          <input
            type="number"
            value="0"
            disabled
          >
        </div>
      </div>

    </div>

    <ol start="2">
      <li>
        有効になっているバディに色が付くので、レベルを入力します。
      </li>
    </ol>

    <div class="help-example help-example-2">
      <table class="buddy-lis">
        <tr>
          <th>キャラ</th>
          <th>効果</th>
          <th>Lv.</th>
        </tr>
        <tr>
          <td>ケイト</td>
          <td>ATK UP（小）</td>
          <td>
            <input type="number" value="1" disabled>
          </td>
        </tr>
        <tr class="buddy-enabled">
          <td>アズール</td>
          <td>HP UP（小）</td>
          <td>
            <input type="number" value="8" disabled class="not-disabled">
          </td>
        </tr>
        <tr>
          <td>トレイ</td>
          <td>HP UP（中）</td>
          <td>
            <input type="number" value="1" disabled>
          </td>
        </tr>
      </table>
    </div>

    <ol start="3">
      <li>
        魔法レベルを入力します。<br>
        DUOの効果を有効にする場合は、チェックボックスに印を付けます。
      </li>
    </ol>
    
    <div class="help-example help-example-3">
      <div class="magic-container">
        <div class="magic-name">
          <h4>ファイアショット[II]</h4>
          <label for="magicLevel">Lv.</label>
          <input
            type="number"
            value="7"
            disabled
          />
        </div>
        <p class="damage">
          damage: <span class="damage-number"> 0 </span>
        </p>
        <div class="magic-description">
          <dl>
            <dt>説明</dt>
            <dd>２連撃の火属性ダメージ(弱)</dd>
            <dt>追加効果</dt>
            <dd>
              [DUO]3連撃に強化（アズール）
              <input type="checkbox" name="DuoEnable" checked/>
            </dd>
          </dl>
        </div>

      </div>
    </div>

    <ol start="4">
      <li>
        味方のバフがかかるよう設定したい場合は「その他のバフ」から追加できます。
      </li>
    </ol>
    
    <div class="help-example help-example-4">
      <div class="accordion">
        <div class="title">
          <div class="title-text">
            その他のバフ (1)
          </div>
          <i class="fas fa-chevron-up" />
        </div>
        <div class="accordion-content">
          <div class="other-buffs">
            <ul class="buffs-list">
              <li class="selected-buffs">
                <div class="buff-name">
                  ダメージ UP（小）（ケイト【式典服】）
                </div>
                <button disabled>
                  <i class="fas fa-times" />
                </button>
              </li>
              <li class="add-buff">
                <select disabled>
                  <option disabled value="" selected>バフを追加</option>
                </select>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    
    
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
        バフ・デバフの効果は、自身へのATK UP・ダメージ UPのみを計算対象に入れています。
      </li>
      <li>
        バディレベルは現在有効なもののみが入力可能で、
        「その他のバフ」で選択できるのは味方の魔法によって発動されるものだけです。
        そのため、最初に5人分の基本情報を入力してから以降の欄を埋めることをおすすめします。
      </li>
      <li>
        より詳細な使い方は作者ブログで公開しています。
      </li>
      <li>
        分からないことやバグの報告、改善してほしい箇所などあれば作者Twitter()までお気軽にご連絡ください。
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

ol {
  margin: 0px;
}

li {
  margin-top: .4rem;
  text-align: left;
}


/* example */

.help-example {
  margin: 20px 10px 35px;
  padding: 5px;
  border: 1px dotted gray;
}

/* help 1 */

.help-example-1 .card-box {
  display: flex;
}

.help-example-1 .card-box .card-detail {
  flex: 1;
}

.help-example-1 .card-box .card-detail select:disabled {
  display: inline-block;
  width: 90%;
  background: none;
  border: none;
  border-radius: 0;
  color: #333;
  border-bottom: #333 solid 3px;
  opacity: unset;
}

.help-example-1 .status-box {
  display: flex;
}

.help-example-1 .status-each {
  flex: 1;
}

.help-example-1 .status-each > label {
  min-width: 3em;
  margin-top: .5em;
  margin-bottom: 0;
}

.help-example-1 .status-each > input:disabled {
  width: 90%;
  max-width: 90%;
  background: none;
  border: none;
  border-radius: 0;
  color: #333;
  border-bottom: #333 solid 3px;
  text-align: right;
  opacity: unset;
}

/* help 2 */

.help-example-2 tr,
.help-example-2 td,
.help-example-2 th {
  border: none;
  background: none;
}

.help-example-2 th {
  color: #667;
  border-bottom: 2px solid #114;
}

.help-example-2 td {
  color: #aaa;
  border-bottom: 1px solid #ddd;
  padding: .2em 0;
}

.help-example-2 tr.buddy-enabled > td {
  font-weight: bold;
  color: #114;
}

.help-example-2 td:last-child {
  width: 25%;
}

.help-example-2 td:first-child {
  width: 30%;
}

.help-example-2 label {
  margin: 0;
}

.help-example-2 input {
  width: 100%;
  background: #fafbfc;
  padding: 0.2em 0.4em;
  margin: 0;
  border: none;
  border-radius: 0;
  background: none;
  text-align: end;
}

.help-example-2 input:disabled {
  color: #aaa;
  background: #f2f4f6;
}

.help-example-2 input.not-disabled {
  color: unset;
  background: unset;
}

/* help 3 */

.help-example-3 h4 {
  display: inline-block;
  font-size: 1.2em;
  margin-right: .2em;
}

.help-example-3 dl {
  margin: 10px 0;
  display: flex;
  flex-wrap: wrap;
}

.help-example-3 dt {
  width: 35%;
  padding: 10px;
  background-color: #DADADA;
  margin: 0 0 10px 0;
  border-top-left-radius: 3px;
  border-bottom-left-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.help-example-3 dd {
  width: 65%;
  padding: 10px;
  background-color: #F3F3F3;
  margin: 0 0 10px 0;
  border-top-right-radius: 3px;
  border-bottom-right-radius: 3px;
}

.help-example-3 dd::before {
  content: "";
}

.help-example-3 .magic-name {
  display: flex;
  align-items: baseline;
}

.help-example-3 .magic-name > h4 {
  flex-grow: 1;
}

.help-example-3 label {
  margin-right: .6em;
}

.help-example-3 input {
  width: 20%;
  text-align: right;
}

/* help 4 */

.help-example-4 ul.buffs-list {
  list-style: none;
  padding-left: 0;
}

.help-example-4 li.selected-buffs {
  border: 2px solid gray;
  border-radius: 3px;
  display: flex;
  justify-content: space-between;
}

.help-example-4 .selected-buffs > div {
  padding: 10px 20px;

}

.help-example-4 .selected-buffs button:disabled {
  width: 15%;
  max-width: 40px;
  background: none;
  color: #333;
  opacity: unset;
  cursor: unset;
}

.help-example-4 .buffs-list select:disabled {
  width: 100%;
  opacity: unset;
}

.help-example-4 .buff-name {
  display: inline-block;
}

.help-example-4 .title {
  margin-bottom: 10px;
  padding: 10px;
  border-bottom: 2px solid gray;
  text-align: left;
}

.help-example-4 .title > div {
  display: inline-block;
  font-weight: bold;
}

.help-example-4 .title i {
  float: right;
  line-height: 1.3;
}

.help-example-4 .content {
  padding: 0 15px;
  margin-bottom: 10px;
}

</style>