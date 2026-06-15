import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to attach the token automatically
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const authAPI = {
  register: async (username, password) => {
    const response = await apiClient.post('/auth/register', { username, password });
    return response.data;
  },
  login: async (username, password) => {
    const response = await apiClient.post('/auth/login', { username, password });
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
    }
    return response.data;
  },
  logout: () => {
    localStorage.removeItem('token');
  },
  getMe: async () => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },
  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  }
};

export const glossaryAPI = {
  getAll: async () => {
    const response = await apiClient.get('/glossary/');
    return response.data;
  },
  create: async (source_term, target_term, notes) => {
    const response = await apiClient.post('/glossary/', { source_term, target_term, notes });
    return response.data;
  },
  update: async (id, data) => {
    const response = await apiClient.put(`/glossary/${id}`, data);
    return response.data;
  },
  delete: async (id) => {
    const response = await apiClient.delete(`/glossary/${id}`);
    return response.data;
  },
  uploadFile: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post('/glossary/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }
};

export const documentAPI = {
  getAll: async () => {
    const response = await apiClient.get('/document/');
    return response.data;
  },
  getDetail: async (id) => {
    const response = await apiClient.get(`/document/${id}`);
    return response.data;
  },
  upload: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post('/document/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
  translate: async (id) => {
    const response = await apiClient.post(`/document/${id}/translate`);
    return response.data;
  },
  stopTranslation: async (id) => {
    const response = await apiClient.post(`/document/${id}/stop`);
    return response.data;
  },
  updateChunk: async (chunkId, translated_text) => {
    const response = await apiClient.put(`/document/chunk/${chunkId}`, {
      translated_text,
      corrected_by_user: true
    });
    return response.data;
  },
  exportUrl: (id) => {
    const token = localStorage.getItem('token');
    return `${API_BASE_URL}/document/${id}/export?token=${token}`;
  }
};

export const settingsAPI = {
  getStatus: async () => {
    const response = await apiClient.get('/settings/status');
    return response.data;
  },
  saveSettings: async (openrouter_api_key) => {
    const response = await apiClient.post('/settings/save', { openrouter_api_key });
    return response.data;
  },
  pullModel: async () => {
    const response = await apiClient.post('/settings/pull-model');
    return response.data;
  }
};

export default apiClient;
