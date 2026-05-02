import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1"
});

export const authHeader = () => {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const setAuthToken = (token) => {
  localStorage.setItem("token", token);
  window.dispatchEvent(new Event("auth-updated"));
};

export const clearAuthToken = () => {
  localStorage.removeItem("token");
  window.dispatchEvent(new Event("auth-updated"));
};
