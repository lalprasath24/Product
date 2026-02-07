import React, { useState, useEffect } from 'react';
import { configureDatabase, getDatabaseConfigs } from '../services/chatApi';

const DatabaseConfig = ({ isOpen, onClose }) => {
  const [config, setConfig] = useState({
    name: '',
    db_type: 'postgresql',
    host: 'localhost',
    port: 5432,
    database: '',
    username: '',
    password: ''
  });
  const [configs, setConfigs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    if (isOpen) {
      loadConfigs();
    }
  }, [isOpen]);

  const loadConfigs = async () => {
    const data = await getDatabaseConfigs();
    setConfigs(data);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setAnalyzing(true);
    
    try {
      const result = await configureDatabase(config);
      if (result.success) {
        alert(`Database configured! Found tables: ${result.tables.join(', ')}`);
        loadConfigs();
        setConfig({
          name: '',
          db_type: 'postgresql',
          host: 'localhost',
          port: 5432,
          database: '',
          username: '',
          password: ''
        });
      } else {
        alert(result.error || 'Configuration failed');
      }
    } catch (error) {
      alert('Configuration failed: ' + error.message);
    }
    
    setAnalyzing(false);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setConfig(prev => ({
      ...prev,
      [name]: name === 'port' ? parseInt(value) : value
    }));
  };

  if (!isOpen) return null;

  return (
    <div className="remo-settings-overlay">
      <div className="remo-settings-modal remo-db-config-modal">
        <div className="remo-settings-header">
          <h3>Database Configuration</h3>
          <button onClick={onClose}>×</button>
        </div>
        
        <div className="remo-settings-content">
          <form onSubmit={handleSubmit}>
            <div className="remo-form-group">
              <label>Configuration Name</label>
              <input
                type="text"
                name="name"
                value={config.name}
                onChange={handleChange}
                required
              />
            </div>
            
            <div className="remo-form-group">
              <label>Database Type</label>
              <select name="db_type" value={config.db_type} onChange={handleChange}>
                <option value="postgresql">PostgreSQL</option>
                <option value="mysql">MySQL</option>
                <option value="sqlite">SQLite</option>
              </select>
            </div>
            
            {config.db_type !== 'sqlite' && (
              <>
                <div className="remo-form-group">
                  <label>Host</label>
                  <input
                    type="text"
                    name="host"
                    value={config.host}
                    onChange={handleChange}
                    required
                  />
                </div>
                
                <div className="remo-form-group">
                  <label>Port</label>
                  <input
                    type="number"
                    name="port"
                    value={config.port}
                    onChange={handleChange}
                    required
                  />
                </div>
                
                <div className="remo-form-group">
                  <label>Username</label>
                  <input
                    type="text"
                    name="username"
                    value={config.username}
                    onChange={handleChange}
                    required
                  />
                </div>
                
                <div className="remo-form-group">
                  <label>Password</label>
                  <input
                    type="password"
                    name="password"
                    value={config.password}
                    onChange={handleChange}
                    required
                  />
                </div>
              </>
            )}
            
            <div className="remo-form-group">
              <label>Database Name</label>
              <input
                type="text"
                name="database"
                value={config.database}
                onChange={handleChange}
                required
              />
            </div>
            
            <div className="remo-settings-actions">
              <button type="submit" className="save-btn" disabled={analyzing}>
                {analyzing ? 'Analyzing Schema...' : 'Analyze & Save'}
              </button>
              <button type="button" className="cancel-btn" onClick={onClose}>
                Cancel
              </button>
            </div>
          </form>
          
          {configs.length > 0 && (
            <div style={{marginTop: '20px'}}>
              <h4>Configured Databases</h4>
              {configs.map(cfg => (
                <div key={cfg.id} className="remo-file-item">
                  <div>
                    <span>{cfg.name}</span>
                    <small> ({cfg.db_type} - {cfg.database})</small>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DatabaseConfig;