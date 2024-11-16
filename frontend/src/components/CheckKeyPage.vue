<template>
  <v-container fluid class="d-flex flex-row pa-2" style="min-height: 100vh; gap: 8px;">
    <v-card class="flex-1-1-100 pa-4" style="height: 100vh;">
      <v-card-title class="d-flex justify-center text-h5 font-weight-bold">
        <span>RSA Public Key Check</span>
      </v-card-title>
      <v-textarea label="Public Key" variant="solo-filled" rows="20" v-model="publicKey" @dragover.prevent
        @dragenter.prevent @drop="handleDrop"></v-textarea>
      <v-container fluid class="d-flex pa-0" style="gap: 8px;">
        <v-text-field type="number" label="Timeout, sec" outlined :min="1" :max="60" v-model="timeout"></v-text-field>
      </v-container>
      <template v-if="loading">
        <v-btn color="red" class="mt-4 mr-4" @click="generate_key">Cancel</v-btn>
        <v-progress-circular class="mt-4" indeterminate></v-progress-circular>
      </template>
      <template v-else>
        <v-btn color="primary" class="mt-4" @click="checkKey">Check</v-btn>
      </template>
    </v-card>
    <v-card class="flex-1-1-100 pa-4" style="height: 100vh;">
      <v-card-title class="d-flex justify-center text-h5 font-weight-bold">
        <span>Results</span>
      </v-card-title>
      <v-divider></v-divider>
      <v-data-table :headers="headers" :items="tests" item-value="description" item-key="description"
        :loading="loading" hide-default-footer>
        <template v-slot:item.status="{ item }">
          <v-icon :color="item.status ? 'green' : 'red'" left>
            {{ item.status ? mdiCheckCircleOutline : mdiCloseCircleOutline }}
          </v-icon>
          {{ item.status ? 'Success' : 'Failed' }}
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import { mdiCheckCircleOutline, mdiCloseCircleOutline } from '@mdi/js'

export default {
  data() {
    return {
      timeout: 30,
      publicKey: "",
      privateKey: "",
      loading: false,
      headers: [
        { title: 'Status', align: 'start', value: 'status', headerProps: {style: 'font-weight: 700'} },
        { title: 'Test', align: 'end', value: 'description', headerProps: {style: 'font-weight: 700'}  },
      ],
      tests: [],
    };
  },
  setup() {
    return {
      mdiCheckCircleOutline,
      mdiCloseCircleOutline
    }
  },
  methods: {
    checkKey() {
      const params = {
        public_key: this.publicKey,
        timeout: this.timeout,
      };

      this.loading = true
      this.$http.post(`check`, params)
        .then(response => {
          const parsed = response.data;
          console.log(response.data)
          this.tests = response.data
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