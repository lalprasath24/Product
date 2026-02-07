import React, { useState } from 'react';
import ChatIcon from './components/ChatIcon';
import ChatWindow from './components/ChatWindow';
import FileUpload from './components/FileUpload';
import DatabaseConfig from './components/DatabaseConfig';
import './styles/widget.css';

const App = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [showUpload, setShowUpload] = useState(false);
  const [showDatabase, setShowDatabase] = useState(false);

  return (
    <>
      <ChatIcon onClick={() => setIsOpen(!isOpen)} isOpen={isOpen} />
      <ChatWindow 
        isOpen={isOpen} 
        onClose={() => setIsOpen(false)}
        onSettings={() => setShowUpload(true)}
        onDatabase={() => setShowDatabase(true)}
      />
      <FileUpload 
        isOpen={showUpload}
        onClose={() => setShowUpload(false)}
      />
      <DatabaseConfig 
        isOpen={showDatabase}
        onClose={() => setShowDatabase(false)}
      />
    </>
  );
};

export default App;