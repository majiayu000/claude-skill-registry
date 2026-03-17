---
name: data-scientist
description: Expert in statistical analysis, predictive modeling, machine learning, and data storytelling to drive business insights.
---

# Data Scientist

## Purpose

Provides statistical analysis and predictive modeling expertise specializing in machine learning, experimental design, and causal inference. Builds rigorous models and translates complex statistical findings into actionable business insights with proper validation and uncertainty quantification.

## When to Use

- Performing exploratory data analysis (EDA) to find patterns and anomalies
- Building predictive models (classification, regression, forecasting)
- Designing and analyzing A/B tests or experiments
- Conducting rigorous statistical hypothesis testing
- Creating advanced visualizations and data narratives
- Defining metrics and KPIs for business problems

---
---

## Core Capabilities

### Statistical Modeling
- Building predictive models using regression, classification, and clustering
- Implementing time series forecasting and causal inference
- Designing and analyzing A/B tests and experiments
- Performing feature engineering and selection

### Machine Learning
- Training and evaluating supervised and unsupervised learning models
- Implementing deep learning models for complex patterns
- Performing hyperparameter tuning and model optimization
- Validating models with cross-validation and holdout sets

### Data Exploration
- Conducting exploratory data analysis (EDA) to discover patterns
- Identifying anomalies and outliers in datasets
- Creating advanced visualizations for insight discovery
- Generating hypotheses from data exploration

### Communication and Storytelling
- Translating statistical findings into business language
- Creating compelling data narratives for stakeholders
- Building interactive notebooks and reports
- Presenting findings with uncertainty quantification

---
---

## 3. Core Workflows

### Workflow 1: Exploratory Data Analysis (EDA) & Cleaning

**Goal:** Understand data distribution, quality, and relationships before modeling.

**Steps:**

1.  **Load and Profile Data**
    ```python
    import pandas as pd
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt

    # Load data
    df = pd.read_csv("customer_data.csv")

    # Basic profiling
    print(df.info())
    print(df.describe())
    
    # Missing values analysis
    missing = df.isnull().sum() / len(df)
    print(missing[missing > 0].sort_values(ascending=False))
    ```

2.  **Univariate Analysis (Distributions)**
    ```python
    # Numerical features
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        sns.histplot(df[col], kde=True)
        plt.subplot(1, 2, 2)
        sns.boxplot(x=df[col])
        plt.show()

    # Categorical features
    cat_cols = df.select_dtypes(exclude=[np.number]).columns
    for col in cat_cols:
        print(df[col].value_counts(normalize=True))
    ```

3.  **Bivariate Analysis (Relationships)**
    ```python
    # Correlation matrix
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    
    # Target vs Features
    target = 'churn'
    sns.boxplot(x=target, y='tenure', data=df)
    ```

4.  **Data Cleaning**
    ```python
    # Impute missing values
    df['age'].fillna(df['age'].median(), inplace=True)
    df['category'].fillna('Unknown', inplace=True)
    
    # Handle outliers (Example: Cap at 99th percentile)
    cap = df['income'].quantile(0.99)
    df['income'] = np.where(df['income'] > cap, cap, df['income'])
    ```

**Verification:**
-   No missing values in critical columns.
-   Distributions understood (normal vs skewed).
-   Target variable balance checked.

---
---

### Workflow 3: A/B Test Analysis

**Goal:** Analyze results of a website conversion experiment.

**Steps:**

1.  **Define Hypothesis**
    -   H0: Conversion Rate B <= Conversion Rate A
    -   H1: Conversion Rate B > Conversion Rate A
    -   Alpha: 0.05

2.  **Load and Aggregate Data**
    ```python
    # data: ['user_id', 'group', 'converted']
    results = df.groupby('group')['converted'].agg(['count', 'sum', 'mean'])
    results.columns = ['n_users', 'conversions', 'conversion_rate']
    print(results)
    ```

3.  **Statistical Test (Proportions Z-test)**
    ```python
    from statsmodels.stats.proportion import proportions_ztest

    control = results.loc['A']
    treatment = results.loc['B']

    count = np.array([treatment['conversions'], control['conversions']])
    nobs = np.array([treatment['n_users'], control['n_users']])

    stat, p_value = proportions_ztest(count, nobs, alternative='larger')
    
    print(f"Z-statistic: {stat:.4f}")
    print(f"P-value: {p_value:.4f}")
    ```

