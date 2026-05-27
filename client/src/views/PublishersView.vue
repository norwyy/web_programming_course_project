<script setup>
import { ref, computed, onBeforeMount } from 'vue'
import axios from 'axios'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()

const publishers = ref([])
const publisherStats = ref(null)
const publisherToAdd = ref({ name: '', description: '' })
const publisherToEdit = ref({})

const filters = ref({
  name: '',
  description: ''
})

const filteredPublishers = computed(() => {
  return publishers.value.filter(publisher => {
    if (filters.value.name && !publisher.name.toLowerCase().includes(filters.value.name.toLowerCase())) {
      return false
    }
    if (filters.value.description && !(publisher.description || '').toLowerCase().includes(filters.value.description.toLowerCase())) {
      return false
    }
    return true
  })
})

async function fetchPublishers() {
  const { data } = await axios.get('/api/publishers/')
  publishers.value = data
}

async function fetchPublishersStats() {
  const { data } = await axios.get('/api/publishers/stats/')
  publisherStats.value = data
}

async function onAdd() {
  await axios.post('/api/publishers/', { ...publisherToAdd.value })
  publisherToAdd.value = { name: '', description: '' }
  await Promise.all([fetchPublishers(), fetchPublishersStats()])
}

function onEdit(item) {
  publisherToEdit.value = { ...item }
}

async function onUpdate() {
  await axios.put(`/api/publishers/${publisherToEdit.value.id}/`, { ...publisherToEdit.value })
  await Promise.all([fetchPublishers(), fetchPublishersStats()])
}

async function onRemove(item) {
  await axios.delete(`/api/publishers/${item.id}/`)
  await Promise.all([fetchPublishers(), fetchPublishersStats()])
}

function canEdit(item) {
  if (!userStore.user) return false
  if (userStore.isAdmin()) return true
  return item.user === userStore.user.id
}

onBeforeMount(async () => {
  await Promise.all([fetchPublishers(), fetchPublishersStats()])
})
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2 class="mb-0">Издательства</h2>
      <div v-if="publisherStats" class="text-muted">
        Всего: <strong>{{ publisherStats.count }}</strong>
      </div>
    </div>
    <form v-if="userStore.isAuthenticated()" @submit.prevent="onAdd" class="row g-2 mb-4">
      <div class="col">
        <input v-model="publisherToAdd.name" class="form-control" placeholder="Название" required />
      </div>
      <div class="col">
        <input v-model="publisherToAdd.description" class="form-control" placeholder="Описание" />
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
      <li v-for="item in filteredPublishers" :key="item.id" class="list-group-item d-flex justify-content-between align-items-center">
        <span>{{ item.name }} - {{ item.description || '-' }}</span>
        <span v-if="canEdit(item)">
          <button class="btn btn-sm btn-success me-1" data-bs-toggle="modal" data-bs-target="#editPublisherModal" @click="onEdit(item)">✎</button>
          <button class="btn btn-sm btn-danger" @click="onRemove(item)">✕</button>
        </span>
      </li>
    </ul>

    <div class="modal fade" id="editPublisherModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать издательство</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-2">
              <label class="form-label">Название</label>
              <input v-model="publisherToEdit.name" class="form-control" />
            </div>
            <div>
              <label class="form-label">Описание</label>
              <input v-model="publisherToEdit.description" class="form-control" />
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
