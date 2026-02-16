<script setup>
import { ref, computed, onBeforeMount } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const books = ref([])

async function fetchBooks() {
  const { data } = await axios.get('/api/books/')
  books.value = data.slice(0, 10)
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

function pictureUrl(p) {
  if (!p) return ''
  return p.startsWith('http') || p.startsWith('/') ? p : '/media/' + p
}

onBeforeMount(async () => {
  await fetchBooks()
})
</script>

<template>
  <main>
    <h1 class="mb-4">Каталог книг</h1>
    
    <h2 class="mb-3">Последние книги</h2>
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
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in books" :key="item.id">
            <td>{{ item.title }}</td>
            <td>{{ item.year || '-' }}</td>
            <td>{{ authorName(item) }}</td>
            <td>{{ genreName(item) }}</td>
            <td>{{ seriesName(item) }}</td>
            <td>{{ publisherName(item) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="text-center mt-3">
      <RouterLink to="/books" class="btn btn-primary">Посмотреть все книги</RouterLink>
    </div>
  </main>
</template>
