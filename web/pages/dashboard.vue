<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-gray-900">Inventory Dashboard</h1>
            <div class="ml-4 px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
              {{ totalItems }} Items
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="refreshData"
              :disabled="isLoading"
              class="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
              Refresh
            </button>
            <button 
              @click="showAddModal = true"
              class="flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
              </svg>
              Add Item
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-2 bg-blue-100 rounded-lg">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Total Items</p>
              <p class="text-2xl font-bold text-gray-900">{{ totalItems }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-2 bg-green-100 rounded-lg">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">In Use</p>
              <p class="text-2xl font-bold text-gray-900">{{ inUseCount }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-2 bg-yellow-100 rounded-lg">
              <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Available</p>
              <p class="text-2xl font-bold text-gray-900">{{ availableCount }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-2 bg-purple-100 rounded-lg">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Total Value</p>
              <p class="text-2xl font-bold text-gray-900">${{ totalValue.toLocaleString() }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters and Search -->
      <div class="bg-white rounded-lg shadow mb-6">
        <div class="p-6 border-b">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
            <div class="flex items-center space-x-4">
              <!-- Search -->
              <div class="relative">
                <input
                  v-model="searchTerm"
                  type="text"
                  placeholder="Search items..."
                  class="w-64 pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <svg class="absolute left-3 top-2.5 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
              </div>
              
              <!-- Status Filter -->
              <select
                v-model="statusFilter"
                class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Status</option>
                <option value="true">In Use</option>
                <option value="false">Available</option>
              </select>
              
              <!-- Client Filter -->
              <select
                v-model="clientFilter"
                class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Clients</option>
                <option v-for="client in uniqueClients" :key="client" :value="client">
                  {{ client }}
                </option>
              </select>
            </div>
            
            <div class="flex items-center space-x-2">
              <span class="text-sm text-gray-500">Sort by:</span>
              <select
                v-model="sortBy"
                class="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="name">Name</option>
                <option value="value">Value</option>
                <option value="client">Client</option>
                <option value="id">ID</option>
              </select>
              <button
                @click="toggleSortOrder"
                class="p-2 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="sortOrder === 'asc' ? 'M3 4l9 16 9-16' : 'M3 20l9-16 9 16'"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Items Table -->
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Item
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Value
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Client
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="isLoading" class="animate-pulse">
                <td colspan="5" class="px-6 py-4 text-center text-gray-500">
                  Loading items...
                </td>
              </tr>
              <tr v-else-if="filteredItems.length === 0">
                <td colspan="5" class="px-6 py-4 text-center text-gray-500">
                  No items found
                </td>
              </tr>
              <tr v-else v-for="item in filteredItems" :key="item.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div>
                      <div class="text-sm font-medium text-gray-900">{{ item.name }}</div>
                      <div class="text-sm text-gray-500">ID: {{ item.id }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">${{ item.value.toLocaleString() }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="[
                    'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                    item.isInUse 
                      ? 'bg-red-100 text-red-800' 
                      : 'bg-green-100 text-green-800'
                  ]">
                    {{ item.isInUse ? 'In Use' : 'Available' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{{ item.client }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button
                    @click="toggleItemStatus(item)"
                    :class="[
                      'mr-2 px-3 py-1 rounded text-xs font-medium',
                      item.isInUse
                        ? 'bg-green-100 text-green-800 hover:bg-green-200'
                        : 'bg-red-100 text-red-800 hover:bg-red-200'
                    ]"
                  >
                    {{ item.isInUse ? 'Mark Available' : 'Mark In Use' }}
                  </button>
                  <button class="text-blue-600 hover:text-blue-800 mr-2">Edit</button>
                  <button class="text-red-600 hover:text-red-800">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>

    <!-- Add Item Modal -->
    <div v-if="showAddModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <!-- Modal Header -->
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-medium text-gray-900">Add New Item</h3>
            <button 
              @click="closeAddModal"
              class="text-gray-400 hover:text-gray-600"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <!-- Add Item Form -->
          <form @submit.prevent="addItem" class="space-y-4">
            <!-- Item Name -->
            <div>
              <label for="itemName" class="block text-sm font-medium text-gray-700 mb-1">
                Item Name *
              </label>
              <input
                id="itemName"
                v-model="newItem.name"
                type="text"
                required
                placeholder="Enter item name"
                :class="[
                  'w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                  formErrors.name ? 'border-red-500 bg-red-50' : 'border-gray-300'
                ]"
              />
              <p v-if="formErrors.name" class="text-red-500 text-xs mt-1">
                {{ formErrors.name }}
              </p>
            </div>

            <!-- Item Value -->
            <div>
              <label for="itemValue" class="block text-sm font-medium text-gray-700 mb-1">
                Value ($) *
              </label>
              <input
                id="itemValue"
                v-model.number="newItem.value"
                type="number"
                step="0.01"
                min="0"
                required
                placeholder="0.00"
                :class="[
                  'w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                  formErrors.value ? 'border-red-500 bg-red-50' : 'border-gray-300'
                ]"
              />
              <p v-if="formErrors.value" class="text-red-500 text-xs mt-1">
                {{ formErrors.value }}
              </p>
            </div>

            <!-- Client -->
            <div>
              <label for="itemClient" class="block text-sm font-medium text-gray-700 mb-1">
                Client *
              </label>
              <input
                id="itemClient"
                v-model="newItem.client"
                type="text"
                required
                placeholder="Enter client name"
                list="clientSuggestions"
                :class="[
                  'w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                  formErrors.client ? 'border-red-500 bg-red-50' : 'border-gray-300'
                ]"
              />
              <datalist id="clientSuggestions">
                <option v-for="client in uniqueClients" :key="client" :value="client" />
              </datalist>
              <p v-if="formErrors.client" class="text-red-500 text-xs mt-1">
                {{ formErrors.client }}
              </p>
            </div>

            <!-- Status -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Initial Status
              </label>
              <div class="flex space-x-4">
                <label class="flex items-center">
                  <input
                    v-model="newItem.isInUse"
                    type="radio"
                    :value="false"
                    class="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                  />
                  <span class="ml-2 text-sm text-gray-700">Available</span>
                </label>
                <label class="flex items-center">
                  <input
                    v-model="newItem.isInUse"
                    type="radio"
                    :value="true"
                    class="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                  />
                  <span class="ml-2 text-sm text-gray-700">In Use</span>
                </label>
              </div>
            </div>

            <!-- Form Actions -->
            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeAddModal"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="isSubmitting"
                class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              >
                <svg
                  v-if="isSubmitting"
                  class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ isSubmitting ? 'Adding...' : 'Add Item' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InventoryDashboard',
  data() {
    return {
      items: [],
      isLoading: false,
      searchTerm: '',
      statusFilter: '',
      clientFilter: '',
      sortBy: 'name',
      sortOrder: 'asc',
      showAddModal: false,
      isSubmitting: false,
      newItem: {
        name: '',
        value: 0,
        client: '',
        isInUse: false
      },
      formErrors: {}
    }
  },
  computed: {
    totalItems() {
      return this.items.length
    },
    inUseCount() {
      return this.items.filter(item => item.isInUse).length
    },
    availableCount() {
      return this.items.filter(item => !item.isInUse).length
    },
    totalValue() {
      return this.items.reduce((sum, item) => sum + item.value, 0)
    },
    uniqueClients() {
      return [...new Set(this.items.map(item => item.client))].sort()
    },
    filteredItems() {
      let filtered = this.items

      // Search filter
      if (this.searchTerm) {
        filtered = filtered.filter(item =>
          item.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          item.client.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          item.id.toString().includes(this.searchTerm)
        )
      }

      // Status filter
      if (this.statusFilter !== '') {
        filtered = filtered.filter(item => item.isInUse === (this.statusFilter === 'true'))
      }

      // Client filter
      if (this.clientFilter) {
        filtered = filtered.filter(item => item.client === this.clientFilter)
      }

      // Sort
      filtered.sort((a, b) => {
        let aValue = a[this.sortBy]
        let bValue = b[this.sortBy]
        
        if (typeof aValue === 'string') {
          aValue = aValue.toLowerCase()
          bValue = bValue.toLowerCase()
        }
        
        if (this.sortOrder === 'asc') {
          return aValue < bValue ? -1 : aValue > bValue ? 1 : 0
        } else {
          return aValue > bValue ? -1 : aValue < bValue ? 1 : 0
        }
      })

      return filtered
    }
  },
  methods: {
    async fetchItems() {
      this.isLoading = true
      try {
        // Simulate API call
        await this.delay(1000)
        
        // Mock data based on your Item class
        this.items = await $fetch("http://localhost:8000/inventory/items", {
            method: "GET"
        }
        )

      } catch (error) {
        console.error('Error fetching items:', error)
      } finally {
        this.isLoading = false
      }
    },
    
    async refreshData() {
      await this.fetchItems()
    },
    
    toggleSortOrder() {
      this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc'
    },
    
    async toggleItemStatus(item) {
      // Simulate API call to update item status
      item.isInUse = !item.isInUse
      // In real app, you would make an API call here
      console.log(`Item ${item.name} status changed to ${item.isInUse ? 'In Use' : 'Available'}`)
    },
    
    delay(ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    },

    closeAddModal() {
      this.showAddModal = false
      this.resetForm()
    },

    resetForm() {
      this.newItem = {
        name: '',
        value: 0,
        client: '',
        isInUse: false
      }
      this.formErrors = {}
    },

    validateForm() {
      this.formErrors = {}

      if (!this.newItem.name.trim()) {
        this.formErrors.name = 'Item name is required'
      }

      if (!this.newItem.value || this.newItem.value <= 0) {
        this.formErrors.value = 'Value must be greater than 0'
      }

      if (!this.newItem.client.trim()) {
        this.formErrors.client = 'Client is required'
      }

      return Object.keys(this.formErrors).length === 0
    },

    async addItem() {
      if (!this.validateForm()) {
        return
      }

      this.isSubmitting = true

      try {
        // Generate a new ID (in real app, this would be handled by the backend)

        
        const itemToAdd = {
          name: this.newItem.name.trim(),
          value: parseFloat(this.newItem.value),
          client: this.newItem.client.trim(),
          isInUse: this.newItem.isInUse
        }

      
        const response = await $fetch("http://localhost:8000/inventory/items", {
          method: "POST",
          body: itemToAdd
        })

        // Add the new item to the local array
        this.items.push(response)
        
        // Close modal and reset form
        this.closeAddModal()
        
        console.log('Item added successfully:', response)
        
      } catch (error) {
        console.error('Error adding item:', error)
        // You could show an error message to the user here
      } finally {
        this.isSubmitting = false
      }
    }
  },
  
  mounted() {
    this.fetchItems()
  }
}
</script>