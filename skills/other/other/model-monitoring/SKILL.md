---
name: Model Monitoring
description: Monitor model performance, detect data drift, concept drift, and anomalies in production using Prometheus, Grafana, and MLflow
---

# Model Monitoring

## Overview

Monitoring deployed machine learning models ensures they continue to perform well in production, detecting data drift, concept drift, and performance degradation.

## When to Use

- When models are deployed in production environments serving real users
- When detecting data drift or concept drift in input features
- When tracking model performance metrics over time
- When ensuring model reliability, accuracy, and operational health
- When implementing ML observability and alerting systems
- When establishing thresholds for model retraining or intervention

## Monitoring Components

- **Performance Metrics**: Accuracy, latency, throughput
- **Data Drift**: Distribution changes in input features
- **Concept Drift**: Changes in target variable relationships
- **Output Drift**: Changes in prediction distribution
- **Feature Drift**: Individual feature distribution changes
- **Anomaly Detection**: Unusual samples in production

## Monitoring Tools

- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboarding
- **MLflow**: Model tracking and registry
- **TensorFlow Data Validation**: Data statistics
- **Evidently**: Drift detection and monitoring
- **Great Expectations**: Data quality assertions

## Python Implementation

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from scipy import stats
import json
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("=== 1. Production Monitoring System ===")

class ModelMonitoringSystem:
    def __init__(self, model, scaler, baseline_data, baseline_targets):
        self.model = model
        self.scaler = scaler
        self.baseline_data = baseline_data
        self.baseline_targets = baseline_targets
        self.baseline_mean = baseline_data.mean(axis=0)
        self.baseline_std = baseline_data.std(axis=0)
        self.baseline_predictions = model.predict(baseline_data)

        self.metrics_history = []
        self.drift_alerts = []
        self.performance_history = []

    def log_predictions(self, X, y_true, y_pred):
        """Log predictions and compute metrics"""
        timestamp = datetime.now()

        # Compute metrics
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)

        metric_record = {
            'timestamp': timestamp,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'n_samples': len(X)
        }

        self.metrics_history.append(metric_record)
        return metric_record

    def detect_data_drift(self, X_new):
        """Detect data drift using Kolmogorov-Smirnov test"""
        drift_detected = False
        drift_features = []

        for feature_idx in range(X_new.shape[1]):
            baseline_feature = self.baseline_data[:, feature_idx]
            new_feature = X_new[:, feature_idx]

            # KS Test
            ks_statistic, p_value = stats.ks_2samp(baseline_feature, new_feature)

            if p_value < 0.05:  # Significant drift detected
                drift_detected = True
                drift_features.append({
                    'feature_index': feature_idx,
                    'ks_statistic': float(ks_statistic),
                    'p_value': float(p_value)
                })

        if drift_detected:
            alert = {
                'timestamp': datetime.now(),
                'type': 'data_drift',
                'severity': 'high',
                'drifted_features': drift_features,
                'n_drifted': len(drift_features)
            }
            self.drift_alerts.append(alert)
            logger.warning(f"Data drift detected in {len(drift_features)} features")

        return drift_detected, drift_features

    def detect_output_drift(self, y_pred_new):
        """Detect drift in model predictions"""
        baseline_pred_dist = pd.Series(self.baseline_predictions).value_counts(normalize=True)
        new_pred_dist = pd.Series(y_pred_new).value_counts(normalize=True)

        # Compare distributions
        classes = set(baseline_pred_dist.index) | set(new_pred_dist.index)
        chi2_stat = 0

        for cls in classes:
            exp = baseline_pred_dist.get(cls, 0.01)
            obs = new_pred_dist.get(cls, 0.01)
            chi2_stat += (obs - exp) ** 2 / max(exp, 0.01)

        p_value = 1 - stats.chi2.cdf(chi2_stat, len(classes) - 1)

        if p_value < 0.05:
            alert = {
                'timestamp': datetime.now(),
                'type': 'output_drift',
                'severity': 'medium',
                'chi2_statistic': float(chi2_stat),
                'p_value': float(p_value)
            }
            self.drift_alerts.append(alert)
            logger.warning("Output drift detected in predictions")
            return True

        return False

    def detect_performance_degradation(self, y_true, y_pred):
        """Detect if model performance has degraded"""
        current_accuracy = accuracy_score(y_true, y_pred)
        baseline_accuracy = accuracy_score(self.baseline_targets, self.baseline_predictions)

        degradation_threshold = 0.05  # 5% drop
        degradation = baseline_accuracy - current_accuracy

        if degradation > degradation_threshold:
            alert = {
                'timestamp': datetime.now(),
                'type': 'performance_degradation',
                'severity': 'critical',
                'baseline_accuracy': float(baseline_accuracy),
                'current_accuracy': float(current_accuracy),
                'degradation': float(degradation)
            }
            self.drift_alerts.append(alert)
            logger.error("Performance degradation detected")
            return True

        return False

    def get_monitoring_report(self):
        """Generate monitoring report"""
        if not self.metrics_history:
            return {}

        metrics_df = pd.DataFrame(self.metrics_history)

        return {
            'monitoring_period': {
                'start': self.metrics_history[0]['timestamp'].isoformat(),
                'end': self.metrics_history[-1]['timestamp'].isoformat(),
                'n_batches': len(self.metrics_history)
            },
            'performance_summary': {
                'avg_accuracy': float(metrics_df['accuracy'].mean()),
                'min_accuracy': float(metrics_df['accuracy'].min()),
                'max_accuracy': float(metrics_df['accuracy'].max()),
                'std_accuracy': float(metrics_df['accuracy'].std()),
                'avg_f1': float(metrics_df['f1'].mean())
            },
            'drift_summary': {
                'total_alerts': len(self.drift_alerts),
                'data_drift_alerts': sum(1 for a in self.drift_alerts if a['type'] == 'data_drift'),
                'output_drift_alerts': sum(1 for a in self.drift_alerts if a['type'] == 'output_drift'),
                'performance_alerts': sum(1 for a in self.drift_alerts if a['type'] == 'performance_degradation')
            },
            'alerts': self.drift_alerts[-10:]  # Last 10 alerts
        }

