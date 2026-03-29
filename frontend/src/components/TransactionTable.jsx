import React, { useState, useEffect, useMemo } from 'react';
import { transactionAPI } from '../services/api';

const TransactionTable = ({ refreshTrigger, currency = '$' }) => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Filters
  const [filterMonth, setFilterMonth] = useState('');
  const [filterType, setFilterType] = useState('');
  const [filterCategory, setFilterCategory] = useState('');
  
  // Inline editing
  const [editingId, setEditingId] = useState(null);
  const [editingCategory, setEditingCategory] = useState('');

  useEffect(() => {
    fetchTransactions();
  }, [refreshTrigger]);

  const fetchTransactions = async () => {
    try {
      const response = await transactionAPI.list();
      setTransactions(response.data);
    } catch (err) {
      console.error('Failed to fetch transactions:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete this transaction?')) {
      try {
        await transactionAPI.delete(id);
        fetchTransactions();
      } catch (err) {
        console.error('Failed to delete:', err);
      }
    }
  };
  
  const handleReclassifySubmit = async (id) => {
    if (!editingCategory.trim()) return;
    try {
      await transactionAPI.reclassify(id, editingCategory);
      setEditingId(null);
      fetchTransactions();
    } catch (err) {
      console.error('Failed to reclassify:', err);
    }
  };

  const filteredTransactions = useMemo(() => {
    return transactions.filter(tx => {
      // Month format expects 'YYYY-MM'
      const txMonth = new Date(tx.timestamp).toISOString().slice(0, 7);
      if (filterMonth && txMonth !== filterMonth) return false;
      if (filterType && tx.transaction_type !== filterType) return false;
      if (filterCategory && tx.category !== filterCategory) return false;
      return true;
    });
  }, [transactions, filterMonth, filterType, filterCategory]);

  // Derived options for filter dropdowns
  const uniqueMonths = [...new Set(transactions.map(tx => new Date(tx.timestamp).toISOString().slice(0, 7)))].sort().reverse();
  const uniqueCategories = [...new Set(transactions.map(tx => tx.category))].sort();

  const formatMonth = (yyyyMm) => {
    const [year, month] = yyyyMm.split('-');
    const date = new Date(year, parseInt(month) - 1);
    return date.toLocaleString('default', { month: 'long', year: 'numeric' });
  };
  
  const handleExportCSV = () => {
    if (filteredTransactions.length === 0) return;
    const headers = ['Date', 'Description', 'Category', 'Type', 'Amount', 'Status', 'Auto-Tagged'];
    const rows = filteredTransactions.map(tx => [
      new Date(tx.timestamp).toISOString().slice(0, 10),
      `"${tx.description.replace(/"/g, '""')}"`,
      tx.category,
      tx.transaction_type,
      tx.amount,
      tx.status || 'verified',
      tx.auto_tagged ? 'Yes' : 'No'
    ]);
    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(","), ...rows.map(r => r.join(","))].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "transactions_export.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (loading) {
    return (
      <div className="w-full flex justify-center py-12">
        <div className="w-8 h-8 border-2 border-slate-200 border-t-slate-800 rounded-full animate-spin"></div>
      </div>
    );
  }

  if (transactions.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-slate-400 py-12 animate-fade-in border-2 border-slate-200 bg-white">
        <div className="w-16 h-16 bg-slate-50 flex items-center justify-center mb-4 border border-slate-200">
           <svg className="w-8 h-8 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="square" strokeLinejoin="miter" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        </div>
        <p className="font-bold text-slate-500 uppercase tracking-widest text-xs">No transactions recorded yet.</p>
        <p className="text-xs mt-1 text-slate-400">Add your first transaction using the form.</p>
      </div>
    );
  }

  return (
    <div className="w-full flex flex-col gap-4">
      {/* Filters Bar */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-2">
        <div className="flex gap-4">
          <select 
            className="text-sm px-3 py-1.5 border border-slate-300 rounded-sm outline-none focus:ring-0 focus:border-slate-900 bg-white"
            value={filterMonth} onChange={e => setFilterMonth(e.target.value)}
          >
            <option value="">All Months</option>
            {uniqueMonths.map(m => <option key={m} value={m}>{formatMonth(m)}</option>)}
          </select>
          
          <select 
            className="text-sm px-3 py-1.5 border border-slate-300 rounded-sm outline-none focus:ring-0 focus:border-slate-900 bg-white"
            value={filterType} onChange={e => setFilterType(e.target.value)}
          >
            <option value="">All Types</option>
            <option value="income">Income</option>
            <option value="expense">Expense</option>
          </select>
          
          <select 
            className="text-sm px-3 py-1.5 border border-slate-300 rounded-sm outline-none focus:ring-0 focus:border-slate-900 bg-white"
            value={filterCategory} onChange={e => setFilterCategory(e.target.value)}
          >
            <option value="">All Categories</option>
            {uniqueCategories.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
        
        <button 
          onClick={handleExportCSV} 
          disabled={filteredTransactions.length === 0}
          className="text-xs uppercase tracking-widest px-4 py-2 bg-slate-900 disabled:opacity-50 hover:bg-slate-800 text-white font-bold rounded-sm flex items-center gap-2 transition outline-none focus:ring-2 focus:ring-slate-900 shadow-sm"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="square" strokeLinejoin="miter" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
          Export CSV
        </button>
      </div>

      {/* Table */}
      <div className="w-full overflow-hidden flex-1 bg-white border border-slate-200 shadow-sm">
        <div className="overflow-x-auto h-[400px] overflow-y-auto w-full">
          <table className="w-full whitespace-nowrap text-left border-collapse">
            <thead className="sticky top-0 z-10 bg-white border-b-2 border-slate-900 text-xs font-bold text-slate-900 uppercase tracking-widest">
              <tr>
                <th className="px-6 py-4">Date</th>
                <th className="px-6 py-4">Description</th>
                <th className="px-6 py-4">Category</th>
                <th className="px-6 py-4 text-right">Amount</th>
                <th className="px-6 py-4 text-center">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100/80 bg-white">
              {filteredTransactions.map((tx) => (
                <tr key={tx.id} className="hover:bg-slate-50/50 transition-colors duration-150 group">
                  <td className="px-6 py-4 text-sm text-slate-500">
                    {new Date(tx.timestamp).toLocaleDateString(undefined, {
                      month: 'short', day: 'numeric', year: 'numeric'
                    })}
                  </td>
                  <td className="px-6 py-4 whitespace-normal min-w-[200px]">
                    <span className="font-medium text-slate-800">{tx.description}</span>
                  </td>
                  <td className="px-6 py-4">
                    {editingId === tx.id ? (
                      <div className="flex items-center gap-2">
                         <input 
                           autoFocus
                           className="text-xs px-2 py-1 border border-slate-900 rounded-sm outline-none ring-0"
                           value={editingCategory}
                           onChange={e => setEditingCategory(e.target.value)}
                           onKeyDown={e => e.key === 'Enter' && handleReclassifySubmit(tx.id)}
                         />
                         <button onClick={() => handleReclassifySubmit(tx.id)} className="text-slate-900 hover:text-black">
                           <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="square" strokeLinejoin="miter" strokeWidth="2" d="M5 13l4 4L19 7" /></svg>
                         </button>
                         <button onClick={() => setEditingId(null)} className="text-slate-400 hover:text-slate-600">
                           <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="square" strokeLinejoin="miter" strokeWidth="2" d="M6 18L18 6M6 6l12 12" /></svg>
                         </button>
                      </div>
                    ) : (
                      <div className="flex items-center gap-2">
                         <span className={`inline-flex items-center px-2 py-0.5 rounded-none text-[10px] font-bold uppercase tracking-widest border
                            ${tx.auto_tagged ? 'bg-slate-900 text-white border-slate-900' : 'bg-white text-slate-600 border-slate-300'}`}>
                            {tx.category || 'Uncategorized'}
                         </span>
                         {tx.auto_tagged && (
                             <span title="Auto-tagged by AI" className="text-slate-400">
                                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="square" strokeLinejoin="miter" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                             </span>
                         )}
                         <button 
                           onClick={() => { setEditingId(tx.id); setEditingCategory(tx.category); }} 
                           className="opacity-0 group-hover:opacity-100 text-slate-400 hover:text-slate-900 transition"
                           title="Reclassify Category"
                         >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="square" strokeLinejoin="miter" strokeWidth="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                         </button>
                      </div>
                    )}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <span className={`font-bold ${
                      tx.transaction_type === 'income' ? 'text-success-600' : 'text-danger-600'
                    }`}>
                      {tx.transaction_type === 'income' ? '+' : '-'}{currency}{Math.abs(tx.amount).toFixed(2)}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-center">
                    <button
                      onClick={() => handleDelete(tx.id)}
                      className="p-1.5 text-slate-400 hover:text-danger-500 hover:bg-danger-50 rounded-lg transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100 outline-none"
                      title="Delete Record"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default TransactionTable;
