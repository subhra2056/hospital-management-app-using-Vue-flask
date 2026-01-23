<template>
  <div class="sidebar">
    <div class="sidebar-content">
      <div class="sidebar-header">
        <div class="profile-section">
          <div class="avatar-container">
            <img class="avatar" :src="profileIcon" alt="Patient Profile" />
            <div class="status-indicator"></div>
          </div>
          <div class="profile-info">
            <h5 class="profile-name">{{ patientName }}</h5>
            <p class="profile-role">Patient</p>
          </div>
        </div>
      </div>

      <nav class="sidebar-nav">
        <div
          v-for="item in menuItems"
          :key="item.key"
          :class="['nav-item', { active: active === item.key }]"
          @click="emit('navigate', item.key)"
        >
          <div class="nav-icon">
            <component :is="item.icon" />
          </div>
          <span class="nav-label">{{ item.label }}</span>
          <div v-if="active === item.key" class="nav-indicator"></div>
        </div>
      </nav>
    </div>

    <div class="sidebar-footer">
      <button class="logout-btn" @click="handleLogout">
        <svg class="logout-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
        </svg>
        <span>Logout</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { h, ref, onMounted } from "vue";
import profileIcon from "../assets/patient.png";
import { useRouter } from "vue-router";
import auth from "../utils/auth";

const router = useRouter();
const patientName = ref("Patient");

defineProps({
  active: String
});

const emit = defineEmits(["navigate"]);

onMounted(() => {
  const user = auth.getUser();
  if (user && user.username) {
    patientName.value = user.username;
  }
});

const menuItems = [
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
    key: "findDoctor",
    label: "Find Doctor",
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
        d: "M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
      })
    ])
  },
  {
    key: "appointments",
    label: "My Appointments",
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
    key: "completed",
    label: "Treatment History",
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
        d: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
      })
    ])
  },
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
  }
];

const handleLogout = () => {
  auth.clearAll();
  router.push("/login");
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

.sidebar-footer {
  padding: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 0.875rem 1.25rem;
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 12px;
  color: white;
  font-weight: 600;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.3);
  border-color: rgba(239, 68, 68, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
}

.logout-icon {
  width: 18px;
  height: 18px;
}

@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    min-height: auto;
  }
}
</style>
