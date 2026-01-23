<template>
  <div class="profile-container">
    <div class="profile-header">
      <h2 class="profile-title text-center">{{ isEditing ? 'Edit Profile' : 'My Profile' }}</h2>
      <p class="profile-subtitle text-center">{{ isEditing ? 'Update your account information' : 'View and manage your account information' }}</p>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="error" class="error-container">
      <div class="alert alert-danger">{{ error }}</div>
    </div>

    <div v-else class="profile-content">
      <div class="profile-main-grid">
        <div class="profile-sidebar-card">
          <div class="profile-avatar-wrapper">
            <div class="profile-avatar-container">
              <img v-if="userRole === 'doctor'" :src="doctorIcon" alt="Doctor" />
              <img v-else-if="userRole === 'patient'" :src="patientIcon" alt="Patient" />
              <img v-else :src="userIcon" alt="Admin" />
              <div class="status-dot"></div>
            </div>
            <div class="profile-badge-modern" :class="getRoleBadgeClass()">
              {{ userRole.toUpperCase() }}
            </div>
          </div>
          
          <div class="profile-info-compact">
            <h3 class="profile-name-modern">{{ profileData.username }}</h3>
            <p class="profile-email-modern">{{ profileData.email }}</p>
          </div>

          <div class="profile-stats">
            <div class="stat-item-modern">
              <div class="stat-icon-modern">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
              </div>
              <div class="stat-content-modern">
                <span class="stat-label-modern">Joined</span>
                <span class="stat-value-modern">{{ formatDate(profileData.created_at) }}</span>
              </div>
            </div>
            <div class="stat-item-modern">
              <div class="stat-icon-modern">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div class="stat-content-modern">
                <span class="stat-label-modern">Status</span>
                <span class="stat-value-modern status-active">{{ profileData.active ? 'Active' : 'Inactive' }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="profile-details-section">
          <div class="details-card-modern">
            <div class="card-header-gradient">
              <h4 class="card-title-modern">
                <svg class="title-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
                {{ isEditing ? 'Edit Details' : 'Profile Details' }}
              </h4>
            </div>
            <div class="card-body-padded">
              <!-- VIEW MODE -->
              <div v-if="!isEditing && userRole === 'patient' && profileData.profile" class="details-grid-modern">
                <div class="detail-card-item">
                  <div class="detail-icon-wrapper">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <label class="detail-label-modern">Age</label>
                    <div class="detail-value-modern">{{ profileData.profile.age || 'Not set' }}</div>
                  </div>
                </div>
                <div class="detail-card-item">
                  <div class="detail-icon-wrapper">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <label class="detail-label-modern">Gender</label>
                    <div class="detail-value-modern">{{ profileData.profile.gender || 'Not set' }}</div>
                  </div>
                </div>
                <div class="detail-card-item">
                  <div class="detail-icon-wrapper">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <label class="detail-label-modern">Phone</label>
                    <div class="detail-value-modern">{{ profileData.profile.phone || 'Not set' }}</div>
                  </div>
                </div>
                <div class="detail-card-item full-width">
                  <div class="detail-icon-wrapper">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <label class="detail-label-modern">Address</label>
                    <div class="detail-value-modern">{{ profileData.profile.address || 'Not set' }}</div>
                  </div>
                </div>
              </div>

              <div v-else-if="userRole === 'doctor' && profileData.profile" class="details-grid-modern">
                <div class="detail-card-item">
                  <div class="detail-icon-wrapper">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <label class="detail-label-modern">Department</label>
                    <div class="detail-value-modern">{{ profileData.profile.department || 'Not set' }}</div>
                  </div>
                </div>
                <div class="detail-card-item">
                  <div class="detail-icon-wrapper">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <label class="detail-label-modern">Specialization</label>
                    <div class="detail-value-modern">{{ profileData.profile.specialization || 'Not set' }}</div>
                  </div>
                </div>
                <div class="detail-card-item">
                  <div class="detail-icon-wrapper">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <label class="detail-label-modern">Experience</label>
                    <div class="detail-value-modern">{{ profileData.profile.experience_years ? profileData.profile.experience_years + ' years' : 'Not set' }}</div>
                  </div>
                </div>
                <div class="detail-card-item">
                  <div class="detail-icon-wrapper">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <label class="detail-label-modern">Gender</label>
                    <div class="detail-value-modern">{{ profileData.profile.gender || 'Not set' }}</div>
                  </div>
                </div>
              </div>

              <div v-else-if="userRole === 'admin'" class="details-grid-modern">
                <div class="detail-card-item full-width admin-card">
                  <div class="detail-icon-wrapper admin-icon">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <label class="detail-label-modern">Role</label>
                    <div class="detail-value-modern">Administrator - Full System Access</div>
                  </div>
                </div>
                <div class="detail-card-item full-width admin-card">
                  <div class="detail-icon-wrapper admin-icon">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <label class="detail-label-modern">Permissions</label>
                    <div class="detail-value-modern">Can manage doctors, patients, appointments, and all system settings</div>
                  </div>
                </div>
              </div>

              <!-- EDIT MODE FOR PATIENTS -->
              <div v-if="isEditing && userRole === 'patient'" class="edit-form-modern">
                <div v-if="saveMessage" class="alert" :class="saveMessage.includes('success') ? 'alert-success' : 'alert-danger'">
                  {{ saveMessage }}
                </div>
                <div class="form-grid">
                  <div class="form-group-modern">
                    <label class="form-label-modern">Age</label>
                    <input 
                      type="number" 
                      class="form-input-modern" 
                      v-model="editForm.age"
                      placeholder="Enter your age"
                      min="1"
                      max="150"
                    />
                  </div>
                  <div class="form-group-modern">
                    <label class="form-label-modern">Gender</label>
                    <select class="form-input-modern" v-model="editForm.gender">
                      <option value="">Select gender</option>
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  <div class="form-group-modern">
                    <label class="form-label-modern">Phone</label>
                    <input 
                      type="tel" 
                      class="form-input-modern" 
                      v-model="editForm.phone"
                      placeholder="Enter your phone number"
                    />
                  </div>
                  <div class="form-group-modern full-width">
                    <label class="form-label-modern">Address</label>
                    <textarea 
                      class="form-input-modern form-textarea" 
                      v-model="editForm.address"
                      placeholder="Enter your address"
                      rows="3"
                    ></textarea>
                  </div>
                </div>
              </div>

              <div class="profile-actions-modern">
                <button 
                  v-if="userRole === 'patient' && !isEditing"
                  class="action-btn-modern primary-btn"
                  @click="startEditing"
                >
                  <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                  </svg>
                  Edit Profile
                </button>
                <button 
                  v-if="isEditing"
                  class="action-btn-modern primary-btn"
                  @click="saveProfile"
                  :disabled="saving"
                >
                  <svg v-if="!saving" class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
                  {{ saving ? 'Saving...' : 'Save Changes' }}
                </button>
                <button 
                  v-if="isEditing"
                  class="action-btn-modern danger-btn"
                  @click="cancelEditing"
                  :disabled="saving"
                >
                  <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                  Cancel
                </button>
                <button 
                  v-if="!isEditing"
                  class="action-btn-modern secondary-btn"
                  @click="goToDashboard"
                >
                  <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
                  </svg>
                  Back to Dashboard
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import doctorIcon from "../../assets/doctor.png";
import patientIcon from "../../assets/patient.png";
import userIcon from "../../assets/user.png";
import auth from "../../utils/auth";

const router = useRouter();
const loading = ref(true);
const error = ref("");
const profileData = ref({});
const isEditing = ref(false);
const saving = ref(false);
const saveMessage = ref("");
const editForm = ref({
  age: "",
  gender: "",
  phone: "",
  address: ""
});

const userRole = computed(() => {
  return profileData.value.role || auth.getRole() || "";
});

const getToken = () => auth.getToken();

const loadProfile = async () => {
  loading.value = true;
  error.value = "";
  
  try {
    const response = await fetch("http://localhost:5000/api/user/profile", {
      headers: { Authorization: `Bearer ${getToken()}` }
    });

    if (!response.ok) {
      throw new Error("Failed to load profile");
    }

    const data = await response.json();
    profileData.value = data;
  } catch (err) {
    error.value = "Failed to load profile. Please try again.";
    console.error("Profile load error:", err);
  } finally {
    loading.value = false;
  }
};

const formatDate = (dateStr) => {
  if (!dateStr) return "N/A";
  try {
    const date = new Date(dateStr);
    return date.toLocaleDateString("en-US", { 
      month: "long", 
      day: "numeric", 
      year: "numeric" 
    });
  } catch (e) {
    return dateStr;
  }
};

const getRoleBadgeClass = () => {
  const role = userRole.value.toLowerCase();
  return {
    "badge-admin": role === "admin",
    "badge-doctor": role === "doctor",
    "badge-patient": role === "patient"
  };
};

const startEditing = () => {
  // Populate form with current profile data
  if (profileData.value.profile) {
    editForm.value = {
      age: profileData.value.profile.age || "",
      gender: profileData.value.profile.gender || "",
      phone: profileData.value.profile.phone || "",
      address: profileData.value.profile.address || ""
    };
  }
  isEditing.value = true;
  saveMessage.value = "";
};

const cancelEditing = () => {
  isEditing.value = false;
  saveMessage.value = "";
};

const saveProfile = async () => {
  saving.value = true;
  saveMessage.value = "";
  
  try {
    const response = await fetch("http://localhost:5000/api/user/profile", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getToken()}`
      },
      body: JSON.stringify({
        age: editForm.value.age,
        gender: editForm.value.gender,
        phone: editForm.value.phone,
        address: editForm.value.address
      })
    });

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.message || "Failed to update profile");
    }

    saveMessage.value = "Profile updated successfully!";
    
    // Reload profile to get updated data
    await loadProfile();
    
    // Exit edit mode after short delay
    setTimeout(() => {
      isEditing.value = false;
      saveMessage.value = "";
    }, 1500);
    
  } catch (err) {
    saveMessage.value = err.message || "Failed to update profile. Please try again.";
    console.error("Profile update error:", err);
  } finally {
    saving.value = false;
  }
};

const goToDashboard = () => {
  const role = userRole.value.toLowerCase();
  if (role === "admin") {
    router.push("/admin/dashboard");
  } else if (role === "doctor") {
    router.push("/doctor/dashboard");
  } else if (role === "patient") {
    router.push("/patient/dashboard");
  } else {
    router.push("/");
  }
};

onMounted(() => {
  loadProfile();
});
</script>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem 2rem 1rem;
}

.profile-header {
  margin-bottom: 2.5rem;
}

.profile-title {
  font-size: 2.25rem;
  font-weight: 800;
  background: linear-gradient(135deg, #5e63b6 0%, #4a50a0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  letter-spacing: -0.5px;
}

.profile-subtitle {
  color: #64748b;
  font-size: 1rem;
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
}

.profile-content {
  margin-top: 1rem;
}

.profile-main-grid {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 2rem;
  align-items: start;
}

.profile-sidebar-card {
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(94, 99, 182, 0.1);
  height: fit-content;
  position: sticky;
  top: 2rem;
}

.profile-avatar-wrapper {
  text-align: center;
  margin-bottom: 1.5rem;
}

.profile-avatar-container {
  position: relative;
  width: 140px;
  height: 140px;
  margin: 0 auto 1rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #5e63b6 0%, #4a50a0 100%);
  padding: 4px;
  box-shadow: 0 8px 24px rgba(94, 99, 182, 0.3);
}

.profile-avatar-container img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid white;
}

.status-dot {
  position: absolute;
  bottom: 8px;
  right: 8px;
  width: 20px;
  height: 20px;
  background: #10b981;
  border: 3px solid white;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.4);
}

.profile-badge-modern {
  display: inline-block;
  padding: 0.5rem 1.25rem;
  border-radius: 25px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.badge-admin {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #991b1b;
}

.badge-doctor {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #1e40af;
}

.badge-patient {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  color: #065f46;
}

.profile-info-compact {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e2e8f0;
}

.profile-name-modern {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  line-height: 1.3;
}

.profile-email-modern {
  font-size: 0.9375rem;
  color: #64748b;
  margin: 0;
  word-break: break-word;
}

.profile-stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.stat-item-modern {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.stat-item-modern:hover {
  border-color: #5e63b6;
  box-shadow: 0 2px 8px rgba(94, 99, 182, 0.1);
  transform: translateY(-2px);
}

.stat-icon-modern {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #5e63b6 0%, #4a50a0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.stat-icon-modern svg {
  width: 20px;
  height: 20px;
}

.stat-content-modern {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
}

.stat-label-modern {
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value-modern {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #1e293b;
}

.stat-value-modern.status-active {
  color: #10b981;
}

.profile-details-section {
  min-width: 0;
}

.details-card-modern {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(94, 99, 182, 0.1);
  overflow: hidden;
}

.card-header-gradient {
  padding: 1.75rem 2rem;
  background: linear-gradient(135deg, #5e63b6 0%, #4a50a0 100%);
  color: white;
}

.card-title-modern {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.title-icon {
  width: 24px;
  height: 24px;
}

.card-body-padded {
  padding: 2rem;
}

.details-grid-modern {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
  margin-bottom: 2rem;
}

.detail-card-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.25rem;
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.detail-card-item:hover {
  border-color: #5e63b6;
  box-shadow: 0 4px 12px rgba(94, 99, 182, 0.15);
  transform: translateY(-2px);
}

.detail-card-item.full-width {
  grid-column: 1 / -1;
}

.detail-card-item.admin-card {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-color: #fbbf24;
}

.detail-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #5e63b6 0%, #4a50a0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(94, 99, 182, 0.3);
}

.detail-icon-wrapper svg {
  width: 24px;
  height: 24px;
}

.detail-icon-wrapper.admin-icon {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
}

.detail-content {
  flex: 1;
  min-width: 0;
}

.detail-label-modern {
  display: block;
  font-size: 0.75rem;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.5rem;
}

.detail-value-modern {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  line-height: 1.5;
  word-break: break-word;
}

.profile-actions-modern {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.action-btn-modern {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.75rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn-modern.primary-btn {
  background: linear-gradient(135deg, #5e63b6 0%, #4a50a0 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(94, 99, 182, 0.3);
}

.action-btn-modern.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(94, 99, 182, 0.4);
}

.action-btn-modern.secondary-btn {
  background: white;
  color: #64748b;
  border: 2px solid #e2e8f0;
}

.action-btn-modern.secondary-btn:hover {
  background: #f8fafc;
  border-color: #5e63b6;
  color: #5e63b6;
  transform: translateY(-2px);
}

.btn-icon {
  width: 18px;
  height: 18px;
}

@media (max-width: 1024px) {
  .profile-container {
    padding: 0 1rem 2rem 1rem;
  }

  .profile-main-grid {
    grid-template-columns: 300px 1fr;
    gap: 1.5rem;
  }
}

@media (max-width: 768px) {
  .profile-container {
    padding: 0 0.75rem 2rem 0.75rem;
  }

  .profile-main-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .profile-sidebar-card {
    position: static;
    margin-bottom: 2rem;
  }

  .profile-title {
    font-size: 1.75rem;
  }

  .details-grid-modern {
    grid-template-columns: 1fr;
  }

  .profile-actions-modern {
    flex-direction: column;
  }

  .action-btn-modern {
    width: 100%;
    justify-content: center;
  }

  .profile-avatar-container {
    width: 120px;
    height: 120px;
  }
}

/* Edit Form Styles */
.edit-form-modern {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.form-group-modern {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group-modern.full-width {
  grid-column: span 2;
}

.form-label-modern {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.form-input-modern {
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  background: #f8fafc;
}

.form-input-modern:focus {
  outline: none;
  border-color: #5e63b6;
  background: white;
  box-shadow: 0 0 0 4px rgba(94, 99, 182, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.danger-btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.danger-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.3);
}

.alert {
  padding: 1rem 1.25rem;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  font-weight: 500;
}

.alert-success {
  background: #ecfdf5;
  color: #059669;
  border: 1px solid #a7f3d0;
}

.alert-danger {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-group-modern.full-width {
    grid-column: span 1;
  }
}
</style>
