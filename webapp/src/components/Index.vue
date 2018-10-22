<template>
  <div v-if="device !== null" id="connect" @click="bleConnect">
    <font-awesome-icon :icon="['fab', 'bluetooth-b']" v-if="!requestBLEDevice"/>
    <font-awesome-icon :icon="['fal','spinner-third']" v-else spin/>
    <p>Click to connect.</p>
  </div>
  <div v-else id="control">
    <!--<p><font-awesome-icon :icon="['fal', 'lightbulb']"/>{{device !== null ? device.name : 'Bulb'}}</p>-->
    <ul id="payload_visualizer"><li  v-for="(color,index) in payload" v-bind:key="index" :style="`background: rgb(${color[0]},${color[1]},${color[2]})`"></li></ul>
    <div id="payload_input">
      <input placeholder="Payload" @focus="inputFocusEffect = true" @blur="inputFocusEffect = false" v-model="usrInput" id="payload" :class="{'input_focus_effect': inputFocusEffect}"/>
      <button @click="sendPayload" :class="{'input_focus_effect': inputFocusEffect}"><font-awesome-icon :icon="['fas', 'bolt']"/></button>
    </div>
    <div id="settings">
      <p>Base color: {{color}}, {{nbBits}}bits, {{xorPasswd.length > 0 ? 'Xored' : 'Not Xored'}} <font-awesome-icon :icon="['fas', 'cog']"/></p>
      <span>Base color:</span><el-color-picker v-model="usrColor" size="mini"></el-color-picker>
      <span>LSB Bits to use:</span> <el-slider v-model="nbBits" :step="1" :min="1" :max="8" :format-tooltip="formatBitsToolTip"></el-slider>
      <span>Xor Password:</span>
      <el-input placeholder="Password" v-model="xorPasswd">
        <font-awesome-icon slot="prefix" :icon="['fal','lock']"/>
      </el-input>
      <span>Sleep</span> <el-slider v-model="sleep" :step="0.5" :min="0" :max="5" :format-tooltip="formatSleepToolTip"></el-slider>
    </div>
  </div>
</template>

