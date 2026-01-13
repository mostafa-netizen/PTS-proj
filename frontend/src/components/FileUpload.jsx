import React, { useState, useRef } from 'react';
import axios from 'axios';

const FileUpload = ({ onUploadSuccess }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploaded, setUploaded] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const handleFileSelect = (file) => {
    setError('');
    
    // Validate file type
    if (file.type !== 'application/pdf') {
      setError('Please upload a PDF file');
      return;
    }
    
    // Validate file size (max 50MB)
    if (file.size > 50 * 1024 * 1024) {
      setError('File size must be less than 50MB');
      return;
    }
    
    setSelectedFile(file);
  };

  const handleFileInputChange = (e) => {
    if (e.target.files.length > 0) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setUploaded(false);
    setError('');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Set uploaded state to trigger green pulsing animation
      setUploaded(true);
      onUploadSuccess(response.data.job_id);
      setSelectedFile(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed. Please try again.');
      setUploaded(false);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div id="upload-section" className="max-w-4xl mx-auto px-4 py-16">
      <div className="card">
        <h2 className="text-3xl font-bold text-industrial-900 mb-6 text-center">
          Upload Your PDF Drawing
        </h2>
        
        {/* Drag and Drop Zone */}
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`border-4 border-dashed rounded-lg p-12 text-center transition-all duration-200 ${
            isDragging 
              ? 'border-industrial-500 bg-industrial-50' 
              : 'border-industrial-300 bg-gray-50'
          }`}
        >
          <div className="text-6xl mb-4">📄</div>
          <p className="text-xl text-steel-700 mb-4">
            Drag and drop your PDF file here
          </p>
          <p className="text-steel-500 mb-6">or</p>
          
          <button
            onClick={() => fileInputRef.current?.click()}
            className="btn-primary"
            disabled={uploading}
          >
            Browse Files
          </button>
          
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handleFileInputChange}
            className="hidden"
          />
          
          <p className="text-sm text-steel-500 mt-4">
            Supported format: PDF (max 50MB)
          </p>
        </div>
        
        {/* Selected File Info */}
        {selectedFile && (
          <div className="mt-6 p-4 bg-industrial-50 rounded-lg border border-industrial-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="text-3xl">📋</div>
                <div>
                  <p className="font-semibold text-steel-900">{selectedFile.name}</p>
                  <p className="text-sm text-steel-600">
                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
              
              <button
                onClick={handleUpload}
                disabled={uploading}
                className={`${
                  uploaded
                    ? 'bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 shadow-md hover:shadow-lg animate-pulse-border'
                    : 'btn-primary'
                } disabled:opacity-50 disabled:cursor-not-allowed`}
                style={uploaded ? {
                  animation: 'pulse-border 2s ease-in-out infinite',
                  border: '3px solid #10b981',
                  boxShadow: '0 0 0 0 rgba(16, 185, 129, 0.7)'
                } : {}}
              >
                {uploading ? 'Uploading...' : 'Upload & Process'}
              </button>
            </div>
          </div>
        )}
        
        {/* Error Message */}
        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-700">{error}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;

