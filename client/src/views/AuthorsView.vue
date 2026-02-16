<script setup>
import { ref, computed, onBeforeMount, nextTick } from 'vue'
import axios from 'axios'
import { Modal } from 'bootstrap'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()

const authors = ref([])
const authorStats = ref(null)
const authorToAdd = ref({ full_name: '', biography: '' })
const authorToEdit = ref({})
const authorsPictureRef = ref()
const authorAddImageUrl = ref()
const authorEditPictureRef = ref()
const authorEditImageUrl = ref()
const imagePreviewUrl = ref()
const imagePreviewModal = ref()


const filters = ref({
  full_name: '',
  biography: ''
})


const filteredAuthors = computed(() => {
  return authors.value.filter(author => {
    if (filters.value.full_name && !author.full_name.toLowerCase().includes(filters.value.full_name.toLowerCase())) {
      return false
    }
    if (filters.value.biography && !(author.biography || '').toLowerCase().includes(filters.value.biography.toLowerCase())) {
      return false
    }
    return true
  })
})

function pictureUrl(p) {
  if (!p) return ''
  return p.startsWith('http') || p.startsWith('/') ? p : '/media/' + p
}

async function fetchAuthors() {
  const { data } = await axios.get('/api/authors/')
  authors.value = data
}

async function fetchAuthorsStats() {
  const { data } = await axios.get('/api/authors/stats/')
  authorStats.value = data
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
  await Promise.all([fetchAuthors(), fetchAuthorsStats()])
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
  await Promise.all([fetchAuthors(), fetchAuthorsStats()])
}

async function onRemove(item) {
  await axios.delete(`/api/authors/${item.id}/`)
  await Promise.all([fetchAuthors(), fetchAuthorsStats()])
}

function openImagePreview(url) {
  if (!url) return
  imagePreviewUrl.value = url
  nextTick(() => {
    try {
      const modalElement = imagePreviewModal.value || document.getElementById('imagePreviewModal')
      if (!modalElement) {
        console.error('Modal element not found')
        return
      }
      const existingModal = Modal.getInstance(modalElement)
      if (existingModal) {
        existingModal.dispose()
      }
      const modal = new Modal(modalElement, {
        backdrop: true,
        keyboard: true
      })
      modal.show()
    } catch (error) {
      console.error('Error opening modal:', error)
    }
  })
}


function canEdit(item) {
  if (!userStore.user) return false
  if (userStore.isAdmin()) return true
  return item.user === userStore.user.id
}

onBeforeMount(async () => {
  await Promise.all([fetchAuthors(), fetchAuthorsStats()])
})
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2 class="mb-0">Авторы</h2>
      <div v-if="authorStats" class="text-muted">
        Всего: <strong>{{ authorStats.count }}</strong>
        <span v-if="authorStats.top_author_name" class="ms-3">
          Самый продуктивный автор: <strong>{{ authorStats.top_author_name }}</strong> ({{ authorStats.top_author_books_count }} книг)
        </span>
      </div>
    </div>
    <form v-if="userStore.isAuthenticated()" @submit.prevent="onAdd" class="row g-2 mb-4 flex-wrap align-items-end">
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
    <div class="mb-2">
      <strong>Фильтры</strong>
    </div>
    <div class="row g-2 mb-3">
      <div class="col-md-6">
        <label class="form-label mb-1" style="font-weight: normal;">ФИО</label>
        <input
          v-model="filters.full_name"
          type="text"
          class="form-control"
        />
      </div>
      <div class="col-md-6">
        <label class="form-label mb-1" style="font-weight: normal;">Биография</label>
        <input
          v-model="filters.biography"
          type="text"
          class="form-control"
        />
      </div>
      <div class="col-auto">
        <button
          class="btn btn-outline-secondary"
          @click="filters = { full_name: '', biography: '' }"
        >
          Очистить фильтры
        </button>
      </div>
    </div>
    <ul class="list-group">
      <li v-for="item in filteredAuthors" :key="item.id" class="list-group-item d-flex justify-content-between align-items-start gap-2">
        <span class="flex-grow-1" style="min-width: 0; word-break: break-word;">{{ item.full_name }} - {{ item.biography || '-' }}</span>
        <div class="d-flex align-items-center gap-2 flex-shrink-0">
          <template v-if="item.picture">
            <img
              :src="pictureUrl(item.picture)"
              alt=""
              style="max-height: 60px; cursor: pointer;"
              @click.stop="openImagePreview(pictureUrl(item.picture))"
              @mousedown.stop
            />
          </template>
          <div v-if="canEdit(item)" class="d-flex gap-1">
            <button class="btn btn-sm btn-success" data-bs-toggle="modal" data-bs-target="#editAuthorModal" @click="onEditClick(item)"><i class="bi bi-pen-fill"></i></button>
            <button class="btn btn-sm btn-danger" @click="onRemove(item)"><i class="bi bi-x"></i></button>
          </div>
        </div>
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

    <div class="modal fade" id="imagePreviewModal" tabindex="-1" ref="imagePreviewModal" data-bs-backdrop="true" data-bs-keyboard="true">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Предпросмотр изображения</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
          </div>
          <div class="modal-body text-center p-0">
            <img v-if="imagePreviewUrl" :src="imagePreviewUrl" alt="" class="img-fluid" style="max-height: 90vh; width: 100%; object-fit: contain;" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