4.  **Confidence Intervals**
    ```python
    from statsmodels.stats.proportion import proportion_confint
    
    (lower_con, lower_treat), (upper_con, upper_treat) = proportion_confint(count, nobs, alpha=0.05)
    
    print(f"Control CI: [{lower_con:.4f}, {upper_con:.4f}]")
    print(f"Treatment CI: [{lower_treat:.4f}, {upper_treat:.4f}]")
    ```

5.  **Conclusion**
    -   If p-value < 0.05: Reject H0. Variation B is statistically significantly better.
    -   Check practical significance (Lift magnitude).

---
---

### Workflow 5: Causal Inference (Propensity Score Matching)

**Goal:** Estimate impact of a "Premium Membership" on "Spend" when A/B test isn't possible (observational data).

**Steps:**

1.  **Problem Setup**
    -   Treatment: Premium Member (1) vs Free (0)
    -   Outcome: Annual Spend ($)
    -   Confounders: Age, Income, Location, Tenure (Factors affecting both membership and spend)

2.  **Calculate Propensity Scores**
    ```python
    from sklearn.linear_model import LogisticRegression
    
    # P(Treatment=1 | Confounders)
    confounders = ['age', 'income', 'tenure']
    logit = LogisticRegression()
    logit.fit(df[confounders], df['is_premium'])
    
    df['propensity_score'] = logit.predict_proba(df[confounders])[:, 1]
    
    # Check overlap (Common Support)
    sns.histplot(data=df, x='propensity_score', hue='is_premium', element='step')
    ```

3.  **Matching (Nearest Neighbor)**
    ```python
    from sklearn.neighbors import NearestNeighbors
    
    # Separate groups
    treatment = df[df['is_premium'] == 1]
    control = df[df['is_premium'] == 0]
    
    # Find neighbors for treatment group in control group
    nn = NearestNeighbors(n_neighbors=1, algorithm='ball_tree')
    nn.fit(control[['propensity_score']])
    
    distances, indices = nn.kneighbors(treatment[['propensity_score']])
    
    # Create matched dataframe
    matched_control = control.iloc[indices.flatten()]
    
    # Compare outcomes
    ate = treatment['spend'].mean() - matched_control['spend'].mean()
    print(f"Average Treatment Effect (ATE): ${ate:.2f}")
    ```

4.  **Validation (Balance Check)**
    -   Check if confounders are balanced after matching (e.g., Mean Age of Treatment vs Matched Control should be similar).
    -   `abs(mean_diff) / pooled_std < 0.1` (Standardized Mean Difference).

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: Data Leakage

**What it looks like:**
-   Scaling/Standardizing the entire dataset *before* train/test split.
-   Using future information (e.g., "next_month_churn") as a feature.
-   Including target-derived features (e.g., mean target encoding) calculated on the whole set.

**Why it fails:**
-   Model performance is artificially inflated during training/validation.
-   Fails completely in production on new, unseen data.

**Correct approach:**
-   **Split FIRST**, then transform.
-   Fit scalers/encoders ONLY on `X_train`, then transform `X_test`.
-   Use `Pipeline` objects to ensure safety.

### ❌ Anti-Pattern 2: P-Hacking (Data Dredging)

**What it looks like:**
-   Testing 50 different hypotheses or subgroups.
-   Reporting only the one result with p < 0.05.
-   Stopping an A/B test exactly when significance is reached (peeking).

**Why it fails:**
-   High probability of False Positives (Type I error).
-   Findings are random noise, not reproducible effects.

**Correct approach:**
-   Pre-register hypotheses.
-   Apply **Bonferroni correction** or False Discovery Rate (FDR) control for multiple comparisons.
-   Determine sample size *before* the experiment and stick to it.

### ❌ Anti-Pattern 3: Ignoring Imbalanced Classes

**What it looks like:**
-   Training a fraud detection model on data with 0.1% fraud.
-   Reporting 99.9% Accuracy as "Success".

**Why it fails:**
-   The model simply predicts "No Fraud" for everyone.
-   Fails to detect the actual class of interest.

**Correct approach:**
-   Use appropriate metrics: **Precision-Recall AUC**, **F1-Score**.
-   Resampling techniques: **SMOTE** (Synthetic Minority Over-sampling Technique), Random Undersampling.
-   Class weights: `scale_pos_weight` in XGBoost, `class_weight='balanced'` in Sklearn.

---
---

## 7. Quality Checklist

**Methodology & Rigor:**
-   [ ] Hypothesis defined clearly *before* analysis.
-   [ ] Assumptions checked (normality, independence, homoscedasticity) for statistical tests.
-   [ ] Train/Test/Validation split performed correctly (no leakage).
-   [ ] Imbalanced classes handled appropriate (metrics, resampling).
-   [ ] Cross-validation used for model assessment.

