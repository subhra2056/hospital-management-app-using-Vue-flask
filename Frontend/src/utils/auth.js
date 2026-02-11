// Auth storage utility - uses sessionStorage for security
// sessionStorage is cleared when the browser tab is closed
// This prevents session persistence when URLs are shared or opened in new browsers

const storage = sessionStorage;

export const auth = {
  // Token management
  getToken: () => storage.getItem("access_token"),
  setToken: (token) => storage.setItem("access_token", token),
  removeToken: () => storage.removeItem("access_token"),

  // User management
  getUser: () => {
    try {
      const userStr = storage.getItem("user");
      return userStr ? JSON.parse(userStr) : null;
    } catch (e) {
      return null;
    }
  },
  setUser: (user) => storage.setItem("user", JSON.stringify(user)),
  removeUser: () => storage.removeItem("user"),

  // Role management
  getRole: () => storage.getItem("role"),
  setRole: (role) => storage.setItem("role", role),
  removeRole: () => storage.removeItem("role"),

  // Check if logged in
  isLoggedIn: () => !!storage.getItem("access_token"),

  // Clear all auth data (logout)
  clearAll: () => {
    storage.removeItem("access_token");
    storage.removeItem("user");
    storage.removeItem("role");
  },

  // Save login data
  saveLoginData: (token, user, role) => {
    storage.setItem("access_token", token);
    storage.setItem("user", JSON.stringify(user));
    storage.setItem("role", role);
  }
};

export default auth;
