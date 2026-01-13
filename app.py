import os
import uuid
import threading
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import numpy as np
from pdf2image import convert_from_path
import cv2
from main import tile_ocr
from test_extractor import extract_tendons

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Store job status in memory (use Redis/DB for production)
jobs = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_pdf(job_id, filepath):
    """Background task to process PDF"""
    try:
        jobs[job_id]['status'] = 'processing'
        jobs[job_id]['message'] = 'Converting PDF to images...'
        
        # Convert PDF to images
        images = convert_from_path(filepath)
        total_pages = len(images)
        jobs[job_id]['total_pages'] = total_pages
        jobs[job_id]['message'] = f'Processing {total_pages} pages...'
        
        # Create job output folder
        job_output_folder = os.path.join(OUTPUT_FOLDER, job_id)
        os.makedirs(job_output_folder, exist_ok=True)
        
        results = []
        
        # Process each page
        for i, drawing in enumerate(images):
            jobs[job_id]['current_page'] = i + 1
            jobs[job_id]['message'] = f'Processing page {i + 1} of {total_pages}...'
            
            drawing = np.asarray(drawing)
            
            # Run OCR
            df_final = tile_ocr(drawing, batch_size=24, gpu=True)
            
            # Extract tendons
            vis = extract_tendons(df_final, drawing)
            
            # Save result
            output_path = os.path.join(job_output_folder, f'page_{i}.png')
            cv2.imwrite(output_path, vis)
            
            results.append({
                'page': i,
                'filename': f'page_{i}.png',
                'path': output_path
            })
        
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['message'] = 'Processing completed successfully!'
        jobs[job_id]['results'] = results
        
    except Exception as e:
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['message'] = f'Error: {str(e)}'
        print(f"Error processing job {job_id}: {str(e)}")

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload PDF file and start processing"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, f"{job_id}_{filename}")
    file.save(filepath)
    
    # Initialize job status
    jobs[job_id] = {
        'status': 'queued',
        'message': 'File uploaded, processing will start shortly...',
        'filename': filename,
        'total_pages': 0,
        'current_page': 0,
        'results': []
    }
    
    # Start background processing
    thread = threading.Thread(target=process_pdf, args=(job_id, filepath))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'job_id': job_id,
        'message': 'File uploaded successfully, processing started'
    }), 202

@app.route('/api/status/<job_id>', methods=['GET'])
def get_status(job_id):
    """Get processing status for a job"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    return jsonify({
        'job_id': job_id,
        'status': job['status'],
        'message': job['message'],
        'total_pages': job['total_pages'],
        'current_page': job['current_page'],
        'progress': (job['current_page'] / job['total_pages'] * 100) if job['total_pages'] > 0 else 0
    })

@app.route('/api/results/<job_id>', methods=['GET'])
def get_results(job_id):
    """Get results for a completed job"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    
    if job['status'] != 'completed':
        return jsonify({'error': 'Job not completed yet'}), 400
    
    return jsonify({
        'job_id': job_id,
        'status': job['status'],
        'total_pages': job['total_pages'],
        'results': job['results']
    })

@app.route('/api/download/<job_id>/<filename>', methods=['GET'])
def download_file(job_id, filename):
    """Download a specific result file"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    filepath = os.path.join(OUTPUT_FOLDER, job_id, filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(filepath, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

