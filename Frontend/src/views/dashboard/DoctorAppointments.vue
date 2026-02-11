<template>
  <div class="appointments-container">
    <div class="appointments-header">
      <h2 class="page-title">My Appointments</h2>
      <p class="page-subtitle">View and manage all your patient appointments</p>
    </div>

    <!-- Tab Navigation -->
    <div class="tabs-container">
      <button 
        v-for="tab in tabs" 
        :key="tab.key"
        :class="['tab-btn', { active: activeTab === tab.key }]"
        @click="activeTab = tab.key"
      >
        <component :is="tab.icon" class="tab-icon" />
        <span>{{ tab.label }}</span>
        <span class="tab-count" :class="tab.key">{{ getTabCount(tab.key) }}</span>
      </button>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else class="appointments-content">
      <!-- Today's Appointments -->
      <div v-if="activeTab === 'today'" class="appointments-section">
        <div v-if="todayAppointments.length === 0" class="empty-state">
          <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
          </svg>
          <p class="empty-text">No appointments scheduled for today</p>
        </div>
        <div v-else class="appointments-grid">
          <div v-for="apt in todayAppointments" :key="apt.id" class="appointment-card today">
            <div class="card-header">
              <div class="status-indicator today"></div>
              <span class="status-text">Today</span>
              <span class="appointment-time">{{ apt.appointment_time }}</span>
            </div>
            <div class="card-body">
              <div class="patient-info">
                <div class="avatar">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                </div>
                <div class="info-text">
                  <h6 class="name">{{ apt.patient_name }}</h6>
                  <p class="email">{{ apt.patient_email }}</p>
                  <p class="phone">{{ apt.patient_phone || 'No phone' }}</p>
                </div>
              </div>
              <div class="card-actions">
                <span class="status-badge" :class="apt.status.toLowerCase()">{{ apt.status }}</span>
                <button 
                  v-if="apt.status === 'BOOKED'"
                  class="btn-action complete"
                  @click="openTreatmentModal(apt)"
                >
                  Complete Visit
                </button>
                <button 
                  v-if="apt.status === 'BOOKED'"
                  class="btn-action cancel"
                  @click="cancelAppointment(apt.id)"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Upcoming Appointments -->
      <div v-if="activeTab === 'upcoming'" class="appointments-section">
        <div v-if="upcomingAppointments.length === 0" class="empty-state">
          <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
          </svg>
          <p class="empty-text">No upcoming appointments</p>
        </div>
        <div v-else class="appointments-grid">
          <div v-for="apt in upcomingAppointments" :key="apt.id" class="appointment-card upcoming">
            <div class="card-header">
              <div class="status-indicator upcoming"></div>
              <span class="status-text">{{ formatDate(apt.appointment_date) }}</span>
              <span class="appointment-time">{{ apt.appointment_time }}</span>
            </div>
            <div class="card-body">
              <div class="patient-info">
                <div class="avatar">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                </div>
                <div class="info-text">
                  <h6 class="name">{{ apt.patient_name }}</h6>
                  <p class="email">{{ apt.patient_email }}</p>
                </div>
              </div>
              <div class="card-actions">
                <span class="status-badge booked">{{ apt.status }}</span>
                <button 
                  class="btn-action cancel"
                  @click="cancelAppointment(apt.id)"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Completed Appointments -->
      <div v-if="activeTab === 'completed'" class="appointments-section">
        <div v-if="completedAppointments.length === 0" class="empty-state">
          <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <p class="empty-text">No completed appointments yet</p>
        </div>
        <div v-else class="appointments-grid">
          <div v-for="apt in completedAppointments" :key="apt.id" class="appointment-card completed">
            <div class="card-header">
              <div class="status-indicator completed"></div>
              <span class="status-text">{{ formatDate(apt.appointment_date) }}</span>
              <span class="appointment-time">{{ apt.appointment_time }}</span>
            </div>
            <div class="card-body">
              <div class="patient-info">
                <div class="avatar">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                </div>
                <div class="info-text">
                  <h6 class="name">{{ apt.patient_name }}</h6>
                  <p class="email">{{ apt.patient_email }}</p>
                </div>
              </div>
              <div class="card-actions">
                <span class="status-badge completed">Completed</span>
                <button 
                  v-if="apt.treatment"
                  class="btn-action view"
                  @click="viewTreatment(apt)"
                >
                  View Treatment
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- All Appointments -->
      <div v-if="activeTab === 'all'" class="appointments-section">
        <!-- Filter Section -->
        <div class="filter-section">
          <div class="filter-row">
            <div class="filter-group">
              <label class="filter-label">From Date</label>
              <input type="date" v-model="filterStartDate" class="filter-input" />
            </div>
            <div class="filter-group">
              <label class="filter-label">To Date</label>
              <input type="date" v-model="filterEndDate" class="filter-input" />
            </div>
            <div class="filter-group">
              <label class="filter-label">Status</label>
              <select v-model="filterStatus" class="filter-input">
                <option value="">All Status</option>
                <option value="BOOKED">Booked</option>
                <option value="COMPLETED">Completed</option>
                <option value="CANCELLED">Cancelled</option>
              </select>
            </div>
            <div class="filter-actions">
              <button class="filter-btn primary" @click="applyFilters">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="16" height="16">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path>
                </svg>
                Apply
              </button>
              <button class="filter-btn secondary" @click="clearFilters">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="16" height="16">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
                Clear
              </button>
            </div>
          </div>
        </div>
        
        <div v-if="appointments.length === 0" class="empty-state">
          <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
          </svg>
          <p class="empty-text">No appointments found</p>
        </div>
        <div v-else class="appointments-table-wrapper">
          <table class="appointments-table">
            <thead>
              <tr>
                <th>Patient</th>
                <th>Date</th>
                <th>Time</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="apt in appointments" :key="apt.id">
                <td>
                  <div class="patient-cell">
                    <span class="patient-name">{{ apt.patient_name }}</span>
                    <span class="patient-email">{{ apt.patient_email }}</span>
                  </div>
                </td>
                <td>{{ formatDate(apt.appointment_date) }}</td>
                <td>{{ apt.appointment_time }}</td>
                <td><span class="status-badge" :class="apt.status.toLowerCase()">{{ apt.status }}</span></td>
                <td>
                  <div class="action-buttons">
                    <button 
                      v-if="apt.status === 'BOOKED'"
                      class="btn-sm complete"
                      @click="openTreatmentModal(apt)"
                      title="Complete Visit"
                    >
                      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                    </button>
                    <button 
                      v-if="apt.status === 'BOOKED'"
                      class="btn-sm cancel"
                      @click="cancelAppointment(apt.id)"
                      title="Cancel"
                    >
                      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                      </svg>
                    </button>
                    <button 
                      v-if="apt.status === 'COMPLETED' && apt.treatment"
                      class="btn-sm view"
                      @click="viewTreatment(apt)"
                      title="View Treatment"
                    >
                      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Treatment Modal -->
    <div v-if="showTreatmentModal" class="modal-overlay" @click.self="closeTreatmentModal">
      <div class="modal-content treatment-modal">
        <div class="modal-header">
          <h4>{{ isViewingTreatment ? 'Treatment Details' : 'Complete Visit' }}</h4>
          <button class="modal-close" @click="closeTreatmentModal">×</button>
        </div>
        <div class="modal-body">
          <div v-if="selectedAppointment" class="patient-summary">
            <p><strong>Patient:</strong> {{ selectedAppointment.patient_name }}</p>
            <p><strong>Date:</strong> {{ formatDate(selectedAppointment.appointment_date) }}</p>
            <p><strong>Time:</strong> {{ selectedAppointment.appointment_time }}</p>
          </div>
          
          <div v-if="isViewingTreatment && selectedAppointment?.treatment" class="treatment-view">
            <div class="treatment-field">
              <label>Diagnosis</label>
              <p>{{ selectedAppointment.treatment.diagnosis }}</p>
            </div>
            <div class="treatment-field">
              <label>Prescription</label>
              <p>{{ selectedAppointment.treatment.prescription || 'None' }}</p>
            </div>
            <div v-if="selectedAppointment.treatment.notes" class="treatment-field">
              <label>Notes</label>
              <p>{{ selectedAppointment.treatment.notes }}</p>
            </div>
            <div v-if="selectedAppointment.treatment.next_visit" class="treatment-field">
              <label>Next Visit</label>
              <p>{{ formatDate(selectedAppointment.treatment.next_visit) }}</p>
            </div>
          </div>
          
          <form v-else @submit.prevent="saveTreatment" class="treatment-form">
            <div class="form-group">
              <label>Diagnosis *</label>
              <textarea v-model="treatmentData.diagnosis" required rows="3" placeholder="Enter diagnosis..."></textarea>
            </div>
            <div class="form-group">
              <label>Prescription</label>
              <textarea v-model="treatmentData.prescription" rows="3" placeholder="Enter prescription..."></textarea>
            </div>
            <div class="form-group">
              <label>Notes</label>
              <textarea v-model="treatmentData.notes" rows="2" placeholder="Additional notes..."></textarea>
            </div>
            <div class="form-group">
              <label>Next Visit Date</label>
              <input type="date" v-model="treatmentData.next_visit" :min="minDate" />
            </div>
            <div class="modal-actions">
              <button type="button" class="btn-secondary" @click="closeTreatmentModal">Cancel</button>
              <button type="submit" class="btn-primary" :disabled="!treatmentData.diagnosis || saving">
                <span v-if="saving" class="spinner"></span>
                {{ saving ? 'Saving...' : 'Save Treatment' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, h } from "vue";
import auth from "../../utils/auth";

const appointments = ref([]);
const loading = ref(true);
const activeTab = ref("today");
const showTreatmentModal = ref(false);
const selectedAppointment = ref(null);
const isViewingTreatment = ref(false);
const saving = ref(false);

// Filter state
const filterStartDate = ref("");
const filterEndDate = ref("");
const filterStatus = ref("");
const treatmentData = ref({
  diagnosis: "",
  prescription: "",
  notes: "",
  next_visit: ""
});

const minDate = computed(() => new Date().toISOString().split('T')[0]);

const tabs = [
  {
    key: "today",
    label: "Today",
    icon: () => h("svg", { fill: "none", stroke: "currentColor", viewBox: "0 0 24 24", class: "icon" }, [
      h("path", { "stroke-linecap": "round", "stroke-linejoin": "round", "stroke-width": "2", d: "M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" })
    ])
  },
  {
    key: "upcoming",
    label: "Upcoming",
    icon: () => h("svg", { fill: "none", stroke: "currentColor", viewBox: "0 0 24 24", class: "icon" }, [
      h("path", { "stroke-linecap": "round", "stroke-linejoin": "round", "stroke-width": "2", d: "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" })
    ])
  },
  {
    key: "completed",
    label: "Completed",
    icon: () => h("svg", { fill: "none", stroke: "currentColor", viewBox: "0 0 24 24", class: "icon" }, [
      h("path", { "stroke-linecap": "round", "stroke-linejoin": "round", "stroke-width": "2", d: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" })
    ])
  },
  {
    key: "all",
    label: "All",
    icon: () => h("svg", { fill: "none", stroke: "currentColor", viewBox: "0 0 24 24", class: "icon" }, [
      h("path", { "stroke-linecap": "round", "stroke-linejoin": "round", "stroke-width": "2", d: "M4 6h16M4 10h16M4 14h16M4 18h16" })
    ])
  }
];

const todayAppointments = computed(() => {
  const today = new Date().toISOString().split('T')[0];
  return appointments.value.filter(apt => apt.appointment_date === today && apt.status === 'BOOKED');
});

const upcomingAppointments = computed(() => {
  const today = new Date().toISOString().split('T')[0];
  return appointments.value.filter(apt => apt.appointment_date > today && apt.status === 'BOOKED');
});

const completedAppointments = computed(() => {
  return appointments.value.filter(apt => apt.status === 'COMPLETED');
});

const getTabCount = (key) => {
  switch (key) {
    case 'today': return todayAppointments.value.length;
    case 'upcoming': return upcomingAppointments.value.length;
    case 'completed': return completedAppointments.value.length;
    case 'all': return appointments.value.length;
    default: return 0;
  }
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
};

const loadAppointments = async () => {
  loading.value = true;
  try {
    const token = auth.getToken();
    
    // Build query string with filters
    const params = new URLSearchParams();
    if (filterStartDate.value) params.append('start_date', filterStartDate.value);
    if (filterEndDate.value) params.append('end_date', filterEndDate.value);
    if (filterStatus.value) params.append('status', filterStatus.value);
    
    const queryString = params.toString();
    const url = `http://localhost:5000/api/doctor/appointments${queryString ? '?' + queryString : ''}`;
    
    const response = await fetch(url, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (response.ok) {
      const data = await response.json();
      appointments.value = data.appointments || [];
    }
  } catch (error) {
    console.error("Error loading appointments:", error);
  } finally {
    loading.value = false;
  }
};

const applyFilters = () => {
  loadAppointments();
};

const clearFilters = () => {
  filterStartDate.value = "";
  filterEndDate.value = "";
  filterStatus.value = "";
  loadAppointments();
};

const openTreatmentModal = (apt) => {
  selectedAppointment.value = apt;
  isViewingTreatment.value = false;
  treatmentData.value = { diagnosis: "", prescription: "", notes: "", next_visit: "" };
  showTreatmentModal.value = true;
};

const viewTreatment = (apt) => {
  selectedAppointment.value = apt;
  isViewingTreatment.value = true;
  showTreatmentModal.value = true;
};

const closeTreatmentModal = () => {
  showTreatmentModal.value = false;
  selectedAppointment.value = null;
  isViewingTreatment.value = false;
};

const saveTreatment = async () => {
  if (!selectedAppointment.value || !treatmentData.value.diagnosis) return;
  saving.value = true;
  try {
    const token = auth.getToken();
    const response = await fetch(`http://localhost:5000/api/doctor/appointments/${selectedAppointment.value.id}/treatment`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(treatmentData.value)
    });
    if (response.ok) {
      await loadAppointments();
      closeTreatmentModal();
    } else {
      const data = await response.json();
      alert(data.message || "Failed to save treatment");
    }
  } catch (error) {
    console.error("Error saving treatment:", error);
    alert("Failed to save treatment");
  } finally {
    saving.value = false;
  }
};

const cancelAppointment = async (id) => {
  if (!confirm("Are you sure you want to cancel this appointment?")) return;
  try {
    const token = auth.getToken();
    const response = await fetch(`http://localhost:5000/api/appointments/${id}/cancel`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` }
    });
    if (response.ok) {
      await loadAppointments();
    } else {
      const data = await response.json();
      alert(data.message || "Failed to cancel appointment");
    }
  } catch (error) {
    console.error("Error cancelling appointment:", error);
    alert("Failed to cancel appointment");
  }
};

onMounted(() => {
  loadAppointments();
});
</script>

<style scoped>
.appointments-container {
  padding: 0;
}

.appointments-header {
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
}

.tabs-container {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  padding: 0.5rem;
  background: #f1f5f9;
  border-radius: 12px;
  flex-wrap: wrap;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border: none;
  background: transparent;
  border-radius: 8px;
  font-weight: 500;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn:hover {
  background: white;
  color: #1e293b;
}

.tab-btn.active {
  background: white;
  color: #5e63b6;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.tab-icon {
  width: 18px;
  height: 18px;
}

.tab-count {
  padding: 0.125rem 0.5rem;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 600;
}

.tab-count.today { background: #dbeafe; color: #1d4ed8; }
.tab-count.upcoming { background: #fef3c7; color: #d97706; }
.tab-count.completed { background: #d1fae5; color: #059669; }
.tab-count.all { background: #e2e8f0; color: #475569; }

.loading-container {
  display: flex;
  justify-content: center;
  padding: 4rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  width: 64px;
  height: 64px;
  color: #cbd5e1;
  margin-bottom: 1rem;
}

.empty-text {
  color: #64748b;
  font-size: 1rem;
}

.appointments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.appointment-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s;
}

.appointment-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.status-indicator.today { background: #3b82f6; }
.status-indicator.upcoming { background: #f59e0b; }
.status-indicator.completed { background: #10b981; }

.status-text {
  font-weight: 500;
  color: #475569;
  flex: 1;
}

.appointment-time {
  font-weight: 600;
  color: #1e293b;
}

.card-body {
  padding: 1.25rem;
}

.patient-info {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.avatar {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #5e63b6, #4a50a0);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.avatar svg {
  width: 24px;
  height: 24px;
  color: white;
}

.info-text .name {
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
}

.info-text .email,
.info-text .phone {
  color: #64748b;
  font-size: 0.875rem;
  margin: 0;
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.status-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.booked { background: #dbeafe; color: #1d4ed8; }
.status-badge.completed { background: #d1fae5; color: #059669; }
.status-badge.cancelled { background: #fee2e2; color: #dc2626; }

.btn-action {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-action.complete {
  background: #10b981;
  color: white;
}

.btn-action.complete:hover {
  background: #059669;
}

.btn-action.cancel {
  background: #fee2e2;
  color: #dc2626;
}

.btn-action.cancel:hover {
  background: #fecaca;
}

.btn-action.view {
  background: #e0e7ff;
  color: #4338ca;
}

.btn-action.view:hover {
  background: #c7d2fe;
}

/* Table Styles */
.appointments-table-wrapper {
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.appointments-table {
  width: 100%;
  border-collapse: collapse;
}

.appointments-table th {
  background: #f8fafc;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #475569;
  border-bottom: 1px solid #e2e8f0;
}

.appointments-table td {
  padding: 1rem;
  border-bottom: 1px solid #f1f5f9;
}

.appointments-table tr:hover {
  background: #f8fafc;
}

.patient-cell {
  display: flex;
  flex-direction: column;
}

.patient-name {
  font-weight: 600;
  color: #1e293b;
}

.patient-email {
  font-size: 0.875rem;
  color: #64748b;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-sm {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-sm svg {
  width: 16px;
  height: 16px;
}

.btn-sm.complete {
  background: #d1fae5;
  color: #059669;
}

.btn-sm.complete:hover {
  background: #10b981;
  color: white;
}

.btn-sm.cancel {
  background: #fee2e2;
  color: #dc2626;
}

.btn-sm.cancel:hover {
  background: #dc2626;
  color: white;
}

.btn-sm.view {
  background: #e0e7ff;
  color: #4338ca;
}

.btn-sm.view:hover {
  background: #4338ca;
  color: white;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h4 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #64748b;
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.patient-summary {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.patient-summary p {
  margin: 0.25rem 0;
  color: #475569;
}

.treatment-view .treatment-field {
  margin-bottom: 1rem;
}

.treatment-field label {
  display: block;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.25rem;
}

.treatment-field p {
  color: #1e293b;
  margin: 0;
}

.treatment-form .form-group {
  margin-bottom: 1rem;
}

.treatment-form label {
  display: block;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.treatment-form textarea,
.treatment-form input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

.treatment-form textarea:focus,
.treatment-form input:focus {
  outline: none;
  border-color: #5e63b6;
  box-shadow: 0 0 0 3px rgba(94, 99, 182, 0.1);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-secondary,
.btn-primary {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary {
  background: #f1f5f9;
  color: #475569;
}

.btn-secondary:hover {
  background: #e2e8f0;
}

.btn-primary {
  background: linear-gradient(135deg, #5e63b6, #4a50a0);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(94, 99, 182, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid white;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-right: 0.5rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .appointments-grid {
    grid-template-columns: 1fr;
  }
  
  .tabs-container {
    flex-direction: column;
  }
  
  .tab-btn {
    width: 100%;
    justify-content: center;
  }
  
  .filter-row {
    flex-direction: column;
  }
  
  .filter-actions {
    margin-left: 0;
    width: 100%;
  }
}

/* Filter Section Styles */
.filter-section {
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: flex-end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 150px;
}

.filter-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filter-input {
  padding: 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.875rem;
  color: #1e293b;
  background: white;
  transition: all 0.2s ease;
}

.filter-input:focus {
  outline: none;
  border-color: #5e63b6;
  box-shadow: 0 0 0 3px rgba(94, 99, 182, 0.1);
}

.filter-actions {
  display: flex;
  gap: 0.5rem;
  margin-left: auto;
}

.filter-btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.filter-btn.primary {
  background: #5e63b6;
  color: white;
}

.filter-btn.primary:hover {
  background: #4f52a3;
}

.filter-btn.secondary {
  background: white;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.filter-btn.secondary:hover {
  background: #f1f5f9;
  color: #1e293b;
}
</style>