print("Monitoring system initialized")

# 2. Create baseline model
print("\n=== 2. Train Baseline Model ===")

from sklearn.datasets import make_classification

# Create baseline data
X_baseline, y_baseline = make_classification(n_samples=1000, n_features=20,
                                            n_informative=15, random_state=42)
scaler = StandardScaler()
X_baseline_scaled = scaler.fit_transform(X_baseline)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_baseline_scaled, y_baseline)

print(f"Baseline model trained on {len(X_baseline)} samples")

# 3. Initialize monitoring
monitor = ModelMonitoringSystem(model, scaler, X_baseline_scaled, y_baseline)

# 4. Simulate production data and monitoring
print("\n=== 3. Production Monitoring Simulation ===")

# Simulate normal production data
X_prod_normal = np.random.randn(500, 20) * 0.5
X_prod_normal_scaled = scaler.transform(X_prod_normal)
y_pred_normal = model.predict(X_prod_normal_scaled)
y_true_normal = np.random.randint(0, 2, 500)

metrics_normal = monitor.log_predictions(X_prod_normal_scaled, y_true_normal, y_pred_normal)
print(f"Normal production batch - Accuracy: {metrics_normal['accuracy']:.4f}")

# Simulate drifted data
X_prod_drift = np.random.randn(500, 20) * 2.0  # Different distribution
X_prod_drift_scaled = scaler.transform(X_prod_drift)
y_pred_drift = model.predict(X_prod_drift_scaled)
y_true_drift = np.random.randint(0, 2, 500)

metrics_drift = monitor.log_predictions(X_prod_drift_scaled, y_true_drift, y_pred_drift)
drift_detected, drift_features = monitor.detect_data_drift(X_prod_drift_scaled)
print(f"Drifted production batch - Accuracy: {metrics_drift['accuracy']:.4f}")
print(f"Data drift detected: {drift_detected}")

# Check performance degradation
perf_degradation = monitor.detect_performance_degradation(y_true_drift, y_pred_drift)
print(f"Performance degradation: {perf_degradation}")

# 5. Prometheus metrics export
print("\n=== 4. Prometheus Metrics Format ===")

prometheus_metrics = f"""
# HELP model_accuracy Model accuracy score
# TYPE model_accuracy gauge
model_accuracy{"{timestamp='2024-01-01'}"} {metrics_normal['accuracy']:.4f}

# HELP model_f1_score Model F1 score
# TYPE model_f1_score gauge
model_f1_score{"{timestamp='2024-01-01'}"} {metrics_normal['f1']:.4f}

# HELP model_predictions_total Total predictions made
# TYPE model_predictions_total counter
model_predictions_total 5000

# HELP model_drift_detected Data drift detection flag
# TYPE model_drift_detected gauge
model_drift_detected {int(drift_detected)}

# HELP model_latency_seconds Prediction latency in seconds
# TYPE model_latency_seconds histogram
model_latency_seconds_bucket{{le="0.01"}} 100
model_latency_seconds_bucket{{le="0.05"}} 450
model_latency_seconds_bucket{{le="0.1"}} 500
"""

