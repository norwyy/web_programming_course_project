import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: () => import('../views/HomeView.vue') },
    { path: '/authors', name: 'authors', component: () => import('../views/AuthorsView.vue') },
    { path: '/genres', name: 'genres', component: () => import('../views/GenresView.vue') },
    { path: '/series', name: 'series', component: () => import('../views/SeriesView.vue') },
    { path: '/publishers', name: 'publishers', component: () => import('../views/PublishersView.vue') },
    { path: '/books', name: 'books', component: () => import('../views/BooksView.vue') },
  ],
})

export default router
