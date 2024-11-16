import { createRouter, createWebHistory } from 'vue-router'
import FactorizationPage from "@/components/FactorizationPage.vue"
import GenerationPage from '@/components/GenerationPage.vue'
import AnalyzingPage from '@/components/AnalyzingPage.vue'
import CheckKeyPage from '@/components/CheckKeyPage.vue'

const routes = [
  { path: '/', redirect: '/check' },
  { path: '/check', component: CheckKeyPage },
  { path: '/factorization', component: FactorizationPage },
  { path: '/generation', component: GenerationPage },
  { path: '/analyze', component: AnalyzingPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
