<template>
  <div class="doctor-dashboard">
    <div class="dashboard-header mb-4">
      <h2 class="dashboard-title">Doctor Dashboard</h2>
      <p class="dashboard-subtitle">Manage your appointments and provide patient care</p>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else>
      <div class="stats-grid mb-4">
        <div class="stat-card stat-card-primary">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
          </div>
          <div class="stat-content">
            <p class="stat-label">Today's Appointments</p>
            <h3 class="stat-value">{{ todayAppointments.length }}</h3>
            <span class="stat-change positive">Scheduled</span>
          </div>
        </div>

        <div class="stat-card stat-card-success">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path>
            </svg>
          </div>
          <div class="stat-content">
            <p class="stat-label">Upcoming</p>
            <h3 class="stat-value">{{ upcomingAppointments.length }}</h3>
            <span class="stat-change neutral">This Week</span>
          </div>
        </div>

        <div class="stat-card stat-card-warning">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div class="stat-content">
            <p class="stat-label">Completed</p>
            <h3 class="stat-value">{{ completedAppointments }}</h3>
            <span class="stat-change positive">Total</span>
          </div>
        </div>

        <div class="stat-card stat-card-info">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div class="stat-content">
            <p class="stat-label">Total Appointments</p>
            <h3 class="stat-value">{{ allAppointments.length }}</h3>
            <span class="stat-change neutral">All Time</span>
          </div>
        </div>
      </div>

      <div class="row g-4">
        <div class="col-lg-8">
          <div class="section-card">
            <div class="section-header">
              <h4 class="section-title">
                <svg class="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                Today's Appointments
              </h4>
            </div>
            <div class="section-body">
              <div v-if="todayAppointments.length === 0" class="empty-state">
                <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                <p class="empty-text">No appointments scheduled for today</p>
              </div>
              <div v-else class="appointments-list">
                <div v-for="apt in todayAppointments" :key="apt.id" class="appointment-card-modern">
                  <div class="appointment-header">
                    <div class="patient-info">
                      <div class="patient-avatar">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                        </svg>
                      </div>
                      <div class="patient-details">
                        <h6 class="patient-name">{{ apt.patient_name }}</h6>
                        <p class="patient-contact">{{ apt.patient_email }}</p>
                        <p class="patient-phone">{{ apt.patient_phone || 'N/A' }}</p>
                      </div>
                    </div>
                    <div class="appointment-time">
                      <div class="time-badge">
                        <svg class="time-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        <span>{{ formatTime(apt.appointment_time) }}</span>
                      </div>
                    </div>
                  </div>
                  <div class="appointment-footer">
                    <span class="status-badge" :class="getStatusBadgeClass(apt.status)">{{ apt.status }}</span>
                    <div class="action-buttons-group">
                      <button 
                        v-if="apt.status === 'BOOKED'"
                        class="action-button primary"
                        @click="openTreatmentModal(apt)"
                      >
                        <svg class="button-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        Complete Visit
                      </button>
                      <button 
                        v-if="apt.status === 'BOOKED'"
                        class="action-button danger"
                        @click="cancelAppointment(apt.id)"
                      >
                        <svg class="button-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                        Cancel
                      </button>
                      <button 
                        v-if="apt.treatment"
                        class="action-button secondary"
                        @click="viewTreatment(apt)"
                      >
                        <svg class="button-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                        </svg>
                        View Treatment
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div id="appointments-section" class="section-card mt-4">
            <div class="section-header">
              <h4 class="section-title">
                <svg class="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                </svg>
                All Appointments
              </h4>
            </div>
            
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
            
            <div class="section-body">
              <div v-if="allAppointments.length === 0" class="empty-state">
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
                    <tr v-for="apt in allAppointments" :key="apt.id">
                      <td>
                        <div class="table-patient">
                          <strong>{{ apt.patient_name }}</strong>
                          <span class="table-email">{{ apt.patient_email }}</span>
                        </div>
                      </td>
                      <td>{{ formatDate(apt.appointment_date) }}</td>
                      <td>{{ formatTime(apt.appointment_time) }}</td>
                      <td>
                        <span class="status-badge-small" :class="getStatusBadgeClass(apt.status)">
                          {{ apt.status }}
                        </span>
                      </td>
                      <td>
                        <div class="table-actions">
                          <button 
                            v-if="apt.status === 'BOOKED'"
                            class="table-btn success"
                            @click="openTreatmentModal(apt)"
                            title="Add Treatment"
                          >
                            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                            </svg>
                          </button>
                          <button 
                            v-if="apt.status === 'BOOKED'"
                            class="table-btn danger"
                            @click="cancelAppointment(apt.id)"
                            title="Cancel Appointment"
                          >
                            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                          </button>
                          <button 
                            v-if="apt.treatment"
                            class="table-btn info"
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
        </div>

        <div class="col-lg-4">
          <div id="availability-section" class="section-card">
            <div class="section-header">
              <h4 class="section-title">
                <svg class="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                Set Availability
              </h4>
            </div>
            <div class="section-body">
              <div class="form-group">
                <label class="form-label">Date</label>
                <input 
                  type="date" 
                  class="form-input" 
                  v-model="availabilityDate" 
                  :min="minDate"
                />
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">Start Time</label>
                  <input 
                    type="time" 
                    class="form-input" 
                    v-model="availabilityStart"
                  />
                </div>
                <div class="form-group">
                  <label class="form-label">End Time</label>
                  <input 
                    type="time" 
                    class="form-input" 
                    v-model="availabilityEnd"
                  />
                </div>
              </div>
              <button 
                class="submit-button" 
                @click="setAvailability" 
                :disabled="!availabilityDate || !availabilityStart || !availabilityEnd"
              >
                <svg class="button-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                </svg>
                Add Availability
              </button>
              <div v-if="availabilityMessage" class="message-alert" :class="availabilityMessage.includes('successfully') ? 'success' : 'error'">
                {{ availabilityMessage }}
              </div>
            </div>
          </div>

          <div class="section-card mt-4">
            <div class="section-header">
              <h4 class="section-title">
                <svg class="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                </svg>
                Upcoming This Week
              </h4>
            </div>
            <div class="section-body">
              <div v-if="upcomingAppointments.length === 0" class="empty-state-small">
                <p class="empty-text-small">No upcoming appointments</p>
              </div>
              <div v-else class="upcoming-list">
                <div v-for="apt in upcomingAppointments.slice(0, 5)" :key="apt.id" class="upcoming-item">
                  <div class="upcoming-date">
                    <span class="date-day">{{ getDayName(apt.appointment_date) }}</span>
                    <span class="date-full">{{ formatDate(apt.appointment_date) }}</span>
                  </div>
                  <div class="upcoming-details">
                    <strong>{{ apt.patient_name }}</strong>
                    <span class="upcoming-time">{{ formatTime(apt.appointment_time) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showTreatmentModal" class="modal-overlay" @click.self="closeTreatmentModal">
      <div class="modal-container">
        <div class="modal-header-modern">
          <h5 class="modal-title-modern">
            <svg class="modal-title-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            Treatment Record
          </h5>
          <button type="button" class="modal-close" @click="closeTreatmentModal">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        <div class="modal-body-modern">
          <div class="patient-badge">
            <svg class="patient-badge-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
            <div>
              <strong>{{ selectedAppointment?.patient_name }}</strong>
              <span>{{ selectedAppointment?.patient_email }}</span>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Diagnosis <span class="required">*</span></label>
            <textarea 
              class="form-textarea" 
              v-model="treatmentData.diagnosis" 
              rows="4" 
              placeholder="Enter patient diagnosis..."
              required
            ></textarea>
          </div>
          <div class="form-group">
            <label class="form-label">Prescription</label>
            <textarea 
              class="form-textarea" 
              v-model="treatmentData.prescription" 
              rows="4"
              placeholder="Enter prescribed medications..."
            ></textarea>
          </div>
          <div class="form-group">
            <label class="form-label">Clinical Notes</label>
            <textarea 
              class="form-textarea" 
              v-model="treatmentData.notes" 
              rows="3"
              placeholder="Additional notes or observations..."
            ></textarea>
          </div>
          <div class="form-group">
            <label class="form-label">Next Visit (Optional)</label>
            <input 
              type="date" 
              class="form-input" 
              v-model="treatmentData.next_visit" 
              :min="minDate"
            />
          </div>
        </div>
        <div class="modal-footer-modern">
          <button type="button" class="modal-button secondary" @click="closeTreatmentModal">
            Cancel
          </button>
          <button 
            type="button" 
            class="modal-button primary" 
            @click="saveTreatment" 
            :disabled="!treatmentData.diagnosis || saving"
          >
            <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
            {{ saving ? 'Saving...' : 'Save Treatment' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick, watch } from "vue";
import { useRoute } from "vue-router";
import auth from "../../utils/auth";

const route = useRoute();

const loading = ref(false);
const appointments = ref([]);
const availabilityDate = ref("");
const availabilityStart = ref("");
const availabilityEnd = ref("");
const availabilityMessage = ref("");
const showTreatmentModal = ref(false);
const selectedAppointment = ref(null);
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

const minDate = new Date().toISOString().split('T')[0];

const todayAppointments = computed(() => {
  const today = new Date().toISOString().split('T')[0];
  return appointments.value.filter(apt => apt.appointment_date === today && apt.status === "BOOKED");
});

const upcomingAppointments = computed(() => {
  const today = new Date().toISOString().split('T')[0];
  return appointments.value.filter(apt => apt.appointment_date > today && apt.status === "BOOKED");
});

const allAppointments = computed(() => {
  return appointments.value;
});

const completedAppointments = computed(() => {
  return appointments.value.filter(apt => apt.status === "COMPLETED").length;
});

const formatTime = (timeStr) => {
  if (!timeStr) return "N/A";
  const [hours, minutes] = timeStr.split(":");
  const hour = parseInt(hours);
  const ampm = hour >= 12 ? "PM" : "AM";
  const displayHour = hour % 12 || 12;
  return `${displayHour}:${minutes} ${ampm}`;
};

const formatDate = (dateStr) => {
  if (!dateStr) return "N/A";
  const date = new Date(dateStr);
  return date.toLocaleDateString("en-US", { 
    month: "short", 
    day: "numeric", 
    year: "numeric" 
  });
};

const getDayName = (dateStr) => {
  if (!dateStr) return "";
  const date = new Date(dateStr);
  return date.toLocaleDateString("en-US", { weekday: "short" });
};

const getToken = () => auth.getToken();

const loadAppointments = async () => {
  loading.value = true;
  try {
    // Build query string with filters
    const params = new URLSearchParams();
    if (filterStartDate.value) params.append('start_date', filterStartDate.value);
    if (filterEndDate.value) params.append('end_date', filterEndDate.value);
    if (filterStatus.value) params.append('status', filterStatus.value);
    
    const queryString = params.toString();
    const url = `http://localhost:5000/api/doctor/appointments${queryString ? '?' + queryString : ''}`;
    
    const response = await fetch(url, {
      headers: { Authorization: `Bearer ${getToken()}` }
    });
    const data = await response.json();
    appointments.value = data.appointments || [];
  } catch (error) {
    console.error("Failed to load appointments:", error);
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

const setAvailability = async () => {
  if (!availabilityDate.value || !availabilityStart.value || !availabilityEnd.value) {
    alert("Please fill all fields");
    return;
  }

  try {
    const response = await fetch("http://localhost:5000/api/doctor/availability", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getToken()}`
      },
      body: JSON.stringify({
        date: availabilityDate.value,
        start_time: availabilityStart.value,
        end_time: availabilityEnd.value
      })
    });

    const data = await response.json();
    if (response.ok) {
      availabilityMessage.value = "Availability added successfully!";
      availabilityDate.value = "";
      availabilityStart.value = "";
      availabilityEnd.value = "";
      setTimeout(() => availabilityMessage.value = "", 3000);
    } else {
      availabilityMessage.value = data.message || "Failed to add availability";
    }
  } catch (error) {
    availabilityMessage.value = "Error adding availability";
  }
};

const openTreatmentModal = (appointment) => {
  selectedAppointment.value = appointment;
  treatmentData.value = {
    diagnosis: appointment.treatment?.diagnosis || "",
    prescription: appointment.treatment?.prescription || "",
    notes: appointment.treatment?.notes || "",
    next_visit: appointment.treatment?.next_visit || ""
  };
  showTreatmentModal.value = true;
};

const closeTreatmentModal = () => {
  showTreatmentModal.value = false;
  selectedAppointment.value = null;
  treatmentData.value = {
    diagnosis: "",
    prescription: "",
    notes: "",
    next_visit: ""
  };
};

const saveTreatment = async () => {
  if (!treatmentData.value.diagnosis) {
    return;
  }

  saving.value = true;
  try {
    const response = await fetch(`http://localhost:5000/api/doctor/appointments/${selectedAppointment.value.id}/treatment`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getToken()}`
      },
      body: JSON.stringify(treatmentData.value)
    });

    const data = await response.json();
    if (response.ok) {
      closeTreatmentModal();
      loadAppointments();
    } else {
      alert(data.message || "Failed to save treatment");
    }
  } catch (error) {
    alert("Error saving treatment");
  } finally {
    saving.value = false;
  }
};

const viewTreatment = (appointment) => {
  if (appointment.treatment) {
    selectedAppointment.value = appointment;
    treatmentData.value = {
      diagnosis: appointment.treatment.diagnosis || "",
      prescription: appointment.treatment.prescription || "",
      notes: appointment.treatment.notes || "",
      next_visit: appointment.treatment.next_visit || ""
    };
    showTreatmentModal.value = true;
  }
};

const getStatusBadgeClass = (status) => {
  const classes = {
    "BOOKED": "status-booked",
    "COMPLETED": "status-completed",
    "CANCELLED": "status-cancelled"
  };
  return classes[status] || "status-default";
};

const cancelAppointment = async (appointmentId) => {
  if (!confirm("Are you sure you want to cancel this appointment?")) {
    return;
  }
  
  try {
    const response = await fetch(`http://localhost:5000/api/appointments/${appointmentId}/cancel`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${getToken()}`
      }
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

onMounted(async () => {
  await loadAppointments();
  
  // Check if we need to scroll to a specific section
  await nextTick();
  scrollToSection(route.query.section);
});

// Watch for route query changes to handle in-page navigation
watch(() => route.query.section, async (newSection) => {
  if (newSection) {
    await nextTick();
    scrollToSection(newSection);
  }
});

// Helper function to scroll to section
const scrollToSection = (section) => {
  if (section === 'availability') {
    const availabilityElement = document.getElementById('availability-section');
    if (availabilityElement) {
      availabilityElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
      availabilityElement.classList.add('highlight-section');
      setTimeout(() => {
        availabilityElement.classList.remove('highlight-section');
      }, 2000);
    }
  } else if (section === 'appointments') {
    const appointmentsElement = document.getElementById('appointments-section');
    if (appointmentsElement) {
      appointmentsElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
      appointmentsElement.classList.add('highlight-section');
      setTimeout(() => {
        appointmentsElement.classList.remove('highlight-section');
      }, 2000);
    }
  }
};
</script>

<style scoped>
.doctor-dashboard {
  padding: 0;
}

/* Filter Section Styles */
.filter-section {
  padding: 1rem 1.5rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
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

.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.dashboard-subtitle {
  color: #64748b;
  font-size: 1rem;
  margin: 0;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 1.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  display: flex;
  align-items: flex-start;
  gap: 1.25rem;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, transparent, currentColor, transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.stat-card:hover::before {
  opacity: 1;
}

.stat-card-primary {
  border-left: 4px solid #3b82f6;
}

.stat-card-primary .stat-icon-wrapper {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.stat-card-success {
  border-left: 4px solid #10b981;
}

.stat-card-success .stat-icon-wrapper {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.stat-card-warning {
  border-left: 4px solid #f59e0b;
}

.stat-card-warning .stat-icon-wrapper {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.stat-card-info {
  border-left: 4px solid #06b6d4;
}

.stat-card-info .stat-icon-wrapper {
  background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
  color: white;
}

.stat-icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon {
  width: 28px;
  height: 28px;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.stat-value {
  font-size: 2.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  line-height: 1.2;
}

.stat-change {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
}

.stat-change.positive {
  background: #d1fae5;
  color: #065f46;
}

.stat-change.neutral {
  background: #fef3c7;
  color: #92400e;
}

.section-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
}

.section-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.section-card.highlight-section {
  animation: highlightPulse 0.5s ease-in-out 3;
  box-shadow: 0 0 0 4px rgba(94, 99, 182, 0.4);
}

@keyframes highlightPulse {
  0%, 100% { box-shadow: 0 0 0 4px rgba(94, 99, 182, 0.4); }
  50% { box-shadow: 0 0 0 8px rgba(94, 99, 182, 0.2); }
}

.section-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.section-icon {
  width: 24px;
  height: 24px;
  color: #5e63b6;
}

.section-body {
  padding: 1.5rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
}

.empty-icon {
  width: 64px;
  height: 64px;
  color: #cbd5e1;
  margin: 0 auto 1rem;
}

.empty-text {
  color: #64748b;
  font-size: 1rem;
  margin: 0;
}

.empty-state-small {
  text-align: center;
  padding: 2rem 1rem;
}

.empty-text-small {
  color: #94a3b8;
  font-size: 0.875rem;
  margin: 0;
}

.appointments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 400px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

/* Custom scrollbar for appointments list */
.appointments-list::-webkit-scrollbar {
  width: 6px;
}

.appointments-list::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.appointments-list::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.appointments-list::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.appointment-card-modern {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.25rem;
  transition: all 0.2s ease;
}

.appointment-card-modern:hover {
  border-color: #5e63b6;
  box-shadow: 0 4px 12px rgba(94, 99, 182, 0.1);
  transform: translateY(-2px);
}

.appointment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.patient-info {
  display: flex;
  gap: 1rem;
  flex: 1;
}

.patient-avatar {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #5e63b6, #4a50a0);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.patient-avatar svg {
  width: 24px;
  height: 24px;
}

.patient-details {
  flex: 1;
}

.patient-name {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
}

.patient-contact {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0 0 0.25rem 0;
}

.patient-phone {
  font-size: 0.875rem;
  color: #94a3b8;
  margin: 0;
}

.appointment-time {
  flex-shrink: 0;
}

.time-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-weight: 600;
  color: #1e293b;
}

.time-icon {
  width: 16px;
  height: 16px;
  color: #5e63b6;
}

.appointment-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.status-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge.status-booked {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.status-completed {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.status-cancelled {
  background: #fee2e2;
  color: #991b1b;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-button.primary {
  background: #10b981;
  color: white;
}

.action-button.primary:hover {
  background: #059669;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.action-button.secondary {
  background: #3b82f6;
  color: white;
}

.action-button.secondary:hover {
  background: #2563eb;
}

.action-button.danger {
  background: #ef4444;
  color: white;
}

.action-button.danger:hover {
  background: #dc2626;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.action-buttons-group {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.button-icon {
  width: 16px;
  height: 16px;
}

.appointments-table-wrapper {
  overflow-x: auto;
  max-height: 450px;
  overflow-y: auto;
}

/* Custom scrollbar for table wrapper */
.appointments-table-wrapper::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.appointments-table-wrapper::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.appointments-table-wrapper::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.appointments-table-wrapper::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.appointments-table {
  width: 100%;
  border-collapse: collapse;
}

.appointments-table thead {
  background: #f8fafc;
  position: sticky;
  top: 0;
  z-index: 1;
}

.appointments-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #1e293b;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #e2e8f0;
  background: #f8fafc;
}

.appointments-table td {
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
  color: #475569;
}

.appointments-table tbody tr:hover {
  background: #f8fafc;
}

.table-patient {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.table-email {
  font-size: 0.875rem;
  color: #94a3b8;
}

.status-badge-small {
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge-small.status-booked {
  background: #fef3c7;
  color: #92400e;
}

.status-badge-small.status-completed {
  background: #d1fae5;
  color: #065f46;
}

.status-badge-small.status-cancelled {
  background: #fee2e2;
  color: #991b1b;
}

.table-actions {
  display: flex;
  gap: 0.5rem;
}

.table-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.table-btn svg {
  width: 16px;
  height: 16px;
}

.table-btn.success {
  background: #d1fae5;
  color: #065f46;
}

.table-btn.success:hover {
  background: #10b981;
  color: white;
}

.table-btn.info {
  background: #dbeafe;
  color: #1e40af;
}

.table-btn.info:hover {
  background: #3b82f6;
  color: white;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-label {
  display: block;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.form-label .required {
  color: #ef4444;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.9375rem;
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #5e63b6;
  box-shadow: 0 0 0 3px rgba(94, 99, 182, 0.1);
}

.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-family: inherit;
  resize: vertical;
  transition: all 0.2s ease;
}

.form-textarea:focus {
  outline: none;
  border-color: #5e63b6;
  box-shadow: 0 0 0 3px rgba(94, 99, 182, 0.1);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.submit-button {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem;
  background: #5e63b6;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-button:hover:not(:disabled) {
  background: #4a50a0;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(94, 99, 182, 0.3);
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.message-alert {
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.875rem;
  margin-top: 1rem;
}

.message-alert.success {
  background: #d1fae5;
  color: #065f46;
  border: 1px solid #10b981;
}

.message-alert.error {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #ef4444;
}

.upcoming-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 280px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

/* Custom scrollbar for upcoming list */
.upcoming-list::-webkit-scrollbar {
  width: 5px;
}

.upcoming-list::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.upcoming-list::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.upcoming-list::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.upcoming-item {
  display: flex;
  gap: 1rem;
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.upcoming-item:hover {
  background: #f1f5f9;
}

.upcoming-date {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 60px;
  padding: 0.5rem;
  background: white;
  border-radius: 8px;
}

.date-day {
  font-size: 0.75rem;
  font-weight: 600;
  color: #5e63b6;
  text-transform: uppercase;
}

.date-full {
  font-size: 0.875rem;
  font-weight: 700;
  color: #1e293b;
}

.upcoming-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.upcoming-details strong {
  color: #1e293b;
  font-size: 0.9375rem;
}

.upcoming-time {
  font-size: 0.875rem;
  color: #64748b;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-container {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header-modern {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-title-modern {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.modal-title-icon {
  width: 24px;
  height: 24px;
  color: #5e63b6;
}

.modal-close {
  width: 32px;
  height: 32px;
  border: none;
  background: #f1f5f9;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.modal-close:hover {
  background: #e2e8f0;
}

.modal-close svg {
  width: 20px;
  height: 20px;
  color: #64748b;
}

.modal-body-modern {
  padding: 1.5rem;
}

.patient-badge {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.patient-badge-icon {
  width: 40px;
  height: 40px;
  color: #5e63b6;
}

.patient-badge div {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.patient-badge strong {
  color: #1e293b;
  font-size: 1rem;
}

.patient-badge span {
  color: #64748b;
  font-size: 0.875rem;
}

.modal-footer-modern {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1.5rem;
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
}

.modal-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.modal-button.secondary {
  background: white;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.modal-button.secondary:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.modal-button.primary {
  background: #5e63b6;
  color: white;
}

.modal-button.primary:hover:not(:disabled) {
  background: #4a50a0;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(94, 99, 182, 0.3);
}

.modal-button.primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .dashboard-title {
    font-size: 1.5rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .appointment-header {
    flex-direction: column;
    gap: 1rem;
  }

  .appointment-footer {
    flex-direction: column;
    gap: 0.75rem;
    align-items: stretch;
  }

  .action-button {
    width: 100%;
    justify-content: center;
  }
}
</style>
