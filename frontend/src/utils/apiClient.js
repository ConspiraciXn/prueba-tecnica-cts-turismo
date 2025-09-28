const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api'

/**
* Builds a complete URL for the API endpoint.
*/
const buildUrl = (endpoint) => {
	if (endpoint.startsWith('http://') || endpoint.startsWith('https://')) {
		return endpoint
	}
	return `${API_BASE_URL.replace(/\/$/, '')}/${endpoint.replace(/^\//, '')}`
}

/**
* Performs an API request with the given endpoint and options using fetch.
*/
export const apiRequest = async (endpoint, { method = 'GET', headers = {}, body, ...rest } = {}) => {
	
	const response = await fetch(buildUrl(endpoint), {
		method,
		headers: {
			'Content-Type': 'application/json',
			...headers,
		},
		body: body !== undefined ? JSON.stringify(body) : undefined,
		...rest,
	})

	const contentType = response.headers.get('content-type') ?? ''
	const isJson = contentType.includes('application/json')
	const payload = isJson ? await response.json() : null

	if (!response.ok) {
		const error = new Error(payload?.message || 'Ha ocurrido un error inesperado.')
		error.status = response.status
		error.data = payload
		throw error
	}

	return payload
}
