<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const authors = ref([])
const authorToAdd = ref({ full_name: '', biography: '' })
const authorToEdit = ref({})

async function fetchAuthors() {
  const { data } = await axios.get('/api/authors/')
  authors.value = data
}

async function onAdd() {
  await axios.post('/api/authors/', { ...authorToAdd.value })
  authorToAdd.value = { full_name: '', biography: '' }
  await fetchAuthors()
}

function onEditClick(item) {
  authorToEdit.value = { ...item }
}

async function onUpdate() {
  await axios.put(`/api/authors/${authorToEdit.value.id}/`, { ...authorToEdit.value })
  await fetchAuthors()
}

async function onRemove(item) {
  await axios.delete(`/api/authors/${item.id}/`)
  await fetchAuthors()
}

onBeforeMount(fetchAuthors)
</script>

<template>
  <div>
    <h2 class="mb-3">Авторы</h2>
    <form @submit.prevent="onAdd" class="row g-2 mb-4">
      <div class="col">
        <input v-model="authorToAdd.full_name" class="form-control" placeholder="ФИО" required />
      </div>
      <div class="col">
        <input v-model="authorToAdd.biography" class="form-control" placeholder="Биография" />
      </div>
      <div class="col-auto">
        <button type="submit" class="btn btn-primary">Добавить</button>
      </div>
    </form>
    <ul class="list-group">
      <li v-for="item in authors" :key="item.id" class="list-group-item d-flex justify-content-between align-items-center">
        <span>{{ item.full_name }} — {{ item.biography || '—' }}</span>
        <span>
          <button class="btn btn-sm btn-success me-1" data-bs-toggle="modal" data-bs-target="#editAuthorModal" @click="onEditClick(item)">✎</button>
          <button class="btn btn-sm btn-danger" @click="onRemove(item)">✕</button>
        </span>
      </li>
    </ul>

    <div class="modal fade" id="editAuthorModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать автора</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-2">
              <label class="form-label">ФИО</label>
              <input v-model="authorToEdit.full_name" class="form-control" />
            </div>
            <div>
              <label class="form-label">Биография</label>
              <input v-model="authorToEdit.biography" class="form-control" />
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
