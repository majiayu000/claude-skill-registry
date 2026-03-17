---
name: model-evaluation
description: Evaluates machine learning models for performance, fairness, and reliability using appropriate metrics and validation techniques. Covers training debugging, hyperparameter tuning, and production monitoring. Trigger keywords: model evaluation, metrics, accuracy, precision, recall, F1, F1-score, ROC, AUC, ROC-AUC, confusion matrix, cross-validation, k-fold, stratified, overfitting, underfitting, bias, variance, bias-variance tradeoff, hyperparameter, hyperparameter tuning, loss, loss function, metric, benchmark, benchmarking, model performance, classification metrics, regression metrics, RMSE, MSE, MAE, MAPE, R2, R-squared, train-test split, validation set, test set, hold-out, learning curve, validation curve, model selection, error analysis, residual analysis, ML testing, training issues, convergence, gradient, vanishing gradient, exploding gradient, training instability, LLM evaluation, language model evaluation, prompt engineering evaluation, A/B testing, champion-challenger, model monitoring, model drift, data drift, concept drift, model decay.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Model Evaluation

## Overview

This skill focuses on comprehensive evaluation of machine learning models across the entire ML lifecycle. It covers metric selection, validation strategies, fairness assessment, training debugging, hyperparameter tuning, LLM evaluation, A/B testing, and production monitoring for ensuring model quality and reliability.

## When to Use This Skill

Use this skill when you need to:

- Select and compute appropriate evaluation metrics for ML models
- Design cross-validation strategies and train/test splits
- Debug training issues (overfitting, underfitting, convergence problems)
- Tune hyperparameters and validate model improvements
- Evaluate LLMs and generative models
- Conduct A/B tests for model comparison in production
- Monitor deployed models for drift and degradation
- Assess model fairness across demographic groups
- Analyze error patterns and residuals
- Create evaluation reports and dashboards

## Related Skills and Agents

**When to Escalate:**

- **senior-software-engineer (Opus)**: For ML system architecture decisions, model selection strategies, complex evaluation pipeline design, distributed evaluation infrastructure, large-scale benchmarking, production monitoring architecture, adversarial robustness evaluation, model poisoning detection, security-aware metrics (use /security-audit and /threat-model skills for security concerns)

**Complementary Skills:**

- Use `/debugging` for systematic debugging of evaluation pipelines and metric computation issues
- Use `/testing` for unit testing evaluation code and validation logic
- Use `/data-validation` for input data quality checks before model evaluation

## Instructions

### 1. Define Evaluation Criteria

**Business Alignment:**

- Identify business objectives and success criteria
- Translate business goals to ML metrics
- Define acceptable performance thresholds
- Consider cost of different error types (false positives vs false negatives)

**Metric Selection:**

- Classification: accuracy, precision, recall, F1, ROC-AUC, PR-AUC
- Regression: MSE, RMSE, MAE, MAPE, R2, explained variance
- Ranking: NDCG, MAP, MRR
- LLMs: perplexity, BLEU, ROUGE, BERTScore, human eval
- Custom metrics for domain-specific requirements

**Fairness Requirements:**

- Identify protected attributes (race, gender, age)
- Choose fairness definitions (demographic parity, equalized odds)
- Set fairness constraints and thresholds

### 2. Design Evaluation Strategy

**Data Splitting:**

- Train/validation/test split ratios (e.g., 60/20/20)
- Stratified splits for class imbalance
- Time-based splits for temporal data
- Group-based splits to prevent data leakage

**Cross-Validation:**

- K-fold CV for standard problems
- Stratified K-fold for imbalanced classes
- TimeSeriesSplit for temporal data
- GroupKFold for clustered data
- Leave-one-out for small datasets

**Handling Imbalance:**

- Stratified sampling
- Class weights in metrics
- Resampling strategies (SMOTE, undersampling)
- Appropriate metrics (F1, PR-AUC instead of accuracy)

