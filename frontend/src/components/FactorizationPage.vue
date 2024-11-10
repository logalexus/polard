<template>
  <v-container fluid class="d-flex flex-row pa-2" style="min-height: 100vh; gap: 8px;">
    <v-card class="flex-1-1-100 pa-4" style="height: 100vh;">
      <v-card-title class="d-flex justify-center">RSA Public key factorization</v-card-title>
      <v-textarea label="Public Key" variant="solo-filled" rows="20" v-model="publicKey" @dragover.prevent
        @dragenter.prevent @drop="handleDrop"></v-textarea>
      <v-container fluid class="d-flex pa-0" style="gap: 8px;">
        <v-text-field type="number" label="Timeout, sec" outlined :min="1" :max="60" v-model="timeout"></v-text-field>
        <v-select label="Method" v-model="selectedMethod" :items="factorMethods"></v-select>
      </v-container>
      <template v-if="loading">
        <v-btn color="red" class="mt-4 mr-4" @click="generate_key">Cancel</v-btn>
        <v-progress-circular class="mt-4" indeterminate></v-progress-circular>
      </template>
      <template v-else>
        <v-btn color="primary" class="mt-4" @click="factorizeKey"> Factorize </v-btn>
      </template>
    </v-card>
    <v-card class="flex-1-1-100 pa-4" style="height: 100vh;">
      <v-card-title class="d-flex justify-center">Results</v-card-title>
      <v-textarea label="Private Key" readonly="true" variant="solo-filled" rows="20" v-model="privateKey"></v-textarea>
      <v-progress-linear class="rounded-sm" v-model="progress" color="green" height="25">
        <template v-slot:default="{ value }">
          <strong>{{ Math.ceil(value) }}%</strong>
        </template>
      </v-progress-linear>
      <v-chip class="mr-2 mt-4">Factor time: {{ factorTime }}s</v-chip>
      <v-chip class="mr-2 mt-4">Status: {{ status }}</v-chip>
    </v-card>
  </v-container>
</template>

<script>
import VMAction from "@/components/VMAction.vue"

export default {
  components: {
    VMAction,
  },
  data() {
    return {
      timeout: 30,
      bitLength: 64,
      progress: 0,
      factorTime: 0,
      status: "-",
      factorMethods: ["Pollard", "Yafu"],
      selectedMethod: "Pollard",
      publicKey: "",
      privateKey: "",
      loading: false,
    };
  },
  methods: {
    factorizeKey() {
      const params = {
        public_key: this.publicKey,
        method: this.selectedMethod,
        timeout: this.timeout,
      };

      this.loading = true
      this.$http.post(`factorize`, params)
        .then(response => {
          const parsed = response.data;
          console.log(response.data)
          this.privateKey = parsed.private_key
          this.factorTime = parsed.factor_time
          this.status = parsed.status
          this.loading = false
        })
        .catch(e => {
          this.$toast.error("An error occurred")
          this.loading = false
        });
    },
    handleDrop(event) {
      event.preventDefault();
      // Получаем файл из события drag-and-drop
      const file = event.dataTransfer.files[0];

      // Проверяем, что файл существует и является текстовым
      if (file) {
        const reader = new FileReader();

        // Читаем содержимое файла как текст
        reader.onload = (e) => {
          this.publicKey = e.target.result; // Устанавливаем содержимое файла в publicKey
        };

        reader.readAsText(file); // Запускаем чтение файла
      } else {
        alert("Please drop a valid text file.");
      }
    },
  },
}
</script>

<style></style>