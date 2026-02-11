<template>
  <div class="login-wrapper">
    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-100">

        <div class="col-12 col-sm-11 col-md-9 col-lg-6">
          <div class="login-card shadow-lg">

            <!-- Header -->
            <div class="text-center mb-4">
              <div class="d-flex justify-content-center align-items-center gap-2">
                <img :src="logo" alt="Healthease Logo" class="login-logo" />
                <h3 class="fw-bold text-white mb-0">Medi<span style="color: #5DD3B6;">core</span> Sign Up</h3>
              </div>
              <p class="text-light small mt-1"></p>
            </div>

            <!-- Profile Form -->
            <form @submit.prevent="handleSignUp">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label text-light">Username</label>
                  <input type="text" class="form-control" placeholder="Enter your username" v-model="username"
                    required />
                </div>

                <div class="col-md-6 mb-3">
                  <label class="form-label text-light">Email</label>
                  <input type="email" class="form-control" placeholder="Enter your email" v-model="email" required />
                </div>
              </div>

              <!--Password-->
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label text-light">Password</label>
                  <input type="password" class="form-control" placeholder="Create a password" v-model="password"
                    @input="validatePassword" required />

                  <p v-if="passwordErrorMessage" class="text-danger password-error">{{ passwordErrorMessage }}</p>
                  <p v-if="passwordStrength" class="password-strength">{{ passwordStrength }}</p>

                </div>

                <div class="col-md-6 mb-3">
                  <label class="form-label text-light">Confirm Password</label>
                  <input type="password" class="form-control" placeholder="Re-enter password" v-model="confirmPassword"
                    required />
                  <p v-if="passwordMatchMessage"
                    :class="isPasswordMatch ? 'password-strength' : 'text-danger password-error'">
                    {{ passwordMatchMessage }}
                  </p>
                </div>
              </div>

              <!--Age-->
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label text-light">Age</label>
                  <input type="number" class="form-control" placeholder="Your age" v-model="age" required />
                </div>

                <!--Gender(select field)-->
                <div class="col-md-6 mb-3">
                  <label class="form-label text-light">Gender</label>
                  <select class="form-select" v-model="gender" required>
                    <option value="" disabled>Select gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>

              <!--Phone-->
              <div class="mb-3">
                <label class="form-label text-light">Phone</label>
                <input type="text" class="form-control" placeholder="Enter phone number" v-model="phone" required />
              </div>

              <!--Address-->
              <div class="mb-4">
                <label class="form-label text-light">Address</label>
                <textarea class="form-control" rows="2" placeholder="Enter your address" v-model="address"
                  required></textarea>
              </div>

              <button type="submit" class="btn btn-createAccount btn-lg w-100">
                Create Account
              </button>

            </form>

            <p v-if="errorMessage" class="text-danger text-center mt-2">
              {{ errorMessage }}
            </p>

            <p class="text-center text-light small mt-4 mb-0">
              Already have an account?
              <RouterLink to="/login" class="text-info">
                Login
              </RouterLink>
            </p>

          </div>
        </div>

      </div>
    </div>

    <Footer />
  </div>
</template>

<script setup>

import { useRouter, RouterLink } from 'vue-router';
import logo from "../../assets/logo.svg";
import Footer from '../../components/Footer.vue';
import { ref, computed } from 'vue';

const router = useRouter();

const username = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const age = ref("");
const gender = ref("");
const phone = ref("");
const address = ref("");
const passwordErrorMessage = ref("");
const passwordStrength = ref("");

const validatePassword = () => {

  passwordErrorMessage.value = "";
  passwordStrength.value = "";

  if (!password.value) return;

  if (password.value.length <= 6) {
    passwordErrorMessage.value = "too short (min 7)"
    return false;
  } else if (password.value.length > 6 && password.value.length <= 20) {
    passwordStrength.value = "Good password";
    return true;
  } else {
    passwordErrorMessage.value = "password too long";
    return false;
  }

};

const passwordMatchMessage = computed(() => {
  if (!confirmPassword.value) return "";

  return password.value === confirmPassword.value
    ? "Passwords match ✅"
    : "Passwords do not match ❌";
});

const isPasswordMatch = computed(() => {
  return (
    password.value === confirmPassword.value &&
    confirmPassword.value !== ""
  );
});


const errorMessage = ref("");

const handleSignUp = async () => {
  errorMessage.value = "";

  try{
    const response = await fetch("http://localhost:5000/api/patient/register", {
      method: "POST",
      headers: {
        "Content-Type" : "application/json",
      },
      body: JSON.stringify({
        username: username.value,
        email: email.value,
        password: password.value,
        age: age.value,
        gender: gender.value,
        phone: phone.value,
        address: address.value,
      }),
    });

    const data = await response.json();

    if (!response.ok){
      errorMessage.value = data.message;
      return;
    }

    router.push("/login");

  } catch (error) {
    errorMessage.value = "Sign up error";
  }
}

</script>



<style scoped>
.login-wrapper {
  background: #27296d;
}

.login-card {
  background: #5e63b6;
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2.2rem;
}

.login-logo {
  width: 42px;
  height: 42px;
}

.form-control,
.form-select {
  border-radius: 10px;
  border: none;
}

.form-control:focus,
.form-select:focus {
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.35);
}

textarea {
  resize: none;
}

.btn-createAccount {
  background-color: #f57018;
  color: white;
  border-radius: 12px;
  padding: 0.7rem;
  font-weight: 600;
}

.btn-createAccount:hover {
  background-color: #d34006;
}

.password-strength {
  font-size: 12px;
  color: rgb(207, 245, 118);
  margin-bottom: -15px;
}

.password-error {
  font-size: 12px;
  margin-bottom: -15px;
}

@media (max-width: 640px) {
  .password-strength {
    margin-bottom: -10px;
  }

  .password-error {
    margin-bottom: -10px;
  }
}
</style>
