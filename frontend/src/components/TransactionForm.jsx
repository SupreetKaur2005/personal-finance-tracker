import React, { useState } from 'react';
import { transactionAPI } from '../services/api';

const TransactionForm = ({ onSuccess, currency = '$' }) => {
  const [formData, setFormData] = useState({
    description: '',
    amount: '',
    transaction_type: 'expense',
    category: ''
  });
  
  const [suggestedCategories, setSuggestedCategories] = useState([]);
  const [errors, setErrors] = useState([]);
  const [loading, setLoading] = useState(false);
  
  // Real-time categorization suggestions
  const handleDescriptionChange = async (e) => {
    const description = e.target.value;
    setFormData({ ...formData, description });
    
    if (description.length >= 3) {
      try {
        const response = await transactionAPI.suggestCategory(description);
        setSuggestedCategories(response.data.suggestions || []);
      } catch (err) {
        console.error('Failed to get suggestions:', err);
      }
    } else {
        setSuggestedCategories([]);
    }
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrors([]);
    
    try {
      const payload = {
        ...formData,
        amount: parseFloat(formData.amount)
      };
      
      await transactionAPI.create(payload);
      
      setFormData({ description: '', amount: '', transaction_type: 'expense', category: '' });
      setSuggestedCategories([]);
      if (onSuccess) onSuccess();
      
    } catch (err) {
      const errorMsg = err.response?.data?.detail;
      if (errorMsg) {
        if (Array.isArray(errorMsg)) {
          setErrors(errorMsg);
        } else {
          setErrors([errorMsg]);
        }
      } else {
        setErrors(['Failed to create transaction']);
      }
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="glass-card p-8 h-full flex flex-col justify-center">
      <div className="flex items-center gap-3 mb-8 border-b border-slate-100 pb-4">
         <div className="w-8 h-8 bg-slate-100 text-slate-900 flex items-center justify-center">
             <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="square" strokeLinejoin="miter" strokeWidth="2" d="M12 4v16m8-8H4" /></svg>
         </div>
         <h2 className="text-xl font-bold text-slate-900 tracking-tighter uppercase">New Transaction</h2>
      </div>

      {errors.length > 0 && (
        <div className="mb-6 p-4 rounded-xl bg-danger-50 border border-danger-100 flex items-start gap-3 animate-slide-up">
          <svg className="w-5 h-5 text-danger-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <ul className="list-disc list-inside text-sm text-danger-600">
            {errors.map((error, idx) => <li key={idx}>{error}</li>)}
          </ul>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="relative group">
          <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Description</label>
          <input
            type="text"
            value={formData.description}
            onChange={handleDescriptionChange}
            required
            placeholder="e.g. Sushi with friends"
            className="input-field"
          />
          
          {/* Rule-Based Category Suggestions */}
          <div className={`transition-all duration-300 ease-in-out overflow-hidden ${suggestedCategories.length > 0 ? 'max-h-32 opacity-100 mt-4' : 'max-h-0 opacity-0'}`}>
            <p className="text-[10px] text-slate-500 font-bold tracking-widest uppercase mb-3 flex items-center gap-2">
               <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="square" strokeLinejoin="miter" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
               Smart Category Suggestions
            </p>
            <div className="flex gap-2 flex-wrap">
              {suggestedCategories.map((cat, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => setFormData({ ...formData, category: cat.category })}
                  className={`px-3 py-1.5 text-xs font-bold uppercase tracking-wider transition-all duration-200 flex items-center gap-2 border ${
                      formData.category === cat.category 
                      ? 'bg-slate-900 border-slate-900 text-white' 
                      : 'bg-white border-slate-200 text-slate-600 hover:border-slate-400'
                  }`}
                >
                  <span className="text-sm">{cat.metadata?.icon || '🔹'}</span> 
                  <span className="capitalize">{cat.category}</span> 
                  <span className="opacity-60 ml-1">{(cat.confidence * 100).toFixed(0)}%</span>
                </button>
              ))}
            </div>
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Amount</label>
            <div className="relative">
               <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 font-medium">{currency}</span>
               <input
                 type="number"
                 value={formData.amount}
                 onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                 placeholder="0.00"
                 step="0.01"
                 min="0"
                 required
                 className="input-field pl-8"
               />
            </div>
          </div>
          
          <div>
            <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Type</label>
            <div className="relative">
               <select
                 value={formData.transaction_type}
                 onChange={(e) => setFormData({ ...formData, transaction_type: e.target.value })}
                 className="input-field appearance-none"
               >
                 <option value="expense">Expense</option>
                 <option value="income">Income</option>
               </select>
               <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-slate-400">
                  <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"/></svg>
               </div>
            </div>
          </div>
        </div>
        
        <div className="pt-6">
           <button
             type="submit"
             disabled={loading}
             className="btn-primary flex items-center justify-center gap-2"
           >
             {loading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Processing...
                </>
             ) : (
                <>
                  Save Transaction
                  <svg className="w-5 h-5 opacity-80 group-hover:translate-x-1 transition" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
                </>
             )}
           </button>
        </div>
      </form>
    </div>
  );
};

export default TransactionForm;
