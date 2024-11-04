import { createApp } from 'vue'
import axios from 'axios';
import VueAxios from 'vue-axios';
import ToastPlugin from 'vue-toast-notification';
// import { createRouter, createWebHistory } from 'vue-router'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import 'vuetify/styles'
import 'vue-toast-notification/dist/theme-bootstrap.css';

import App from './App.vue'

const axiosInstance = axios.create({
    baseURL: `http://${window.location.hostname}:1337/api`,
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
});

// const router = createRouter({
//     routes: [{
//         path: '/',
//         name: 'home',
//         component: App
//     },
//     ],
//     linkActiveClass: 'active',
//     history: createWebHistory()
// })

const vuetify = createVuetify({
    components,
    directives,
    icons: {
        defaultSet: 'mdi',
        aliases,
        sets: {
            mdi,
        },
    },
})

const app = createApp(App);
app.use(VueAxios, axiosInstance)
app.use(ToastPlugin);
app.use(vuetify)
// app.use(router)
app.mount('#app')
