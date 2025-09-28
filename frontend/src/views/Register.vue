<template>
	<section class="mx-auto max-w-3xl rounded-2xl bg-white/80 p-8 shadow-xl backdrop-blur space-y-10">

		<!-- Header -->
		<header class="text-center space-y-3">
			<span class="flex items-center justify-center text-pink-600">
				<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 16 16"><g fill="currentColor"><path d="M8 5.993c1.664-1.711 5.825 1.283 0 5.132c-5.825-3.85-1.664-6.843 0-5.132M2.25 4a.25.25 0 0 0-.25.25v1.5a.25.25 0 0 0 .5 0V4.5h1.25a.25.25 0 0 0 0-.5zm10 0a.25.25 0 1 0 0 .5h1.25v1.25a.25.25 0 1 0 .5 0v-1.5a.25.25 0 0 0-.25-.25zM2.5 10.25a.25.25 0 1 0-.5 0v1.5c0 .138.112.25.25.25h1.5a.25.25 0 1 0 0-.5H2.5zm11.5 0a.25.25 0 1 0-.5 0v1.25h-1.25a.25.25 0 1 0 0 .5h1.5a.25.25 0 0 0 .25-.25z"/><path fill-rule="evenodd" d="M0 2.994v-.06a1 1 0 0 1 .859-.99l13-1.857a1 1 0 0 1 1.141.99V2a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zM1 3v10h14V3z"/></g></svg>
			</span>
			<h1 class="text-3xl font-semibold text-slate-900">Inscripción al sorteo de San Valentín</h1>
			<p class="mt-2 text-sm text-slate-600">
				Completa tus datos para participar por una estadía de dos noches con todo pagado para ti y tu pareja. Te enviaremos un correo para validar tu
				cuenta.
			</p>
		</header>

		<!-- Error message -->
		<div v-if="generalError" class="mb-6 rounded-xl border border-rose-200 bg-rose-50/90 p-4 text-rose-700">
			{{ generalError }}
		</div>

		<!-- user data form -->
		<form v-if="!successMessage" class="space-y-6" @submit.prevent="handleSubmit">
			<div class="grid gap-6 md:grid-cols-2">

				<!-- Name -->
				<div>
					<label for="first-name" class="mb-1 block text-sm font-medium text-slate-700">Nombre</label>
					<input id="first-name" v-model.trim="form.firstName" type="text"
						class="w-full rounded-lg border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-rose-400 focus:ring-2 focus:ring-rose-200"
						:class="{ 'border-rose-400 focus:ring-rose-300': fieldErrors('first_name') }"
						placeholder="Ingresa tu nombre" autocomplete="given-name" required />
					<p v-if="fieldErrors('first_name')" class="mt-2 text-sm text-rose-600">
						{{ fieldErrors('first_name')?.join(' ') }}
					</p>
				</div>

				<!-- Last name -->
				<div>
					<label for="last-name" class="mb-1 block text-sm font-medium text-slate-700">Apellido</label>
					<input id="last-name" v-model.trim="form.lastName" type="text"
						class="w-full rounded-lg border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-rose-400 focus:ring-2 focus:ring-rose-200"
						:class="{ 'border-rose-400 focus:ring-rose-300': fieldErrors('last_name') }"
						placeholder="Ingresa tu apellido" autocomplete="family-name" required />
					<p v-if="fieldErrors('last_name')" class="mt-2 text-sm text-rose-600">
						{{ fieldErrors('last_name')?.join(' ') }}
					</p>
				</div>
			</div>

			<!-- Email -->
			<div class="grid gap-6 md:grid-cols-2">
				<div class="md:col-span-2">
					<label for="email" class="mb-1 block text-sm font-medium text-slate-700">Correo electrónico</label>
					<input id="email" v-model.trim="form.email" type="email"
						class="w-full rounded-lg border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-rose-400 focus:ring-2 focus:ring-rose-200"
						:class="{ 'border-rose-400 focus:ring-rose-300': fieldErrors('email') }"
						placeholder="nombre@correo.com" autocomplete="email" required />
					<p v-if="fieldErrors('email')" class="mt-2 text-sm text-rose-600">
						{{ fieldErrors('email')?.join(' ') }}
					</p>
				</div>
			</div>

			<!-- RUT + Phone -->
			<div class="grid gap-6 md:grid-cols-2">

				<!-- Rut -->
				<div>
					<label for="rut" class="mb-1 block text-sm font-medium text-slate-700">RUT</label>
					<input id="rut" v-model.trim="form.rut" type="text"
						class="w-full rounded-lg border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-rose-400 focus:ring-2 focus:ring-rose-200"
						:class="{ 'border-rose-400 focus:ring-rose-300': fieldErrors('rut') }" placeholder="12345678-9"
						required />
					<p v-if="fieldErrors('rut')" class="mt-2 text-sm text-rose-600">
						{{ fieldErrors('rut')?.join(' ') }}
					</p>
				</div>

				<!-- Phone -->
				<div>
					<label for="phone" class="mb-1 block text-sm font-medium text-slate-700">Teléfono</label>
					<input id="phone" v-model.trim="form.phone" type="tel"
						class="w-full rounded-lg border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-rose-400 focus:ring-2 focus:ring-rose-200"
						:class="{ 'border-rose-400 focus:ring-rose-300': fieldErrors('phone') }"
						placeholder="+56 9 1234 5678" required />
					<p v-if="fieldErrors('phone')" class="mt-2 text-sm text-rose-600">
						{{ fieldErrors('phone')?.join(' ') }}
					</p>
				</div>
			</div>

			<!-- Address -->
			<div>
				<label for="address" class="mb-1 block text-sm font-medium text-slate-700">Dirección</label>
				<textarea id="address" v-model.trim="form.address" rows="3"
					class="w-full rounded-lg border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-rose-400 focus:ring-2 focus:ring-rose-200"
					:class="{ 'border-rose-400 focus:ring-rose-300': fieldErrors('address') }"
					placeholder="Calle, número, ciudad" required></textarea>
				<p v-if="fieldErrors('address')" class="mt-2 text-sm text-rose-600">
					{{ fieldErrors('address')?.join(' ') }}
				</p>
			</div>

			<button type="submit"
				class="w-full items-center justify-center rounded-lg bg-gradient-to-r from-gray-900 to-blue-900 px-6 py-3 font-semibold text-white shadow-lg transition hover:from-gray-800 hover:to-blue-800 disabled:cursor-not-allowed disabled:opacity-60 cursor-pointer"
				:disabled="isSubmitting">
				<span v-if="!isSubmitting">Registrar participación</span>
				<span v-else>Registrando...</span>
			</button>

		</form>

		<!-- Success message -->
		<div v-if="successMessage"
			class="mb-8 rounded-xl border border-emerald-200 bg-emerald-50/80 p-6 text-emerald-700">
			<h2 class="text-lg font-semibold">¡Solo un paso más!</h2>
			<p class="mt-2">{{ successMessage }}</p>
		</div>

	</section>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { apiRequest } from '@/utils/apiClient'

