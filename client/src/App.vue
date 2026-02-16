<script setup>
import { onBeforeMount } from 'vue'
import axios from 'axios'
import Cookies from 'js-cookie'

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')
})
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
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Пользователь</a>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="/admin">Админка</a></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <RouterView />
  </div>
</template>
