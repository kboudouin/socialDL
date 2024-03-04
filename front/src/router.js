import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from './components/Dashboard.vue';
import NotFound from './components/NotFound.vue';

const routes = [
  { path: '/', component: Dashboard },
  { path: '/:catchAll(.*)', component: NotFound }
];

const router = createRouter({
  history: createWebHistory(),
  
  routes,
});

export default router;
