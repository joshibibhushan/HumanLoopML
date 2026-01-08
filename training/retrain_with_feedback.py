"""
Retraining Script with Human Feedback

Combines original training data with collected human feedback
and retrains the model. Creates a new model version.
"""

import os
import sys
import json
import joblib
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
import datasets

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from evaluation.metrics import calculate_metrics, save_metrics


def load_original_data():
    """Load original AG News training data."""
    print("Loading original AG News training data...")
    dataset = datasets.load_dataset("ag_news")
    
    train_texts = dataset['train']['text']
    train_labels = dataset['train']['label']
    test_texts = dataset['test']['text']
    test_labels = dataset['test']['label']
    
    label_names = ['World', 'Sports', 'Business', 'Sci/Tech']
    
    return train_texts, train_labels, test_texts, test_labels, label_names


def load_feedback(feedback_path):
    """
    Load collected human feedback.
    
    Args:
        feedback_path: Path to feedback JSON file
    
    Returns:
        List of (text, label) tuples
    """
    if not os.path.exists(feedback_path):
        print(f"No feedback file found at {feedback_path}")
        return []
    
    with open(feedback_path, 'r') as f:
        feedback_data = json.load(f)
    
    # Extract text and human_label pairs
    feedback_samples = []
    for entry in feedback_data:
        text = entry.get('text', '')
        human_label = entry.get('human_label', None)
        
        if text and human_label is not None:
            feedback_samples.append((text, human_label))
    
    print(f"Loaded {len(feedback_samples)} feedback samples")
    return feedback_samples


def get_current_model_version(models_dir):
    """
    Get the current highest model version number.
    
    Args:
        models_dir: Directory containing model files
    
    Returns:
        Current version number (int)
    """
    if not os.path.exists(models_dir):
        return 0
    
    versions = []
    for filename in os.listdir(models_dir):
        if filename.startswith('model_v') and filename.endswith('.joblib'):
            try:
                version = int(filename.replace('model_v', '').replace('.joblib', ''))
                versions.append(version)
            except ValueError:
                continue
    
    return max(versions) if versions else 0


def combine_datasets(original_texts, original_labels, feedback_samples, feedback_weight=1.0):
    """
    Combine original training data with feedback.
    
    Args:
        original_texts: Original training texts
        original_labels: Original training labels
        feedback_samples: List of (text, label) tuples from feedback
        feedback_weight: Weight multiplier for feedback samples (for oversampling)
    
    Returns:
        Combined texts and labels arrays
    """
    # Convert original data to lists
    combined_texts = list(original_texts)
    combined_labels = list(original_labels)
    
    # Add feedback samples (with optional weighting via repetition)
    for text, label in feedback_samples:
        # Repeat feedback samples based on weight
        for _ in range(int(feedback_weight)):
            combined_texts.append(text)
            combined_labels.append(label)
    
    print(f"\nCombined dataset:")
    print(f"  Original samples: {len(original_texts)}")
    print(f"  Feedback samples: {len(feedback_samples)}")
    print(f"  Weighted feedback: {int(feedback_weight) * len(feedback_samples)}")
    print(f"  Total samples: {len(combined_texts)}")
    
    return np.array(combined_texts), np.array(combined_labels)


def retrain_model(train_texts, train_labels, test_texts, test_labels, label_names, 
                  vectorizer=None, max_features=10000):
    """
    Retrain model with combined data.
    
    Args:
        train_texts: Training texts
        train_labels: Training labels
        test_texts: Test texts
        test_labels: Test labels
        label_names: Label names
        vectorizer: Existing vectorizer (if None, creates new one)
        max_features: Maximum features for TF-IDF
    
    Returns:
        Trained model, vectorizer, and metrics
    """
    print("\nTraining TF-IDF vectorizer...")
    if vectorizer is None:
        vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95
        )
        X_train = vectorizer.fit_transform(train_texts)
    else:
        # Use existing vectorizer vocabulary
        X_train = vectorizer.transform(train_texts)
    
    X_test = vectorizer.transform(test_texts)
    
    print(f"Feature matrix shape: {X_train.shape}")
    
    print("\nTraining Logistic Regression model...")
    model = LogisticRegression(
        max_iter=1000,
        random_state=42,
        C=1.0,
        solver='lbfgs'
    )
    
    model.fit(X_train, train_labels)
    
    # Evaluate
    print("\nEvaluating on test set...")
    test_pred = model.predict(X_test)
    
    test_acc = accuracy_score(test_labels, test_pred)
    test_f1 = f1_score(test_labels, test_pred, average='macro')
    
    print(f"\nTest Accuracy: {test_acc:.4f}")
    print(f"Test F1 (macro): {test_f1:.4f}")
    
    # Calculate detailed metrics
    metrics = calculate_metrics(test_labels, test_pred, label_names)
    
    # Print confusion matrix
    cm = confusion_matrix(test_labels, test_pred)
    print("\nConfusion Matrix:")
    print(cm)
    
    return model, vectorizer, metrics


