import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ResultsDisplay = ({ jobId, onNewUpload }) => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const response = await axios.get(`/api/results/${jobId}`);
        setResults(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load results');
        setLoading(false);
      }
    };

    if (jobId) {
      fetchResults();
    }
  }, [jobId]);

  const downloadImage = (filename) => {
    window.open(`/api/download/${jobId}/${filename}`, '_blank');
  };

  const downloadAll = () => {
    results.results.forEach((result) => {
      setTimeout(() => downloadImage(result.filename), 100);
    });
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="card text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-industrial-600 mx-auto mb-4"></div>
          <p className="text-steel-700">Loading results...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="card text-center">
          <div className="text-6xl mb-4">❌</div>
          <p className="text-red-600 text-xl">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="card">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h2 className="text-3xl font-bold text-industrial-900 mb-2">
              Analysis Complete
            </h2>
            <p className="text-steel-600">
              Successfully processed {results.total_pages} page{results.total_pages !== 1 ? 's' : ''}
            </p>
          </div>
          
          <div className="flex gap-3">
            <button
              onClick={downloadAll}
              className="btn-secondary"
            >
              📥 Download All
            </button>
            <button
              onClick={onNewUpload}
              className="btn-primary"
            >
              ➕ New Upload
            </button>
          </div>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-gradient-to-br from-industrial-50 to-industrial-100 p-6 rounded-lg border border-industrial-200">
            <div className="text-3xl mb-2">📄</div>
            <p className="text-2xl font-bold text-industrial-900">{results.total_pages}</p>
            <p className="text-steel-600">Pages Processed</p>
          </div>
          
          <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-lg border border-green-200">
            <div className="text-3xl mb-2">✅</div>
            <p className="text-2xl font-bold text-green-900">{results.results.length}</p>
            <p className="text-steel-600">Results Generated</p>
          </div>
          
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-lg border border-blue-200">
            <div className="text-3xl mb-2">🎯</div>
            <p className="text-2xl font-bold text-blue-900">100%</p>
            <p className="text-steel-600">Success Rate</p>
          </div>
        </div>

        {/* Results Grid */}
        <div>
          <h3 className="text-2xl font-bold text-industrial-900 mb-4">
            Annotated Drawings
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {results.results.map((result, index) => (
              <div
                key={index}
                className="bg-gray-50 rounded-lg border-2 border-industrial-200 overflow-hidden hover:border-industrial-500 transition-all duration-200 cursor-pointer group"
                onClick={() => setSelectedImage(result)}
              >
                <div className="aspect-video bg-gradient-to-br from-industrial-100 to-steel-100 flex items-center justify-center relative overflow-hidden">
                  <img
                    src={`/api/download/${jobId}/${result.filename}`}
                    alt={`Page ${result.page + 1}`}
                    className="w-full h-full object-contain group-hover:scale-105 transition-transform duration-200"
                  />
                  <div className="absolute inset-0 bg-black opacity-0 group-hover:opacity-10 transition-opacity duration-200"></div>
                </div>
                
                <div className="p-4">
                  <p className="font-semibold text-steel-900 mb-2">
                    Page {result.page + 1}
                  </p>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      downloadImage(result.filename);
                    }}
                    className="w-full bg-industrial-600 hover:bg-industrial-700 text-white py-2 px-4 rounded transition-colors duration-200"
                  >
                    Download
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Image Modal */}
      {selectedImage && (
        <div
          className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4"
          onClick={() => setSelectedImage(null)}
        >
          <div className="max-w-6xl max-h-full overflow-auto">
            <img
              src={`/api/download/${jobId}/${selectedImage.filename}`}
              alt={`Page ${selectedImage.page + 1}`}
              className="w-full h-auto"
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;

