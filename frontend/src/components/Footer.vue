<template>
  <footer class="bg-slate-950 text-slate-100">
    <div class="mx-auto max-w-7xl px-6 py-10 sm:px-8">
      <div class="grid gap-10 md:grid-cols-[2fr,1fr,1fr]">
        <div class="space-y-4">
          <div class="flex items-center gap-3">
            <img src="/images/logo-cts.png" alt="Logo CTS Turismo" class="h-12 w-12 rounded-full border border-white/20 bg-white/10 p-1" />
            <div>
              <p class="text-lg font-semibold">CTS Turismo</p>
              <p class="text-sm uppercase tracking-[0.2em] text-white/60">Sorteo de San Valentín</p>
            </div>
          </div>
          <p class="text-sm text-white/70">
            Abriendo rutas y creando destinos desde nuestros inicios. Diseñamos y operamos experiencias memorables para parejas, familias y grupos inspirados en el amor por viajar.
          </p>
        </div>

        <div class="space-y-3">
          <h3 class="text-sm font-semibold uppercase tracking-wide text-white/70">Explora</h3>
          <nav class="flex flex-col gap-2 text-sm">
            <RouterLink
              v-for="link in navigation"
              :key="link.label"
              :to="link.to"
              class="transition hover:text-rose-300 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-rose-200"
            >
              {{ link.label }}
            </RouterLink>
          </nav>
        </div>

        <div class="space-y-3">
          <h3 class="text-sm font-semibold uppercase tracking-wide text-white/70">Contacto</h3>
          <ul class="space-y-2 text-sm text-white/70">
            <li>consultas@ctsturismo.com</li>
            <li>+54 (11) 5555-1234</li>
            <li>Buenos Aires, Argentina</li>
          </ul>
        </div>
      </div>

      <div class="mt-10 flex flex-col gap-4 border-t border-white/10 pt-6 text-xs text-white/50 sm:flex-row sm:items-center sm:justify-between">
        <p>&copy; {{ currentYear }} CTS Turismo. Todos los derechos reservados.</p>
        <div class="flex flex-wrap gap-4">
          <a href="#" class="hover:text-rose-300 transition">Términos</a>
          <a href="#" class="hover:text-rose-300 transition">Privacidad</a>
          <a href="#" class="hover:text-rose-300 transition">Soporte</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'

const navigation = [
  { label: 'Registro', to: { name: 'register' } },
  { label: 'Verificar correo', to: { name: 'email-verification' } },
  { label: 'Acceso admin', to: { name: 'admin-login' } },
]

const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped>
nav :deep(a.router-link-active) {
  color: #fbcfe8;
}
</style>
