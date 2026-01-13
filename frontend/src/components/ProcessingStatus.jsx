import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ProcessingStatus = ({ jobId, onComplete }) => {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!jobId) return;

    const pollStatus = async () => {
      try {
        const response = await axios.get(`/api/status/${jobId}`);
        setStatus(response.data);

        if (response.data.status === 'completed') {
          onComplete(jobId);
        } else if (response.data.status === 'failed') {
          setError(response.data.message);
        }
      } catch (err) {
        setError('Failed to fetch status');
      }
    };

    // Poll every 2 seconds
    const interval = setInterval(pollStatus, 2000);
    pollStatus(); // Initial call

    return () => clearInterval(interval);
  }, [jobId, onComplete]);

  if (!status) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="card text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-industrial-600 mx-auto mb-4"></div>
          <p className="text-steel-700">Initializing...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="card">
          <div className="text-center">
            <div className="text-6xl mb-4">❌</div>
            <h3 className="text-2xl font-bold text-red-600 mb-2">Processing Failed</h3>
            <p className="text-steel-700">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="card">
        <h2 className="text-3xl font-bold text-industrial-900 mb-6 text-center">
          Processing Your Document
        </h2>

        {/* Status Icon */}
        <div className="text-center mb-6">
          {status.status === 'completed' ? (
            <div className="text-6xl mb-4">✅</div>
          ) : (
            <div className="animate-spin rounded-full h-20 w-20 border-b-4 border-industrial-600 mx-auto mb-4"></div>
          )}
        </div>

        {/* Progress Bar */}
        <div className="mb-6">
          <div className="flex justify-between text-sm text-steel-600 mb-2">
            <span>{status.message}</span>
            <span>{Math.round(status.progress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
            <div
              className="bg-gradient-to-r from-industrial-500 to-industrial-600 h-4 rounded-full transition-all duration-500 ease-out"
              style={{ width: `${status.progress}%` }}
            ></div>
          </div>
        </div>

        {/* Page Progress */}
        {status.total_pages > 0 && (
          <div className="text-center">
            <p className="text-lg text-steel-700">
              Processing page <span className="font-bold text-industrial-700">{status.current_page}</span> of{' '}
              <span className="font-bold text-industrial-700">{status.total_pages}</span>
            </p>
          </div>
        )}

        {/* Processing Steps */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className={`p-4 rounded-lg border-2 ${
            status.status !== 'queued' ? 'border-green-500 bg-green-50' : 'border-gray-300 bg-gray-50'
          }`}>
            <div className="text-2xl mb-2">📤</div>
            <p className="font-semibold text-steel-900">Upload</p>
            <p className="text-sm text-steel-600">File received</p>
          </div>

          <div className={`p-4 rounded-lg border-2 ${
            status.status === 'processing' || status.status === 'completed' 
              ? 'border-green-500 bg-green-50' 
              : 'border-gray-300 bg-gray-50'
          }`}>
            <div className="text-2xl mb-2">🔍</div>
            <p className="font-semibold text-steel-900">Analysis</p>
            <p className="text-sm text-steel-600">OCR & Detection</p>
          </div>

          <div className={`p-4 rounded-lg border-2 ${
            status.status === 'completed' 
              ? 'border-green-500 bg-green-50' 
              : 'border-gray-300 bg-gray-50'
          }`}>
            <div className="text-2xl mb-2">✨</div>
            <p className="font-semibold text-steel-900">Complete</p>
            <p className="text-sm text-steel-600">Results ready</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProcessingStatus;

