import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export const getTransactions = async () => {
  const response = await api.get('/');
  return response.data.items;
};

export const deleteTransaction = async (id) => {
  const response = await api.delete(`/transaction/${id}`);
  return response.data;
};

export const getTransactionById = async (id) => {
  const response = await api.get(`/transaction/${id}`);
  return response.data;
};

export const addTransaction = async (transaction) => {
  const response = await api.post('/items', transaction);
  return response.data;
};