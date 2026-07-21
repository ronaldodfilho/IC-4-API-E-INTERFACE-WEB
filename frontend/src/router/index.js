import { createRouter, createWebHistory } from 'vue-router';
import OperadorasView from '../views/OperadorasView.vue';
import DetalhesOperadoraView from '../views/DetalhesOperadoraView.vue';

const routes = [
  {
    path: '/',
    name: 'Operadoras',
    component: OperadorasView
  },

  {
    path: '/operadoras/:cnpj',
    name: 'detalhes-operadora',
    component: DetalhesOperadoraView
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})  

export default router;