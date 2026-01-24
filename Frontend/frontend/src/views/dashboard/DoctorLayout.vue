<template>
  <div class="doctor-layout">
    <SidePanel :active="activeSection" @change="handleChange" />
    <div class="doctor-content">
      <!-- AI Assistant Section -->
      <div v-if="activeSection === 'aiAssistant'" class="ai-assistant-panel">
        <div class="panel-header">
          <h2 class="panel-title">AI Scheduling Assistant</h2>
          <p class="panel-subtitle">Let AI help you manage your availability quickly</p>
        </div>
        <div class="chatbot-wrapper">
          <DoctorAIChatbot />
        </div>
      </div>
      <router-view v-else />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import SidePanel from "../../components/DoctorSidePanel.vue";
import DoctorAIChatbot from "../../components/DoctorAIChatbot.vue";

const router = useRouter();
const activeSection = ref("dashboard");

function handleChange(section) {
  activeSection.value = section;

  if (section === "dashboard") router.push("/doctor/dashboard");
  if (section === "appointments") router.push("/doctor/appointments");
  if (section === "availability") router.push("/doctor/availability");
  if (section === "profile") router.push("/profile");
  // AI Assistant doesn't need a route change as it's rendered inline
}
</script>

<style scoped>
.doctor-layout {
  display: flex;
  min-height: 100vh;
  background: #f8fafc;
}

.doctor-content {
  flex: 1;
  padding: 2rem;
  overflow-x: hidden;
  background: #f8fafc;
}

/* AI Assistant Panel Styles */
.ai-assistant-panel {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 4rem);
}

.panel-header {
  margin-bottom: 1.5rem;
}

.panel-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.panel-subtitle {
  color: #64748b;
  margin: 0;
}

.chatbot-wrapper {
  flex: 1;
  min-height: 0;
  overflow: hidden;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

@media (max-width: 768px) {
  .doctor-layout {
    flex-direction: column;
  }

  .doctor-content {
    padding: 1rem;
  }

  .ai-assistant-panel {
    height: calc(100vh - 120px);
  }
}
</style>
