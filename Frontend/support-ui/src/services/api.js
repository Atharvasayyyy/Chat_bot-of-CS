import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "https://customer-support-api.onrender.com",
  timeout: 5000,
});

export const sendMessage = (formData) => API.post("/chat", formData);

export const getUserOrders = (userId) => API.get(`/orders/${userId}`);

export const getDashboard = () => API.get("/dashboard");

export const getDatabaseTables = () => API.get("/database");

export const updateTicket = (id, status) =>
  API.post("/admin/ticket/update", null, {
    params: { ticket_id: id, status },
  });

export const updateExchange = (id, status) =>
  API.post("/admin/exchange/update", null, {
    params: { exchange_id: id, status },
  });

export default API;