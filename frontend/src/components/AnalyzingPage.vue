<template>
  <v-container fluid class="d-flex flex-row pa-2" style="min-height: 100vh; gap: 8px;">
    <v-card class="flex-1-1-100 pa-4" style="height: 100vh;">
      <v-card-title class="d-flex justify-center text-h5 font-weight-bold">
        <span>Factorization Methods Analyzer</span>
      </v-card-title>
      <v-container fluid class="d-flex pa-0" style="gap: 8px;">
        <v-text-field type="number" label="Timeout, sec" outlined :min="1" :max="60" v-model="timeout"></v-text-field>
        <v-select label="Method" v-model="selectedMethod" :items="factorMethods"></v-select>
      </v-container>
      <template v-if="isAnalyzing">
        <v-btn color="red" class="mt-4 mr-4" @click="cancelAnalyze">Cancel</v-btn>
        <v-progress-circular class="mt-4" indeterminate></v-progress-circular>
      </template>
      <template v-else>
        <v-btn color="primary" class="mt-4" @click="analyze"> Analyze </v-btn>
      </template>
    </v-card>
    <v-card class="flex-1-1-100 pa-4" style="height: 100vh;">
      <v-card-title class="d-flex justify-center text-h5 font-weight-bold">
        <span>Results</span>
      </v-card-title>
      <v-divider></v-divider>
      <Line ref="chart" :data="chartData" :options="chartOptions" />
      <v-data-table :items="items" :headers="headers">
        <template v-slot:item.status="{ item }">
        <div>
          <v-chip :color="item.status === 'Success' ? 'green' : 'red'" :text="item.status" class="text-uppercase"
            size="small" label></v-chip>
        </div>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);

export default {
  components: {
    Line,
  },
  data() {
    return {
      timeout: 5,
      bitLength: 64,
      factorMethods: ["Pollard", "Yafu"],
      selectedMethod: "Pollard",
      chartData: {
        labels: [],
        datasets: [
          {
            label: 'Factor time, sec',
            data: [],
            borderColor: '#42A5F5',
            fill: false,
          },
        ],
      },
      chartOptions: {
        responsive: true,
        scales: {
          x: {
            title: {
              display: true,
              text: 'Key length, bits',
            },
          },
          y: {
            title: {
              display: true,
              text: 'Factor time, sec',
            },
            min: 0,
          },
        },
      },
      items: [],
      headers: [
        { title: 'N', align: 'start', key: 'id', headerProps: {style: 'font-weight: 700'} },
        { title: 'Bits', align: 'end', key: 'bits', headerProps: {style: 'font-weight: 700'}  },
        { title: 'Time', align: 'end', key: 'time', headerProps: {style: 'font-weight: 700'}  },
        { title: 'Status', align: 'end', value: 'status', headerProps: {style: 'font-weight: 700'}  },
      ],
      websocket: null,
      isAnalyzing: false
    };
  },
  unmounted() {
    this.cancelAnalyze()
  },
  methods: {
    analyze() {
      if (this.websocket !== null) return;
      this.websocket = new WebSocket(`ws://${window.location.hostname}:8000/api/analyze?method=${this.selectedMethod}&timeout=${this.timeout}`);
      this.websocket.onopen = () => {
        console.info('[WS] Connected');
        this.$toast.info("Connected")
        this.isAnalyzing = true
        this.items = []
        let newChartData = JSON.parse(JSON.stringify(this.chartData));
        newChartData.labels = []
        newChartData.datasets[0].data = []
        this.chartData = newChartData;
      };
      this.websocket.onclose = (ev) => {
        console.info('[WS] Disconnected', ev.code, ev.reason);
        this.$toast.info("Disconnected")
        this.websocket = null;
        this.isAnalyzing = false
      };
      this.websocket.onmessage = (ev) => {
        const analyzedResult = JSON.parse(ev.data);
        this.items.push(analyzedResult)
        let newChartData = JSON.parse(JSON.stringify(this.chartData));
        newChartData.labels.push(analyzedResult.bits);
        newChartData.datasets[0].data.push(analyzedResult.time);
        this.chartData = newChartData;
      };
      this.websocket.onerror = (ev) => {
        console.warn('[WS] Error', ev);
        this.$toast.error("Error")
        this.isAnalyzing = false
      };
    },
    cancelAnalyze() {
      this.websocket?.close();
      this.websocket = null;
      this.isAnalyzing = false
      console.info('[WS] Closed');
    },
    startUpdatingGraph() {
      let count = 10;

      this.interval = setInterval(() => {
        count += 10;
        let newChartData = JSON.parse(JSON.stringify(this.chartData));
        newChartData.labels.push(count);
        newChartData.datasets[0].data.push(Math.random() * count);
        this.chartData = newChartData;
        if (count >= 120) {
          clearInterval(this.interval);
        }
      }, 1000); 
    },
  },
}
</script>

<style></style>