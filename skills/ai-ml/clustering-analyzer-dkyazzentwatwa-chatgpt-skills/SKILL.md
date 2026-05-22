---
name: clustering-analyzer
description: Cluster data using K-Means, DBSCAN, hierarchical clustering. Use for customer segmentation, pattern discovery, or data grouping.
---

# Clustering Analyzer

Analyze and cluster data using multiple algorithms with visualization and evaluation.

## Features

- **K-Means**: Partition-based clustering with elbow method
- **DBSCAN**: Density-based clustering for arbitrary shapes
- **Hierarchical**: Agglomerative clustering with dendrograms
- **Evaluation**: Silhouette scores, cluster statistics
- **Visualization**: 2D/3D plots, dendrograms, elbow curves
- **Export**: Labeled data, cluster summaries

## Quick Start

```python
from clustering_analyzer import ClusteringAnalyzer

analyzer = ClusteringAnalyzer()
analyzer.load_csv("customers.csv")

# K-Means clustering
result = analyzer.kmeans(n_clusters=3)
print(f"Silhouette Score: {result['silhouette_score']:.3f}")

# Visualize
analyzer.plot_clusters("clusters.png")
```

## CLI Usage

```bash
# K-Means clustering
python clustering_analyzer.py --input data.csv --method kmeans --clusters 3

# Find optimal clusters (elbow method)
python clustering_analyzer.py --input data.csv --method kmeans --find-optimal

# DBSCAN clustering
python clustering_analyzer.py --input data.csv --method dbscan --eps 0.5 --min-samples 5

# Hierarchical clustering
python clustering_analyzer.py --input data.csv --method hierarchical --clusters 4

# Generate plots
python clustering_analyzer.py --input data.csv --method kmeans --clusters 3 --plot clusters.png

# Export labeled data
python clustering_analyzer.py --input data.csv --method kmeans --clusters 3 --output labeled.csv

# Select specific columns
python clustering_analyzer.py --input data.csv --columns age,income,spending --method kmeans --clusters 3
```

## API Reference

### ClusteringAnalyzer Class

```python
class ClusteringAnalyzer:
    def __init__(self)

    # Data loading
    def load_csv(self, filepath: str, columns: list = None) -> 'ClusteringAnalyzer'
    def load_dataframe(self, df: pd.DataFrame, columns: list = None) -> 'ClusteringAnalyzer'

    # Clustering methods
    def kmeans(self, n_clusters: int, **kwargs) -> dict
    def dbscan(self, eps: float = 0.5, min_samples: int = 5) -> dict
    def hierarchical(self, n_clusters: int, linkage: str = "ward") -> dict

    # Optimal clusters
    def find_optimal_clusters(self, max_k: int = 10) -> dict
    def elbow_plot(self, output: str, max_k: int = 10) -> str

    # Evaluation
    def silhouette_score(self) -> float
    def cluster_statistics(self) -> dict

    # Visualization
    def plot_clusters(self, output: str, dimensions: list = None) -> str
    def plot_dendrogram(self, output: str) -> str
    def plot_silhouette(self, output: str) -> str

    # Export
    def get_labels(self) -> list
    def to_dataframe(self) -> pd.DataFrame
    def save_labeled(self, output: str) -> str
```

## Clustering Methods

### K-Means

Best for spherical clusters with known number of groups:

```python
result = analyzer.kmeans(n_clusters=3)

# Returns:
{
    "labels": [0, 1, 2, 0, ...],
    "n_clusters": 3,
    "silhouette_score": 0.65,
    "inertia": 1234.56,
    "cluster_sizes": {0: 150, 1: 200, 2: 100},
    "centroids": [[...], [...], [...]]
}
```

### DBSCAN

Best for arbitrary-shaped clusters:

```python
result = analyzer.dbscan(eps=0.5, min_samples=5)

# Returns:
{
    "labels": [0, 0, 1, -1, ...],  # -1 = noise
    "n_clusters": 3,
    "n_noise": 15,
    "silhouette_score": 0.58,
    "cluster_sizes": {0: 150, 1: 200, 2: 100}
}
```

### Hierarchical (Agglomerative)

Best for understanding cluster hierarchy:

