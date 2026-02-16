<script setup>
import { onBeforeMount, onMounted, computed, ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Cookies from 'js-cookie'
import { useUserStore } from './stores/user'

const router = useRouter()
const userStore = useUserStore()
const showDropdown = ref(false)
const dropdownRef = ref(null)

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')
  try {
    await userStore.fetchCurrentUser()
  } catch (err) {
  }
})

onMounted(() => {
  document.addEventListener('click', (e) => {
    if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
      showDropdown.value = false
    }
  })
})

const isAuthenticated = computed(() => userStore.isAuthenticated())
const currentUser = computed(() => userStore.user)

function toggleDropdown() {
  showDropdown.value = !showDropdown.value
}

async function handleLogout() {
  showDropdown.value = false
  try {
    await userStore.logout()
    router.push('/login')
  } catch (err) {
    console.error('Ошибка при выходе:', err)
  }
}
</script>

<template>
  <div class="container-fluid py-3">
    <nav class="navbar navbar-expand-lg navbar-light bg-light rounded mb-3">
      <div class="container-fluid">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Меню">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link">Главная</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/books" class="nav-link">Книги</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/authors" class="nav-link">Авторы</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/series" class="nav-link">Серии</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/genres" class="nav-link">Жанры</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/publishers" class="nav-link">Издательства</RouterLink>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li v-if="isAuthenticated" ref="dropdownRef" class="nav-item dropdown">
              <a 
                class="nav-link dropdown-toggle" 
                href="#" 
                role="button" 
                @click.prevent="toggleDropdown"
              >
                {{ currentUser?.username || 'Пользователь' }}
              </a>
              <ul v-show="showDropdown" class="dropdown-menu dropdown-menu-end show">
                <li v-if="currentUser?.is_superuser">
                  <a class="dropdown-item" href="/admin" target="_blank">Админка</a>
                </li>
                <li v-if="currentUser?.is_superuser"><hr class="dropdown-divider"></li>
                <li>
                  <a class="dropdown-item" href="#" @click.prevent="handleLogout">Выйти</a>
                </li>
              </ul>
            </li>
            <li v-else class="nav-item">
              <RouterLink to="/login" class="nav-link">Войти</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <RouterView />
  </div>
</template>