### 3. Conduct Evaluation

**Performance Metrics:**

- Calculate primary and secondary metrics
- Compute confidence intervals
- Compare against baselines
- Statistical significance testing

**Error Analysis:**

- Confusion matrix analysis
- Per-class performance breakdown
- Error type categorization
- Hard example mining

**Fairness Assessment:**

- Group-wise metric comparison
- Demographic parity evaluation
- Equalized odds analysis
- Disparate impact measurement

**Edge Case Testing:**

- Boundary condition validation
- Out-of-distribution detection
- Adversarial robustness
- Stress testing with extreme inputs

### 4. Debug Training Issues

**Overfitting Detection:**

- Train vs validation performance gap
- Learning curves analysis
- Validation metrics plateauing while training improves
- Mitigation: regularization, dropout, early stopping, data augmentation

**Underfitting Detection:**

- Poor performance on both train and validation
- Learning curves not converging
- Model too simple for problem complexity
- Mitigation: increase model capacity, feature engineering, longer training

**Convergence Problems:**

- Loss not decreasing
- Loss oscillating or unstable
- Exploding gradients (loss becomes NaN)
- Vanishing gradients (loss stays constant)
- Mitigation: learning rate tuning, gradient clipping, batch normalization

**Learning Rate Issues:**

- Too high: training unstable, loss oscillates
- Too low: training too slow, stuck in local minima
- Solution: learning rate schedules, warmup, cosine annealing

**Batch Size Effects:**

- Small batch: noisy gradients, poor generalization
- Large batch: memory issues, sharp minima
- Find sweet spot through experimentation

### 5. Hyperparameter Tuning

**Search Strategies:**

- Grid search: exhaustive but expensive
- Random search: better coverage for high-dimensional spaces
- Bayesian optimization: sample efficient
- Hyperband: adaptive resource allocation

**Key Hyperparameters:**

- Learning rate (most critical)
- Batch size
- Regularization strength (L1, L2, dropout)
- Network architecture (layers, units)
- Optimizer choice (Adam, SGD, AdamW)

**Validation:**

- Use validation set for hyperparameter selection
- Never tune on test set
- Consider nested cross-validation for small datasets

### 6. LLM and Generative Model Evaluation

**Automatic Metrics:**

- Perplexity for language models
- BLEU, ROUGE for text generation
- BERTScore for semantic similarity
- Exact match, F1 for QA tasks

**Human Evaluation:**

- Fluency, coherence, relevance
- Factual accuracy
- Safety and toxicity
- Instruction following

**Prompt Engineering Evaluation:**

- Few-shot vs zero-shot comparison
- Prompt template A/B testing
- Chain-of-thought effectiveness
- System message impact

**LLM-as-Judge:**

- Use stronger models to evaluate weaker models
- Pairwise comparison for ranking
- Rubric-based scoring
- Calibration against human judgments

### 7. A/B Testing for Model Comparison

**Experimental Design:**

- Random traffic split (50/50 or 90/10)
- Minimum sample size calculation
- Statistical power analysis
- Duration planning for seasonality

**Metrics:**

- Primary business metric (conversion, revenue)
- Secondary metrics (latency, user satisfaction)
- Guardrail metrics (error rate, bias)
- Sample ratio mismatch checks

**Analysis:**

- Statistical significance testing (t-test, Mann-Whitney)
- Effect size estimation
- Confidence intervals
- Multiple testing correction (Bonferroni)

**Decision Criteria:**

- Primary metric improvement threshold
- No degradation in guardrail metrics
- Sufficient statistical power
- Business case validation

### 8. Production Model Monitoring

**Performance Monitoring:**

- Track key metrics over time
- Compare against baseline/champion model
- Detect performance degradation
- Alert on threshold violations

**Data Drift Detection:**

- Input distribution shifts
- Feature statistics tracking
- KL divergence, KS test, PSI
- Covariate shift detection

