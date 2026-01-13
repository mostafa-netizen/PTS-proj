# Configuration Guide

This guide explains how to configure the Structural Drawing Analysis Platform using `config.py`.

## 📋 Overview

All configurable parameters are centralized in `config.py`. You can modify these values to customize the behavior of both the command-line tool (`main.py`) and the web server (`server.py`) without changing the code.

## ⚙️ Configuration Parameters

### PDF Processing Configuration

#### `PDF_DPI`
- **Type**: Integer
- **Default**: `200`
- **Range**: 72 - 600
- **Description**: DPI (dots per inch) for PDF to image conversion
- **Impact**: 
  - Higher values = better quality but slower processing and larger files
  - Lower values = faster processing but lower quality
- **Example**:
  ```python
  PDF_DPI = 300  # Higher quality
  PDF_DPI = 150  # Faster processing
  ```

#### `OCR_BATCH_SIZE`
- **Type**: Integer
- **Default**: `24`
- **Range**: 1 - 100
- **Description**: Number of image tiles to process at once during OCR
- **Impact**:
  - Higher values = faster processing but more memory usage
  - Lower values = slower but uses less memory
- **Example**:
  ```python
  OCR_BATCH_SIZE = 32  # If you have more RAM
  OCR_BATCH_SIZE = 16  # If you have limited RAM
  ```

### Main.py Configuration (Command Line)

#### `INPUT_PDF_PATH`
- **Type**: String
- **Default**: `'/Users/mostafaazab/Desktop/Work/Truestack AI/Rick Thompson/Plan Samples/plan.pdf'`
- **Description**: Path to the PDF file to process when running `main.py`
- **Example**:
  ```python
  # Absolute path
  INPUT_PDF_PATH = '/path/to/your/document.pdf'
  
  # Relative path (from project root)
  INPUT_PDF_PATH = 'data/plan.pdf'
  ```

#### `OUTPUT_DIR`
- **Type**: String
- **Default**: `'data/final_output'`
- **Description**: Directory where processed images will be saved
- **Example**:
  ```python
  OUTPUT_DIR = 'results'
  OUTPUT_DIR = '/absolute/path/to/output'
  ```

#### `OUTPUT_FILENAME_PATTERN`
- **Type**: String
- **Default**: `'tendons-{i}.png'`
- **Description**: Filename pattern for output images. `{i}` is replaced with page number
- **Example**:
  ```python
  OUTPUT_FILENAME_PATTERN = 'page_{i}_result.png'
  OUTPUT_FILENAME_PATTERN = 'analysis-{i}.png'
  ```

#### `AUTO_OPEN_RESULT`
- **Type**: Boolean
- **Default**: `True`
- **Description**: Whether to automatically open result images after processing
- **Example**:
  ```python
  AUTO_OPEN_RESULT = True   # Open images automatically
  AUTO_OPEN_RESULT = False  # Don't open images
  ```

### Server Configuration

#### `SERVER_HOST`
- **Type**: String
- **Default**: `'0.0.0.0'`
- **Description**: Server host address. `0.0.0.0` means accessible from any network interface
- **Example**:
  ```python
  SERVER_HOST = '0.0.0.0'     # Accessible from network
  SERVER_HOST = '127.0.0.1'   # Only accessible locally
  ```

#### `SERVER_PORT`
- **Type**: Integer
- **Default**: `3000`
- **Range**: 1024 - 65535
- **Description**: Port number for the web server
- **Example**:
  ```python
  SERVER_PORT = 3000
  SERVER_PORT = 8080
  ```

#### `UPLOAD_FOLDER`
- **Type**: String
- **Default**: `'uploads'`
- **Description**: Directory for temporary PDF storage during upload

#### `SERVER_OUTPUT_FOLDER`
- **Type**: String
- **Default**: `'outputs'`
- **Description**: Directory for processed results from web uploads

#### `MAX_FILE_SIZE`
- **Type**: Integer (bytes)
- **Default**: `52428800` (50 MB)
- **Description**: Maximum file size for PDF uploads
- **Example**:
  ```python
  MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
  ```

### GPU Configuration

#### `USE_GPU`
- **Type**: Boolean
- **Default**: `True`
- **Description**: Enable GPU acceleration if available
- **Example**:
  ```python
  USE_GPU = True   # Use GPU if available
  USE_GPU = False  # Force CPU usage
  ```

### Logging Configuration

#### `LOG_FILE`
- **Type**: String
- **Default**: `'server.log'`
- **Description**: Path to the log file

#### `LOG_LEVEL`
- **Type**: String
- **Default**: `'INFO'`
- **Options**: `'DEBUG'`, `'INFO'`, `'WARNING'`, `'ERROR'`, `'CRITICAL'`
- **Description**: Logging level for the application

#### `DEBUG_MODE`
- **Type**: Boolean
- **Default**: `True`
- **Description**: Enable Flask debug mode (auto-reload on code changes)

## 🚀 Usage Examples

### Example 1: Process a Different PDF

Edit `config.py`:
```python
INPUT_PDF_PATH = 'data/my_drawing.pdf'
OUTPUT_DIR = 'results/my_drawing'
```

Then run:
```bash
python3 main.py
```

### Example 2: Increase Quality

Edit `config.py`:
```python
PDF_DPI = 300  # Higher quality
```

### Example 3: Optimize for Low Memory

Edit `config.py`:
```python
OCR_BATCH_SIZE = 8  # Smaller batches
```

### Example 4: Change Server Port

Edit `config.py`:
```python
SERVER_PORT = 8080
```

Then run:
```bash
python3 server.py
```

Access at: http://localhost:8080

## 🔍 Viewing Current Configuration

Run this command to see your current configuration:
```bash
python3 config.py
```

## ⚠️ Important Notes

1. **Validation**: The configuration is automatically validated when imported. Invalid values will raise an error.

2. **Server Restart**: After changing configuration, restart the server for changes to take effect.

3. **Path Formats**: Use forward slashes (`/`) in paths, even on Windows. Python handles this correctly.

4. **Memory Usage**: If you encounter memory errors, reduce `OCR_BATCH_SIZE`.

5. **Performance**: Higher `PDF_DPI` and `OCR_BATCH_SIZE` improve quality and speed but require more resources.

## 🐛 Troubleshooting

### "Configuration errors" on startup
- Check that all values are within valid ranges
- Ensure paths use proper format
- Verify boolean values are `True` or `False` (capitalized)

### Out of memory errors
- Reduce `OCR_BATCH_SIZE`
- Reduce `PDF_DPI`
- Set `USE_GPU = False` if GPU memory is limited

### Server won't start
- Check if `SERVER_PORT` is already in use
- Try a different port number
- Ensure port is between 1024 and 65535

