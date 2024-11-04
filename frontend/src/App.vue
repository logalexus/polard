<template>
  <v-responsive>
    <v-app :theme="theme">
      <v-app-bar :elevation="1">
        <template v-slot:prepend>
          <v-app-bar-nav-icon @click="rail = !rail"></v-app-bar-nav-icon>
          <v-app-bar-title>CryptoLab</v-app-bar-title>
          <v-icon :icon="mdiTestTube"></v-icon>
        </template>
        <template v-slot:append>
          <v-btn :icon="mdiWeatherSunny" @click="theme = theme === 'light' ? 'dark' : 'light'"></v-btn>
        </template>
      </v-app-bar>
      <v-navigation-drawer :rail="rail" permanent >
        <v-list density="compact" nav>
          <v-list-item :prepend-icon="mdiServerOutline" title="Key Recovery" value="key"></v-list-item>
          <v-list-item :prepend-icon="mdiServerOutline" title="Tests" value="tests"></v-list-item>
        </v-list>
      </v-navigation-drawer>
      <v-main >
        <Recovery />
      </v-main>
    </v-app>
  </v-responsive>
</template>

<script>
import VMList from "@/components/VMList.vue"
import Recovery from "@/components/Recovery.vue"
import { mdiServerOutline, mdiTestTube, mdiWeatherSunny } from '@mdi/js'

export default {
  components: {
    VMList,
    Recovery,
  },
  data() {
    return {
      drawer: true,
      rail: true,
      theme: "dark"
    }
  },
  setup() {
    return {
      mdiServerOutline,
      mdiTestTube,
      mdiWeatherSunny,
    }
  }
}
</script>

<style>
::-webkit-scrollbar {
  display: none;
}
</style>
