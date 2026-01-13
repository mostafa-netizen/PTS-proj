# 📊 Logging Guide

## Overview

Comprehensive logging has been added to `server.py` to help debug errors and track processing progress.

---

## Log Files

### 1. **server.log** (File)
- Location: `./server.log`
- Contains: All log messages from the server
- Persistent across server restarts

### 2. **Console Output** (Terminal)
- Real-time log messages displayed in terminal
- Same content as `server.log`

---

## Log Levels

The logging system uses standard Python logging levels:

- **INFO**: Normal operations (uploads, processing steps, completions)
- **WARNING**: Non-critical issues (job not found, invalid requests)
- **ERROR**: Errors with full stack traces
- **DEBUG**: Detailed debugging information (disabled by default)

---

## What Gets Logged

### Upload Process
```
✅ Upload request received
✅ File received: filename.pdf
✅ Generated job ID: uuid
✅ File saved: path (size bytes)
✅ Job initialized with status: queued
✅ Background processing thread started
```

### PDF Processing
```
✅ [Job uuid] Starting PDF processing: filepath
✅ [Job uuid] Converting PDF to images at 300 DPI...
✅ [Job uuid] PDF converted to N images
✅ [Job uuid] Processing page 1/N
✅ [Job uuid] Image shape: (height, width, channels), dtype: uint8
✅ [Job uuid] Running OCR with GPU=True, batch_size=4
✅ [Job uuid] OCR completed. Result type: DataFrame, shape: (rows, cols)
✅ [Job uuid] Extracting tendons and drawing annotations...
✅ [Job uuid] Tendon extraction and annotation completed
✅ [Job uuid] Saving output to: path
✅ [Job uuid] Image saved successfully
✅ [Job uuid] Page 1 completed successfully
✅ [Job uuid] All pages processed successfully. Total results: N
```

### Errors
```
❌ [Job uuid] OCR failed: error message
❌ [Job uuid] OCR traceback: full stack trace
❌ [Job uuid] Tendon extraction failed: error message
❌ [Job uuid] Extraction traceback: full stack trace
❌ [Job uuid] Processing failed with error: error message
❌ [Job uuid] Full traceback: complete error details
```

---

## How to View Logs

### Real-Time (Terminal)
Watch logs as they happen in the terminal where you ran `python3 server.py`

### Log File
```bash
# View entire log
cat server.log

# Follow log in real-time
tail -f server.log

# View last 50 lines
tail -n 50 server.log

# Search for errors
grep "ERROR" server.log

# Search for specific job
grep "Job uuid" server.log
```

---

## Common Error Patterns

### 1. "list index out of range"
**Cause**: Trying to access an empty list or array
**Location**: Usually in `extract_tendons()` or OCR processing
**Check logs for**:
- OCR result shape
- Tendon extraction details
- Full traceback

### 2. "not enough values to unpack (expected 2, got 0)"
**Cause**: Function expecting multiple return values but got none
**Location**: Usually in template matching or line detection
**Check logs for**:
- Image processing steps
- Template matching results

### 3. "tile_ocr() missing 1 required positional argument: 'gpu'"
**Cause**: Missing GPU parameter
**Status**: ✅ FIXED - GPU detection added

---

## Debugging Workflow

### Step 1: Upload a PDF
Upload through the web interface at http://localhost:3000

### Step 2: Note the Job ID
Check the browser console or server logs for the job ID (UUID)

### Step 3: Monitor Logs
```bash
# In a separate terminal
tail -f server.log | grep "Job YOUR_JOB_ID"
```

### Step 4: Check for Errors
```bash
# Find errors for your job
grep -A 10 "Job YOUR_JOB_ID.*ERROR" server.log
```

### Step 5: Analyze Stack Trace
Look for the full traceback in the logs to identify the exact line causing the error

---

## Log Analysis Examples

### Example 1: Successful Processing
```
2026-01-10 22:45:00 - INFO - Upload request received
2026-01-10 22:45:00 - INFO - File received: plan.pdf
2026-01-10 22:45:00 - INFO - Generated job ID: abc-123
2026-01-10 22:45:00 - INFO - File saved: uploads/abc-123_plan.pdf (1048576 bytes)
2026-01-10 22:45:00 - INFO - [Job abc-123] Starting PDF processing
2026-01-10 22:45:01 - INFO - [Job abc-123] PDF converted to 5 images
2026-01-10 22:45:01 - INFO - [Job abc-123] Processing page 1/5
2026-01-10 22:45:05 - INFO - [Job abc-123] OCR completed
2026-01-10 22:45:06 - INFO - [Job abc-123] Page 1 completed successfully
...
2026-01-10 22:46:00 - INFO - [Job abc-123] All pages processed successfully
```

### Example 2: Error During Processing
```
2026-01-10 22:45:00 - INFO - [Job abc-123] Processing page 1/5
2026-01-10 22:45:05 - INFO - [Job abc-123] Running OCR with GPU=True
2026-01-10 22:45:10 - ERROR - [Job abc-123] Tendon extraction failed: list index out of range
2026-01-10 22:45:10 - ERROR - [Job abc-123] Extraction traceback:
Traceback (most recent call last):
  File "server.py", line 105, in process_pdf
    output_img = extract_tendons(ocr_result, img_bgr)
  File "test_extractor.py", line 86, in extract_tendons
    found = detect_line_ending_in_bbox(final_lines, bbox)
  File "ocr/line_detector.py", line 123, in detect_line_ending_in_bbox
    line = lines[0]
IndexError: list index out of range
```

---

## Tips

1. **Keep logs organized**: Archive old `server.log` files periodically
2. **Use grep**: Search logs efficiently with grep patterns
3. **Check timestamps**: Correlate errors with user actions
4. **Save error logs**: Copy error sections for debugging
5. **Monitor in real-time**: Use `tail -f` during testing

---

## Next Steps

When you encounter an error:

1. ✅ Check `server.log` for the full error message
2. ✅ Find the job ID from the browser or logs
3. ✅ Search for that job ID in the logs
4. ✅ Look for ERROR messages with stack traces
5. ✅ Share the relevant log section for debugging

---

**All logging is now active! Upload a PDF and check `server.log` for detailed information.** 📊

