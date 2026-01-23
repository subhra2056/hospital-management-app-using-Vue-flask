<template>
  <div class="container">
    <h2 class="mb-4 text-center text-primary fw-bold">Patient List</h2>

    <div v-if="loading" class="text-center mt-5">
      <div class="spinner-border text-primary"></div>
      <p class="mt-3">Loading patients...</p>
    </div>

    <div v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </div>

    <div class="row">
      <div
        v-for="patient in patients"
        :key="patient.id"
        class="col-md-4 mb-4"
      >
        <div class="patient-card shadow-lg">
          <div class="card-header-area">
            <img class="avatar" :src="patientIcon" />
            <h5 class="patient-name">{{ patient.username }}</h5>
            <p class="patient-email">{{ patient.email }}</p>
          </div>

          <div class="patient-info">
            <p><strong>Age:</strong> {{ patient.age }}</p>
            <p><strong>Gender:</strong> {{ patient.gender }}</p>
            <p><strong>Phone:</strong> {{ patient.phone }}</p>
            <p><strong>Address:</strong> {{ patient.address }}</p>
          </div>

          <div class="action-buttons mt-3">
            <button class="btn edit-btn" @click="editPatient(patient)"> Edit</button>
            <button class="btn delete-btn" @click="deletePatient(patient)"> Delete </button>
            <button class="btn block-btn" @click="blockPatient(patient)"> Block </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Patient Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click="closeEditModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Edit Patient</h3>
          <button class="close-btn" @click="closeEditModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitEditPatient">
            <div class="form-group">
              <label for="edit-username">Username</label>
              <input type="text" id="edit-username" v-model="editForm.username" required />
            </div>
            <div class="form-group">
              <label for="edit-email">Email</label>
              <input type="email" id="edit-email" v-model="editForm.email" required />
            </div>
            <div class="form-group">
              <label for="edit-age">Age</label>
              <input type="number" id="edit-age" v-model.number="editForm.age" required />
            </div>
            <div class="form-group">
              <label for="edit-gender">Gender</label>
              <select id="edit-gender" v-model="editForm.gender" required>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div class="form-group">
              <label for="edit-phone">Phone</label>
              <input type="text" id="edit-phone" v-model="editForm.phone" required />
            </div>
            <div class="form-group">
              <label for="edit-address">Address</label>
              <textarea id="edit-address" v-model="editForm.address" required></textarea>
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
import patientIcon from "../../assets/patient.png";
import auth from "../../utils/auth";

const router = useRouter();
const patients = ref([]);
const loading = ref(false);
const errorMessage = ref("");
const showEditModal = ref(false);
const editForm = ref({
  id: null,
  username: "",
  email: "",
  age: "",
  gender: "",
  phone: "",
  address: ""
});

const fetchPatients = async () => {
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
    patients.value = data.patients.filter(p => p.active);

  } catch (err) {
    errorMessage.value = "Failed to load patients.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchPatients();
});

const editPatient = (patient) => {
  editForm.value = {
    id: patient.id,
    username: patient.username,
    email: patient.email,
    age: patient.age,
    gender: patient.gender,
    phone: patient.phone,
    address: patient.address
  };
  showEditModal.value = true;
};

const submitEditPatient = async () => {
  const token = auth.getToken();
  if (!token) {
    alert("Please login first");
    router.push("/login");
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:5000/api/admin/patients/${editForm.value.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        username: editForm.value.username,
        email: editForm.value.email,
        age: editForm.value.age,
        gender: editForm.value.gender,
        phone: editForm.value.phone,
        address: editForm.value.address
      })
    });

    if (response.ok) {
      alert("Patient updated successfully");
      showEditModal.value = false;
      fetchPatients();
    } else {
      if (response.status === 401) {
        alert("Please login again");
        auth.clearAll();
        router.push("/login");
      } else if (response.status === 403) {
        alert("Unauthorized");
      } else {
        const errorData = await response.json();
        alert(errorData.message || "Failed to update patient");
      }
    }
  } catch (err) {
    console.error(err);
    alert("Error updating patient");
  }
};

const closeEditModal = () => {
  showEditModal.value = false;
};

const deletePatient = async (patient) => {
  const token = auth.getToken();
  if (!token) {
    alert("Please login first");
    router.push("/login");
    return;
  }

  if (confirm(`Are you sure you want to delete ${patient.username}?`)) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/admin/patients/${patient.id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (response.ok) {
        alert("Patient deleted successfully");
        fetchPatients();
      } else {
        if (response.status === 401) {
          alert("Please login again");
          auth.clearAll();
          router.push("/login");
        } else if (response.status === 403) {
          alert("Unauthorized");
        } else {
          alert("Failed to delete patient");
        }
      }
    } catch (err) {
      console.error(err);
      alert("Error deleting patient");
    }
  }
};

const blockPatient = async (patient) => {
  const token = auth.getToken();
  if (!token) {
    alert("Please login first");
    router.push("/login");
    return;
  }

  if (confirm(`Are you sure you want to block ${patient.username}?`)) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/admin/users/${patient.id}/block`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (response.ok) {
        alert("Patient blocked successfully");
        fetchPatients();
      } else {
        if (response.status === 401) {
          alert("Please login again");
          auth.clearAll();
          router.push("/login");
        } else if (response.status === 403) {
          alert("Unauthorized");
        } else {
          alert("Failed to block patient");
        }
      }
    } catch (err) {
      console.error(err);
      alert("Error blocking patient");
    }
  }
};

</script>

<style scoped>
.patient-card {
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

.patient-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #10b981, #059669);
}

.patient-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border-color: rgba(16, 185, 129, 0.2);
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
  border: 4px solid #d1fae5;
  box-shadow: 0 4px 14px 0 rgba(16, 185, 129, 0.15);
  transition: all 0.3s ease;
}

.avatar:hover {
  transform: scale(1.05);
}

.patient-name {
  font-size: 1.375rem;
  color: #1e293b;
  font-weight: 700;
  margin-bottom: 4px;
  letter-spacing: 0.025em;
  line-height: 1.4;
}

.patient-email {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 16px;
  letter-spacing: 0.025em;
  line-height: 1.5;
}

.patient-info p {
  margin-bottom: 8px;
  font-size: 0.875rem;
  color: #475569;
  letter-spacing: 0.025em;
  line-height: 1.6;
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
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 8px;
  font-size: 0.875rem;
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
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
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.save-btn:hover {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}
</style>
