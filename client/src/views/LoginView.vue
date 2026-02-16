<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const username = ref('')
const password = ref('')
const error = ref('')
const isLoading = ref(false)

async function handleLogin() {
  error.value = ''
  isLoading.value = true
  
  try {
    await userStore.login(username.value, password.value)
    router.push('/')
  } catch (err) {
    error.value = userStore.error || 'Ошибка при авторизации'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-4">
        <div class="card mt-5">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">Авторизация</h2>
            
            <div v-if="error" class="alert alert-danger" role="alert">
              {{ error }}
            </div>

            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label for="username" class="form-label">Имя пользователя</label>
                <input
                  id="username"
                  v-model="username"
                  type="text"
                  class="form-control"
                  required
                  autocomplete="username"
                  :disabled="isLoading"
                />
              </div>

              <div class="mb-3">
                <label for="password" class="form-label">Пароль</label>
                <input
                  id="password"
                  v-model="password"
                  type="password"
                  class="form-control"
                  required
                  autocomplete="current-password"
                  :disabled="isLoading"
                />
              </div>

              <button
                type="submit"
                class="btn btn-primary w-100"
                :disabled="isLoading"
              >
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                {{ isLoading ? 'Вход...' : 'Войти' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
