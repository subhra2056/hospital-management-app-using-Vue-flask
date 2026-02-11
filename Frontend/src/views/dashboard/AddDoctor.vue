<template>
  <div class="container">
    <div class="row justify-content-center align-items-center min-vh-100">
      <div class="col-12 col-sm-10 col-md-8 col-lg-6">

        <div class="card shadow-lg border-0 rounded-4">
          <div class="card-body p-4">

            <h3 class="text-center text-primary mb-4 fw-bold">
              Doctor Registration
            </h3>

            <form @submit.prevent="handleDoctorRegister">

              <!-- Username -->
              <div class="mb-3">
                <label class="form-label">Username</label>
                <input
                  type="text"
                  class="form-control"
                  placeholder="Enter Username"
                  v-model="username"
                  required
                />
              </div>

              <!-- Email -->
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input
                  type="email"
                  class="form-control"
                  placeholder="Enter Email"
                  v-model="email"
                  required
                />
              </div>

              <!-- Password -->
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Password</label>
                  <input
                    type="password"
                    class="form-control"
                    placeholder="Create a password"
                    v-model="password"
                    @input="validatePassword"
                    required
                  />

                  <p v-if="passwordErrorMessage" class="text-danger password-error">
                    {{ passwordErrorMessage }}
                  </p>
                  <p v-if="passwordStrength" class="password-strength">
                    {{ passwordStrength }}
                  </p>
                </div>

                <div class="col-md-6 mb-3">
                  <label class="form-label">Confirm Password</label>
                  <input
                    type="password"
                    class="form-control"
                    placeholder="Re-enter password"
                    v-model="confirmPassword"
                    required
                  />
                  <p
                    v-if="passwordMatchMessage"
                    :class="isPasswordMatch ? 'password-strength' : 'text-danger password-error'"
                  >
                    {{ passwordMatchMessage }}
                  </p>
                </div>
              </div>

              <!-- Department -->
              <div class="mb-3">
                <label class="form-label">Department</label>
                <select
                  class="form-select"
                  v-model="department_id"
                  required
                  :disabled="loadingDepartments"
                >
                  <option disabled value="">Select Department</option>
                  <option
                    v-for="dept in departments"
                    :key="dept.id"
                    :value="dept.id"
                  >
                    {{ dept.name }}
                  </option>
                </select>
                <div v-if="loadingDepartments" class="mt-2">
                  <small class="text-muted">Loading departments...</small>
                </div>
              </div>

              <!-- Specialization -->
              <div class="mb-3">
                <label class="form-label">Specialization</label>
                <input
                  type="text"
                  class="form-control"
                  placeholder="Enter Specialization"
                  v-model="specialization"
                  required
                />
              </div>

              <!-- Experience -->
              <div class="mb-3">
                <label class="form-label">Experience (Years)</label>
                <input
                  type="number"
                  class="form-control"
                  min="0"
                  placeholder="Enter Experience"
                  v-model="experience"
                  required
                />
              </div>

              <!-- Gender -->
              <div class="mb-3">
                <label class="form-label">Gender</label>
                <select class="form-select" v-model="gender" required>
                  <option disabled value="">Select Gender</option>
                  <option>Male</option>
                  <option>Female</option>
                  <option>Other</option>
                </select>
              </div>

              <!-- Error Message -->
              <p v-if="errorMessage" class="text-danger fw-semibold text-center">
                {{ errorMessage }}
              </p>

              <!-- Submit Button -->
              <div class="text-center mt-4">
                <button type="submit" class="btn btn-primary px-4 py-2 fw-semibold">
                  Register Doctor
                </button>
              </div>

            </form>

          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import auth from "../../utils/auth";

const router = useRouter();

// Form fields
const username = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const department_id = ref("");
const specialization = ref("");
const experience = ref("");
const gender = ref("");

// Departments data
const departments = ref([]);
const loadingDepartments = ref(true);

// Load departments on component mount
onMounted(async () => {
  try {
    const token = auth.getToken();
    const response = await fetch("http://localhost:5000/api/admin/departments", {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (response.ok) {
      const data = await response.json();
      departments.value = data.departments || [];
    } else {
      console.error("Failed to load departments");
    }
  } catch (error) {
    console.error("Error loading departments:", error);
  } finally {
    loadingDepartments.value = false;
  }
});

// Password validation
const passwordErrorMessage = ref("");
const passwordStrength = ref("");

const validatePassword = () => {
  passwordErrorMessage.value = "";
  passwordStrength.value = "";

  if (!password.value) return;

  if (password.value.length <= 6) {
    passwordErrorMessage.value = "Too short (minimum 7 characters)";
  } else if (password.value.length > 6 && password.value.length <= 20) {
    passwordStrength.value = "Good password";
  } else {
    passwordErrorMessage.value = "Password too long";
  }
};

// Password match
const passwordMatchMessage = computed(() => {
  if (!confirmPassword.value) return "";

  return password.value === confirmPassword.value
    ? "Passwords match ✅"
    : "Passwords do not match ❌";
});

const isPasswordMatch = computed(() => {
  return password.value === confirmPassword.value && confirmPassword.value !== "";
});

// General error message
const errorMessage = ref("");

// Backend Submission
const handleDoctorRegister = async () => {
  errorMessage.value = "";

  if (!isPasswordMatch.value) {
    errorMessage.value = "Passwords do not match.";
    return;
  }

  try {
    const token = auth.getToken();
    const response = await fetch("http://localhost:5000/api/doctor/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },

      body: JSON.stringify({
        username: username.value,
        email: email.value,
        password: password.value,
        department_id: department_id.value,
        specialization: specialization.value,
        experience_years: experience.value,
        gender: gender.value,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.message;
      return;
    }

    router.push("/admin/doctor-list");

  } catch (error) {
    errorMessage.value = "Registration failed. Try again.";
  }
};
</script>

