# HumanLoopML - System Architecture

## Overview

HumanLoopML is a human-in-the-loop machine learning system that demonstrates how iterative human feedback improves model performance over time. The system performs multi-class text classification on the AG News dataset and continuously learns from human corrections.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (GitHub Pages)                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Static HTML/CSS/JS                                       │  │
│  │  - Text input                                             │  │
│  │  - Prediction display                                     │  │
│  │  - Feedback collection UI                                 │  │
│  │  - Performance visualization                              │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/REST API
                             │ (fetch requests)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                              │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │  /predict        │  │  /feedback       │                   │
│  │  POST endpoint   │  │  POST endpoint   │                   │
│  └────────┬─────────┘  └────────┬─────────┘                   │
│           │                      │                              │
│           ▼                      ▼                              │
│  ┌──────────────────────────────────────────┐                  │
│  │  Model Manager                            │                  │
│  │  - Load current model version            │                  │
│  │  - Predict with confidence                │                  │
│  └──────────────────────────────────────────┘                  │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────────────────────────────┐                  │
│  │  Feedback Storage                        │                  │
│  │  - Store (text, prediction, label)       │                  │
│  │  - Timestamp & model version tracking    │                  │
│  └──────────────────────────────────────────┘                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TRAINING PIPELINE                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Baseline Training                                       │  │
│  │  - Load AG News dataset                                  │  │
│  │  - TF-IDF vectorization                                  │  │
│  │  - Logistic Regression                                   │  │
│  │  - Save model v1                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│                             ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Retraining with Feedback                                │  │
│  │  - Combine original training + feedback                  │  │
│  │  - Optionally weight feedback samples                    │  │
│  │  - Retrain model                                         │  │
│  │  - Version new model (v2, v3, ...)                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EVALUATION & METRICS                          │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │  Metrics         │  │  Visualization   │                   │
│  │  - Accuracy      │  │  - Performance   │                   │
│  │  - F1-score      │  │    over time     │                   │
│  │  - Confusion     │  │  - Before/After  │                   │
│  │    Matrix        │  │    comparison    │                   │
│  └──────────────────┘  └──────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend (frontend/)
- **Technology**: Static HTML/CSS/JavaScript
- **Deployment**: GitHub Pages (can use frontend/ or docs/ folder)
- **Features**:
  - Text input for classification
  - Real-time prediction display with confidence scores
  - Feedback collection interface (Correct/Incorrect buttons)
  - Label selection when prediction is incorrect
  - Performance charts showing improvement over time
- **Communication**: REST API calls to FastAPI backend using `fetch()`

### 2. Backend API (api/)
- **Technology**: FastAPI (Python)
- **Endpoints**:
  - `POST /predict`: Accepts text, returns prediction + confidence
  - `POST /feedback`: Accepts feedback (text, prediction, correct label)
  - `GET /metrics`: Returns current model performance metrics
  - `GET /model/version`: Returns current model version
- **Model Management**:
  - Loads current model version from disk
  - Handles model versioning (v1, v2, v3, ...)
  - Stores feedback in persistent storage (JSON/CSV)

### 3. Training Pipeline (training/)
- **Baseline Training** (`train_baseline.py`):
  - Loads AG News dataset
  - Splits into train/validation/test
  - Trains TF-IDF + Logistic Regression
  - Saves model as v1
  - Evaluates and saves baseline metrics
  
- **Retraining** (`retrain_with_feedback.py`):
  - Loads original training data
  - Loads collected feedback
  - Combines datasets (optionally weights feedback)
  - Retrains model
  - Increments version number
  - Evaluates and saves new metrics

### 4. Evaluation (evaluation/)
- **Metrics** (`metrics.py`):
  - Accuracy calculation
  - Macro F1-score
  - Confusion matrix generation
  - Per-class metrics
  
- **Visualization** (`plots.py`):
  - Performance over time charts
  - Before/after comparison plots
  - Confusion matrix visualization

### 5. Data Storage
- **Models**: `models/` directory (pickle/joblib)
  - `model_v1.pkl`
  - `model_v2.pkl`
  - `model_v3.pkl`
  - ...
- **Feedback**: `data/feedback/` directory (JSON/CSV)
  - `feedback.json` or `feedback.csv`
  - Stores: text, model_prediction, human_label, timestamp, model_version
- **Metrics**: `data/metrics/` directory (JSON)
  - `metrics_v1.json`
  - `metrics_v2.json`
  - ...

## Data Flow

### Prediction Flow
1. User enters text in frontend
2. Frontend sends POST request to `/predict`
3. Backend loads current model version
4. Model predicts label and confidence
5. Backend returns prediction to frontend
6. Frontend displays result

### Feedback Flow
1. User clicks "Incorrect" and selects correct label
2. Frontend sends POST request to `/feedback`
3. Backend stores feedback with timestamp and model version
4. Backend acknowledges receipt

### Retraining Flow
1. Admin/script triggers retraining
2. Training script loads original training data
3. Training script loads all collected feedback
4. Combines datasets (with optional weighting)
5. Retrains model
6. Saves new model version
7. Evaluates on test set
8. Saves metrics
9. New model becomes active for predictions

## Human-in-the-Loop Design

The system implements a continuous learning loop:

