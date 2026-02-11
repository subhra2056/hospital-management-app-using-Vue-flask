<template>
  <div class="patient-list-container">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
          </svg>
        </div>
        <div class="header-text">
          <h1>Patient Directory</h1>
          <p>Manage and view all registered patients</p>
        </div>
      </div>
      <div class="header-stats">
        <div class="stat-badge">
          <span class="stat-number">{{ patients.length }}</span>
          <span class="stat-label">Total Patients</span>
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
          placeholder="Search patients by name..." 
          class="search-input"
        />
        <button v-if="searchQuery" class="clear-btn" @click="searchQuery = ''">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
      <div class="results-count">
        <span>Showing <strong>{{ filteredPatients.length }}</strong> of <strong>{{ patients.length }}</strong> patients</span>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="loader"></div>
      <p>Loading patients...</p>
    </div>

    <div v-if="errorMessage" class="error-alert">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      {{ errorMessage }}
    </div>

    <!-- Empty search results -->
    <div v-if="!loading && filteredPatients.length === 0 && searchQuery" class="no-results">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      <h3>No patients found</h3>
      <p>No patients match "{{ searchQuery }}"</p>
    </div>

    <div class="cards-scroll-container">
      <div class="cards-grid">
        <div
          v-for="patient in filteredPatients"
        :key="patient.id"
        class="patient-card"
      >
        <div class="card-accent"></div>
        <div class="card-content">
          <div class="card-header">
            <div class="avatar-wrapper">
              <img class="avatar" :src="patientIcon" alt="Patient" />
              <div class="avatar-badge">
                <svg fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
              </div>
            </div>
            <div class="patient-identity">
              <h3 class="patient-name">{{ patient.username }}</h3>
              <p class="patient-email">{{ patient.email }}</p>
            </div>
          </div>

          <div class="info-grid">
            <div class="info-item">
              <div class="info-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
              </div>
              <div class="info-content">
                <span class="info-label">Age</span>
                <span class="info-value">{{ patient.age }} years</span>
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
                <span class="info-value">{{ patient.gender }}</span>
              </div>
            </div>
            <div class="info-item">
              <div class="info-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                </svg>
              </div>
              <div class="info-content">
                <span class="info-label">Phone</span>
                <span class="info-value">{{ patient.phone }}</span>
              </div>
            </div>
            <div class="info-item full-width">
              <div class="info-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
              </div>
              <div class="info-content">
                <span class="info-label">Address</span>
                <span class="info-value">{{ patient.address }}</span>
              </div>
            </div>
          </div>

          <div class="card-actions">
            <button class="action-btn edit-btn" @click="editPatient(patient)">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
              </svg>
              Edit
            </button>
            <button class="action-btn delete-btn" @click="deletePatient(patient)">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
              </svg>
              Delete
            </button>
            <button class="action-btn block-btn" @click="blockPatient(patient)">
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

    <!-- Edit Patient Modal -->
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
                <h3>Edit Patient</h3>
              </div>
              <button class="close-btn" @click="closeEditModal">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="submitEditPatient">
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
                    <label for="edit-age">Age</label>
                    <input type="number" id="edit-age" v-model.number="editForm.age" required />
                  </div>
                  <div class="form-group">
                    <label for="edit-gender">Gender</label>
                    <select id="edit-gender" v-model="editForm.gender" required>
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                </div>
                <div class="form-group">
                  <label for="edit-phone">Phone</label>
                  <input type="text" id="edit-phone" v-model="editForm.phone" required />
                </div>
                <div class="form-group">
                  <label for="edit-address">Address</label>
                  <textarea id="edit-address" v-model="editForm.address" required></textarea>
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
import patientIcon from "../../assets/patient.png";
import auth from "../../utils/auth";

const router = useRouter();
const patients = ref([]);
const loading = ref(false);
const errorMessage = ref("");
const showEditModal = ref(false);
const searchQuery = ref("");

// Computed property for filtered patients
const filteredPatients = computed(() => {
  if (!searchQuery.value.trim()) {
    return patients.value;
  }
  const query = searchQuery.value.toLowerCase().trim();
  return patients.value.filter(patient => 
    patient.username.toLowerCase().includes(query)
  );
});
const editForm = ref({
  id: null,
  username: "",
  email: "",
  age: "",
  gender: "",
  phone: "",
  address: ""
});

