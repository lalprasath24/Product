import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Create widget container
const createWidget = () => {
  const container = document.createElement('div');
  container.id = 'remo-widget-container';
  document.body.appendChild(container);
  
  const root = ReactDOM.createRoot(container);
  root.render(<App />);
};

// Auto-initialize if script is loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', createWidget);
} else {
  createWidget();
}

// Export for manual initialization
window.RemoWidget = { init: createWidget };