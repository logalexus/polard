<template>
  <v-responsive>
    <v-app :theme="theme">
      <v-app-bar :elevation="1">
        <template v-slot:prepend>
          <v-app-bar-nav-icon @click="rail = !rail"></v-app-bar-nav-icon>
          <v-app-bar-title>Лаборатория RSA</v-app-bar-title>
          <v-icon :icon="mdiTestTube"></v-icon>
        </template>
        <template v-slot:append>
          <v-btn :icon="mdiWeatherSunny" @click="theme = theme === 'light' ? 'dark' : 'light'"></v-btn>
        </template>
      </v-app-bar>
      <v-navigation-drawer :rail="rail" permanent>
        <v-list density="compact" nav>
          <v-list-item :prepend-icon="mdiCheckCircleOutline" title="Тестирование" value="check"
            @click="$router.push('/check')"></v-list-item>
          <v-list-item :prepend-icon="mdiKeyRemove" title="Факторизация" value="keyFactor"
            @click="$router.push('/factorization')"></v-list-item>
          <v-list-item :prepend-icon="mdiKeyPlus" title="Генерация" value="generation"
            @click="$router.push('/generation')"></v-list-item>
          <v-list-item :prepend-icon="mdiTestTube" title="Анализ" value="tests"
            @click="$router.push('/analyze')"></v-list-item>
        </v-list>
      </v-navigation-drawer>
      <v-main>
        <router-view />
      </v-main>
    </v-app>
  </v-responsive>
</template>

<script>
import { mdiServerOutline, mdiTestTube, mdiWeatherSunny, mdiKeyRemove, mdiKeyPlus, mdiCheckCircleOutline  } from '@mdi/js'

export default {
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
      mdiCheckCircleOutline,
    }
  }
}
</script>

<style>
::-webkit-scrollbar {
  display: none;
}
</style>
