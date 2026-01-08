# HumanLoopML

A recruiter-facing, human-in-the-loop machine learning system that demonstrates how human feedback improves model performance over time.

## Problem Statement

Traditional machine learning models are trained once and deployed. However, real-world data often contains patterns not seen during training, leading to prediction errors. This system demonstrates a **human-in-the-loop** approach where:

1. A baseline model makes predictions on new text
2. Humans identify incorrect predictions and provide correct labels
3. The model is retrained using this feedback
4. Performance improves iteratively with each retraining cycle

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│              FRONTEND (GitHub Pages)                     │
│  Static HTML/CSS/JS - Prediction UI & Feedback          │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP/REST API
                       ▼
┌─────────────────────────────────────────────────────────┐
│              FASTAPI BACKEND                            │
│  /predict  - Text classification                        │
│  /feedback - Human feedback collection                  │
│  /metrics  - Performance metrics                        │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│         TRAINING PIPELINE                               │
│  Baseline: TF-IDF + Logistic Regression                 │
│  Retraining: Original data + Human feedback            │
└─────────────────────────────────────────────────────────┘
```

### Key Components

- **Task**: Multi-class text classification (AG News dataset)
- **Labels**: World, Sports, Business, Sci/Tech
- **Baseline Model**: TF-IDF + Logistic Regression (simple, explainable)
- **Feedback Loop**: Collects corrections → Retrains → Improves performance

## Human-in-the-Loop Design

The system implements a continuous learning loop:

1. **Initial State**: Baseline model (v1) trained on AG News training set
2. **Inference**: Model predicts labels for new text inputs
3. **Feedback Collection**: Users identify incorrect predictions and provide correct labels
4. **Learning**: System combines original training data with feedback
5. **Improvement**: New model version (v2+) shows improved performance
6. **Iteration**: Process repeats, creating v3, v4, etc.

### Design Decisions

- **Simple Baseline**: TF-IDF + Logistic Regression chosen for fast training, interpretability, and clear demonstration of improvement
- **Feedback Weighting**: Configurable weight for feedback samples (default: equal weight)
- **Versioning**: Each retraining creates a new model version for performance comparison
- **Static Frontend**: No backend required for frontend deployment (GitHub Pages compatible)

## Results

### Baseline vs Feedback-Enhanced

After collecting human feedback and retraining:

- **Baseline (v1)**: Trained on original AG News training set
- **Enhanced (v2+)**: Trained on original data + human feedback

Expected improvements:
- Better accuracy on edge cases identified by humans
- Improved F1 scores, especially for classes with more feedback
- Reduced confusion between similar classes

*Note: Actual results depend on the quality and quantity of feedback collected.*

## Tradeoffs

### What We Chose

✅ **Simple, explainable model** (TF-IDF + Logistic Regression)
- Pro: Easy to understand and debug
- Con: May not achieve state-of-the-art performance

✅ **File-based storage** (JSON for feedback, joblib for models)
- Pro: Simple, no database setup required
- Con: Not suitable for high-volume production

✅ **Manual retraining** (script-based)
- Pro: Full control, easy to understand
- Con: Requires manual intervention

### What We Didn't Include

❌ Deep learning models (Transformers, BERT)
- Would improve accuracy but reduce explainability

❌ Database storage
- Would scale better but adds complexity

❌ Automatic retraining
- Would be more automated but harder to debug

❌ Authentication/rate limiting
- Would be needed for production but not for demo

## Quick Start (Under 5 Minutes)

### Prerequisites

- Python 3.8+
- pip

### Step 1: Clone and Setup

```bash
git clone <your-repo-url>
cd HumanLoopML

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r api/requirements.txt
```

### Step 2: Train Baseline Model

```bash
python training/train_baseline.py
```

This will:
- Download AG News dataset
- Train TF-IDF + Logistic Regression model
- Save model as `models/model_v1.joblib`
- Save metrics as `data/metrics/metrics_v1.json`

### Step 3: Start Backend API

```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Step 4: Open Frontend

1. Open `frontend/index.html` in a web browser
2. Update `API_BASE_URL` in `frontend/app.js` if needed (default: `http://localhost:8000`)
3. Enter text and get predictions!

### Step 5: Collect Feedback & Retrain

1. Use the frontend to make predictions
2. Click "Incorrect" when predictions are wrong
3. Select the correct label
4. After collecting feedback, retrain:

```bash
python training/retrain_with_feedback.py
```

This creates `model_v2.joblib` with improved performance.

## Deployment

### Frontend (GitHub Pages)

**Option 1: Use frontend folder directly**
1. Push code to GitHub repository
2. Go to repository Settings → Pages
3. Select source: "Deploy from a branch"
4. Select branch: `main` (or `master`)
5. Select folder: `/frontend`
6. Your site will be at: `https://<username>.github.io/humanloopml/`

