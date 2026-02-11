<template>
  <div class="container">
    <h2 class="mb-4 text-center text-primary fw-bold">Blocked Users</h2>

    <div v-if="loading" class="text-center mt-5">
      <div class="spinner-border text-primary"></div>
      <p class="mt-3">Loading blocked users...</p>
    </div>

    <div v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </div>

    <div class="row">
      <div
        v-for="user in blockedUsers"
        :key="user.id"
        class="col-md-4 mb-4"
      >
        <div class="user-card shadow-lg">
          <div class="card-header-area">
            <img class="avatar" :src="user.role === 'doctor' ? DoctorIcon : PatientIcon" />
            <h5 class="user-name">{{ user.username }}</h5>
            <p class="user-email">{{ user.email }}</p>
            <span class="user-role">
              {{ user.role }}
            </span>
          </div>

          <div class="user-info">
            <p><strong>Role:</strong> {{ user.role }}</p>
            <p><strong>Status:</strong> <span class="badge-blocked">Blocked</span></p>
          </div>

          <div class="action-buttons mt-3">
            <button class="btn unblock-btn" @click="unblockUser(user)"> Unblock</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import DoctorIcon from "../../assets/doctor.png";
import PatientIcon from "../../assets/patient.png";
import auth from "../../utils/auth";

const router = useRouter();
const blockedUsers = ref([]);
const loading = ref(false);
const errorMessage = ref("");

const fetchBlockedUsers = async () => {
  loading.value = true;

  try {
    const token = auth.getToken();

    // Fetch blocked doctors
    const doctorResponse = await fetch("http://127.0.0.1:5000/api/admin/doctor-list", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      }
    });

    // Fetch blocked patients
    const patientResponse = await fetch("http://127.0.0.1:5000/api/admin/patient-list", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      }
    });

    if (!doctorResponse.ok || !patientResponse.ok) {
      throw new Error("Failed to fetch users");
    }

    const doctorData = await doctorResponse.json();
    const patientData = await patientResponse.json();

    // Filter blocked users (assuming active: false means blocked)
    const blockedDoctors = doctorData.doctors.filter(doctor => !doctor.active);
    const blockedPatients = patientData.patients.filter(patient => !patient.active);

    blockedUsers.value = [...blockedDoctors, ...blockedPatients];

  } catch (err) {
    errorMessage.value = "Failed to load blocked users.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

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
        fetchBlockedUsers();
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

onMounted(() => {
  fetchBlockedUsers();
});
</script>

<style scoped>
.user-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%);
  border-radius: 16px;
  padding: 28px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(148, 163, 184, 0.1);
  backdrop-filter: blur(20px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.user-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #ef4444, #dc2626);
}

.user-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border-color: rgba(239, 68, 68, 0.2);
}

.card-header-area {
  text-align: center;
  margin-bottom: 20px;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-bottom: 12px;
  border: 4px solid #fecaca;
  box-shadow: 0 4px 14px 0 rgba(239, 68, 68, 0.15);
  transition: all 0.3s ease;
}

.avatar:hover {
  transform: scale(1.05);
}

.user-name {
  font-size: 1.375rem;
  color: #1e293b;
  font-weight: 700;
  margin-bottom: 4px;
  letter-spacing: 0.025em;
  line-height: 1.4;
}

.user-email {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 16px;
  letter-spacing: 0.025em;
  line-height: 1.5;
}

.user-info p {
  margin-bottom: 8px;
  font-size: 0.875rem;
  color: #475569;
  letter-spacing: 0.025em;
  line-height: 1.6;
}

.user-role {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
  letter-spacing: 0.025em;
}

.badge-blocked {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #b91c1c;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.action-buttons {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

.btn {
  border-radius: 25px;
  padding: 10px 20px;
  font-size: 0.875rem;
  font-weight: 600;
  border: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn:hover::before {
  left: 100%;
}

.unblock-btn {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  color: #166534;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.unblock-btn:hover {
  background: linear-gradient(135deg, #bbf7d0 0%, #a7f3d0 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(34, 197, 94, 0.3);
}
</style>