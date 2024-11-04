<template>
  <v-card flat>
    <v-card-title class="d-flex align-center pe-2">
      Labs
      <v-spacer></v-spacer>
    </v-card-title>
    <v-divider></v-divider>
    <v-card-title class="d-flex align-start">
      <v-spacer></v-spacer>
      <v-textarea label="Public Key" variant="solo-filled" rows="20"></v-textarea>
      <v-spacer></v-spacer>
    </v-card-title>
    <v-card-title class="d-flex align-center justify-center ">
      <v-btn> Factorize </v-btn>
    </v-card-title>
  </v-card>
</template>

<script>
import VMAction from "@/components/VMAction.vue"

export default {
  components: {
    VMAction
  },
  data() {
    return {
      search: '',
      headers: [
        { title: 'Name', value: 'name' },
        { title: 'OS', align: 'center', value: 'os' },
        { title: 'IP', align: 'center', value: 'ip' },
        { title: 'Status', align: 'center', value: 'status' },
        { title: "Actions", value: "action", align: 'center', sortable: false, width: "300px" }
      ],
      items: [],
      loading: true,
      itemsPerPage: 5,
      totalItems: 0,
    }
  },
  setup() {
    return {
    }
  },
  mounted() {
    this.get_labs();
  },
  methods: {
    get_labs() {
      this.loading = true
      this.$http.get('labs').then(response => {
        console.log(response.data);
        this.items = response.data
        this.loading = false
      });
    },
    escapeHtml(in_) {
      return in_.replace(/(<span style="background-color: #(?:[A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})">|<\/span>)|[&<>"'/]/g, ($0, $1) => {
        const entityMap = {
          '&': '&amp;',
          '<': '&lt;',
          '>': '&gt;',
          '"': '&quot;',
          '\'': '&#39;',
          '/': '&#x2F;',
        };

        return $1 ? $1 : entityMap[$0];
      });
    },
    stringdata(data) {
      if (data == NaN) {
        return "Nothing"
      }
      return this.escapeHtml(data)
        .split('\n')
        .join('<br>');
    },
  },
}
</script>

<style>
.key-block {
  display: flex;
  align-items: center;
  height: 100%;
}

.key-field {
  display: flex;
  width: 500px;
}
</style>