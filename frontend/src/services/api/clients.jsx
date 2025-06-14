import axios from 'axios';

const client = axios.create({
  baseURL: 'http://localhost:8000/api',
});

client.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default client;
