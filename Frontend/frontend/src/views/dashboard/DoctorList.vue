<template>
  <div class="doctor-list-container">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <div class="header-text">
          <h1>Doctor Directory</h1>
          <p>Manage and view all registered doctors</p>
        </div>
      </div>
      <div class="header-stats">
        <div class="stat-badge">
          <span class="stat-number">{{ doctors.length }}</span>
          <span class="stat-label">Total Doctors</span>
        </div>
      </div>
    </div>

    <!-- Search & Filter Bar -->
    <div class="search-filter-bar">
      <div class="search-box">
        <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search by name or email..." 
          class="search-input"
        />
        <button v-if="searchQuery" class="clear-btn" @click="searchQuery = ''">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
      <div class="filter-box">
        <svg class="filter-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
        </svg>
        <select v-model="departmentFilter" class="filter-select">
          <option value="">All Departments</option>
          <option v-for="dept in departments" :key="dept" :value="dept">{{ dept }}</option>
        </select>
      </div>
      <div class="results-count">
        <span>Showing <strong>{{ filteredDoctors.length }}</strong> of <strong>{{ doctors.length }}</strong> doctors</span>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="loader"></div>
      <p>Loading doctors...</p>
    </div>

    <div v-if="errorMessage" class="error-alert">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      {{ errorMessage }}
    </div>

    <!-- Empty search results -->
    <div v-if="!loading && filteredDoctors.length === 0 && (searchQuery || departmentFilter)" class="no-results">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      <h3>No doctors found</h3>
      <p>No doctors match your search criteria</p>
    </div>

    <div class="cards-scroll-container">
      <div class="cards-grid">
        <div
          v-for="doctor in filteredDoctors"
        :key="doctor.id"
        class="doctor-card"
      >
        <div class="card-accent"></div>
        <div class="card-content">
          <div class="card-header">
            <div class="avatar-wrapper">
              <img class="avatar" :src="DoctorIcon" alt="Doctor" />
              <div class="avatar-badge">
                <svg fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
            </div>
            <div class="doctor-identity">
              <h3 class="doctor-name">{{ doctor.username }}</h3>
              <p class="doctor-email">{{ doctor.email }}</p>
            </div>
          </div>

          <div class="badges-row">
            <span class="badge badge-department">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
              {{ doctor.department_name }}
            </span>
            <span class="badge badge-specialization">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
              </svg>
              {{ doctor.specialization }}
            </span>
          </div>

          <div class="info-grid">
            <div class="info-item">
              <div class="info-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                </svg>
              </div>
              <div class="info-content">
                <span class="info-label">Experience</span>
                <span class="info-value">{{ doctor.experience_years }} years</span>
              </div>
            </div>
            <div class="info-item">
              <div class="info-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <div class="info-content">
                <span class="info-label">Gender</span>
                <span class="info-value">{{ doctor.gender }}</span>
              </div>
            </div>
          </div>

          <div class="card-actions">
            <button class="action-btn edit-btn" @click="editDoctor(doctor)">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
              </svg>
              Edit
            </button>
            <button class="action-btn delete-btn" @click="deleteDoctor(doctor)">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
              </svg>
              Delete
            </button>
            <button class="action-btn block-btn" @click="blockDoctor(doctor)">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"></path>
              </svg>
              Block
            </button>
          </div>
        </div>
      </div>
    </div>
    </div>

    <!-- Edit Doctor Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showEditModal" class="modal-overlay" @click.self="closeEditModal">
          <div class="modal-container">
            <div class="modal-header">
              <div class="modal-title-group">
                <div class="modal-icon">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                  </svg>
                </div>
                <h3>Edit Doctor</h3>
              </div>
              <button class="close-btn" @click="closeEditModal">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="submitEditDoctor">
                <div class="form-row">
                  <div class="form-group">
                    <label for="edit-username">Username</label>
                    <input type="text" id="edit-username" v-model="editForm.username" required />
                  </div>
                  <div class="form-group">
                    <label for="edit-email">Email</label>
                    <input type="email" id="edit-email" v-model="editForm.email" required />
                  </div>
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label for="edit-specialization">Specialization</label>
                    <input type="text" id="edit-specialization" v-model="editForm.specialization" required />
                  </div>
                  <div class="form-group">
                    <label for="edit-experience">Experience (years)</label>
                    <input type="number" id="edit-experience" v-model.number="editForm.experience_years" required />
                  </div>
                </div>
                <div class="form-group">
                  <label for="edit-gender">Gender</label>
                  <select id="edit-gender" v-model="editForm.gender" required>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
                <div class="modal-actions">
                  <button type="button" class="btn-secondary" @click="closeEditModal">Cancel</button>
                  <button type="submit" class="btn-primary">Save Changes</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>


