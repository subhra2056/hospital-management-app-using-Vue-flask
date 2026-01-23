<template>
  <div class="container">
    <h2 class="mb-4 text-center text-primary fw-bold">Doctor List</h2>

    <div v-if="loading" class="text-center mt-5">
      <div class="spinner-border text-primary"></div>
      <p class="mt-3">Loading doctors...</p>
    </div>

    <div v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </div>

    <div class="row">
      <div
        v-for="doctor in doctors"
        :key="doctor.id"
        class="col-md-4 mb-4"
      >
        <div class="doctor-card shadow-lg">
          <div class="card-header-area">
            <img class="avatar" :src="DoctorIcon" />
            <h5 class="doctor-name">{{ doctor.username }}</h5>
            <p class="doctor-email">{{ doctor.email }}</p>
          </div>

          <div class="doctor-info">
            <p><strong>Department:</strong> <span class="badge-blue">{{ doctor.department_name }}</span></p>
            <p><strong>Specialization:</strong> <span class="badge-green">{{ doctor.specialization }}</span></p>
            <p><strong>Experience:</strong> {{ doctor.experience_years }} years</p>
            <p><strong>Gender:</strong> {{ doctor.gender }}</p>
          </div>

          <div class="action-buttons mt-3">
            <button class="btn edit-btn" @click="editDoctor(doctor)"> Edit</button>
            <button class="btn delete-btn" @click="deleteDoctor(doctor)"> Delete</button>
            <button class="btn block-btn" @click="blockDoctor(doctor)"> Block</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Doctor Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click="closeEditModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Edit Doctor</h3>
          <button class="close-btn" @click="closeEditModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitEditDoctor">
            <div class="form-group">
              <label for="edit-username">Username</label>
              <input type="text" id="edit-username" v-model="editForm.username" required />
            </div>
            <div class="form-group">
              <label for="edit-email">Email</label>
              <input type="email" id="edit-email" v-model="editForm.email" required />
            </div>
            <div class="form-group">
              <label for="edit-specialization">Specialization</label>
              <input type="text" id="edit-specialization" v-model="editForm.specialization" required />
            </div>
            <div class="form-group">
              <label for="edit-experience">Experience (years)</label>
              <input type="number" id="edit-experience" v-model.number="editForm.experience_years" required />
            </div>
            <div class="form-group">
              <label for="edit-gender">Gender</label>
              <select id="edit-gender" v-model="editForm.gender" required>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div class="modal-actions">
              <button type="button" class="btn cancel-btn" @click="closeEditModal">Cancel</button>
              <button type="submit" class="btn save-btn">Save Changes</button>
            </div>
          </form>
        </div>
      </div>
    </div>

  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import DoctorIcon from "../../assets/doctor.png"
import auth from "../../utils/auth";

const router = useRouter();
const doctors = ref([]);
const loading = ref(false);
const errorMessage = ref("");
const showEditModal = ref(false);
const editForm = ref({
  id: null,
  username: "",
  email: "",
  specialization: "",
  experience_years: "",
  gender: ""
});

const fetchDoctors = async () => {
  loading.value = true;

  try {
    const token = auth.getToken();

    const response = await fetch("http://127.0.0.1:5000/api/admin/doctor-list", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error("Failed to fetch");
    }

    const data = await response.json();
    doctors.value = data.doctors.filter(d => d.active);

  } catch (err) {
    errorMessage.value = "Failed to load doctors.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchDoctors();
});

const editDoctor = (doctor) => {
  editForm.value = {
    id: doctor.id,
    username: doctor.username,
    email: doctor.email,
    specialization: doctor.specialization,
    experience_years: doctor.experience_years,
    gender: doctor.gender
  };
  showEditModal.value = true;
};

const submitEditDoctor = async () => {
  const token = auth.getToken();
  if (!token) {
    alert("Please login first");
    router.push("/login");
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:5000/api/admin/doctors/${editForm.value.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        username: editForm.value.username,
        email: editForm.value.email,
        specialization: editForm.value.specialization,
        experience_years: editForm.value.experience_years,
        gender: editForm.value.gender
      })
    });

    if (response.ok) {
      alert("Doctor updated successfully");
      showEditModal.value = false;
      fetchDoctors();
    } else {
      if (response.status === 401) {
        alert("Please login again");
        auth.clearAll();
        router.push("/login");
      } else if (response.status === 403) {
        alert("Unauthorized");
      } else {
        const errorData = await response.json();
        alert(errorData.message || "Failed to update doctor");
      }
    }
  } catch (err) {
    console.error(err);
    alert("Error updating doctor");
  }
};

