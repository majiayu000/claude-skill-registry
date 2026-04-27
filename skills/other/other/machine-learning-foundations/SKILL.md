---
name: machine-learning-foundations
description: Supervised and unsupervised learning, bias-variance tradeoff, cross-validation, decision trees, ensemble methods, neural network fundamentals, and the practitioner's workflow from problem framing through deployment. Covers classification, regression, clustering, dimensionality reduction, regularization, hyperparameter tuning, and evaluation metrics. Use when building predictive models, selecting algorithms, or understanding the machine learning pipeline.
type: skill
category: data-science
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/data-science/machine-learning-foundations/SKILL.md
superseded_by: null
---
# Machine Learning Foundations

Machine learning is the practice of building systems that learn patterns from data and use those patterns to make predictions or decisions on new data. Where statistical modeling (the inference culture) asks "what is the relationship between X and Y?", machine learning (the prediction culture) asks "given X, what is the best prediction of Y?" This skill covers the foundational concepts, algorithms, and workflow of machine learning from the practitioner's perspective.

**Agent affinity:** breiman (algorithm selection, ensemble methods), tukey (feature engineering, EDA)

**Concept IDs:** data-correlation, data-distributions, data-measures-of-spread, data-hypothesis-testing

## The ML Workflow

| Stage | Goal | Key operations |
|---|---|---|
| 1. Problem framing | Define the task precisely | Classification vs. regression vs. clustering; define target variable and success metric |
| 2. Data collection | Assemble training data | Sources, sampling, labeling; ensure data represents the deployment population |
| 3. Feature engineering | Create informative inputs | Domain-driven features, transformations, encoding categoricals |
| 4. Train/test split | Prevent overfitting evaluation | Hold out 20-30% for testing; never touch test set during development |
| 5. Model selection | Choose algorithm family | Based on data size, interpretability needs, problem structure |
| 6. Training | Fit model parameters | Optimization (gradient descent, tree splitting, etc.) |
| 7. Validation | Tune hyperparameters | k-fold cross-validation on training set only |
| 8. Evaluation | Assess on held-out test set | Metrics appropriate to the problem (accuracy, F1, RMSE, etc.) |
| 9. Interpretation | Understand what the model learned | Feature importance, partial dependence, SHAP values |
| 10. Deployment | Put the model in production | Monitoring, drift detection, retraining schedule |

## Supervised Learning

### Classification

The task: given features X, predict a categorical label y.

**Key algorithms:**

| Algorithm | Strengths | Weaknesses | When to use |
|---|---|---|---|
| **Logistic regression** | Interpretable, fast, probabilistic | Linear decision boundary | Baseline; when interpretability matters |
| **k-Nearest Neighbors** | Non-parametric, no training phase | Slow at prediction, curse of dimensionality | Small datasets, low dimensionality |
| **Decision tree** | Interpretable, handles mixed types | Overfits easily, unstable | When interpretability is paramount; as building block for ensembles |
| **Random forest** | Robust, handles high dimensions | Less interpretable than single tree | Default for tabular data |
| **Gradient boosting** | State-of-the-art tabular performance | Prone to overfitting without tuning | Competition-grade tabular prediction |
| **SVM** | Effective in high dimensions | Slow on large datasets, kernel choice | Text classification, small-medium datasets |
| **Neural network** | Learns complex patterns, scales to huge data | Requires large data, expensive, black box | Images, text, sequences, very large datasets |

### Regression

The task: given features X, predict a continuous value y.

Same algorithms apply (linear regression, k-NN regression, decision tree regression, random forest regression, gradient boosting regression, neural network regression). The loss function changes from cross-entropy to squared error (or absolute error, Huber loss, etc.).

### Evaluation Metrics

**Classification:**

| Metric | Formula / Definition | When to use |
|---|---|---|
| **Accuracy** | Correct / Total | Balanced classes only |
| **Precision** | TP / (TP + FP) | Cost of false positives is high (spam detection) |
| **Recall** | TP / (TP + FN) | Cost of false negatives is high (cancer screening) |
| **F1 score** | 2 * Precision * Recall / (Precision + Recall) | Need balance between precision and recall |
| **ROC-AUC** | Area under ROC curve | Ranking quality across thresholds |
| **Log loss** | Negative log-likelihood of predicted probabilities | When calibrated probabilities matter |

**Regression:**