<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import DoctorIcon from "../../assets/doctor.png"
import auth from "../../utils/auth";

const router = useRouter();
const doctors = ref([]);
const loading = ref(false);
const errorMessage = ref("");
const showEditModal = ref(false);
const searchQuery = ref("");
const departmentFilter = ref("");

// Computed property for unique departments
const departments = computed(() => {
  const deptSet = new Set(doctors.value.map(d => d.department_name));
  return Array.from(deptSet).sort();
});

// Computed property for filtered doctors
const filteredDoctors = computed(() => {
  let result = doctors.value;
  
  // Filter by department
  if (departmentFilter.value) {
    result = result.filter(doctor => doctor.department_name === departmentFilter.value);
  }
  
  // Filter by search query (name or email)
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim();
    result = result.filter(doctor => 
      doctor.username.toLowerCase().includes(query) ||
      doctor.email.toLowerCase().includes(query)
    );
  }
  
  return result;
});
const editForm = ref({
  id: null,
  username: "",
  email: "",
  specialization: "",
  experience_years: "",
  gender: ""
});

const fetchDoctors = async () => {
  loading.value = true;

  try {
    const token = auth.getToken();

    const response = await fetch("http://127.0.0.1:5000/api/admin/doctor-list", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error("Failed to fetch");
    }

    const data = await response.json();
    doctors.value = data.doctors.filter(d => d.active);

  } catch (err) {
    errorMessage.value = "Failed to load doctors.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchDoctors();
});

const editDoctor = (doctor) => {
  editForm.value = {
    id: doctor.id,
    username: doctor.username,
    email: doctor.email,
    specialization: doctor.specialization,
    experience_years: doctor.experience_years,
    gender: doctor.gender
  };
  showEditModal.value = true;
};

const submitEditDoctor = async () => {
  const token = auth.getToken();
  if (!token) {
    alert("Please login first");
    router.push("/login");
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:5000/api/admin/doctors/${editForm.value.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        username: editForm.value.username,
        email: editForm.value.email,
        specialization: editForm.value.specialization,
        experience_years: editForm.value.experience_years,
        gender: editForm.value.gender
      })
    });

    if (response.ok) {
      alert("Doctor updated successfully");
      showEditModal.value = false;
      fetchDoctors();
    } else {
      if (response.status === 401) {
        alert("Please login again");
        auth.clearAll();
        router.push("/login");
      } else if (response.status === 403) {
        alert("Unauthorized");
      } else {
        const errorData = await response.json();
        alert(errorData.message || "Failed to update doctor");
      }
    }
  } catch (err) {
    console.error(err);
    alert("Error updating doctor");
  }
};

const closeEditModal = () => {
  showEditModal.value = false;
};

const deleteDoctor = async (doctor) => {
  const token = auth.getToken();
  if (!token) {
    alert("Please login first");
    router.push("/login");
    return;
  }

  if (confirm(`Are you sure you want to delete ${doctor.username}?`)) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/admin/doctors/${doctor.id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (response.ok) {
        alert("Doctor deleted successfully");
        fetchDoctors();
      } else {
        if (response.status === 401) {
          alert("Please login again");
          auth.clearAll();
          router.push("/login");
        } else if (response.status === 403) {
          alert("Unauthorized");
        } else {
          const errorData = await response.json();
          alert(errorData.message || "Failed to delete doctor");
        }
      }
    } catch (err) {
      console.error(err);
      alert("Error deleting doctor");
    }
  }
};

