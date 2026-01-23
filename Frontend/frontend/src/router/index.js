import { createRouter, createWebHistory } from "vue-router";
import MainLayout from "../views/home/MainLayout.vue";
import Login from "../views/auth/LoginUser.vue";
import HomePage from "../views/home/HomePage.vue";
import CreateAccount from "../views/auth/CreateAccount.vue";
import AdminDashboard from "../views/dashboard/AdminDashboard.vue";
import PatientDashboard from "../views/dashboard/PatientDashboard.vue";
import DoctorAvailability from "../views/dashboard/DoctorAvailability.vue";
import DoctorAppointments from "../views/dashboard/DoctorAppointments.vue";
import ViewProfile from "../views/profile/ViewProfile.vue";
import AdminLayout from "../views/dashboard/AdminLayout.vue";
import AddDoctor from "../forms/AddDoctor.vue";
import DoctorList from "../views/dashboard/DoctorList.vue";
import PatientList from "../views/dashboard/PatientList.vue";
import DepartmentManagement from "../views/dashboard/DepartmentManagement.vue";
import BlockedDoctors from "../views/dashboard/BlockedDoctors.vue";
import BlockedPatients from "../views/dashboard/BlockedPatients.vue";
import AdminAppointments from "../views/dashboard/AdminAppointments.vue";
import DoctorLayout from "../views/dashboard/DoctorLayout.vue";
import DoctorDashboard from "../views/dashboard/DoctorDashboard.vue";

const routes = [
  //Homepage
  {
    path: "/",
    component: MainLayout,
    children: [
      {
        path: "",
        component: HomePage,
      },
    ],
  },
  //Login
  {
    path: "/login",
    component: Login,
  },
  //signup
  {
    path: "/signup",
    component: CreateAccount,
  },
  //Profile
  {
    path: "/profile",
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: "",
        component: ViewProfile,
      },
    ],
  },

  //==================================================
  //Dashboards
  //==================================================

  //Admin dashboard
  {
    path: "/admin",
    component: MainLayout,
    meta: { role: "admin" },
    children: [
      {
        path: "",
        component: AdminLayout,
        children: [
          {
            path: "",
            redirect: "/admin/dashboard",
          },
          {
            path: "dashboard",
            component: AdminDashboard,
          },
          {
            path: "add-doctor",
            component: AddDoctor,
          },
          {
            path: "doctor-list",
            component: DoctorList,
          },
          {
            path: "patient-list",
            component: PatientList,
          },
          {
            path: "departments",
            component: DepartmentManagement,
          },
          {
            path: "appointments",
            component: AdminAppointments,
          },
          {
            path: "blocked-doctors",
            component: BlockedDoctors,
          },
          {
            path: "blocked-patients",
            component: BlockedPatients,
          }
        ],
      },
    ],
  },

  //Patient dashboard
  {
    path: "/patient",
    component: MainLayout,
    meta: { role: "patient" },
    children: [
      {
        path: "",
        redirect: "/patient/dashboard",
      },
      {
        path: "dashboard",
        component: PatientDashboard,
      },
    ],
  },

  //Doctor dashboard
  {
    path: "/doctor",
    component: MainLayout,
    meta: { role: "doctor" },
    children: [
      {
        path: "",
        component: DoctorLayout,
        children: [
          {
            path: "",
            redirect: "/doctor/dashboard",
          },
          {
            path: "dashboard",
            component: DoctorDashboard,
          },
          {
            path: "appointments",
            component: DoctorAppointments,
          },
          {
            path: "availability",
            component: DoctorAvailability,
          },
          {
            path: "manage-availability",
            component: DoctorAvailability,
          },
        ],
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Import auth utility for session management
import auth from "../utils/auth";

// Router guard for authentication and role-based access
router.beforeEach((to, from, next) => {
  const token = auth.getToken();
  const userRole = auth.getRole();
  const user = auth.getUser();

  // Block access if user is inactive (blocked)
  if (user && user.active === false) {
    // If trying to access anything except login, force logout and show message
    if (to.path !== '/login') {
      auth.clearAll();
      alert('Account is blocked. Contact admin.');
      next('/login');
      return;
    }
  }

  // Check if route requires authentication
  if (to.meta.requiresAuth) {
    if (!token) {
      next('/login');
      return;
    }
  }

  // Check role-based access
  if (to.meta.role) {
    if (!token) {
      next('/login');
      return;
    }
    if (userRole !== to.meta.role) {
      if (userRole === 'admin') next('/admin/dashboard');
      else if (userRole === 'patient') next('/patient/dashboard');
      else if (userRole === 'doctor') next('/doctor/dashboard');
      else next('/');
      return;
    }
  }
  next();
});

export default router;
