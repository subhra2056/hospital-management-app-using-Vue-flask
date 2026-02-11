
<template>
  <div class="login-wrapper">
    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-100">

        <div class="col-12 col-sm-10 col-md-8 col-lg-5">
          <div class="login-card shadow">

            <div class="text-center mb-4">
              <div class="d-flex justify-content-center align-items-center gap-2">
                <img :src="logo" alt="Healthease Logo" class="login-logo" />
                <h3 class="fw-bold text-white mb-0">Medi<span style="color: #5DD3B6;">core</span> Login</h3>
              </div>
            </div>

            <form @submit.prevent="handleLogin">

              <div class="mb-3">
                <label class="form-label text-light">Email</label>
                <input
                  type="email"
                  class="form-control"
                  placeholder="Enter your email"
                  v-model="email"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label text-light">Password</label>
                <input
                  type="password"
                  class="form-control"
                  placeholder="Enter password"
                  v-model="password"
                  required
                />
              </div>

              <button type="submit" class="btn btn-login w-100 mt-3">
                Login
              </button>

            </form>

            <p v-if="errorMessage" class="text-danger text-center mt-2">
              {{ errorMessage }}
            </p>

            <p class="text-center text-light small mt-4 mb-0">
              Don’t have an account?
              <RouterLink to="/signup" class="text-info">
                Register
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

import { ref } from "vue";
import { useRouter, RouterLink } from "vue-router";
import logo from "../../assets/logo.svg";
import Footer from "../../components/Footer.vue";
import auth from "../../utils/auth";

const router = useRouter();

const email = ref("");
const password = ref("");
const errorMessage = ref("");

const handleLogin = async () => {
  errorMessage.value = "";

  try {
    const response = await fetch("http://localhost:5000/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email.value,
        password: password.value,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      // If blocked, show specific message
      if (data.blocked) {
        errorMessage.value = data.message || "Account is blocked. Contact admin.";
      } else {
        errorMessage.value = data.message || "Login failed";
      }
      return;
    }

    // Check if user is inactive (should not happen, but double check)
    if (data.user_details && data.user_details.active === false) {
      errorMessage.value = "Account is blocked. Contact admin.";
      return;
    }

    auth.saveLoginData(data.access_token, data.user_details, data.user_details.role);

    const role = data.user_details.role;
    if (role === "admin") {
      router.push("/admin");
    } else if (role === "patient") {
      router.push("/patient");
    } else if (role === "doctor") {
      router.push("/doctor");
    } else {
      errorMessage.value = "Login error";
    }
  } catch (error) {
    errorMessage.value = "Login error";
  }
};

</script>




<style scoped>

.login-wrapper {
  background: #27296d;
}


.login-card {
  background: #5e63b6;
  backdrop-filter: blur(12px);
  border-radius: 16px;
  padding: 2.5rem;
}


.login-logo {
  width: 40px;
}


.form-control {
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 10px;
  padding: 0.75rem;
}

.form-control:focus {
  box-shadow: 0 0 0 0.15rem rgba(50, 130, 184, 0.5);
}


.btn-login {
  background-color: #f57018;
  color: white;
  border-radius: 12px;
  padding: 0.7rem;
  font-weight: 600;
}

.btn-login:hover {
  background-color: #d34006;
}


@media (max-width: 576px) {
  .login-card {
    padding: 2rem 1.5rem;
  }
}

.warning-text{
  font-size: 12px;
  margin-top: -10px;
}

.password-strength{
  font-size: 12px;
  margin-top: -10px;
  color: rgb(188, 243, 104);
}

</style>

