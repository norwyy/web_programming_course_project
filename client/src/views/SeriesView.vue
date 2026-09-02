<script setup>
import { ref, computed, onBeforeMount } from 'vue'
import axios from 'axios'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()

const series = ref([])
const seriesStats = ref(null)
const seriesToAdd = ref({ name: '', description: '' })
const seriesToEdit = ref({})

const filters = ref({
  name: '',
  description: ''
})

const filteredSeries = computed(() => {
  return series.value.filter(s => {
    if (filters.value.name && !s.name.toLowerCase().includes(filters.value.name.toLowerCase())) {
      return false
    }
    if (filters.value.description && !(s.description || '').toLowerCase().includes(filters.value.description.toLowerCase())) {
      return false
    }
    return true
  })
})

async function fetchSeries() {
  const { data } = await axios.get('/api/series/')
  series.value = data
}

async function fetchSeriesStats() {
  const { data } = await axios.get('/api/series/stats/')
  seriesStats.value = data
}

async function onAdd() {
  await axios.post('/api/series/', { ...seriesToAdd.value })
  seriesToAdd.value = { name: '', description: '' }
  await Promise.all([fetchSeries(), fetchSeriesStats()])
}

function onEdit(item) {
  seriesToEdit.value = { ...item }
}

async function onUpdate() {
  await axios.put(`/api/series/${seriesToEdit.value.id}/`, { ...seriesToEdit.value })
  await Promise.all([fetchSeries(), fetchSeriesStats()])
}

async function onRemove(item) {
  await axios.delete(`/api/series/${item.id}/`)
  await Promise.all([fetchSeries(), fetchSeriesStats()])
}

function canEdit(item) {
  if (!userStore.user) return false
  if (userStore.isAdmin()) return true
  return item.user === userStore.user.id
}

onBeforeMount(async () => {
  await Promise.all([fetchSeries(), fetchSeriesStats()])
})
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2 class="mb-0">Серии</h2>
      <div v-if="seriesStats" class="text-muted">
        Всего: <strong>{{ seriesStats.count }}</strong>
      </div>
    </div>
    <form v-if="userStore.isAuthenticated()" @submit.prevent="onAdd" class="row g-2 mb-4">
      <div class="col">
        <input v-model="seriesToAdd.name" class="form-control" placeholder="Название" required />
      </div>
      <div class="col">
        <input v-model="seriesToAdd.description" class="form-control" placeholder="Описание" />
      </div>
      <div class="col-auto">
        <button type="submit" class="btn btn-primary">Добавить</button>
      </div>
    </form>
    <div class="mb-2">
      <strong>Фильтры</strong>
    </div>
    <div class="row g-2 mb-3">
      <div class="col-6">
        <label class="form-label mb-1" style="font-weight: normal;">Название</label>
        <input
          v-model="filters.name"
          type="text"
          class="form-control"
        />
      </div>
      <div class="col-6">
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
      <li v-for="item in filteredSeries" :key="item.id" class="list-group-item d-flex justify-content-between align-items-center">
        <span>{{ item.name }} - {{ item.description || '-' }}</span>
        <span v-if="canEdit(item)">
          <button class="btn btn-sm btn-success me-1" data-bs-toggle="modal" data-bs-target="#editSeriesModal" @click="onEdit(item)">✎</button>
          <button class="btn btn-sm btn-danger" @click="onRemove(item)">✕</button>
        </span>
      </li>
    </ul>

    <div class="modal fade" id="editSeriesModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать серию</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-2">
              <label class="form-label">Название</label>
              <input v-model="seriesToEdit.name" class="form-control" />
            </div>
            <div>
              <label class="form-label">Описание</label>
              <input v-model="seriesToEdit.description" class="form-control" />
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
