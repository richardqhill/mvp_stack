<template>
  <div>
    <h1>User Info</h1>
    <p v-if="user">ID: {{ user.id }}, Name: {{ user.name }}</p>
    <p v-else>Loading user data...</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const user = ref<{ id: number; name: string } | null>(null)

onMounted(async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/user/1`)
    if (!response.ok) throw new Error('Network response was not ok')
    user.value = await response.json()
  } catch (error) {
    console.error('Error fetching user:', error)
  }
})
</script>
