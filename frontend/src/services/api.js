import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Jobs API
export const jobsAPI = {
  getAll: (params = {}) => api.get('/jobs', { params }),
  getById: (id) => api.get(`/jobs/${id}`),
  create: (data) => api.post('/jobs', data),
  delete: (id) => api.delete(`/jobs/${id}`),
  calculateMatch: (jobId, userId) =>
    api.post(`/jobs/${jobId}/calculate-match`, null, { params: { user_id: userId } }),
  searchBySkills: (skills) =>
    api.get('/jobs/search/skills', { params: { skills } }),
}

// Applications API
export const applicationsAPI = {
  getAll: (params = {}) => api.get('/applications', { params }),
  getById: (id) => api.get(`/applications/${id}`),
  create: (data) => api.post('/applications', data),
  update: (id, data) => api.put(`/applications/${id}`, data),
  delete: (id) => api.delete(`/applications/${id}`),
  generateCoverLetter: (id, tone = 'professional') =>
    api.post(`/applications/${id}/generate-cover-letter`, null, { params: { tone } }),
  getStats: (userId) => api.get(`/applications/stats/user/${userId}`),
}

// Users API
export const usersAPI = {
  create: (data) => api.post('/users', data),
  getById: (id) => api.get(`/users/${id}`),
  createProfile: (userId, data) => api.post(`/users/${userId}/profile`, data),
  getProfile: (userId) => api.get(`/users/${userId}/profile`),
}

// Scraper API
export const scraperAPI = {
  scrape: (data) => api.post('/scraper/scrape', data),
  scrapeSync: (data) => api.post('/scraper/scrape-sync', data),
}

export default api
