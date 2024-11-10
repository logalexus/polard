<template>
  <v-responsive>
    <v-app :theme="theme">
      <v-app-bar :elevation="1">
        <template v-slot:prepend>
          <v-app-bar-nav-icon @click="rail = !rail"></v-app-bar-nav-icon>
          <v-app-bar-title>Crypto Analyzer</v-app-bar-title>
          <v-icon :icon="mdiTestTube"></v-icon>
        </template>
        <template v-slot:append>
          <v-btn :icon="mdiWeatherSunny" @click="theme = theme === 'light' ? 'dark' : 'light'"></v-btn>
        </template>
      </v-app-bar>
      <v-navigation-drawer :rail="rail" permanent>
        <v-list density="compact" nav>
          <v-list-item :prepend-icon="mdiKeyRemove" title="Factorization" value="key"
            @click="$router.push('/factorization')"></v-list-item>
          <v-list-item :prepend-icon="mdiKeyPlus" title="Generation" value="generation"
            @click="$router.push('/generation')"></v-list-item>
          <v-list-item :prepend-icon="mdiTestTube" title="Tests" value="tests"
            @click="$router.push('/tests')"></v-list-item>
        </v-list>
      </v-navigation-drawer>
      <v-main>
        <router-view />
      </v-main>
    </v-app>
  </v-responsive>
</template>

<script>
import VMList from "@/components/VMList.vue"
import FactorizationPage from "@/components/FactorizationPage.vue"
import { mdiServerOutline, mdiTestTube, mdiWeatherSunny, mdiKeyRemove, mdiKeyPlus } from '@mdi/js'

export default {
  components: {
    VMList,
    FactorizationPage,
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
      mdiKeyRemove,
      mdiKeyPlus,
    }
  }
}
</script>

<style>
::-webkit-scrollbar {
  display: none;
}
</style>
