"""
Baseline Model Training Script

Trains a TF-IDF + Logistic Regression model on the AG News dataset.
Saves the model as version 1 and baseline metrics.
"""

import os
import sys
import json
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
import datasets

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from evaluation.metrics import calculate_metrics, save_metrics


def load_ag_news():
    """Load AG News dataset from HuggingFace datasets."""
    print("Loading AG News dataset...")
    dataset = datasets.load_dataset("ag_news")
    
    # Extract texts and labels
    train_texts = dataset['train']['text']
    train_labels = dataset['train']['label']
    test_texts = dataset['test']['text']
    test_labels = dataset['test']['label']
    
    # AG News label mapping
    label_names = ['World', 'Sports', 'Business', 'Sci/Tech']
    
    print(f"Training samples: {len(train_texts)}")
    print(f"Test samples: {len(test_texts)}")
    
    return train_texts, train_labels, test_texts, test_labels, label_names


def train_baseline_model(train_texts, train_labels, test_texts, test_labels, label_names):
    """Train TF-IDF + Logistic Regression baseline model."""
    
    print("\nTraining TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )
    
    X_train = vectorizer.fit_transform(train_texts)
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
    
    # Make predictions
    print("\nEvaluating on test set...")
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    
    train_acc = accuracy_score(train_labels, train_pred)
    test_acc = accuracy_score(test_labels, test_pred)
    
    train_f1 = f1_score(train_labels, train_pred, average='macro')
    test_f1 = f1_score(test_labels, test_pred, average='macro')
    
    print(f"\nTraining Accuracy: {train_acc:.4f}")
    print(f"Test Accuracy: {test_acc:.4f}")
    print(f"Training F1 (macro): {train_f1:.4f}")
    print(f"Test F1 (macro): {test_f1:.4f}")
    
    # Calculate detailed metrics
    metrics = calculate_metrics(test_labels, test_pred, label_names)
    
    # Print confusion matrix
    cm = confusion_matrix(test_labels, test_pred)
    print("\nConfusion Matrix:")
    print(cm)
    
    # Print classification report
    print("\nClassification Report:")
    print(classification_report(test_labels, test_pred, target_names=label_names))
    
    return model, vectorizer, metrics


def save_model(model, vectorizer, version=1):
    """Save model and vectorizer to disk."""
    model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    os.makedirs(model_dir, exist_ok=True)
    
    model_path = os.path.join(model_dir, f'model_v{version}.joblib')
    vectorizer_path = os.path.join(model_dir, f'vectorizer_v{version}.joblib')
    
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    
    print(f"\nModel saved to: {model_path}")
    print(f"Vectorizer saved to: {vectorizer_path}")
    
    return model_path, vectorizer_path


def main():
    """Main training function."""
    print("=" * 60)
    print("BASELINE MODEL TRAINING")
    print("=" * 60)
    
    # Load data
    train_texts, train_labels, test_texts, test_labels, label_names = load_ag_news()
    
    # Train model
    model, vectorizer, metrics = train_baseline_model(
        train_texts, train_labels, test_texts, test_labels, label_names
    )
    
    # Save model
    model_path, vectorizer_path = save_model(model, vectorizer, version=1)
    
    # Save metrics
    metrics_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'metrics')
    os.makedirs(metrics_dir, exist_ok=True)
    save_metrics(metrics, version=1, metrics_dir=metrics_dir)
    
    # Save label names for reference
    label_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'label_names.json')
    with open(label_path, 'w') as f:
        json.dump(label_names, f)
    
    print("\n" + "=" * 60)
    print("BASELINE TRAINING COMPLETE")
    print("=" * 60)
    print(f"\nModel Version: v1")
    print(f"Test Accuracy: {metrics['accuracy']:.4f}")
    print(f"Test F1 (macro): {metrics['f1_macro']:.4f}")


if __name__ == "__main__":
    main()
