import React, { useState } from 'react';
import HeroSection from './components/HeroSection';
import FileUpload from './components/FileUpload';
import ProcessingStatus from './components/ProcessingStatus';
import ResultsDisplay from './components/ResultsDisplay';

function App() {
  const [currentJobId, setCurrentJobId] = useState(null);
  const [processingComplete, setProcessingComplete] = useState(false);

  const handleUploadSuccess = (jobId) => {
    setCurrentJobId(jobId);
    setProcessingComplete(false);
  };

  const handleProcessingComplete = (jobId) => {
    setProcessingComplete(true);
  };

  const handleNewUpload = () => {
    setCurrentJobId(null);
    setProcessingComplete(false);
    // Scroll to upload section
    setTimeout(() => {
      document.getElementById('upload-section')?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  return (
    <div className="min-h-screen bg-industrial-50">
      {/* Hero Section - Always visible */}
      <HeroSection />

      {/* Main Content */}
      <div className="pb-16">
        {!currentJobId && !processingComplete && (
          <FileUpload onUploadSuccess={handleUploadSuccess} />
        )}

        {currentJobId && !processingComplete && (
          <ProcessingStatus 
            jobId={currentJobId} 
            onComplete={handleProcessingComplete}
          />
        )}

        {processingComplete && currentJobId && (
          <ResultsDisplay 
            jobId={currentJobId}
            onNewUpload={handleNewUpload}
          />
        )}
      </div>

      {/* Footer */}
      <footer className="bg-industrial-900 text-white py-8">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <p className="text-industrial-300">
            © 2026 Structural Drawing Analysis Platform. Powered by Truestack AI.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;

