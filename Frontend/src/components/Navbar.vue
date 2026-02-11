

<template>
  <nav class="navbar navbar-expand-lg healthease-navbar">
    <div class="container">
      <a class="navbar-brand d-flex align-items-center gap-2 text-white" href="#">
        <img :src="logo" alt="Healthease Logo" class="brand-logo" />
        <span>Medi<span style="color: #5DD3B6;">core</span></span>
      </a>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarContent"
        aria-controls="navbarContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse justify-content-end" id="navbarContent">
        <div class="d-flex align-items-lg-center gap-3 flex-column flex-lg-row mt-3 mt-lg-0">

          <div class="dropdown">
            <button
              class="btn account-btn dropdown-toggle"
              data-bs-toggle="dropdown"
            >
              Account
            </button>

            <ul class="dropdown-menu dropdown-menu-end">
              <template v-if="isLoggedIn">
                <li>
                  <RouterLink class="dropdown-item" to="/profile" @click="closeDropdown">View Profile</RouterLink>
                </li>
                <li><hr class="dropdown-divider" /></li>
                <li>
                  <RouterLink class="dropdown-item text-danger" to="/" @click="logout">
                    Logout
                  </RouterLink>
                </li>
              </template>

              <template v-else>
                <li>
                  <RouterLink class="dropdown-item" to="/login">Login</RouterLink>
                </li>
                <li>
                  <RouterLink class="dropdown-item" to="/signup">Create Account</RouterLink>
                </li>
              </template>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>


<script>
import logo from "../assets/logo.svg";
import { RouterLink } from "vue-router";
import auth from "../utils/auth";

export default {
  name: "Navbar",
  data() {
    return {
      logo,
      isLoggedIn: false,
    };
  },
  mounted() {
    this.checkLoginStatus();
  },
  watch: {
    '$route'() {
      this.checkLoginStatus();
    }
  },
  methods: {
    checkLoginStatus() {
      this.isLoggedIn = auth.isLoggedIn();
    },
    logout() {
      auth.clearAll();
      this.isLoggedIn = false;
      this.$router.push('/');
    },
    closeDropdown() {
      const dropdown = document.querySelector('.dropdown-menu');
      if (dropdown) {
        const bsDropdown = bootstrap.Dropdown.getInstance(document.querySelector('[data-bs-toggle="dropdown"]'));
        if (bsDropdown) {
          bsDropdown.hide();
        }
      }
    },
  },
};
</script>

<style scoped>
.healthease-navbar {
  background: #27296d;
  padding: 0.6rem 0;
}

.nav-link::after {
  content: "";
  position: relative;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 3px;
  background: #fff;
  transition: 0.3s ease;
}

.nav-link:hover::after {
  width: 100%;
}

.search-input {
  width: 260px;
  border-radius: 20px;
  padding: 0.45rem 1rem;
}

.account-btn {
  background: #a393eb;
  border-radius: 20px;
  padding: 0.45rem 1.1rem;
  font-weight: 500;
}

@media (max-width: 991px) {
  .search-input {
    width: 80%;
  }
}

.navbar-brand:hover .brand-logo {
  transform: rotate(-3deg) scale(1.05);
  transition: 0.3s ease;
}

.brand-logo {
  height: 32px;
  width: auto;
  max-height: 32px;
}

.dropdown-menu {
  background-color: #5e63b6;
}

.dropdown-item {
  color: white;
}

.dropdown-item:hover {
  color: black;
}
</style>
