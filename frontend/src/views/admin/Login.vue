<template>
	<section class="mx-auto my-12 max-w-md rounded-2xl bg-white/80 p-8 shadow-2xl backdrop-blur space-y-10">

		<!-- Header -->
		<header class="text-center">
			<h1 class="text-3xl font-semibold text-slate-900">Panel administrativo</h1>
			<p class="mt-2 text-sm text-slate-600">Inicia sesión con tu correo institucional para gestionar el sorteo.
			</p>
		</header>

		<!-- Error message -->
		<div v-if="generalError" class="mb-6 rounded-xl border border-rose-200 bg-rose-50/90 p-4 text-rose-700">
			{{ generalError }}
		</div>

		<!-- Success message -->
		<div v-if="successMessage"
			class="mb-6 rounded-xl border border-emerald-200 bg-emerald-50/80 p-5 text-emerald-700">
			{{ successMessage }}
		</div>

		<!-- Form -->
		<form class="space-y-6" @submit.prevent="submitForm">

			<!-- Email -->
			<div>
				<label for="email" class="mb-1 block text-sm font-medium text-slate-700">Correo electrónico</label>
				<input id="email" v-model.trim="form.email" type="email"
					class="w-full rounded-lg border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-rose-400 focus:ring-2 focus:ring-rose-200"
					:class="{ 'border-rose-400 focus:ring-rose-300': fieldErrors('email').length }"
					placeholder="admin@ctsturismo.com" required />
				<p v-if="fieldErrors('email').length" class="mt-2 text-sm text-rose-600">
					{{ fieldErrors('email').join(' ') }}
				</p>
			</div>

			<!-- Password -->
			<div>
				<label for="password" class="mb-1 block text-sm font-medium text-slate-700">Contraseña</label>
				<input id="password" v-model="form.password" type="password"
					class="w-full rounded-lg border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-rose-400 focus:ring-2 focus:ring-rose-200"
					:class="{ 'border-rose-400 focus:ring-rose-300': fieldErrors('password').length }"
					placeholder="********" required />
				<p v-if="fieldErrors('password').length" class="mt-2 text-sm text-rose-600">
					{{ fieldErrors('password').join(' ') }}
				</p>
			</div>

			<!-- Actions -->
			<button type="submit"
				class="inline-flex w-full items-center justify-center rounded-lg bg-gradient-to-r from-gray-900 to-blue-900 px-6 py-3 text-base font-semibold text-white shadow-lg transition hover:from-gray-800 hover:to-blue-800 disabled:cursor-not-allowed disabled:opacity-60 cursor-pointer"
				:disabled="isSubmitting">
				<span v-if="!isSubmitting">Ingresar</span>
				<span v-else>Validando...</span>
			</button>

		</form>

	</section>
</template>

<script>
import { apiRequest } from '@/utils/apiClient'

export default {
	
	name: 'AdminLogin',

	data() {
		return {
			form: {
				email: '',
				password: '',
			},
			isSubmitting: false,
			generalError: '',
			successMessage: '',
			errors: {},
		}
	},

	created() {

		const existingToken = window.localStorage.getItem('adminAuthToken')
		if (existingToken) {
			this.successMessage = 'Ya tienes una sesión activa.'
			this.redirectAfterSuccess()
		}

	},

	methods: {

		fieldErrors(field) {
			return this.errors[field] || []
		},

		resetState() {
			this.errors = {}
			this.generalError = ''
			this.successMessage = ''
		},

		persistSession(token) {
			window.localStorage.setItem('adminAuthToken', token)
		},

		redirectAfterSuccess() {
			const redirect = this.$route.query.redirect
			if (redirect) {
				this.$router.replace(redirect)
			} else {
				this.$router.replace({ name: 'admin-dashboard' })
			}
		},
		
		async submitForm() {
			this.resetState()
			this.isSubmitting = true

			try {
				const response = await apiRequest('/admin/login/', {
					method: 'POST',
					body: {
						email: this.form.email,
						password: this.form.password,
					},
				})

				const token = response && response.data && response.data.token
				if (token) {
					this.persistSession(token)
				}

				this.successMessage = response && response.message
					? response.message
					: 'Inicio de sesión exitoso.'

				this.form.password = ''
				this.redirectAfterSuccess()
			} 
			
			catch (error) {
				this.generalError = error && error.data && error.data.message
					? error.data.message
					: error.message || 'No pudimos iniciar sesión con las credenciales ingresadas.'

				if (error && error.data && error.data.errors && typeof error.data.errors === 'object') {
					Object.entries(error.data.errors).forEach(([field, details]) => {
						this.errors[field] = Array.isArray(details) ? details : [String(details)]
					})
				}
			} 
			
			finally {
				this.isSubmitting = false
			}
			
		},
	},
}
</script>
