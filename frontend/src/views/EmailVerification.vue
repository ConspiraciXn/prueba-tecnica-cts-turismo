<template>
	<section class="mx-auto mt-6 max-w-xl rounded-2xl bg-white/80 p-8 shadow-xl backdrop-blur">

		<!-- Header -->
		<header class="mb-6 text-center">
			<h1 class="text-2xl font-semibold text-slate-900">Verificación de correo</h1>
			<p class="mt-2 text-sm text-slate-600">
				Crea tu contraseña para activar la cuenta y confirmar tu participación.
			</p>
		</header>

		<!-- Error message -->
		<div v-if="generalError" class="mb-6 rounded-xl border border-rose-200 bg-rose-50/90 p-4 text-rose-700">
			{{ generalError }}
		</div>

		<!-- Validating status -->
		<div v-if="isValidating" class="mb-6 rounded-xl border border-slate-200 bg-slate-50/80 p-4 text-slate-600">
			Validando enlace de verificación...
		</div>

		<!-- Success message -->
		<div v-if="successMessage"
			class="mb-6 rounded-xl border border-emerald-200 bg-emerald-50/80 p-5 text-emerald-700">
			<h2 class="text-lg font-semibold">¡Cuenta activada!</h2>
			<p class="mt-2">{{ successMessage }}</p>
		</div>

		<!-- Password message -->
		<form v-if="linkValid && !successMessage" class="space-y-5" @submit.prevent="submitForm">
			<div>
				<label for="password" class="mb-1 block text-sm font-medium text-slate-700">Contraseña</label>
				<input id="password" v-model="form.password" type="password"
					class="w-full rounded-lg border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-rose-400 focus:ring-2 focus:ring-rose-200"
					:class="{ 'border-rose-400 focus:ring-rose-300': fieldErrors('password').length }"
					placeholder="Ingresa una contraseña segura" required minlength="8" />
				<p v-if="fieldErrors('password').length" class="mt-2 text-sm text-rose-600">
					{{ fieldErrors('password').join(' ') }}
				</p>
			</div>

			<div>
				<label for="confirm-password" class="mb-1 block text-sm font-medium text-slate-700">Confirmar
					contraseña</label>
				<input id="confirm-password" v-model="form.confirmPassword" type="password"
					class="w-full rounded-lg border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-rose-400 focus:ring-2 focus:ring-rose-200"
					:class="{ 'border-rose-400 focus:ring-rose-300': fieldErrors('confirm_password').length }"
					placeholder="Repite la contraseña" required minlength="8" />
				<p v-if="fieldErrors('confirm_password').length" class="mt-2 text-sm text-rose-600">
					{{ fieldErrors('confirm_password').join(' ') }}
				</p>
			</div>

			<button type="submit"
				class="inline-flex w-full items-center justify-center rounded-lg bg-gradient-to-r from-gray-900 to-blue-900 px-6 py-3 text-base font-semibold text-white shadow-lg transition hover:from-gray-800 hover:to-blue-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-rose-200 disabled:cursor-not-allowed disabled:opacity-60"
				:disabled="isSubmitting || !linkValid || isValidating">
				<span v-if="!isSubmitting">Activar cuenta</span>
				<span v-else>Activando...</span>
			</button>
		</form>

	</section>
</template>

<script>
import { apiRequest } from '@/utils/apiClient'

export default {

	name: 'EmailVerification',

	data() {
		return {
			form: {
				password: '',
				confirmPassword: '',
			},
			isSubmitting: false,
			isValidating: false,
			linkValid: false,
			generalError: '',
			successMessage: '',
			errors: {},
		}
	},

	computed: {
		uid() {
			return this.$route.query.uid || ''
		},
		token() {
			return this.$route.query.token || ''
		},
		hasTokens() {
			return Boolean(this.uid && this.token)
		},
	},

	watch: {
		'$route.query': 'validateLink',
	},

	created() {
		this.validateLink()
	},

	methods: {

		fieldErrors(field) {
			return this.errors[field] || []
		},

		resetErrors() {
			this.errors = {}
		},

		async validateLink() {
			this.linkValid = false
			this.resetErrors()

			if (!this.hasTokens) {
				this.generalError = 'El enlace de verificación no es válido o ha expirado.'
				return
			}

			this.generalError = ''
			this.isValidating = true

			try {
				await apiRequest('/participants/verify-email/validate/', {
					method: 'POST',
					body: {
						uid: this.uid,
						token: this.token,
					},
				})

				this.linkValid = true

			} catch (error) {
				this.generalError = error && error.data && error.data.message
					? error.data.message
					: error && error.message
						? error.message
						: 'El enlace de verificación no es válido o ha expirado.'

				if (error && error.data && error.data.errors && typeof error.data.errors === 'object') {
					Object.entries(error.data.errors).forEach(([field, details]) => {
						this.errors[field] = Array.isArray(details) ? details : [String(details)]
					})
				}
			} finally {
				this.isValidating = false
			}
		},

		async submitForm() {
			if (!this.linkValid || !this.hasTokens) {
				this.generalError = 'El enlace de verificación no es válido o ha expirado.'
				return
			}

			this.resetErrors()
			this.generalError = ''
			this.isSubmitting = true

			try {
				const response = await apiRequest('/participants/verify-email/', {
					method: 'POST',
					body: {
						uid: this.uid,
						token: this.token,
						password: this.form.password,
						confirm_password: this.form.confirmPassword,
					},
				})

				this.successMessage = response && response.message
					? response.message
					: 'Tu cuenta ha sido activada. Ya estás participando en el sorteo.'
				this.form.password = ''
				this.form.confirmPassword = ''
			} catch (error) {
				this.generalError = error && error.data && error.data.message
					? error.data.message
					: error && error.message
						? error.message
						: 'No pudimos activar tu cuenta.'

				if (error && error.data && error.data.errors && typeof error.data.errors === 'object') {
					Object.entries(error.data.errors).forEach(([field, details]) => {
						this.errors[field] = Array.isArray(details) ? details : [String(details)]
					})
				}
			} finally {
				this.isSubmitting = false
			}
		},
		
	},
}
</script>