**Option 2: Use docs folder (alternative)**
1. Copy `frontend/` contents to `docs/` folder
2. Push to GitHub
3. In repository Settings → Pages, select folder: `/docs`

**Important**: Update `API_BASE_URL` in `frontend/app.js` with your backend URL.

### Backend (Free Hosting - Render)

1. **Sign up** at [Render.com](https://render.com) (free tier available)

2. **Create New Web Service**:
   - Connect your GitHub repository
   - Name: `humanloopml-api`
   - Environment: `Python 3`
   - Build Command: `pip install -r api/requirements.txt`
   - Start Command: `cd api && uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variable**:
   - Key: `PORT`
   - Value: `10000`

4. **Deploy**: Render will automatically deploy on every push

5. **Get URL**: Your backend will be at `https://your-app-name.onrender.com`

6. **Update Frontend**: Change `API_BASE_URL` in `frontend/app.js` to your Render URL

### Alternative Backend Hosting

- **Railway**: Similar to Render, $5 free credit/month
- **Fly.io**: Requires Dockerfile, generous free tier
- **PythonAnywhere**: Simple but has CORS limitations

See `docs/architecture.md` for detailed deployment instructions.

## Project Structure

```
humanloopml/
├── frontend/              # Frontend (HTML/CSS/JS)
│   ├── index.html
│   ├── app.js
│   └── style.css
├── docs/                  # Documentation
│   └── architecture.md
├── api/                   # FastAPI Backend
│   ├── main.py            # FastAPI app
│   ├── model.py           # Model utilities
│   └── requirements.txt
├── training/              # Training Scripts
│   ├── train_baseline.py
│   └── retrain_with_feedback.py
├── evaluation/            # Metrics & Visualization
│   ├── metrics.py
│   └── plots.py
├── data/                  # Data Storage
│   ├── feedback/          # Human feedback (JSON)
│   └── metrics/           # Evaluation metrics (JSON)
├── models/                # Trained models (joblib)
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## API Endpoints

### `POST /predict`
Predict label for input text.

**Request:**
```json
{
  "text": "Apple releases new AI-powered MacBook"
}
```

**Response:**
```json
{
  "prediction": "Sci/Tech",
  "confidence": 0.82,
  "model_version": "v1"
}
```

### `POST /feedback`
Submit human feedback.

**Request:**
```json
{
  "text": "Apple releases new AI-powered MacBook",
  "model_prediction": "Sci/Tech",
  "human_label": "Business"
}
```

**Response:**
```json
{
  "message": "Feedback received successfully",
  "timestamp": "2024-01-15T10:30:00"
}
```

### `GET /metrics`
Get performance metrics for current or specific model version.

**Query Parameters:**
- `version` (optional): Model version number

**Response:**
```json
{
  "version": "v1",
  "metrics": {
    "accuracy": 0.89,
    "f1_macro": 0.88,
    "f1_weighted": 0.89,
    "per_class": {...},
    "confusion_matrix": [...]
  }
}
```

### `GET /model/version`
Get current model version.

**Response:**
```json
{
  "version": "v1",
  "version_number": 1
}
```

## Development

### Running Tests

```bash
# Test API endpoints
curl http://localhost:8000/predict -X POST -H "Content-Type: application/json" -d '{"text":"Test article"}'
```

### Retraining with Custom Feedback Weight

```bash
python training/retrain_with_feedback.py --feedback-weight 2.0
```

This weights feedback samples 2x higher than original training data.

### Generating Performance Plots

```python
from evaluation.plots import plot_performance_over_time, plot_before_after_comparison

# Plot performance over time
plot_performance_over_time([1, 2, 3], 'data/metrics', 'performance.png')

# Compare baseline vs improved
plot_before_after_comparison(1, 2, 'data/metrics', 'comparison.png')
```

## Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Ensure all dependencies are installed: `pip install -r api/requirements.txt`
- Verify model exists: `ls models/model_v1.joblib`

### Frontend can't connect to backend
- Check `API_BASE_URL` in `docs/app.js`
- Ensure backend is running: `curl http://localhost:8000/health`
- Check CORS settings in `api/main.py`

### Model not found
- Run `python training/train_baseline.py` first
- Check `models/` directory exists and contains model files

### Feedback not saving
- Check `data/feedback/` directory exists
- Verify write permissions
- Check `data/feedback/feedback.json` file

## License

MIT License - feel free to use this project for learning and demonstrations.

## Contributing

This is a demonstration project. For production use, consider:
- Adding authentication
- Using a database for feedback storage
- Implementing automatic retraining
- Adding more sophisticated models
- Implementing proper logging and monitoring

---

**Built with**: FastAPI, scikit-learn, HTML/CSS/JavaScript

**For**: ML Engineers, Applied Scientists, Research Engineers evaluating ML system design
