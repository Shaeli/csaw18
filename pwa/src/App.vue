<template>
  <div id="app">
    <header>
      <h1>Magic Blue</h1>
      <div id="rainbow_gradient"></div>
    </header>
    <main>
      <router-view/>
    </main>
    <footer>
    </footer>
  </div>
</template>

<script>
export default {
};
</script>

<style>
body{
  margin: 0px;
  padding: 0px;
  background: #000;
  color: #fff;
  font-family: sans-serif;
}

#app{
  width: 100vw;
  height: 100vh;
  box-sizing: border-box;
}

header{
  display: block;
  width: 100%;
  height: 60px;
  text-align: center;
  background: #000;
  position: fixed;
  line-height: 60px;
  z-index: 100;
}

header h1{
  margin: 0px;
  padding: 0px;
  font-size: 1.2em;
  font-weight: 300;
  vertical-align: middle;
}

#rainbow_gradient{
  display: block;
  height: 2px;
  width: 100%;
  background: linear-gradient(to right, orange , yellow, green, cyan, blue, violet);
  position: absolute;
  bottom: 0;
}

main{
  position: relative;
  z-index: 1;
  padding-top: 60px;
  padding-bottom: 60px;
  background: #303030;
  min-height: 100vh;
  max-width: 100vw;
  overflow-x: hidden;
  overflow-y: auto;
  width: 100vw;
  display: flex;
  box-sizing: border-box;
}

footer{
  position: fixed;
  top: calc(100vh - 60px);
  display: block;
  width: 100%;
  height: 60px;
  background: #000;
  z-index: 100;
}

.button{
  color: #303030;
  border: 1px solid #6fb833;
  background: #6fb833;
  padding: 10px;
  font-size: 1em;
  font-weight: 500;
  border-radius: 5px;
  box-sizing: border-box;
}
</style>
