<template>
  <div class="admin-layout">
    <SidePanel :active="activeSection" @change="handleChange" />
    <div class="admin-content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import SidePanel from "../../components/AdminSidePanel.vue";

const router = useRouter();
const activeSection = ref("dashboard");

function handleChange(section) {
  activeSection.value = section;

  if (section === "profile") router.push("/profile");
  if (section === "dashboard") router.push("/admin/dashboard");
  if (section === "addDoctor") router.push("/admin/add-doctor");
  if (section === "viewDoctors") router.push("/admin/doctor-list");
  if (section === "viewPatients") router.push("/admin/patient-list");
  if (section === "departments") router.push("/admin/departments");
  if (section === "appointments") router.push("/admin/appointments");
  if (section === "blockedDoctors") router.push("/admin/blocked-doctors");
  if (section === "blockedPatients") router.push("/admin/blocked-patients");
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f8fafc;
}

.admin-content {
  flex: 1;
  padding: 2rem;
  overflow-x: hidden;
  background: #f8fafc;
}

@media (max-width: 768px) {
  .admin-layout {
    flex-direction: column;
  }

  .admin-content {
    padding: 1rem;
  }
}
</style>