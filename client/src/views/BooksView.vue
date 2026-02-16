<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const books = ref([])
const authors = ref([])
const genres = ref([])
const series = ref([])
const publishers = ref([])

const bookToAdd = ref({
  title: '',
  year: null,
  description: '',
  author: null,
  genre: null,
  series: null,
  publisher: null,
})
const bookToEdit = ref({})
const booksPictureRef = ref()
const bookAddImageUrl = ref()
const bookEditPictureRef = ref()
const bookEditImageUrl = ref()
const imagePreviewUrl = ref()
const imagePreviewModal = ref()

function pictureUrl(p) {
  if (!p) return ''
  return p.startsWith('http') || p.startsWith('/') ? p : '/media/' + p
}

async function fetchBooks() {
  const { data } = await axios.get('/api/books/')
  books.value = data
}

async function fetchOptions() {
  const [a, g, s, p] = await Promise.all([
    axios.get('/api/authors/'),
    axios.get('/api/genres/'),
    axios.get('/api/series/'),
    axios.get('/api/publishers/'),
  ])
  authors.value = a.data
  genres.value = g.data
  series.value = s.data
  publishers.value = p.data
}

function bookAddPictureChange() {
  const file = booksPictureRef.value?.files?.[0]
  if (file) {
    if (bookAddImageUrl.value) URL.revokeObjectURL(bookAddImageUrl.value)
    bookAddImageUrl.value = URL.createObjectURL(file)
  }
}

function bookEditPictureChange() {
  const file = bookEditPictureRef.value?.files?.[0]
  if (file) {
    if (bookEditImageUrl.value) URL.revokeObjectURL(bookEditImageUrl.value)
    bookEditImageUrl.value = URL.createObjectURL(file)
  }
}

