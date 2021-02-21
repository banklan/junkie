<template>
  <v-app>
    <Navbar />
    <!-- <v-btn dark color="pink darken--2">Go to Home</v-btn> -->
    <v-main>
      <router-view></router-view>
    </v-main>
    <FooterNav />
  </v-app>
</template>

<script>
import Navbar from './components/includes/Navbar'
import FooterNav from './components/includes/Footer'

export default {
  name: 'App',
  components: {
    Navbar, FooterNav
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  /* color: #2c3e50; */
  /* margin-top: 60px; */
}
</style>
