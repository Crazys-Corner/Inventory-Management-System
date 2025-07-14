<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600 p-4">
    <div class="bg-white rounded-xl shadow-2xl p-8 w-full max-w-md relative">
      <!-- Header -->
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-gray-800 mb-2">Welcome Back</h2>
        <p class="text-gray-600 text-sm">Please sign in to your account</p>
      </div>
      
      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="space-y-6">
        <!-- Email Field -->
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
            Email
          </label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="Enter your email"
            :class="[
              'w-full px-4 py-3 border rounded-lg text-sm transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
              errors.email ? 'border-red-500 bg-red-50' : 'border-gray-300 hover:border-gray-400'
            ]"
            required
          />
          <p v-if="errors.email" class="text-red-500 text-xs mt-1">
            {{ errors.email }}
          </p>
        </div>

        <!-- Password Field -->
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
            Password
          </label>
          <div class="relative">
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Enter your password"
              :class="[
                'w-full px-4 py-3 pr-12 border rounded-lg text-sm transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                errors.password ? 'border-red-500 bg-red-50' : 'border-gray-300 hover:border-gray-400'
              ]"
              required
            />
            <button
              type="button"
              @click="togglePassword"
              class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 transition-colors"
            >
              <span v-if="showPassword" class="text-lg">👁️</span>
              <span v-else class="text-lg">👁️‍🗨️</span>
            </button>
          </div>
          <p v-if="errors.password" class="text-red-500 text-xs mt-1">
            {{ errors.password }}
          </p>
        </div>

        <!-- Form Options -->
        <div class="flex items-center justify-between">
          <label class="flex items-center">
            <input
              v-model="form.rememberMe"
              type="checkbox"
              class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <span class="ml-2 text-sm text-gray-600">Remember me</span>
          </label>
          <a href="#" class="text-sm text-blue-600 hover:text-blue-800 hover:underline">
            Forgot password?
          </a>
        </div>

        <!-- Login Button -->
        <button
          type="submit"
          :disabled="isLoading"
          class="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 px-4 rounded-lg font-medium text-sm transition-all duration-200 transform hover:scale-105 hover:shadow-lg disabled:opacity-70 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center"
        >
          <svg
            v-if="isLoading"
            class="animate-spin -ml-1 mr-3 h-4 w-4 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          {{ isLoading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>

      <!-- Footer -->
      <div class="text-center mt-8">
        <p class="text-sm text-gray-600">
          Don't have an account?
          <a href="#" class="text-blue-600 hover:text-blue-800 hover:underline font-medium">
            Sign up
          </a>
        </p>
      </div>

      <!-- Success/Error Messages -->
      <div
        v-if="message"
        :class="[
          'absolute -bottom-16 left-0 right-0 mx-4 p-4 rounded-lg text-sm font-medium',
          messageType === 'success' 
            ? 'bg-green-100 border border-green-300 text-green-800' 
            : 'bg-red-100 border border-red-300 text-red-800'
        ]"
      >
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      form: {
        email: '',
        password: '',
        rememberMe: false
      },
      errors: {},
      isLoading: false,
      showPassword: false,
      message: '',
      messageType: 'success' // 'success' or 'error'
    }
  },
  methods: {
    validateForm() {
      this.errors = {}
      
      if (!this.form.email) {
        this.errors.email = 'Email is required'
      } else if (!this.isValidEmail(this.form.email)) {
        this.errors.email = 'Please enter a valid email'
      }
      
      if (!this.form.password) {
        this.errors.password = 'Password is required'
      } else if (this.form.password.length < 6) {
        this.errors.password = 'Password must be at least 6 characters'
      }
      
      return Object.keys(this.errors).length === 0
    },
    
    isValidEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      return emailRegex.test(email)
    },
    
    async handleLogin() {
      if (!this.validateForm()) {
        return
      }
      
      this.isLoading = true
      this.message = ''
      
      try {
        // Simulate API call
        await this.loginAPI(this.form)
        
        this.message = 'Login successful! Redirecting...'
        this.messageType = 'success'
        
        // Simulate redirect after successful login
        setTimeout(() => {
          // Replace with actual router navigation
          console.log('Redirecting to dashboard...')
          // this.$router.push('/dashboard')
        }, 1500)
        
      } catch (error) {
        this.message = error.message || 'Login failed. Please try again.'
        this.messageType = 'error'
      } finally {
        this.isLoading = false
      }
    },
    
    async loginAPI(credentials) {
      // Simulate API call
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          // Simulate successful login for demo purposes
          if (credentials.email === 'demo@example.com' && credentials.password === 'password123') {
            resolve({ success: true, token: 'fake-jwt-token' })
          } else {
            reject(new Error('Invalid email or password'))
          }
        }, 1000)
      })
    },
    
    togglePassword() {
      this.showPassword = !this.showPassword
    }
  }
}
</script>