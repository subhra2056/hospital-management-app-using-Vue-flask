<template>
  <div class="department-management">
    <div class="header-section">
      <h2 class="page-title">Department Management</h2>
      <p class="page-subtitle">Manage hospital departments and specializations</p>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else class="content-section">
      <!-- Add Department Form -->
      <div class="card mb-4">
        <div class="card-header">
          <h5 class="card-title mb-0">Add New Department</h5>
        </div>
        <div class="card-body">
          <form @submit.prevent="addDepartment" class="row g-3">
            <div class="col-md-5">
              <label for="departmentName" class="form-label">Department Name</label>
              <input
                type="text"
                class="form-control"
                id="departmentName"
                v-model="newDepartment.name"
                required
                placeholder="Enter department name"
              />
            </div>
            <div class="col-md-5">
              <label for="departmentDescription" class="form-label">Description</label>
              <input
                type="text"
                class="form-control"
                id="departmentDescription"
                v-model="newDepartment.description"
                required
                placeholder="Enter department description"
              />
            </div>
            <div class="col-md-2 d-flex align-items-end">
              <button type="submit" class="btn btn-primary w-100" :disabled="addingDepartment">
                <span v-if="addingDepartment" class="spinner-border spinner-border-sm me-2" role="status"></span>
                {{ addingDepartment ? 'Adding...' : 'Add Department' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Departments List -->
      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">Departments ({{ departments.length }})</h5>
          <button class="btn btn-outline-primary btn-sm" @click="loadDepartments">
            <svg class="me-1" width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
            Refresh
          </button>
        </div>
        <div class="card-body">
          <div v-if="departments.length === 0" class="text-center py-5">
            <svg width="64" height="64" fill="none" stroke="currentColor" viewBox="0 0 24 24" class="text-muted mb-3">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
            </svg>
            <h5 class="text-muted">No departments found</h5>
            <p class="text-muted">Add your first department using the form above.</p>
          </div>

          <div v-else class="departments-grid">
            <div
              v-for="department in departments"
              :key="department.id"
              class="department-card"
            >
              <div class="department-header">
                <h6 class="department-name">{{ department.name }}</h6>
                <div class="department-actions">
                  <button
                    class="btn btn-outline-danger btn-sm"
                    @click="deleteDepartment(department.id)"
                    :disabled="deletingDepartment === department.id"
                  >
                    <span v-if="deletingDepartment === department.id" class="spinner-border spinner-border-sm me-1" role="status"></span>
                    <svg v-else width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </button>
                </div>
              </div>
              <p class="department-description">{{ department.description }}</p>
              <div class="department-stats">
                <small class="text-muted">
                  <svg class="me-1" width="12" height="12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                  </svg>
                  {{ department.doctors_registered || 0 }} doctors registered
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import auth from '../../utils/auth'

const departments = ref([])
const loading = ref(true)
const addingDepartment = ref(false)
const deletingDepartment = ref(null)

const newDepartment = ref({
  name: '',
  description: ''
})

const loadDepartments = async () => {
  loading.value = true
  try {
    const token = auth.getToken()
    const response = await fetch('http://localhost:5000/api/admin/departments', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      const data = await response.json()
      departments.value = data.departments || []
    } else {
      console.error('Failed to load departments')
    }
  } catch (error) {
    console.error('Error loading departments:', error)
  } finally {
    loading.value = false
  }
}

const addDepartment = async () => {
  if (!newDepartment.value.name.trim() || !newDepartment.value.description.trim()) {
    return
  }

  addingDepartment.value = true
  try {
    const token = auth.getToken()
    const response = await fetch('http://localhost:5000/api/admin/departments', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newDepartment.value)
    })

    if (response.ok) {
      const data = await response.json()
      departments.value.push(data.department)
      newDepartment.value = { name: '', description: '' }
      alert('Department added successfully!')
    } else {
      const error = await response.json()
      alert(error.message || 'Failed to add department')
    }
  } catch (error) {
    console.error('Error adding department:', error)
    alert('Failed to add department')
  } finally {
    addingDepartment.value = false
  }
}

const deleteDepartment = async (departmentId) => {
  if (!confirm('Are you sure you want to delete this department? This action cannot be undone.')) {
    return
  }

  deletingDepartment.value = departmentId
  try {
    const token = auth.getToken()
    const response = await fetch(`http://localhost:5000/api/admin/departments/${departmentId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      departments.value = departments.value.filter(dept => dept.id !== departmentId)
      alert('Department deleted successfully!')
    } else {
      const error = await response.json()
      alert(error.message || 'Failed to delete department')
    }
  } catch (error) {
    console.error('Error deleting department:', error)
    alert('Failed to delete department')
  } finally {
    deletingDepartment.value = null
  }
}

onMounted(() => {
  loadDepartments()
})
</script>

<style scoped>
.department-management {
  padding: 0;
}

.header-section {
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  color: #64748b;
  font-size: 1rem;
  margin-bottom: 0;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.card-header {
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  border-radius: 12px 12px 0 0 !important;
  padding: 1.5rem;
}

.card-title {
  font-weight: 600;
  color: #1e293b;
}

.card-body {
  padding: 1.5rem;
}

.form-label {
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.form-control {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 0.75rem;
  font-size: 0.875rem;
}

.form-control:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.btn {
  border-radius: 8px;
  font-weight: 500;
  padding: 0.75rem 1.5rem;
  transition: all 0.2s;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  border: none;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn-outline-primary {
  border-color: #3b82f6;
  color: #3b82f6;
}

.btn-outline-primary:hover {
  background: #3b82f6;
  border-color: #3b82f6;
}

.btn-outline-danger {
  border-color: #ef4444;
  color: #ef4444;
}

.btn-outline-danger:hover {
  background: #ef4444;
  border-color: #ef4444;
}

.departments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.department-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.2s;
}

.department-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.department-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.department-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
  flex: 1;
}

.department-actions {
  opacity: 0;
  transition: opacity 0.2s;
}

.department-card:hover .department-actions {
  opacity: 1;
}

.department-description {
  color: #64748b;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.department-stats {
  padding-top: 0.75rem;
  border-top: 1px solid #f1f5f9;
}

@media (max-width: 768px) {
  .departments-grid {
    grid-template-columns: 1fr;
  }

  .department-header {
    flex-direction: column;
    gap: 0.75rem;
  }

  .department-actions {
    opacity: 1;
  }
}
</style>