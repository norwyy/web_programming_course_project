import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: () => import('../views/HomeView.vue') },
    { path: '/login', component: () => import('../views/LoginView.vue') },
    { path: '/authors', component: () => import('../views/AuthorsView.vue') },
    { path: '/genres', component: () => import('../views/GenresView.vue') },
    { path: '/series', component: () => import('../views/SeriesView.vue') },
    { path: '/publishers', component: () => import('../views/PublishersView.vue') },
    { path: '/books', component: () => import('../views/BooksView.vue') },
  ],
})

export default router