print("Prometheus metrics:")
print(prometheus_metrics)

# 6. Grafana dashboard JSON
print("\n=== 5. Grafana Dashboard Configuration ===")

grafana_dashboard = {
    'title': 'ML Model Monitoring Dashboard',
    'panels': [
        {
            'title': 'Model Accuracy',
            'targets': [{'metric': 'model_accuracy'}],
            'type': 'graph'
        },
        {
            'title': 'Data Drift Alerts',
            'targets': [{'metric': 'model_drift_detected'}],
            'type': 'stat'
        },
        {
            'title': 'Prediction Latency',
            'targets': [{'metric': 'model_latency_seconds'}],
            'type': 'graph'
        },
        {
            'title': 'Feature Distributions',
            'targets': [{'metric': 'feature_distribution_change'}],
            'type': 'heatmap'
        }
    ]
}

print("Grafana dashboard configured with 4 panels")

# 7. Visualization
print("\n=== 6. Monitoring Visualization ===")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Performance over time
metrics_df = pd.DataFrame(monitor.metrics_history)
axes[0, 0].plot(range(len(metrics_df)), metrics_df['accuracy'], marker='o', label='Accuracy')
axes[0, 0].axhline(y=metrics_df['accuracy'].mean(), color='r', linestyle='--', label='Mean')
axes[0, 0].set_xlabel('Batch')
axes[0, 0].set_ylabel('Accuracy')
axes[0, 0].set_title('Model Accuracy Over Time')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Precision, Recall, F1
axes[0, 1].plot(range(len(metrics_df)), metrics_df['precision'], label='Precision', marker='s')
axes[0, 1].plot(range(len(metrics_df)), metrics_df['recall'], label='Recall', marker='^')
axes[0, 1].plot(range(len(metrics_df)), metrics_df['f1'], label='F1', marker='d')
axes[0, 1].set_xlabel('Batch')
axes[0, 1].set_ylabel('Score')
axes[0, 1].set_title('Performance Metrics Over Time')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Feature distributions (baseline vs current)
feature_stats = pd.DataFrame({
    'Baseline Mean': np.mean(X_baseline, axis=0)[:10],
    'Current Mean': np.mean(X_prod_drift, axis=0)[:10]
})
axes[1, 0].bar(range(len(feature_stats)), feature_stats['Baseline Mean'], alpha=0.7, label='Baseline')
axes[1, 0].bar(range(len(feature_stats)), feature_stats['Current Mean'], alpha=0.7, label='Current')
axes[1, 0].set_xlabel('Feature')
axes[1, 0].set_ylabel('Mean Value')
axes[1, 0].set_title('Feature Distribution Drift (First 10)')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Alerts over time
alert_types = [a['type'] for a in monitor.drift_alerts]
alert_counts = pd.Series(alert_types).value_counts()
axes[1, 1].barh(alert_counts.index, alert_counts.values, color=['red', 'orange', 'yellow'])
axes[1, 1].set_xlabel('Count')
axes[1, 1].set_title('Alert Types Distribution')
axes[1, 1].grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('model_monitoring_dashboard.png', dpi=100, bbox_inches='tight')
print("\nMonitoring dashboard saved as 'model_monitoring_dashboard.png'")

# 8. Report generation
report = monitor.get_monitoring_report()
print("\n=== 7. Monitoring Report ===")
print(json.dumps(report, indent=2, default=str))

print("\nModel monitoring system setup completed!")
```

## Drift Detection Techniques

- **Kolmogorov-Smirnov Test**: Statistical test for distribution change
- **Population Stability Index**: Measures feature distribution shifts
- **Chi-square Test**: Categorical feature drift
- **Wasserstein Distance**: Optimal transport-based distance
- **Jensen-Shannon Divergence**: Information-theoretic metric

## Alert Thresholds

- **Critical**: >5% accuracy drop, immediate action
- **High**: Data drift in 3+ features, investigation needed
- **Medium**: Output drift, monitoring increased
- **Low**: Single feature drift, log and track

## Deliverables

- Monitoring dashboards
- Alert configuration
- Drift detection reports
- Performance degradation analysis
- Retraining recommendations
- Action playbook
