# How to Run HumanLoopML

## Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r api/requirements.txt
```

### Step 2: Train the Baseline Model
```bash
python training/train_baseline.py
```
⏱️ This takes 2-3 minutes (downloads AG News dataset and trains model)

### Step 3: Start the Backend & Open Frontend

**Terminal 1 - Start Backend:**
```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Browser - Open Frontend:**
- Open `frontend/index.html` in your web browser
- Or double-click the file

That's it! You should now be able to:
- Enter text and get predictions
- Submit feedback when predictions are wrong
- See performance metrics

---

## Detailed Instructions

### Prerequisites Check
```bash
python --version  # Should be 3.8 or higher
```

### Full Setup Process

1. **Install Python Dependencies**
   ```bash
   pip install -r api/requirements.txt
   ```
   
   This installs:
   - FastAPI (web framework)
   - scikit-learn (ML library)
   - datasets (for AG News)
   - uvicorn (ASGI server)
   - And other dependencies

2. **Train Baseline Model** (Required First Time)
   ```bash
   python training/train_baseline.py
   ```
   
   What this does:
   - Downloads AG News dataset (120K news articles)
   - Trains TF-IDF + Logistic Regression model
   - Saves model to `models/model_v1.joblib`
   - Saves metrics to `data/metrics/metrics_v1.json`
   
   Expected output:
   ```
   Loading AG News dataset...
   Training samples: 120000
   Test samples: 7600
   Training TF-IDF vectorizer...
   Training Logistic Regression model...
   Test Accuracy: 0.89XX
   Model saved to: models/model_v1.joblib
   ```

3. **Start the Backend API**
   ```bash
   cd api
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   You should see:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   INFO:     Application startup complete.
   ```
   
   Keep this terminal open!

4. **Open the Frontend**
   - Navigate to the `frontend` folder
   - Double-click `index.html` OR
   - Right-click → Open with → Your browser
   
   The frontend will automatically connect to `http://localhost:8000`

5. **Test It Out!**
   - Enter text: "Apple releases new iPhone with AI features"
   - Click "Predict"
   - See prediction: "Sci/Tech" with confidence score
   - If wrong, click "Incorrect" → Select correct label → Submit

---

## Collecting Feedback & Retraining

After collecting some feedback through the UI:

1. **Retrain Model with Feedback**
   ```bash
   python training/retrain_with_feedback.py
   ```
   
   This creates `model_v2.joblib` with improved performance!

2. **Restart Backend** (to load new model)
   - Stop the backend (Ctrl+C)
   - Start again: `uvicorn main:app --reload`

---

## Troubleshooting

### ❌ "No module named 'datasets'"
**Solution:**
```bash
pip install -r api/requirements.txt
```

### ❌ "Model not found" or "No model found"
**Solution:**
```bash
python training/train_baseline.py
```
Make sure this completes successfully before starting the API.

### ❌ Port 8000 already in use
**Solution 1:** Use a different port
```bash
uvicorn main:app --reload --port 8001
```
Then update `API_BASE_URL` in `frontend/app.js` to `http://localhost:8001`

**Solution 2:** Find and kill the process using port 8000
```bash
# Windows PowerShell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### ❌ Frontend can't connect to backend
**Check:**
1. Backend is running (see terminal output)
2. Test backend: Open `http://localhost:8000` in browser (should see API docs)
3. Check `API_BASE_URL` in `docs/app.js` matches your backend URL
4. Check browser console (F12) for errors

### ❌ "CORS error" in browser console
**Solution:** The backend is configured to allow all origins. If you see CORS errors, make sure:
- Backend is running
- Frontend is accessing the correct URL
- Check `api/main.py` CORS settings

### ❌ Training script fails
**Common issues:**
- Internet connection needed (downloads dataset)
- Out of memory (try reducing dataset size in code)
- Missing dependencies: `pip install -r api/requirements.txt`

---

## Alternative: Using Docker

If you have Docker installed:

```bash
# Build and run
docker-compose up --build
```

Backend will be at `http://localhost:8000`

---

## Testing the API Directly

### Test Prediction
```bash
curl -X POST http://localhost:8000/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"The stock market reached new highs today\"}"
```

### Test Health
```bash
curl http://localhost:8000/health
```

### Get Metrics
```bash
curl http://localhost:8000/metrics
```

---

## What's Running Where?

- **Backend API**: `http://localhost:8000`
  - API Docs: `http://localhost:8000/docs` (Swagger UI)
  - Health Check: `http://localhost:8000/health`
  
- **Frontend**: `frontend/index.html` (file:// protocol)
  - Connects to backend at `http://localhost:8000`

---

## Next Steps After Running

1. ✅ Make some predictions
2. ✅ Submit feedback for incorrect predictions
3. ✅ Retrain: `python training/retrain_with_feedback.py`
4. ✅ See improved metrics in the frontend
5. 📚 Read `README.md` for deployment instructions
6. 🚀 Deploy to production (GitHub Pages + Render)

---

## Need Help?

- Check `README.md` for detailed documentation
- Check `QUICKSTART.md` for condensed guide
- Check `docs/architecture.md` for system design
