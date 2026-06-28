import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/', // Endereço do seu backend Django
});

export default api;