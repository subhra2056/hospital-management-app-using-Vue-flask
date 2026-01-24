<template>
  <div class="chatbot-container">
    <div class="chat-header">
      <div class="header-content">
        <div class="bot-avatar">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
          </svg>
        </div>
        <div class="header-info">
          <h3>AI Health Assistant</h3>
          <span class="status">
            <span class="status-dot"></span>
            Online
          </span>
        </div>
      </div>
      <button class="clear-btn" @click="clearChat" title="Clear chat">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
        </svg>
      </button>
    </div>

    <div class="chat-messages" ref="messagesContainer">
      <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
        <div class="message-avatar">
          <svg v-if="message.type === 'bot'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
          </svg>
          <svg v-else fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
          </svg>
        </div>
        <div class="message-content">
          <div class="message-bubble" v-html="formatMessage(message.text)"></div>
          <span class="message-time">{{ formatTime(message.timestamp) }}</span>
        </div>
      </div>

      <!-- Doctor Recommendations -->
      <div v-if="recommendedDoctors.length > 0" class="doctor-recommendations">
        <h4 class="recommendations-title">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
          </svg>
          Recommended Doctors
        </h4>
        <div class="doctor-cards">
          <div v-for="doctor in recommendedDoctors" :key="doctor.id" class="doctor-card">
            <div class="doctor-avatar">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </div>
            <div class="doctor-info">
              <h5 class="doctor-name">Dr. {{ doctor.username }}</h5>
              <p class="doctor-specialization">{{ doctor.specialization }}</p>
              <p class="doctor-department">{{ doctor.department_name }}</p>
              <div class="doctor-experience">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span>{{ doctor.experience_years || 0 }} years experience</span>
              </div>
            </div>
            <button class="book-btn" @click="$emit('bookDoctor', doctor)">
              Book Appointment
            </button>
          </div>
        </div>
      </div>

      <!-- Loading indicator -->
      <div v-if="isLoading" class="message bot">
        <div class="message-avatar">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
          </svg>
        </div>
        <div class="message-content">
          <div class="message-bubble typing">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Suggestions -->
    <div class="quick-suggestions">
      <button 
        v-for="suggestion in suggestions" 
        :key="suggestion" 
        class="suggestion-btn"
        @click="sendMessage(suggestion)"
      >
        {{ suggestion }}
      </button>
    </div>

    <div class="chat-input">
      <input 
        v-model="userInput" 
        type="text" 
        placeholder="Describe your symptoms or ask about doctors..."
        @keyup.enter="sendMessage(userInput)"
        :disabled="isLoading"
      />
      <button class="send-btn" @click="sendMessage(userInput)" :disabled="!userInput.trim() || isLoading">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import auth from "../utils/auth";

const emit = defineEmits(["bookDoctor"]);

const userInput = ref("");
const messages = ref([]);
const recommendedDoctors = ref([]);
const isLoading = ref(false);
const messagesContainer = ref(null);

const suggestions = [
  "I have a headache",
  "Heart problems",
  "Skin issues",
  "Child health",
  "Back pain"
];

const getToken = () => auth.getToken();

onMounted(() => {
  // Welcome message
  messages.value.push({
    type: "bot",
    text: "👋 Hello! I'm your AI Health Assistant. I can help you find the right doctor based on your symptoms or health concerns.\n\nYou can:\n• Describe your symptoms\n• Ask about specific departments\n• Search for doctors by specialization\n\nHow can I help you today?",
    timestamp: new Date()
  });
});

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const formatTime = (date) => {
  return new Date(date).toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit"
  });
};

const formatMessage = (text) => {
  // Convert newlines to <br> and preserve formatting
  return text.replace(/\n/g, "<br>");
};

const sendMessage = async (text) => {
  if (!text.trim()) return;

  // Add user message
  messages.value.push({
    type: "user",
    text: text.trim(),
    timestamp: new Date()
  });

  userInput.value = "";
  recommendedDoctors.value = [];
  isLoading.value = true;
  await scrollToBottom();

  try {
    const response = await fetch("http://localhost:5000/api/chatbot/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getToken()}`
      },
      body: JSON.stringify({ message: text.trim() })
    });

    const data = await response.json();

    if (response.ok) {
      // Add bot response
      messages.value.push({
        type: "bot",
        text: data.response,
        timestamp: new Date()
      });

      // Show recommended doctors if any
      if (data.doctors && data.doctors.length > 0) {
        recommendedDoctors.value = data.doctors;
      }
    } else {
      // Show more specific error message
      const errorMsg = data.message || data.msg || "I'm sorry, I couldn't process your request. Please try again.";
      messages.value.push({
        type: "bot",
        text: response.status === 401 
          ? "Your session has expired. Please log out and log back in to continue."
          : errorMsg,
        timestamp: new Date()
      });
    }
  } catch (error) {
    console.error("Chatbot error:", error);
    messages.value.push({
      type: "bot",
      text: "I'm having trouble connecting to the server. Please make sure the backend server is running and try again.",
      timestamp: new Date()
    });
  } finally {
    isLoading.value = false;
    await scrollToBottom();
  }
};

