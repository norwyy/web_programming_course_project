<script setup>
import { ref, computed, onBeforeMount, nextTick } from 'vue'
import axios from 'axios'
import { Modal } from 'bootstrap'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()

const currentYear = computed(() => new Date().getFullYear())

const books = ref([])
const bookStats = ref(null)
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

const filters = ref({
  title: '',
  year: '',
  author: '',
  genre: '',
  series: '',
  publisher: ''
})

const filteredBooks = computed(() => {
  return books.value.filter(book => {
    if (filters.value.title && !book.title.toLowerCase().includes(filters.value.title.toLowerCase())) {
      return false
    }
    if (filters.value.year) {
      const yearStr = String(book.year || '')
      if (!yearStr.includes(filters.value.year)) {
        return false
      }
    }
    if (filters.value.author) {
      const authorNameStr = (book.author?.full_name ?? '-').toLowerCase()
      if (!authorNameStr.includes(filters.value.author.toLowerCase())) {
        return false
      }
    }
    if (filters.value.genre) {
      const genreNameStr = (book.genre?.name ?? '-').toLowerCase()
      if (!genreNameStr.includes(filters.value.genre.toLowerCase())) {
        return false
      }
    }
    if (filters.value.series) {
      const seriesNameStr = (book.series?.name ?? '-').toLowerCase()
      if (!seriesNameStr.includes(filters.value.series.toLowerCase())) {
        return false
      }
    }
    if (filters.value.publisher) {
      const publisherNameStr = (book.publisher?.name ?? '-').toLowerCase()
      if (!publisherNameStr.includes(filters.value.publisher.toLowerCase())) {
        return false
      }
    }
    return true
  })
})

function pictureUrl(p) {
  if (!p) return ''
  return p.startsWith('http') || p.startsWith('/') ? p : '/media/' + p
}

async function fetchBooks() {
  const { data } = await axios.get('/api/books/')
  books.value = data
}

