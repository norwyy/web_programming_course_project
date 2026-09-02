<script setup>
import { ref, computed, onBeforeMount } from 'vue'
import axios from 'axios'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()

const genres = ref([])
const genreStats = ref(null)
const genreToAdd = ref({ name: '', description: '' })
const genreToEdit = ref({})

const filters = ref({
  name: '',
  description: ''
})

const filteredGenres = computed(() => {
  return genres.value.filter(genre => {
    if (filters.value.name && !genre.name.toLowerCase().includes(filters.value.name.toLowerCase())) {
      return false
    }
    if (filters.value.description && !(genre.description || '').toLowerCase().includes(filters.value.description.toLowerCase())) {
      return false
    }
    return true
  })
})

async function fetchGenres() {
  const { data } = await axios.get('/api/genres/')
  genres.value = data
}

async function fetchGenresStats() {
  const { data } = await axios.get('/api/genres/stats/')
  genreStats.value = data
}

async function onAdd() {
  await axios.post('/api/genres/', { ...genreToAdd.value })
  genreToAdd.value = { name: '', description: '' }
  await Promise.all([fetchGenres(), fetchGenresStats()])
}

function onEdit(item) {
  genreToEdit.value = { ...item }
}

async function onUpdate() {
  await axios.put(`/api/genres/${genreToEdit.value.id}/`, { ...genreToEdit.value })
  await Promise.all([fetchGenres(), fetchGenresStats()])
}

async function onRemove(item) {
  await axios.delete(`/api/genres/${item.id}/`)
  await Promise.all([fetchGenres(), fetchGenresStats()])
}

function canEdit(item) {
  if (!userStore.user) return false
  if (userStore.isAdmin()) return true
  return item.user === userStore.user.id
}

onBeforeMount(async () => {
  await Promise.all([fetchGenres(), fetchGenresStats()])
})
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2 class="mb-0">Жанры</h2>
      <div v-if="genreStats" class="text-muted">
        Всего: <strong>{{ genreStats.count }}</strong>
        <span v-if="genreStats.top_genre_name" class="ms-3">
          Самый популярный жанр: <strong>{{ genreStats.top_genre_name }}</strong> 45 книг
        </span>
      </div>
    </div>
    <form v-if="userStore.isAuthenticated()" @submit.prevent="onAdd" class="row g-2 mb-4">
      <div class="col">
        <input v-model="genreToAdd.name" class="form-control" placeholder="Название" required />
      </div>
      <div class="col">
        <input v-model="genreToAdd.description" class="form-control" placeholder="Описание" />
      </div>
      <div class="col-auto">
        <button type="submit" class="btn btn-primary">Добавить</button>
      </div>
    </form>
    <div class="mb-2">
      <strong>Фильтры</strong>
    </div>
    <div class="row g-2 mb-3">
      <div class="col-md-6">
        <label class="form-label mb-1" style="font-weight: normal;">Название</label>
        <input
          v-model="filters.name"
          type="text"
          class="form-control"
        />
      </div>
      <div class="col-md-6">
        <label class="form-label mb-1" style="font-weight: normal;">Описание</label>
        <input
          v-model="filters.description"
          type="text"
          class="form-control"
        />
      </div>
      <div class="col-auto">
        <button
          class="btn btn-outline-secondary"
          @click="filters = { name: '', description: '' }"
        >
          Очистить фильтры
        </button>
      </div>
    </div>
    <ul class="list-group">
      <li v-for="item in filteredGenres" :key="item.id" class="list-group-item d-flex justify-content-between align-items-center">
        <span>{{ item.name }} - {{ item.description || '-' }}</span>
        <span v-if="canEdit(item)">
          <button class="btn btn-sm btn-success me-1" data-bs-toggle="modal" data-bs-target="#editGenreModal" @click="onEdit(item)">✎</button>
          <button class="btn btn-sm btn-danger" @click="onRemove(item)">✕</button>
        </span>
      </li>
    </ul>

    <div class="modal fade" id="editGenreModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать жанр</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-2">
              <label class="form-label">Название</label>
              <input v-model="genreToEdit.name" class="form-control" />
            </div>
            <div>
              <label class="form-label">Описание</label>
              <input v-model="genreToEdit.description" class="form-control" />
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdate">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
