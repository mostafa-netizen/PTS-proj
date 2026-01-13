#!/usr/bin/env python3
"""
Manual test script to process plan.pdf without the frontend
This will help verify the backend processing is working correctly
"""

import os
import sys
import uuid
from pdf2image import convert_from_path
import cv2
import numpy as np
import torch
from main import tile_ocr
from test_extractor import extract_tendons

# Detect GPU availability
def detect_gpu():
    """Detect if GPU is available (CUDA or MPS for Apple Silicon)"""
    if torch.cuda.is_available():
        print("🎮 Using CUDA GPU")
        return True
    elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
        print("🎮 Using MPS (Apple Silicon GPU)")
        return True
    else:
        print("💻 Using CPU")
        return False

def process_pdf_manual(pdf_path):
    """Process a PDF file manually without the web interface"""

    print("=" * 60)
    print("🚀 MANUAL PDF PROCESSING TEST")
    print("=" * 60)

    # Detect GPU
    gpu_available = detect_gpu()
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File not found: {pdf_path}")
        return False
    
    print(f"📄 Input PDF: {pdf_path}")
    print(f"📊 File size: {os.path.getsize(pdf_path) / 1024 / 1024:.2f} MB")
    
    # Generate job ID
    job_id = str(uuid.uuid4())
    print(f"🆔 Job ID: {job_id}")
    
    # Create output directory
    output_dir = f'outputs/{job_id}'
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Output directory: {output_dir}")
    
    try:
        # Step 1: Convert PDF to images
        print("\n" + "=" * 60)
        print("STEP 1: Converting PDF to images...")
        print("=" * 60)
        
        images = convert_from_path(pdf_path, dpi=300)
        print(f"✅ Converted {len(images)} page(s)")
        
        results = []
        
        # Step 2: Process each page
        for page_num, image in enumerate(images):
            print("\n" + "-" * 60)
            print(f"STEP 2: Processing Page {page_num + 1}/{len(images)}")
            print("-" * 60)
            
            # Convert PIL image to numpy array
            img_array = np.array(image)
            
            # Convert RGB to BGR for OpenCV
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            print(f"📐 Image size: {img_array.shape[1]}x{img_array.shape[0]} pixels")
            
            # Step 2a: OCR
            print("\n🔍 Running OCR (tile_ocr)...")
            ocr_results = tile_ocr(img_array, gpu=gpu_available)
            print(f"✅ OCR complete: Found {len(ocr_results)} text regions")
            
            # Step 2b: Extract tendons
            print("\n🎯 Extracting tendons (extract_tendons)...")
            # Note: extract_tendons expects (words, image) not (image, words)
            annotated_image = extract_tendons(ocr_results, img_array)
            print(f"✅ Tendon extraction complete")
            
            # Step 2c: Save result
            output_filename = f'{job_id}_page_{page_num}.png'
            output_path = os.path.join(output_dir, output_filename)
            
            print(f"\n💾 Saving annotated image...")
            cv2.imwrite(output_path, annotated_image)
            print(f"✅ Saved: {output_path}")
            
            # Verify file was saved
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / 1024
                print(f"📊 Output file size: {file_size:.2f} KB")
            else:
                print(f"❌ Warning: Output file not found!")
            
            results.append({
                'page': page_num,
                'filename': output_filename,
                'path': output_path
            })
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ PROCESSING COMPLETE!")
        print("=" * 60)
        print(f"📄 Total pages processed: {len(results)}")
        print(f"📁 Output directory: {output_dir}")
        print(f"\n📋 Results:")
        for result in results:
            print(f"  - Page {result['page'] + 1}: {result['filename']}")
        
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! All pages processed successfully.")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERROR OCCURRED!")
        print("=" * 60)
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        
        import traceback
        print("\nFull traceback:")
        print(traceback.format_exc())
        
        return False

if __name__ == '__main__':
    # Default to plan.pdf in data directory
    pdf_path = 'data/plan.pdf'
    
    # Allow custom path from command line
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    
    print("\n")
    success = process_pdf_manual(pdf_path)
    
    if success:
        print("\n✅ Test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Test failed!")
        sys.exit(1)