| Metric | Formula / Definition | When to use |
|---|---|---|
| **MSE** | Mean of (y - y_hat)^2 | Default; penalizes large errors |
| **RMSE** | sqrt(MSE) | Same scale as y; more interpretable |
| **MAE** | Mean of |y - y_hat| | Robust to outliers |
| **R-squared** | 1 - (SS_res / SS_tot) | Proportion of variance explained |
| **MAPE** | Mean of |y - y_hat| / |y| * 100 | Percentage interpretation; fails when y near 0 |

## The Bias-Variance Tradeoff

The expected prediction error decomposes into three components:

Error = Bias^2 + Variance + Irreducible noise

- **Bias:** Error from oversimplifying the model. A linear model fit to a quadratic relationship has high bias (underfitting).
- **Variance:** Error from model sensitivity to training data. A deep decision tree memorizes the training set and varies wildly across samples (overfitting).
- **Irreducible noise:** Inherent randomness in the data. No model can reduce this.

**The tradeoff:** Increasing model complexity reduces bias but increases variance. Decreasing complexity reduces variance but increases bias. The optimal model balances both.

**Regularization** controls this tradeoff by penalizing complexity:

| Method | Penalty | Effect |
|---|---|---|
| **Ridge (L2)** | Sum of beta_j^2 | Shrinks coefficients toward zero; keeps all predictors |
| **Lasso (L1)** | Sum of |beta_j| | Shrinks coefficients; sets some exactly to zero (feature selection) |
| **Elastic net** | Alpha * L1 + (1 - Alpha) * L2 | Combines ridge and lasso benefits |
| **Tree depth limit** | Max depth, min samples per leaf | Prevents tree from memorizing noise |
| **Dropout** | Randomly zero out neurons during training | Prevents neural network co-adaptation |
| **Early stopping** | Stop training when validation error increases | Universal; works for any iterative algorithm |

## Cross-Validation

Cross-validation estimates out-of-sample performance using only the training data.

### k-Fold Cross-Validation

1. Split training data into k equal folds (k = 5 or 10 is standard).
2. For each fold i: train on all folds except i, evaluate on fold i.
3. Average performance across all k evaluations.
4. Use this average to select hyperparameters.

### Critical Rules

- **Never use test data for any decision during training.** The test set is opened exactly once, at the very end.
- **Stratified k-fold for classification.** Preserve class proportions in each fold.
- **Group k-fold for grouped data.** If observations belong to groups (e.g., multiple images from the same patient), all observations from a group must be in the same fold.
- **Time series split for temporal data.** Training set always precedes validation set in time. No random shuffling.

## Decision Trees

### How They Work

A decision tree recursively partitions the feature space by choosing splits that maximize information gain (classification) or minimize mean squared error (regression).

**Splitting criteria for classification:**

- **Gini impurity:** G = 1 - sum(p_k^2). Measures probability of misclassification.
- **Entropy:** H = -sum(p_k * log(p_k)). Information-theoretic measure of impurity.
- **In practice:** Gini and entropy produce nearly identical trees. Gini is slightly faster to compute.

**Controlling complexity:**

| Parameter | Effect |
|---|---|
| Max depth | Limits tree height; primary regularization lever |
| Min samples split | Minimum observations to attempt a split |
| Min samples leaf | Minimum observations in a terminal node |
| Max features | Number of features considered at each split (critical for random forests) |

### Why Single Trees Overfit

A fully grown tree achieves 100% training accuracy by creating one leaf per observation. This is pure memorization. The tree's variance is enormous -- small changes in training data produce completely different trees. This instability is why ensemble methods exist.

## Ensemble Methods

### Bagging (Bootstrap Aggregating)

Train multiple models on bootstrap samples (random samples with replacement) and average their predictions. Reduces variance without increasing bias.

**Random forest** = bagging + random feature subsets at each split. The feature randomization decorrelates the trees, making the average more effective. Random forests are the default algorithm for tabular data because they work well out of the box with minimal tuning.

### Boosting

Train models sequentially, with each new model correcting the errors of the previous ensemble:

- **AdaBoost:** Reweights misclassified observations. Simple but sensitive to outliers.
- **Gradient boosting:** Fits each new tree to the residuals (negative gradient of the loss function). More general and powerful.
- **XGBoost / LightGBM / CatBoost:** Optimized gradient boosting implementations with regularization, parallel training, and categorical handling. State-of-the-art for tabular data competitions.

### Bagging vs. Boosting