const closeEditModal = () => {
  showEditModal.value = false;
};

const deleteDoctor = async (doctor) => {
  const token = auth.getToken();
  if (!token) {
    alert("Please login first");
    router.push("/login");
    return;
  }

  if (confirm(`Are you sure you want to delete ${doctor.username}?`)) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/admin/doctors/${doctor.id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (response.ok) {
        alert("Doctor deleted successfully");
        fetchDoctors();
      } else {
        if (response.status === 401) {
          alert("Please login again");
          auth.clearAll();
          router.push("/login");
        } else if (response.status === 403) {
          alert("Unauthorized");
        } else {
          const errorData = await response.json();
          alert(errorData.message || "Failed to delete doctor");
        }
      }
    } catch (err) {
      console.error(err);
      alert("Error deleting doctor");
    }
  }
};

const blockDoctor = async (doctor) => {
  const token = auth.getToken();
  if (!token) {
    alert("Please login first");
    router.push("/login");
    return;
  }

  if (confirm(`Are you sure you want to block ${doctor.username}?`)) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/admin/users/${doctor.id}/block`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (response.ok) {
        alert("Doctor blocked successfully");
        fetchDoctors();
      } else {
        if (response.status === 401) {
          alert("Please login again");
          auth.clearAll();
          router.push("/login");
        } else if (response.status === 403) {
          alert("Unauthorized");
        } else {
          alert("Failed to block doctor");
        }
      }
    } catch (err) {
      console.error(err);
      alert("Error blocking doctor");
    }
  }
};
</script>


<style scoped>
.doctor-card {
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

.doctor-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #3b82f6, #1d4ed8);
}

.doctor-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border-color: rgba(59, 130, 246, 0.2);
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
  border: 4px solid #e0f2fe;
  box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.15);
  transition: all 0.3s ease;
}

.avatar:hover {
  transform: scale(1.05);
}

.doctor-name {
  font-size: 1.375rem;
  color: #1e293b;
  font-weight: 700;
  margin-bottom: 4px;
  letter-spacing: 0.025em;
  line-height: 1.4;
}

.doctor-email {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 16px;
  letter-spacing: 0.025em;
  line-height: 1.5;
}

.doctor-info p {
  margin-bottom: 8px;
  font-size: 0.875rem;
  color: #475569;
  letter-spacing: 0.025em;
  line-height: 1.6;
}

.badge-blue {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  padding: 6px 12px;
  border-radius: 20px;
  color: #1e40af;
  font-size: 0.75rem;
  font-weight: 600;
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.badge-green {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  padding: 6px 12px;
  border-radius: 20px;
  color: #166534;
  font-size: 0.75rem;
  font-weight: 600;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.action-buttons {
  display: flex;
  gap: 12px;
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

.edit-btn {
  background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
  color: #0c4a6e;
  border: 1px solid rgba(14, 165, 233, 0.2);
}

.edit-btn:hover {
  background: linear-gradient(135deg, #bae6fd 0%, #7dd3fc 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(14, 165, 233, 0.3);
}

.delete-btn {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #991b1b;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.delete-btn:hover {
  background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3);
}

.block-btn {
  background: linear-gradient(135deg, #fef9c3 0%, #fde68a 100%);
  color: #92400e;
  border: 1px solid rgba(245, 158, 11, 0.2);
}

.block-btn:hover {
  background: linear-gradient(135deg, #fde68a 0%, #fcd34d 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%);
  border-radius: 16px;
  padding: 0;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(148, 163, 184, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 28px 16px;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.modal-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: 0.025em;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  color: #64748b;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #dc2626;
}

.modal-body {
  padding: 24px 28px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  color: #374151;
  font-weight: 600;
  font-size: 0.875rem;
  letter-spacing: 0.025em;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 8px;
  font-size: 0.875rem;
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  background: rgba(255, 255, 255, 1);
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 32px;
}

.cancel-btn {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  color: #475569;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.cancel-btn:hover {
  background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(148, 163, 184, 0.2);
}

.save-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.save-btn:hover {
  background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}
</style>
