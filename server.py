"""
Combined server that serves both the HTML frontend and the API backend
This eliminates CORS issues by serving everything from the same origin
"""
import os
import uuid
import threading
import logging
import traceback
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import numpy as np
from pdf2image import convert_from_path
import cv2
import torch
from main import tile_ocr
from test_extractor import extract_tendons
import config

# Configure logging using config values
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Detect GPU availability
def detect_gpu():
    """Detect if GPU is available (CUDA or MPS for Apple Silicon)"""
    if not config.USE_GPU:
        logger.info("GPU disabled in config - Using CPU")
        return False

    if torch.cuda.is_available():
        logger.info("Using CUDA GPU")
        return True
    elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
        logger.info("Using MPS (Apple Silicon GPU)")
        return True
    else:
        logger.info("No GPU available - Using CPU")
        return False

GPU_AVAILABLE = detect_gpu()

app = Flask(__name__, static_folder='.')
CORS(app)

# Use configuration values
UPLOAD_FOLDER = config.UPLOAD_FOLDER
OUTPUT_FOLDER = config.SERVER_OUTPUT_FOLDER
ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Store job status in memory (use Redis/DB for production)
jobs = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_pdf(job_id, filepath):
    """Background task to process PDF"""
    try:
        logger.info(f"[Job {job_id}] ========== STARTING PDF PROCESSING ==========")
        logger.info(f"[Job {job_id}] File path: {filepath}")
        logger.info(f"[Job {job_id}] File exists: {os.path.exists(filepath)}")
        logger.info(f"[Job {job_id}] File size: {os.path.getsize(filepath)} bytes")

        jobs[job_id]['status'] = 'processing'
        jobs[job_id]['message'] = 'Converting PDF to images...'

        # Convert PDF to images using configured DPI
        logger.info(f"[Job {job_id}] STEP 1: Converting PDF to images at {config.PDF_DPI} DPI...")
        try:
            if config.PDF_DPI == 200:  # Default DPI
                images = convert_from_path(filepath)
            else:
                images = convert_from_path(filepath, dpi=config.PDF_DPI)
            total_pages = len(images)
            logger.info(f"[Job {job_id}] ✅ PDF converted successfully to {total_pages} images")
            logger.info(f"[Job {job_id}] First image type: {type(images[0])}")
            logger.info(f"[Job {job_id}] First image size: {images[0].size}")
            logger.info(f"[Job {job_id}] First image mode: {images[0].mode}")
        except Exception as pdf_error:
            logger.error(f"[Job {job_id}] ❌ PDF conversion failed: {str(pdf_error)}")
            logger.error(f"[Job {job_id}] PDF conversion traceback: {traceback.format_exc()}")
            raise

        jobs[job_id]['total_pages'] = total_pages

        results = []

        for page_num, image in enumerate(images):
            logger.info(f"[Job {job_id}] ========== PROCESSING PAGE {page_num + 1}/{total_pages} ==========")
            jobs[job_id]['current_page'] = page_num + 1

            # Calculate base progress for this page (each page gets equal share)
            page_base_progress = (page_num / total_pages) * 100
            page_progress_range = 100 / total_pages

            # Step 1: PDF to image conversion (already done, 5% of page progress)
            jobs[job_id]['message'] = f'Converting page {page_num + 1} to image...'
            jobs[job_id]['progress'] = page_base_progress + (page_progress_range * 0.05)

            # Convert PIL image to numpy array
            logger.info(f"[Job {job_id}] STEP 2: Converting PIL image to numpy array...")
            try:
                img_array = np.array(image)
                logger.info(f"[Job {job_id}] ✅ Image converted to numpy array")
                logger.info(f"[Job {job_id}] Array shape: {img_array.shape}")
                logger.info(f"[Job {job_id}] Array dtype: {img_array.dtype}")
                logger.info(f"[Job {job_id}] Array min/max values: {img_array.min()}/{img_array.max()}")
            except Exception as array_error:
                logger.error(f"[Job {job_id}] ❌ Array conversion failed: {str(array_error)}")
                logger.error(f"[Job {job_id}] Array conversion traceback: {traceback.format_exc()}")
                raise

            # Step 2: Run OCR with progress tracking (10% to 80% of page progress)
            jobs[job_id]['message'] = f'Running OCR on page {page_num + 1}...'
            jobs[job_id]['progress'] = page_base_progress + (page_progress_range * 0.10)

            logger.info(f"[Job {job_id}] STEP 3: Running OCR...")
            logger.info(f"[Job {job_id}] OCR parameters: GPU={GPU_AVAILABLE}, batch_size={config.OCR_BATCH_SIZE}")

            def ocr_progress_callback(current_batch, total_batches):
                """Update progress during OCR processing"""
                ocr_progress = (current_batch / total_batches) * 0.70  # OCR takes 70% of page progress
                jobs[job_id]['progress'] = page_base_progress + (page_progress_range * (0.10 + ocr_progress))
                jobs[job_id]['message'] = f'Running OCR on page {page_num + 1} (batch {current_batch}/{total_batches})...'
                logger.info(f"[Job {job_id}] OCR progress: {current_batch}/{total_batches} batches")

            try:
                ocr_result = tile_ocr(img_array, gpu=GPU_AVAILABLE, batch_size=config.OCR_BATCH_SIZE, progress_callback=ocr_progress_callback)
                logger.info(f"[Job {job_id}] ✅ OCR completed successfully")
                logger.info(f"[Job {job_id}] OCR result type: {type(ocr_result)}")

                # Check if it's a DataFrame
                if hasattr(ocr_result, 'shape'):
                    logger.info(f"[Job {job_id}] OCR result shape: {ocr_result.shape}")
                if hasattr(ocr_result, 'columns'):
                    logger.info(f"[Job {job_id}] OCR result columns: {list(ocr_result.columns)}")
                if hasattr(ocr_result, '__len__'):
                    logger.info(f"[Job {job_id}] OCR result length: {len(ocr_result)}")

                # Log first few rows if it's a DataFrame
                if hasattr(ocr_result, 'head'):
                    logger.info(f"[Job {job_id}] OCR result preview:\n{ocr_result.head()}")

            except Exception as ocr_error:
                logger.error(f"[Job {job_id}] ❌ OCR failed: {str(ocr_error)}")
                logger.error(f"[Job {job_id}] OCR error type: {type(ocr_error).__name__}")
                logger.error(f"[Job {job_id}] OCR traceback:\n{traceback.format_exc()}")
                raise

            # Step 3: Extract tendons and draw annotations (80% to 95% of page progress)
            jobs[job_id]['message'] = f'Extracting tendons from page {page_num + 1}...'
            jobs[job_id]['progress'] = page_base_progress + (page_progress_range * 0.80)

            # NOTE: Passing img_array directly (RGB format) to match main.py behavior
            logger.info(f"[Job {job_id}] STEP 4: Extracting tendons and drawing annotations...")
            logger.info(f"[Job {job_id}] Calling extract_tendons(ocr_result, img_array)...")
            logger.info(f"[Job {job_id}] Parameter 1 (ocr_result) type: {type(ocr_result)}")
            logger.info(f"[Job {job_id}] Parameter 2 (img_array) type: {type(img_array)}, shape: {img_array.shape}")

            try:
                output_img = extract_tendons(ocr_result, img_array)
                logger.info(f"[Job {job_id}] ✅ Tendon extraction completed successfully")
                logger.info(f"[Job {job_id}] Output image type: {type(output_img)}")
                logger.info(f"[Job {job_id}] Output image shape: {output_img.shape if hasattr(output_img, 'shape') else 'N/A'}")
            except Exception as extract_error:
                logger.error(f"[Job {job_id}] ❌ Tendon extraction failed: {str(extract_error)}")
                logger.error(f"[Job {job_id}] Error type: {type(extract_error).__name__}")
                logger.error(f"[Job {job_id}] Error message: {str(extract_error)}")
                logger.error(f"[Job {job_id}] Full traceback:\n{traceback.format_exc()}")
                raise

            # Step 4: Save output image (95% to 100% of page progress)
            jobs[job_id]['message'] = f'Saving results for page {page_num + 1}...'
            jobs[job_id]['progress'] = page_base_progress + (page_progress_range * 0.95)
            logger.info(f"[Job {job_id}] STEP 5: Saving output image...")
            output_filename = f"{job_id}_page_{page_num}.png"
            output_path = os.path.join(OUTPUT_FOLDER, job_id, output_filename)

            logger.info(f"[Job {job_id}] Output filename: {output_filename}")
            logger.info(f"[Job {job_id}] Output path: {output_path}")
            logger.info(f"[Job {job_id}] Creating output directory...")

            try:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                logger.info(f"[Job {job_id}] ✅ Output directory created/verified")
            except Exception as dir_error:
                logger.error(f"[Job {job_id}] ❌ Directory creation failed: {str(dir_error)}")
                logger.error(f"[Job {job_id}] Directory creation traceback: {traceback.format_exc()}")
                raise

            logger.info(f"[Job {job_id}] Writing image file...")
            try:
                # output_img is already in BGR format from extract_tendons
                success = cv2.imwrite(output_path, output_img)
                if success:
                    logger.info(f"[Job {job_id}] ✅ Image saved successfully")
                    logger.info(f"[Job {job_id}] Saved file size: {os.path.getsize(output_path)} bytes")
                else:
                    logger.error(f"[Job {job_id}] ❌ cv2.imwrite returned False")
                    raise Exception("cv2.imwrite failed to save image")
            except Exception as save_error:
                logger.error(f"[Job {job_id}] ❌ Save failed: {str(save_error)}")
                logger.error(f"[Job {job_id}] Save traceback: {traceback.format_exc()}")
                raise

            results.append({
                'page': page_num,
                'filename': output_filename,
                'tendon_count': 0  # extract_tendons doesn't return count, just annotated image
            })
            logger.info(f"[Job {job_id}] ✅ Page {page_num + 1} completed successfully")
            logger.info(f"[Job {job_id}] ========== PAGE {page_num + 1} COMPLETE ==========\n")

        logger.info(f"[Job {job_id}] ========== ALL PAGES PROCESSED ==========")
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['message'] = 'Processing complete!'
        jobs[job_id]['progress'] = 100
        jobs[job_id]['results'] = results
        logger.info(f"[Job {job_id}] ✅ SUCCESS: All {len(results)} pages processed successfully")
        logger.info(f"[Job {job_id}] Results: {results}")

    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['message'] = f'Error: {error_msg}'
        logger.error(f"[Job {job_id}] ========== PROCESSING FAILED ==========")
        logger.error(f"[Job {job_id}] ❌ Error type: {error_type}")
        logger.error(f"[Job {job_id}] ❌ Error message: {error_msg}")
        logger.error(f"[Job {job_id}] ❌ Full traceback:\n{traceback.format_exc()}")
        logger.error(f"[Job {job_id}] ========== END ERROR LOG ==========\n")

