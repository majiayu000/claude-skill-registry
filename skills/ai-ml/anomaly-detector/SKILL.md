---
name: anomaly-detector
description: |
  Anomaly and outlier detection using Isolation Forest, One-Class SVM, autoencoders, and statistical methods. Activates for "anomaly detection", "outlier detection", "fraud detection", "intrusion detection", "abnormal behavior", "unusual patterns", "detect anomalies", "system monitoring". Handles supervised and unsupervised anomaly detection with SpecWeave increment integration.
---

# Anomaly Detector

## Overview

Detect unusual patterns, outliers, and anomalies in data using statistical methods, machine learning, and deep learning. Critical for fraud detection, security monitoring, quality control, and system health monitoring—all integrated with SpecWeave's increment workflow.

## Why Anomaly Detection is Different

**Challenge**: Anomalies are rare (0.1% - 5% of data)

**Standard classification doesn't work**:
- ❌ Extreme class imbalance
- ❌ Unknown anomaly patterns
- ❌ Expensive to label anomalies
- ❌ Anomalies evolve over time

**Anomaly detection approaches**:
- ✅ Unsupervised (no labels needed)
- ✅ Semi-supervised (learn from normal data)
- ✅ Statistical (deviation from expected)
- ✅ Context-aware (what's normal for this user/time/location?)

## Anomaly Detection Methods

### 1. Statistical Methods (Baseline)

**Z-Score / Standard Deviation**:
```python
from specweave import AnomalyDetector

detector = AnomalyDetector(
    method="statistical",
    increment="0042"
)

# Flag values > 3 standard deviations from mean
anomalies = detector.detect(
    data=transaction_amounts,
    threshold=3.0
)

# Simple, fast, but assumes normal distribution
```

**IQR (Interquartile Range)**:
```python
# More robust to non-normal distributions
detector = AnomalyDetector(method="iqr")

# Flag values outside [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
anomalies = detector.detect(data=response_times)

# Good for skewed distributions
```

### 2. Isolation Forest (Recommended)

**Best for**: General purpose, high-dimensional data

```python
from specweave import IsolationForestDetector

detector = IsolationForestDetector(
    contamination=0.05,  # Expected anomaly rate (5%)
    increment="0042"
)

# Train on normal data (or mixed data)
detector.fit(X_train)

# Detect anomalies
predictions = detector.predict(X_test)
# -1 = anomaly, 1 = normal

anomaly_scores = detector.score(X_test)
# Lower score = more anomalous

# Generates:
# - Anomaly scores for all samples
# - Feature importance (which features contribute to anomaly)
# - Threshold visualization
# - Top anomalies ranked by score
```

**Why Isolation Forest works**:
- Fast (O(n log n))
- Handles high dimensions well
- No assumptions about data distribution
- Anomalies are easier to isolate (fewer splits)

### 3. One-Class SVM

**Best for**: When you have only normal data for training

```python
from specweave import OneClassSVMDetector

# Train only on normal transactions
detector = OneClassSVMDetector(
    kernel='rbf',
    nu=0.05,  # Expected anomaly rate
    increment="0042"
)

detector.fit(X_normal)

# Detect anomalies in new data
predictions = detector.predict(X_new)
# -1 = anomaly, 1 = normal

# Good for: Clean training data of normal samples
```

### 4. Autoencoders (Deep Learning)

**Best for**: Complex patterns, high-dimensional data, images

```python
from specweave import AutoencoderDetector

# Learn to reconstruct normal data
detector = AutoencoderDetector(
    encoding_dim=32,  # Compressed representation
    layers=[64, 32, 16, 32, 64],
    increment="0042"
)

# Train on normal data
detector.fit(
    X_normal,
    epochs=100,
    validation_split=0.2
)

# Anomalies have high reconstruction error
anomaly_scores = detector.score(X_test)

# Generates:
# - Reconstruction error distribution
# - Threshold recommendation
# - Top anomalies with explanations
# - Learned representations (t-SNE plot)
```

**How autoencoders work**:
```
Input → Encoder → Compressed → Decoder → Reconstructed

Normal data: Low reconstruction error (learned well)
Anomalies: High reconstruction error (never seen before)
```

### 5. LOF (Local Outlier Factor)

**Best for**: Density-based anomalies (sparse regions)

```python
from specweave import LOFDetector

# Detects points in low-density regions
detector = LOFDetector(
    n_neighbors=20,
    contamination=0.05,
    increment="0042"
)

detector.fit(X_train)
predictions = detector.predict(X_test)

# Good for: Clustered data with sparse anomalies
```

## Anomaly Detection Workflows

### Workflow 1: Fraud Detection

```python
from specweave import FraudDetectionPipeline

pipeline = FraudDetectionPipeline(increment="0042")

# Features: transaction amount, location, time, merchant, etc.
pipeline.fit(normal_transactions)

# Real-time fraud detection
fraud_scores = pipeline.predict_proba(new_transactions)

# For each transaction:
# - Fraud probability (0-1)
# - Anomaly score
# - Contributing features
# - Similar past cases

# Generates:
# - Precision-Recall curve (fraud is rare)
# - Cost-benefit analysis (false positives vs missed fraud)
# - Feature importance for fraud
# - Fraud patterns identified
```

**Fraud Detection Best Practices**:
```python
# 1. Use multiple signals
pipeline.add_signals([
    'amount_vs_user_average',
    'distance_from_home',
    'merchant_risk_score',
    'velocity_24h'  # Transactions in last 24h
])

# 2. Set threshold based on cost
# False Positive cost: $5 (manual review)
# False Negative cost: $500 (fraud loss)
# Optimal threshold: Maximize (savings - review_cost)

# 3. Provide explanations
explanation = pipeline.explain_prediction(suspicious_transaction)
# "Flagged because: amount 10x user average, new merchant, foreign location"
```

### Workflow 2: System Anomaly Detection

```python
from specweave import SystemAnomalyPipeline

# Monitor system metrics (CPU, memory, latency, errors)
pipeline = SystemAnomalyPipeline(increment="0042")

# Train on normal system behavior
pipeline.fit(normal_metrics)

# Detect system anomalies
anomalies = pipeline.detect(current_metrics)

# For each anomaly:
# - Severity (low, medium, high, critical)
# - Affected metrics
# - Similar past incidents
# - Recommended actions

# Generates:
# - Anomaly timeline
# - Metric correlations (which metrics moved together)
# - Root cause analysis
# - Alert rules
```

**System Monitoring Best Practices**:
```python
# 1. Use time windows
pipeline.add_time_windows([
    '5min',   # Immediate spikes
    '1hour',  # Short-term trends
    '24hour'  # Daily patterns
])

# 2. Correlate metrics
pipeline.detect_correlations([
    ('high_cpu', 'slow_response'),
    ('memory_leak', 'increasing_errors')
])

# 3. Reduce alert fatigue
pipeline.set_alert_rules(
    min_severity='medium',
    min_duration='5min',  # Ignore transient spikes
    max_alerts_per_hour=5
)
```

### Workflow 3: Manufacturing Quality Control

```python
from specweave import QualityControlPipeline

# Detect defective products from sensor data
pipeline = QualityControlPipeline(increment="0042")

# Train on good products
pipeline.fit(good_product_sensors)

# Detect defects in production line
defect_scores = pipeline.predict(production_line_data)

# Generates:
# - Real-time defect alerts
# - Defect rate trends
# - Most common defect patterns
# - Preventive maintenance recommendations
```

### Workflow 4: Network Intrusion Detection

```python
from specweave import IntrusionDetectionPipeline

# Detect malicious network traffic
pipeline = IntrusionDetectionPipeline(increment="0042")

# Features: packet size, frequency, ports, protocols, etc.
pipeline.fit(normal_network_traffic)

# Detect intrusions
intrusions = pipeline.detect(network_traffic_stream)

# Generates:
# - Attack type classification (DDoS, port scan, etc.)
# - Severity scores
# - Source IPs
# - Attack timeline
```

## Evaluation Metrics

**Anomaly detection metrics** (different from classification):

```python
from specweave import AnomalyEvaluator

evaluator = AnomalyEvaluator(increment="0042")

metrics = evaluator.evaluate(
    y_true=true_labels,  # 0=normal, 1=anomaly
    y_pred=predictions,
    y_scores=anomaly_scores
)
```

**Key Metrics**:

1. **Precision @ K** - Of top K flagged anomalies, how many are real?
   ```python
   precision_at_100 = evaluator.precision_at_k(k=100)
   # "Of 100 flagged transactions, 85 were actual fraud" = 85%
   ```

2. **Recall @ K** - Of all real anomalies, how many did we catch in top K?
   ```python
   recall_at_100 = evaluator.recall_at_k(k=100)
   # "We caught 78% of all fraud in top 100 flagged"
   ```

3. **ROC AUC** - Overall discrimination ability
   ```python
   roc_auc = evaluator.roc_auc(y_true, y_scores)
   # 0.95 = excellent discrimination
   ```

4. **PR AUC** - Better for imbalanced data
   ```python
   pr_auc = evaluator.pr_auc(y_true, y_scores)
   # More informative when anomalies are rare (<5%)
   ```

**Evaluation Report**:
```markdown
# Anomaly Detection Evaluation

## Dataset
- Total samples: 100,000
- Anomalies: 500 (0.5%)
- Features: 25

## Method: Isolation Forest

## Performance Metrics
- ROC AUC: 0.94 ✅ (excellent)
- PR AUC: 0.78 ✅ (good for 0.5% anomaly rate)

## Precision-Recall Tradeoff
- Precision @ 100: 85% (85 true anomalies in top 100)
- Recall @ 100: 17% (caught 17% of all anomalies)
- Precision @ 500: 62% (310 true anomalies in top 500)
- Recall @ 500: 62% (caught 62% of all anomalies)

## Business Impact (Fraud Detection Example)
- Review budget: 500 transactions/day
- At Precision @ 500 = 62%:
  - True fraud caught: 310/day ($155,000 saved)
  - False positives: 190/day ($950 review cost)
  - Net benefit: $154,050/day ✅

## Recommendation
✅ DEPLOY with threshold for top 500 (62% precision)
```

## Integration with SpecWeave

### Increment Structure

```
.specweave/increments/0042-fraud-detection/
├── spec.md (detection requirements, business impact)
├── plan.md (method selection, threshold tuning)
├── tasks.md
├── data/
│   ├── normal_transactions.csv
│   ├── labeled_fraud.csv (if available)
│   └── schema.yaml
├── experiments/
│   ├── statistical-baseline/
│   ├── isolation-forest/
│   ├── one-class-svm/
│   └── autoencoder/
├── models/
│   ├── isolation_forest_model.pkl
│   └── threshold_config.json
├── evaluation/
│   ├── precision_recall_curve.png
│   ├── roc_curve.png
│   ├── top_anomalies.csv
│   └── evaluation_report.md
└── deployment/
    ├── real_time_api.py
    ├── monitoring_dashboard.json
    └── alert_rules.yaml
```

## Best Practices

### 1. Start with Labeled Anomalies (if available)

```python
# Use labeled data to validate unsupervised methods
detector.fit(X_train)  # Unlabeled

# Evaluate on labeled test set
metrics = evaluator.evaluate(y_true_test, detector.predict(X_test))

# Choose method with best precision @ K
```

### 2. Tune Contamination Parameter

```python
# Try different contamination rates
for contamination in [0.01, 0.05, 0.1, 0.2]:
    detector = IsolationForestDetector(contamination=contamination)
    detector.fit(X_train)
    
    metrics = evaluator.evaluate(y_test, detector.predict(X_test))
    
# Choose contamination that maximizes business value
```

### 3. Explain Anomalies

```python
# Don't just flag anomalies - explain why
explainer = AnomalyExplainer(detector, increment="0042")

for anomaly in top_anomalies:
    explanation = explainer.explain(anomaly)
    print(f"Anomaly: {anomaly.id}")
    print(f"Reasons:")
    print(f"  - {explanation.top_features}")
    print(f"  - Similar cases: {explanation.similar_cases}")
```

### 4. Handle Concept Drift

```python
# Anomalies evolve over time
monitor = AnomalyMonitor(increment="0042")

# Track detection performance
monitor.track_daily_performance()

# Retrain when accuracy drops
if monitor.performance_degraded():
    detector.retrain(new_normal_data)
```

### 5. Set Business-Driven Thresholds

```python
# Balance false positives vs false negatives
optimizer = ThresholdOptimizer(increment="0042")

optimal_threshold = optimizer.find_optimal(
    detector=detector,
    data=validation_data,
    false_positive_cost=5,    # $5 per manual review
    false_negative_cost=500   # $500 per missed fraud
)

# Use optimal threshold for deployment
```

## Advanced Features

### 1. Ensemble Anomaly Detection

```python
# Combine multiple detectors
ensemble = AnomalyEnsemble(increment="0042")

ensemble.add_detector("isolation_forest", weight=0.4)
ensemble.add_detector("one_class_svm", weight=0.3)
ensemble.add_detector("autoencoder", weight=0.3)

# Ensemble vote (more robust)
anomalies = ensemble.detect(X_test)
```

### 2. Contextual Anomaly Detection

```python
# What's normal varies by context
detector = ContextualAnomalyDetector(increment="0042")

# Different normality for different contexts
detector.fit(data, contexts=['user_id', 'time_of_day', 'location'])

# $10 transaction: Normal for user A, anomaly for user B
```

### 3. Sequential Anomaly Detection

```python
# Detect anomalous sequences (not just individual points)
detector = SequenceAnomalyDetector(
    method='lstm',
    window_size=10,
    increment="0042"
)

# Example: Login from unusual sequence of locations
```

## Commands

```bash
# Train anomaly detector
/ml:train-anomaly-detector 0042

# Evaluate detector
/ml:evaluate-anomaly-detector 0042

# Explain top anomalies
/ml:explain-anomalies 0042 --top 100
```

## Summary

Anomaly detection is critical for:
- ✅ Fraud detection (financial transactions)
- ✅ Security monitoring (intrusion detection)
- ✅ Quality control (manufacturing defects)
- ✅ System health (performance monitoring)
- ✅ Business intelligence (unusual patterns)

This skill provides battle-tested methods integrated with SpecWeave's increment workflow, ensuring anomaly detectors are reproducible, explainable, and business-aligned.
