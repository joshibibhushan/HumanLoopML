# Quick Start Guide

Get HumanLoopML running in under 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Step-by-Step Setup

### 1. Install Dependencies

```bash
pip install -r api/requirements.txt
```

Or use the setup script:
```bash
python setup.py
```

### 2. Train Baseline Model

```bash
python training/train_baseline.py
```

This will:
- Download the AG News dataset (first time only)
- Train a TF-IDF + Logistic Regression model
- Save model as `models/model_v1.joblib`
- Save metrics as `data/metrics/metrics_v1.json`

**Expected time**: 2-3 minutes

### 3. Start the Backend API

```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4. Open the Frontend

1. Open `frontend/index.html` in your web browser
2. The frontend is pre-configured to connect to `http://localhost:8000`

### 5. Test It Out!

1. Enter some text in the text box (e.g., "Apple releases new iPhone")
2. Click "Predict"
3. See the prediction and confidence score
4. If incorrect, click "Incorrect" and select the correct label
5. Submit feedback

### 6. Retrain with Feedback

After collecting some feedback:

```bash
python training/retrain_with_feedback.py
```

This creates `model_v2.joblib` with improved performance!

## Troubleshooting

### "No module named 'datasets'"
```bash
pip install -r api/requirements.txt
```

### "Model not found"
Make sure you ran `python training/train_baseline.py` first.

### Frontend can't connect
- Check backend is running: `curl http://localhost:8000/health`
- Check browser console for errors
- Verify `API_BASE_URL` in `docs/app.js`

### Port 8000 already in use
Change the port:
```bash
uvicorn main:app --reload --port 8001
```
And update `API_BASE_URL` in `frontend/app.js` to `http://localhost:8001`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [docs/architecture.md](docs/architecture.md) for system design
- Deploy to production using the deployment guide in README

## Example API Calls

### Predict
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "The stock market reached new highs today"}'
```

### Submit Feedback
```bash
curl -X POST http://localhost:8000/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The stock market reached new highs today",
    "model_prediction": "Business",
    "human_label": "Business"
  }'
```

### Get Metrics
```bash
curl http://localhost:8000/metrics
```

Happy learning! 🚀