# Serve the main HTML page
@app.route('/')
def index():
    response = send_file('index.html')
    # Disable caching to ensure browser always gets the latest version
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# API Routes
@app.route('/api/upload', methods=['POST'])
def upload_file():
    logger.info("Upload request received")

    if 'file' not in request.files:
        logger.warning("Upload failed: No file in request")
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        logger.warning("Upload failed: Empty filename")
        return jsonify({'error': 'No file selected'}), 400

    logger.info(f"File received: {file.filename}")

    if not allowed_file(file.filename):
        logger.warning(f"Upload failed: Invalid file type - {file.filename}")
        return jsonify({'error': 'Invalid file type. Only PDF files are allowed'}), 400

    # Generate unique job ID
    job_id = str(uuid.uuid4())
    logger.info(f"Generated job ID: {job_id}")

    # Save file
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, f"{job_id}_{filename}")

    try:
        file.save(filepath)
        file_size = os.path.getsize(filepath)
        logger.info(f"File saved: {filepath} ({file_size} bytes)")
    except Exception as save_error:
        logger.error(f"Failed to save file: {str(save_error)}")
        logger.error(f"Save error traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Failed to save file'}), 500

    # Initialize job status
    jobs[job_id] = {
        'status': 'queued',
        'message': 'File uploaded, waiting to process...',
        'progress': 0,
        'total_pages': 0,
        'current_page': 0,
        'results': []
    }
    logger.info(f"Job {job_id} initialized with status: queued")

    # Start background processing
    thread = threading.Thread(target=process_pdf, args=(job_id, filepath))
    thread.daemon = True
    thread.start()
    logger.info(f"Background processing thread started for job {job_id}")

    return jsonify({
        'job_id': job_id,
        'message': 'File uploaded successfully, processing started'
    }), 202

@app.route('/api/status/<job_id>', methods=['GET'])
def get_status(job_id):
    logger.debug(f"Status check for job: {job_id}")

    if job_id not in jobs:
        logger.warning(f"Status check failed: Job {job_id} not found")
        return jsonify({'error': 'Job not found'}), 404

    status = jobs[job_id]
    logger.debug(f"Job {job_id} status: {status['status']}, progress: {status['progress']}%")
    return jsonify(status)

@app.route('/api/results/<job_id>', methods=['GET'])
def get_results(job_id):
    logger.info(f"Results requested for job: {job_id}")

    if job_id not in jobs:
        logger.warning(f"Results request failed: Job {job_id} not found")
        return jsonify({'error': 'Job not found'}), 404

    job = jobs[job_id]

    if job['status'] != 'completed':
        logger.warning(f"Results request failed: Job {job_id} status is {job['status']}, not completed")
        return jsonify({'error': 'Job not completed yet'}), 400

    logger.info(f"Returning results for job {job_id}: {len(job['results'])} pages")
    return jsonify({
        'job_id': job_id,
        'total_pages': job['total_pages'],
        'results': job['results']
    })

@app.route('/api/download/<job_id>/<filename>', methods=['GET'])
def download_file(job_id, filename):
    logger.info(f"Download requested: {job_id}/{filename}")
    filepath = os.path.join(OUTPUT_FOLDER, job_id, filename)

    if not os.path.exists(filepath):
        logger.warning(f"Download failed: File not found - {filepath}")
        return jsonify({'error': 'File not found'}), 404

    logger.info(f"Serving file: {filepath}")
    return send_file(filepath, mimetype='image/png')

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Structural Drawing Analysis Platform")
    print("=" * 60)
    print(f"✅ Server starting on http://localhost:{config.SERVER_PORT}")
    print(f"✅ API available at http://localhost:{config.SERVER_PORT}/api/*")
    print("=" * 60)
    print(f"📖 Open http://localhost:{config.SERVER_PORT} in your browser")
    print("=" * 60)
    print(f"⚙️  Configuration:")
    print(f"   - PDF DPI: {config.PDF_DPI}")
    print(f"   - OCR Batch Size: {config.OCR_BATCH_SIZE}")
    print(f"   - GPU Enabled: {config.USE_GPU}")
    print(f"   - Debug Mode: {config.DEBUG_MODE}")
    print("=" * 60)
    app.run(debug=config.DEBUG_MODE, host=config.SERVER_HOST, port=config.SERVER_PORT)

