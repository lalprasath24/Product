import React, { useState, useEffect } from 'react';
import { uploadFile, getFiles, deleteFile as deleteFileApi } from '../services/chatApi';

const FileUpload = ({ isOpen, onClose }) => {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      loadFilesList();
    }
  }, [isOpen]);

  const loadFilesList = async () => {
    try {
      const filesList = await getFiles();
      setFiles(filesList);
    } catch (error) {
      console.error('Error loading files:', error);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file || file.type !== 'text/plain') return;
    
    setUploading(true);
    
    try {
      const result = await uploadFile(file);
      if (result.success) {
        loadFilesList();
      }
    } catch (error) {
      console.error('Upload error:', error);
    }
    setUploading(false);
  };

  const handleDeleteFile = async (filename) => {
    try {
      await deleteFileApi(filename);
      loadFilesList();
    } catch (error) {
      console.error('Delete error:', error);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="remo-settings-overlay">
      <div className="remo-settings-modal">
        <div className="remo-settings-header">
          <h3>Knowledge Base</h3>
          <button onClick={onClose}>×</button>
        </div>
        <div className="remo-settings-content">
          <div className="remo-upload-section">
            <label className="remo-upload-btn">
              📄 Upload Text File
              <input
                type="file"
                accept=".txt"
                onChange={handleFileUpload}
                style={{display: 'none'}}
              />
            </label>
            {uploading && <span>Uploading...</span>}
          </div>
          
          <div className="remo-files-list">
            <h4>Uploaded Files ({files.length})</h4>
            {files.length === 0 ? (
              <p>No files uploaded yet</p>
            ) : (
              files.map(file => (
                <div key={file.name} className="remo-file-item">
                  <span>{file.name}</span>
                  <small>{file.uploadDate}</small>
                  <button onClick={() => handleDeleteFile(file.name)}>🗑️</button>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;