# Quick Configuration Reference Card

## 🎯 Most Common Configurations

### Change Input PDF
```python
# Edit config.py
INPUT_PDF_PATH = '/path/to/your/document.pdf'
```

### Change Output Location
```python
# Edit config.py
OUTPUT_DIR = 'results'
OUTPUT_FILENAME_PATTERN = 'page_{i}_result.png'
```

### Disable Auto-Open Images
```python
# Edit config.py
AUTO_OPEN_RESULT = False
```

### Change Server Port
```python
# Edit config.py
SERVER_PORT = 8080
```

### Increase Image Quality
```python
# Edit config.py
PDF_DPI = 300  # Default is 200
```

### Reduce Memory Usage
```python
# Edit config.py
OCR_BATCH_SIZE = 8  # Default is 24
```

### Force CPU Usage (Disable GPU)
```python
# Edit config.py
USE_GPU = False
```

## 📋 View Current Settings

```bash
python3 config.py
```

## 🚀 Run After Configuration

```bash
# Command line processing
python3 main.py

# Web server
python3 server.py
```

## ⚙️ All Available Parameters

| Parameter | Default | What it does |
|-----------|---------|--------------|
| `PDF_DPI` | 200 | Image quality (72-600) |
| `OCR_BATCH_SIZE` | 24 | Processing speed vs memory (1-100) |
| `INPUT_PDF_PATH` | (path) | PDF file to process |
| `OUTPUT_DIR` | `data/final_output` | Where to save results |
| `OUTPUT_FILENAME_PATTERN` | `tendons-{i}.png` | Output filename format |
| `AUTO_OPEN_RESULT` | `True` | Open images after processing |
| `SERVER_HOST` | `0.0.0.0` | Server network interface |
| `SERVER_PORT` | 3000 | Server port number |
| `UPLOAD_FOLDER` | `uploads` | Temporary upload storage |
| `SERVER_OUTPUT_FOLDER` | `outputs` | Server output directory |
| `MAX_FILE_SIZE` | 50 MB | Max upload size |
| `USE_GPU` | `True` | Enable GPU acceleration |
| `LOG_FILE` | `server.log` | Log file location |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `DEBUG_MODE` | `True` | Flask debug mode |

## 🔍 Troubleshooting

### Out of Memory
```python
OCR_BATCH_SIZE = 8  # or lower
```

### Port Already in Use
```python
SERVER_PORT = 8080  # or any other port
```

### Slow Processing
```python
PDF_DPI = 150  # Lower quality, faster
OCR_BATCH_SIZE = 32  # Larger batches (if you have RAM)
```

### GPU Not Working
```python
USE_GPU = False  # Force CPU
```

## 📚 Full Documentation

- **Detailed Guide**: See `CONFIG_GUIDE.md`
- **Summary**: See `CONFIGURATION_SUMMARY.md`
- **Code**: See `config.py`

## 💡 Tips

1. **Always restart** the server after changing config
2. **Test with small PDFs** first when changing DPI or batch size
3. **Keep backups** of working configurations
4. **Use relative paths** when possible for portability
5. **Check validation errors** if config won't load

## ⚡ Quick Examples

### Example 1: High Quality Processing
```python
PDF_DPI = 300
OCR_BATCH_SIZE = 16
AUTO_OPEN_RESULT = True
```

### Example 2: Fast Processing (Low Memory)
```python
PDF_DPI = 150
OCR_BATCH_SIZE = 8
AUTO_OPEN_RESULT = False
```

### Example 3: Production Server
```python
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 80
DEBUG_MODE = False
LOG_LEVEL = 'WARNING'
```

### Example 4: Development Setup
```python
SERVER_PORT = 3000
DEBUG_MODE = True
LOG_LEVEL = 'DEBUG'
AUTO_OPEN_RESULT = True
```