**Concept Drift Detection:**

- Model prediction distribution changes
- Label distribution shifts (when available)
- Performance metric trends
- Adversarial Validation

**Monitoring Infrastructure:**

- Real-time metric computation
- Dashboards for visualization
- Alerting and on-call rotation
- Automated retraining triggers

### 9. Report and Document

**Evaluation Report Structure:**

- Executive summary with key findings
- Methodology and experimental setup
- Comprehensive metric tables
- Error analysis and case studies
- Fairness assessment results
- Recommendations and next steps

**Visualization:**

- ROC and PR curves
- Confusion matrices
- Learning curves
- Residual plots
- Fairness comparison charts

**Version Control:**

- Model version and checkpoints
- Dataset versions and splits
- Hyperparameter configurations
- Evaluation code and environment

## Best Practices

### General Principles

1. **Match Metrics to Goals**: Choose metrics aligned with business objectives, not just academic standards
2. **Use Multiple Metrics**: No single metric tells the whole story; use complementary metrics
3. **Proper Validation**: Use appropriate cross-validation schemes to avoid overfitting to validation set
4. **Test Distribution Shift**: Evaluate on out-of-distribution data to assess generalization
5. **Check for Bias**: Assess fairness across demographic groups before deployment
6. **Version Everything**: Track models, data, metrics, and code for reproducibility
7. **Monitor Production**: Continuously track model performance after deployment

### Training and Debugging

1. **Start Simple**: Begin with simple baselines before complex models
2. **Visualize Learning**: Plot learning curves early and often
3. **Debug Incrementally**: Change one thing at a time when debugging training issues
4. **Sanity Check**: Overfit on small batch first to verify model can learn
5. **Early Stopping**: Use validation-based early stopping to prevent overfitting
6. **Gradient Monitoring**: Track gradient norms to detect vanishing/exploding gradients

### Evaluation Rigor

1. **Hold-out Test Set**: Never touch test set until final evaluation
2. **Stratified Splits**: Use stratification for imbalanced datasets
3. **Statistical Testing**: Use significance tests for model comparisons
4. **Error Analysis**: Dive deep into errors to understand failure modes
5. **Temporal Validation**: For time-series, validate on future data only

### Production and Monitoring

1. **Shadow Mode**: Deploy new models in shadow mode before switching traffic
2. **Gradual Rollout**: Use canary deployments or gradual percentage rollouts
3. **Rollback Plan**: Have automated rollback triggers for performance degradation
4. **Alert Fatigue**: Set meaningful alert thresholds to avoid noise

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
    print(f"  Overfitting gap: {values['overfit_gap']:.4f}")
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

### Example 5: Training Debugging with Learning Curves

```python
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve

def plot_learning_curves(model, X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 10)):
    """
    Plot learning curves to diagnose overfitting/underfitting.

    Args:
        model: Sklearn-compatible model
        X: Features
        y: Target
        cv: Cross-validation folds
        train_sizes: Array of training set size fractions
    """
    train_sizes, train_scores, val_scores = learning_curve(
        model, X, y,
        cv=cv,
        train_sizes=train_sizes,
        scoring='accuracy',
        n_jobs=-1
    )

    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    val_mean = np.mean(val_scores, axis=1)
    val_std = np.std(val_scores, axis=1)

    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_mean, label='Training score', color='blue', marker='o')
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.15, color='blue')
    plt.plot(train_sizes, val_mean, label='Validation score', color='red', marker='o')
    plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.15, color='red')

    plt.xlabel('Training Set Size')
    plt.ylabel('Accuracy')
    plt.title('Learning Curves')
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)

    # Add diagnostic annotations
    final_gap = train_mean[-1] - val_mean[-1]
    if final_gap > 0.1:
        plt.text(0.5, 0.05, 'HIGH OVERFITTING: Large gap between train and validation',
                 transform=plt.gca().transAxes, color='red', fontweight='bold')
    elif val_mean[-1] < 0.7:
        plt.text(0.5, 0.05, 'UNDERFITTING: Both train and validation scores are low',
                 transform=plt.gca().transAxes, color='orange', fontweight='bold')

    plt.tight_layout()
    plt.show()

    return {
        'final_train_score': train_mean[-1],
        'final_val_score': val_mean[-1],
        'overfit_gap': final_gap
    }
```