| Property | Bagging (Random Forest) | Boosting (Gradient Boosting) |
|---|---|---|
| Reduces | Variance | Bias (primarily) + variance |
| Training | Parallel (fast) | Sequential (slower) |
| Overfitting risk | Low | Higher without tuning |
| Tuning effort | Minimal | Significant (learning rate, depth, iterations) |
| Default choice | Yes, for most tabular problems | When you need maximum performance and will tune |

## Unsupervised Learning

### Clustering

Grouping observations without labels.

| Algorithm | Assumption | Strengths | Weaknesses |
|---|---|---|---|
| **k-Means** | Spherical, equal-size clusters | Fast, scalable | Must specify k; sensitive to initialization |
| **DBSCAN** | Density-based clusters | Finds arbitrary shapes, handles noise | Sensitive to epsilon and min_samples parameters |
| **Hierarchical** | Nested cluster structure | Dendrogram visualization, no k needed | O(n^2) or worse; not for large datasets |
| **Gaussian Mixture** | Elliptical clusters | Soft assignments (probabilities) | Must specify k; can converge to local optima |

**Choosing k:** Elbow method (plot inertia vs. k), silhouette scores, domain knowledge. There is no universally correct k -- clustering is exploratory, not definitive.

### Dimensionality Reduction

| Method | Linear? | Preserves | Use when |
|---|---|---|---|
| **PCA** | Yes | Global variance | High-dimensional data, preprocessing for modeling |
| **t-SNE** | No | Local neighbor structure | 2D/3D visualization of high-dimensional data |
| **UMAP** | No | Local + some global structure | Faster than t-SNE, better global structure |

## Neural Networks Introduction

### Architecture

A neural network is a composition of linear transformations and non-linear activations:

output = f_L(W_L * f_{L-1}(W_{L-1} * ... f_1(W_1 * x + b_1) ... + b_{L-1}) + b_L)

- **Input layer:** Feature vector x.
- **Hidden layers:** Each applies a linear transformation (W * x + b) followed by an activation function (ReLU, sigmoid, tanh).
- **Output layer:** Sigmoid for binary classification, softmax for multiclass, linear for regression.

### Training

- **Loss function:** Cross-entropy (classification), MSE (regression).
- **Optimization:** Stochastic gradient descent (SGD) and variants (Adam, RMSProp).
- **Backpropagation:** Chain rule applied to compute gradients through the network.
- **Batch size:** Mini-batches (32-256) balance noise and computation.
- **Learning rate:** Most important hyperparameter. Too high -> divergence. Too low -> slow convergence.

### When to Use Neural Networks

Neural networks excel when data is large (>100K samples), structured (images, text, sequences), and the relationship is highly non-linear. For tabular data with <10K samples, gradient boosting typically wins. Neural networks are not magic -- they are function approximators that need sufficient data to justify their complexity.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Data leakage | Future information in training features | Audit every feature for temporal leakage |
| Not holding out a test set | Reported performance is overly optimistic | Split before any modeling decisions |
| Using accuracy on imbalanced data | 95% accuracy is trivial when 95% of data is one class | Use F1, precision-recall, or balanced accuracy |
| Tuning on the test set | Test performance becomes optimistic | Tune on validation/CV only; test set opened once |
| Feature scaling mismatch | Fit scaler on full data, including test | Fit scaler on training data only, transform test with same scaler |
| Ignoring class imbalance | Model predicts majority class for everything | Oversampling (SMOTE), class weights, or threshold adjustment |

## Cross-References

- **breiman agent:** Algorithm selection, random forests, and the "two cultures" perspective on prediction vs. inference.
- **tukey agent:** Exploratory analysis and feature engineering that precede model training.
- **cairo agent:** Communicating model results through visualization -- feature importance plots, partial dependence, calibration curves.
- **statistical-modeling skill:** The inference-focused counterpart to this prediction-focused skill.
- **data-wrangling skill:** Data preparation pipeline that produces training-ready features.
- **ethics-governance skill:** Algorithmic bias, fairness metrics, and responsible deployment of ML models.

## References

- Breiman, L. (2001). "Random Forests." *Machine Learning*, 45(1), 5-32.
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning*. 2nd edition. Springer.
- James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning*. 2nd edition. Springer.
- Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.
- Chen, T. & Guestrin, C. (2016). "XGBoost: A Scalable Tree Boosting System." *Proceedings of KDD*, 785-794.
