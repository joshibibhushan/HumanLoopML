"""
Visualization Module

Provides functions for creating performance plots and visualizations.
"""

import matplotlib.pyplot as plt
import numpy as np
from evaluation.metrics import load_metrics, compare_models


def plot_confusion_matrix(cm, label_names, title="Confusion Matrix", save_path=None):
    """
    Plot confusion matrix.
    
    Args:
        cm: Confusion matrix (numpy array or list)
        label_names: List of label names
        title: Plot title
        save_path: Optional path to save figure
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    
    # Set labels
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=label_names,
           yticklabels=label_names,
           title=title,
           ylabel='True Label',
           xlabel='Predicted Label')
    
    # Add text annotations
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], 'd'),
                   ha="center", va="center",
                   color="white" if cm[i, j] > thresh else "black")
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Confusion matrix saved to: {save_path}")
    
    return fig


def plot_performance_over_time(versions, metrics_dir, save_path=None):
    """
    Plot performance metrics over model versions.
    
    Args:
        versions: List of version numbers
        metrics_dir: Directory containing metrics
        save_path: Optional path to save figure
    """
    comparison = compare_models(versions, metrics_dir)
    
    if not comparison:
        print("No metrics found to plot")
        return None
    
    version_labels = list(comparison.keys())
    accuracies = [comparison[v]['accuracy'] for v in version_labels]
    f1_scores = [comparison[v]['f1_macro'] for v in version_labels]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Accuracy plot
    ax1.plot(version_labels, accuracies, marker='o', linewidth=2, markersize=8)
    ax1.set_xlabel('Model Version')
    ax1.set_ylabel('Accuracy')
    ax1.set_title('Accuracy Over Time')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([0, 1])
    
    # F1 Score plot
    ax2.plot(version_labels, f1_scores, marker='s', linewidth=2, markersize=8, color='orange')
    ax2.set_xlabel('Model Version')
    ax2.set_ylabel('F1 Score (Macro)')
    ax2.set_title('F1 Score Over Time')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim([0, 1])
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Performance plot saved to: {save_path}")
    
    return fig


def plot_before_after_comparison(baseline_version, improved_version, metrics_dir, save_path=None):
    """
    Plot before/after comparison of two model versions.
    
    Args:
        baseline_version: Baseline model version number
        improved_version: Improved model version number
        metrics_dir: Directory containing metrics
        save_path: Optional path to save figure
    """
    baseline_metrics = load_metrics(baseline_version, metrics_dir)
    improved_metrics = load_metrics(improved_version, metrics_dir)
    
    if not baseline_metrics or not improved_metrics:
        print("Metrics not found for comparison")
        return None
    
    metrics_to_compare = ['accuracy', 'f1_macro', 'f1_weighted']
    baseline_values = [baseline_metrics[m] for m in metrics_to_compare]
    improved_values = [improved_metrics[m] for m in metrics_to_compare]
    
    x = np.arange(len(metrics_to_compare))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars1 = ax.bar(x - width/2, baseline_values, width, label=f'Baseline (v{baseline_version})', alpha=0.8)
    bars2 = ax.bar(x + width/2, improved_values, width, label=f'Improved (v{improved_version})', alpha=0.8)
    
    ax.set_ylabel('Score')
    ax.set_title('Model Performance: Before vs After Feedback')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_to_compare)
    ax.legend()
    ax.set_ylim([0, 1])
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}',
                   ha='center', va='bottom')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Comparison plot saved to: {save_path}")
    
    return fig
