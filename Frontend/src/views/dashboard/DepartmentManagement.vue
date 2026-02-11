<template>
  <div class="department-container">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
          </svg>
        </div>
        <div class="header-text">
          <h1>Department Management</h1>
          <p>Manage hospital departments and specializations</p>
        </div>
      </div>
      <div class="header-stats">
        <div class="stat-badge">
          <span class="stat-number">{{ departments.length }}</span>
          <span class="stat-label">Departments</span>
        </div>
      </div>
    </div>

    <!-- Add Department Form -->
    <div class="add-department-card">
      <div class="add-card-header">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
        </svg>
        <h3>Add New Department</h3>
      </div>
      <form @submit.prevent="addDepartment" class="add-form">
        <div class="form-group">
          <label for="departmentName">Department Name</label>
          <input
            type="text"
            id="departmentName"
            v-model="newDepartment.name"
            required
            placeholder="e.g., Cardiology"
          />
        </div>
        <div class="form-group">
          <label for="departmentDescription">Description</label>
          <input
            type="text"
            id="departmentDescription"
            v-model="newDepartment.description"
            required
            placeholder="e.g., Heart and cardiovascular system"
          />
        </div>
        <button type="submit" class="add-btn" :disabled="addingDepartment">
          <span v-if="addingDepartment" class="btn-loader"></span>
          <svg v-else fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
          </svg>
          {{ addingDepartment ? 'Adding...' : 'Add Department' }}
        </button>
      </form>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="loader"></div>
      <p>Loading departments...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="departments.length === 0" class="empty-state">
      <div class="empty-icon">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
        </svg>
      </div>
      <h3>No Departments Found</h3>
      <p>Add your first department using the form above</p>
    </div>

    <!-- Departments Grid -->
    <div v-else class="departments-section">
      <div class="section-header">
        <h2>All Departments</h2>
        <button class="refresh-btn" @click="loadDepartments">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          Refresh
        </button>
      </div>
      
      <div class="departments-grid">
        <div
          v-for="department in departments"
          :key="department.id"
          class="dept-card"
        >
          <div class="dept-accent"></div>
          <div class="dept-content">
            <div class="dept-header">
              <div class="dept-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                </svg>
              </div>
              <div class="dept-info">
                <h4 class="dept-name">{{ department.name }}</h4>
                <p class="dept-description">{{ department.description }}</p>
              </div>
            </div>
            
            <div class="dept-footer">
              <div class="dept-stat">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                </svg>
                <span>{{ department.doctors_registered || 0 }} doctors</span>
              </div>
              <button
                class="delete-btn"
                @click="deleteDepartment(department.id)"
                :disabled="deletingDepartment === department.id"
              >
                <span v-if="deletingDepartment === department.id" class="btn-loader-sm"></span>
                <svg v-else fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
              </button>
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
.department-container {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, #5e63b6 0%, #4a50a0 100%);
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(94, 99, 182, 0.3);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.header-icon {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
}

.header-icon svg {
  width: 32px;
  height: 32px;
  color: white;
}

.header-text h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: white;
  margin: 0;
}

.header-text p {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 0.25rem 0 0;
}

.header-stats {
  display: flex;
  gap: 1rem;
}

.stat-badge {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  padding: 1rem 1.5rem;
  border-radius: 16px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-number {
  display: block;
  font-size: 1.75rem;
  font-weight: 700;
  color: white;
}

.stat-label {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.8);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Add Department Card */
.add-department-card {
  background: white;
  border-radius: 20px;
  padding: 1.5rem 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.add-card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f1f5f9;
}

.add-card-header svg {
  width: 24px;
  height: 24px;
  color: #5e63b6;
}

.add-card-header h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.add-form {
  display: flex;
  gap: 1rem;
  align-items: flex-end;
  flex-wrap: wrap;
}

.form-group {
  flex: 1;
  min-width: 200px;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 0.95rem;
  color: #1e293b;
  background: #fafafa;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #5e63b6;
  background: white;
  box-shadow: 0 0 0 4px rgba(94, 99, 182, 0.1);
}

.form-group input::placeholder {
  color: #94a3b8;
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #5e63b6 0%, #4a50a0 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.add-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(94, 99, 182, 0.4);
}

.add-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.add-btn svg {
  width: 20px;
  height: 20px;
}

.btn-loader {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  color: #64748b;
}

.loader {
  width: 48px;
  height: 48px;
  border: 4px solid #e2e8f0;
  border-top-color: #5e63b6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  text-align: center;
}

.empty-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #e9d8fd 0%, #faf5ff 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.empty-icon svg {
  width: 40px;
  height: 40px;
  color: #5e63b6;
}

.empty-state h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem;
}

.empty-state p {
  color: #64748b;
  margin: 0;
}

/* Section Header */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #5e63b6;
  cursor: pointer;
  transition: all 0.3s ease;
}

.refresh-btn:hover {
  background: #5e63b6;
  border-color: #5e63b6;
  color: white;
}

.refresh-btn svg {
  width: 18px;
  height: 18px;
}

/* Departments Grid */
.departments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

/* Department Card */
.dept-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.dept-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(94, 99, 182, 0.2);
}

.dept-accent {
  height: 6px;
  background: linear-gradient(90deg, #5e63b6 0%, #7c3aed 50%, #5e63b6 100%);
  background-size: 200% 100%;
  animation: shimmer 3s ease infinite;
}

@keyframes shimmer {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.dept-content {
  padding: 1.5rem;
}

.dept-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.dept-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #e9d8fd 0%, #faf5ff 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.dept-icon svg {
  width: 26px;
  height: 26px;
  color: #5e63b6;
}

.dept-info {
  flex: 1;
  min-width: 0;
}

.dept-name {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.375rem;
}

.dept-description {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.dept-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;
}

.dept-stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.dept-stat svg {
  width: 18px;
  height: 18px;
  color: #5e63b6;
}

.delete-btn {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fef2f2;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.delete-btn:hover:not(:disabled) {
  background: #ef4444;
}

.delete-btn svg {
  width: 18px;
  height: 18px;
  color: #ef4444;
  transition: color 0.3s ease;
}

.delete-btn:hover:not(:disabled) svg {
  color: white;
}

.delete-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-loader-sm {
  width: 16px;
  height: 16px;
  border: 2px solid #fecaca;
  border-top-color: #ef4444;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* Responsive */
@media (max-width: 768px) {
  .department-container {
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .header-content {
    flex-direction: column;
  }

  .add-form {
    flex-direction: column;
  }

  .form-group {
    width: 100%;
  }

  .add-btn {
    width: 100%;
    justify-content: center;
  }

  .departments-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>