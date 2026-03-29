import React, { useState, useEffect } from 'react';
import { transactionAPI } from '../services/api';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler
} from 'chart.js';
import { Bar as BarChart, Doughnut as DoughnutChart, Line as LineChart } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale, LinearScale, PointElement, LineElement, BarElement,
  Title, Tooltip, Legend, ArcElement, Filler
);

ChartJS.defaults.font.family = "'Inter', sans-serif";
ChartJS.defaults.color = '#64748b';

const Dashboard = ({ refreshTrigger, currency }) => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [chartType, setChartType] = useState('doughnut');

  useEffect(() => {
    fetchSummary();
  }, [refreshTrigger]);

  const fetchSummary = async () => {
    try {
      const response = await transactionAPI.getSummary();
      const rawData = response.data.data;
      
      // Get the latest month for display
      const months = Object.keys(rawData).sort();
      const latestMonth = months[months.length - 1];
      
      if (latestMonth) {
        setSummary({ month: latestMonth, ...rawData[latestMonth] });
      } else {
        setSummary({
          month: 'No Data',
          income_total: 0,
          expense_total: 0,
          net: 0,
          by_category: {}
        });
      }
    } catch (err) {
      console.error('Failed to fetch summary:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !summary) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 animate-pulse">
        {[1,2,3].map(i => (
          <div key={i} className="glass-card h-32 flex items-center justify-center">
             <div className="w-8 h-8 border-2 border-slate-200 border-t-slate-800 rounded-full animate-spin"></div>
          </div>
        ))}
      </div>
    );
  }

  // Sophisticated minimal colors
  const categoryColors = [
    '#0f172a', // slate-900
    '#334155', // slate-700
    '#64748b', // slate-500
    '#94a3b8', // slate-400
    '#2563eb', // blue-600 (accent)
    '#dc2626', // red-600 (accent)
    '#1d4ed8', // blue-700
  ];

  const chartData = {
    labels: Object.keys(summary.by_category),
    datasets: [
      {
        label: 'Spending amount',
        data: Object.values(summary.by_category),
        backgroundColor: chartType === 'line' ? '#0f172a' : categoryColors,
        borderColor: chartType === 'line' ? '#0f172a' : categoryColors,
        borderWidth: chartType === 'doughnut' ? 0 : 2,
        tension: 0.2, // For smooth Line charts
        hoverOffset: 4,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '75%', // Thinner ring
    plugins: {
      legend: {
        position: 'right',
        labels: { boxWidth: 12, usePointStyle: true, padding: 20 }
      }
    }
  };

  const StatCard = ({ title, amount, type, icon }) => {
    return (
      <div className="glass-card p-6 flex flex-col justify-between">
        <div className="flex justify-between items-start mb-4 border-b border-slate-100 pb-2">
          <h3 className="text-xs font-bold text-slate-500 tracking-widest uppercase">{title}</h3>
          <div className="text-slate-900">
            {icon}
          </div>
        </div>
        <div>
          <p className="text-4xl font-bold tracking-tighter text-slate-900">
            {currency}{Math.abs(amount).toFixed(2)}
          </p>
          <p className="text-xs text-slate-500 mt-2 font-semibold uppercase tracking-widest">For {summary.month}</p>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-8 fade-in">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard 
          title="Total Income" 
          amount={summary.income_total} 
          type="income" 
          icon={(
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" /></svg>
          )}
        />
        <StatCard 
          title="Total Expenses" 
          amount={summary.expense_total} 
          type="expense"
          icon={(
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" /></svg>
          )} 
        />
        <StatCard 
          title="Net Cashflow" 
          amount={summary.net} 
          type="net"
          icon={(
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          )} 
        />
      </div>

      <div className="glass-card p-6">
        <div className="border-b border-slate-100 pb-4 mb-6 flex justify-between items-center">
          <h3 className="text-lg font-bold text-slate-900 uppercase tracking-tight">Spending Breakdown</h3>
          <div className="flex bg-slate-100 p-1 border border-slate-200">
             <button 
                onClick={() => setChartType('doughnut')} 
                className={`px-3 py-1 text-xs font-bold uppercase tracking-widest ${chartType === 'doughnut' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
             >
                Pie
             </button>
             <button 
                onClick={() => setChartType('bar')} 
                className={`px-3 py-1 text-xs font-bold uppercase tracking-widest ${chartType === 'bar' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
             >
                Bar
             </button>
             <button 
                onClick={() => setChartType('line')} 
                className={`px-3 py-1 text-xs font-bold uppercase tracking-widest ${chartType === 'line' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
             >
                Line
             </button>
          </div>
        </div>
        <div className="h-72 flex justify-center w-full">
           {Object.keys(summary.by_category).length > 0 ? (
               <>
                 {chartType === 'doughnut' && <DoughnutChart data={chartData} options={chartOptions} />}
                 {chartType === 'bar' && <BarChart data={chartData} options={{...chartOptions, plugins: { legend: { display: false } }}} />}
                 {chartType === 'line' && <LineChart data={chartData} options={{...chartOptions, plugins: { legend: { display: false } }}} />}
               </>
           ) : (
               <div className="flex flex-col items-center justify-center text-slate-400 h-full">
                  <svg className="w-12 h-12 mb-4 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="square" strokeLinejoin="miter" strokeWidth="1.5" d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2m8-10a4 4 0 100-8 4 4 0 000 8z" /></svg>
                  <p className="uppercase tracking-widest text-xs font-semibold">No Data Available</p>
               </div>
           )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