const clearChat = () => {
  messages.value = [{
    type: "bot",
    text: "👋 Hello! I'm your AI Health Assistant. How can I help you today?",
    timestamp: new Date()
  }];
  recommendedDoctors.value = [];
};
</script>

<style scoped>
.chatbot-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, #5e63b6, #4a50a0);
  color: white;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.bot-avatar {
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bot-avatar svg {
  width: 28px;
  height: 28px;
}

.header-info h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  opacity: 0.9;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.clear-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 8px;
  padding: 0.5rem;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
}

.clear-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.clear-btn svg {
  width: 20px;
  height: 20px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: #f8fafc;
}

.message {
  display: flex;
  gap: 0.75rem;
  max-width: 85%;
}

.message.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message.bot {
  align-self: flex-start;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message.bot .message-avatar {
  background: linear-gradient(135deg, #5e63b6, #4a50a0);
  color: white;
}

.message.user .message-avatar {
  background: #e2e8f0;
  color: #64748b;
}

.message-avatar svg {
  width: 20px;
  height: 20px;
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.message.user .message-content {
  align-items: flex-end;
}

.message-bubble {
  padding: 0.875rem 1.25rem;
  border-radius: 16px;
  line-height: 1.5;
  font-size: 0.9375rem;
}

.message.bot .message-bubble {
  background: white;
  color: #1e293b;
  border: 1px solid #e2e8f0;
  border-bottom-left-radius: 4px;
}

.message.user .message-bubble {
  background: linear-gradient(135deg, #5e63b6, #4a50a0);
  color: white;
  border-bottom-right-radius: 4px;
}

.message-time {
  font-size: 0.75rem;
  color: #94a3b8;
}

/* Typing indicator */
.typing {
  display: flex;
  gap: 4px;
  padding: 1rem 1.25rem;
}

.typing .dot {
  width: 8px;
  height: 8px;
  background: #94a3b8;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing .dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing .dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

/* Doctor Recommendations */
.doctor-recommendations {
  background: white;
  border-radius: 16px;
  padding: 1.25rem;
  border: 1px solid #e2e8f0;
  margin-top: 0.5rem;
}

.recommendations-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 1rem 0;
}

.recommendations-title svg {
  width: 20px;
  height: 20px;
  color: #5e63b6;
}

.doctor-cards {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.doctor-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s;
}

.doctor-card:hover {
  border-color: #5e63b6;
  box-shadow: 0 4px 12px rgba(94, 99, 182, 0.1);
}

.doctor-card .doctor-avatar {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #e0e7ff, #c7d2fe);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.doctor-card .doctor-avatar svg {
  width: 24px;
  height: 24px;
  color: #5e63b6;
}

.doctor-card .doctor-info {
  flex: 1;
  min-width: 0;
}

.doctor-card .doctor-name {
  margin: 0 0 0.25rem 0;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #1e293b;
}

.doctor-card .doctor-specialization {
  margin: 0 0 0.125rem 0;
  font-size: 0.8125rem;
  color: #5e63b6;
  font-weight: 500;
}

.doctor-card .doctor-department {
  margin: 0 0 0.375rem 0;
  font-size: 0.8125rem;
  color: #64748b;
}

.doctor-experience {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.75rem;
  color: #94a3b8;
}

.doctor-experience svg {
  width: 14px;
  height: 14px;
}

.book-btn {
  padding: 0.625rem 1rem;
  background: linear-gradient(135deg, #5e63b6, #4a50a0);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.book-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(94, 99, 182, 0.3);
}

/* Quick Suggestions */
.quick-suggestions {
  display: flex;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  overflow-x: auto;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
}

.quick-suggestions::-webkit-scrollbar {
  display: none;
}

.suggestion-btn {
  padding: 0.5rem 1rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  font-size: 0.8125rem;
  color: #64748b;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.suggestion-btn:hover {
  background: #5e63b6;
  border-color: #5e63b6;
  color: white;
}

/* Chat Input */
.chat-input {
  display: flex;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  background: white;
  border-top: 1px solid #e2e8f0;
}

.chat-input input {
  flex: 1;
  padding: 0.875rem 1.25rem;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 0.9375rem;
  outline: none;
  transition: all 0.2s;
}

.chat-input input:focus {
  border-color: #5e63b6;
  box-shadow: 0 0 0 3px rgba(94, 99, 182, 0.1);
}

.chat-input input::placeholder {
  color: #94a3b8;
}

.send-btn {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #5e63b6, #4a50a0);
  border: none;
  border-radius: 12px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(94, 99, 182, 0.3);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-btn svg {
  width: 22px;
  height: 22px;
}

@media (max-width: 768px) {
  .doctor-card {
    flex-direction: column;
    text-align: center;
  }

  .doctor-card .doctor-info {
    text-align: center;
  }

  .doctor-experience {
    justify-content: center;
  }
}
</style>