1. **Initial State**: Baseline model (v1) trained on AG News training set
2. **Inference**: Model makes predictions on new text
3. **Feedback Collection**: Humans identify incorrect predictions and provide correct labels
4. **Learning**: System retrains using original data + feedback
5. **Improvement**: New model version (v2+) should show improved performance
6. **Iteration**: Process repeats, creating v3, v4, etc.

### Key Design Decisions

- **Simple Baseline**: TF-IDF + Logistic Regression chosen for:
  - Fast training and inference
  - Interpretability
  - Clear demonstration of improvement
  
- **Feedback Weighting**: Option to weight feedback samples higher than original training data to emphasize recent corrections

- **Versioning**: Each retraining creates a new model version, allowing comparison of performance over time

- **Static Frontend**: No backend required for frontend deployment, making GitHub Pages hosting simple

## Technology Stack

- **Backend**: Python 3.8+, FastAPI, scikit-learn
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **ML**: scikit-learn (TF-IDF, Logistic Regression)
- **Data**: AG News dataset
- **Storage**: File-based (JSON/CSV for feedback, pickle/joblib for models)
- **Deployment**: GitHub Pages (frontend), Free cloud hosting (backend)

## Deployment Strategy

### Frontend Deployment (GitHub Pages)
- **Location**: `frontend/` folder in repository (or copy to `docs/` if preferred)
- **URL**: `https://<username>.github.io/humanloopml/`
- **Setup**: Enable GitHub Pages in repository settings, point to `/frontend` folder (or `/docs`)
- **Cost**: Free

### Backend Deployment (Free Hosting Options)

Since GitHub Pages only serves static files, the FastAPI backend needs to be hosted separately. Here are the best **free** options:

#### Option 1: Render (Recommended - Easiest)
- **URL**: https://render.com
- **Free Tier**: 
  - 750 hours/month (enough for 24/7)
  - Spins down after 15 min inactivity (cold start ~30s)
  - 512MB RAM
- **Setup**:
  1. Connect GitHub repository
  2. Select "Web Service"
  3. Build command: `pip install -r api/requirements.txt`
  4. Start command: `cd api && uvicorn main:app --host 0.0.0.0 --port $PORT`
  5. Add environment variable: `PORT=10000`
- **Pros**: Very easy, automatic HTTPS, GitHub integration
- **Cons**: Cold starts after inactivity
- **Backend URL**: `https://your-app-name.onrender.com`

#### Option 2: Railway
- **URL**: https://railway.app
- **Free Tier**: 
  - $5 credit/month (usually enough for small apps)
  - 512MB RAM
  - No cold starts
- **Setup**:
  1. Connect GitHub repository
  2. Auto-detects FastAPI
  3. Set start command: `cd api && uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Pros**: No cold starts, easy setup
- **Cons**: Limited free credit (may need to upgrade for heavy use)
- **Backend URL**: `https://your-app-name.up.railway.app`

#### Option 3: Fly.io
- **URL**: https://fly.io
- **Free Tier**: 
  - 3 shared VMs (256MB each)
  - 160GB outbound data transfer
- **Setup**: Requires Dockerfile, more setup complexity
- **Pros**: Good performance, generous free tier
- **Cons**: More complex setup, requires Docker knowledge

#### Option 4: PythonAnywhere
- **URL**: https://www.pythonanywhere.com
- **Free Tier**: 
  - Limited to 1 web app
  - External requests only (can't receive from GitHub Pages due to CORS)
  - 512MB disk space
- **Setup**: Upload files via web interface or Git
- **Pros**: Simple Python hosting
- **Cons**: CORS limitations, less modern

### Recommended Setup: Render

For this project, **Render is recommended** because:
1. ✅ Easiest setup (just connect GitHub)
2. ✅ Automatic HTTPS
3. ✅ Free tier sufficient for demo
4. ✅ Good documentation
5. ✅ Handles FastAPI out of the box

### Frontend-Backend Connection

The frontend JavaScript will need to be configured with the backend URL:

```javascript
// In docs/app.js
const API_BASE_URL = 'https://your-app-name.onrender.com';
// or for local development:
// const API_BASE_URL = 'http://localhost:8000';
```

### CORS Configuration

The FastAPI backend must allow requests from the GitHub Pages domain:

```python
# In api/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://<username>.github.io",  # GitHub Pages URL
        "http://localhost:8000",  # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Deployment Checklist

1. **Backend**:
   - [ ] Push code to GitHub
   - [ ] Deploy to Render/Railway/etc.
   - [ ] Test API endpoints
   - [ ] Note the backend URL

2. **Frontend**:
   - [ ] Update `API_BASE_URL` in `frontend/app.js` with backend URL
   - [ ] Push to GitHub
   - [ ] Enable GitHub Pages in repo settings (point to `/frontend` folder)
   - [ ] Test frontend-backend connection

3. **Training**:
   - [ ] Run `train_baseline.py` locally
   - [ ] Upload trained model to backend (or include in repo)
   - [ ] Verify model loads correctly on backend

## Scalability Considerations

For a production system, consider:
- Database instead of file storage for feedback
- Model serving infrastructure (e.g., MLflow, TensorFlow Serving)
- Authentication and rate limiting
- Distributed training for large datasets
- Real-time model updates without downtime

For this demo, file-based storage and simple model loading are sufficient and keep the system understandable.
