import React from 'react';

const Message = ({ message }) => (
  <div className={`remo-message ${message.sender}`}>
    <div className="remo-message-content">
      {message.text}
    </div>
  </div>
);

export default Message;