const form = reactive({
	firstName: '',
	lastName: '',
	email: '',
	rut: '',
	phone: '',
	address: '',
})

const errors = reactive({})
const generalError = ref('')
const successMessage = ref('')
const registeredParticipant = ref(null)
const isSubmitting = ref(false)

const resetErrors = () => {
	Object.keys(errors).forEach((key) => {
		delete errors[key]
	})
	generalError.value = ''
}

const fieldErrors = (field) => errors[field] || null

const handleSubmit = async () => {
	resetErrors()
	isSubmitting.value = true

	try {
		const response = await apiRequest('/participants/register/', {
			method: 'POST',
			body: {
				first_name: form.firstName,
				last_name: form.lastName,
				email: form.email,
				rut: form.rut,
				phone: form.phone,
				address: form.address,
			},
		})

		successMessage.value = response?.message ?? '¡Gracias por registrarte! Revisa tu correo para verificar tu cuenta.'
		registeredParticipant.value = response?.data ?? null

		form.firstName = ''
		form.lastName = ''
		form.email = ''
		form.rut = ''
		form.phone = ''
		form.address = ''
	} catch (error) {
		generalError.value = error?.data?.message || error.message || 'No pudimos completar el registro.'

		if (error?.data?.errors && typeof error.data.errors === 'object') {
			Object.entries(error.data.errors).forEach(([field, details]) => {
				errors[field] = Array.isArray(details) ? details : [String(details)]
			})
		}
	} finally {
		isSubmitting.value = false
	}
}
</script>
