<template>
  <v-container fluid class="d-flex flex-row pa-2" style="min-height: 100vh; gap: 8px;">
    <v-card class="flex-1-1-100 pa-4" style="height: 100vh;">
      <v-card-title class="d-flex justify-center">Pollard Test</v-card-title>
      <v-text-field type="number" label="Timeout, sec" outlined class="mt-4" :min="1" :max="60" v-model="timeout"
        style="width: 200px;"></v-text-field>
      <v-text-field type="number" label="Bit Length" outlined class="mt-4" :min="10" :max="128" v-model="bitLength"
        style="width: 200px;"></v-text-field>
      <v-btn color="primary" class="mt-4" @click="factorizeKey"> Factorize </v-btn>
    </v-card>
    <v-card class="flex-1-1-100 pa-4" style="height: 100vh;">
      <v-card-title class="d-flex justify-center">Results</v-card-title>
      <Line ref="chart" :data="chartData" :options="chartOptions" />
      <v-data-table :items="items"></v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import VMAction from "@/components/VMAction.vue"
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);

export default {
  components: {
    VMAction,
    Line,
  },
  data() {
    return {
      timeout: 30,
      bitLength: 64,
      chartData: {
        labels: [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        datasets: [
          {
            label: 'Factor time, sec',
            data: [0.1, 0.3, 0.5, 1, 2, 3, 5, 8, 13, 21],
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
      items: [
        {
          N: '1',
          Bits: '10',
          Time: '20',
          Status: 'Factorized',
        },
        {
          N: '2',
          Bits: '11',
          Time: '22',
          Status: 'Factorized',
        },
      ],
    };
  },
  methods: {
    factorizeKey() {
      console.log("Timeout:", this.timeout);
      console.log("Bit Length:", this.bitLength);
      this.startUpdatingGraph();
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
      }, 1000); // Интервал в 1 секунду
    },
  },
}
</script>

<style></style>