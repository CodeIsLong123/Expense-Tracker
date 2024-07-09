import React, { useEffect, useState, useCallback } from 'react';
import { getTransactions, deleteTransaction, addTransaction } from './services/api';
import './App.css';

const TransactionList = ({ transactions, onDelete }) => (
  <ul className="transaction-list">
    {transactions.map(transaction => (
      <li key={transaction.id} className={`transaction-item ${transaction.category}`}>
        <span>{transaction.name}</span>
        <span>{transaction.category === 'income' ? '+' : '-'}${Math.abs(transaction.amount)}</span>
        <button className="delete-btn" onClick={() => onDelete(transaction.id)}>X</button>
      </li>
    ))}
  </ul>
);

const AddTransactionForm = ({ onAdd, isAdding }) => {
  const [newTransaction, setNewTransaction] = useState({ name: '', amount: '', category: '' });

  const handleSubmit = (e) => {
    e.preventDefault();
    onAdd(newTransaction);
    setNewTransaction({ name: '', amount: '', category: '' });
  };

  return (
    <form onSubmit={handleSubmit} className="add-transaction-form">
      <input
        type="text"
        placeholder="Enter text"
        value={newTransaction.name}
        onChange={(e) => setNewTransaction({ ...newTransaction, name: e.target.value })}
        required
      />
      <input
        type="number"
        placeholder="Enter amount"
        value={newTransaction.amount}
        onChange={(e) => setNewTransaction({ ...newTransaction, amount: e.target.value })}
        required
      />
      <select
        value={newTransaction.category}
        onChange={(e) => setNewTransaction({ ...newTransaction, category: e.target.value })}
        required
      >
        <option value="">Select Category</option>
        <option value="income">Income</option>
        <option value="expense">Expense</option>
      </select>
      <button type="submit" disabled={isAdding}>
        {isAdding ? 'Adding...' : 'Add transaction'}
      </button>
    </form>
  );
};

function App() {
  const [transactions, setTransactions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isAdding, setIsAdding] = useState(false);

  const fetchTransactions = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getTransactions();
      setTransactions(data);
    } catch (err) {
      setError('Failed to fetch transactions. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTransactions();
  }, [fetchTransactions]);

  const handleDelete = async (id) => {
    try {
      await deleteTransaction(id);
      setTransactions(transactions.filter(transaction => transaction.id !== id));
      console.log('Transaction deleted successfully',id);

    } catch (err) {
      setError('Failed to delete transaction. Please try again.');
    }
  };

  const handleAdd = async (newTransaction) => {
    setIsAdding(true);
    setError(null);
    try {
      const addedTransaction = await addTransaction(newTransaction);
      setTransactions([...transactions, addedTransaction]);
    } catch (err) {
      setError('Failed to add transaction. Please try again.');
      console.error('Error in handleAdd:', err);
    } finally {
      setIsAdding(false);
    }
  };

  const income = transactions
    .filter(t => t.category === 'income')
    .reduce((acc, t) => acc + parseFloat(t.amount), 0)
    .toFixed(2);

  const expense = transactions
    .filter(t => t.category === 'expense')
    .reduce((acc, t) => acc + parseFloat(t.amount), 0)
    .toFixed(2);

  const balance = (parseFloat(income) - parseFloat(expense)).toFixed(2);

  if (isLoading) return <div className="loading">Loading...</div>;

  return (
    <div className="App">
      <h1>Expense Tracker</h1>
      
      <div className="balance">
        <h2>YOUR BALANCE</h2>
        <p>{balance}kr</p>
      </div>
      
      <div className="income-expense">
        <div className="income">
          <h3>INCOME</h3>
          <p>{income}kr</p>
        </div>
        <div className="expense">
          <h3>EXPENSE</h3>
          <p>{expense}kr</p>
        </div>
      </div>
      
      <h2>History</h2>
      <TransactionList transactions={transactions} onDelete={handleDelete} />
      
      <h2>Add new transaction</h2>
      <AddTransactionForm onAdd={handleAdd} isAdding={isAdding} />

      {error && <div className="error">{error}</div>}
    </div>
  );
}

export default App;