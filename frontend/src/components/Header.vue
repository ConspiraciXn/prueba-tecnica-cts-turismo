<template>
  <header class="bg-gradient-to-r from-rose-600 via-purple-600 to-indigo-600 text-white shadow-lg">
    <div class="mx-auto flex max-w-7xl flex-col gap-6 px-6 py-5 sm:px-8 md:flex-row md:items-center md:justify-between">
      <div class="flex flex-1 items-center gap-4">
        <img src="/images/logo-cts.png" alt="Logo CTS Turismo" class="h-12 w-12 flex-shrink-0 rounded-full border border-white/30 bg-white/10 p-1" />
        <div>
          <p class="text-base font-medium uppercase tracking-[0.2em] text-white/80">Sorteo de San Valentín</p>
          <p class="text-2xl font-semibold leading-tight">CTS Turismo</p>
        </div>
      </div>
      <nav class="flex flex-wrap items-center justify-center gap-3 md:justify-end">
        <RouterLink
          v-for="link in navigation"
          :key="link.label"
          :to="link.to"
          class="rounded-full px-4 py-2 text-sm font-medium transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white/70"
          :class="isActive(link.to) ? 'bg-white text-rose-600 shadow' : 'bg-white/10 hover:bg-white/20'"
        >
          {{ link.label }}
        </RouterLink>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const navigation = [
  { label: 'Registro', to: { name: 'register' } },
  { label: 'Verificar correo', to: { name: 'email-verification' } },
  { label: 'Acceso admin', to: { name: 'admin-login' } },
]

const isActive = (to) => {
  const target = (typeof to === 'string' ? { path: to } : to) ?? {}

  if (target.name) {
    return route.name === target.name
  }

  if (target.path) {
    return route.path === target.path
  }

  return false
}
</script>

<style scoped>
nav :deep(a.router-link-active) {
  text-decoration: none;
}
</style>
