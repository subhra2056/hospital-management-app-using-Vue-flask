<template>
  <div class="availability-container">
    <div class="availability-header">
      <h2 class="availability-title">Manage Availability</h2>
      <p class="availability-subtitle">View, edit, and manage your availability schedule</p>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="error" class="error-container">
      <div class="alert alert-danger">{{ error }}</div>
    </div>

    <div v-else class="availability-content">
      <!-- Add New Availability Button -->
      <div class="add-availability-section">
        <button class="btn btn-primary" @click="showAddModal = true">
          <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          Add Availability
        </button>
      </div>

      <!-- Availability List -->
      <div v-if="availabilities.length === 0" class="no-availability">
        <div class="no-availability-icon">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <h4>No Availability Set</h4>
        <p>You haven't set any availability slots yet. Add your first availability to start accepting appointments.</p>
      </div>

      <div v-else class="availability-grid">
        <div
          v-for="availability in availabilities"
          :key="availability.id"
          class="availability-card"
        >
          <div class="availability-header">
            <div class="date-info">
              <h5 class="date">{{ formatDate(availability.date) }}</h5>
              <span class="day">{{ getDayOfWeek(availability.date) }}</span>
            </div>
            <div class="status-badge" :class="availability.is_booked ? 'booked' : 'available'">
              {{ availability.is_booked ? 'Booked' : 'Available' }}
            </div>
          </div>

          <div class="time-info">
            <div class="time-slot">
              <svg class="time-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <span>{{ formatTime(availability.start_time) }} - {{ formatTime(availability.end_time) }}</span>
            </div>
          </div>

          <div class="availability-actions">
            <button
              class="btn btn-outline-primary btn-sm"
              @click="editAvailability(availability)"
              :disabled="availability.is_booked"
            >
              <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
              </svg>
              Edit
            </button>
            <button
              class="btn btn-outline-danger btn-sm"
              @click="deleteAvailability(availability.id)"
              :disabled="availability.is_booked"
            >
              <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
              </svg>
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Availability Modal -->
    <div v-if="showAddModal || showEditModal" class="modal-overlay" @click="closeModals">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h5 class="modal-title">{{ showEditModal ? 'Edit Availability' : 'Add Availability' }}</h5>
          <button class="close-btn" @click="closeModals">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="saveAvailability">
            <div class="form-group">
              <label class="form-label">Date</label>
              <input
                type="date"
                class="form-control"
                v-model="availabilityForm.date"
                :min="minDate"
                required
              />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Start Time</label>
                <input
                  type="time"
                  class="form-control"
                  v-model="availabilityForm.start_time"
                  required
                />
              </div>

              <div class="form-group">
                <label class="form-label">End Time</label>
                <input
                  type="time"
                  class="form-control"
                  v-model="availabilityForm.end_time"
                  required
                />
              </div>
            </div>

            <div v-if="timeError" class="error-message">
              {{ timeError }}
            </div>

            <div class="modal-actions">
              <button type="button" class="btn btn-secondary" @click="closeModals">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="!!timeError">
                {{ showEditModal ? 'Update' : 'Add' }} Availability
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import auth from "../../utils/auth";

const availabilities = ref([]);
const loading = ref(true);
const error = ref("");
const showAddModal = ref(false);
const showEditModal = ref(false);
const editingAvailability = ref(null);

const availabilityForm = ref({
  date: "",
  start_time: "",
  end_time: ""
});

const timeError = computed(() => {
  if (!availabilityForm.value.start_time || !availabilityForm.value.end_time) return "";
  if (availabilityForm.value.start_time >= availabilityForm.value.end_time) {
    return "End time must be after start time";
  }
  return "";
});

const minDate = computed(() => {
  const today = new Date();
  return today.toISOString().split('T')[0];
});

