<template>
  <div class="blocked-list-container">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"></path>
          </svg>
        </div>
        <div class="header-text">
          <h1>Blocked Patients</h1>
          <p>Manage blocked patient accounts</p>
        </div>
      </div>
      <div class="header-stats">
        <div class="stat-badge">
          <span class="stat-number">{{ blockedPatients.length }}</span>
          <span class="stat-label">Blocked</span>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="loader"></div>
      <p>Loading blocked patients...</p>
    </div>

    <div v-if="errorMessage" class="error-alert">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      {{ errorMessage }}
    </div>

    <!-- Empty State -->
    <div v-if="!loading && blockedPatients.length === 0" class="empty-state">
      <div class="empty-icon">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
      </div>
      <h3>No Blocked Patients</h3>
      <p>All patient accounts are currently active</p>
    </div>

    <div class="cards-grid">
      <div
        v-for="patient in blockedPatients"
        :key="patient.id"
        class="blocked-card"
      >
        <div class="card-accent"></div>
        <div class="blocked-overlay">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"></path>
          </svg>
        </div>
        <div class="card-content">
          <div class="card-header">
            <div class="avatar-wrapper">
              <img class="avatar" :src="PatientIcon" alt="Patient" />
              <div class="status-badge blocked">
                <svg fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M13.477 14.89A6 6 0 015.11 6.524l8.367 8.368zm1.414-1.414L6.524 5.11a6 6 0 018.367 8.367zM18 10a8 8 0 11-16 0 8 8 0 0116 0z" clip-rule="evenodd"></path>
                </svg>
              </div>
            </div>
            <div class="user-identity">
              <h3 class="user-name">{{ patient.username }}</h3>
              <p class="user-email">{{ patient.email }}</p>
              <span class="role-badge">Patient</span>
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
          </div>

          <div class="status-section">
            <div class="status-indicator">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
              </svg>
              <span>Account Blocked</span>
            </div>
          </div>

          <div class="card-actions">
            <button class="action-btn unblock-btn" @click="unblockUser(patient)">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z"></path>
              </svg>
              Unblock Account
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import PatientIcon from "../../assets/patient.png";
import auth from "../../utils/auth";

const router = useRouter();
const blockedPatients = ref([]);
const loading = ref(false);
const errorMessage = ref("");

const fetchBlockedPatients = async () => {
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
    blockedPatients.value = data.patients.filter(patient => !patient.active);

  } catch (err) {
    errorMessage.value = "Failed to load blocked patients.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchBlockedPatients();
});

const unblockUser = async (user) => {
  const token = auth.getToken();
  if (!token) {
    alert("Please login first");
    router.push("/login");
    return;
  }

  if (confirm(`Are you sure you want to unblock ${user.username}?`)) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/admin/users/${user.id}/unblock`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (response.ok) {
        alert("User unblocked successfully");
        fetchBlockedPatients();
      } else {
        if (response.status === 401) {
          alert("Please login again");
          auth.clearAll();
          router.push("/login");
        } else if (response.status === 403) {
          alert("Unauthorized");
        } else {
          alert("Failed to unblock user");
        }
      }
    } catch (err) {
      console.error(err);
      alert("Error unblocking user");
    }
  }
};
</script>

<style scoped>
.blocked-list-container {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(45, 55, 72, 0.3);
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
  border-top-color: #4a5568;
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
}

.empty-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.empty-icon svg {
  width: 40px;
  height: 40px;
  color: #16a34a;
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

/* Cards Grid */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 1.5rem;
}

/* Blocked Card */
.blocked-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.blocked-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(45, 55, 72, 0.2);
}

.card-accent {
  height: 6px;
  background: linear-gradient(90deg, #e53e3e 0%, #fc8181 50%, #e53e3e 100%);
  background-size: 200% 100%;
  animation: shimmer 3s ease infinite;
}

@keyframes shimmer {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.blocked-overlay {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 40px;
  height: 40px;
  background: rgba(229, 62, 62, 0.08);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.blocked-overlay svg {
  width: 24px;
  height: 24px;
  color: #e53e3e;
  opacity: 0.5;
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
  border: 3px solid #e2e8f0;
  filter: grayscale(20%);
  transition: all 0.3s ease;
}

.blocked-card:hover .avatar {
  filter: grayscale(0%);
}

.status-badge {
  position: absolute;
  bottom: -4px;
  right: -4px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid white;
}

.status-badge.blocked {
  background: #e53e3e;
}

.status-badge svg {
  width: 14px;
  height: 14px;
  color: white;
}

.user-identity {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0 0 0.5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.role-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  color: #475569;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

/* Info Grid */
.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.25rem;
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
  background: linear-gradient(135deg, #e9d8fd 0%, #faf5ff 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.info-icon svg {
  width: 18px;
  height: 18px;
  color: #6b46c1;
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

/* Status Section */
.status-section {
  margin-bottom: 1.25rem;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
  border: 1px solid #feb2b2;
  border-radius: 12px;
  color: #c53030;
  font-weight: 600;
  font-size: 0.875rem;
}

.status-indicator svg {
  width: 18px;
  height: 18px;
}

/* Card Actions */
.card-actions {
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;
}

.action-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.unblock-btn {
  background: linear-gradient(135deg, #5e63b6 0%, #4a50a0 100%);
  color: white;
}

.unblock-btn:hover {
  background: linear-gradient(135deg, #4a50a0 0%, #3d4190 100%);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(94, 99, 182, 0.4);
}

/* Responsive */
@media (max-width: 768px) {
  .blocked-list-container {
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

  .cards-grid {
    grid-template-columns: 1fr;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>