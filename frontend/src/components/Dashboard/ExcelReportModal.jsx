import React, { useState } from 'react';
import './ExcelReportModal.css';

const ExcelReportModal = ({ isOpen, onClose }) => {
  const [selectedReport, setSelectedReport] = useState('');
  const [dateRange, setDateRange] = useState({ from: '', to: '' });

  const reportTypes = [
    { id: 'customers', name: 'Customer Report', description: 'Export all customer data' },
    { id: 'products', name: 'Product Report', description: 'Export product inventory and details' },
    { id: 'deliveryarea', name: 'Delivery Area Report', description: 'Export delivery zones and coverage' },
    { id: 'orders', name: 'Orders Report', description: 'Export order history and status' },
    { id: 'revenue', name: 'Revenue Report', description: 'Export sales and revenue data' }
  ];

  const handleGenerate = () => {
    if (!selectedReport) {
      alert('Please select a report type');
      return;
    }
    
    if (selectedReport === 'customers') {
      const url = 'http://127.0.0.1:8000/v1/delivery_area_based_customers?excel=true';
      window.open(url, '_blank');
    } else {
      // TODO: Add other report APIs
      alert(`${reportTypes.find(r => r.id === selectedReport)?.name} API not implemented yet`);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>📊 Excel Report Generation</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>
        
        <div className="modal-body">
          <div className="section">
            <h3>Select Report Type</h3>
            <div className="report-grid">
              {reportTypes.map(report => (
                <div 
                  key={report.id}
                  className={`report-card ${selectedReport === report.id ? 'selected' : ''}`}
                  onClick={() => setSelectedReport(report.id)}
                >
                  <h4>{report.name}</h4>
                  <p>{report.description}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="section">
            <h3>Date Range (Optional)</h3>
            <div className="date-inputs">
              <input 
                type="date" 
                value={dateRange.from}
                onChange={e => setDateRange({...dateRange, from: e.target.value})}
                placeholder="From Date"
              />
              <input 
                type="date" 
                value={dateRange.to}
                onChange={e => setDateRange({...dateRange, to: e.target.value})}
                placeholder="To Date"
              />
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <button className="cancel-btn" onClick={onClose}>Cancel</button>
          <button className="generate-btn" onClick={handleGenerate}>
            📥 Generate Excel Report
          </button>
        </div>
      </div>
    </div>
  );
};

export default ExcelReportModal;