import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-icons/font/bootstrap-icons.min.css'
import 'bootstrap/dist/js/bootstrap.bundle'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'
import Cookies from 'js-cookie'

import App from './App.vue'
import router from './router'


axios.interceptors.request.use((config) => {
  const token = Cookies.get('csrftoken')
  if (token) config.headers['X-CSRFToken'] = token
  return config
})

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
