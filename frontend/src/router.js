import { createRouter, createWebHistory } from 'vue-router'
import FactorizationPage from "@/components/FactorizationPage.vue"
import GenerationPage from '@/components/GenerationPage.vue'
import TestingPage from '@/components/TestingPage.vue'

const routes = [
  { path: '/', redirect: '/factorization' },
  { path: '/factorization', component: FactorizationPage },
  { path: '/generation', component: GenerationPage },
  { path: '/tests', component: TestingPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
