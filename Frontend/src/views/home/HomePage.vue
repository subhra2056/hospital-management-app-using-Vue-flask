<script setup>
import { RouterLink } from "vue-router";
import { ref, onMounted } from "vue";

const stats = ref({
  total_patients: 0,
  total_doctors: 0,
  total_appointments: 0
});

const fetchStats = async () => {
  try {
    const response = await fetch("http://localhost:5000/api/home/stats");
    if (response.ok) {
      const data = await response.json();
      stats.value = data;
    }
  } catch (error) {
    console.error("Error fetching stats:", error);
  }
};

onMounted(() => {
  fetchStats();
});
</script>

<template>
  <div class="homepage">
    <section class="hero-section">
      <div class="hero-background">
        <div class="gradient-overlay"></div>
        <div class="pattern-overlay"></div>
      </div>
      <div class="container hero-content">
        <div class="hero-text">
          <div class="badge-wrapper">
            <span class="hero-badge">
              <svg class="badge-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              Trusted Healthcare Solution
            </span>
          </div>
          <h1 class="hero-title">
            Welcome to <span class="title-accent">Medicore</span>
          </h1>
          <p class="hero-description">
            A modern hospital management system designed for efficiency, care, and simplicity. 
            Streamline your healthcare operations with cutting-edge technology.
          </p>
          <div class="hero-actions">
            <RouterLink to="/login" class="btn-primary">
              <span>Get Started</span>
              <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
              </svg>
            </RouterLink>
            <RouterLink to="/signup" class="btn-secondary">
              <span>Create Account</span>
            </RouterLink>
          </div>
          <div class="hero-stats">
            <div class="stat-item">
              <div class="stat-number">{{ stats.total_patients }}+</div>
              <div class="stat-label">Active Users</div>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <div class="stat-number">{{ stats.total_doctors }}+</div>
              <div class="stat-label">Doctors</div>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <div class="stat-number">24/7</div>
              <div class="stat-label">Support</div>
            </div>
          </div>
        </div>
        <div class="hero-visual">
          <div class="floating-card card-1">
            <div class="card-icon">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
            </div>
            <div class="card-content">
              <div class="card-title">Patients</div>
              <div class="card-value">{{ stats.total_patients }}</div>
            </div>
          </div>
          <div class="floating-card card-2">
            <div class="card-icon">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="card-content">
              <div class="card-title">Doctors</div>
              <div class="card-value">{{ stats.total_doctors }}</div>
            </div>
          </div>
          <div class="floating-card card-3">
            <div class="card-icon">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
            </div>
            <div class="card-content">
              <div class="card-title">Appointments</div>
              <div class="card-value">{{ stats.total_appointments }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="features-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Why Choose Medicore?</h2>
          <p class="section-subtitle">Everything you need to manage your healthcare facility efficiently</p>
        </div>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <svg class="feature-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
            </div>
            <h3 class="feature-title">Patient Management</h3>
            <p class="feature-description">
              Securely store patient records, appointment history, diagnoses, and treatments all in one centralized system.
            </p>
          </div>

          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <svg class="feature-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
            </div>
            <h3 class="feature-title">Smart Appointments</h3>
            <p class="feature-description">
              Schedule and manage appointments with doctors efficiently and accurately with real-time availability tracking.
            </p>
          </div>

          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <svg class="feature-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
            </div>
            <h3 class="feature-title">Hospital Operations</h3>
            <p class="feature-description">
              Streamline departments, staff coordination, and reporting in one unified platform.
            </p>
          </div>
        </div>
      </div>
    </section>

    <section class="trust-section">
      <div class="container">
        <div class="trust-content">
          <h3 class="trust-title">Built for Modern Healthcare</h3>
          <div class="trust-badges">
            <div class="trust-badge">
              <svg class="trust-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
              </svg>
              <span>Secure</span>
            </div>
            <div class="trust-badge">
              <svg class="trust-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
              </svg>
              <span>Reliable</span>
            </div>
            <div class="trust-badge">
              <svg class="trust-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
              <span>Scalable</span>
            </div>
            <div class="trust-badge">
              <svg class="trust-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <span>Easy to Use</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.homepage {
  overflow-x: hidden;
}

