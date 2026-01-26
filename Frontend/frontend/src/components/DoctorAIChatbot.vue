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
          <h3>AI Scheduling Assistant</h3>
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
      <div v-for="(message, index) in messages" :key="index">
        <div :class="['message', message.type]">
          <div class="message-avatar">
            <svg v-if="message.type === 'bot'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
            </svg>
            <svg v-else fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div class="message-content">
            <div class="message-bubble" v-html="formatMessage(message.text)"></div>
            <span class="message-time">{{ formatTime(message.timestamp) }}</span>
            
            <!-- Created Slots Display - inline with the message -->
            <div v-if="message.created_slots && message.created_slots.length > 0" class="created-slots-inline">
              <div class="slots-summary">
                <strong>📅 Created {{ message.created_slots.length }} slot(s):</strong>
              </div>
              <div v-for="(slot, idx) in message.created_slots" :key="idx" class="slot-card-mini">
                <span class="slot-info">
                  <span class="slot-date-display">{{ slot.date_formatted || formatDisplayDate(slot.date) }}</span>
                  <span class="slot-time-display">{{ formatTimeRange(slot.start_time, slot.end_time) }}</span>
                </span>
                <span class="slot-badge">✓ Created</span>
              </div>
              <div v-if="message.created_slots.length > 5" class="slots-more">
                ... and {{ message.created_slots.length - 5 }} more slots
              </div>
            </div>

            <!-- Debug Raw AI Output -->
            <div v-if="message.debug_raw_ai" class="debug-raw-ai">
              <strong>Debug (AI Output):</strong>
              <pre>{{ message.debug_raw_ai }}</pre>
            </div>
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
        placeholder="Tell me when you'd like to be available (e.g., 'tomorrow 9am to 5pm')"
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

const userInput = ref("");
const messages = ref([]);
const isLoading = ref(false);
const messagesContainer = ref(null);

const suggestions = [
  "Create availability tomorrow 9am to 5pm",
  "Create availability Monday 10am to 4pm",
  "Show my current availability",
  "Delete slot",
  "View my appointments"
];

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

onMounted(() => {
  messages.value.push({
    type: "bot",
    text: `
👋 Hello Doctor! I'm your AI Scheduling Assistant.

I can help you:
• Create availability: "create availability tomorrow 9am to 5pm"
• View schedule: "show my current availability"
• Delete slots: "delete slot 5" or "delete slot #5"
• View appointments: "view my appointments"

💡 Tip: When you create availability, it creates one slot for the entire time range. You can delete individual slots later if needed.

How can I help you today?
    `,
    timestamp: new Date()
  });
});

const sendMessage = async (text) => {
  if (!text.trim()) return;

  messages.value.push({
    type: "user",
    text: text.trim(),
    timestamp: new Date()
  });

  userInput.value = "";
  isLoading.value = true;
  await scrollToBottom();

  try {
    const token = auth.getToken();

    const response = await fetch("http://localhost:5000/api/doctor/chatbot", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ message: text.trim() })
    });

    const data = await response.json();

    // Backend returns: { response: "...", created_slots: [...], debug_raw_ai: "..." }
    if (data.response) {
      messages.value.push({
        type: "bot",
        text: data.response,
        timestamp: new Date(),
        created_slots: data.created_slots || null,
        debug_raw_ai: data.debug_raw_ai || null
      });
    } else {
      messages.value.push({
        type: "bot",
        text: "⚠️ Unexpected response from server.",
        timestamp: new Date()
      });
    }

  } catch (err) {
    console.error(err);
    messages.value.push({
      type: "bot",
      text: "❌ Cannot reach the server. Please make sure backend is running.",
      timestamp: new Date()
    });

  } finally {
    isLoading.value = false;
    await scrollToBottom();
  }
};

const formatTime = (date) => {
  return new Date(date).toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit"
  });
};

const formatMessage = (text) => text.replace(/\n/g, "<br>");

const formatDisplayDate = (dateStr) => {
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric"
  });
};

const formatTimeRange = (startTime, endTime) => {
  // Handle both "HH:MM" and "HH:MM" formats
  const formatTime = (timeStr) => {
    if (!timeStr) return "";
    // If already formatted (contains AM/PM), return as is
    if (timeStr.includes("AM") || timeStr.includes("PM")) {
      return timeStr;
    }
    // Convert "HH:MM" to "H:MM AM/PM"
    const [hours, minutes] = timeStr.split(":");
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? "PM" : "AM";
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${minutes} ${ampm}`;
  };
  
  return `${formatTime(startTime)} - ${formatTime(endTime)}`;
};

const clearChat = () => {
  messages.value = [{
    type: "bot",
    text: `👋 Hello Doctor! I'm your AI Scheduling Assistant.

I can help you:
• Create availability: "create availability tomorrow 9am to 5pm"
• View schedule: "show my current availability"
• Delete slots: "delete slot 5" or "delete slot #5"
• View appointments: "view my appointments"

💡 Tip: When you create availability, it creates one slot for the entire time range. You can delete individual slots later if needed.

How can I help you today?`,
    timestamp: new Date()
  }];
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
  background: #a5b4fc;
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

/* Created Slots Display */
.created-slots {
  background: white;
  border-radius: 16px;
  padding: 1.25rem;
  border: 1px solid #e0e7ff;
  margin-top: 0.5rem;
}

.slots-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  color: #3730a3;
  margin: 0 0 1rem 0;
}

.slots-title svg {
  width: 20px;
  height: 20px;
  color: #5e63b6;
}

.slots-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.slot-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 0.875rem 1rem;
  background: #eef2ff;
  border-radius: 10px;
  border: 1px solid #c7d2fe;
}

.slot-date, .slot-time {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #374151;
}

.slot-date svg, .slot-time svg {
  width: 16px;
  height: 16px;
  color: #5e63b6;
}

.slot-status {
  margin-left: auto;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.slot-status.success {
  background: #e0e7ff;
  color: #3730a3;
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

/* Inline created slots */
.created-slots-inline {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 300px;
  overflow-y: auto;
  padding-right: 4px;
}

.slots-summary {
  font-size: 0.875rem;
  color: #374151;
  margin-bottom: 4px;
  font-weight: 600;
}

.slot-card-mini {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 0.85rem;
  border-left: 3px solid #4caf50;
  transition: transform 0.2s;
}

.slot-card-mini:hover {
  transform: translateX(2px);
}

.slot-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  color: #2e7d32;
  font-weight: 500;
}

.slot-date-display {
  font-weight: 600;
  font-size: 0.9rem;
}

.slot-time-display {
  font-size: 0.8rem;
  opacity: 0.9;
}

.slot-badge {
  background: #4caf50;
  color: white;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.slots-more {
  font-size: 0.8rem;
  color: #64748b;
  font-style: italic;
  text-align: center;
  padding: 4px;
}

@media (max-width: 768px) {
  .slot-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .slot-status {
    margin-left: 0;
  }
  
  .slot-card-mini {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
}
</style>
