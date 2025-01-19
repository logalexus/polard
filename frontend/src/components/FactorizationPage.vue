<template>
  <v-container fluid class="d-flex flex-row pa-2" style="min-height: 100vh; gap: 8px;">
    <v-card class="flex-1-1-100 pa-4" style="height: 100vh;">
      <v-card-title class="d-flex justify-center text-h5 font-weight-bold">
        <span>Факторизация публичного ключа RSA</span>
      </v-card-title>
      <v-textarea label="Публичный ключ" variant="solo-filled" rows="20" v-model="publicKey" @dragover.prevent
        @dragenter.prevent @drop="handleDrop"></v-textarea>
      <v-container fluid class="d-flex pa-0" style="gap: 8px;">
        <v-text-field type="number" label="Таймаут, сек" outlined :min="1" :max="60" v-model="timeout"></v-text-field>
        <v-select label="Метод" v-model="selectedMethod" :items="factorMethods"></v-select>
      </v-container>
      <template v-if="loading">
        <v-btn color="red" class="mt-4 mr-4" @click="generate_key">Отменить</v-btn>
        <v-progress-circular class="mt-4" indeterminate></v-progress-circular>
      </template>
      <template v-else>
        <v-btn color="primary" class="mt-4" @click="factorizeKey"> Факторизовать </v-btn>
      </template>
    </v-card>
    <v-card class="flex-1-1-100 pa-4" style="height: 100vh;">
      <v-card-title class="d-flex justify-center text-h5 font-weight-bold">
        <span>Результаты</span>
      </v-card-title>
      <v-textarea label="Приватный ключ" readonly="true" variant="solo-filled" rows="20" v-model="privateKey"></v-textarea>
      <!-- <v-progress-linear class="rounded-sm" v-model="progress" color="green" height="25">
        <template v-slot:default="{ value }">
          <strong>{{ Math.ceil(value) }}%</strong>
        </template>
      </v-progress-linear> -->
      <v-chip class="mr-2 mt-4">Время факторизации: {{ factorTime }}с</v-chip>
      <v-chip class="mr-2 mt-4" :color="status === 'Success' ? 'green' : 'red'">Статус: {{ status === 'Success' ? 'Успех' : 'Провал' }}</v-chip>
    </v-card>
  </v-container>
</template>

<script>

export default {
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
      const file = event.dataTransfer.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.publicKey = e.target.result; 
        };

        reader.readAsText(file); 
      } else {
        alert("Please drop a valid text file.");
      }
    },
  },
}
</script>

<style></style>