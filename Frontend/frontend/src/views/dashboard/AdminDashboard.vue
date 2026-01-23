<template>
  <div class="dashboard-container">
    <div class="dashboard-header mb-4">
      <h2 class="dashboard-title">Dashboard Overview</h2>
      <p class="dashboard-subtitle">Monitor your hospital management system at a glance</p>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else class="stats-grid">
      <div class="stat-card stat-card-primary">
        <div class="stat-icon-wrapper">
          <svg class="stat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">Total Patients</p>
          <h3 class="stat-value">{{ PatientCount }}</h3>
          <span class="stat-change positive">Active</span>
        </div>
      </div>

      <div class="stat-card stat-card-success">
        <div class="stat-icon-wrapper">
          <svg class="stat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">Total Doctors</p>
          <h3 class="stat-value">{{ doctorCount }}</h3>
          <span class="stat-change positive">Available</span>
        </div>
      </div>

      <div class="stat-card stat-card-warning">
        <div class="stat-icon-wrapper">
          <svg class="stat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">Upcoming Appointments</p>
          <h3 class="stat-value">{{ upcomingAppointmentsCount }}</h3>
          <span class="stat-change neutral">Scheduled</span>
        </div>
      </div>

      <div class="stat-card stat-card-danger">
        <div class="stat-icon-wrapper">
          <svg class="stat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">Completed</p>
          <h3 class="stat-value">{{ completedAppointmentsCount }}</h3>
          <span class="stat-change positive">Treatments</span>
        </div>
      </div>
    </div>

    <!-- Appointments Sections -->
    <div class="appointments-sections mt-4">
      <div class="row g-4">
        <!-- Upcoming Appointments -->
        <div class="col-lg-4">
          <div class="section-card">
            <div class="section-header upcoming">
              <h4 class="section-title">
                <svg class="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                Upcoming
              </h4>
              <span class="badge-count">{{ upcomingAppointments.length }}</span>
            </div>
            <div class="section-body">
              <div v-if="upcomingAppointments.length === 0" class="empty-state">
                <p class="empty-text">No upcoming appointments</p>
              </div>
              <div v-else class="appointments-scroll">
                <div v-for="apt in upcomingAppointments.slice(0, 5)" :key="apt.id" class="mini-appointment-card">
                  <div class="mini-apt-header">
                    <span class="patient-name">{{ apt.patient_name }}</span>
                    <span class="status-dot upcoming"></span>
                  </div>
                  <div class="mini-apt-details">
                    <span class="doctor-info">Dr. {{ apt.doctor_name }}</span>
                    <span class="apt-datetime">{{ formatDate(apt.appointment_date) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Latest/Recent Appointments -->
        <div class="col-lg-4">
          <div class="section-card">
            <div class="section-header recent">
              <h4 class="section-title">
                <svg class="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                Latest Booked
              </h4>
              <span class="badge-count recent">{{ latestAppointments.length }}</span>
            </div>
            <div class="section-body">
              <div v-if="latestAppointments.length === 0" class="empty-state">
                <p class="empty-text">No recent appointments</p>
              </div>
              <div v-else class="appointments-scroll">
                <div v-for="apt in latestAppointments.slice(0, 5)" :key="apt.id" class="mini-appointment-card">
                  <div class="mini-apt-header">
                    <span class="patient-name">{{ apt.patient_name }}</span>
                    <span class="status-dot recent"></span>
                  </div>
                  <div class="mini-apt-details">
                    <span class="doctor-info">Dr. {{ apt.doctor_name }}</span>
                    <span class="apt-datetime">{{ formatDate(apt.appointment_date) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Completed/Expired Appointments -->
        <div class="col-lg-4">
          <div class="section-card">
            <div class="section-header completed">
              <h4 class="section-title">
                <svg class="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                Completed
              </h4>
              <span class="badge-count completed">{{ completedAppointments.length }}</span>
            </div>
            <div class="section-body">
              <div v-if="completedAppointments.length === 0" class="empty-state">
                <p class="empty-text">No completed appointments</p>
              </div>
              <div v-else class="appointments-scroll">
                <div v-for="apt in completedAppointments.slice(0, 5)" :key="apt.id" class="mini-appointment-card">
                  <div class="mini-apt-header">
                    <span class="patient-name">{{ apt.patient_name }}</span>
                    <span class="status-dot completed"></span>
                  </div>
                  <div class="mini-apt-details">
                    <span class="doctor-info">Dr. {{ apt.doctor_name }}</span>
                    <span class="apt-datetime">{{ formatDate(apt.appointment_date) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="quick-actions mt-5">
      <h4 class="section-title mb-3">Quick Actions</h4>
      <div class="actions-grid">
        <button class="action-btn" @click="$router.push('/admin/add-doctor')">
          <svg class="action-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          <span>Add New Doctor</span>
        </button>
        <button class="action-btn" @click="$router.push('/admin/doctor-list')">
          <svg class="action-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
          </svg>
          <span>View All Doctors</span>
        </button>
        <button class="action-btn" @click="$router.push('/admin/patient-list')">
          <svg class="action-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
          </svg>
          <span>View All Patients</span>
        </button>
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
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
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

.stat-card-danger {
  border-left: 4px solid #ef4444;
}

.stat-card-danger .stat-icon-wrapper {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
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

.stat-change.negative {
  background: #fee2e2;
  color: #991b1b;
}

.stat-change.neutral {
  background: #fef3c7;
  color: #92400e;
}

.quick-actions {
  margin-top: 3rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 1rem;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.action-btn {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 600;
  color: #475569;
}

.action-btn:hover {
  border-color: #5e63b6;
  background: #f8fafc;
  color: #5e63b6;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(94, 99, 182, 0.15);
}

.action-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .dashboard-title {
    font-size: 1.5rem;
  }

  .stat-value {
    font-size: 1.75rem;
  }
}

/* Appointments Sections Styles */
.appointments-sections {
  margin-top: 2rem;
}

.section-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  height: 100%;
}

.section-header {
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.section-header.upcoming {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.section-header.recent {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.section-header.completed {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.section-header .section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: white;
  margin: 0;
}

.section-icon {
  width: 20px;
  height: 20px;
}

.badge-count {
  background: rgba(255, 255, 255, 0.25);
  color: white;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
}

.section-body {
  padding: 1rem;
  max-height: 300px;
  overflow-y: auto;
}

.appointments-scroll {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.mini-appointment-card {
  background: #f8fafc;
  border-radius: 10px;
  padding: 0.85rem 1rem;
  border-left: 3px solid #e2e8f0;
  transition: all 0.2s ease;
}

.mini-appointment-card:hover {
  background: #f1f5f9;
  transform: translateX(4px);
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
  font-size: 0.9rem;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.upcoming {
  background: #f59e0b;
}

.status-dot.recent {
  background: #3b82f6;
}

.status-dot.completed {
  background: #10b981;
}

.mini-apt-details {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #64748b;
}

.doctor-info {
  font-weight: 500;
}

.apt-datetime {
  font-weight: 500;
  color: #94a3b8;
}

.empty-state {
  text-align: center;
  padding: 2rem 1rem;
}

.empty-text {
  color: #94a3b8;
  font-size: 0.9rem;
  margin: 0;
}

@media (max-width: 992px) {
  .appointments-sections .row {
    gap: 1rem;
  }
  
  .section-body {
    max-height: 250px;
  }
}
</style>