### Example 6: LLM Evaluation

```python
from typing import List, Dict
import openai

def evaluate_llm_generation(
    prompts: List[str],
    references: List[str],
    model: str,
    judge_model: str = "gpt-4"
) -> Dict:
    """
    Evaluate LLM generation quality using LLM-as-judge.

    Args:
        prompts: Input prompts
        references: Reference outputs (if available)
        model: Model to evaluate
        judge_model: Model to use as judge

    Returns:
        Dictionary with evaluation scores
    """
    results = []

    for prompt, reference in zip(prompts, references):
        # Generate response
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        generation = response.choices[0].message.content

        # LLM-as-judge evaluation
        judge_prompt = f"""Evaluate the following AI-generated response on a scale of 1-5 for:
1. Accuracy: Is the information correct?
2. Relevance: Does it address the prompt?
3. Fluency: Is it well-written and coherent?
4. Helpfulness: Is it useful to the user?

Prompt: {prompt}
Reference (if available): {reference}
Response: {generation}

Provide scores in JSON format: {{"accuracy": X, "relevance": X, "fluency": X, "helpfulness": X, "overall": X}}
"""

        judge_response = openai.ChatCompletion.create(
            model=judge_model,
            messages=[{"role": "user", "content": judge_prompt}]
        )

        scores = json.loads(judge_response.choices[0].message.content)
        results.append({
            'prompt': prompt,
            'generation': generation,
            'scores': scores
        })

    # Aggregate scores
    avg_scores = {}
    for key in ['accuracy', 'relevance', 'fluency', 'helpfulness', 'overall']:
        avg_scores[key] = np.mean([r['scores'][key] for r in results])

    return {
        'individual_results': results,
        'average_scores': avg_scores
    }
```

### Example 7: A/B Test Analysis

```python
from scipy import stats

def analyze_ab_test(control_metric: np.ndarray, treatment_metric: np.ndarray, alpha: float = 0.05):
    """
    Analyze A/B test results with statistical significance testing.

    Args:
        control_metric: Metric values for control group
        treatment_metric: Metric values for treatment group
        alpha: Significance level

    Returns:
        Dictionary with test results
    """
    # Descriptive statistics
    control_mean = np.mean(control_metric)
    treatment_mean = np.mean(treatment_metric)
    relative_lift = (treatment_mean - control_mean) / control_mean * 100

    # Statistical test
    t_stat, p_value = stats.ttest_ind(treatment_metric, control_metric)
    is_significant = p_value < alpha

    # Effect size (Cohen's d)
    pooled_std = np.sqrt((np.std(control_metric)**2 + np.std(treatment_metric)**2) / 2)
    cohens_d = (treatment_mean - control_mean) / pooled_std

    # Confidence interval
    ci = stats.t.interval(
        confidence=1-alpha,
        df=len(control_metric) + len(treatment_metric) - 2,
        loc=treatment_mean - control_mean,
        scale=stats.sem(np.concatenate([control_metric, treatment_metric]))
    )

    return {
        'control_mean': control_mean,
        'treatment_mean': treatment_mean,
        'relative_lift_pct': relative_lift,
        'p_value': p_value,
        'is_significant': is_significant,
        'cohens_d': cohens_d,
        'confidence_interval': ci,
        'recommendation': 'LAUNCH' if is_significant and relative_lift > 0 else 'DO NOT LAUNCH'
    }

# Usage
results = analyze_ab_test(control_conversions, treatment_conversions)
print(f"Relative Lift: {results['relative_lift_pct']:.2f}%")
print(f"P-value: {results['p_value']:.4f}")
print(f"Recommendation: {results['recommendation']}")
```

