<template>
  <v-container fluid class="d-flex flex-row pa-2" style="min-height: 100vh; gap: 8px;">
    <v-card class="flex-1-1-100 pa-4" style="height: 100vh;">
      <v-card-title class="d-flex justify-center">RSA Public key generator</v-card-title>
      <div class="d-flex flex-column align-center" style="width: 100%;">
        <v-textarea class="mt-4" label="Public Key" variant="solo-filled" rows="20" readonly="true" v-model="publicKey"
          style="min-width: 50%;"></v-textarea>
        <v-text-field type="number" label="Bit Length" outlined class="mt-4" :min="10" :max="128" v-model="bitLength"
          style="width: 200px;"></v-text-field>
        <template v-if="loading">
          <v-progress-circular class="mt-4" indeterminate></v-progress-circular>
        </template>
        <template v-else>
          <v-btn color="primary" class="mt-4" @click="generate_key">Generate</v-btn>
        </template>
      </div>
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
      bitLength: 64,
      publicKey: "",
      loading: false,
    };
  },
  methods: {
    generate_key() {
      this.loading = true;
      this.$http.get(`public_generate?bits=${this.bitLength}`)
        .then(response => {
          this.$toast.success("Public key generated")
          this.publicKey = response.data
          this.loading = false;
        })
        .catch(e => {
          this.$toast.error(e.response.data.detail || "An error occurred")
          this.loading = false;
        });
    },
  },
}
</script>

<style></style>