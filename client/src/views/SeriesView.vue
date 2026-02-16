<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const series = ref([])
const seriesToAdd = ref({ name: '', description: '' })
const seriesToEdit = ref({})

async function fetchSeries() {
  const { data } = await axios.get('/api/series/')
  series.value = data
}

async function onAdd() {
  await axios.post('/api/series/', { ...seriesToAdd.value })
  seriesToAdd.value = { name: '', description: '' }
  await fetchSeries()
}

function onEditClick(item) {
  seriesToEdit.value = { ...item }
}

async function onUpdate() {
  await axios.put(`/api/series/${seriesToEdit.value.id}/`, { ...seriesToEdit.value })
  await fetchSeries()
}

async function onRemove(item) {
  await axios.delete(`/api/series/${item.id}/`)
  await fetchSeries()
}

onBeforeMount(fetchSeries)
</script>

<template>
  <div>
    <h2 class="mb-3">Серии</h2>
    <form @submit.prevent="onAdd" class="row g-2 mb-4">
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
    <ul class="list-group">
      <li v-for="item in series" :key="item.id" class="list-group-item d-flex justify-content-between align-items-center">
        <span>{{ item.name }} — {{ item.description || '—' }}</span>
        <span>
          <button class="btn btn-sm btn-success me-1" data-bs-toggle="modal" data-bs-target="#editSeriesModal" @click="onEditClick(item)">✎</button>
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
