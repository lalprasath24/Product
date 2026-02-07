import React from 'react';

const ChatIcon = ({ onClick, isOpen }) => (
  <div 
    className={`remo-chat-icon ${isOpen ? 'open' : ''}`}
    onClick={onClick}
  >
    🤖
  </div>
);

export default ChatIcon;