def main(feedback_weight=1.0):
    """
    Main retraining function.
    
    Args:
        feedback_weight: Weight multiplier for feedback samples (default: 1.0)
    """
    print("=" * 60)
    print("RETRAINING WITH HUMAN FEEDBACK")
    print("=" * 60)
    
    # Get project root
    project_root = os.path.dirname(os.path.dirname(__file__))
    models_dir = os.path.join(project_root, 'models')
    feedback_path = os.path.join(project_root, 'data', 'feedback', 'feedback.json')
    metrics_dir = os.path.join(project_root, 'data', 'metrics')
    
    # Get current version and calculate next version
    current_version = get_current_model_version(models_dir)
    if current_version == 0:
        print("ERROR: No baseline model found. Please run train_baseline.py first.")
        return
    
    next_version = current_version + 1
    print(f"\nCurrent model version: v{current_version}")
    print(f"Training new model version: v{next_version}")
    
    # Load original data
    train_texts, train_labels, test_texts, test_labels, label_names = load_original_data()
    
    # Load feedback
    feedback_samples = load_feedback(feedback_path)
    
    if len(feedback_samples) == 0:
        print("\nWARNING: No feedback samples found. Model will be retrained on original data only.")
    
    # Combine datasets
    combined_texts, combined_labels = combine_datasets(
        train_texts, train_labels, feedback_samples, feedback_weight=feedback_weight
    )
    
    # Load existing vectorizer to maintain vocabulary
    vectorizer_path = os.path.join(models_dir, f'vectorizer_v{current_version}.joblib')
    vectorizer = None
    if os.path.exists(vectorizer_path):
        print(f"\nLoading existing vectorizer from v{current_version}...")
        vectorizer = joblib.load(vectorizer_path)
    
    # Retrain model
    model, vectorizer, metrics = retrain_model(
        combined_texts, combined_labels, test_texts, test_labels, label_names, vectorizer
    )
    
    # Save new model
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, f'model_v{next_version}.joblib')
    vectorizer_path = os.path.join(models_dir, f'vectorizer_v{next_version}.joblib')
    
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    
    print(f"\nModel saved to: {model_path}")
    print(f"Vectorizer saved to: {vectorizer_path}")
    
    # Save metrics
    os.makedirs(metrics_dir, exist_ok=True)
    save_metrics(metrics, version=next_version, metrics_dir=metrics_dir)
    
    # Update current model version marker (optional - can be handled by API)
    current_model_path = os.path.join(models_dir, 'current_version.txt')
    with open(current_model_path, 'w') as f:
        f.write(str(next_version))
    
    print("\n" + "=" * 60)
    print("RETRAINING COMPLETE")
    print("=" * 60)
    print(f"\nNew Model Version: v{next_version}")
    print(f"Test Accuracy: {metrics['accuracy']:.4f}")
    print(f"Test F1 (macro): {metrics['f1_macro']:.4f}")
    
    # Compare with baseline
    if current_version >= 1:
        from evaluation.metrics import load_metrics
        baseline_metrics = load_metrics(1, metrics_dir)
        if baseline_metrics:
            acc_improvement = metrics['accuracy'] - baseline_metrics['accuracy']
            f1_improvement = metrics['f1_macro'] - baseline_metrics['f1_macro']
            print(f"\nImprovement over baseline (v1):")
            print(f"  Accuracy: {acc_improvement:+.4f}")
            print(f"  F1 (macro): {f1_improvement:+.4f}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Retrain model with human feedback')
    parser.add_argument('--feedback-weight', type=float, default=1.0,
                       help='Weight multiplier for feedback samples (default: 1.0)')
    
    args = parser.parse_args()
    main(feedback_weight=args.feedback_weight)
