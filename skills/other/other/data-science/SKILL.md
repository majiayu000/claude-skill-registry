---
name: data-science
version: 0.1.0
description: >
  Use this skill when performing exploratory data analysis, statistical testing,
  data visualization, or building predictive models. Triggers on EDA, pandas,
  matplotlib, seaborn, hypothesis testing, A/B test analysis, correlation,
  regression, feature engineering, and any task requiring data analysis or
  statistical inference.
category: ai-ml
tags: [data-science, eda, statistics, visualization, pandas, analysis]
recommended_skills: [analytics-engineering, data-pipelines, nlp-engineering, computer-vision]
platforms:
  - claude-code
  - gemini-cli
  - openai-codex
license: MIT
maintainers:
  - github: maddhruv
---

When this skill is activated, always start your first response with the 🧢 emoji.

# Data Science

A practitioner's guide for exploratory data analysis, statistical inference, and
predictive modeling. Covers the full analytical workflow - from raw data to
reproducible conclusions - with an emphasis on *when* to apply each technique, not
just *how*. Designed for engineers and analysts who can code but need opinionated
guidance on statistical rigor and common traps.

---

## When to use this skill

Trigger this skill when the user:
- Loads a new dataset and wants to understand its structure and distributions
- Needs to clean, reshape, or impute missing data in a pandas DataFrame
- Runs a hypothesis test (t-test, chi-square, ANOVA, Mann-Whitney)
- Analyzes an A/B test or experiment result for statistical significance
- Builds a correlation matrix or investigates feature relationships
- Plots distributions, trends, or model diagnostics with matplotlib or seaborn
- Engineers features for a machine learning model
- Fits a linear or logistic regression and needs to interpret coefficients
- Calculates confidence intervals, p-values, or effect sizes
- Needs to choose the right statistical test for their data type

Do NOT trigger this skill for:
- Deep learning / neural network architecture (use an ML engineering skill)
- Data engineering pipelines, ETL, or streaming (use a data engineering skill)

---

## Key principles

1. **Visualize before modeling** - Plot every variable before fitting anything.
   Distributions, outliers, and relationships invisible in summary statistics leap
   out in charts. A histogram takes 2 seconds; debugging a model trained on bad
   assumptions takes days.

2. **Check your assumptions** - Every statistical test has assumptions (normality,
   equal variance, independence). Violating them silently produces misleading results.
   Run the assumption check first, then choose the test.

3. **Correlation is not causation** - A strong correlation between X and Y might
   mean X causes Y, Y causes X, a third variable Z causes both, or pure coincidence.
   Never state causation from observational data without a causal framework.

4. **Validate on holdout data** - Any model evaluated on the same data it was trained
   on is measuring memorization, not learning. Always split before fitting; never
   peek at the test set to tune parameters.

5. **Reproducible notebooks** - Set random seeds (`np.random.seed`, `random_state`),
   pin library versions, and document every data transformation in order. A result
   you cannot reproduce is not a result.

---

## Core concepts

**Distributions** describe how values are spread: normal (bell curve), skewed,
bimodal, uniform. Knowing the shape tells you which statistics are meaningful
(mean vs. median) and which tests are valid.

**Central Limit Theorem** - the mean of a large enough sample is approximately
normally distributed regardless of the population distribution. This is why t-tests
work on non-normal data with n > 30.

**p-values** measure the probability of observing your data (or more extreme) if
the null hypothesis were true. They do NOT measure the probability the null is true,
the effect size, or practical significance. A p-value < 0.05 is a threshold, not a
truth detector.

**Confidence intervals** give the range of plausible values for a parameter. A 95%
CI means: if you repeated the experiment 100 times, ~95 intervals would contain the
true value. Always report CIs alongside p-values - a significant result with a CI
spanning near-zero means the effect is tiny.

**Bias-variance tradeoff** - underfitting (high bias) means the model is too simple
to capture the signal; overfitting (high variance) means it captures noise too.
Cross-validation is the primary tool for diagnosing which problem you have.

