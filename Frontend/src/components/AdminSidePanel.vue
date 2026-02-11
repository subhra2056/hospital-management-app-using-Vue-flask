<template>
  <div class="sidebar">
    <div class="sidebar-content">
      <div class="sidebar-header">
        <div class="profile-section">
          <div class="avatar-container">
            <img class="avatar" :src="profileIcon" alt="Admin Profile" />
            <div class="status-indicator"></div>
          </div>
          <div class="profile-info">
            <h5 class="profile-name">Admin</h5>
            <p class="profile-role">Administrator</p>
          </div>
        </div>
      </div>

      <nav class="sidebar-nav">
        <div
          v-for="item in menuItems"
          :key="item.key"
          :class="['nav-item', { active: active === item.key }]"
          @click="emit('change', item.key)"
        >
          <div class="nav-icon">
            <component :is="item.icon" />
          </div>
          <span class="nav-label">{{ item.label }}</span>
          <div v-if="active === item.key" class="nav-indicator"></div>
        </div>
        
        <!-- Logout Option -->
        <div class="nav-item logout-item" @click="showLogoutModal = true">
          <div class="nav-icon">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" class="icon">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
          </div>
          <span class="nav-label">Logout</span>
        </div>
      </nav>
    </div>
  </div>

  <!-- Logout Confirmation Modal -->
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="showLogoutModal" class="modal-overlay" @click.self="showLogoutModal = false">
        <div class="modal-container">
          <div class="modal-icon">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
          </div>
          <h3 class="modal-title">Logout Confirmation</h3>
          <p class="modal-message">Are you sure you want to logout?</p>
          <div class="modal-actions">
            <button class="btn-cancel" @click="showLogoutModal = false">Cancel</button>
            <button class="btn-confirm" @click="confirmLogout">Yes, Logout</button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { h, ref } from "vue";
import profileIcon from "../assets/user.png";
import { useRouter } from "vue-router";
import auth from "../utils/auth";

const router = useRouter();

defineProps({
  active: String
});

const emit = defineEmits(["change"]);

const menuItems = [
   {
    key: "profile",
    label: "View Profile",
    icon: () => h("svg", {
      fill: "none",
      stroke: "currentColor",
      viewBox: "0 0 24 24",
      class: "icon"
    }, [
      h("path", {
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "stroke-width": "2",
        d: "M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
      })
    ])
  },
  {
    key: "dashboard",
    label: "Dashboard",
    icon: () => h("svg", {
      fill: "none",
      stroke: "currentColor",
      viewBox: "0 0 24 24",
      class: "icon"
    }, [
      h("path", {
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "stroke-width": "2",
        d: "M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
      })
    ])
  },
  {
    key: "addDoctor",
    label: "Add Doctor",
    icon: () => h("svg", {
      fill: "none",
      stroke: "currentColor",
      viewBox: "0 0 24 24",
      class: "icon"
    }, [
      h("path", {
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "stroke-width": "2",
        d: "M12 4v16m8-8H4"
      })
    ])
  },
  {
    key: "viewDoctors",
    label: "Doctor List",
    icon: () => h("svg", {
      fill: "none",
      stroke: "currentColor",
      viewBox: "0 0 24 24",
      class: "icon"
    }, [
      h("path", {
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "stroke-width": "2",
        d: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"
      })
    ])
  },
  {
    key: "viewPatients",
    label: "Patient List",
    icon: () => h("svg", {
      fill: "none",
      stroke: "currentColor",
      viewBox: "0 0 24 24",
      class: "icon"
    }, [
      h("path", {
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "stroke-width": "2",
        d: "M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
      })
    ])
  },
  {
    key: "departments",
    label: "Departments",
    icon: () => h("svg", {
      fill: "none",
      stroke: "currentColor",
      viewBox: "0 0 24 24",
      class: "icon"
    }, [
      h("path", {
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "stroke-width": "2",
        d: "M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
      })
    ])
  },
  {
    key: "appointments",
    label: "Appointments",
    icon: () => h("svg", {
      fill: "none",
      stroke: "currentColor",
      viewBox: "0 0 24 24",
      class: "icon"
    }, [
      h("path", {
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "stroke-width": "2",
        d: "M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
      })
    ])
  },
  {
    key: "blockedDoctors",
    label: "Blocked Doctors",
    icon: () => h("svg", {
      fill: "none",
      stroke: "currentColor",
      viewBox: "0 0 24 24",
      class: "icon"
    }, [
      h("path", {
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "stroke-width": "2",
        d: "M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"
      })
    ])
  },
  {
    key: "blockedPatients",
    label: "Blocked Patients",
    icon: () => h("svg", {
      fill: "none",
      stroke: "currentColor",
      viewBox: "0 0 24 24",
      class: "icon"
    }, [
      h("path", {
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "stroke-width": "2",
        d: "M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"
      })
    ])
  }
];

const handleLogout = () => {
  auth.clearAll();
  router.push("/login");
};

const showLogoutModal = ref(false);

const confirmLogout = () => {
  showLogoutModal.value = false;
  handleLogout();
};
</script>

<style scoped>
.sidebar {
  width: 280px;
  background: linear-gradient(180deg, #5e63b6 0%, #4a50a0 100%);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 100vh;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
}

.sidebar-header {
  padding: 2rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.profile-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.avatar-container {
  position: relative;
  flex-shrink: 0;
}

.avatar {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  object-fit: cover;
  background: rgba(255, 255, 255, 0.2);
}

.status-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 14px;
  height: 14px;
  background: #10b981;
  border: 2px solid #5e63b6;
  border-radius: 50%;
}

.profile-info {
  flex: 1;
  min-width: 0;
}

.profile-name {
  font-size: 1rem;
  font-weight: 700;
  color: white;
  margin: 0 0 0.25rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.profile-role {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

.sidebar-nav {
  padding: 1rem 0;
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.875rem 1.5rem;
  margin: 0.25rem 0.75rem;
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9375rem;
  font-weight: 500;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  transform: translateX(4px);
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-weight: 600;
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 60%;
  background: white;
  border-radius: 0 4px 4px 0;
}

.nav-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-icon .icon {
  width: 100%;
  height: 100%;
}

.nav-label {
  flex: 1;
}

.nav-indicator {
  width: 6px;
  height: 6px;
  background: white;
  border-radius: 50%;
  flex-shrink: 0;
}

/* Logout item styling */
.logout-item {
  margin-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 1rem !important;
}

.logout-item:hover {
  background: rgba(239, 68, 68, 0.3) !important;
  color: #fca5a5 !important;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-container {
  background: white;
  border-radius: 20px;
  padding: 2.5rem;
  max-width: 400px;
  width: 90%;
  text-align: center;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-icon {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}

.modal-icon svg {
  width: 35px;
  height: 35px;
  color: #ef4444;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

.modal-message {
  color: #6b7280;
  font-size: 1rem;
  margin-bottom: 2rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn-cancel {
  padding: 0.75rem 1.5rem;
  border: 2px solid #e5e7eb;
  background: white;
  color: #6b7280;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.btn-confirm {
  padding: 0.75rem 1.5rem;
  border: none;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.btn-confirm:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(239, 68, 68, 0.4);
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

@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    min-height: auto;
  }
}
</style>
