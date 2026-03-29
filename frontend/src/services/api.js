import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const transactionAPI = {
  // Create transaction
  create: (data) => 
    api.post('/transactions', data),
  
  // List transactions
  list: (skip = 0, limit = 100) =>
    api.get('/transactions', { params: { skip, limit } }),
  
  // Get summary
  getSummary: (year, month) =>
    api.get('/transactions/summary', { params: { year, month } }),
    
  // Suggest category
  suggestCategory: (description) =>
    api.post('/transactions/suggest-category', { description }),
    
  // Get Analytics Insights
  getInsights: () =>
    api.get('/transactions/analytics/insights'),
    
  // Batch Import
  batchImport: (formData) =>
    api.post('/transactions/batch/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }),
    
  // Batch Reclassify
  batchReclassify: (filter, newCategory) =>
    api.patch('/transactions/batch/reclassify', { filter, new_category: newCategory }),

  // Reclassify single transaction
  reclassify: (id, newCategory) =>
    api.patch(`/transactions/${id}/reclassify`, { category: newCategory }),
    
  // Update transaction status
  updateStatus: (id, newStatus, userId = 'system') =>
    api.patch(`/transactions/${id}/status`, { new_status: newStatus, user_id: userId }),

  // Delete transaction
  delete: (id) =>
    api.delete(`/transactions/${id}`),
};

export default api;