---

## Common tasks

### EDA workflow

Load data and profile it systematically before any analysis:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data.csv")

# Shape, types, missing values
print(df.shape)
print(df.dtypes)
print(df.isnull().sum().sort_values(ascending=False))

# Numeric summary
print(df.describe())

# Categorical value counts
for col in df.select_dtypes("object"):
    print(f"\n{col}:\n{df[col].value_counts().head(10)}")

# Distribution of each numeric feature
df.hist(bins=30, figsize=(14, 10))
plt.tight_layout()
plt.show()

# Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(
    df.select_dtypes("number").corr(),
    annot=True, fmt=".2f", cmap="coolwarm", center=0
)
plt.show()
```

> Always check `df.duplicated().sum()` and `df.dtypes` - columns that should be
> numeric but are `object` type signal parsing issues or mixed data.

### Data cleaning pipeline

Build a repeatable cleaning function rather than inline mutations:

```python
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()  # Never mutate the original

    # 1. Standardize column names
    df.columns = df.columns.str.lower().str.replace(r"\s+", "_", regex=True)

    # 2. Drop duplicates
    df = df.drop_duplicates()

    # 3. Handle missing values
    numeric_cols = df.select_dtypes("number").columns
    categorical_cols = df.select_dtypes("object").columns

    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    df[categorical_cols] = df[categorical_cols].fillna("unknown")

    # 4. Remove outliers (IQR method - only for numeric targets)
    for col in numeric_cols:
        q1, q3 = df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        df = df[(df[col] >= q1 - 1.5 * iqr) & (df[col] <= q3 + 1.5 * iqr)]

    return df
```

> The `df.copy()` guard is critical. Pandas operations on slices can silently
> modify the original via `SettingWithCopyWarning`. Always copy first.

### Hypothesis testing

Choose the test based on data type and group count (see
`references/statistical-tests.md`), then check assumptions:

```python
from scipy import stats

# Independent samples t-test (two groups, continuous outcome)
group_a = df[df["variant"] == "control"]["revenue"]
group_b = df[df["variant"] == "treatment"]["revenue"]

# Check normality (Shapiro-Wilk - only reliable for n < 5000)
_, p_norm_a = stats.shapiro(group_a.sample(min(len(group_a), 500)))
_, p_norm_b = stats.shapiro(group_b.sample(min(len(group_b), 500)))
print(f"Normality p-values: A={p_norm_a:.4f}, B={p_norm_b:.4f}")

# If p_norm < 0.05 on small samples, prefer Mann-Whitney U
if p_norm_a < 0.05 or p_norm_b < 0.05:
    stat, p_value = stats.mannwhitneyu(group_a, group_b, alternative="two-sided")
    print(f"Mann-Whitney U: stat={stat:.2f}, p={p_value:.4f}")
else:
    stat, p_value = stats.ttest_ind(group_a, group_b)
    print(f"t-test: t={stat:.2f}, p={p_value:.4f}")

# Effect size (Cohen's d)
pooled_std = np.sqrt((group_a.std() ** 2 + group_b.std() ** 2) / 2)
cohens_d = (group_b.mean() - group_a.mean()) / pooled_std
print(f"Cohen's d: {cohens_d:.3f}")  # < 0.2 small, 0.5 medium, > 0.8 large

# Chi-square test for categorical outcomes
contingency = pd.crosstab(df["variant"], df["converted"])
chi2, p_chi2, dof, expected = stats.chi2_contingency(contingency)
print(f"Chi-square: chi2={chi2:.2f}, p={p_chi2:.4f}, dof={dof}")
```

### A/B test analysis with sample size planning

Always calculate required sample size before running an experiment:

```python
from statsmodels.stats.power import TTestIndPower, NormalIndPower
from statsmodels.stats.proportion import proportions_ztest

# Sample size for conversion rate test
# effect_size = (p2 - p1) / sqrt(p_pooled * (1 - p_pooled))
baseline_rate = 0.05       # current conversion
minimum_detectable = 0.01  # smallest change worth detecting
alpha = 0.05               # false positive rate
power = 0.80               # 1 - false negative rate