const blockDoctor = async (doctor) => {
  const token = auth.getToken();
  if (!token) {
    alert("Please login first");
    router.push("/login");
    return;
  }

  if (confirm(`Are you sure you want to block ${doctor.username}?`)) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/admin/users/${doctor.id}/block`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (response.ok) {
        alert("Doctor blocked successfully");
        fetchDoctors();
      } else {
        if (response.status === 401) {
          alert("Please login again");
          auth.clearAll();
          router.push("/login");
        } else if (response.status === 403) {
          alert("Unauthorized");
        } else {
          alert("Failed to block doctor");
        }
      }
    } catch (err) {
      console.error(err);
      alert("Error blocking doctor");
    }
  }
};
</script>


<style scoped>
.doctor-list-container {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding: 1.25rem 1.75rem;
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
  letter-spacing: -0.025em;
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

/* Search & Filter Bar */
.search-filter-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  align-items: center;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 250px;
  max-width: 350px;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #94a3b8;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.875rem 2.5rem 0.875rem 3rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 0.95rem;
  background: white;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #5e63b6;
  box-shadow: 0 0 0 4px rgba(94, 99, 182, 0.1);
}

.search-input::placeholder {
  color: #94a3b8;
}

.clear-btn {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  width: 28px;
  height: 28px;
  border: none;
  background: #f1f5f9;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.clear-btn:hover {
  background: #e2e8f0;
}

.clear-btn svg {
  width: 16px;
  height: 16px;
  color: #64748b;
}

.filter-box {
  position: relative;
  min-width: 200px;
}

.filter-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: #94a3b8;
  pointer-events: none;
  z-index: 1;
}

.filter-select {
  width: 100%;
  padding: 0.875rem 1rem 0.875rem 2.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 0.95rem;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%2394a3b8' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.75rem center;
  background-repeat: no-repeat;
  background-size: 1.25rem;
}

.filter-select:focus {
  outline: none;
  border-color: #5e63b6;
  box-shadow: 0 0 0 4px rgba(94, 99, 182, 0.1);
}

.results-count {
  padding: 0.75rem 1.25rem;
  background: #f8fafc;
  border-radius: 10px;
  font-size: 0.875rem;
  color: #64748b;
  white-space: nowrap;
  margin-left: auto;
}

.results-count strong {
  color: #5e63b6;
  font-weight: 600;
}

/* No Results */
.no-results {
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

.no-results svg {
  width: 64px;
  height: 64px;
  color: #cbd5e1;
  margin-bottom: 1rem;
}

.no-results h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #334155;
  margin: 0 0 0.5rem;
}

.no-results p {
  color: #64748b;
  margin: 0;
}

/* Scrollable Cards Container */
.cards-scroll-container {
  max-height: calc(100vh - 380px);
  overflow-y: auto;
  padding-right: 0.5rem;
  margin-right: -0.5rem;
}

.cards-scroll-container::-webkit-scrollbar {
  width: 8px;
}

.cards-scroll-container::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}

.cards-scroll-container::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

.cards-scroll-container::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
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

/* Error Alert */
.error-alert {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  color: #dc2626;
  margin-bottom: 1.5rem;
}

.error-alert svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

/* Cards Grid */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 1.5rem;
}

/* Doctor Card */
.doctor-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.doctor-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(94, 99, 182, 0.2);
}

.card-accent {
  height: 6px;
  background: linear-gradient(90deg, #5e63b6 0%, #7c81d4 50%, #5e63b6 100%);
  background-size: 200% 100%;
  animation: shimmer 3s ease infinite;
}

@keyframes shimmer {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.card-content {
  padding: 1.75rem;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.25rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid #f1f5f9;
}

.avatar-wrapper {
  position: relative;
  flex-shrink: 0;
}

.avatar {
  width: 72px;
  height: 72px;
  border-radius: 18px;
  object-fit: cover;
  border: 3px solid #f1f5f9;
  transition: all 0.3s ease;
}

.doctor-card:hover .avatar {
  border-color: #5e63b6;
}

.avatar-badge {
  position: absolute;
  bottom: -4px;
  right: -4px;
  width: 24px;
  height: 24px;
  background: #5e63b6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid white;
}

.avatar-badge svg {
  width: 14px;
  height: 14px;
  color: white;
}

.doctor-identity {
  flex: 1;
  min-width: 0;
}

.doctor-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.doctor-email {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Badges Row */
.badges-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 0.875rem;
  border-radius: 25px;
  font-size: 0.8rem;
  font-weight: 600;
}

.badge svg {
  width: 14px;
  height: 14px;
}

.badge-department {
  background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
  color: #5e63b6;
}

.badge-specialization {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  color: #16a34a;
}

/* Info Grid */
.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.875rem;
  background: #f8fafc;
  border-radius: 12px;
  transition: all 0.2s ease;
}

.info-item:hover {
  background: #f1f5f9;
}

.info-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #5e63b6 0%, #7c81d4 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.info-icon svg {
  width: 18px;
  height: 18px;
  color: white;
}

.info-content {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.info-label {
  font-size: 0.75rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.info-value {
  font-size: 0.9rem;
  color: #334155;
  font-weight: 500;
}

/* Card Actions */
.card-actions {
  display: flex;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.edit-btn {
  background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
  color: #5e63b6;
}

.edit-btn:hover {
  background: linear-gradient(135deg, #5e63b6 0%, #4a50a0 100%);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(94, 99, 182, 0.3);
}

.delete-btn {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #dc2626;
}

.delete-btn:hover {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.3);
}

.block-btn {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #d97706;
}

.block-btn:hover {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(245, 158, 11, 0.3);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-container {
  background: white;
  border-radius: 24px;
  width: 90%;
  max-width: 560px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, #5e63b6 0%, #4a50a0 100%);
}

.modal-title-group {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.modal-icon {
  width: 44px;
  height: 44px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

.modal-header h3 {
  margin: 0;
  color: white;
  font-size: 1.25rem;
  font-weight: 700;
}

.close-btn {
  width: 36px;
  height: 36px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.close-btn svg {
  width: 20px;
  height: 20px;
  color: white;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.modal-body {
  padding: 2rem;
  max-height: calc(90vh - 120px);
  overflow-y: auto;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #374151;
  font-weight: 600;
  font-size: 0.875rem;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  box-sizing: border-box;
  background: #fafafa;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #5e63b6;
  background: white;
  box-shadow: 0 0 0 4px rgba(94, 99, 182, 0.1);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.btn-secondary {
  padding: 0.875rem 1.5rem;
  border: 2px solid #e5e7eb;
  background: white;
  color: #64748b;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.btn-primary {
  padding: 0.875rem 1.5rem;
  border: none;
  background: linear-gradient(135deg, #5e63b6 0%, #4a50a0 100%);
  color: white;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(94, 99, 182, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(94, 99, 182, 0.4);
}

/* Modal Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .doctor-list-container {
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
    margin-bottom: 1.5rem;
  }

  .header-content {
    flex-direction: column;
  }

  .search-filter-bar {
    flex-direction: column;
  }

  .search-box,
  .filter-box {
    max-width: 100%;
    width: 100%;
  }

  .results-count {
    width: 100%;
    text-align: center;
    margin-left: 0;
  }

  .cards-scroll-container {
    max-height: calc(100vh - 500px);
  }

  .cards-grid {
    grid-template-columns: 1fr;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .card-actions {
    flex-direction: column;
  }

  .badges-row {
    justify-content: center;
  }
}
</style>
