---
name: Anomaly Detection
description: Identify unusual patterns, outliers, and anomalies in data using statistical methods, isolation forests, and autoencoders for fraud detection and quality monitoring
---

# Anomaly Detection

## Overview

Anomaly detection identifies unusual patterns, outliers, and anomalies in data that deviate significantly from normal behavior, enabling fraud detection and system monitoring.

## When to Use

- Detecting fraudulent transactions or suspicious activity in financial data
- Identifying system failures, network intrusions, or security breaches
- Monitoring manufacturing quality and identifying defective products
- Finding unusual patterns in healthcare data or patient vital signs
- Detecting abnormal sensor readings in IoT or industrial systems
- Identifying outliers in customer behavior for targeted intervention

## Detection Methods

- **Statistical**: Z-score, IQR, modified Z-score
- **Distance-based**: K-nearest neighbors, Local Outlier Factor
- **Isolation**: Isolation Forest
- **Density-based**: DBSCAN
- **Deep Learning**: Autoencoders, GANs

## Anomaly Types

- **Point Anomalies**: Single unusual records
- **Contextual**: Unusual in specific context
- **Collective**: Unusual patterns in sequences
- **Novel Classes**: Completely new patterns

## Implementation with Python

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope
from scipy import stats

# Generate sample data with anomalies
np.random.seed(42)

# Normal data
n_normal = 950
normal_data = np.random.normal(100, 15, (n_normal, 2))