p1, p2 = baseline_rate, baseline_rate + minimum_detectable
p_pool = (p1 + p2) / 2
effect_size = (p2 - p1) / np.sqrt(p_pool * (1 - p_pool))

analysis = NormalIndPower()
n = analysis.solve_power(effect_size=effect_size, alpha=alpha, power=power)
print(f"Required n per group: {int(np.ceil(n))}")

# Analysis after experiment
control_conversions = 520
control_n = 10000
treatment_conversions = 570
treatment_n = 10000

counts = np.array([treatment_conversions, control_conversions])
nobs = np.array([treatment_n, control_n])
z_stat, p_value = proportions_ztest(counts, nobs)
lift = (treatment_conversions / treatment_n) / (control_conversions / control_n) - 1
print(f"Lift: {lift:.1%}, z={z_stat:.2f}, p={p_value:.4f}")
```

> Never peek at results mid-experiment to decide whether to stop. This inflates
> the false positive rate. Use sequential testing (e.g., alpha spending) if you
> need early stopping.

### Visualization best practices

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set a consistent style once at the top of the notebook
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)

# Distribution comparison - violin > box when showing distribution shape
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.violinplot(data=df, x="group", y="value", ax=axes[0])
axes[0].set_title("Distribution by Group")

# Scatter with regression line - always show the uncertainty band
sns.regplot(data=df, x="feature", y="target", scatter_kws={"alpha": 0.3}, ax=axes[1])
axes[1].set_title("Feature vs Target")
plt.tight_layout()

# Time series - always label axes and use ISO date format
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(df["date"], df["metric"], color="steelblue", linewidth=1.5)
ax.fill_between(df["date"], df["lower_ci"], df["upper_ci"], alpha=0.2)
ax.set_xlabel("Date")
ax.set_ylabel("Metric")
ax.set_title("Metric Over Time with 95% CI")
plt.xticks(rotation=45)
plt.tight_layout()
```

> Use `alpha=0.3` on scatter plots when n > 1000 - overplotting hides the real
> density. For very large datasets use `sns.kdeplot` or hexbin instead.

### Feature engineering

```python
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

# 1. Split first - to prevent leakage
X = df.drop("target", axis=1)
y = df["target"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 2. Numeric features - fit scaler on train, transform both
scaler = StandardScaler()
num_cols = X_train.select_dtypes("number").columns
X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
X_test[num_cols] = scaler.transform(X_test[num_cols])  # transform only, no fit

# 3. Date features
df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour
df["day_of_week"] = pd.to_datetime(df["timestamp"]).dt.dayofweek
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

# 4. Interaction features (only when domain knowledge suggests it)
df["price_per_sqft"] = df["price"] / df["sqft"].replace(0, np.nan)

# 5. Target encoding (use cross-val folds to prevent leakage)
from category_encoders import TargetEncoder
encoder = TargetEncoder(smoothing=10)
X_train["cat_encoded"] = encoder.fit_transform(X_train["category"], y_train)
X_test["cat_encoded"] = encoder.transform(X_test["category"])
```

> Feature leakage - fitting a scaler or encoder on the full dataset before
> splitting - is the single most common modeling mistake. Always split first.

### Linear and logistic regression

```python
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    mean_squared_error, r2_score,
    classification_report, roc_auc_score
)
import statsmodels.api as sm

# Linear regression with statistical output (p-values, CIs)
X_with_const = sm.add_constant(X_train[["feature_1", "feature_2"]])
ols_model = sm.OLS(y_train, X_with_const).fit()
print(ols_model.summary())  # Shows coefficients, p-values, R-squared

# Sklearn for prediction pipeline
lr = LinearRegression()
lr.fit(X_train[num_cols], y_train)
y_pred = lr.predict(X_test[num_cols])
print(f"RMSE: {mean_squared_error(y_test, y_pred, squared=False):.4f}")
print(f"R2: {r2_score(y_test, y_pred):.4f}")

# Logistic regression
clf = LogisticRegression(max_iter=1000, random_state=42)
clf.fit(X_train[num_cols], y_train)
y_prob = clf.predict_proba(X_test[num_cols])[:, 1]
print(classification_report(y_test, clf.predict(X_test[num_cols])))
print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")
```

