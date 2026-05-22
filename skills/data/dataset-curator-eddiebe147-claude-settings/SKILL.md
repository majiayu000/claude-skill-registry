---
name: Dataset Curator
slug: dataset-curator
description: Curate and clean training datasets for high-quality machine learning
category: ai-ml
complexity: intermediate
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "curate dataset"
  - "clean training data"
  - "prepare dataset"
  - "data quality"
  - "dataset curation"
tags:
  - data-curation
  - data-quality
  - training-data
  - machine-learning
  - data-cleaning
---

# Dataset Curator

The Dataset Curator skill guides you through the critical process of preparing high-quality training data for machine learning models. Data quality is the single most important factor in model performance, yet it is often underinvested. This skill helps you systematically clean, validate, augment, and maintain datasets that lead to better models.

From initial collection to ongoing maintenance, this skill covers deduplication, label quality assessment, bias detection, augmentation strategies, and version control. It applies best practices from production ML systems to ensure your datasets are not just clean, but strategically optimized for your learning objectives.

Whether you are building a classifier, fine-tuning an LLM, or training a custom model, this skill ensures your data foundation is solid.

## Core Workflows

### Workflow 1: Assess Dataset Quality
1. **Profile** the dataset:
   - Size and dimensionality
   - Label distribution and balance
   - Missing value patterns
   - Feature statistics
2. **Identify** quality issues:
   - Duplicates (exact and near-duplicate)
   - Mislabeled examples
   - Outliers and anomalies
   - Data leakage
   - Bias and representation gaps
3. **Measure** quality metrics:
   ```python
   def assess_quality(dataset):
       return {
           "size": len(dataset),
           "duplicate_rate": find_duplicates(dataset).ratio,
           "missing_rate": dataset.isnull().mean(),
           "label_balance": compute_entropy(dataset.labels),
           "outlier_rate": detect_outliers(dataset).ratio,
           "estimated_label_noise": estimate_label_noise(dataset)
       }
   ```
4. **Prioritize** issues by impact
5. **Create** remediation plan

### Workflow 2: Clean and Prepare Data
1. **Remove** duplicates:
   - Exact duplicates: hash-based dedup
   - Near-duplicates: similarity-based clustering
   - Decide: keep first, best, or merge
2. **Handle** missing values:
   - Understand missingness mechanism (MCAR, MAR, MNAR)
   - Impute, drop, or flag appropriately
3. **Fix** label quality:
   - Identify likely mislabels with confidence scoring
   - Route to human review or automatic correction
   - Document labeling guidelines
4. **Normalize** and standardize:
   - Consistent formatting
   - Schema validation
   - Encoding standardization
5. **Validate** cleaned dataset

### Workflow 3: Augment and Balance
1. **Analyze** class imbalance:
   - Compute imbalance ratios
   - Assess impact on model training
2. **Apply** balancing strategies:
   - Oversampling minority classes (SMOTE, random)
   - Undersampling majority classes
   - Class weights in training
3. **Generate** augmentations:
   - Text: paraphrase, synonym substitution, back-translation
   - Image: rotation, flip, color jitter, mixup
   - Tabular: noise injection, feature perturbation
4. **Validate** augmentation quality:
   - Ensure augmented samples are realistic
   - Check for introduced biases
5. **Version** and document changes

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Assess quality | "Check quality of this dataset" |
| Find duplicates | "Find duplicates in dataset" |
| Clean labels | "Fix mislabeled data" |
| Balance classes | "Handle class imbalance" |
| Augment data | "Augment dataset for [task]" |
| Version dataset | "Set up dataset versioning" |

## Best Practices

- **Profile Before Processing**: Understand your data before changing it
  - Compute statistics and visualize distributions
  - Document original state for reference
  - Identify patterns in issues

- **Preserve Provenance**: Track every transformation
  - Version control datasets like code
  - Log all cleaning operations
  - Maintain mapping between original and cleaned data

- **Prioritize Label Quality**: Garbage labels in, garbage model out
  - Invest in clear labeling guidelines
  - Use multiple annotators and measure agreement
  - Regular quality audits of labels

- **Test Cleaning Impact**: Measure effect of cleaning
  - Train models on original vs cleaned data
  - Track which cleaning steps help most
  - Avoid cleaning that hurts performance

- **Stratify Splits Carefully**: Maintain distribution in train/val/test
  - Stratify by label and key features
  - Keep related samples in same split
  - Ensure temporal ordering if applicable

- **Document Everything**: Future you will thank present you
  - Dataset cards with key statistics
  - Known issues and limitations
  - Collection methodology and biases

## Advanced Techniques

### Confident Learning for Label Noise
Identify and fix mislabeled examples:
```python
from cleanlab import find_label_issues

# Train model to get predicted probabilities
model.fit(X_train, y_train)
pred_probs = model.predict_proba(X_train)

# Find likely mislabeled examples
issues = find_label_issues(
    labels=y_train,
    pred_probs=pred_probs,
    return_indices_ranked_by="self_confidence"
)

# Review and correct top issues
for idx in issues[:100]:
    review_and_correct(X_train[idx], y_train[idx])
```

### Similarity-Based Deduplication
Remove near-duplicates using embeddings:
```python
def deduplicate_semantic(texts, threshold=0.95):
    embeddings = embed(texts)
    clusters = cluster_by_similarity(embeddings, threshold)

    # Keep one representative per cluster
    deduplicated = []
    for cluster in clusters:
        representative = select_best(cluster)  # longest, most recent, etc.
        deduplicated.append(representative)

    return deduplicated
```

### Active Learning for Efficient Labeling
Prioritize labeling effort:
```python
def active_learning_loop(unlabeled_pool, labeled_set, budget):
    while len(labeled_set) < budget:
        # Train on current labeled data
        model.fit(labeled_set)

        # Score unlabeled by uncertainty
        uncertainties = model.uncertainty(unlabeled_pool)

        # Select most uncertain for labeling
        to_label = select_top_k(unlabeled_pool, uncertainties, k=10)
        labels = human_label(to_label)

        # Update sets
        labeled_set.add(to_label, labels)
        unlabeled_pool.remove(to_label)

    return labeled_set
```

### Data Slice Analysis
Find problematic subgroups:
```python
def find_weak_slices(model, data, features):
    # Evaluate on all slices
    slices = generate_slices(data, features)

    weak_slices = []
    for slice_name, slice_data in slices:
        performance = evaluate(model, slice_data)
        if performance < overall_performance - threshold:
            weak_slices.append({
                "slice": slice_name,
                "size": len(slice_data),
                "performance": performance
            })

    return sorted(weak_slices, key=lambda x: x["performance"])
```

## Common Pitfalls to Avoid

- Cleaning test data the same way as training data (causes leakage)
- Over-aggressive deduplication that removes valid variations
- Imputing values without understanding the missingness mechanism
- Augmenting in ways that introduce unrealistic examples
- Ignoring class imbalance until model training fails
- Not versioning datasets, making experiments irreproducible
- Assuming more data is always better (quality > quantity)
- Failing to document data collection biases and limitations