```python
result = analyzer.hierarchical(n_clusters=4, linkage="ward")

# Returns:
{
    "labels": [0, 1, 2, 3, ...],
    "n_clusters": 4,
    "silhouette_score": 0.62,
    "cluster_sizes": {0: 100, 1: 150, 2: 120, 3: 80}
}
```

## Finding Optimal Clusters

### Elbow Method

```python
optimal = analyzer.find_optimal_clusters(max_k=10)

# Returns:
{
    "optimal_k": 4,
    "inertias": [1000, 800, 500, 300, 280, ...],
    "silhouettes": [0.5, 0.55, 0.6, 0.65, 0.63, ...]
}
```

### Elbow Plot

```python
analyzer.elbow_plot("elbow.png", max_k=10)
```

Generates plot showing inertia vs number of clusters.

## Cluster Statistics

```python
stats = analyzer.cluster_statistics()

# Returns:
{
    "n_clusters": 3,
    "cluster_sizes": {0: 150, 1: 200, 2: 100},
    "cluster_means": {
        0: {"age": 25.5, "income": 45000, ...},
        1: {"age": 45.2, "income": 75000, ...},
        2: {"age": 35.1, "income": 55000, ...}
    },
    "cluster_std": {
        0: {"age": 5.2, "income": 8000, ...},
        ...
    },
    "overall_silhouette": 0.65
}
```

## Visualization

### Cluster Plot

```python
# 2D plot (uses first 2 features or PCA)
analyzer.plot_clusters("clusters_2d.png")

# Specify dimensions
analyzer.plot_clusters("clusters.png", dimensions=["age", "income"])
```

### Dendrogram

```python
# For hierarchical clustering
analyzer.hierarchical(n_clusters=4)
analyzer.plot_dendrogram("dendrogram.png")
```

### Silhouette Plot

```python
analyzer.plot_silhouette("silhouette.png")
```

Shows silhouette coefficient for each sample.

## Export Results

### Get Labels

```python
labels = analyzer.get_labels()
# [0, 1, 2, 0, 1, ...]
```

### Save Labeled Data

```python
analyzer.save_labeled("labeled_data.csv")
# Original data + cluster_label column
```

### Get Full DataFrame

```python
df = analyzer.to_dataframe()
# DataFrame with cluster_label column
```

## Example Workflows

### Customer Segmentation

```python
analyzer = ClusteringAnalyzer()
analyzer.load_csv("customers.csv", columns=["age", "income", "spending_score"])

# Find optimal number of segments
optimal = analyzer.find_optimal_clusters(max_k=8)
print(f"Optimal segments: {optimal['optimal_k']}")

# Cluster with optimal k
result = analyzer.kmeans(n_clusters=optimal['optimal_k'])

# Get segment characteristics
stats = analyzer.cluster_statistics()
for cluster_id, means in stats["cluster_means"].items():
    print(f"\nSegment {cluster_id}:")
    for feature, value in means.items():
        print(f"  {feature}: {value:.2f}")

# Save segmented data
analyzer.save_labeled("customer_segments.csv")
```

### Anomaly Detection with DBSCAN

```python
analyzer = ClusteringAnalyzer()
analyzer.load_csv("transactions.csv", columns=["amount", "frequency"])

# DBSCAN identifies noise points as potential anomalies
result = analyzer.dbscan(eps=0.3, min_samples=10)

print(f"Found {result['n_noise']} potential anomalies")

# Get anomalous records
df = analyzer.to_dataframe()
anomalies = df[df["cluster_label"] == -1]
```

### Document Clustering

```python
# After TF-IDF transformation
analyzer = ClusteringAnalyzer()
analyzer.load_dataframe(tfidf_matrix)

# Hierarchical clustering to see document relationships
result = analyzer.hierarchical(n_clusters=5)
analyzer.plot_dendrogram("doc_dendrogram.png")
```

## Data Preprocessing

The analyzer automatically:
- Handles missing values (imputation)
- Scales features (standardization)
- Reduces dimensions for visualization (PCA)

For custom preprocessing:

```python
from sklearn.preprocessing import StandardScaler

# Preprocess manually
df = pd.read_csv("data.csv")
scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

# Load preprocessed data
analyzer.load_dataframe(df_scaled)
```

## Dependencies

- scikit-learn>=1.3.0
- pandas>=2.0.0
- numpy>=1.24.0
- matplotlib>=3.7.0
- scipy>=1.10.0
