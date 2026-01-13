# 🚀 Running Instructions

## ✅ Currently Running

Your application is now running with:

### Combined Server (Flask + HTML)
- **URL**: http://localhost:3000
- **Status**: ✅ Running
- **File**: `server.py` (serves both frontend and API)
- **No CORS issues!** Everything runs on the same port

---

## 🌐 Access the Application

**Open in your browser:** http://localhost:3000

---

## 🛑 Stop the Server

```bash
# Find and kill the process
pkill -f "python3 server.py"

# Or use:
lsof -ti:3000 | xargs kill -9
```

---

## 🔄 Start/Restart the Server

### One Command - Everything!
```bash
python3 server.py
```

This will:
- ✅ Serve the HTML frontend at http://localhost:3000
- ✅ Provide API endpoints at http://localhost:3000/api/*
- ✅ Handle file uploads and processing
- ✅ No CORS issues (same origin)

---

## 📝 Important Notes

### Simplified Architecture
- **Everything runs on port 3000** - No more CORS issues!
- **One server** (`server.py`) handles both frontend and API
- **No Node.js required** - Pure Python + HTML

### No Node.js Required!
- The frontend is a **standalone HTML file** (`index.html`)
- Uses **Tailwind CSS CDN** (no build step needed)
- Pure JavaScript (no React build required)
- Works directly in any browser

### File Structure
```
project-latest-update/
├── server.py           # ⭐ Combined server (frontend + API on port 3000)
├── index.html          # Standalone frontend HTML
├── app.py              # Old backend (not used anymore)
├── main.py             # Your existing OCR processing
├── test_extractor.py   # Tendon extraction
├── ocr/                # OCR modules
├── uploads/            # Uploaded PDFs (auto-created)
└── outputs/            # Processed results (auto-created)
```

---

## 🧪 Testing the Application

1. **Open**: http://localhost:3000
2. **Upload**: Drag & drop a PDF or click "Browse Files"
3. **Process**: Click "Upload & Process"
4. **Wait**: Watch real-time progress
5. **Download**: View and download annotated results

---

## 🔧 Troubleshooting

### Server not responding
```bash
# Check if server is running
curl http://localhost:3000

# Check what's using port 3000
lsof -i :3000

# Restart server
pkill -f "python3 server.py"
python3 server.py
```

### Port already in use
```bash
# Find what's using the port
lsof -i :3000

# Kill the process
lsof -ti:3000 | xargs kill -9

# Then restart
python3 server.py
```

### Upload fails
- Check browser console (F12) for errors
- Make sure `uploads/` folder exists and is writable
- Verify file is a valid PDF under 50MB
- Check server terminal for error messages

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `http://localhost:3000/` | GET | Main HTML page |
| `http://localhost:3000/api/upload` | POST | Upload PDF |
| `http://localhost:3000/api/status/:id` | GET | Check status |
| `http://localhost:3000/api/results/:id` | GET | Get results |
| `http://localhost:3000/api/download/:id/:file` | GET | Download image |

---

## 🎨 Features Working

✅ Hero section with industrial design  
✅ Drag-and-drop PDF upload  
✅ File validation (PDF only, max 50MB)  
✅ Real-time processing status  
✅ Progress bar with percentage  
✅ Results gallery with thumbnails  
✅ Individual and batch download  
✅ Full-screen image preview  
✅ Responsive design  
✅ Error handling  

---

## 💡 Quick Commands

```bash
# Start server (ONE COMMAND!)
python3 server.py

# Stop server
pkill -f "python3 server.py"

# Force kill if needed
lsof -ti:3000 | xargs kill -9

# Check what's running
ps aux | grep server.py
lsof -i :3000

# Test API
curl http://localhost:3000
curl -X POST -F "file=@data/plan.pdf" http://localhost:3000/api/upload
```

---

## 🎯 Next Steps

1. **Test with a PDF**: Upload a structural drawing
2. **Check results**: Verify tendon detection works
3. **Optimize**: Adjust batch_size in `app.py` if needed
4. **Deploy**: Consider using gunicorn for production

---

**Your application is ready to use!** 🎉

Open http://localhost:3000 and start analyzing structural drawings!

