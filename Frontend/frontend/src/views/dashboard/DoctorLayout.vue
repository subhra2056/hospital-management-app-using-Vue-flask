<template>
  <div class="doctor-layout">
    <SidePanel :active="activeSection" @change="handleChange" />
    <div class="doctor-content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import SidePanel from "../../components/DoctorSidePanel.vue";

const router = useRouter();
const activeSection = ref("dashboard");

function handleChange(section) {
  activeSection.value = section;

  if (section === "dashboard") router.push("/doctor/dashboard");
  if (section === "appointments") router.push("/doctor/appointments");
  if (section === "availability") router.push("/doctor/availability");
  if (section === "profile") router.push("/profile");
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

@media (max-width: 768px) {
  .doctor-layout {
    flex-direction: column;
  }

  .doctor-content {
    padding: 1rem;
  }
}
</style>
