"""
Model Management Utilities

Helper functions for model loading and management.
"""

import os
import joblib
import json


def load_model_and_vectorizer(version, models_dir):
    """
    Load model and vectorizer for a specific version.
    
    Args:
        version: Model version number
        models_dir: Directory containing models
    
    Returns:
        Tuple of (model, vectorizer)
    """
    model_path = os.path.join(models_dir, f'model_v{version}.joblib')
    vectorizer_path = os.path.join(models_dir, f'vectorizer_v{version}.joblib')
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model v{version} not found")
    
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    
    return model, vectorizer


def load_label_names(models_dir):
    """
    Load label names from JSON file.
    
    Args:
        models_dir: Directory containing models
    
    Returns:
        List of label names
    """
    label_path = os.path.join(models_dir, 'label_names.json')
    
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            return json.load(f)
    
    # Default labels for AG News
    return ['World', 'Sports', 'Business', 'Sci/Tech']
