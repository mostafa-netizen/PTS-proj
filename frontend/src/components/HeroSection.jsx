import React from 'react';

const HeroSection = () => {
  const scrollToUpload = () => {
    document.getElementById('upload-section')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="bg-gradient-to-br from-industrial-900 via-industrial-800 to-steel-900 text-white py-20 px-4">
      <div className="max-w-6xl mx-auto text-center">
        {/* Main Title */}
        <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
          Structural Drawing Analysis Platform
        </h1>
        
        {/* Subtitle */}
        <p className="text-xl md:text-2xl text-industrial-200 mb-8 max-w-3xl mx-auto">
          AI-Powered Tendon Detection and Analysis for Construction Plans
        </p>
        
        {/* Description */}
        <p className="text-lg text-industrial-300 mb-10 max-w-2xl mx-auto">
          Upload your PDF structural drawings and let our advanced computer vision system 
          automatically detect and analyze tendons with precision and speed.
        </p>
        
        {/* CTA Button */}
        <button 
          onClick={scrollToUpload}
          className="bg-industrial-500 hover:bg-industrial-600 text-white font-bold py-4 px-10 rounded-lg text-lg transition-all duration-300 shadow-xl hover:shadow-2xl transform hover:-translate-y-1"
        >
          Get Started
        </button>
        
        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
            <div className="text-4xl mb-4">🔍</div>
            <h3 className="text-xl font-semibold mb-2">Advanced OCR</h3>
            <p className="text-industrial-200">
              State-of-the-art optical character recognition for accurate text extraction
            </p>
          </div>
          
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
            <div className="text-4xl mb-4">⚡</div>
            <h3 className="text-xl font-semibold mb-2">Fast Processing</h3>
            <p className="text-industrial-200">
              GPU-accelerated analysis for rapid results on multi-page documents
            </p>
          </div>
          
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-semibold mb-2">Detailed Results</h3>
            <p className="text-industrial-200">
              Comprehensive tendon detection with visual annotations and data export
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;