async function fetchBooksStats() {
  const { data } = await axios.get('/api/books/stats/')
  bookStats.value = data
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
  if (!bookToAdd.value.author || !bookToAdd.value.genre || !bookToAdd.value.publisher) {
    alert('Заполните все обязательные поля: Автор, Жанр, Издательство')
    return
  }

  const formData = new FormData()
  formData.set('title', bookToAdd.value.title)
  if (bookToAdd.value.year !== null && bookToAdd.value.year !== undefined && bookToAdd.value.year !== '') {
    formData.set('year', String(bookToAdd.value.year))
  }
  formData.set('description', bookToAdd.value.description || '')
  formData.set('author', String(bookToAdd.value.author))
  formData.set('genre', String(bookToAdd.value.genre))
  if (bookToAdd.value.series !== null && bookToAdd.value.series !== undefined && bookToAdd.value.series !== '') {
    formData.set('series', String(bookToAdd.value.series))
  }
  formData.set('publisher', String(bookToAdd.value.publisher))
  const file = booksPictureRef.value?.files?.[0]
  if (file) formData.append('picture', file)

  try {
    await axios.post('/api/books/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  } catch (error) {
    console.error('Ошибка при создании книги:', error.response?.data || error.message)
    alert('Ошибка: ' + (error.response?.data?.detail || JSON.stringify(error.response?.data) || error.message))
    return
  }
  bookToAdd.value = { title: '', year: null, description: '', author: null, genre: null, series: null, publisher: null }
  if (booksPictureRef.value) booksPictureRef.value.value = ''
  if (bookAddImageUrl.value) {
    URL.revokeObjectURL(bookAddImageUrl.value)
    bookAddImageUrl.value = null
  }
  await fetchBooks()
}

function onEdit(item) {
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
  if (bookToEdit.value.year !== null && bookToEdit.value.year !== undefined && bookToEdit.value.year !== '') {
    formData.set('year', String(bookToEdit.value.year))
  }
  formData.set('description', bookToEdit.value.description || '')
  formData.set('author', String(bookToEdit.value.author))
  formData.set('genre', String(bookToEdit.value.genre))
  if (bookToEdit.value.series !== null && bookToEdit.value.series !== undefined && bookToEdit.value.series !== '') {
    formData.set('series', String(bookToEdit.value.series))
  }
  formData.set('publisher', String(bookToEdit.value.publisher))
  const file = bookEditPictureRef.value?.files?.[0]
  if (file) formData.append('picture', file)

  try {
    await axios.patch(`/api/books/${bookToEdit.value.id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  } catch (error) {
    console.error('Ошибка при обновлении книги:', error.response?.data || error.message)
    alert('Ошибка: ' + (error.response?.data?.detail || JSON.stringify(error.response?.data) || error.message))
    return
  }
  cache.books = { data: null, timestamp: null }
  await Promise.all([fetchBooks(), fetchBooksStats()])
}

async function onRemove(item) {
  await axios.delete(`/api/books/${item.id}/`)
  cache.books = { data: null, timestamp: null }
  await Promise.all([fetchBooks(), fetchBooksStats()])
}

function authorName(book) {
  return book.author?.full_name ?? '-'
}

function genreName(book) {
  return book.genre?.name ?? '-'
}

function seriesName(book) {
  return book.series?.name ?? '-'
}

function publisherName(book) {
  return book.publisher?.name ?? '-'
}

function canEdit(item) {
  if (!userStore.user) return false
  if (userStore.isAdmin()) return true
  return item.user === userStore.user.id
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

onBeforeMount(async () => {
  await Promise.all([fetchOptions(), fetchBooks(), fetchBooksStats()])
})
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2 class="mb-0">Книги</h2>
      <div v-if="bookStats" class="text-muted">
        Всего: <strong>{{ bookStats.count }}</strong>
        <span v-if="bookStats.avg_year" class="ms-3">Средний год: <strong>{{ Math.round(bookStats.avg_year) }}</strong></span>
        <span v-if="bookStats.min_year" class="ms-3">От: <strong>{{ bookStats.min_year }}</strong></span>
        <span v-if="bookStats.max_year" class="ms-2">До: <strong>{{ bookStats.max_year }}</strong></span>
      </div>
    </div>
    <form v-if="userStore.isAuthenticated()" @submit.prevent="onAdd" class="row g-2 mb-4 flex-wrap align-items-end">
      <div class="col-12 col-md">
        <label class="form-label">Название</label>
        <input v-model="bookToAdd.title" class="form-control" placeholder="Название" required />
      </div>
      <div class="col-6 col-md-1">
        <label class="form-label">Год</label>
        <input v-model.number="bookToAdd.year" type="number" class="form-control" placeholder="Год" min="1000" :max="currentYear" />
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
    <div class="mb-2">
      <strong>Фильтры</strong>
    </div>
    <div class="table-responsive">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Название</th>
            <th>Год</th>
            <th>Автор</th>
            <th>Жанр</th>
            <th>Серия</th>
            <th>Издательство</th>
            <th></th>
          </tr>
          <tr>
            <th>
              <input
                v-model="filters.title"
                type="text"
                class="form-control form-control-sm"
              />
            </th>
            <th>
              <input
                v-model="filters.year"
                type="text"
                class="form-control form-control-sm"
              />
            </th>
            <th>
              <input
                v-model="filters.author"
                type="text"
                class="form-control form-control-sm"
              />
            </th>
            <th>
              <input
                v-model="filters.genre"
                type="text"
                class="form-control form-control-sm"
              />
            </th>
            <th>
              <input
                v-model="filters.series"
                type="text"
                class="form-control form-control-sm"
              />
            </th>
            <th>
              <input
                v-model="filters.publisher"
                type="text"
                class="form-control form-control-sm"
              />
            </th>
            <th>
              <button
                class="btn btn-sm btn-outline-secondary"
                @click="filters = { title: '', year: '', author: '', genre: '', series: '', publisher: '' }"
                title="Очистить фильтры"
              >
                ✕
              </button>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredBooks" :key="item.id">
            <td>{{ item.title }}</td>
            <td>{{ item.year || '-' }}</td>
            <td>{{ authorName(item) }}</td>
            <td>{{ genreName(item) }}</td>
            <td>{{ seriesName(item) }}</td>
            <td>{{ publisherName(item) }}</td>
            <td>
              <div class="d-flex align-items-center gap-2 justify-content-end">
                <template v-if="item.picture">
                  <img
                    :src="pictureUrl(item.picture)"
                    alt=""
                    style="max-height: 60px; cursor: pointer;"
                    @click.stop="openImagePreview(pictureUrl(item.picture))"
                    @mousedown.stop
                  />
                </template>
                <template v-if="canEdit(item)">
                  <button class="btn btn-sm btn-success" data-bs-toggle="modal" data-bs-target="#editBookModal" @click="onEdit(item)"><i class="bi bi-pen-fill"></i></button>
                  <button class="btn btn-sm btn-danger" @click="onRemove(item)"><i class="bi bi-x"></i></button>
                </template>
              </div>
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
                <input v-model.number="bookToEdit.year" type="number" class="form-control" min="1000" :max="currentYear" />
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
                  <option :value="null">-</option>
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
