<template>
  <div class="appointments-container">
    <div class="appointments-header">
      <h2 class="page-title">Appointments Management</h2>
      <p class="page-subtitle">View and manage all appointments in the system</p>
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
              <span class="status-text">Upcoming</span>
            </div>
            <div class="card-body">
              <div class="patient-info">
                <div class="avatar patient-avatar">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                </div>
                <div class="info-text">
                  <h6 class="name">{{ apt.patient_name }}</h6>
                  <p class="email">{{ apt.patient_email }}</p>
                </div>
              </div>
              <div class="doctor-info">
                <div class="avatar doctor-avatar">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <div class="info-text">
                  <h6 class="name">Dr. {{ apt.doctor_name }}</h6>
                  <p class="specialty">{{ apt.doctor_specialization || 'General' }}</p>
                </div>
              </div>
              <div class="datetime-info">
                <div class="date">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  <span>{{ formatDate(apt.appointment_date) }}</span>
                </div>
                <div class="time">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span>{{ apt.appointment_time }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Expired/Missed Appointments -->
      <div v-if="activeTab === 'expired'" class="appointments-section">
        <div v-if="expiredAppointments.length === 0" class="empty-state">
          <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <p class="empty-text">No expired appointments</p>
        </div>
        <div v-else class="appointments-grid">
          <div v-for="apt in expiredAppointments" :key="apt.id" class="appointment-card expired">
            <div class="card-header">
              <div class="status-indicator expired"></div>
              <span class="status-text">Expired</span>
            </div>
            <div class="card-body">
              <div class="patient-info">
                <div class="avatar patient-avatar">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                </div>
                <div class="info-text">
                  <h6 class="name">{{ apt.patient_name }}</h6>
                  <p class="email">{{ apt.patient_email }}</p>
                </div>
              </div>
              <div class="doctor-info">
                <div class="avatar doctor-avatar">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <div class="info-text">
                  <h6 class="name">Dr. {{ apt.doctor_name }}</h6>
                  <p class="specialty">{{ apt.doctor_specialization || 'General' }}</p>
                </div>
              </div>
              <div class="datetime-info">
                <div class="date">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  <span>{{ formatDate(apt.appointment_date) }}</span>
                </div>
                <div class="time">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span>{{ apt.appointment_time }}</span>
                </div>
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
          <p class="empty-text">No completed appointments</p>
        </div>
        <div v-else class="appointments-grid">
          <div v-for="apt in completedAppointments" :key="apt.id" class="appointment-card completed">
            <div class="card-header">
              <div class="status-indicator completed"></div>
              <span class="status-text">Completed</span>
            </div>
            <div class="card-body">
              <div class="patient-info">
                <div class="avatar patient-avatar">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                </div>
                <div class="info-text">
                  <h6 class="name">{{ apt.patient_name }}</h6>
                  <p class="email">{{ apt.patient_email }}</p>
                </div>
              </div>
              <div class="doctor-info">
                <div class="avatar doctor-avatar">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <div class="info-text">
                  <h6 class="name">Dr. {{ apt.doctor_name }}</h6>
                  <p class="specialty">{{ apt.doctor_specialization || 'General' }}</p>
                </div>
              </div>
              <div class="datetime-info">
                <div class="date">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  <span>{{ formatDate(apt.appointment_date) }}</span>
                </div>
                <div class="time">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span>{{ apt.appointment_time }}</span>
                </div>
              </div>
              <div v-if="apt.treatment" class="treatment-preview">
                <span class="treatment-label">Treatment recorded</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, h } from "vue";
import auth from "../../utils/auth";

const loading = ref(true);
const activeTab = ref("upcoming");
const allAppointments = ref([]);

