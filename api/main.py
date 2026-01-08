"""
FastAPI Backend for HumanLoopML

Provides REST API endpoints for:
- Text classification predictions
- Human feedback collection
- Model metrics retrieval
"""

import os
import json
import joblib
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

# Get project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')
FEEDBACK_DIR = os.path.join(PROJECT_ROOT, 'data', 'feedback')
METRICS_DIR = os.path.join(PROJECT_ROOT, 'data', 'metrics')

# Initialize FastAPI app
app = FastAPI(
    title="HumanLoopML API",
    description="Human-in-the-loop ML system for text classification",
    version="1.0.0"
)

# CORS middleware - allow requests from GitHub Pages and localhost
# Note: For production, replace with specific origins for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for loaded model
current_model = None
current_vectorizer = None
current_version = None
label_names = None


# Pydantic models for request/response
class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    prediction: str
    confidence: float
    model_version: str


class FeedbackRequest(BaseModel):
    text: str
    model_prediction: str
    human_label: str


class FeedbackResponse(BaseModel):
    message: str
    timestamp: str


def get_current_model_version():
    """Get the current active model version."""
    version_file = os.path.join(MODELS_DIR, 'current_version.txt')
    if os.path.exists(version_file):
        with open(version_file, 'r') as f:
            return int(f.read().strip())
    
    # If no current_version.txt, find highest version
    versions = []
    if os.path.exists(MODELS_DIR):
        for filename in os.listdir(MODELS_DIR):
            if filename.startswith('model_v') and filename.endswith('.joblib'):
                try:
                    version = int(filename.replace('model_v', '').replace('.joblib', ''))
                    versions.append(version)
                except ValueError:
                    continue
    
    return max(versions) if versions else None


def load_model(version=None):
    """Load model and vectorizer from disk."""
    global current_model, current_vectorizer, current_version, label_names
    
    if version is None:
        version = get_current_model_version()
        if version is None:
            raise ValueError("No model found. Please train a baseline model first.")
    
    model_path = os.path.join(MODELS_DIR, f'model_v{version}.joblib')
    vectorizer_path = os.path.join(MODELS_DIR, f'vectorizer_v{version}.joblib')
    label_path = os.path.join(MODELS_DIR, 'label_names.json')
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model v{version} not found at {model_path}")
    
    current_model = joblib.load(model_path)
    current_vectorizer = joblib.load(vectorizer_path)
    current_version = version
    
    # Load label names
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            label_names = json.load(f)
    else:
        label_names = ['World', 'Sports', 'Business', 'Sci/Tech']
    
    print(f"Loaded model v{version}")


def get_label_name(label_id):
    """Convert label ID to label name."""
    if label_names and label_id < len(label_names):
        return label_names[label_id]
    return f"Label_{label_id}"


def get_label_id(label_name):
    """Convert label name to label ID."""
    if label_names:
        try:
            return label_names.index(label_name)
        except ValueError:
            pass
    return None


@app.on_event("startup")
async def startup_event():
    """Load model on startup."""
    try:
        load_model()
        print("Model loaded successfully on startup")
    except Exception as e:
        print(f"Warning: Could not load model on startup: {e}")
        print("Model will be loaded on first prediction request")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "HumanLoopML API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "POST /predict",
            "feedback": "POST /feedback",
            "metrics": "GET /metrics",
            "model_version": "GET /model/version"
        }
    }


@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """
    Predict label for input text.
    
    Args:
        request: PredictRequest with text field
    
    Returns:
        PredictResponse with prediction, confidence, and model version
    """
    global current_model, current_vectorizer, current_version
    
    # Load model if not loaded
    if current_model is None or current_vectorizer is None:
        try:
            load_model()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Model not available: {str(e)}")
    
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        # Vectorize text
        text_vector = current_vectorizer.transform([request.text])
        
        # Predict
        prediction_id = current_model.predict(text_vector)[0]
        prediction_proba = current_model.predict_proba(text_vector)[0]
        confidence = float(prediction_proba[prediction_id])
        
        # Get label name
        prediction_name = get_label_name(prediction_id)
        
        return PredictResponse(
            prediction=prediction_name,
            confidence=confidence,
            model_version=f"v{current_version}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """
    Submit human feedback for a prediction.
    
    Args:
        request: FeedbackRequest with text, model_prediction, and human_label
    
    Returns:
        FeedbackResponse confirming receipt
    """
    # Validate input
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if not request.human_label:
        raise HTTPException(status_code=400, detail="Human label cannot be empty")
    
    # Get current model version
    version = get_current_model_version()
    if version is None:
        version = 1  # Default if no model found
    
    # Create feedback entry
    feedback_entry = {
        "text": request.text,
        "model_prediction": request.model_prediction,
        "human_label": request.human_label,
        "timestamp": datetime.utcnow().isoformat(),
        "model_version": f"v{version}"
    }
    
    # Save feedback
    os.makedirs(FEEDBACK_DIR, exist_ok=True)
    feedback_file = os.path.join(FEEDBACK_DIR, 'feedback.json')
    
    # Load existing feedback or create new list
    if os.path.exists(feedback_file):
        with open(feedback_file, 'r') as f:
            feedback_data = json.load(f)
    else:
        feedback_data = []
    
    # Append new feedback
    feedback_data.append(feedback_entry)
    
    # Save updated feedback
    with open(feedback_file, 'w') as f:
        json.dump(feedback_data, f, indent=2)
    
    return FeedbackResponse(
        message="Feedback received successfully",
        timestamp=feedback_entry["timestamp"]
    )


@app.get("/metrics")
async def get_metrics(version: Optional[int] = None):
    """
    Get metrics for a specific model version or current version.
    
    Args:
        version: Optional model version number
    
    Returns:
        Metrics dictionary
    """
    if version is None:
        version = get_current_model_version()
        if version is None:
            raise HTTPException(status_code=404, detail="No model found")
    
    metrics_file = os.path.join(METRICS_DIR, f'metrics_v{version}.json')
    
    if not os.path.exists(metrics_file):
        raise HTTPException(status_code=404, detail=f"Metrics for v{version} not found")
    
    with open(metrics_file, 'r') as f:
        metrics = json.load(f)
    
    return {
        "version": f"v{version}",
        "metrics": metrics
    }


@app.get("/model/version")
async def get_model_version():
    """Get current model version."""
    version = get_current_model_version()
    if version is None:
        raise HTTPException(status_code=404, detail="No model found")
    
    return {
        "version": f"v{version}",
        "version_number": version
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": current_model is not None,
        "current_version": f"v{current_version}" if current_version else None
    }
