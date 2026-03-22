---
name: data-mining
description: "Extract patterns and insights from large datasets using association rules, clustering, classification, and anomaly detection. Use for market basket analysis, customer segmentation, fraud detection, pattern discovery, predictive modeling, and knowledge extraction from structured and unstructured data."
---

# Data Mining

Extract valuable patterns, relationships, and insights from large datasets using computational algorithms.

## Overview

Data mining is the process of discovering patterns, correlations, and anomalies within large datasets to predict outcomes and extract actionable knowledge. It combines techniques from statistics, machine learning, and database systems to analyze data from multiple perspectives. This skill covers association rule learning, clustering algorithms, classification methods, and anomaly detection techniques.

## Core Data Mining Techniques

| Technique | Purpose | Common Algorithms | Use Cases |
|-----------|---------|-------------------|-----------|
| Association Rules | Find relationships between items | Apriori, FP-Growth, ECLAT | Market basket analysis, recommendation systems |
| Clustering | Group similar items | K-Means, DBSCAN, Hierarchical | Customer segmentation, image segmentation |
| Classification | Predict categorical outcomes | Decision Trees, Random Forest, SVM | Spam detection, credit scoring |
| Regression | Predict numerical outcomes | Linear Regression, Gradient Boosting | Sales forecasting, price prediction |
| Anomaly Detection | Identify outliers | Isolation Forest, LOF, One-Class SVM | Fraud detection, network intrusion |

## Association Rule Learning

### Key Concepts

**Support**: Frequency of itemset in dataset
- Formula: support(X) = count(X) / total_transactions
- High support = common itemset

**Confidence**: Strength of rule X → Y
- Formula: confidence(X → Y) = support(X ∪ Y) / support(X)
- High confidence = strong predictive relationship

**Lift**: Correlation between X and Y
- Formula: lift(X → Y) = confidence(X → Y) / support(Y)
- Lift > 1: positive correlation
- Lift < 1: negative correlation
- Lift = 1: independence

### Apriori Algorithm

```python
from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

# Prepare transaction data (one-hot encoded)
# Each row is a transaction, each column is an item (True/False)
transactions = pd.DataFrame({
    'milk': [True, True, False, True],
    'bread': [True, True, True, False],
    'butter': [False, True, True, True],
    'beer': [False, False, True, True]
})

# Find frequent itemsets
frequent_itemsets = apriori(transactions, min_support=0.5, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)

# Filter by lift
strong_rules = rules[rules['lift'] > 1.2]
```

### FP-Growth Algorithm

Faster than Apriori for large datasets:
- Builds FP-tree (compressed representation)
- Mines frequent patterns without candidate generation
- More efficient for dense datasets

### Applications

1. **Market Basket Analysis**
   - Product placement optimization
   - Cross-selling strategies
   - Bundle pricing

2. **Web Usage Mining**
   - Page navigation patterns
   - User behavior analysis
   - Content recommendation

3. **Healthcare**
   - Symptom-disease associations
   - Drug interaction detection
   - Treatment effectiveness patterns

## Clustering Algorithms

### K-Means Clustering

**Algorithm**:
1. Initialize K cluster centroids randomly
2. Assign each point to nearest centroid
3. Recalculate centroids as mean of assigned points
4. Repeat until convergence

```python
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Fit K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X)

# Visualize
plt.scatter(X[:, 0], X[:, 1], c=clusters, cmap='viridis')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], 
            marker='x', s=200, linewidths=3, color='r')
plt.show()

# Elbow method for optimal K
inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

plt.plot(range(1, 11), inertias, marker='o')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.show()
```

**Strengths**: Fast, scalable, simple
**Weaknesses**: Requires K specification, sensitive to outliers, assumes spherical clusters

### DBSCAN (Density-Based Spatial Clustering)

**Parameters**:
- `eps`: Maximum distance between points in same cluster
- `min_samples`: Minimum points to form dense region

```python
from sklearn.cluster import DBSCAN

# Fit DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)
clusters = dbscan.fit_predict(X)

# -1 indicates noise/outliers
n_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
n_noise = list(clusters).count(-1)
```

**Strengths**: Finds arbitrary-shaped clusters, identifies outliers, no need to specify K
**Weaknesses**: Sensitive to parameters, struggles with varying densities

### Hierarchical Clustering

**Agglomerative (bottom-up)**:
1. Start with each point as cluster
2. Merge closest clusters
3. Repeat until single cluster

```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# Fit hierarchical clustering
hierarchical = AgglomerativeClustering(n_clusters=3, linkage='ward')
clusters = hierarchical.fit_predict(X)

# Create dendrogram
linkage_matrix = linkage(X, method='ward')
dendrogram(linkage_matrix)
plt.title('Hierarchical Clustering Dendrogram')
plt.show()
```