# Anomalies
n_anomalies = 50
anomalies = np.random.uniform(0, 200, (n_anomalies, 2))
anomalies[n_anomalies//2:, 0] = np.random.uniform(80, 120, n_anomalies//2)
anomalies[n_anomalies//2:, 1] = np.random.uniform(-50, 0, n_anomalies//2)

X = np.vstack([normal_data, anomalies])
y_true = np.hstack([np.zeros(n_normal), np.ones(n_anomalies)])

df = pd.DataFrame(X, columns=['Feature1', 'Feature2'])
df['is_anomaly_true'] = y_true

print("Data Summary:")
print(f"Normal samples: {n_normal}")
print(f"Anomalies: {n_anomalies}")
print(f"Total: {len(df)}")

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 1. Statistical Methods (Z-score)
z_scores = np.abs(stats.zscore(X))
z_anomaly_mask = (z_scores > 3).any(axis=1)
df['z_score_anomaly'] = z_anomaly_mask

print(f"\n1. Z-score Method:")
print(f"Anomalies detected: {z_anomaly_mask.sum()}")
print(f"Accuracy: {(z_anomaly_mask == y_true).mean():.2%}")

# 2. Isolation Forest
iso_forest = IsolationForest(contamination=n_anomalies/len(df), random_state=42)
iso_predictions = iso_forest.fit_predict(X_scaled)
iso_anomaly_mask = iso_predictions == -1
iso_scores = iso_forest.score_samples(X_scaled)

df['iso_anomaly'] = iso_anomaly_mask
df['iso_score'] = iso_scores

print(f"\n2. Isolation Forest:")
print(f"Anomalies detected: {iso_anomaly_mask.sum()}")
print(f"Accuracy: {(iso_anomaly_mask == y_true).mean():.2%}")

# 3. Local Outlier Factor
lof = LocalOutlierFactor(n_neighbors=20, contamination=n_anomalies/len(df))
lof_predictions = lof.fit_predict(X_scaled)
lof_anomaly_mask = lof_predictions == -1
lof_scores = lof.negative_outlier_factor_

df['lof_anomaly'] = lof_anomaly_mask
df['lof_score'] = lof_scores

print(f"\n3. Local Outlier Factor:")
print(f"Anomalies detected: {lof_anomaly_mask.sum()}")
print(f"Accuracy: {(lof_anomaly_mask == y_true).mean():.2%}")

# 4. Elliptic Envelope (Robust Covariance)
ee = EllipticEnvelope(contamination=n_anomalies/len(df), random_state=42)
ee_predictions = ee.fit_predict(X_scaled)
ee_anomaly_mask = ee_predictions == -1
ee_scores = ee.mahalanobis(X_scaled)

df['ee_anomaly'] = ee_anomaly_mask
df['ee_score'] = ee_scores

print(f"\n4. Elliptic Envelope:")
print(f"Anomalies detected: {ee_anomaly_mask.sum()}")
print(f"Accuracy: {(ee_anomaly_mask == y_true).mean():.2%}")

# 5. IQR Method
Q1 = np.percentile(X, 25, axis=0)
Q3 = np.percentile(X, 75, axis=0)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

iqr_anomaly_mask = ((X < lower_bound) | (X > upper_bound)).any(axis=1)
df['iqr_anomaly'] = iqr_anomaly_mask

print(f"\n5. IQR Method:")
print(f"Anomalies detected: {iqr_anomaly_mask.sum()}")
print(f"Accuracy: {(iqr_anomaly_mask == y_true).mean():.2%}")

# Visualization of anomaly detection methods
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

methods = [
    (z_anomaly_mask, 'Z-score', None),
    (iso_anomaly_mask, 'Isolation Forest', iso_scores),
    (lof_anomaly_mask, 'LOF', lof_scores),
    (ee_anomaly_mask, 'Elliptic Envelope', ee_scores),
    (iqr_anomaly_mask, 'IQR', None),
]

# True anomalies
ax = axes[0, 0]
colors = ['blue' if not a else 'red' for a in y_true]
ax.scatter(df['Feature1'], df['Feature2'], c=colors, alpha=0.6, s=30)
ax.set_title('True Anomalies')
ax.set_xlabel('Feature 1')
ax.set_ylabel('Feature 2')

# Plot each method
for idx, (anomaly_mask, method_name, scores) in enumerate(methods):
    ax = axes.flatten()[idx + 1]

    if scores is not None:
        scatter = ax.scatter(df['Feature1'], df['Feature2'], c=scores, cmap='RdYlBu_r', alpha=0.6, s=30)
        plt.colorbar(scatter, ax=ax, label='Score')
    else:
        colors = ['red' if a else 'blue' for a in anomaly_mask]
        ax.scatter(df['Feature1'], df['Feature2'], c=colors, alpha=0.6, s=30)

    ax.set_title(f'{method_name}\n({anomaly_mask.sum()} anomalies)')
    ax.set_xlabel('Feature 1')
    ax.set_ylabel('Feature 2')

plt.tight_layout()
plt.show()

# 6. Anomaly score comparison
fig, axes = plt.subplots(2, 2, figsize=(14, 8))

# ISO Forest scores
axes[0, 0].hist(iso_scores[~y_true], bins=30, alpha=0.7, label='Normal', color='blue')
axes[0, 0].hist(iso_scores[y_true == 1], bins=10, alpha=0.7, label='Anomaly', color='red')
axes[0, 0].set_xlabel('Anomaly Score')
axes[0, 0].set_title('Isolation Forest Score Distribution')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# LOF scores
axes[0, 1].hist(lof_scores[~y_true], bins=30, alpha=0.7, label='Normal', color='blue')
axes[0, 1].hist(lof_scores[y_true == 1], bins=10, alpha=0.7, label='Anomaly', color='red')
axes[0, 1].set_xlabel('Anomaly Score')
axes[0, 1].set_title('LOF Score Distribution')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# ROC-like curve for Isolation Forest
iso_scores_sorted = np.sort(iso_scores)
detected_at_threshold = []
for threshold in iso_scores_sorted:
    detected = (iso_scores <= threshold).sum()
    true_detected = ((iso_scores <= threshold) & (y_true == 1)).sum()
    if detected > 0:
        precision = true_detected / detected
        recall = true_detected / n_anomalies
        detected_at_threshold.append({'Threshold': threshold, 'Precision': precision, 'Recall': recall})

if detected_at_threshold:
    threshold_df = pd.DataFrame(detected_at_threshold)
    axes[1, 0].plot(threshold_df['Recall'], threshold_df['Precision'], linewidth=2)
    axes[1, 0].set_xlabel('Recall')
    axes[1, 0].set_ylabel('Precision')
    axes[1, 0].set_title('Precision-Recall Curve (Isolation Forest)')
    axes[1, 0].grid(True, alpha=0.3)

# Method comparison
methods_comparison = pd.DataFrame({
    'Method': ['Z-score', 'Isolation Forest', 'LOF', 'Elliptic Envelope', 'IQR'],
    'Accuracy': [
        (z_anomaly_mask == y_true).mean(),
        (iso_anomaly_mask == y_true).mean(),
        (lof_anomaly_mask == y_true).mean(),
        (ee_anomaly_mask == y_true).mean(),
        (iqr_anomaly_mask == y_true).mean(),
    ]
})

axes[1, 1].barh(methods_comparison['Method'], methods_comparison['Accuracy'], color='steelblue', edgecolor='black')
axes[1, 1].set_xlabel('Accuracy')
axes[1, 1].set_title('Method Comparison')
axes[1, 1].set_xlim([0, 1])
for i, v in enumerate(methods_comparison['Accuracy']):
    axes[1, 1].text(v, i, f' {v:.2%}', va='center')

plt.tight_layout()
plt.show()

# 7. Ensemble anomaly detection
# Combine multiple methods
ensemble_votes = (z_anomaly_mask.astype(int) +
                  iso_anomaly_mask.astype(int) +
                  lof_anomaly_mask.astype(int) +
                  ee_anomaly_mask.astype(int) +
                  iqr_anomaly_mask.astype(int))

df['ensemble_votes'] = ensemble_votes
ensemble_anomaly = ensemble_votes >= 3  # Majority vote

print(f"\n6. Ensemble (Majority Vote):")
print(f"Anomalies detected: {ensemble_anomaly.sum()}")
print(f"Accuracy: {(ensemble_anomaly == y_true).mean():.2%}")

# Visualize ensemble
fig, ax = plt.subplots(figsize=(10, 8))
scatter = ax.scatter(df['Feature1'], df['Feature2'], c=ensemble_votes, cmap='RdYlGn_r',
                     s=100 * (ensemble_anomaly.astype(int) + 0.5), alpha=0.6, edgecolors='black')
ax.set_xlabel('Feature 1')
ax.set_ylabel('Feature 2')
ax.set_title('Ensemble Anomaly Detection (Color: Vote Count, Size: Anomaly)')
cbar = plt.colorbar(scatter, ax=ax, label='Number of Methods')
plt.show()

# 8. Time-series anomalies
time_series_data = np.sin(np.arange(100) * 0.2) * 10 + 100
time_series_data = time_series_data + np.random.normal(0, 2, 100)
# Add anomalies
time_series_data[25] = 150
time_series_data[50] = 50
time_series_data[75] = 140

# Detect using rolling statistics
rolling_mean = pd.Series(time_series_data).rolling(window=5).mean()
rolling_std = pd.Series(time_series_data).rolling(window=5).std()
z_scores_ts = np.abs((time_series_data - rolling_mean) / rolling_std) > 2

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(time_series_data, linewidth=1, label='Data')
ax.plot(rolling_mean, linewidth=2, label='Rolling Mean')
ax.scatter(np.where(z_scores_ts)[0], time_series_data[z_scores_ts], color='red', s=100, label='Anomalies', zorder=5)
ax.fill_between(range(len(time_series_data)), rolling_mean - 2*rolling_std, rolling_mean + 2*rolling_std,
                alpha=0.2, label='±2 Std Dev')
ax.set_xlabel('Time')
ax.set_ylabel('Value')
ax.set_title('Time-Series Anomaly Detection')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("\nAnomaly detection analysis complete!")
```

## Method Selection Guide

- **Z-score**: Simple, fast, assumes normal distribution
- **IQR**: Robust, non-parametric, good for outliers
- **Isolation Forest**: Efficient, good for high dimensions
- **LOF**: Density-based, finds local anomalies
- **Autoencoders**: Complex patterns, deep learning

## Threshold Selection

- **Conservative**: Fewer false positives, more false negatives
- **Aggressive**: More anomalies flagged, more false positives
- **Data-driven**: Use validation set to optimize threshold

## Deliverables

- Anomaly detection results
- Anomaly scores visualization
- Comparison of methods
- Identified anomalous records
- Recommendation for production deployment
- Threshold optimization analysis
