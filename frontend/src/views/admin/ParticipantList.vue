<template>
	<section class="mx-auto my-8 max-w-5xl space-y-10">

		<!-- Header -->
		<header class="space-y-3 text-center">
			<h1 class="text-3xl font-semibold text-slate-900">Participantes registrados</h1>
			<p class="text-sm text-slate-600">Consulta el estado de verificación, busca por nombre, correo o RUT y
				filtra por
				estado.</p>
		</header>

		<!-- List -->
		<div class="flex flex-col gap-4 rounded-2xl bg-white/80 p-6 shadow-xl backdrop-blur">

			<!-- Search and filters -->
			<form class="grid gap-4 md:grid-cols-[1fr,200px,auto]" @submit.prevent="fetchParticipants">

				<!-- Search input -->
				<div>
					<label for="search" class="mb-1 block text-sm font-medium text-slate-700">Buscar</label>
					<input id="search" v-model.trim="filters.search" type="text"
						class="w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-900 shadow-sm outline-none transition focus:border-rose-400 focus:ring-2 focus:ring-rose-200"
						placeholder="Nombre, correo o RUT" />
				</div>

				<!-- Status filter -->
				<div>
					<label for="verified" class="mb-1 block text-sm font-medium text-slate-700">Estado</label>
					<select id="verified" v-model="filters.verified"
						class="w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-900 shadow-sm outline-none transition focus:border-rose-400 focus:ring-2 focus:ring-rose-200">
						<option value="">Todos</option>
						<option value="true">Verificados</option>
						<option value="false">Pendientes</option>
					</select>
				</div>

				<!-- Search actions -->
				<div class="flex items-end gap-3">
					<button type="submit"
						class="inline-flex flex-1 items-center justify-center rounded-lg bg-gradient-to-r from-gray-900 to-blue-900 px-4 py-2.5 text-sm font-semibold text-white shadow-lg transition hover:from-gray-800 hover:to-blue-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-rose-200"
						:disabled="isLoading">
						<span v-if="!isLoading">Aplicar filtros</span>
						<span v-else>Actualizando...</span>
					</button>
					<button type="button"
						class="inline-flex items-center justify-center rounded-lg border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-700 transition hover:border-slate-300 hover:bg-slate-50"
						@click="resetFilters" :disabled="isLoading">
						Limpiar
					</button>
				</div>

			</form>

			<!-- Error message -->
			<div v-if="generalError" class="rounded-xl border border-rose-200 bg-rose-50/90 p-4 text-rose-700">
				{{ generalError }}
			</div>

			<!-- Loading fallback -->
			<div v-if="isLoading" class="rounded-xl border border-slate-200 bg-slate-50/80 p-4 text-slate-600">
				Cargando participantes...
			</div>

			<!-- No participants found -->
			<div v-if="!isLoading && participants.length === 0"
				class="rounded-xl border border-slate-200 bg-white/80 p-6 text-center text-slate-500">
				No se encontraron participantes con los filtros actuales.
			</div>

			<!-- Participants list -->
			<div v-if="participants.length"
				class="overflow-hidden rounded-2xl border border-slate-200 bg-white/90 shadow-lg">
				<table class="min-w-full divide-y divide-slate-200">

					<!-- Table head -->
					<thead class="bg-slate-50">
						<tr class="text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
							<th class="px-6 py-3">Participante</th>
							<th class="px-6 py-3">Correo</th>
							<th class="px-6 py-3">RUT</th>
							<th class="px-6 py-3">Registrado</th>
							<th class="px-6 py-3 text-center">Estado</th>
						</tr>
					</thead>

					<!-- Table body -->
					<tbody class="divide-y divide-slate-100 bg-white">
						<tr v-for="participant in participants" :key="participant.id" class="text-sm text-slate-700">
							<td class="px-6 py-4">
								<p class="font-medium text-slate-900">{{ formatName(participant) }}</p>
							</td>
							<td class="px-6 py-4">
								<p class="text-sm text-slate-600">{{ participant.email }}</p>
							</td>
							<td class="px-6 py-4">
								<span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">{{
									participant.rut
									|| '—' }}</span>
							</td>
							<td class="px-6 py-4">
								<p class="text-xs text-slate-500">{{ formatDate(participant.registered_at) }}</p>
							</td>
							<td class="px-6 py-4 text-center">
								<span
									class="inline-flex items-center justify-center rounded-full px-3 py-1 text-xs font-semibold"
									:class="participant.verified ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'">
									{{ participant.verified ? 'Verificado' : 'Pendiente' }}
								</span>
							</td>
						</tr>
					</tbody>

				</table>
			</div>
		</div>
	</section>
</template>

<script>
import { apiRequest } from '@/utils/apiClient'

export default {

	name: 'AdminParticipantList',
	
	data() {
		return {
			participants: [],
			isLoading: false,
			generalError: '',
			filters: {
				search: '',
				verified: '',
			},
		}
	},
	
	created() {
		this.fetchParticipants()
	},
	
	methods: {

		authToken() {
			return window.localStorage.getItem('adminAuthToken')
		},

		authHeaders() {
			const token = this.authToken()
			return token
				? {
					Authorization: `Token ${token}`,
				}
				: {}
		},

		redirectToLogin() {
			window.localStorage.removeItem('adminAuthToken')
			this.$router.replace({ name: 'admin-login', query: { redirect: this.$route.fullPath } })
		},

		formatName(participant) {
			return `${participant.first_name || ''} ${participant.last_name || ''}`.trim() || 'Participante sin nombre'
		},

		formatDate(isoString) {
			if (!isoString) {
				return '—'
			}
			const date = new Date(isoString)
			return date.toLocaleString('es-CL', {
				year: 'numeric',
				month: 'short',
				day: 'numeric',
				hour: '2-digit',
				minute: '2-digit',
			})
		},

		buildQuery() {
			const params = new URLSearchParams()
			if (this.filters.search) {
				params.set('search', this.filters.search)
			}
			if (this.filters.verified) {
				params.set('verified', this.filters.verified)
			}
			const query = params.toString()
			return query ? `?${query}` : ''
		},

		async fetchParticipants() {
			const token = this.authToken()
			if (!token) {
				this.generalError = 'Tu sesión ha expirado. Vuelve a iniciar sesión.'
				this.redirectToLogin()
				return
			}

			this.isLoading = true
			this.generalError = ''

			try {
				const response = await apiRequest(`/admin/participants/${this.buildQuery()}`, {
					method: 'GET',
					headers: this.authHeaders(),
				})

				this.participants = response && response.data && response.data.results ? response.data.results : []
			} catch (error) {
				const status = error && error.status
				if (status === 401 || status === 403) {
					this.generalError = 'No tienes permisos o tu sesión expiró.'
					this.redirectToLogin()
				} else {
					this.generalError = error && error.data && error.data.message
						? error.data.message
						: error && error.message
							? error.message
							: 'No pudimos obtener la lista de participantes.'
				}
				this.participants = []
			} finally {
				this.isLoading = false
			}
		},

		resetFilters() {
			this.filters.search = ''
			this.filters.verified = ''
			this.fetchParticipants()
		},
		
	},
}
</script>