**Linkage methods**:
- Ward: Minimizes within-cluster variance
- Complete: Maximum distance between clusters
- Average: Average distance between clusters
- Single: Minimum distance between clusters

## Classification Techniques

### Decision Trees

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree

# Train decision tree
dt = DecisionTreeClassifier(max_depth=5, min_samples_split=20, random_state=42)
dt.fit(X_train, y_train)

# Visualize tree
plt.figure(figsize=(20, 10))
plot_tree(dt, feature_names=feature_names, class_names=class_names, filled=True)
plt.show()

# Feature importance
importances = pd.DataFrame({
    'feature': feature_names,
    'importance': dt.feature_importances_
}).sort_values('importance', ascending=False)
```

### Random Forest

Ensemble of decision trees:
- Reduces overfitting
- Improves accuracy
- Provides feature importance

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
rf.fit(X_train, y_train)

# Out-of-bag score (internal validation)
rf_oob = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=42)
rf_oob.fit(X_train, y_train)
print(f"OOB Score: {rf_oob.oob_score_}")
```

## Anomaly Detection

### Isolation Forest

Isolates anomalies by randomly partitioning data:
- Anomalies are easier to isolate (fewer splits needed)
- Normal points require more splits

```python
from sklearn.ensemble import IsolationForest

# Fit Isolation Forest
iso_forest = IsolationForest(contamination=0.1, random_state=42)
predictions = iso_forest.fit_predict(X)

# -1 indicates anomaly, 1 indicates normal
anomalies = X[predictions == -1]
normal = X[predictions == 1]
```

### Local Outlier Factor (LOF)

Measures local density deviation:
- Compares density of point to neighbors
- Low density relative to neighbors = outlier

```python
from sklearn.neighbors import LocalOutlierFactor

lof = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
predictions = lof.fit_predict(X)
```

## Data Mining Workflow

### 1. Business Understanding
- Define objectives
- Identify success criteria
- Assess resources and constraints

### 2. Data Understanding
- Collect initial data
- Explore data characteristics
- Verify data quality

### 3. Data Preparation
- Select relevant data
- Clean data (handle missing values, outliers)
- Transform features
- Integrate data from multiple sources

### 4. Modeling
- Select modeling techniques
- Build models
- Tune hyperparameters

### 5. Evaluation
- Assess model performance
- Validate against business objectives
- Determine next steps

### 6. Deployment
- Plan deployment strategy
- Implement model in production
- Monitor and maintain

## Best Practices

### Data Preparation

1. **Handle missing values appropriately**
   - Imputation strategies
   - Consider missingness patterns
   - Document decisions

2. **Scale features when necessary**
   - Distance-based algorithms (K-Means, DBSCAN) require scaling
   - Tree-based algorithms don't require scaling

3. **Encode categorical variables**
   - One-hot encoding for nominal categories
   - Ordinal encoding for ordered categories

### Model Selection

1. **Match algorithm to problem type**
   - Association rules for relationship discovery
   - Clustering for segmentation
   - Classification for prediction

2. **Consider interpretability vs. accuracy trade-off**
   - Decision trees: interpretable
   - Random forests: more accurate, less interpretable

3. **Validate thoroughly**
   - Cross-validation
   - Hold-out test set
   - Domain expert review

### Performance Optimization

1. **Use appropriate data structures**
   - Sparse matrices for high-dimensional data
   - Efficient storage formats

2. **Leverage parallel processing**
   - Many algorithms support n_jobs parameter
   - Distribute computation across cores

3. **Sample large datasets**
   - Stratified sampling preserves distributions
   - Incremental learning for very large datasets

## Common Challenges

### Curse of Dimensionality

**Problem**: Performance degrades with many features
**Solutions**:
- Feature selection
- Dimensionality reduction (PCA, t-SNE)
- Regularization

### Imbalanced Data

**Problem**: Rare class underrepresented
**Solutions**:
- Resampling (SMOTE, undersampling)
- Class weights
- Anomaly detection instead of classification

### Scalability

**Problem**: Algorithms don't scale to large datasets
**Solutions**:
- Mini-batch processing
- Approximate algorithms
- Distributed computing (Spark MLlib)

## Using the Reference Files

### When to Read Each Reference

**`/references/association-rules-advanced.md`** — Read when implementing market basket analysis, optimizing Apriori/FP-Growth parameters, or working with large transaction datasets.

**`/references/clustering-comprehensive.md`** — Read when performing customer segmentation, comparing clustering algorithms, or evaluating cluster quality.

**`/references/classification-methods.md`** — Read when building predictive models, handling imbalanced data, or optimizing classification performance.

**`/references/anomaly-detection-techniques.md`** — Read when detecting fraud, identifying network intrusions, or finding unusual patterns in data.

**`/references/data-mining-case-studies.md`** — Read when starting a new data mining project or looking for real-world application examples.
