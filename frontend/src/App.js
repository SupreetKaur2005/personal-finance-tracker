import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import TransactionForm from './components/TransactionForm';
import TransactionTable from './components/TransactionTable';

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [isExpanded, setIsExpanded] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [userProfile, setUserProfile] = useState({
    name: 'HQ',
    email: '',
    currency: '$'
  });

  useEffect(() => {
    const savedName = localStorage.getItem('app_profile_name');
    const savedEmail = localStorage.getItem('app_profile_email');
    const savedCurrency = localStorage.getItem('app_profile_currency');
    
    setUserProfile({
      name: savedName || 'HQ',
      email: savedEmail || '',
      currency: savedCurrency || '$'
    });
  }, []);

  const handleSaveProfile = (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const updatedProfile = {
      name: formData.get('name') || 'HQ',
      email: formData.get('email'),
      currency: formData.get('currency')
    };
    
    localStorage.setItem('app_profile_name', updatedProfile.name);
    localStorage.setItem('app_profile_email', updatedProfile.email);
    localStorage.setItem('app_profile_currency', updatedProfile.currency);
    
    setUserProfile(updatedProfile);
    setIsProfileOpen(false);
  };

  const getInitials = (name) => {
    if (!name || name === 'HQ') return 'HQ';
    return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
  };

  return (
    <div className="min-h-screen relative bg-[#F8F9FA]">
      
      {/* Stark, minimalist Header */}
      <nav className="sticky top-0 z-50 bg-white border-b border-slate-200">
        <div className="max-w-[96%] mx-auto px-4 md:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-none bg-slate-900 flex items-center justify-center text-white font-bold text-xl">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="square" strokeLinejoin="miter" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h1 className="text-xl font-bold text-slate-900 tracking-tighter">
              FINANCE
            </h1>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm font-semibold text-slate-500 uppercase tracking-widest">Client Portal</span>
            <div 
              onClick={() => setIsProfileOpen(true)}
              className="w-9 h-9 border-2 border-slate-900 flex items-center justify-center text-slate-900 font-bold cursor-pointer hover:bg-slate-900 hover:text-white transition-colors"
            >
              {getInitials(userProfile.name)}
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-[96%] mx-auto px-4 md:px-8 py-10 relative z-10 animate-fade-in">
        <Dashboard refreshTrigger={refreshTrigger} currency={userProfile.currency} />
        
        <div className="mt-12 grid grid-cols-1 lg:grid-cols-3 gap-8 ">
          {!isExpanded && (
            <div className="lg:col-span-1 animate-slide-up" style={{animationDelay: '0.1s'}}>
              <TransactionForm
                onSuccess={() => setRefreshTrigger(prev => prev + 1)}
                currency={userProfile.currency}
              />
            </div>
          )}
          
          <div className={`${isExpanded ? 'lg:col-span-3' : 'lg:col-span-2'} animate-slide-up transition-all duration-300`} style={{animationDelay: '0.2s'}} id="transaction-table-section">
            <div className="glass-card p-6 h-full flex flex-col">
              <div className="flex justify-between items-center mb-6 border-b border-slate-100 pb-4">
                 <h2 className="text-lg font-bold text-slate-900 tracking-tight uppercase">Ledger</h2>
                 <button onClick={() => {
                   setIsExpanded(!isExpanded);
                   document.getElementById('transaction-table-section').scrollIntoView({ behavior: 'smooth' });
                 }} className="text-sm text-slate-500 font-semibold hover:text-slate-900 flex items-center gap-1 transition-colors uppercase tracking-wider">
                   {isExpanded ? (
                     <><span aria-hidden="true">&larr;</span> Collapse</>
                   ) : (
                     <>Expand <span aria-hidden="true">&rarr;</span></>
                   )}
                 </button>
              </div>
              <TransactionTable refreshTrigger={refreshTrigger} currency={userProfile.currency} />
            </div>
          </div>
        </div>
      </main>

      {/* Profile Modal */}
      {isProfileOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-slate-900/40 backdrop-blur-sm p-4 animate-fade-in">
          <div className="bg-white border border-slate-200 shadow-2xl w-full max-w-md animate-slide-up p-8">
            <div className="flex justify-between items-center mb-6 border-b border-slate-100 pb-4">
               <h2 className="text-xl font-bold text-slate-900 tracking-tighter uppercase">Client Profile</h2>
               <button onClick={() => setIsProfileOpen(false)} className="text-slate-400 hover:text-slate-900">
                 <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="square" strokeLinejoin="miter" strokeWidth="2" d="M6 18L18 6M6 6l12 12" /></svg>
               </button>
            </div>
            
            <form onSubmit={handleSaveProfile} className="space-y-6">
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Display Name</label>
                <input 
                  type="text" 
                  name="name" 
                  defaultValue={userProfile.name !== 'HQ' ? userProfile.name : ''} 
                  className="w-full text-sm px-4 py-3 bg-slate-50 border border-slate-200 outline-none focus:border-slate-900 focus:bg-white transition-colors text-slate-900" 
                  placeholder="e.g. John Doe" 
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Email Address</label>
                <input 
                  type="email" 
                  name="email" 
                  defaultValue={userProfile.email} 
                  className="w-full text-sm px-4 py-3 bg-slate-50 border border-slate-200 outline-none focus:border-slate-900 focus:bg-white transition-colors text-slate-900" 
                  placeholder="name@company.com" 
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Preferred Currency</label>
                <select 
                  name="currency" 
                  defaultValue={userProfile.currency} 
                  className="w-full text-sm px-4 py-3 bg-slate-50 border border-slate-200 outline-none focus:border-slate-900 focus:bg-white transition-colors text-slate-900 cursor-pointer"
                >
                  <option value="$">US Dollar ($)</option>
                  <option value="€">Euro (€)</option>
                  <option value="£">British Pound (£)</option>
                  <option value="¥">Japanese Yen (¥)</option>
                  <option value="₹">Indian Rupee (₹)</option>
                </select>
              </div>
              
              <div className="pt-4 flex gap-3">
                <button type="button" onClick={() => setIsProfileOpen(false)} className="flex-1 py-3 border border-slate-300 text-slate-600 text-xs font-bold uppercase tracking-widest hover:border-slate-900 hover:text-slate-900 transition-colors">
                  Cancel
                </button>
                <button type="submit" className="flex-1 py-3 bg-slate-900 text-white text-xs font-bold uppercase tracking-widest hover:bg-slate-800 focus:ring-2 focus:ring-slate-900 transition-colors">
                  Save Settings
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
