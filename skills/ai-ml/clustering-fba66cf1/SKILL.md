---
name: clustering
description: Discover patterns in unlabeled data using clustering, dimensionality reduction, and anomaly detection
version: "1.4.0"
sasmp_version: "1.4.0"
bonded_agent: 03-unsupervised-learning
bond_type: PRIMARY_BOND

# Parameter Validation
parameters:
  required:
    - name: X
      type: array
      validation: "2D array, scaled numeric"
  optional:
    - name: n_clusters
      type: integer
      default: null
      validation: "2 <= n <= 50"
    - name: method
      type: string
      default: "kmeans"
      validation: "[kmeans|dbscan|hierarchical|hdbscan]"

# Retry Logic
retry_logic:
  strategy: exponential_backoff
  max_attempts: 3
  base_delay_ms: 1000

# Observability
logging:
  level: info
  metrics: [n_clusters, silhouette_score, execution_time]
---

# Clustering Skill

> Discover hidden patterns and groupings in unlabeled data.

## Quick Start

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# Always scale before clustering
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Cluster
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_scaled)

# Evaluate
score = silhouette_score(X_scaled, labels)
print(f"Silhouette Score: {score:.4f}")
```

## Key Topics

### 1. Clustering Algorithms

| Algorithm | Best For | Key Params |
|-----------|----------|------------|
| **K-Means** | Spherical clusters | n_clusters |
| **DBSCAN** | Arbitrary shapes, noise | eps, min_samples |
| **Hierarchical** | Nested clusters | linkage |
| **HDBSCAN** | Variable density | min_cluster_size |

```python
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
import hdbscan

algorithms = {
    'kmeans': KMeans(n_clusters=5, random_state=42),
    'dbscan': DBSCAN(eps=0.5, min_samples=5),
    'hierarchical': AgglomerativeClustering(n_clusters=5),
    'hdbscan': hdbscan.HDBSCAN(min_cluster_size=15)
}
```

### 2. Finding Optimal K

```python
from sklearn.metrics import silhouette_score, calinski_harabasz_score
import matplotlib.pyplot as plt

def find_optimal_k(X, max_k=15):
    """Find optimal number of clusters."""
    metrics = {'inertia': [], 'silhouette': [], 'calinski': []}
    K = range(2, max_k + 1)

    for k in K:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X)

        metrics['inertia'].append(kmeans.inertia_)
        metrics['silhouette'].append(silhouette_score(X, labels))
        metrics['calinski'].append(calinski_harabasz_score(X, labels))

    # Find optimal k
    optimal_k = K[np.argmax(metrics['silhouette'])]
    return optimal_k, metrics
```

### 3. Dimensionality Reduction

| Method | Preserves | Speed |
|--------|-----------|-------|
| **PCA** | Global variance | Fast |
| **t-SNE** | Local structure | Slow |
| **UMAP** | Both local/global | Fast |

```python
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap

# PCA for preprocessing
pca = PCA(n_components=0.95)  # Keep 95% variance
X_pca = pca.fit_transform(X)

# UMAP for visualization
reducer = umap.UMAP(n_components=2, random_state=42)
X_2d = reducer.fit_transform(X)
```

### 4. Anomaly Detection

```python
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

# Isolation Forest
iso_forest = IsolationForest(contamination=0.1, random_state=42)
anomalies = iso_forest.fit_predict(X)  # -1 for anomaly

# Local Outlier Factor
lof = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
anomalies = lof.fit_predict(X)
```

### 5. Cluster Validation

```python
from sklearn.metrics import (
    silhouette_score,
    calinski_harabasz_score,
    davies_bouldin_score
)

def validate_clustering(X, labels):
    """Comprehensive cluster validation."""
    return {
        'silhouette': silhouette_score(X, labels),  # Higher = better
        'calinski_harabasz': calinski_harabasz_score(X, labels),  # Higher = better
        'davies_bouldin': davies_bouldin_score(X, labels),  # Lower = better
        'n_clusters': len(set(labels) - {-1})
    }
```

## Best Practices

### DO
- Always scale features before clustering
- Try multiple algorithms
- Use multiple validation metrics
- Visualize clusters in 2D
- Interpret clusters with domain knowledge

### DON'T
- Don't use K-Means for non-spherical clusters
- Don't ignore the silhouette score per cluster
- Don't assume first result is optimal
- Don't use t-SNE for new point projection

## Exercises

### Exercise 1: Elbow Method
```python
# TODO: Implement elbow method to find optimal K
# Plot inertia vs K and identify elbow point
```

### Exercise 2: Compare Algorithms
```python
# TODO: Compare K-Means, DBSCAN, and HDBSCAN
# on the same dataset using silhouette score
```

## Unit Test Template

```python
import pytest
import numpy as np
from sklearn.datasets import make_blobs

def test_clustering_finds_groups():
    """Test clustering finds expected number of clusters."""
    X, y_true = make_blobs(n_samples=100, centers=3, random_state=42)

    kmeans = KMeans(n_clusters=3, random_state=42)
    labels = kmeans.fit_predict(X)

    assert len(set(labels)) == 3

def test_scaling_improves_score():
    """Test that scaling improves clustering quality."""
    X, _ = make_blobs(n_samples=100, centers=3)
    X[:, 0] *= 100  # Make first feature much larger

    # Without scaling
    labels_raw = KMeans(n_clusters=3).fit_predict(X)
    score_raw = silhouette_score(X, labels_raw)

    # With scaling
    X_scaled = StandardScaler().fit_transform(X)
    labels_scaled = KMeans(n_clusters=3).fit_predict(X_scaled)
    score_scaled = silhouette_score(X_scaled, labels_scaled)

    assert score_scaled > score_raw
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| All in one cluster | Wrong eps/K | Reduce eps or increase K |
| Too many clusters | Parameters too sensitive | Increase eps or min_samples |
| Poor silhouette | Wrong algorithm | Try different clustering method |
| Memory error | Large dataset | Use MiniBatchKMeans |

## Related Resources

- **Agent**: `03-unsupervised-learning`
- **Previous**: `supervised-learning`
- **Next**: `deep-learning`

---

**Version**: 1.4.0 | **Status**: Production Ready
