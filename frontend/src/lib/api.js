import axios from 'axios';

// Create API client
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// API endpoints
export const endpoints = {
  // Auth endpoints
  auth: {
    login: '/api/auth/login',
    register: '/api/auth/register',
    me: '/api/auth/me',
  },
  
  // Mutual fund endpoints
  mutualFunds: {
    list: '/api/mutual-funds',
    detail: (id) => `/api/mutual-funds/${id}`,
    performance: (id) => `/api/mutual-funds/${id}/performance`,
    allocations: (id) => `/api/mutual-funds/${id}/allocations`,
    holdings: (id) => `/api/mutual-funds/${id}/holdings`,
  },
  
  // Investment endpoints
  investments: {
    list: '/api/investments',
    create: '/api/investments',
    detail: (id) => `/api/investments/${id}`,
  },
  
  // Portfolio endpoints
  portfolio: {
    summary: '/api/portfolio/summary',
    performance: '/api/portfolio/performance',
    composition: '/api/portfolio/composition',
    overlap: '/api/portfolio/overlap',
  },
};

// Auth API calls
export const authApi = {
  login: (credentials) => api.post(endpoints.auth.login, credentials),
  register: (userData) => api.post(endpoints.auth.register, userData),
  me: () => api.get(endpoints.auth.me),
};

// Mutual Funds API calls
export const mutualFundsApi = {
  list: () => api.get(endpoints.mutualFunds.list),
  detail: (id) => api.get(endpoints.mutualFunds.detail(id)),
  performance: (id) => api.get(endpoints.mutualFunds.performance(id)),
  allocations: (id) => api.get(endpoints.mutualFunds.allocations(id)),
  holdings: (id) => api.get(endpoints.mutualFunds.holdings(id)),
};

// Investment API calls
export const investmentsApi = {
  list: () => api.get(endpoints.investments.list),
  create: (investmentData) => api.post(endpoints.investments.create, investmentData),
  detail: (id) => api.get(endpoints.investments.detail(id)),
};

// Portfolio API calls
export const portfolioApi = {
  summary: () => api.get(endpoints.portfolio.summary),
  performance: (params) => api.get(endpoints.portfolio.performance, { params }),
  composition: () => api.get(endpoints.portfolio.composition),
  overlap: (params) => api.get(endpoints.portfolio.overlap, { params }),
};

export default api;