**Code & Reproducibility:**
-   [ ] Code stored in git with `requirements.txt` or `environment.yml`.
-   [ ] Random seeds set for reproducibility (`random_state=42`).
-   [ ] Hardcoded paths replaced with relative paths or config variables.
-   [ ] Complex logic wrapped in functions/classes with docstrings.

**Interpretation & Communication:**
-   [ ] Results interpreted in business terms (e.g., "Revenue lift" vs "Log-loss decrease").
-   [ ] Confidence intervals provided for estimates.
-   [ ] "Black box" models explained using SHAP or LIME if needed.
-   [ ] Caveats and limitations explicitly stated.

**Performance:**
-   [ ] EDA performed on sampled data if dataset > 10GB.
-   [ ] Vectorized operations used (pandas/numpy) instead of loops.
-   [ ] Query optimized (filtering early, selecting only needed columns).

## Examples

### Example 1: A/B Test Analysis for Feature Launch

**Scenario:** Product team wants to know if a new recommendation algorithm increases user engagement.

**Analysis Approach:**
1. **Experimental Design**: Random assignment (50/50), minimum sample size calculation
2. **Data Collection**: Tracked click-through rate, time on page, conversion
3. **Statistical Testing**: Two-sample t-test with bootstrapped confidence intervals
4. **Results**: Significant improvement in CTR (p < 0.01), 12% lift

**Key Analysis:**
```python
# Bootstrap confidence interval for difference in means
from scipy import stats
diff = treatment_means - control_means
ci = np.percentile(bootstrap_diffs, [2.5, 97.5])
```

**Outcome:** Feature launched with 95% probability of positive impact

### Example 2: Time Series Forecasting for Demand Planning

**Scenario:** Retail chain needs to forecast next-quarter sales for inventory planning.

**Modeling Approach:**
1. **Exploratory Analysis**: Identified trends, seasonality (weekly, holiday)
2. **Feature Engineering**: Promotions, weather, economic indicators
3. **Model Selection**: Compared ARIMA, Prophet, and gradient boosting
4. **Validation**: Walk-forward validation on last 12 months

**Results:**
| Model | MAPE | 90% CI Width |
|-------|------|--------------|
| ARIMA | 12.3% | ±15% |
| Prophet | 9.8% | ±12% |
| XGBoost | 7.2% | ±9% |

**Deliverable:** Production model with automated retraining pipeline

### Example 3: Causal Attribution Analysis

**Scenario:** Marketing wants to understand which channels drive actual conversions vs. appear correlated.

**Causal Methods:**
1. **Propensity Score Matching**: Match users with similar characteristics
2. **Difference-in-Differences**: Compare changes before/after campaigns
3. **Instrumental Variables**: Address selection bias in observational data

**Key Findings:**
- TV ads: 3.2x ROAS (strongest attribution)
- Social media: 1.1x ROAS (attribution unclear)
- Email: 5.8x ROAS (highest efficiency)

## Best Practices

### Experimental Design

- **Randomization**: Ensure true random assignment to treatment/control
- **Sample Size Calculation**: Power analysis before starting experiments
- **Multiple Testing**: Adjust significance levels when testing multiple hypotheses
- **Control Variables**: Include relevant covariates to reduce variance
- **Duration Planning**: Run experiments long enough for stable results

### Model Development

- **Feature Engineering**: Create interpretable, predictive features
- **Cross-Validation**: Use time-aware splits for time series data
- **Model Interpretability**: Use SHAP/LIME to explain predictions
- **Validation Metrics**: Choose metrics aligned with business objectives
- **Overfitting Prevention**: Regularization, early stopping, held-out data

### Statistical Rigor

- **Uncertainty Quantification**: Always report confidence intervals
- **Significance Interpretation**: P-value is not effect size
- **Assumption Checking**: Validate statistical test assumptions
- **Sensitivity Analysis**: Test robustness to modeling choices
- **Pre-registration**: Document analysis plan before seeing results

### Communication and Impact

- **Business Translation**: Convert statistical terms to business impact
- **Actionable Recommendations**: Tie findings to specific decisions
- **Visual Storytelling**: Create compelling narratives from data
- **Stakeholder Communication**: Tailor level of technical detail
- **Documentation**: Maintain reproducible analysis records

### Ethical Data Science

- **Fairness Considerations**: Check for bias across protected groups
- **Privacy Protection**: Anonymize sensitive data appropriately
- **Transparency**: Document data sources and methodology
- **Responsible AI**: Consider societal impact of models
- **Data Quality**: Acknowledge limitations and potential biases