const fetchPatients = async () => {
  loading.value = true;

  try {
    const token = auth.getToken();

    const response = await fetch("http://127.0.0.1:5000/api/admin/patient-list", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error("Failed to fetch patients");
    }

    const data = await response.json();
    patients.value = data.patients.filter(p => p.active);

  } catch (err) {
    errorMessage.value = "Failed to load patients.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchPatients();
});

const editPatient = (patient) => {
  editForm.value = {
    id: patient.id,
    username: patient.username,
    email: patient.email,
    age: patient.age,
    gender: patient.gender,
    phone: patient.phone,
    address: patient.address
  };
  showEditModal.value = true;
};

const submitEditPatient = async () => {
  const token = auth.getToken();
  if (!token) {
    alert("Please login first");
    router.push("/login");
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:5000/api/admin/patients/${editForm.value.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        username: editForm.value.username,
        email: editForm.value.email,
        age: editForm.value.age,
        gender: editForm.value.gender,
        phone: editForm.value.phone,
        address: editForm.value.address
      })
    });

    if (response.ok) {
      alert("Patient updated successfully");
      showEditModal.value = false;
      fetchPatients();
    } else {
      if (response.status === 401) {
        alert("Please login again");
        auth.clearAll();
        router.push("/login");
      } else if (response.status === 403) {
        alert("Unauthorized");
      } else {
        const errorData = await response.json();
        alert(errorData.message || "Failed to update patient");
      }
    }
  } catch (err) {
    console.error(err);
    alert("Error updating patient");
  }
};

const closeEditModal = () => {
  showEditModal.value = false;
};

const deletePatient = async (patient) => {
  const token = auth.getToken();
  if (!token) {
    alert("Please login first");
    router.push("/login");
    return;
  }

  if (confirm(`Are you sure you want to delete ${patient.username}?`)) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/admin/patients/${patient.id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (response.ok) {
        alert("Patient deleted successfully");
        fetchPatients();
      } else {
        if (response.status === 401) {
          alert("Please login again");
          auth.clearAll();
          router.push("/login");
        } else if (response.status === 403) {
          alert("Unauthorized");
        } else {
          alert("Failed to delete patient");
        }
      }
    } catch (err) {
      console.error(err);
      alert("Error deleting patient");
    }
  }
};

const blockPatient = async (patient) => {
  const token = auth.getToken();
  if (!token) {
    alert("Please login first");
    router.push("/login");
    return;
  }

  if (confirm(`Are you sure you want to block ${patient.username}?`)) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/admin/users/${patient.id}/block`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (response.ok) {
        alert("Patient blocked successfully");
        fetchPatients();
      } else {
        if (response.status === 401) {
          alert("Please login again");
          auth.clearAll();
          router.push("/login");
        } else if (response.status === 403) {
          alert("Unauthorized");
        } else {
          alert("Failed to block patient");
        }
      }
    } catch (err) {
      console.error(err);
      alert("Error blocking patient");
    }
  }
};

</script>

<style scoped>
.patient-list-container {
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
  min-width: 280px;
  max-width: 400px;
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

.results-count {
  padding: 0.75rem 1.25rem;
  background: #f8fafc;
  border-radius: 10px;
  font-size: 0.875rem;
  color: #64748b;
  white-space: nowrap;
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

/* Patient Card */
.patient-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.patient-card:hover {
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
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
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

.patient-card:hover .avatar {
  border-color: #5e63b6;
}

.avatar-badge {
  position: absolute;
  bottom: -4px;
  right: -4px;
  width: 24px;
  height: 24px;
  background: #10b981;
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

.patient-identity {
  flex: 1;
  min-width: 0;
}

.patient-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.patient-email {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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

.info-item.full-width {
  grid-column: 1 / -1;
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
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  box-sizing: border-box;
  background: #fafafa;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
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
  .patient-list-container {
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

  .search-box {
    max-width: 100%;
    width: 100%;
  }

  .results-count {
    width: 100%;
    text-align: center;
  }

  .cards-scroll-container {
    max-height: calc(100vh - 480px);
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
}
</style>
