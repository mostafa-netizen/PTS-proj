# 🚀 Quick Start Guide

## One-Command Setup & Run

```bash
# Make startup script executable (first time only)
chmod +x start.sh

# Run the application
./start.sh
```

Then open: **http://localhost:3000**

---

## Manual Setup (If needed)

### 1. Install Dependencies

```bash
# Backend
pip3 install -r requirements.txt

# Frontend
cd frontend
npm install
cd ..
```

### 2. Run Servers

**Terminal 1 - Backend:**
```bash
python3 app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## First Time Setup

### macOS
```bash
# Install poppler for PDF processing
brew install poppler

# Install Node.js (if not installed)
brew install node
```

### Ubuntu/Debian
```bash
# Install poppler
sudo apt-get install poppler-utils

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

---

## Usage Flow

1. **Upload** → Drag & drop PDF or browse
2. **Process** → Wait for AI analysis (progress shown)
3. **Download** → View and download annotated results

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `npm: command not found` | Install Node.js |
| `Module 'flask' not found` | Run `pip3 install -r requirements.txt` |
| `PDF conversion failed` | Install poppler-utils |
| Port already in use | Change ports in `app.py` and `vite.config.js` |

---

## File Locations

- **Uploads**: `uploads/` (auto-created)
- **Results**: `outputs/` (auto-created)
- **Frontend**: `frontend/src/`
- **Backend**: `app.py`

---

## Key URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Docs**: See `README.md`

---

## Need More Help?

- 📖 Full documentation: `README.md`
- 🔧 Setup guide: `SETUP_GUIDE.md`
- 📊 Project summary: `PROJECT_SUMMARY.md`
- 🎨 UI preview: `UI_PREVIEW.md`

---

**Ready in 3 minutes!** ⚡

