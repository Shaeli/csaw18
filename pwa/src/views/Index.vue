<template>
  <div id="pair" v-if="device !== null">
    <div>
      <font-awesome-icon icon="lightbulb-slash" id="no_bulb_icon"/>
      <h2>No device paired !</h2>
    </div>
    <div class="button" @click="bleConnect">Add a new device</div>
    <div id="install_pop_up" v-if="installPrompt !== null" @click="showInstallPrompt">
      <div>
      <img alt="Vue logo" src="../assets/logo.png">
      <h1>Click and select add to homescreen to install our Magic Blue app !</h1>
      </div>
    </div>
  </div>
  <div id="wrapper" v-else>
    <div id="program" v-if="!sending">
      <h3>Connected to {{this.device !== null ? this.device.name : 'Bulb'}}</h3>
      <ul id="payload_visualizer"><li  v-for="(color,index) in payload" v-bind:key="index" :style="`background: rgb(${color[0]},${color[1]},${color[2]})`"></li></ul>
      <div id="settings">
        <p>{{color}}, {{nbBits}}bits, {{sleep}}s delay, {{xorPasswd.length > 0 ? 'Xored' : 'Not Xored'}}</p>
        <ul>
          <li> <input placeholder="Payload" v-model="usrInput"/></li>
          <li>
            <input placeholder="Xor password" v-model="xorPasswd"/>
          </li>
          <li><span class="range" @click="decrNbBits()">-</span><span>{{nbBits}} bits</span><span class="range" @click="incrNbBits()">+</span></li>
          <li><span class="range" @click="decrDelay()">-</span><span>{{sleep}}s delay</span><span class="range" @click="incrDelay()">+</span></li>
          <li><span>Base color : </span><input type="color" v-model="usrColor" value="#fffff"/></li>
        </ul>
      </div>
      <button @click="sendPayload" class="button">Send !</button>
    </div>
    <div v-else id="sending_indicator">
      <div>
        <font-awesome-icon icon="spinner-third" spin class="spinner"/>
        <p v-if="step < payload.length">Sending command {{step + 1}} of {{payload.length}} - {{remainingTime}}s remaining</p>
      </div>
    </div>
  </div>
</template>

