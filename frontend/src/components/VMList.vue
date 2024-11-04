<template>
  <v-card flat>
    <v-card-title class="d-flex align-center pe-2">
      Labs
      <v-spacer></v-spacer>
      <v-text-field v-model="search" density="compact" label="Search" variant="solo-filled" flat hide-details
        single-line></v-text-field>
    </v-card-title>
    <v-divider></v-divider>
    <v-data-table v-model:search="search" :items="items" show-expand item-value="name" :headers="headers"
      :loading="loading">
      <template v-slot:item.status="{ item }">
        <div>
          <v-chip :color="item.status === 'Running' ? 'green' : 'red'" :text="item.status" class="text-uppercase"
            size="small" label></v-chip>
        </div>
      </template>
      <template v-slot:expanded-row="{ columns, item }">
        <tr>
          <td :colspan="columns.length">
            <p class="pt-2 pb-2 mb-3" v-html="stringdata(item.logs)"></p>
          </td>
        </tr>
      </template>
      <template v-slot:item.action="{ item }">
        <VMAction :status="item.status" :lab="item" @update="get_labs" />
      </template>
    </v-data-table>
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

<style></style>-