async function onAdd() {
  const formData = new FormData()
  formData.set('title', bookToAdd.value.title)
  formData.set('year', bookToAdd.value.year ?? '')
  formData.set('description', bookToAdd.value.description || '')
  formData.set('author', bookToAdd.value.author)
  formData.set('genre', bookToAdd.value.genre)
  formData.set('series', bookToAdd.value.series ?? '')
  formData.set('publisher', bookToAdd.value.publisher)
  const file = booksPictureRef.value?.files?.[0]
  if (file) formData.append('picture', file)

  await axios.post('/api/books/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  bookToAdd.value = { title: '', year: null, description: '', author: null, genre: null, series: null, publisher: null }
  if (booksPictureRef.value) booksPictureRef.value.value = ''
  if (bookAddImageUrl.value) {
    URL.revokeObjectURL(bookAddImageUrl.value)
    bookAddImageUrl.value = null
  }
  await fetchBooks()
}

function onEditClick(item) {
  bookToEdit.value = {
    id: item.id,
    title: item.title,
    year: item.year,
    description: item.description || '',
    author: item.author?.id ?? item.author,
    genre: item.genre?.id ?? item.genre,
    series: item.series?.id ?? item.series ?? null,
    publisher: item.publisher?.id ?? item.publisher,
    picture: item.picture,
  }
  bookEditImageUrl.value = item.picture ? pictureUrl(item.picture) : null
  if (bookEditPictureRef.value) bookEditPictureRef.value.value = ''
}

async function onUpdate() {
  const formData = new FormData()
  formData.set('title', bookToEdit.value.title)
  formData.set('year', bookToEdit.value.year ?? '')
  formData.set('description', bookToEdit.value.description || '')
  formData.set('author', bookToEdit.value.author)
  formData.set('genre', bookToEdit.value.genre)
  formData.set('series', bookToEdit.value.series ?? '')
  formData.set('publisher', bookToEdit.value.publisher)
  const file = bookEditPictureRef.value?.files?.[0]
  if (file) formData.append('picture', file)

  await axios.patch(`/api/books/${bookToEdit.value.id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  await fetchBooks()
}

async function onRemove(item) {
  await axios.delete(`/api/books/${item.id}/`)
  await fetchBooks()
}

function authorName(book) {
  return book.author?.full_name ?? '—'
}

function genreName(book) {
  return book.genre?.name ?? '—'
}

function seriesName(book) {
  return book.series?.name ?? '—'
}

function publisherName(book) {
  return book.publisher?.name ?? '—'
}

function openImagePreview(url) {
  imagePreviewUrl.value = url
  const modal = new window.bootstrap.Modal(imagePreviewModal.value)
  modal.show()
}

onBeforeMount(async () => {
  await fetchOptions()
  await fetchBooks()
})
</script>

<template>
  <div>
    <h2 class="mb-3">Книги</h2>
    <form @submit.prevent="onAdd" class="row g-2 mb-4 flex-wrap align-items-end">
      <div class="col-12 col-md">
        <label class="form-label">Название</label>
        <input v-model="bookToAdd.title" class="form-control" placeholder="Название" required />
      </div>
      <div class="col-6 col-md-1">
        <label class="form-label">Год</label>
        <input v-model.number="bookToAdd.year" type="number" class="form-control" placeholder="Год" />
      </div>
      <div class="col-6 col-md">
        <label class="form-label">Описание</label>
        <input v-model="bookToAdd.description" class="form-control" placeholder="Описание" />
      </div>
      <div class="col-6 col-md">
        <label class="form-label">Автор</label>
        <select v-model="bookToAdd.author" class="form-select" required>
          <option :value="null">Автор</option>
          <option v-for="a in authors" :key="a.id" :value="a.id">{{ a.full_name }}</option>
        </select>
      </div>
      <div class="col-6 col-md">
        <label class="form-label">Жанр</label>
        <select v-model="bookToAdd.genre" class="form-select" required>
          <option :value="null">Жанр</option>
          <option v-for="g in genres" :key="g.id" :value="g.id">{{ g.name }}</option>
        </select>
      </div>
      <div class="col-6 col-md">
        <label class="form-label">Серия</label>
        <select v-model="bookToAdd.series" class="form-select">
          <option :value="null">Серия</option>
          <option v-for="s in series" :key="s.id" :value="s.id">{{ s.name }}</option>
        </select>
      </div>
      <div class="col-6 col-md">
        <label class="form-label">Издательство</label>
        <select v-model="bookToAdd.publisher" class="form-select" required>
          <option :value="null">Издательство</option>
          <option v-for="p in publishers" :key="p.id" :value="p.id">{{ p.name }}</option>
        </select>
      </div>
      <div class="col-auto">
        <label class="form-label">Обложка</label>
        <input
          ref="booksPictureRef"
          type="file"
          class="form-control"
          accept="image/*"
          @change="bookAddPictureChange"
        />
      </div>
      <div class="col-auto" v-show="bookAddImageUrl">
        <img :src="bookAddImageUrl" alt="" style="max-height: 60px;" />
      </div>
      <div class="col-auto">
        <button type="submit" class="btn btn-primary">Добавить</button>
      </div>
    </form>
    <div class="table-responsive">
      <table class="table table-striped">
        <thead>
          <tr>
            <th></th>
            <th>Название</th>
            <th>Год</th>
            <th>Автор</th>
            <th>Жанр</th>
            <th>Серия</th>
            <th>Издательство</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in books" :key="item.id">
            <td>
              <template v-if="item.picture">
                <img
                  :src="pictureUrl(item.picture)"
                  alt=""
                  style="max-height: 60px; cursor: pointer;"
                  @click="openImagePreview(pictureUrl(item.picture))"
                />
              </template>
              <span v-else class="text-muted">—</span>
            </td>
            <td>{{ item.title }}</td>
            <td>{{ item.year || '—' }}</td>
            <td>{{ authorName(item) }}</td>
            <td>{{ genreName(item) }}</td>
            <td>{{ seriesName(item) }}</td>
            <td>{{ publisherName(item) }}</td>
            <td>
              <button class="btn btn-sm btn-success me-1" data-bs-toggle="modal" data-bs-target="#editBookModal" @click="onEditClick(item)"><i class="bi bi-pen-fill"></i></button>
              <button class="btn btn-sm btn-danger" @click="onRemove(item)"><i class="bi bi-x"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="modal fade" id="editBookModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать книгу</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="row g-2 mb-2">
              <div class="col-12">
                <label class="form-label">Название</label>
                <input v-model="bookToEdit.title" class="form-control" />
              </div>
              <div class="col-6">
                <label class="form-label">Год</label>
                <input v-model.number="bookToEdit.year" type="number" class="form-control" />
              </div>
              <div class="col-12">
                <label class="form-label">Описание</label>
                <input v-model="bookToEdit.description" class="form-control" />
              </div>
              <div class="col-6">
                <label class="form-label">Автор</label>
                <select v-model="bookToEdit.author" class="form-select">
                  <option v-for="a in authors" :key="a.id" :value="a.id">{{ a.full_name }}</option>
                </select>
              </div>
              <div class="col-6">
                <label class="form-label">Жанр</label>
                <select v-model="bookToEdit.genre" class="form-select">
                  <option v-for="g in genres" :key="g.id" :value="g.id">{{ g.name }}</option>
                </select>
              </div>
              <div class="col-6">
                <label class="form-label">Серия</label>
                <select v-model="bookToEdit.series" class="form-select">
                  <option :value="null">—</option>
                  <option v-for="s in series" :key="s.id" :value="s.id">{{ s.name }}</option>
                </select>
              </div>
              <div class="col-6">
                <label class="form-label">Издательство</label>
                <select v-model="bookToEdit.publisher" class="form-select">
                  <option v-for="p in publishers" :key="p.id" :value="p.id">{{ p.name }}</option>
                </select>
              </div>
              <div class="col-12">
                <label class="form-label">Изменить обложку</label>
                <input
                  ref="bookEditPictureRef"
                  type="file"
                  class="form-control"
                  accept="image/*"
                  @change="bookEditPictureChange"
                />
              </div>
              <div v-show="bookEditImageUrl" class="col-12">
                <img :src="bookEditImageUrl" alt="" style="max-height: 80px;" />
              </div>
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
