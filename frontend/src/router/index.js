import { createRouter, createWebHistory } from 'vue-router'

// Auth validation
const isAdminAuthenticated = () => {
	if (typeof window === 'undefined') {
		return false
	}

	return Boolean(window.localStorage.getItem('adminAuthToken'))
}

// Routes
const router = createRouter({

	history: createWebHistory(import.meta.env.BASE_URL),

	routes: [

		// Public
		{
			path: '/',
			redirect: { name: 'register' },
		},
		{
			path: '/register',
			name: 'register',
			component: () => import('../views/Register.vue'),
			meta: { requiresAuth: false },
		},
		{
			path: '/email-verification',
			name: 'email-verification',
			component: () => import('../views/EmailVerification.vue'),
			meta: { requiresAuth: false },
		},
		{
			path: '/admin/login',
			name: 'admin-login',
			component: () => import('../views/admin/Login.vue'),
			meta: { requiresAuth: false },
		},

		// Protected by authentication
		{
			path: '/admin/participants',
			name: 'admin-participant-list',
			component: () => import('../views/admin/ParticipantList.vue'),
			meta: { requiresAuth: true },
		},
		{
			path: '/admin/dashboard',
			name: 'admin-dashboard',
			component: () => import('../views/admin/Dashboard.vue'),
			meta: { requiresAuth: true },
		},

	],
	 
})

// Router guard
router.beforeEach((to, from, next) => {
	
	const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
	const isAuthenticated = isAdminAuthenticated()

	// Protected routes validation
	if (requiresAuth && !isAuthenticated) {
		return next({
			name: 'admin-login',
			query: { redirect: to.fullPath },
		})
	}

	// If already authenticated
	if (to.name === 'admin-login' && isAuthenticated) {
		const redirect = typeof to.query.redirect === 'string' ? to.query.redirect : null
		return next(redirect || { name: 'admin-dashboard' })
	}

	// Allow navigation
	return next()

})

export default router
