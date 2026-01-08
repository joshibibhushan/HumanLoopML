# How to Run HumanLoopML on Windows

## Quick Start (Copy & Paste These Commands)

### Step 1: Install Dependencies
```powershell
py -m pip install -r api/requirements.txt
```

### Step 2: Train Baseline Model
```powershell
py training/train_baseline.py
```
⏱️ Takes 2-3 minutes (downloads dataset and trains model)

### Step 3: Start Backend
```powershell
cd api
py -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: Open Frontend
- Navigate to `docs` folder
- Double-click `index.html`

---

## Complete Step-by-Step

### 1. Open PowerShell or Command Prompt
Press `Win + X` → Select "Windows PowerShell" or "Terminal"

### 2. Navigate to Project Directory
```powershell
cd C:\Users\hapti\Desktop\codehome\HumanLoopML
```

### 3. Install Dependencies
```powershell
py -m pip install -r api/requirements.txt
```

**Expected output:**
```
Collecting fastapi==0.104.1
Collecting uvicorn[standard]==0.24.0
...
Successfully installed ...
```

### 4. Train Baseline Model (First Time Only)
```powershell
py training/train_baseline.py
```

**What happens:**
- Downloads AG News dataset (~50MB)
- Trains TF-IDF + Logistic Regression
- Saves model to `models/model_v1.joblib`

**Expected output:**
```
Loading AG News dataset...
Training samples: 120000
Test samples: 7600
Training TF-IDF vectorizer...
Training Logistic Regression model...
Test Accuracy: 0.89XX
Model saved to: models/model_v1.joblib
```

⏱️ **This takes 2-3 minutes** - be patient!

### 5. Start Backend Server

**Open a NEW PowerShell window** (keep the first one open if you want to see training output)

```powershell
cd C:\Users\hapti\Desktop\codehome\HumanLoopML\api
py -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
INFO:     Model loaded successfully on startup
```

✅ **Keep this window open!** The backend is now running.

### 6. Open Frontend

1. Open File Explorer
2. Navigate to: `C:\Users\hapti\Desktop\codehome\HumanLoopML\docs`
3. Double-click `index.html`
4. It will open in your default browser

### 7. Test It!

1. In the browser, enter text: **"Apple releases new iPhone with AI"**
2. Click **"Predict"**
3. You should see: **Prediction: Sci/Tech** with confidence score
4. Try more examples!

---

## Using the Application

### Making Predictions
- Enter any news article text
- Click "Predict"
- See the predicted category (World, Sports, Business, Sci/Tech)

### Submitting Feedback
1. If prediction is **correct**: Click "Correct ✓"
2. If prediction is **wrong**: 
   - Click "Incorrect ✗"
   - Select the correct label
   - Click "Submit Feedback"

### Retraining with Feedback

After collecting some feedback:

1. **Stop the backend** (Press `Ctrl+C` in the backend window)

2. **Retrain the model:**
   ```powershell
   cd C:\Users\hapti\Desktop\codehome\HumanLoopML
   py training/retrain_with_feedback.py
   ```

3. **Restart backend:**
   ```powershell
   cd api
   py -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Refresh the frontend** to see updated metrics!

---

## Troubleshooting

### ❌ "py is not recognized"
**Solution:** Use `python` instead:
```powershell
python -m pip install -r api/requirements.txt
python training/train_baseline.py
```

### ❌ "No module named 'fastapi'"
**Solution:** Install dependencies:
```powershell
py -m pip install -r api/requirements.txt
```

### ❌ Port 8000 already in use
**Solution:** Use a different port:
```powershell
py -m uvicorn main:app --reload --port 8001
```
Then edit `frontend/app.js` and change:
```javascript
const API_BASE_URL = 'http://localhost:8001';
```

### ❌ "Model not found"
**Solution:** Make sure you ran:
```powershell
py training/train_baseline.py
```
And it completed successfully.

### ❌ Frontend shows "Error making prediction"
**Check:**
1. Backend is running (see terminal)
2. Open `http://localhost:8000` in browser - should show API docs
3. Check browser console (F12) for errors

### ❌ Training takes too long
**Normal!** First run downloads dataset (~50MB) and trains model. Subsequent runs are faster.

---

## Quick Reference Commands

```powershell
# Install dependencies
py -m pip install -r api/requirements.txt

# Train baseline
py training/train_baseline.py

# Start backend
cd api
py -m uvicorn main:app --reload

# Retrain with feedback
py training/retrain_with_feedback.py

# Check if backend is running
curl http://localhost:8000/health
```

---

## What You Should See

### Backend Terminal:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
INFO:     Model loaded successfully on startup
INFO:     127.0.0.1:XXXXX - "POST /predict HTTP/1.1" 200 OK
```

### Browser:
- Clean, modern UI with gradient header
- Text input box
- Prediction results with confidence
- Feedback buttons
- Performance metrics chart

---

## Next Steps

1. ✅ Make predictions and collect feedback
2. ✅ Retrain model: `py training/retrain_with_feedback.py`
3. ✅ See improved performance metrics
4. 📚 Read `README.md` for deployment
5. 🚀 Deploy to GitHub Pages + Render

---

**Need help?** Check `README.md` or `RUN.md` for more details!