<script>
  /* eslint-disable */

  import sha256 from 'sha256';

  export default {
    name: 'Index',
    data() {
      return {
        device: null,
        filters: [{ services: ['0000ffe5-0000-1000-8000-00805f9b34fb'] }],
        usrInput: 'Payload',
        nbBits: 4,
        usrColor: '#6fb833',
        xorPasswd: '',
        delay: 1,
        sleep: 1,
        sending: false,
        step: 0,
        installPrompt: null
      };
    },
    computed: {
      msg() {
        if (this.xorMsg.length > 0) {
          return `${this.xorMsg}\x04`;
        }
        return 'Skynet is Alive\x04';
      },
      color() {
        return this.usrColor !== null ? this.usrColor : '#FFFFFF';
      },
      refColor() {
        const hexColor = this.color.slice(1);
        const a = [];
        for (let i = 0, len = hexColor.length; i < len; i += 2) {
          a.push(parseInt(hexColor.substr(i, 2), 16));
        }
        return new Uint8Array(a);
      },
      payload() {
        let msgBinaryStr = this.msg
          .split('')
          .map(char => '00'.concat(char.charCodeAt(0).toString(2)).slice(-8))
          .join('');
        const payloadColorsArray = [];
        const color = this.refColor;
        const mask = 256 - Math.pow(2, this.nbBits);
        if (!this.nbBits.isNaN) {
          while (msgBinaryStr.length % this.nbBits !== 0) {
            msgBinaryStr += '0';
          }
        }
        let i = 0;
        for (i; msgBinaryStr.length > 0; i++) {
          const data = parseInt(msgBinaryStr.slice(0, this.nbBits), 2);
          msgBinaryStr = msgBinaryStr.substr(this.nbBits);
          if (i % 3 === 0) {
            payloadColorsArray.push([]);
          }
          payloadColorsArray[Math.floor(i / 3)].push((color[i % 3] & mask) + data);
        }
        for (i; i % 3 !== 0; i++) {
          payloadColorsArray[Math.floor(i / 3)].push(color[i % 3]);
        }
        return payloadColorsArray;
      },
      xorMsg() {
        let xoredString = '';
        if (this.xorPasswd.length > 0) {
          const pass = sha256(this.xorPasswd, { asString: true });
          xoredString = this.xor(this.usrInput, pass);
        } else {
          xoredString = this.usrInput;
        }
        return btoa(xoredString);
      },
      remainingTime() {
        return (this.payload.length - this.step) * this.sleep;
      },
    },
    methods: {
      bleConnect() {
        try {
          navigator.bluetooth.requestDevice({ filters: this.filters })
          //navigator.bluetooth.requestDevice({acceptAllDevices: true})
            .then((device) => {
              console.log(`Connected to ${device.name}`);
              this.device = device;
            })
            .catch((error) => {
              console.log(error);
            });
        } catch (error) {
          console.log(error);
        }
      },
      bleSendCommand(command) {
        const c = new Uint8Array(command.match(/.{1,2}/g).map(byte => parseInt(byte, 16)));
        if (typeof this.device !== 'undefined') {
          return this.device.gatt.connect()
            .then((server) => {
              console.log(`Connected to ${server.device.name}`);
              return server.getPrimaryService('0000ffe5-0000-1000-8000-00805f9b34fb');
            })
            .then((service) => {
              console.log(`Service: ${service.uuid}`);
              return service.getCharacteristic('0000ffe9-0000-1000-8000-00805f9b34fb');
            })
            .then((characteristic) => {
              console.log(`Characteristic: ${characteristic.uuid}`);
              return characteristic.writeValue(c);
            });
        }
      },
      sendPayload() {
        const payload = this.payload;
        const that = this;
        this.sending = true;
        (async function loop() {
          for (let i = 0; i < payload.length; i++) {
            const command = `56${payload[i][0].toString(16)}${payload[i][1].toString(16)}${payload[i][2].toString(16)}00f0aa`;
            try {
              await that.bleSendCommand(command);
              await new Promise(resolve => setTimeout(resolve, that.sleep * 1000));
            } catch (error) {
              console.log(error);
              break;
            }
            that.step += 1;
          }
          setTimeout(() => {
            that.step = 0;
            that.sending = false;
          }, 3000);
        }());
      },
      xor(msg, pass) {
        let xor = '';
        for (let i = 0; i < msg.length; i++) {
          xor += String.fromCharCode(msg.charCodeAt(i) ^ pass.charCodeAt(i % pass.length));
        }
        return xor;
      },
      decrNbBits(){
        if (this.nbBits > 1){
          this.nbBits -= 1
        }
      },
      incrNbBits(){
        if (this.nbBits < 8){
          this.nbBits += 1
        }
      },
      decrDelay(){
        if (this.sleep > 0){
          this.sleep -= 1
        }
      },
      incrDelay(){
        if (this.sleep < 10){
          this.sleep += 1
        }
      },
      showInstallPrompt() {
        this.installPrompt.prompt()
        this.installPrompt.userChoice
          .then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
              this.installPrompt = null
            }
          })
      }
    },beforeCreate() {
      window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault()
        this.installPrompt = e
      })
    }
  };
</script>

<style scoped>
  #wrapper{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
  #program{
    color: #aaaaaa;
    text-align: center;
    flex: 1;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    flex-direction: column;
    padding: 0px 0px 20px 0px;
  }

  #program h3{
    padding: 0px;
    margin: 0px;
  }
  #payload_visualizer{
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    list-style: none;
    padding: 0px;
    width: 90vw;
  }

  #payload_visualizer li {
    flex: 1;
    height: 50px;
    border: solid 1px #000;
  }

  input{
    background: #1a1a1a;
    border: solid 1px #000;
    color: #aaaaaa;
    font-size: 1em;
    padding: 10px;
    width: 70vw;
  }

  #settings ul{
    padding: 0px;
    list-style: none;
  }

  #settings ul li{
    margin: 20px;
  }

  #settings input[type="color"]{
    padding: 0px;
    background: none;
    border: none;
    margin: auto;
    width: 30px;
    height: 30px;
    vertical-align: middle;
    margin-left: 15px;
  }

  #settings .range{
    margin: 0px 20px;
    font-size: 1.5em;
    font-weight: 600;
    background: #6fb833;
    width: 30px;
    height: 30px;
    line-height: 30px;
    display: inline-block;
    border-radius: 100px;
    color: #303030;
  }

  #sending_indicator{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    color: #6fb833;
  }

  #sending_indicator .spinner{
    font-size: 3em;
  }

  #pair{
    text-align: center;
    color: #aaaaaa;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    flex: 1;
    flex-direction: column;
  }

  #pair #no_bulb_icon{
    font-size: 4em;
  }

  #pair h2{
    font-size: 1.2em;
    font-weight: 800;
    text-align: center;
  }

  #install_pop_up{
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100vw;
    height: 100vh;
    background: #000;
    box-sizing: border-box;
    position: fixed;
    top: 0;
    left: 0;
  }

  #install_pop_up img{
    width: 150px;
  }

  #install_pop_up h1{
    font-size: 1.2em;
    font-weight: 600;
    width: 80%;
    margin: auto;
    margin-top: 20px;
  }
</style>
