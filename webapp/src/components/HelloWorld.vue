<template>
  <div>
    Msg:
    <input type="text" v-model="msg"/>
    Nb bits:
    <input type="number" v-model="nbBits"/>
    Base color:
    <input type="color" v-model="color"/>
    <div v-for="(color,index) in payload" v-bind:key="index">
      <p>{{`${index}: ${color[0]} ${color[1]} ${color[2]}`}}
        <span :style="`display: inline-block; width: 20px; height: 20px; border: 1px solid black; background:rgb(${color[0]},${color[1]},${color[2]})`"></span>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Coucou toi :)',
      nbBits: 4,
      color: '#FFFFFF'

    }
  },
  computed: {
    refColor () {
      let hexColor = this.color.slice(1)
      let a = []
      for (let i = 0, len = hexColor.length; i < len; i += 2) {
        a.push(parseInt(hexColor.substr(i, 2), 16))
      }
      return new Uint8Array(a)
    },
    payload: function () {
      let msgBinaryStr = this.msg
        .split('')
        .map((char) => '00'.concat(char.charCodeAt(0).toString(2)).slice(-8))
        .join('')
      let payloadByteArray = []
      let color = this.refColor
      let mask = 256 - Math.pow(2, this.nbBits)
      if (!this.nbBits.isNaN) {
        while (msgBinaryStr.length % this.nbBits !== 0) {
          msgBinaryStr += '0'
        }
      }
      console.log('Binary string: ')
      console.log(msgBinaryStr.replace(/(.{4})/g, '$1 '))
      let i = 0
      for (i; msgBinaryStr.length > 0; i++) {
        let data = parseInt(msgBinaryStr.slice(0, this.nbBits), 2)
        msgBinaryStr = msgBinaryStr.substr(this.nbBits)
        if (i % 3 === 0) {
          payloadByteArray.push([])
        }
        payloadByteArray[Math.floor(i / 3)].push((color[i % 3] & mask) + data)
      }
      for (i; i % 3 !== 0; i++) {
        payloadByteArray[Math.floor(i / 3)].push(color[i % 3])
      }
      console.log(`RGB Array. Base color: ${this.color}. ${this.nbBits} bits per color channel.`)
      console.log(payloadByteArray)
      return payloadByteArray
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