### Example 8: Production Model Monitoring

```python
from scipy.stats import ks_2samp
import pandas as pd

class ModelMonitor:
    """Monitor deployed model for drift and degradation."""

    def __init__(self, baseline_data: pd.DataFrame, baseline_predictions: np.ndarray):
        self.baseline_data = baseline_data
        self.baseline_predictions = baseline_predictions

    def detect_data_drift(self, current_data: pd.DataFrame, threshold: float = 0.05) -> Dict:
        """Detect feature distribution drift using KS test."""
        drift_results = {}

        for col in self.baseline_data.columns:
            if pd.api.types.is_numeric_dtype(self.baseline_data[col]):
                statistic, p_value = ks_2samp(
                    self.baseline_data[col].dropna(),
                    current_data[col].dropna()
                )
                drift_results[col] = {
                    'ks_statistic': statistic,
                    'p_value': p_value,
                    'drift_detected': p_value < threshold
                }

        return drift_results

    def detect_prediction_drift(self, current_predictions: np.ndarray, threshold: float = 0.05) -> Dict:
        """Detect prediction distribution drift."""
        statistic, p_value = ks_2samp(self.baseline_predictions, current_predictions)

        return {
            'ks_statistic': statistic,
            'p_value': p_value,
            'drift_detected': p_value < threshold,
            'baseline_mean': np.mean(self.baseline_predictions),
            'current_mean': np.mean(current_predictions),
            'mean_shift': np.mean(current_predictions) - np.mean(self.baseline_predictions)
        }

    def performance_degradation_check(
        self,
        current_metric: float,
        baseline_metric: float,
        threshold_pct: float = 5.0
    ) -> Dict:
        """Check for performance degradation."""
        degradation_pct = (baseline_metric - current_metric) / baseline_metric * 100

        return {
            'baseline_metric': baseline_metric,
            'current_metric': current_metric,
            'degradation_pct': degradation_pct,
            'alert': degradation_pct > threshold_pct,
            'recommendation': 'RETRAIN MODEL' if degradation_pct > threshold_pct else 'OK'
        }

# Usage
monitor = ModelMonitor(baseline_df, baseline_preds)
drift_check = monitor.detect_data_drift(current_df)
pred_drift = monitor.detect_prediction_drift(current_preds)
perf_check = monitor.performance_degradation_check(current_accuracy, baseline_accuracy)
```

## Common Pitfalls

1. **Test Set Contamination**: Never use test set for hyperparameter tuning or model selection
2. **Data Leakage**: Ensure validation/test data doesn't leak into training (temporal ordering, group splits)
3. **Wrong Metric Choice**: Using accuracy for imbalanced datasets, not considering business costs
4. **Ignoring Confidence Intervals**: Point estimates without uncertainty can be misleading
5. **Multiple Comparisons**: Not correcting p-values when testing many hypotheses
6. **Survivorship Bias**: Evaluating only on successful cases, ignoring failures
7. **Overfitting to Validation**: Repeatedly tuning on validation set effectively makes it a second training set
8. **Ignoring Fairness**: Deploying models without fairness evaluation can cause harm
9. **No Baseline**: Not comparing against simple baselines (random, majority class, linear model)
10. **Production-Training Skew**: Evaluation setup doesn't match production environment

## Additional Resources

- **Metrics**: Scikit-learn metrics documentation, Hugging Face evaluate library
- **Fairness**: AI Fairness 360, Fairlearn
- **LLM Evaluation**: HELM, lm-evaluation-harness, BIG-bench
- **A/B Testing**: Evan Miller's A/B testing tools, experimentation platform docs
- **Monitoring**: Evidently AI, WhyLabs, Fiddler
