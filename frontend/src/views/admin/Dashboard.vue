<template>
	<section class="mx-auto mt-10 max-w-4xl space-y-10">

		<!-- Header -->
		<header class="space-y-2 text-center">
			<h1 class="text-3xl font-semibold text-slate-900">Panel de administración</h1>
			<p class="text-sm text-slate-600">Gestiona el sorteo y selecciona un ganador entre los participantes
				verificados.</p>
		</header>

		<!-- Main content -->
		<div class="rounded-2xl bg-white/80 p-8 shadow-2xl backdrop-blur">
			<h2 class="text-xl font-semibold text-slate-900">Sorteo de ganador</h2>
			<p class="mt-1 text-sm text-slate-600">Al seleccionar un ganador se enviará automáticamente un correo de
				notificación.</p>

			<!-- Error message -->
			<div v-if="generalError" class="mt-4 rounded-xl border border-rose-200 bg-rose-50/90 p-4 text-rose-700">
				{{ generalError }}
			</div>

			<!-- Success message -->
			<div v-if="successMessage"
				class="mt-4 rounded-xl border border-emerald-200 bg-emerald-50/80 p-4 text-emerald-700">
				{{ successMessage }}
			</div>

			<!-- Winner -->
			<div v-if="winner" class="mt-6 grid gap-4 rounded-2xl border border-slate-200 bg-white/90 p-6 shadow-inner">
				<div class="flex items-center justify-between">
					<div>
						<p class="text-sm uppercase tracking-wide text-slate-400">Ganador seleccionado</p>
						<p class="text-xl font-semibold text-slate-900">{{ fullName(winner) }}</p>
					</div>
					<span class="rounded-full px-3 py-1 text-xs font-semibold"
						:class="winner.email_sent ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'">
						{{ winner.email_sent ? 'Correo enviado' : 'Correo pendiente' }}
					</span>
				</div>
				<div class="grid gap-2 text-sm text-slate-600 md:grid-cols-2">
					<p><strong class="font-medium text-slate-700">Correo:</strong> {{ winner.email }}</p>
					<p><strong class="font-medium text-slate-700">RUT:</strong> {{ winner.rut || '—' }}</p>
				</div>
			</div>

			<!-- Actions -->
			<button type="button"
				class="mt-6 inline-flex w-full items-center justify-center rounded-lg bg-gradient-to-r from-gray-900 to-blue-900 px-5 py-3 text-sm font-semibold text-white shadow-lg transition hover:from-gray-800 hover:to-blue-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-rose-200 disabled:cursor-not-allowed disabled:opacity-60"
				:disabled="isDrawing" @click="drawWinner">
				<span v-if="!isDrawing">Generar ganador aleatorio</span>
				<span v-else>Seleccionando ganador...</span>
			</button>

		</div>
	</section>
</template>

<script>
import { apiRequest } from '@/utils/apiClient'

export default {

	name: 'AdminDashboard',
	
	data() {
		return {
			isDrawing: false,
			generalError: '',
			successMessage: '',
			winner: null,
		}
	},
	
	methods: {

		getToken() {
			return window.localStorage.getItem('adminAuthToken')
		},

		authHeaders() {
			const token = this.getToken()
			return token
				? {
					Authorization: `Token ${token}`,
				}
				: {}
		},

		ensureLogged() {
			const token = this.getToken()
			if (!token) {
				this.generalError = 'Tu sesión ha expirado. Vuelve a iniciar sesión.'
				this.$router.replace({ name: 'admin-login', query: { redirect: this.$route.fullPath } })
				return false
			}
			return true
		},

		fullName(participant) {
			return `${participant.first_name || ''} ${participant.last_name || ''}`.trim() || participant.email
		},

		async drawWinner() {
			if (!this.ensureLogged()) {
				return
			}

			this.isDrawing = true
			this.generalError = ''
			this.successMessage = ''

			try {
				const response = await apiRequest('/admin/draw-winner/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						...this.authHeaders(),
					},
				})

				this.winner = response && response.data ? response.data : null
				this.successMessage = response && response.message
					? response.message
					: 'Ganador seleccionado correctamente.'
			} catch (error) {
				const status = error && error.status
				if (status === 401 || status === 403) {
					this.generalError = 'No tienes permisos para realizar el sorteo.'
					window.localStorage.removeItem('adminAuthToken')
					this.$router.replace({ name: 'admin-login', query: { redirect: this.$route.fullPath } })
				} else {
					this.generalError = error && error.data && error.data.message
						? error.data.message
						: error && error.message
							? error.message
							: 'No pudimos completar el sorteo.'
				}
			} finally {
				this.isDrawing = false
			}
		},
		
	},
}
</script>
