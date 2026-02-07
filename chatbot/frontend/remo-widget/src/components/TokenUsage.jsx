import React, { useState, useEffect } from 'react';
import { getTokenUsage } from '../services/chatApi';

const TokenUsage = ({ isVisible }) => {
  const [usage, setUsage] = useState({ today: { total: 0 }, monthly: { total: 0 } });
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    if (isVisible) {
      loadUsage();
      const interval = setInterval(loadUsage, 30000); // Update every 30 seconds
      return () => clearInterval(interval);
    }
  }, [isVisible]);

  const loadUsage = async () => {
    const data = await getTokenUsage();
    setUsage(data);
  };

  if (!isVisible) return null;

  return (
    <div className="token-usage">
      <div 
        className="token-icon" 
        onClick={() => setShowDetails(!showDetails)}
        title="Token Usage"
      >
        📊
      </div>
      
      {showDetails && (
        <div className="token-details">
          <div className="usage-item">
            <span>Today:</span>
            <span>{usage.today.total.toLocaleString()}</span>
          </div>
          <div className="usage-item">
            <span>Monthly:</span>
            <span>{usage.monthly.total.toLocaleString()}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default TokenUsage;