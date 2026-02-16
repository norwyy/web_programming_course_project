import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const isLoading = ref(false)
  const error = ref(null)

  async function fetchCurrentUser() {
    isLoading.value = true
    error.value = null
    try {
      const { data } = await axios.get('/api/auth/current-user/')
      user.value = data
      return data
    } catch (err) {
      if (err.response?.status === 401) {
        user.value = null
        return null
      }
      error.value = err.response?.data?.error || 'Ошибка при получении информации о пользователе'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function login(username, password) {
    isLoading.value = true
    error.value = null
    try {
      const { data } = await axios.post('/api/auth/login/', {
        username,
        password
      })
      user.value = data
      return data
    } catch (err) {
      error.value = err.response?.data?.error || 'Ошибка при авторизации'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function logout() {
    isLoading.value = true
    error.value = null
    try {
      await axios.post('/api/auth/logout/')
      user.value = null
    } catch (err) {
      error.value = err.response?.data?.error || 'Ошибка при выходе'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const isAuthenticated = () => {
    return user.value !== null
  }

  const isAdmin = () => {
    return user.value?.is_superuser === true
  }

  return {
    user,
    isLoading,
    error,
    fetchCurrentUser,
    login,
    logout,
    isAuthenticated,
    isAdmin
  }
})
