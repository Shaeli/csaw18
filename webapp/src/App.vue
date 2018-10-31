<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
  @import url('https://fonts.googleapis.com/css?family=Roboto');
  body{
    font-family: 'Roboto', sans-serif;
    background: #fefefe;
  }
  #app {
    display: flex;
    width: 100vw;
    height: 100vh;
    justify-content: center;
    align-items: center;
  }
</style>
