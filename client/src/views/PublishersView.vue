<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const publishers = ref([])
const publisherToAdd = ref({ name: '', description: '' })
const publisherToEdit = ref({})

async function fetchPublishers() {
  const { data } = await axios.get('/api/publishers/')
  publishers.value = data
}

async function onAdd() {
  await axios.post('/api/publishers/', { ...publisherToAdd.value })
  publisherToAdd.value = { name: '', description: '' }
  await fetchPublishers()
}

function onEditClick(item) {
  publisherToEdit.value = { ...item }
}

async function onUpdate() {
  await axios.put(`/api/publishers/${publisherToEdit.value.id}/`, { ...publisherToEdit.value })
  await fetchPublishers()
}

async function onRemove(item) {
  await axios.delete(`/api/publishers/${item.id}/`)
  await fetchPublishers()
}

onBeforeMount(fetchPublishers)
</script>

<template>
  <div>
    <h2 class="mb-3">Издательства</h2>
    <form @submit.prevent="onAdd" class="row g-2 mb-4">
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
    <ul class="list-group">
      <li v-for="item in publishers" :key="item.id" class="list-group-item d-flex justify-content-between align-items-center">
        <span>{{ item.name }} — {{ item.description || '—' }}</span>
        <span>
          <button class="btn btn-sm btn-success me-1" data-bs-toggle="modal" data-bs-target="#editPublisherModal" @click="onEditClick(item)">✎</button>
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
