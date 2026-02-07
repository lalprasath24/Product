const API_BASE_URL = 'http://localhost:8000/api';

let sessionId = localStorage.getItem('remo_session_id');
if (!sessionId) {
  sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  localStorage.setItem('remo_session_id', sessionId);
}

export const configureDatabase = async (config) => {
  try {
    const response = await fetch(`${API_BASE_URL}/database/config`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config)
    });
    return await response.json();
  } catch (error) {
    console.error('Database config error:', error);
    return { error: 'Failed to configure database' };
  }
};

export const getDatabaseConfigs = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/database/configs`);
    return await response.json();
  } catch (error) {
    console.error('Get database configs error:', error);
    return [];
  }
};

export const sendMessage = async (message, chatType = 'rag') => {
  console.log('Sending message:', message);
  console.log('API URL:', `${API_BASE_URL}/chat`);
  
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, session_id: sessionId, chat_type: chatType })
    });
    
    console.log('Response status:', response.status);
    const data = await response.json();
    console.log('Response data:', data);
    
    return data;
  } catch (error) {
    console.error('Chat API error:', error);
    return { error: 'Failed to send message' };
  }
};

export const getChatHistory = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/history/${sessionId}`);
    const data = await response.json();
    return data.history || [];
  } catch (error) {
    console.error('Get history error:', error);
    return [];
  }
};

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData
    });
    return await response.json();
  } catch (error) {
    console.error('Upload error:', error);
    return { error: 'Failed to upload file' };
  }
};

export const getFiles = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/files`);
    return await response.json();
  } catch (error) {
    console.error('Get files error:', error);
    return [];
  }
};

export const deleteFile = async (filename) => {
  try {
    const response = await fetch(`${API_BASE_URL}/files/${filename}`, {
      method: 'DELETE'
    });
    return await response.json();
  } catch (error) {
    console.error('Delete file error:', error);
    return { error: 'Failed to delete file' };
  }
};