> Use `statsmodels` when you need p-values and confidence intervals for
> coefficients (inference). Use `sklearn` when you need prediction pipelines,
> cross-validation, and integration with other estimators.

---

## Anti-patterns / common mistakes

| Mistake | Why it's wrong | What to do instead |
|---|---|---|
| Analyzing the test set before the experiment is over | Inflates false positive rate (p-hacking) | Pre-register sample size, run full duration, analyze once |
| Fitting scaler/encoder on full dataset before splitting | Test set leaks into training, inflates evaluation metrics | Always `train_test_split` first, then `fit_transform` train only |
| Reporting p-value without effect size | A tiny effect with huge n produces p < 0.05; means nothing practical | Always report Cohen's d, odds ratio, or relative lift alongside p |
| Using mean on skewed distributions | Mean is pulled by outliers; misrepresents the typical value | Report median and IQR for skewed data; log-transform for modeling |
| Imputing after splitting | Future information leaks from test to train set | Split first, impute train separately, apply same transform to test |
| Dropping all rows with missing data | Loses information, can introduce bias if not MCAR | Use median/mode imputation or model-based imputation (IterativeImputer) |

---

## Gotchas

1. **Feature leakage from fitting transformers before splitting** - Fitting a `StandardScaler`, `LabelEncoder`, or imputer on the full dataset before `train_test_split` leaks test set statistics into training. The model then appears to generalize well but fails in production. Always split first, then `fit_transform` on train only, and `transform` on test.

2. **Peeking at results mid-experiment inflates false positive rate** - Running a significance test daily and stopping as soon as `p < 0.05` is reached is p-hacking. The actual false positive rate can reach 30%+ instead of the nominal 5%. Pre-register your sample size, run the full duration, and analyze once. Use sequential testing (alpha spending) if early stopping is a genuine business requirement.

3. **Shapiro-Wilk normality test unreliable above n=5000** - With large samples, Shapiro-Wilk becomes so sensitive it rejects normality for trivially small deviations that don't matter practically. For n > 5000, use visual diagnostics (Q-Q plot, histogram) instead of the test, and prefer non-parametric tests (Mann-Whitney U) or rely on the Central Limit Theorem for means.

4. **`df.copy()` omission causes silent SettingWithCopyWarning mutations** - Chained indexing on a pandas slice (`df[mask]["col"] = value`) silently fails to modify the original DataFrame. Always call `.copy()` when creating a subset DataFrame you intend to modify. Pandas 2.0+ converts this from a warning to an error, so existing code that worked may break on upgrade.

5. **Outlier removal before splitting contaminates the test set** - Applying IQR outlier removal to the full dataset before splitting removes some test set rows based on information from the training distribution. This is a subtle form of data leakage. Apply outlier handling only within the training fold during cross-validation or after splitting.

---

## References

For deeper guidance on specific topics, load the relevant references file:

- `references/statistical-tests.md` - decision tree for choosing the right test,
  assumption checks, and non-parametric alternatives

Only load references files when the current task requires them - they are detailed
and will consume context.

---

## Companion check

> On first activation of this skill in a conversation: check which companion skills are installed by running `ls ~/.claude/skills/ ~/.agent/skills/ ~/.agents/skills/ .claude/skills/ .agent/skills/ .agents/skills/ 2>/dev/null`. Compare the results against the `recommended_skills` field in this file's frontmatter. For any that are missing, mention them once and offer to install:
> ```
> npx skills add AbsolutelySkilled/AbsolutelySkilled --skill <name>
> ```
> Skip entirely if `recommended_skills` is empty or all companions are already installed.