<script>
import sha256 from 'sha256'
export default {
  name: 'Bluetooth',
  data () {
    return {
      inputFocusEffect: false,
      requestBLEDevice: false,
      device: null,
      filters: [{services: ['0000ffe5-0000-1000-8000-00805f9b34fb']}],
      usrInput: 'Payload',
      nbBits: 4,
      usrColor: '#3A8EE6',
      xorPasswd: '',
      delay: 1,
      sleep: 1
    }
  },
  computed: {
    msg () {
      if (this.xorMsg.length > 0) {
        console.log(this.xorMsg.length)
        console.log(this.xorMsg)
        console.log(btoa(this.xorMsg))
        return this.xorMsg + '\x04'
      } else {
        return 'Skynet is Alive\x04'
      }
    },
    color () {
      return this.usrColor !== null ? this.usrColor : '#FFFFFF'
    },
    refColor () {
      let hexColor = this.color.slice(1)
      let a = []
      for (let i = 0, len = hexColor.length; i < len; i += 2) {
        a.push(parseInt(hexColor.substr(i, 2), 16))
      }
      return new Uint8Array(a)
    },
    payload () {
      let msgBinaryStr = this.msg
        .split('')
        .map((char) => '00'.concat(char.charCodeAt(0).toString(2)).slice(-8))
        .join('')
      let payloadColorsArray = []
      let color = this.refColor
      let mask = 256 - Math.pow(2, this.nbBits)
      if (!this.nbBits.isNaN) {
        while (msgBinaryStr.length % this.nbBits !== 0) {
          msgBinaryStr += '0'
        }
      }
      let i = 0
      for (i; msgBinaryStr.length > 0; i++) {
        let data = parseInt(msgBinaryStr.slice(0, this.nbBits), 2)
        msgBinaryStr = msgBinaryStr.substr(this.nbBits)
        if (i % 3 === 0) {
          payloadColorsArray.push([])
        }
        payloadColorsArray[Math.floor(i / 3)].push((color[i % 3] & mask) + data)
      }
      for (i; i % 3 !== 0; i++) {
        payloadColorsArray[Math.floor(i / 3)].push(color[i % 3])
      }
      return payloadColorsArray
    },
    xorMsg () {
      let xoredString = ''
      if (this.xorPasswd.length > 0) {
        let pass = sha256(this.xorPasswd, { asString: true })
        xoredString = this.xor(this.usrInput, pass)
      } else {
        xoredString = this.usrInput
      }
      return xoredString
    }
  },
  methods: {
    bleConnect: function () {
      try {
        this.requestBLEDevice = true
        navigator.bluetooth.requestDevice({filters: this.filters})
        // navigator.bluetooth.requestDevice({acceptAllDevices: true})
          .then(device => {
            console.log(`Connected to ${device.name}`)
            this.$notify({
              dangerouslyUseHTMLString: true,
              message: `<svg style="color: #3a8ee6; margin-right: 20px;" aria-hidden="true" data-prefix="fab" data-icon="bluetooth-b" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" class="svg-inline--fa fa-bluetooth-b fa-w-10"><path fill="currentColor" d="M196.48 260.023l92.626-103.333L143.125 0v206.33l-86.111-86.111-31.406 31.405 108.061 108.399L25.608 368.422l31.406 31.405 86.111-86.111L145.84 512l148.552-148.644-97.912-103.333zm40.86-102.996l-49.977 49.978-.338-100.295 50.315 50.317zM187.363 313.04l49.977 49.978-50.315 50.316.338-100.294z" class=""></path></svg> Connected to ${this.device !== null ? this.device.name : 'Bulb'}`
            })
            this.device = device
            this.requestBLEDevice = false
          })
          .catch(error => {
            this.requestBLEDevice = false
            console.log(error)
          })
      } catch (error) {
        console.log(error)
        this.requestBLEDevice = false
        this.$alert('<p style="text-align: justify;">Please make sure your web browser is up to date and has the Bluetooth Web API activated.<br>On chrome, Bluetooth Web API can be activated by enabling the flag <em style="background: #f0f0f0">chrome://flags/#enable-experimental-web-platform-features</em></p>', 'Bluetooth not found !', {
          confirmButtonText: 'OK',
          type: 'error',
          center: true,
          dangerouslyUseHTMLString: true
        })
      }
    },
    bleSendCommand: function (command) {
      let c = new Uint8Array(command.match(/.{1,2}/g).map(byte => parseInt(byte, 16)))
      console.log(c)
      if (typeof this.device !== 'undefined') {
        return this.device.gatt.connect()
          .then(server => {
            console.log(`Connected to ${server.device.name}`)
            return server.getPrimaryService('0000ffe5-0000-1000-8000-00805f9b34fb')
          })
          .then(service => {
            console.log(`Service: ${service.uuid}`)
            return service.getCharacteristic('0000ffe9-0000-1000-8000-00805f9b34fb')
          })
          .then(characteristic => {
            console.log(`Characteristic: ${characteristic.uuid}`)
            return characteristic.writeValue(c)
          })
      }
    },
    sendPayload: function () {
      let payload = this.payload
      let that = this;
      (async function loop () {
        for (let i = 0; i < payload.length; i++) {
          let command = `56${payload[i][0].toString(16)}${payload[i][1].toString(16)}${payload[i][2].toString(16)}00f0aa`
          try {
            await that.bleSendCommand(command)
            await new Promise(resolve => setTimeout(resolve, that.sleep * 1000))
          } catch (error) {
            console.log(error)
            break
          }
        }
      })()
    },
    xor: function (msg, pass) {
      let xor = ''
      for (let i = 0; i < msg.length; i++) {
        xor += String.fromCharCode(msg.charCodeAt(i) ^ pass.charCodeAt(i % pass.length))
      }
      return xor
    },
    formatBitsToolTip: function (value) {
      return value + ' bits'
    },
    formatSleepToolTip: function (value) {
      return value + 's'
    }
  }
}
</script>

<style scoped>
  #connect{
    color: #c8c4c8;
    text-align: center;
    cursor: pointer;
  }
  #connect .svg-inline--fa{
    width: 50px;
    height: 50px;
    padding: 20px;
    border-radius: 100px;
    box-shadow: 1px 1px 1px #e6e6e6;
    background: #03a8fd;
    color: #fff;
  }

  #control{
    text-align: center;
  }

  #control p{
    color: #c8c4c8;
  }

  #payload_input input,
  #payload_input button{
    font-size: 1em;
    border: none;
    box-shadow: 1px 1px 1px #f0f0f0;
    background: #f1f1f1;
    border: 1px solid rgba(0,0,0,0);
  }

  #payload_input input:focus,
  #payload_input button:focus{
    outline: none;
  }

  #payload_input input{
    padding: 15px;
    border-radius: 100px 0px 0px 100px;
    width: 30vw;
  }

  #payload_input button{
    padding: 15px 20px;
    border-radius: 0px 100px 100px 0px;
    margin-left: -4px;
  }

  #payload_input .input_focus_effect{
    border-top: 1px solid #b3bcc7;
    border-bottom: 1px solid #b3bcc7;
  }

  #payload_input input.input_focus_effect{
    border-left: 1px solid #b3bcc7;
  }

  #payload_input button.input_focus_effect{
    border-right: 1px solid #b3bcc7;
  }

  #payload_input button:hover{
    cursor: pointer;
    color: #3a8ee6;
  }

  #settings{
    display: block;
    overflow: hidden;
    animation: showSettings 0.5s ease-out;
    margin: 40px;
  }

  #payload_visualizer{
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    list-style: none;
    padding: 0px;
    width: 30vw;
    margin: auto;
    margin-bottom: 20px;
  }

  #payload_visualizer li{
    flex: 1;
    height: 15vh;
  }

  @keyframes showSettings {
    0%{
      margin-top: 0px;
      opacity: 0;
    }
    100%{
      margin-top: 40px;
      opacity: 1;
    }
  }
</style>
