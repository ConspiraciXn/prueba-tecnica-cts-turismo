<template>
	<footer class="bg-gray-900 text-slate-100">
		<div class="mx-auto max-w-7xl px-6 py-10 sm:px-8">

			<!-- Main footer -->
			<div class="grid gap-10 md:grid-cols-[2fr,1fr,1fr]">

				<div class="space-y-4">
					<div class="flex items-center gap-3">
						<img src="/images/logo-cts.png" alt="Logo CTS Turismo"
							class="h-12" />
					</div>
					<p class="text-sm text-white/70 md:w-1/2">
						Abriendo rutas y creando destinos desde nuestros inicios. Diseñamos y operamos experiencias
						memorables para parejas, familias y grupos inspirados en el amor por viajar.
					</p>
				</div>

			</div>

			<!-- Seocndary footer -->
			<div
				class="mt-10 flex flex-col gap-4 border-t border-white/10 pt-6 text-xs text-white/50 sm:flex-row sm:items-center sm:justify-between">
				<p>&copy; {{ currentYear }} CTS Turismo. Todos los derechos reservados.</p>
				<div class="flex flex-wrap gap-4">
					<a href="#" class="transition hover:text-rose-300">Términos</a>
					<a href="#" class="transition hover:text-rose-300">Privacidad</a>
					<a href="#" class="transition hover:text-rose-300">Soporte</a>
				</div>
			</div>

		</div>
	</footer>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

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