const tabs = [
  {
    key: "upcoming",
    label: "Upcoming",
    icon: () => h("svg", { fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" }, [
      h("path", { "stroke-linecap": "round", "stroke-linejoin": "round", "stroke-width": "2", d: "M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" })
    ])
  },
  {
    key: "expired",
    label: "Expired",
    icon: () => h("svg", { fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" }, [
      h("path", { "stroke-linecap": "round", "stroke-linejoin": "round", "stroke-width": "2", d: "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" })
    ])
  },
  {
    key: "completed",
    label: "Completed",
    icon: () => h("svg", { fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" }, [
      h("path", { "stroke-linecap": "round", "stroke-linejoin": "round", "stroke-width": "2", d: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" })
    ])
  }
];

const getToken = () => auth.getToken();

const upcomingAppointments = computed(() => {
  const today = new Date().toISOString().split('T')[0];
  return allAppointments.value.filter(apt => 
    apt.appointment_date >= today && apt.status === "BOOKED"
  );
});

const expiredAppointments = computed(() => {
  const today = new Date().toISOString().split('T')[0];
  return allAppointments.value.filter(apt => 
    apt.appointment_date < today && apt.status === "BOOKED"
  );
});

const completedAppointments = computed(() => {
  return allAppointments.value.filter(apt => apt.status === "COMPLETED");
});

const getTabCount = (tabKey) => {
  switch(tabKey) {
    case "upcoming": return upcomingAppointments.value.length;
    case "expired": return expiredAppointments.value.length;
    case "completed": return completedAppointments.value.length;
    default: return 0;
  }
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', { 
    weekday: 'short',
    month: 'short', 
    day: 'numeric',
    year: 'numeric'
  });
};

const loadAppointments = async () => {
  loading.value = true;
  try {
    const response = await fetch("http://localhost:5000/api/admin/appointments", {
      headers: { Authorization: `Bearer ${getToken()}` }
    });
    
    if (response.ok) {
      const data = await response.json();
      allAppointments.value = data.appointments || [];
    }
  } catch (error) {
    console.error("Failed to load appointments:", error);
  } finally {
    loading.value = false;
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
  margin: 0;
}

.tabs-container {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  background: white;
  padding: 0.5rem;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  background: transparent;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  color: #64748b;
  transition: all 0.3s ease;
  flex: 1;
  justify-content: center;
}

.tab-btn:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.tab-btn.active {
  background: linear-gradient(135deg, #5e63b6 0%, #4a50a0 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(94, 99, 182, 0.3);
}

.tab-icon {
  width: 20px;
  height: 20px;
}

.tab-count {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
}

.tab-btn:not(.active) .tab-count {
  background: #e2e8f0;
  color: #64748b;
}

.tab-btn.active .tab-count {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
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
  font-size: 1.1rem;
  margin: 0;
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
  transition: all 0.3s ease;
}

.appointment-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #f1f5f9;
}

.status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.status-indicator.upcoming {
  background: #3b82f6;
  box-shadow: 0 0 8px rgba(59, 130, 246, 0.4);
}

.status-indicator.expired {
  background: #f59e0b;
  box-shadow: 0 0 8px rgba(245, 158, 11, 0.4);
}

.status-indicator.completed {
  background: #10b981;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.4);
}

.status-text {
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.appointment-card.upcoming .status-text {
  color: #3b82f6;
}

.appointment-card.expired .status-text {
  color: #f59e0b;
}

.appointment-card.completed .status-text {
  color: #10b981;
}

.card-body {
  padding: 1.5rem;
}

.patient-info,
.doctor-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.avatar {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar svg {
  width: 24px;
  height: 24px;
}

.patient-avatar {
  background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
  color: #4f46e5;
}

.doctor-avatar {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  color: #16a34a;
}

.info-text .name {
  font-size: 0.95rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
}

.info-text .email,
.info-text .specialty {
  font-size: 0.85rem;
  color: #64748b;
  margin: 0;
}

.datetime-info {
  display: flex;
  gap: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;
}

.datetime-info .date,
.datetime-info .time {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  font-size: 0.9rem;
}

.datetime-info svg {
  width: 18px;
  height: 18px;
  color: #94a3b8;
}

.treatment-preview {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;
}

.treatment-label {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #ecfdf5;
  color: #059669;
  font-size: 0.85rem;
  font-weight: 500;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .tabs-container {
    flex-direction: column;
  }

  .appointments-grid {
    grid-template-columns: 1fr;
  }

  .datetime-info {
    flex-direction: column;
    gap: 0.75rem;
  }
}
</style>
