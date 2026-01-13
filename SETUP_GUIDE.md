# Quick Setup Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Prerequisites

#### macOS
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js
brew install node

# Install poppler (for PDF processing)
brew install poppler
```

#### Ubuntu/Debian
```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install poppler
sudo apt-get install poppler-utils
```

### Step 2: Install Dependencies

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Step 3: Run the Application

#### Option A: Use the startup script (Recommended)
```bash
./start.sh
```

#### Option B: Run servers manually

**Terminal 1 - Backend:**
```bash
python3 app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## 🌐 Access the Application

Once both servers are running:
- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:5000

## 📝 Usage

1. Open http://localhost:3000 in your browser
2. Upload a PDF structural drawing
3. Wait for processing (real-time progress shown)
4. View and download annotated results

## ⚙️ Configuration

### GPU Settings
The system automatically detects GPU. To force CPU mode, edit `app.py`:
```python
df_final = tile_ocr(drawing, batch_size=24, gpu=False)  # Change to False
```

### File Size Limit
To change the 50MB upload limit, edit `frontend/src/components/FileUpload.jsx`:
```javascript
if (file.size > 50 * 1024 * 1024) {  // Change 50 to desired MB
```

### Port Configuration
- **Backend**: Edit `app.py` - change `port=5000`
- **Frontend**: Edit `frontend/vite.config.js` - change `port: 3000`

## 🐛 Common Issues

### "npm: command not found"
- Install Node.js (see Step 1)

### "Module 'flask' not found"
```bash
pip3 install -r requirements.txt
```

### "PDF conversion failed"
- Install poppler-utils (see Step 1)

### Frontend can't connect to backend
- Ensure backend is running on port 5000
- Check browser console for errors
- Verify CORS is enabled in Flask

### GPU not detected
```bash
# Check PyTorch GPU support
python3 -c "import torch; print(f'CUDA: {torch.cuda.is_available()}, MPS: {torch.backends.mps.is_available()}')"
```

## 📦 Production Deployment

### Backend
```bash
# Use gunicorn for production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend
```bash
cd frontend
npm run build
# Serve the 'dist' folder with nginx or similar
```

## 🔒 Security Notes

For production deployment:
1. Add authentication to API endpoints
2. Implement rate limiting
3. Use HTTPS
4. Set up proper CORS policies
5. Add input validation and sanitization
6. Use environment variables for sensitive config

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [DocTR Documentation](https://mindee.github.io/doctr/)

## 💡 Tips

- Use Chrome/Firefox for best compatibility
- Ensure stable internet for initial dependency downloads
- First run may take longer due to model downloads
- GPU processing is significantly faster than CPU
- Keep PDF files under 50MB for optimal performance

## 🆘 Need Help?

If you encounter issues:
1. Check the terminal output for error messages
2. Review the browser console (F12) for frontend errors
3. Ensure all dependencies are installed correctly
4. Verify ports 3000 and 5000 are not in use by other applications

---

**Ready to analyze your structural drawings!** 🏗️

