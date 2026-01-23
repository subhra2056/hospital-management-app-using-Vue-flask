<template>
  <div class="patient-dashboard">
    <PatientSidePanel :active="activePanel" @navigate="handlePanelNav" />
    <div class="dashboard-main">
      <!-- Dashboard Overview -->
      <div v-if="activePanel === 'dashboard'" class="dashboard-content">
        <div class="dashboard-header">
          <h2 class="dashboard-title">Welcome Back!</h2>
          <p class="dashboard-subtitle">Manage your appointments and view your health records</p>
        </div>

        <div class="stats-grid">
          <div class="stat-card stat-card-primary">
            <div class="stat-icon-wrapper">
              <svg class="stat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
            </div>
            <div class="stat-content">
              <p class="stat-label">Upcoming</p>
              <h3 class="stat-value">{{ upcomingAppointments.length }}</h3>
              <span class="stat-change positive">Appointments</span>
            </div>
          </div>

          <div class="stat-card stat-card-success">
            <div class="stat-icon-wrapper">
              <svg class="stat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="stat-content">
              <p class="stat-label">Completed</p>
              <h3 class="stat-value">{{ completedAppointments.length }}</h3>
              <span class="stat-change positive">Treatments</span>
            </div>
          </div>

          <div class="stat-card stat-card-warning">
            <div class="stat-icon-wrapper">
              <svg class="stat-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="stat-content">
              <p class="stat-label">Pending</p>
              <h3 class="stat-value">{{ pendingAppointments.length }}</h3>
              <span class="stat-change neutral">Review</span>
            </div>
          </div>
        </div>

        <div class="row g-4 mt-2">
          <div class="col-lg-6">
            <div class="section-card">
              <div class="section-header">
                <h4 class="section-title">
                  <svg class="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  Upcoming Appointments
                </h4>
              </div>
              <div class="section-body">
                <div v-if="loading" class="loading-state">
                  <div class="spinner-border text-primary" role="status"></div>
                </div>
                <div v-else-if="upcomingAppointments.length === 0" class="empty-state">
                  <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  <p class="empty-text">No upcoming appointments</p>
                  <button class="btn-book" @click="activePanel = 'findDoctor'">Book Now</button>
                </div>
                <div v-else class="appointments-list">
                  <div v-for="apt in upcomingAppointments.slice(0, 3)" :key="apt.id" class="appointment-card">
                    <div class="appointment-info">
                      <div class="doctor-avatar">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                        </svg>
                      </div>
                      <div class="appointment-details">
                        <h6 class="doctor-name">Dr. {{ apt.doctor_name }}</h6>
                        <p class="department">{{ apt.doctor_specialization || 'General' }}</p>
                        <div class="datetime">
                          <span class="date">{{ formatDate(apt.appointment_date) }}</span>
                          <span class="time">{{ apt.appointment_time }}</span>
                        </div>
                      </div>
                    </div>
                    <div class="appointment-actions">
                      <span class="status-badge booked">{{ apt.status }}</span>
                      <button class="btn-cancel" @click="cancelAppointment(apt.id)">Cancel</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-lg-6">
            <div class="section-card">
              <div class="section-header">
                <h4 class="section-title">
                  <svg class="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  Recent Treatments
                </h4>
              </div>
              <div class="section-body">
                <div v-if="completedAppointments.length === 0" class="empty-state">
                  <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                  <p class="empty-text">No treatment records yet</p>
                </div>
                <div v-else class="treatments-list">
                  <div v-for="apt in completedAppointments.slice(0, 3)" :key="apt.id" class="treatment-card">
                    <div class="treatment-header">
                      <h6 class="doctor-name">Dr. {{ apt.doctor_name }}</h6>
                      <span class="treatment-date">{{ formatDate(apt.appointment_date) }}</span>
                    </div>
                    <div v-if="apt.treatment" class="treatment-body">
                      <p class="diagnosis"><strong>Diagnosis:</strong> {{ apt.treatment.diagnosis }}</p>
                      <p class="prescription"><strong>Prescription:</strong> {{ apt.treatment.prescription }}</p>
                    </div>
                    <span class="status-badge completed">Completed</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Find Doctor Section -->
      <div v-else-if="activePanel === 'findDoctor'" class="dashboard-content">
        <div class="dashboard-header">
          <h2 class="dashboard-title">Find a Doctor</h2>
          <p class="dashboard-subtitle">Browse doctors by department and book an appointment</p>
        </div>

        <div class="find-doctor-section">
          <!-- Step Indicator -->
          <div class="step-indicator">
            <div :class="['step', { active: true, completed: selectedDepartment }]">
              <div class="step-number">1</div>
              <span class="step-label">Select Department</span>
            </div>
            <div class="step-line" :class="{ active: selectedDepartment }"></div>
            <div :class="['step', { active: selectedDepartment, completed: selectedDoctor }]">
              <div class="step-number">2</div>
              <span class="step-label">Choose Doctor</span>
            </div>
            <div class="step-line" :class="{ active: selectedDoctor }"></div>
            <div :class="['step', { active: selectedDoctor && showSlots }]">
              <div class="step-number">3</div>
              <span class="step-label">Book Slot</span>
            </div>
          </div>

          <!-- Department Selection -->
          <div class="section-card">
            <div class="section-card-header">
              <div class="section-card-icon departments">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                </svg>
              </div>
              <div>
                <h3 class="section-card-title">Select Department</h3>
                <p class="section-card-desc">Choose from our specialized medical departments</p>
              </div>
            </div>
            <div class="department-grid">
              <div 
                v-for="dept in departments" 
                :key="dept.id" 
                :class="['department-card', { active: selectedDepartment === dept.id }]"
                @click="selectDepartment(dept.id)"
              >
                <div class="dept-icon-wrapper">
                  <div class="dept-icon">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                    </svg>
                  </div>
                  <div v-if="selectedDepartment === dept.id" class="check-badge">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path>
                    </svg>
                  </div>
                </div>
                <h5 class="dept-name">{{ dept.name }}</h5>
                <p class="dept-desc">{{ dept.description || 'Expert medical care' }}</p>
                <div class="dept-doctors-count">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                  <span>{{ dept.doctors_registered || 0 }} Doctors</span>
                </div>
              </div>
            </div>
            <div v-if="departments.length === 0" class="empty-departments">
              <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
              <p>No departments available</p>
            </div>
          </div>

          <!-- Doctors List -->
          <div v-if="selectedDepartment" class="section-card doctors-card">
            <div class="section-card-header">
              <div class="section-card-icon doctors">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div>
                <h3 class="section-card-title">Available Doctors</h3>
                <p class="section-card-desc">Select a doctor to view available appointment slots</p>
              </div>
            </div>
            
            <div v-if="filteredDoctors.length === 0" class="empty-doctors">
              <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <p>No doctors available in this department</p>
            </div>
            
            <div v-else class="doctors-grid">
              <div 
                v-for="doc in filteredDoctors" 
                :key="doc.id" 
                :class="['doctor-card', { selected: selectedDoctor && selectedDoctor.id === doc.id }]"
              >
                <div class="doctor-card-top">
                  <div class="doctor-avatar-wrapper">
                    <div class="doctor-avatar-large">
                      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                      </svg>
                    </div>
                    <div class="doctor-status online"></div>
                  </div>
                  <div class="doctor-info">
                    <h5 class="doctor-name">Dr. {{ doc.username }}</h5>
                    <div class="doctor-badge">
                      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
                      </svg>
                      <span>{{ doc.specialization || 'General Physician' }}</span>
                    </div>
                  </div>
                </div>
                <div class="doctor-card-body">
                  <div class="doctor-stats">
                    <div class="stat-item">
                      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      <span>{{ doc.experience_years || 0 }} Years Exp</span>
                    </div>
                    <div class="stat-item">
                      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"></path>
                      </svg>
                      <span>4.8 Rating</span>
                    </div>
                  </div>
                </div>
                <button 
                  class="btn-view-slots" 
                  @click="viewDoctorAvailability(doc)"
                >
                  <span>View Available Slots</span>
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Availability Slots -->
          <div v-if="selectedDoctor && showSlots" class="section-card slots-card">
            <div class="section-card-header">
              <div class="section-card-icon slots">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
              </div>
              <div class="flex-grow-1">
                <h3 class="section-card-title">Book Appointment with Dr. {{ selectedDoctor.username }}</h3>
                <p class="section-card-desc">Select your preferred date and time slot</p>
              </div>
              <button class="btn-close-slots" @click="closeSlots">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            
            <div v-if="loadingSlots" class="loading-state">
              <div class="spinner-border text-primary" role="status"></div>
              <p>Loading available slots...</p>
            </div>
            
            <div v-else-if="availableSlots.length === 0" class="empty-slots">
              <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <p>No available slots at the moment</p>
              <span class="empty-hint">Please check back later or try another doctor</span>
            </div>
            
            <div v-else>
              <div class="slots-grid">
                <div 
                  v-for="slot in availableSlots" 
                  :key="slot.id" 
                  :class="['slot-card', { selected: selectedSlot?.id === slot.id }]"
                  @click="selectedSlot = slot"
                >
                  <div class="slot-check" v-if="selectedSlot?.id === slot.id">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path>
                    </svg>
                  </div>
                  <div class="slot-date-icon">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                  </div>
                  <div class="slot-date">{{ formatDate(slot.date) }}</div>
                  <div class="slot-time">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    {{ slot.start_time }} - {{ slot.end_time }}
                  </div>
                </div>
              </div>
              
              <div class="booking-footer">
                <div v-if="selectedSlot" class="selected-slot-info">
                  <span class="info-label">Selected:</span>
                  <span class="info-value">{{ formatDate(selectedSlot.date) }} at {{ selectedSlot.start_time }}</span>
                </div>
                <button 
                  class="btn-book-appointment"
                  @click="bookAppointment"
                  :disabled="!selectedSlot || bookingInProgress"
                >
                  <span v-if="bookingInProgress" class="spinner-border spinner-border-sm me-2"></span>
                  <svg v-else fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  {{ bookingInProgress ? 'Booking...' : 'Confirm Booking' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- My Appointments Section -->
      <div v-else-if="activePanel === 'appointments'" class="dashboard-content">
        <div class="dashboard-header">
          <h2 class="dashboard-title">My Appointments</h2>
          <p class="dashboard-subtitle">View and manage all your appointments</p>
        </div>

        <div class="appointments-tabs">
          <button 
            :class="['tab-btn', { active: appointmentTab === 'upcoming' }]"
            @click="appointmentTab = 'upcoming'"
          >
            Upcoming ({{ upcomingAppointments.length }})
          </button>
          <button 
            :class="['tab-btn', { active: appointmentTab === 'pending' }]"
            @click="appointmentTab = 'pending'"
          >
            Pending ({{ pendingAppointments.length }})
          </button>
          <button 
            :class="['tab-btn', { active: appointmentTab === 'all' }]"
            @click="appointmentTab = 'all'"
          >
            All ({{ appointments.length }})
          </button>
        </div>

        <div class="appointments-container">
          <div v-if="loading" class="loading-state">
            <div class="spinner-border text-primary" role="status"></div>
          </div>
          <div v-else-if="displayedAppointments.length === 0" class="empty-state">
            <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
            <p class="empty-text">No appointments found</p>
          </div>
          <div v-else class="appointments-table-wrapper">
            <table class="appointments-table">
              <thead>
                <tr>
                  <th>Doctor</th>
                  <th>Department</th>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="apt in displayedAppointments" :key="apt.id">
                  <td>
                    <div class="table-doctor">
                      <strong>Dr. {{ apt.doctor_name }}</strong>
                    </div>
                  </td>
                  <td>{{ apt.doctor_specialization || 'General' }}</td>
                  <td>{{ formatDate(apt.appointment_date) }}</td>
                  <td>{{ apt.appointment_time }}</td>
                  <td>
                    <span class="status-badge-small" :class="getStatusClass(apt.status)">
                      {{ apt.status }}
                    </span>
                  </td>
                  <td>
                    <button 
                      v-if="apt.status === 'BOOKED'"
                      class="btn-action cancel"
                      @click="cancelAppointment(apt.id)"
                    >
                      Cancel
                    </button>
                    <button 
                      v-if="apt.treatment"
                      class="btn-action view"
                      @click="viewTreatmentDetails(apt)"
                    >
                      View Treatment
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Treatment History Section -->
      <div v-else-if="activePanel === 'completed'" class="dashboard-content">
        <div class="dashboard-header">
          <h2 class="dashboard-title">Treatment History</h2>
          <p class="dashboard-subtitle">View all your completed treatments and diagnoses</p>
        </div>

        <div class="treatments-container">
          <div v-if="loading" class="loading-state">
            <div class="spinner-border text-primary" role="status"></div>
          </div>
          <div v-else-if="completedAppointments.length === 0" class="empty-state">
            <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            <p class="empty-text">No treatment history available</p>
          </div>
          <div v-else class="treatment-history-list">
            <div v-for="apt in completedAppointments" :key="apt.id" class="treatment-history-card">
              <div class="treatment-history-header">
                <div class="doctor-info">
                  <div class="doctor-avatar-small">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                    </svg>
                  </div>
                  <div>
                    <h5 class="doctor-name">Dr. {{ apt.doctor_name }}</h5>
                    <p class="department">{{ apt.doctor_specialization || 'General' }}</p>
                  </div>
                </div>
                <div class="visit-date">
                  <span class="date-label">Visit Date</span>
                  <span class="date-value">{{ formatDate(apt.appointment_date) }}</span>
                </div>
              </div>
              <div v-if="apt.treatment" class="treatment-history-body">
                <div class="treatment-detail">
                  <h6 class="detail-label">Diagnosis</h6>
                  <p class="detail-value">{{ apt.treatment.diagnosis }}</p>
                </div>
                <div class="treatment-detail">
                  <h6 class="detail-label">Prescription</h6>
                  <p class="detail-value">{{ apt.treatment.prescription }}</p>
                </div>
                <div v-if="apt.treatment.notes" class="treatment-detail">
                  <h6 class="detail-label">Doctor's Notes</h6>
                  <p class="detail-value">{{ apt.treatment.notes }}</p>
                </div>
              </div>
              <div class="treatment-history-footer">
                <span class="status-badge completed">Completed</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Export Records Section -->
      <div v-else-if="activePanel === 'export'" class="dashboard-content">
        <div class="dashboard-header">
          <h2 class="dashboard-title">Export Records</h2>
          <p class="dashboard-subtitle">Download your complete medical history</p>
        </div>

        <div class="export-section">
          <div class="export-card">
            <div class="export-icon">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <h4 class="export-title">Export Treatment History</h4>
            <p class="export-desc">Download your complete treatment history as a CSV file. This includes all diagnoses, prescriptions, and doctor notes.</p>
            <button class="btn-export" @click="exportTreatments" :disabled="exporting">
              <span v-if="exporting" class="spinner-border spinner-border-sm me-2"></span>
              {{ exporting ? 'Exporting...' : 'Export to CSV' }}
            </button>
            <div v-if="exportMessage" class="export-message" :class="{ success: exportMessage.includes('success') || exportMessage.includes('started') }">
              {{ exportMessage }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Treatment Details Modal -->
    <div v-if="showTreatmentModal" class="modal-overlay" @click.self="showTreatmentModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h4>Treatment Details</h4>
          <button class="modal-close" @click="showTreatmentModal = false">×</button>
        </div>
        <div v-if="selectedTreatment" class="modal-body">
          <div class="modal-field">
            <label>Doctor</label>
            <p>Dr. {{ selectedTreatment.doctor_name }}</p>
          </div>
          <div class="modal-field">
            <label>Date</label>
            <p>{{ formatDate(selectedTreatment.appointment_date) }}</p>
          </div>
          <div class="modal-field">
            <label>Diagnosis</label>
            <p>{{ selectedTreatment.treatment?.diagnosis || 'N/A' }}</p>
          </div>
          <div class="modal-field">
            <label>Prescription</label>
            <p>{{ selectedTreatment.treatment?.prescription || 'N/A' }}</p>
          </div>
          <div v-if="selectedTreatment.treatment?.notes" class="modal-field">
            <label>Notes</label>
            <p>{{ selectedTreatment.treatment.notes }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import PatientSidePanel from "../../components/PatientSidePanel.vue";
import auth from "../../utils/auth";

const router = useRouter();
const loading = ref(false);
const appointments = ref([]);
const exporting = ref(false);
const exportMessage = ref("");
const activePanel = ref("dashboard");
const appointmentTab = ref("upcoming");

// Find doctor state
const departments = ref([]);
const filteredDoctors = ref([]);
const availableSlots = ref([]);
const selectedDepartment = ref(null);
const selectedDoctor = ref(null);
const selectedSlot = ref(null);
const showSlots = ref(false);
const loadingSlots = ref(false);
const bookingInProgress = ref(false);

// Treatment modal
const showTreatmentModal = ref(false);
const selectedTreatment = ref(null);

const getToken = () => auth.getToken();

const upcomingAppointments = computed(() => {
  const today = new Date().toISOString().split('T')[0];
  return appointments.value.filter(apt => 
    apt.appointment_date >= today && apt.status === "BOOKED"
  );
});

const completedAppointments = computed(() => {
  return appointments.value.filter(apt => apt.status === "COMPLETED");
});

const pendingAppointments = computed(() => {
  return appointments.value.filter(apt => apt.status === "PENDING");
});

const displayedAppointments = computed(() => {
  if (appointmentTab.value === 'upcoming') return upcomingAppointments.value;
  if (appointmentTab.value === 'pending') return pendingAppointments.value;
  return appointments.value;
});

const handlePanelNav = (panel) => {
  if (panel === 'profile') {
    router.push('/profile');
    return;
  }
  activePanel.value = panel;
  if (panel === 'findDoctor') {
    fetchDepartments();
  }
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
};

const getStatusClass = (status) => {
  const classes = {
    'BOOKED': 'booked',
    'COMPLETED': 'completed',
    'CANCELLED': 'cancelled',
    'PENDING': 'pending'
  };
  return classes[status] || 'pending';
};

// Fetch departments
const fetchDepartments = async () => {
  try {
    const response = await fetch("http://localhost:5000/api/departments", {
      headers: { Authorization: `Bearer ${getToken()}` }
    });
    const data = await response.json();
    departments.value = data.departments || [];
  } catch (error) {
    console.error("Error fetching departments:", error);
    departments.value = [];
  }
};

// Select department and fetch doctors
const selectDepartment = async (deptId) => {
  selectedDepartment.value = deptId;
  selectedDoctor.value = null;
  showSlots.value = false;
  selectedSlot.value = null;
  
  try {
    const response = await fetch(`http://localhost:5000/api/search/doctors?department_id=${deptId}`, {
      headers: { Authorization: `Bearer ${getToken()}` }
    });
    const data = await response.json();
    filteredDoctors.value = (data.doctors || []).filter(doc => doc.department_id === deptId);
  } catch (error) {
    console.error("Error fetching doctors:", error);
    filteredDoctors.value = [];
  }
};

// View doctor availability
const viewDoctorAvailability = async (doctor) => {
  selectedDoctor.value = doctor;
  showSlots.value = true;
  loadingSlots.value = true;
  selectedSlot.value = null;
  
  try {
    const response = await fetch(`http://localhost:5000/api/doctor/availability/${doctor.id}`, {
      headers: { Authorization: `Bearer ${getToken()}` }
    });
    const data = await response.json();
    availableSlots.value = data.availabilities || [];
  } catch (error) {
    console.error("Error fetching slots:", error);
    availableSlots.value = [];
  } finally {
    loadingSlots.value = false;
  }
};

const closeSlots = () => {
  showSlots.value = false;
  selectedDoctor.value = null;
  selectedSlot.value = null;
};

// Book appointment
const bookAppointment = async () => {
  if (!selectedSlot.value) return;
  
  bookingInProgress.value = true;
  try {
    // Format time to HH:MM format (remove seconds if present)
    const startTime = selectedSlot.value.start_time.substring(0, 5);
    
    const response = await fetch("http://localhost:5000/api/patient/appointments/book", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getToken()}`
      },
      body: JSON.stringify({ 
        doctor_id: selectedDoctor.value.id,
        appointment_date: selectedSlot.value.date,
        appointment_time: startTime
      })
    });
    
    const data = await response.json();
    if (response.ok) {
      alert("Appointment booked successfully!");
      closeSlots();
      selectedDepartment.value = null;
      filteredDoctors.value = [];
      loadAppointments();
      activePanel.value = 'appointments';
    } else {
      alert(data.message || "Failed to book appointment");
    }
  } catch (error) {
    console.error("Error booking appointment:", error);
    alert("Error booking appointment");
  } finally {
    bookingInProgress.value = false;
  }
};

// Cancel appointment
const cancelAppointment = async (appointmentId) => {
  if (!confirm("Are you sure you want to cancel this appointment?")) return;
  
  try {
    const response = await fetch(`http://localhost:5000/api/appointments/${appointmentId}/cancel`, {
      method: "POST",
      headers: { Authorization: `Bearer ${getToken()}` }
    });
    
    if (response.ok) {
      alert("Appointment cancelled successfully");
      loadAppointments();
    } else {
      alert("Failed to cancel appointment");
    }
  } catch (error) {
    console.error("Error cancelling appointment:", error);
    alert("Error cancelling appointment");
  }
};

// Load appointments
const loadAppointments = async () => {
  loading.value = true;
  try {
    const response = await fetch("http://localhost:5000/api/patient/appointments", {
      headers: { Authorization: `Bearer ${getToken()}` }
    });
    const data = await response.json();
    appointments.value = data.appointments || [];
  } catch (error) {
    console.error("Error loading appointments:", error);
    appointments.value = [];
  } finally {
    loading.value = false;
  }
};

// View treatment details
const viewTreatmentDetails = (apt) => {
  selectedTreatment.value = apt;
  showTreatmentModal.value = true;
};

// Export treatments
const exportTreatments = async () => {
  exporting.value = true;
  exportMessage.value = "";
  
  try {
    const response = await fetch("http://localhost:5000/api/patient/export-treatments", {
      method: "POST",
      headers: { Authorization: `Bearer ${getToken()}` }
    });
    const data = await response.json();
    
    if (response.ok) {
      exportMessage.value = "Export started successfully! You will receive an email shortly.";
    } else {
      exportMessage.value = data.message || "Export failed";
    }
  } catch (error) {
    console.error("Error exporting:", error);
    exportMessage.value = "Error starting export";
  } finally {
    exporting.value = false;
  }
};

onMounted(() => {
  loadAppointments();
  fetchDepartments();
});
</script>

<style scoped>
.patient-dashboard {
  display: flex;
  min-height: 100vh;
  background: #f8fafc;
}

.dashboard-main {
  flex: 1;
  overflow-x: hidden;
}

.dashboard-content {
  padding: 2rem;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.dashboard-subtitle {
  color: #64748b;
  font-size: 1rem;
  margin: 0;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.stat-card-primary { border-left: 4px solid #3b82f6; }
.stat-card-success { border-left: 4px solid #10b981; }
.stat-card-warning { border-left: 4px solid #f59e0b; }

.stat-card-primary .stat-icon-wrapper { background: linear-gradient(135deg, #3b82f6, #2563eb); }
.stat-card-success .stat-icon-wrapper { background: linear-gradient(135deg, #10b981, #059669); }
.stat-card-warning .stat-icon-wrapper { background: linear-gradient(135deg, #f59e0b, #d97706); }

.stat-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-icon {
  width: 24px;
  height: 24px;
}

.stat-label {
  font-size: 0.75rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
  margin: 0;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0.25rem 0;
}

.stat-change {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
}

.stat-change.positive { background: #d1fae5; color: #065f46; }
.stat-change.neutral { background: #fef3c7; color: #92400e; }

/* Section Cards */
.section-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.section-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-icon {
  width: 20px;
  height: 20px;
  color: #10b981;
}

.section-body {
  padding: 1.5rem;
}

/* Empty & Loading States */
.empty-state, .loading-state {
  text-align: center;
  padding: 2rem;
}

.empty-icon {
  width: 48px;
  height: 48px;
  color: #cbd5e1;
  margin-bottom: 1rem;
}

.empty-text {
  color: #64748b;
  margin: 0 0 1rem 0;
}

.btn-book {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-book:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

/* Appointment Cards */
.appointments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.appointment-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.appointment-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.doctor-avatar {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #10b981, #059669);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.doctor-avatar svg {
  width: 24px;
  height: 24px;
}

.doctor-name {
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
}

.department {
  color: #64748b;
  font-size: 0.875rem;
  margin: 0;
}

.datetime {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.date, .time {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  background: #e2e8f0;
  border-radius: 4px;
  color: #475569;
}

.appointment-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.status-badge {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.375rem 0.75rem;
  border-radius: 20px;
}

.status-badge.booked { background: #fef3c7; color: #92400e; }
.status-badge.completed { background: #d1fae5; color: #065f46; }
.status-badge.cancelled { background: #fee2e2; color: #991b1b; }
.status-badge.pending { background: #e0e7ff; color: #3730a3; }

.btn-cancel {
  background: transparent;
  border: 1px solid #ef4444;
  color: #ef4444;
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: #ef4444;
  color: white;
}

/* Find Doctor Section */
.find-doctor-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Step Indicator */
.step-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  padding: 1.5rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  opacity: 0.5;
  transition: all 0.3s ease;
}

.step.active {
  opacity: 1;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #64748b;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background: linear-gradient(135deg, #5e63b6, #4a50a0);
  color: white;
}

.step.completed .step-number {
  background: linear-gradient(135deg, #10b981, #059669);
}

.step-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #64748b;
  white-space: nowrap;
}

.step.active .step-label {
  color: #1e293b;
}

.step-line {
  width: 80px;
  height: 3px;
  background: #e2e8f0;
  margin: 0 1rem;
  margin-bottom: 1.5rem;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.step-line.active {
  background: linear-gradient(90deg, #10b981, #059669);
}

/* Section Cards */
.section-card {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.section-card-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f1f5f9;
}

.section-card-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.section-card-icon.departments {
  background: linear-gradient(135deg, #5e63b6, #4a50a0);
  color: white;
}

.section-card-icon.doctors {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
}

.section-card-icon.slots {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.section-card-icon svg {
  width: 24px;
  height: 24px;
}

.section-card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
}

.section-card-desc {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
}

/* Department Grid */
.department-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}

.department-card {
  background: #f8fafc;
  border: 2px solid transparent;
  border-radius: 16px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  position: relative;
}

.department-card:hover {
  background: white;
  border-color: #5e63b6;
  transform: translateY(-4px);
  box-shadow: 0 10px 30px rgba(94, 99, 182, 0.15);
}

.department-card.active {
  background: linear-gradient(135deg, rgba(94, 99, 182, 0.1), rgba(74, 80, 160, 0.05));
  border-color: #5e63b6;
}

.dept-icon-wrapper {
  position: relative;
  display: inline-block;
  margin-bottom: 1rem;
}

.dept-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: linear-gradient(135deg, #5e63b6, #4a50a0);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: all 0.3s ease;
}

.department-card:hover .dept-icon {
  transform: scale(1.1);
}

.dept-icon svg {
  width: 32px;
  height: 32px;
}

.check-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 24px;
  height: 24px;
  background: #10b981;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  border: 2px solid white;
}

.check-badge svg {
  width: 14px;
  height: 14px;
}

.dept-name {
  font-weight: 700;
  font-size: 1rem;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.dept-desc {
  font-size: 0.8rem;
  color: #64748b;
  margin: 0 0 1rem 0;
  min-height: 2.4em;
}

.dept-doctors-count {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: #5e63b6;
  font-weight: 600;
}

.dept-doctors-count svg {
  width: 16px;
  height: 16px;
}

.empty-departments, .empty-doctors, .empty-slots {
  text-align: center;
  padding: 3rem 2rem;
  color: #64748b;
}

.empty-departments .empty-icon,
.empty-doctors .empty-icon,
.empty-slots .empty-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-hint {
  display: block;
  font-size: 0.8rem;
  color: #94a3b8;
  margin-top: 0.5rem;
}

/* Doctors Grid */
.doctors-card {
  border-left: 4px solid #3b82f6;
}

.doctors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.doctor-card {
  background: #f8fafc;
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.doctor-card:hover {
  background: white;
  border-color: #3b82f6;
  box-shadow: 0 10px 30px rgba(59, 130, 246, 0.1);
}

.doctor-card.selected {
  background: white;
  border-color: #10b981;
  box-shadow: 0 10px 30px rgba(16, 185, 129, 0.15);
}

.doctor-card-top {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.doctor-avatar-wrapper {
  position: relative;
  flex-shrink: 0;
}

.doctor-avatar-large {
  width: 70px;
  height: 70px;
  border-radius: 16px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.doctor-avatar-large svg {
  width: 36px;
  height: 36px;
}

.doctor-status {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 3px solid #f8fafc;
}

.doctor-status.online {
  background: #10b981;
}

.doctor-info {
  flex: 1;
  min-width: 0;
}

.doctor-info .doctor-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.doctor-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.05));
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  color: #059669;
  font-weight: 600;
}

.doctor-badge svg {
  width: 14px;
  height: 14px;
}

.doctor-card-body {
  padding: 1rem 0;
  border-top: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 1rem;
}

.doctor-stats {
  display: flex;
  gap: 1.5rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #64748b;
}

.stat-item svg {
  width: 16px;
  height: 16px;
  color: #5e63b6;
}

.btn-view-slots {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1.25rem;
  background: linear-gradient(135deg, #5e63b6, #4a50a0);
  border: none;
  border-radius: 12px;
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-view-slots:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(94, 99, 182, 0.35);
}

.btn-view-slots svg {
  width: 18px;
  height: 18px;
  transition: transform 0.2s ease;
}

.btn-view-slots:hover svg {
  transform: translateX(4px);
}

/* Slots Card */
.slots-card {
  border-left: 4px solid #10b981;
}

.btn-close-slots {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  border: none;
  border-radius: 10px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.btn-close-slots:hover {
  background: #fee2e2;
  color: #ef4444;
}

.btn-close-slots svg {
  width: 18px;
  height: 18px;
}

.loading-state {
  text-align: center;
  padding: 3rem;
}

.loading-state p {
  color: #64748b;
  margin-top: 1rem;
}

.slots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.slot-card {
  position: relative;
  padding: 1.25rem;
  background: #f8fafc;
  border: 2px solid transparent;
  border-radius: 14px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.slot-card:hover {
  border-color: #10b981;
  background: white;
  transform: translateY(-2px);
}

.slot-card.selected {
  border-color: #10b981;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.05));
}

.slot-check {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 22px;
  height: 22px;
  background: #10b981;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.slot-check svg {
  width: 12px;
  height: 12px;
}

.slot-date-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.75rem;
}

.slot-date-icon svg {
  width: 28px;
  height: 28px;
  color: #5e63b6;
}

.slot-date {
  font-weight: 700;
  font-size: 0.95rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.slot-time {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  font-size: 0.85rem;
  color: #10b981;
  font-weight: 600;
}

.slot-time svg {
  width: 14px;
  height: 14px;
}

.booking-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.selected-slot-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: #f0fdf4;
  border-radius: 10px;
}

.info-label {
  font-size: 0.85rem;
  color: #64748b;
}

.info-value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #059669;
}

.btn-book-appointment {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #10b981, #059669);
  border: none;
  border-radius: 12px;
  color: white;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-left: auto;
}

.btn-book-appointment:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.35);
}

.btn-book-appointment:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-book-appointment svg {
  width: 20px;
  height: 20px;
}

@media (max-width: 768px) {
  .step-indicator {
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  .step-line {
    display: none;
  }
  
  .department-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  }
  
  .doctors-grid {
    grid-template-columns: 1fr;
  }
  
  .booking-footer {
    flex-direction: column;
  }
  
  .btn-book-appointment {
    width: 100%;
    margin-left: 0;
  }
}

/* Appointments Tabs */
.appointments-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.tab-btn {
  padding: 0.75rem 1.5rem;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  color: #64748b;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn:hover {
  border-color: #10b981;
  color: #10b981;
}

.tab-btn.active {
  background: #10b981;
  border-color: #10b981;
  color: white;
}

/* Appointments Table */
.appointments-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.appointments-table-wrapper {
  overflow-x: auto;
}

.appointments-table {
  width: 100%;
  border-collapse: collapse;
}

.appointments-table th,
.appointments-table td {
  padding: 1rem 1.5rem;
  text-align: left;
}

.appointments-table th {
  background: #f8fafc;
  font-weight: 600;
  color: #64748b;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #e2e8f0;
}

.appointments-table td {
  border-bottom: 1px solid #e2e8f0;
}

.appointments-table tr:last-child td {
  border-bottom: none;
}

.table-doctor strong {
  color: #1e293b;
}

.status-badge-small {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
}

.status-badge-small.booked { background: #fef3c7; color: #92400e; }
.status-badge-small.completed { background: #d1fae5; color: #065f46; }
.status-badge-small.cancelled { background: #fee2e2; color: #991b1b; }
.status-badge-small.pending { background: #e0e7ff; color: #3730a3; }

.btn-action {
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-right: 0.5rem;
}

.btn-action.cancel {
  background: transparent;
  border: 1px solid #ef4444;
  color: #ef4444;
}

.btn-action.cancel:hover {
  background: #ef4444;
  color: white;
}

.btn-action.view {
  background: transparent;
  border: 1px solid #3b82f6;
  color: #3b82f6;
}

.btn-action.view:hover {
  background: #3b82f6;
  color: white;
}

/* Treatment History */
.treatments-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.treatment-history-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.treatment-history-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.treatment-history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.treatment-history-header .doctor-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.doctor-avatar-small {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.doctor-avatar-small svg {
  width: 20px;
  height: 20px;
}

.visit-date {
  text-align: right;
}

.date-label {
  display: block;
  font-size: 0.75rem;
  color: #64748b;
}

.date-value {
  font-weight: 600;
  color: #1e293b;
}

.treatment-history-body {
  padding: 1.5rem;
}

.treatment-detail {
  margin-bottom: 1rem;
}

.treatment-detail:last-child {
  margin-bottom: 0;
}

.detail-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #64748b;
  margin: 0 0 0.25rem 0;
}

.detail-value {
  color: #1e293b;
  margin: 0;
}

.treatment-history-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
}

/* Export Section */
.export-section {
  max-width: 500px;
}

.export-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.export-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: linear-gradient(135deg, #10b981, #059669);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  color: white;
}

.export-icon svg {
  width: 32px;
  height: 32px;
}

.export-title {
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.export-desc {
  color: #64748b;
  font-size: 0.875rem;
  margin: 0 0 1.5rem 0;
}

.btn-export {
  padding: 0.875rem 2rem;
  background: linear-gradient(135deg, #10b981, #059669);
  border: none;
  border-radius: 10px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-export:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.btn-export:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.export-message {
  margin-top: 1rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  background: #fee2e2;
  color: #991b1b;
  font-size: 0.875rem;
}

.export-message.success {
  background: #d1fae5;
  color: #065f46;
}

/* Treatments List in Dashboard */
.treatments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.treatment-card {
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.treatment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.treatment-date {
  font-size: 0.75rem;
  color: #64748b;
}

.treatment-body {
  margin-bottom: 0.75rem;
}

.diagnosis, .prescription {
  font-size: 0.875rem;
  color: #475569;
  margin: 0 0 0.5rem 0;
}

/* Modal */
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
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h4 {
  margin: 0;
  font-weight: 600;
  color: #1e293b;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #64748b;
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.modal-field {
  margin-bottom: 1rem;
}

.modal-field label {
  display: block;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #64748b;
  margin-bottom: 0.25rem;
}

.modal-field p {
  margin: 0;
  color: #1e293b;
}

@media (max-width: 768px) {
  .patient-dashboard {
    flex-direction: column;
  }

  .dashboard-content {
    padding: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .department-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .doctors-grid {
    grid-template-columns: 1fr;
  }
}
</style>
