<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const authors = ref([])
const authorToAdd = ref({ full_name: '', biography: '' })
const authorToEdit = ref({})
const authorsPictureRef = ref()
const authorAddImageUrl = ref()
const authorEditPictureRef = ref()
const authorEditImageUrl = ref()
const imagePreviewUrl = ref()
const imagePreviewModal = ref()

function pictureUrl(p) {
  if (!p) return ''
  return p.startsWith('http') || p.startsWith('/') ? p : '/media/' + p
}

async function fetchAuthors() {
  const { data } = await axios.get('/api/authors/')
  authors.value = data
}

function authorAddPictureChange() {
  const file = authorsPictureRef.value?.files?.[0]
  if (file) {
    if (authorAddImageUrl.value) URL.revokeObjectURL(authorAddImageUrl.value)
    authorAddImageUrl.value = URL.createObjectURL(file)
  }
}

function authorEditPictureChange() {
  const file = authorEditPictureRef.value?.files?.[0]
  if (file) {
    if (authorEditImageUrl.value) URL.revokeObjectURL(authorEditImageUrl.value)
    authorEditImageUrl.value = URL.createObjectURL(file)
  }
}

async function onAdd() {
  const formData = new FormData()
  formData.set('full_name', authorToAdd.value.full_name)
  formData.set('biography', authorToAdd.value.biography || '')
  const file = authorsPictureRef.value?.files?.[0]
  if (file) formData.append('picture', file)

  await axios.post('/api/authors/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  authorToAdd.value = { full_name: '', biography: '' }
  if (authorsPictureRef.value) authorsPictureRef.value.value = ''
  if (authorAddImageUrl.value) {
    URL.revokeObjectURL(authorAddImageUrl.value)
    authorAddImageUrl.value = null
  }
  await fetchAuthors()
}

function onEditClick(item) {
  authorToEdit.value = { ...item }
  authorEditImageUrl.value = item.picture ? pictureUrl(item.picture) : null
  if (authorEditPictureRef.value) authorEditPictureRef.value.value = ''
}

async function onUpdate() {
  const formData = new FormData()
  formData.set('full_name', authorToEdit.value.full_name)
  formData.set('biography', authorToEdit.value.biography || '')
  const file = authorEditPictureRef.value?.files?.[0]
  if (file) formData.append('picture', file)

  await axios.patch(`/api/authors/${authorToEdit.value.id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  await fetchAuthors()
}

async function onRemove(item) {
  await axios.delete(`/api/authors/${item.id}/`)
  await fetchAuthors()
}

function openImagePreview(url) {
  imagePreviewUrl.value = url
  const modal = new window.bootstrap.Modal(imagePreviewModal.value)
  modal.show()
}

onBeforeMount(fetchAuthors)
</script>

<template>
  <div>
    <h2 class="mb-3">Авторы</h2>
    <form @submit.prevent="onAdd" class="row g-2 mb-4 flex-wrap align-items-end">
      <div class="col">
        <label class="form-label">ФИО</label>
        <input v-model="authorToAdd.full_name" class="form-control" placeholder="ФИО" required />
      </div>
      <div class="col">
        <label class="form-label">Биография</label>
        <input v-model="authorToAdd.biography" class="form-control" placeholder="Биография" />
      </div>
      <div class="col-auto">
        <label class="form-label">Изображение</label>
        <input
          ref="authorsPictureRef"
          type="file"
          class="form-control"
          accept="image/*"
          @change="authorAddPictureChange"
        />
      </div>
      <div class="col-auto" v-show="authorAddImageUrl">
        <img :src="authorAddImageUrl" alt="" style="max-height: 60px;" />
      </div>
      <div class="col-auto">
        <button type="submit" class="btn btn-primary">Добавить</button>
      </div>
    </form>
    <ul class="list-group">
      <li v-for="item in authors" :key="item.id" class="list-group-item d-flex justify-content-between align-items-center flex-wrap gap-2">
        <span class="d-flex align-items-center gap-2">
          <template v-if="item.picture">
            <img
              :src="pictureUrl(item.picture)"
              alt=""
              style="max-height: 60px; cursor: pointer;"
              @click="openImagePreview(pictureUrl(item.picture))"
            />
          </template>
          <span>{{ item.full_name }} — {{ item.biography || '—' }}</span>
        </span>
        <span>
          <button class="btn btn-sm btn-success me-1" data-bs-toggle="modal" data-bs-target="#editAuthorModal" @click="onEditClick(item)"><i class="bi bi-pen-fill"></i></button>
          <button class="btn btn-sm btn-danger" @click="onRemove(item)"><i class="bi bi-x"></i></button>
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
            <div class="mb-2">
              <label class="form-label">Биография</label>
              <input v-model="authorToEdit.biography" class="form-control" />
            </div>
            <div class="mb-2">
              <label class="form-label">Изменить изображение</label>
              <input
                ref="authorEditPictureRef"
                type="file"
                class="form-control"
                accept="image/*"
                @change="authorEditPictureChange"
              />
            </div>
            <div v-show="authorEditImageUrl" class="mb-2">
              <img :src="authorEditImageUrl" alt="" style="max-height: 80px;" />
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdate">Сохранить</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="imagePreviewModal" tabindex="-1" ref="imagePreviewModal">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-body text-center p-0">
            <img v-if="imagePreviewUrl" :src="imagePreviewUrl" alt="" class="img-fluid" style="max-height: 90vh;" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