.hero-section {
  position: relative;
  min-height: 90vh;
  display: flex;
  align-items: center;
  padding: 4rem 0;
  overflow: hidden;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #5e63b6 0%, #4a50a0 50%, #27296d 100%);
  z-index: 0;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 50%, rgba(93, 211, 182, 0.15) 0%, transparent 50%),
              radial-gradient(circle at 80% 80%, rgba(167, 147, 235, 0.15) 0%, transparent 50%);
}

.pattern-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 1px 1px, rgba(255, 255, 255, 0.1) 1px, transparent 0);
  background-size: 40px 40px;
  opacity: 0.3;
}

.hero-content {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.hero-text {
  color: white;
}

.badge-wrapper {
  margin-bottom: 1.5rem;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
  animation: fadeInUp 0.6s ease;
}

.badge-icon {
  width: 16px;
  height: 16px;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  animation: fadeInUp 0.8s ease;
}

.title-accent {
  color: #5DD3B6;
  position: relative;
}

.title-accent::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #5DD3B6, transparent);
  border-radius: 2px;
}

.hero-description {
  font-size: 1.125rem;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 2.5rem;
  max-width: 540px;
  animation: fadeInUp 1s ease;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 3rem;
  animation: fadeInUp 1.2s ease;
}

.btn-primary,
.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 2rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  text-decoration: none;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: #5DD3B6;
  color: #1e293b;
  box-shadow: 0 4px 15px rgba(93, 211, 182, 0.3);
}

.btn-primary:hover {
  background: #4ab89d;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(93, 211, 182, 0.4);
  color: #1e293b;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
  color: white;
}

.btn-icon {
  width: 18px;
  height: 18px;
}

.hero-stats {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  animation: fadeInUp 1.4s ease;
}

.stat-item {
  text-align: left;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #5DD3B6;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.7);
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
}

.hero-visual {
  position: relative;
  height: 500px;
}

.floating-card {
  position: absolute;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  gap: 1rem;
  animation: float 6s ease-in-out infinite;
}

.card-1 {
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.card-2 {
  top: 50%;
  right: 10%;
  animation-delay: 2s;
}

.card-3 {
  bottom: 10%;
  left: 20%;
  animation-delay: 4s;
}

.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-1 .card-icon {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
}

.card-2 .card-icon {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.card-3 .card-icon {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.card-icon svg {
  width: 24px;
  height: 24px;
}

.card-content {
  flex: 1;
}

.card-title {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.card-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
}

.features-section {
  padding: 6rem 0;
  background: #f8fafc;
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 1rem;
}

.section-subtitle {
  font-size: 1.125rem;
  color: #64748b;
  max-width: 600px;
  margin: 0 auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2.5rem;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 1px solid #e2e8f0;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(94, 99, 182, 0.15);
  border-color: #5e63b6;
}

.feature-icon-wrapper {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: linear-gradient(135deg, #5e63b6, #4a50a0);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.feature-icon {
  width: 32px;
  height: 32px;
  color: white;
}

.feature-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 1rem;
}

.feature-description {
  font-size: 1rem;
  line-height: 1.7;
  color: #64748b;
  margin: 0;
}

.trust-section {
  padding: 4rem 0;
  background: white;
}

.trust-content {
  text-align: center;
}

.trust-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 2.5rem;
}

.trust-badges {
  display: flex;
  justify-content: center;
  gap: 3rem;
  flex-wrap: wrap;
}

.trust-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 1.5rem;
  border-radius: 16px;
  background: #f8fafc;
  transition: all 0.3s ease;
  min-width: 120px;
}

.trust-badge:hover {
  background: #5e63b6;
  color: white;
  transform: translateY(-4px);
}

.trust-badge:hover .trust-icon {
  color: white;
}

.trust-icon {
  width: 32px;
  height: 32px;
  color: #5e63b6;
  transition: color 0.3s ease;
}

.trust-badge span {
  font-weight: 600;
  font-size: 0.9375rem;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

@media (max-width: 968px) {
  .hero-content {
    grid-template-columns: 1fr;
    gap: 3rem;
  }

  .hero-visual {
    height: 300px;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-actions {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
    justify-content: center;
  }

  .hero-stats {
    flex-wrap: wrap;
    justify-content: center;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style> 

