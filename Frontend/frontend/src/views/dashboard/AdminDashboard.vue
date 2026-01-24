<template>
  <div class="dashboard-container">
    <!-- Hero Header -->
    <div class="dashboard-hero">
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">Dashboard Overview</h1>
          <p class="hero-subtitle">Monitor your hospital management system at a glance</p>
        </div>
        <div class="hero-date">
          <svg class="date-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
          </svg>
          <span>{{ currentDate }}</span>
        </div>
      </div>
      <div class="hero-pattern"></div>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner">
        <div class="spinner-ring"></div>
        <span class="loading-text">Loading dashboard...</span>
      </div>
    </div>

    <div v-else>
      <!-- Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card" :class="{ 'animate-in': !loading }" style="--delay: 0.1s">
          <div class="stat-glow stat-glow-blue"></div>
          <div class="stat-icon-wrapper stat-icon-blue">
            <svg class="stat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
          </div>
          <div class="stat-content">
            <p class="stat-label">Total Patients</p>
            <h3 class="stat-value">{{ PatientCount }}</h3>
            <div class="stat-footer">
              <span class="stat-badge stat-badge-blue">
                <svg class="badge-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Active
              </span>
            </div>
          </div>
        </div>

        <div class="stat-card" :class="{ 'animate-in': !loading }" style="--delay: 0.2s">
          <div class="stat-glow stat-glow-emerald"></div>
          <div class="stat-icon-wrapper stat-icon-emerald">
            <svg class="stat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div class="stat-content">
            <p class="stat-label">Total Doctors</p>
            <h3 class="stat-value">{{ doctorCount }}</h3>
            <div class="stat-footer">
              <span class="stat-badge stat-badge-emerald">
                <svg class="badge-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Available
              </span>
            </div>
          </div>
        </div>

        <div class="stat-card" :class="{ 'animate-in': !loading }" style="--delay: 0.3s">
          <div class="stat-glow stat-glow-amber"></div>
          <div class="stat-icon-wrapper stat-icon-amber">
            <svg class="stat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div class="stat-content">
            <p class="stat-label">Upcoming</p>
            <h3 class="stat-value">{{ upcomingAppointmentsCount }}</h3>
            <div class="stat-footer">
              <span class="stat-badge stat-badge-amber">
                <svg class="badge-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                Scheduled
              </span>
            </div>
          </div>
        </div>

        <div class="stat-card" :class="{ 'animate-in': !loading }" style="--delay: 0.4s">
          <div class="stat-glow stat-glow-purple"></div>
          <div class="stat-icon-wrapper stat-icon-purple">
            <svg class="stat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div class="stat-content">
            <p class="stat-label">Completed</p>
            <h3 class="stat-value">{{ completedAppointmentsCount }}</h3>
            <div class="stat-footer">
              <span class="stat-badge stat-badge-purple">
                <svg class="badge-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Treatments
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Appointments Sections -->
      <div class="appointments-sections">
        <div class="section-header-main">
          <h2 class="section-main-title">Appointment Overview</h2>
          <p class="section-main-subtitle">Track and manage all appointments</p>
        </div>
        
        <div class="row g-4">
          <!-- Upcoming Appointments -->
          <div class="col-lg-4">
            <div class="section-card section-card-upcoming">
              <div class="card-accent"></div>
              <div class="section-header">
                <div class="header-left">
                  <div class="header-icon-wrapper upcoming">
                    <svg class="header-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                  </div>
                  <h4 class="section-title">Upcoming</h4>
                </div>
                <span class="badge-count upcoming">{{ upcomingAppointments.length }}</span>
              </div>
              <div class="section-body">
                <div v-if="upcomingAppointments.length === 0" class="empty-state">
                  <div class="empty-icon-wrapper">
                    <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                  </div>
                  <p class="empty-text">No upcoming appointments</p>
                </div>
                <div v-else class="appointments-scroll">
                  <div v-for="apt in upcomingAppointments.slice(0, 5)" :key="apt.id" class="mini-appointment-card">
                    <div class="mini-card-accent upcoming"></div>
                    <div class="mini-card-content">
                      <div class="mini-apt-header">
                        <span class="patient-name">{{ apt.patient_name }}</span>
                        <span class="status-indicator upcoming">
                          <span class="status-pulse"></span>
                        </span>
                      </div>
                      <div class="mini-apt-details">
                        <span class="doctor-info">
                          <svg class="detail-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                          </svg>
                          Dr. {{ apt.doctor_name }}
                        </span>
                        <span class="apt-datetime">{{ formatDate(apt.appointment_date) }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Latest/Recent Appointments -->
          <div class="col-lg-4">
            <div class="section-card section-card-recent">
              <div class="card-accent recent"></div>
              <div class="section-header">
                <div class="header-left">
                  <div class="header-icon-wrapper recent">
                    <svg class="header-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </div>
                  <h4 class="section-title">Latest Booked</h4>
                </div>
                <span class="badge-count recent">{{ latestAppointments.length }}</span>
              </div>
              <div class="section-body">
                <div v-if="latestAppointments.length === 0" class="empty-state">
                  <div class="empty-icon-wrapper">
                    <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </div>
                  <p class="empty-text">No recent appointments</p>
                </div>
                <div v-else class="appointments-scroll">
                  <div v-for="apt in latestAppointments.slice(0, 5)" :key="apt.id" class="mini-appointment-card">
                    <div class="mini-card-accent recent"></div>
                    <div class="mini-card-content">
                      <div class="mini-apt-header">
                        <span class="patient-name">{{ apt.patient_name }}</span>
                        <span class="status-indicator recent">
                          <span class="status-pulse"></span>
                        </span>
                      </div>
                      <div class="mini-apt-details">
                        <span class="doctor-info">
                          <svg class="detail-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                          </svg>
                          Dr. {{ apt.doctor_name }}
                        </span>
                        <span class="apt-datetime">{{ formatDate(apt.appointment_date) }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Completed Appointments -->
          <div class="col-lg-4">
            <div class="section-card section-card-completed">
              <div class="card-accent completed"></div>
              <div class="section-header">
                <div class="header-left">
                  <div class="header-icon-wrapper completed">
                    <svg class="header-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </div>
                  <h4 class="section-title">Completed</h4>
                </div>
                <span class="badge-count completed">{{ completedAppointments.length }}</span>
              </div>
              <div class="section-body">
                <div v-if="completedAppointments.length === 0" class="empty-state">
                  <div class="empty-icon-wrapper">
                    <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </div>
                  <p class="empty-text">No completed appointments</p>
                </div>
                <div v-else class="appointments-scroll">
                  <div v-for="apt in completedAppointments.slice(0, 5)" :key="apt.id" class="mini-appointment-card">
                    <div class="mini-card-accent completed"></div>
                    <div class="mini-card-content">
                      <div class="mini-apt-header">
                        <span class="patient-name">{{ apt.patient_name }}</span>
                        <span class="status-indicator completed">
                          <svg class="check-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                          </svg>
                        </span>
                      </div>
                      <div class="mini-apt-details">
                        <span class="doctor-info">
                          <svg class="detail-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                          </svg>
                          Dr. {{ apt.doctor_name }}
                        </span>
                        <span class="apt-datetime">{{ formatDate(apt.appointment_date) }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="quick-actions">
        <div class="section-header-main">
          <h2 class="section-main-title">Quick Actions</h2>
          <p class="section-main-subtitle">Common tasks and shortcuts</p>
        </div>
        <div class="actions-grid">
          <button class="action-card" @click="$router.push('/admin/add-doctor')">
            <div class="action-icon-wrapper action-icon-add">
              <svg class="action-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
              </svg>
            </div>
            <div class="action-content">
              <span class="action-title">Add New Doctor</span>
              <span class="action-desc">Register a new physician</span>
            </div>
            <svg class="action-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>

          <button class="action-card" @click="$router.push('/admin/doctor-list')">
            <div class="action-icon-wrapper action-icon-doctors">
              <svg class="action-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
            </div>
            <div class="action-content">
              <span class="action-title">View All Doctors</span>
              <span class="action-desc">Manage physician records</span>
            </div>
            <svg class="action-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>

          <button class="action-card" @click="$router.push('/admin/patient-list')">
            <div class="action-icon-wrapper action-icon-patients">
              <svg class="action-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
              </svg>
            </div>
            <div class="action-content">
              <span class="action-title">View All Patients</span>
              <span class="action-desc">Browse patient database</span>
            </div>
            <svg class="action-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>

          <button class="action-card" @click="$router.push('/admin/appointments')">
            <div class="action-icon-wrapper action-icon-appointments">
              <svg class="action-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
            </div>
            <div class="action-content">
              <span class="action-title">All Appointments</span>
              <span class="action-desc">View complete schedule</span>
            </div>
            <svg class="action-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import auth from "../../utils/auth";

const router = useRouter();
const doctorCount = ref(0);
const PatientCount = ref(0);
const upcomingAppointmentsCount = ref(0);
const completedAppointmentsCount = ref(0);
const totalAppointments = ref(0);
const loading = ref(true);
const allAppointments = ref([]);

const currentDate = computed(() => {
  return new Date().toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
});

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
};

const upcomingAppointments = computed(() => {
  const today = new Date().toISOString().split('T')[0];
  return allAppointments.value.filter(apt => 
    apt.appointment_date >= today && apt.status === "BOOKED"
  );
});

const latestAppointments = computed(() => {
  return [...allAppointments.value]
    .filter(apt => apt.status === "BOOKED")
    .sort((a, b) => new Date(b.created_at || b.appointment_date) - new Date(a.created_at || a.appointment_date))
    .slice(0, 10);
});

const completedAppointments = computed(() => {
  return allAppointments.value.filter(apt => apt.status === "COMPLETED");
});

onMounted(async () => {
  const token = auth.getToken();

  try {
    const [doctorsRes, patientsRes, appointmentsRes, allAppointmentsRes] = await Promise.all([
      fetch("http://localhost:5000/api/admin/doctors/count", {
        headers: { Authorization: `Bearer ${token}` },
      }),
      fetch("http://localhost:5000/api/admin/patients/count", {
        headers: { Authorization: `Bearer ${token}` },
      }),
      fetch("http://localhost:5000/api/admin/appointments/count", {
        headers: { Authorization: `Bearer ${token}` },
      }),
      fetch("http://localhost:5000/api/admin/appointments", {
        headers: { Authorization: `Bearer ${token}` },
      }),
    ]);

    if (doctorsRes.ok) {
      const data = await doctorsRes.json();
      doctorCount.value = data.total_doctors;
    }

    if (patientsRes.ok) {
      const data = await patientsRes.json();
      PatientCount.value = data.total_patients;
    }

    if (appointmentsRes.ok) {
      const data = await appointmentsRes.json();
      totalAppointments.value = data.total_appointments || 0;
      upcomingAppointmentsCount.value = data.booked || 0;
      completedAppointmentsCount.value = data.completed || 0;
    }

    if (allAppointmentsRes.ok) {
      const data = await allAppointmentsRes.json();
      allAppointments.value = data.appointments || [];
    }
  } catch (error) {
    console.error("Failed to fetch dashboard data:", error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.dashboard-container {
  padding: 0;
  min-height: 100vh;
}

/* Hero Header */
.dashboard-hero {
  background: linear-gradient(135deg, #5e63b6 0%, #4a50a0 50%, #3d4195 100%);
  border-radius: 20px;
  padding: 2rem 2.5rem;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(94, 99, 182, 0.3);
}

.hero-pattern {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 40%;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.5;
}

.hero-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 1;
}

.hero-title {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin: 0 0 0.5rem 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.hero-subtitle {
  color: rgba(255, 255, 255, 0.85);
  font-size: 1rem;
  margin: 0;
}

.hero-date {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  padding: 0.75rem 1.25rem;
  border-radius: 12px;
  color: white;
  font-weight: 500;
}

.date-icon {
  width: 18px;
  height: 18px;
}

/* Loading State */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.spinner-ring {
  width: 48px;
  height: 48px;
  border: 3px solid #e2e8f0;
  border-top-color: #5e63b6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  color: #64748b;
  font-weight: 500;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.stat-card {
  background: white;
  border-radius: 20px;
  padding: 1.75rem;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: flex-start;
  gap: 1.25rem;
  opacity: 0;
  transform: translateY(20px);
}

.stat-card.animate-in {
  animation: slideUp 0.6s ease forwards;
  animation-delay: var(--delay, 0s);
}

@keyframes slideUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stat-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
}

.stat-glow {
  position: absolute;
  top: -50%;
  right: -50%;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  opacity: 0.1;
  transition: opacity 0.3s ease;
}

.stat-card:hover .stat-glow {
  opacity: 0.15;
}

.stat-glow-blue { background: radial-gradient(circle, #3b82f6 0%, transparent 70%); }
.stat-glow-emerald { background: radial-gradient(circle, #10b981 0%, transparent 70%); }
.stat-glow-amber { background: radial-gradient(circle, #f59e0b 0%, transparent 70%); }
.stat-glow-purple { background: radial-gradient(circle, #8b5cf6 0%, transparent 70%); }

.stat-icon-wrapper {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: transform 0.3s ease;
}

.stat-card:hover .stat-icon-wrapper {
  transform: scale(1.1) rotate(5deg);
}

.stat-icon-blue {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
}

.stat-icon-emerald {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
}

.stat-icon-amber {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  box-shadow: 0 8px 20px rgba(245, 158, 11, 0.3);
}

.stat-icon-purple {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  box-shadow: 0 8px 20px rgba(139, 92, 246, 0.3);
}

.stat-icon {
  width: 28px;
  height: 28px;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 0.85rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
  line-height: 1.1;
}

.stat-footer {
  margin-top: 0.75rem;
}

.stat-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
}

.badge-icon {
  width: 12px;
  height: 12px;
}

.stat-badge-blue { background: #dbeafe; color: #1d4ed8; }
.stat-badge-emerald { background: #d1fae5; color: #047857; }
.stat-badge-amber { background: #fef3c7; color: #b45309; }
.stat-badge-purple { background: #ede9fe; color: #6d28d9; }

/* Section Headers */
.section-header-main {
  margin-bottom: 1.5rem;
}

.section-main-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
}

.section-main-subtitle {
  color: #64748b;
  margin: 0;
  font-size: 0.95rem;
}

/* Appointments Sections */
.appointments-sections {
  margin-bottom: 2.5rem;
}

.section-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  height: 100%;
  transition: all 0.3s ease;
  position: relative;
}

.section-card:hover {
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
  transform: translateY(-4px);
}

.card-accent {
  height: 4px;
  width: 100%;
}

.card-accent.upcoming, .section-card-upcoming .card-accent { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.card-accent.recent, .section-card-recent .card-accent { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
.card-accent.completed, .section-card-completed .card-accent { background: linear-gradient(90deg, #10b981, #34d399); }

.section-header {
  padding: 1.25rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #f1f5f9;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-icon-wrapper {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-icon-wrapper.upcoming { background: #fef3c7; color: #d97706; }
.header-icon-wrapper.recent { background: #dbeafe; color: #2563eb; }
.header-icon-wrapper.completed { background: #d1fae5; color: #059669; }

.header-icon {
  width: 20px;
  height: 20px;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.badge-count {
  font-size: 0.85rem;
  font-weight: 700;
  padding: 0.35rem 0.9rem;
  border-radius: 20px;
}

.badge-count.upcoming { background: #fef3c7; color: #b45309; }
.badge-count.recent { background: #dbeafe; color: #1d4ed8; }
.badge-count.completed { background: #d1fae5; color: #047857; }

.section-body {
  padding: 1rem;
  max-height: 320px;
  overflow-y: auto;
}

.section-body::-webkit-scrollbar {
  width: 6px;
}

.section-body::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.section-body::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.appointments-scroll {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.mini-appointment-card {
  background: #f8fafc;
  border-radius: 14px;
  overflow: hidden;
  display: flex;
  transition: all 0.25s ease;
}

.mini-appointment-card:hover {
  background: #f1f5f9;
  transform: translateX(4px);
}

.mini-card-accent {
  width: 4px;
  flex-shrink: 0;
}

.mini-card-accent.upcoming { background: #f59e0b; }
.mini-card-accent.recent { background: #3b82f6; }
.mini-card-accent.completed { background: #10b981; }

.mini-card-content {
  padding: 1rem;
  flex: 1;
}

.mini-apt-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.patient-name {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.95rem;
}

.status-indicator {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.status-indicator.upcoming { background: rgba(245, 158, 11, 0.2); }
.status-indicator.recent { background: rgba(59, 130, 246, 0.2); }
.status-indicator.completed { background: rgba(16, 185, 129, 0.2); }

.status-pulse {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.status-indicator.upcoming .status-pulse { background: #f59e0b; }
.status-indicator.recent .status-pulse { background: #3b82f6; }

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}

.check-icon {
  width: 12px;
  height: 12px;
  color: #10b981;
}

.mini-apt-details {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.85rem;
  color: #64748b;
}

.doctor-info {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-weight: 500;
  color: #475569;
}

.detail-icon {
  width: 14px;
  height: 14px;
  color: #94a3b8;
}

.apt-datetime {
  font-weight: 600;
  color: #94a3b8;
  background: white;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  font-size: 0.8rem;
}

.empty-state {
  text-align: center;
  padding: 2.5rem 1rem;
}

.empty-icon-wrapper {
  width: 56px;
  height: 56px;
  background: #f1f5f9;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}

.empty-icon {
  width: 28px;
  height: 28px;
  color: #94a3b8;
}

.empty-text {
  color: #94a3b8;
  font-size: 0.95rem;
  margin: 0;
  font-weight: 500;
}

/* Quick Actions */
.quick-actions {
  margin-top: 1rem;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
}

.action-card {
  background: white;
  border: none;
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  text-align: left;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(94, 99, 182, 0.15);
}

.action-card:hover .action-arrow {
  transform: translateX(4px);
  color: #5e63b6;
}

.action-card:hover .action-icon-wrapper {
  transform: scale(1.1);
}

.action-icon-wrapper {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: transform 0.3s ease;
}

.action-icon-add {
  background: linear-gradient(135deg, #5e63b6 0%, #4a50a0 100%);
  color: white;
}

.action-icon-doctors {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.action-icon-patients {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.action-icon-appointments {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.action-icon {
  width: 24px;
  height: 24px;
}

.action-content {
  flex: 1;
}

.action-title {
  display: block;
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.action-desc {
  display: block;
  font-size: 0.85rem;
  color: #64748b;
}

.action-arrow {
  width: 20px;
  height: 20px;
  color: #cbd5e1;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

/* Responsive */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .dashboard-hero {
    padding: 1.5rem;
  }
  
  .hero-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .hero-title {
    font-size: 1.5rem;
  }
  
  .stat-value {
    font-size: 2rem;
  }
  
  .section-body {
    max-height: 250px;
  }
}
</style>
