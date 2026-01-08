"""
Metrics Calculation Module

Provides functions for calculating and storing evaluation metrics.
"""

import json
import os
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, precision_recall_fscore_support


def calculate_metrics(y_true, y_pred, label_names):
    """
    Calculate comprehensive metrics for model evaluation.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        label_names: List of label names
    
    Returns:
        Dictionary containing all metrics
    """
    accuracy = accuracy_score(y_true, y_pred)
    f1_macro = f1_score(y_true, y_pred, average='macro')
    f1_weighted = f1_score(y_true, y_pred, average='weighted')
    
    # Per-class metrics
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=range(len(label_names)), zero_division=0
    )
    
    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=range(len(label_names)))
    
    # Per-class metrics as dictionary
    per_class_metrics = {}
    for i, label in enumerate(label_names):
        per_class_metrics[label] = {
            'precision': float(precision[i]),
            'recall': float(recall[i]),
            'f1': float(f1[i]),
            'support': int(support[i])
        }
    
    metrics = {
        'accuracy': float(accuracy),
        'f1_macro': float(f1_macro),
        'f1_weighted': float(f1_weighted),
        'per_class': per_class_metrics,
        'confusion_matrix': cm.tolist(),
        'label_names': label_names
    }
    
    return metrics


def save_metrics(metrics, version, metrics_dir):
    """
    Save metrics to JSON file.
    
    Args:
        metrics: Dictionary of metrics
        version: Model version number
        metrics_dir: Directory to save metrics
    """
    os.makedirs(metrics_dir, exist_ok=True)
    
    metrics_path = os.path.join(metrics_dir, f'metrics_v{version}.json')
    
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"Metrics saved to: {metrics_path}")


def load_metrics(version, metrics_dir):
    """
    Load metrics from JSON file.
    
    Args:
        version: Model version number
        metrics_dir: Directory containing metrics
    
    Returns:
        Dictionary of metrics
    """
    metrics_path = os.path.join(metrics_dir, f'metrics_v{version}.json')
    
    if not os.path.exists(metrics_path):
        return None
    
    with open(metrics_path, 'r') as f:
        metrics = json.load(f)
    
    return metrics


def compare_models(versions, metrics_dir):
    """
    Compare metrics across multiple model versions.
    
    Args:
        versions: List of version numbers to compare
        metrics_dir: Directory containing metrics
    
    Returns:
        Dictionary comparing metrics across versions
    """
    comparison = {}
    
    for version in versions:
        metrics = load_metrics(version, metrics_dir)
        if metrics:
            comparison[f'v{version}'] = {
                'accuracy': metrics['accuracy'],
                'f1_macro': metrics['f1_macro'],
                'f1_weighted': metrics['f1_weighted']
            }
    
    return comparison