const loadAvailabilities = async () => {
  loading.value = true;
  error.value = "";

  try {
    const token = auth.getToken();
    const response = await fetch("http://localhost:5000/api/doctor/availability", {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) {
      throw new Error("Failed to load availabilities");
    }

    const data = await response.json();
    availabilities.value = data.availabilities || [];
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const saveAvailability = async () => {
  if (timeError.value) return;

  try {
    const token = auth.getToken();
    const method = showEditModal.value ? "PUT" : "POST";
    const url = showEditModal.value
      ? `http://localhost:5000/api/doctor/availability/edit/${editingAvailability.value.id}`
      : "http://localhost:5000/api/doctor/availability";

    const response = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(availabilityForm.value),
    });

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.message || "Failed to save availability");
    }

    await loadAvailabilities();
    closeModals();
  } catch (err) {
    error.value = err.message;
  }
};

const editAvailability = (availability) => {
  editingAvailability.value = availability;
  availabilityForm.value = {
    date: availability.date,
    start_time: availability.start_time,
    end_time: availability.end_time
  };
  showEditModal.value = true;
};

const deleteAvailability = async (id) => {
  if (!confirm("Are you sure you want to delete this availability slot?")) return;

  try {
    const token = auth.getToken();
    const response = await fetch(`http://localhost:5000/api/doctor/availability/edit/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) {
      throw new Error("Failed to delete availability");
    }

    await loadAvailabilities();
  } catch (err) {
    error.value = err.message;
  }
};

const closeModals = () => {
  showAddModal.value = false;
  showEditModal.value = false;
  editingAvailability.value = null;
  availabilityForm.value = { date: "", start_time: "", end_time: "" };
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

const getDayOfWeek = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { weekday: 'long' });
};

const formatTime = (timeString) => {
  const [hours, minutes] = timeString.split(':');
  const date = new Date();
  date.setHours(hours, minutes);
  return date.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  });
};

onMounted(() => {
  loadAvailabilities();
});
</script>

<style scoped>
.availability-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.availability-header {
  text-align: center;
  margin-bottom: 3rem;
}

.availability-title {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #5e63b6 0%, #4a50a0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.75rem;
  letter-spacing: -0.5px;
}

.availability-subtitle {
  color: #64748b;
  font-size: 1.125rem;
  margin: 0;
  font-weight: 500;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.error-container {
  margin-top: 2rem;
  text-align: center;
}

.add-availability-section {
  margin-bottom: 2rem;
  text-align: center;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.2s ease;
}

.btn-icon {
  width: 18px;
  height: 18px;
}

.no-availability {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.no-availability-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  color: #cbd5e1;
}

.no-availability h4 {
  color: #475569;
  margin-bottom: 1rem;
}

.no-availability p {
  color: #64748b;
  max-width: 400px;
  margin: 0 auto;
}

.availability-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.availability-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(94, 99, 182, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.availability-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.availability-card .availability-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  text-align: left;
}

.date-info h5 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
}

.date-info .day {
  display: block;
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.status-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge.available {
  background: #dcfce7;
  color: #166534;
}

.status-badge.booked {
  background: #fee2e2;
  color: #dc2626;
}

.time-info {
  margin-bottom: 1.5rem;
}

.time-slot {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #475569;
  font-weight: 500;
}

.time-icon {
  width: 20px;
  height: 20px;
  color: #5e63b6;
}

.availability-actions {
  display: flex;
  gap: 0.75rem;
}

.availability-actions .btn {
  flex: 1;
  justify-content: center;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.availability-actions .btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
}

.close-btn {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: #64748b;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.close-btn:hover {
  background: #f1f5f9;
}

.modal-body {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-label {
  display: block;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.form-control:focus {
  outline: none;
  border-color: #5e63b6;
  box-shadow: 0 0 0 3px rgba(94, 99, 182, 0.1);
}

.error-message {
  color: #dc2626;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .availability-container {
    padding: 1rem;
  }

  .availability-title {
    font-size: 2rem;
  }

  .availability-grid {
    grid-template-columns: 1fr;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .modal-body {
    padding: 1.5rem;
  }

  .modal-header {
    padding: 1.5rem;
  }
}
</style>