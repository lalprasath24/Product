import React, { useState, useEffect } from 'react';
import Message from './Message';
import Loader from './Loader';
import { sendMessage as sendMessageAPI, getChatHistory } from '../services/chatApi';

const ChatWindow = ({ isOpen, onClose, onSettings, onDatabase }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [chatType, setChatType] = useState('rag'); // 'rag' or 'sql'

  useEffect(() => {
    if (isOpen) {
      loadChatHistory();
    }
  }, [isOpen]);

  const loadChatHistory = async () => {
    const history = await getChatHistory();
    const formattedMessages = history.map((msg, index) => ({
      id: index,
      text: msg.content,
      sender: msg.role === 'user' ? 'user' : 'bot'
    }));
    
    if (formattedMessages.length === 0) {
      formattedMessages.push({
        id: 0,
        text: "Hi! I'm Remo, your knowledge-based AI assistant. Upload documents and ask me questions about them!",
        sender: 'bot'
      });
    }
    
    setMessages(formattedMessages);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const userMessage = { id: Date.now(), text: input, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    const query = input;
    setInput('');
    setLoading(true);

    try {
      const data = await sendMessageAPI(query, chatType);
      const responseText = data.response || data.error || 'Sorry, I\'m having trouble connecting to the server.';
      
      const botMessage = { id: Date.now() + 1, text: responseText, sender: 'bot' };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const botMessage = { id: Date.now() + 1, text: 'Sorry, I\'m having trouble connecting to the server.', sender: 'bot' };
      setMessages(prev => [...prev, botMessage]);
    }
    setLoading(false);
  };

  if (!isOpen) return null;

  return (
    <div className="remo-chat-window">
      <div className="remo-chat-header">
        <span>Remo AI {chatType === 'sql' ? '(SQL)' : '(RAG)'}</span>
        <div className="remo-header-actions">
          <button 
            onClick={() => setChatType(chatType === 'rag' ? 'sql' : 'rag')}
            title={`Switch to ${chatType === 'rag' ? 'SQL' : 'RAG'} mode`}
          >
            {chatType === 'rag' ? '🗃️' : '📄'}
          </button>
          <button onClick={onSettings} className="upload-btn">📄</button>
          <button onClick={onDatabase} title="Database Config">🗄️</button>
          <button onClick={onClose}>×</button>
        </div>
      </div>
      <div className="remo-chat-messages">
        {messages.map(msg => <Message key={msg.id} message={msg} />)}
        {loading && <Loader />}
      </div>
      <div className="remo-chat-input">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatWindow;