---
name: model-evaluation
description: 'Evaluates machine learning models for performance, fairness, and reliability
  using appropriate metrics and validation techniques. Trigger keywords: model evaluation,
  metrics, accuracy, precision, reca'
---

---
name: model-evaluation
description: Evaluates machine learning models for performance, fairness, and reliability using appropriate metrics and validation techniques. Trigger keywords: model evaluation, metrics, accuracy, precision, recall, F1, ROC, AUC, cross-validation, ML testing.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Model Evaluation

## Overview

This skill focuses on comprehensive evaluation of machine learning models. It covers metric selection, validation strategies, fairness assessment, and production monitoring for ensuring model quality and reliability.

## Instructions

### 1. Define Evaluation Criteria

- Identify business objectives
- Select appropriate metrics
- Define success thresholds
- Consider fairness requirements

### 2. Design Evaluation Strategy

- Choose validation approach
- Plan for data splits
- Handle class imbalance
- Account for temporal aspects

### 3. Conduct Evaluation

- Calculate performance metrics
- Analyze error patterns
- Assess model fairness
- Test edge cases

### 4. Report and Monitor

- Document evaluation results
- Create monitoring dashboards
- Set up alerting thresholds
- Plan for retraining

## Best Practices

1. **Match Metrics to Goals**: Choose metrics aligned with business objectives
2. **Use Multiple Metrics**: No single metric tells the whole story
3. **Proper Validation**: Use appropriate cross-validation schemes
4. **Test Distribution Shift**: Evaluate on out-of-distribution data
5. **Check for Bias**: Assess fairness across demographic groups
6. **Version Everything**: Track models, data, and metrics
7. **Monitor Production**: Continuously track model performance

## Examples

### Example 1: Classification Model Evaluation

```python
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    classification_report, roc_curve, precision_recall_curve
)
import matplotlib.pyplot as plt

class ClassificationEvaluator:
    """Comprehensive classification model evaluator."""

    def __init__(self, y_true, y_pred, y_prob=None, class_names=None):
        self.y_true = y_true
        self.y_pred = y_pred
        self.y_prob = y_prob
        self.class_names = class_names or ['Negative', 'Positive']

    def compute_metrics(self) -> dict:
        """Compute all classification metrics."""
        metrics = {
            'accuracy': accuracy_score(self.y_true, self.y_pred),
            'precision': precision_score(self.y_true, self.y_pred, average='weighted'),
            'recall': recall_score(self.y_true, self.y_pred, average='weighted'),
            'f1': f1_score(self.y_true, self.y_pred, average='weighted'),
        }

        if self.y_prob is not None:
            metrics['roc_auc'] = roc_auc_score(self.y_true, self.y_prob)
            metrics['average_precision'] = average_precision_score(self.y_true, self.y_prob)

        return metrics

    def confusion_matrix_analysis(self) -> dict:
        """Analyze confusion matrix in detail."""
        cm = confusion_matrix(self.y_true, self.y_pred)
        tn, fp, fn, tp = cm.ravel()

        return {
            'confusion_matrix': cm,
            'true_negatives': tn,
            'false_positives': fp,
            'false_negatives': fn,
            'true_positives': tp,
            'specificity': tn / (tn + fp),
            'sensitivity': tp / (tp + fn),
            'false_positive_rate': fp / (fp + tn),
            'false_negative_rate': fn / (fn + tp),
        }

    def plot_roc_curve(self, save_path=None):
        """Plot ROC curve with AUC."""
        if self.y_prob is None:
            raise ValueError("Probabilities required for ROC curve")

        fpr, tpr, thresholds = roc_curve(self.y_true, self.y_prob)
        auc = roc_auc_score(self.y_true, self.y_prob)

        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, label=f'ROC (AUC = {auc:.3f})')
        plt.plot([0, 1], [0, 1], 'k--', label='Random')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend()
        plt.grid(True, alpha=0.3)

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show()

    def generate_report(self) -> str:
        """Generate comprehensive evaluation report."""
        metrics = self.compute_metrics()
        cm_analysis = self.confusion_matrix_analysis()

        report = f"""
# Classification Model Evaluation Report

## Overall Metrics
| Metric | Value |
|--------|-------|
| Accuracy | {metrics['accuracy']:.4f} |
| Precision | {metrics['precision']:.4f} |
| Recall | {metrics['recall']:.4f} |
| F1 Score | {metrics['f1']:.4f} |
| ROC AUC | {metrics.get('roc_auc', 'N/A'):.4f if isinstance(metrics.get('roc_auc'), float) else 'N/A'} |

## Confusion Matrix Analysis
| Metric | Value |
|--------|-------|
| True Positives | {cm_analysis['true_positives']} |
| True Negatives | {cm_analysis['true_negatives']} |
| False Positives | {cm_analysis['false_positives']} |
| False Negatives | {cm_analysis['false_negatives']} |
| Sensitivity | {cm_analysis['sensitivity']:.4f} |
| Specificity | {cm_analysis['specificity']:.4f} |

## Detailed Classification Report
{classification_report(self.y_true, self.y_pred, target_names=self.class_names)}
"""
        return report

# Usage
evaluator = ClassificationEvaluator(y_true, y_pred, y_prob)
print(evaluator.generate_report())
evaluator.plot_roc_curve('roc_curve.png')
```

### Example 2: Regression Model Evaluation

```python
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    mean_absolute_percentage_error, explained_variance_score
)
import numpy as np

class RegressionEvaluator:
    """Comprehensive regression model evaluator."""

    def __init__(self, y_true, y_pred):
        self.y_true = np.array(y_true)
        self.y_pred = np.array(y_pred)
        self.residuals = self.y_true - self.y_pred

    def compute_metrics(self) -> dict:
        """Compute all regression metrics."""
        mse = mean_squared_error(self.y_true, self.y_pred)

        return {
            'mse': mse,
            'rmse': np.sqrt(mse),
            'mae': mean_absolute_error(self.y_true, self.y_pred),
            'mape': mean_absolute_percentage_error(self.y_true, self.y_pred) * 100,
            'r2': r2_score(self.y_true, self.y_pred),
            'explained_variance': explained_variance_score(self.y_true, self.y_pred),
        }

    def residual_analysis(self) -> dict:
        """Analyze residual patterns."""
        return {
            'mean_residual': np.mean(self.residuals),
            'std_residual': np.std(self.residuals),
            'max_overestimate': np.min(self.residuals),
            'max_underestimate': np.max(self.residuals),
            'residual_skewness': self._skewness(self.residuals),
        }

    def _skewness(self, data):
        """Calculate skewness."""
        n = len(data)
        mean = np.mean(data)
        std = np.std(data)
        return (n / ((n-1) * (n-2))) * np.sum(((data - mean) / std) ** 3)

    def plot_diagnostics(self, save_path=None):
        """Plot diagnostic plots for residual analysis."""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        # Actual vs Predicted
        ax1 = axes[0, 0]
        ax1.scatter(self.y_true, self.y_pred, alpha=0.5)
        ax1.plot([self.y_true.min(), self.y_true.max()],
                 [self.y_true.min(), self.y_true.max()], 'r--')
        ax1.set_xlabel('Actual')
        ax1.set_ylabel('Predicted')
        ax1.set_title('Actual vs Predicted')

        # Residuals vs Predicted
        ax2 = axes[0, 1]
        ax2.scatter(self.y_pred, self.residuals, alpha=0.5)
        ax2.axhline(y=0, color='r', linestyle='--')
        ax2.set_xlabel('Predicted')
        ax2.set_ylabel('Residuals')
        ax2.set_title('Residuals vs Predicted')

        # Residual histogram
        ax3 = axes[1, 0]
        ax3.hist(self.residuals, bins=30, edgecolor='black')
        ax3.set_xlabel('Residual')
        ax3.set_ylabel('Frequency')
        ax3.set_title('Residual Distribution')

        # Q-Q plot
        ax4 = axes[1, 1]
        from scipy import stats
        stats.probplot(self.residuals, dist="norm", plot=ax4)
        ax4.set_title('Q-Q Plot')

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show()
```

### Example 3: Cross-Validation Strategies

```python
from sklearn.model_selection import (
    cross_val_score, StratifiedKFold, TimeSeriesSplit,
    GroupKFold, cross_validate
)

def evaluate_with_cv(model, X, y, cv_strategy='stratified', n_splits=5, groups=None):
    """
    Evaluate model with appropriate cross-validation strategy.

    Args:
        model: Sklearn-compatible model
        X: Features
        y: Target
        cv_strategy: 'stratified', 'timeseries', 'group', or 'kfold'
        n_splits: Number of CV folds
        groups: Group labels for GroupKFold

    Returns:
        Dictionary with CV results
    """
    # Select CV strategy
    if cv_strategy == 'stratified':
        cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    elif cv_strategy == 'timeseries':
        cv = TimeSeriesSplit(n_splits=n_splits)
    elif cv_strategy == 'group':
        cv = GroupKFold(n_splits=n_splits)
    else:
        cv = n_splits

    # Define scoring metrics
    scoring = {
        'accuracy': 'accuracy',
        'precision': 'precision_weighted',
        'recall': 'recall_weighted',
        'f1': 'f1_weighted',
        'roc_auc': 'roc_auc'
    }

    # Perform cross-validation
    cv_results = cross_validate(
        model, X, y,
        cv=cv,
        scoring=scoring,
        groups=groups,
        return_train_score=True,
        n_jobs=-1
    )

    # Summarize results
    summary = {}
    for metric in scoring.keys():
        test_scores = cv_results[f'test_{metric}']
        train_scores = cv_results[f'train_{metric}']
        summary[metric] = {
            'test_mean': np.mean(test_scores),
            'test_std': np.std(test_scores),
            'train_mean': np.mean(train_scores),
            'train_std': np.std(train_scores),
            'overfit_gap': np.mean(train_scores) - np.mean(test_scores)
        }

    return summary

# Usage example
results = evaluate_with_cv(model, X, y, cv_strategy='stratified', n_splits=5)
for metric, values in results.items():
    print(f"{metric}: {values['test_mean']:.4f} (+/- {values['test_std']:.4f})")
```

### Example 4: Fairness Evaluation

```python
def evaluate_fairness(y_true, y_pred, sensitive_attr, favorable_label=1):
    """
    Evaluate model fairness across demographic groups.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        sensitive_attr: Protected attribute values
        favorable_label: The favorable outcome label

    Returns:
        Dictionary with fairness metrics
    """
    groups = np.unique(sensitive_attr)
    results = {'group_metrics': {}}

    for group in groups:
        mask = sensitive_attr == group
        group_true = y_true[mask]
        group_pred = y_pred[mask]

        # Calculate group-specific metrics
        tp = np.sum((group_true == favorable_label) & (group_pred == favorable_label))
        fp = np.sum((group_true != favorable_label) & (group_pred == favorable_label))
        fn = np.sum((group_true == favorable_label) & (group_pred != favorable_label))
        tn = np.sum((group_true != favorable_label) & (group_pred != favorable_label))

        results['group_metrics'][group] = {
            'selection_rate': np.mean(group_pred == favorable_label),
            'tpr': tp / (tp + fn) if (tp + fn) > 0 else 0,
            'fpr': fp / (fp + tn) if (fp + tn) > 0 else 0,
            'accuracy': np.mean(group_true == group_pred),
            'size': len(group_true)
        }

    # Calculate fairness metrics
    selection_rates = [m['selection_rate'] for m in results['group_metrics'].values()]
    tprs = [m['tpr'] for m in results['group_metrics'].values()]
    fprs = [m['fpr'] for m in results['group_metrics'].values()]

    results['fairness_metrics'] = {
        'demographic_parity_diff': max(selection_rates) - min(selection_rates),
        'equalized_odds_tpr_diff': max(tprs) - min(tprs),
        'equalized_odds_fpr_diff': max(fprs) - min(fprs),
    }

    return results
```
