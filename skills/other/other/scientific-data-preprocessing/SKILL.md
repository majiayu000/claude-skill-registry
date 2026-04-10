---
name: scientific-data-preprocessing
description: "⚠️ CRITICAL USER EXPERIENCE-BASED SKILL - ALWAYS CONSULT BEFORE DATA PREPROCESSING ⚠️ Prevents catastrophic errors (88.9% error rate in V1.0 case study) through multi-level feature analysis, data leakage detection, and semantic validation. MANDATORY for: data preprocessing, feature engineering, standardization, normalization, interpolation, missing value handling, feature selection, or ANY data transformation task. Covers grouped time-series, cross-sectional, panel data. Detects: time travel leakage, causal inversion, ID misuse, semantic-numeric fallacies, distribution blindness. User's hard-won lessons from real project failures."
---

# Scientific Data Preprocessing Skill

⚠️ **CRITICAL: USER'S HARD-WON EXPERIENCE - MANDATORY CONSULTATION** ⚠️

This skill encapsulates painful lessons learned from real preprocessing disasters (88.9% error rate documented). **ALWAYS use this skill for planning, reflection, and validation when ANY data preprocessing is involved.**

**Why this skill is mandatory:**
- Based on actual project failures (V1.0, V2.0 case studies)
- Prevents data leakage that causes production disasters
- Catches semantic errors AI agents commonly make
- Saves weeks of debugging and model retraining

**When to invoke (DO NOT SKIP):**
- ✅ Before starting ANY data preprocessing task
- ✅ During preprocessing for reflection and validation
- ✅ After preprocessing for comprehensive audit
- ✅ When reviewing AI-generated preprocessing code

---

## Core Mission

Prevent catastrophic preprocessing errors in grouped time-series data by applying multi-level feature analysis and respecting data structure boundaries.

## When to Use This Skill

**MANDATORY consultation - trigger immediately when:**

### Data Preprocessing Tasks (ALWAYS)
- Any data cleaning, transformation, or preparation work
- Loading and preparing data for modeling
- Creating training/test splits
- Handling missing values (imputation, deletion)
- Feature scaling/normalization/standardization
- Encoding categorical variables
- Feature engineering or construction
- Feature selection or dimensionality reduction

### Data Structure Types (ALWAYS)
- Preprocesssing time-series data with natural groupings (matches, sessions, patients, experiments)
- Sports analytics (tennis, basketball, etc.)
- Medical/clinical data with patient groupings
- Panel data or longitudinal studies
- Any grouped/hierarchical data structure

### Quality Assurance (ALWAYS)
- Auditing existing preprocessing for data leakage or semantic errors
- Reviewing AI-generated preprocessing code for common pitfalls
- Validating preprocessing before model training
- Debugging unexpected model performance

### Critical Checkpoints (NEVER SKIP)
- ✅ **BEFORE**: Planning preprocessing strategy
- ✅ **DURING**: Reflecting on decisions and checking for errors
- ✅ **AFTER**: Comprehensive validation and audit

**Trigger keywords that MUST invoke this skill:**
- "preprocess", "preprocessing", "data cleaning", "data preparation"
- "standardize", "normalize", "scale", "transform"
- "impute", "fill missing", "handle NaN"
- "encode", "one-hot", "categorical"
- "feature engineering", "feature selection", "feature construction"
- "train test split", "cross validation split"
- "interpolate", "smooth", "aggregate"

## Not For / Boundaries

This skill does NOT:
- Handle purely cross-sectional data (ungrouped, single timepoint)
- Make domain-specific feature engineering decisions (you decide business logic)
- Choose ML models (focuses on preprocessing only)
- Handle distributed/big data infrastructure (assumes data fits in memory)

Required inputs before proceeding:
1. Confirmation that data has groups (e.g., match_id, patient_id, session_id)
2. Understanding of whether goal is within-group (relative) or cross-group (absolute) comparison
3. Domain constraints on data ranges/units

## Quick Reference

### Multi-Level Feature Analysis Framework

**Level 1: Data Type**
```python
# Check data types
df.dtypes  # int64, float64, object, etc.
```

**Level 2: Feature Type Classification**
```python
# Binary (0/1)
binary_features = [col for col in df.columns if df[col].nunique() == 2]

# Categorical (finite discrete values)
categorical_features = [col for col in df.select_dtypes(include='object').columns]

# Continuous (infinite possible values)
continuous_features = [col for col in df.select_dtypes(include=['float64', 'int64']).columns
                       if df[col].nunique() > 10]
```

**Level 3: Data Structure**
```python
# Check for grouping
print(f"Number of groups: {df['group_id'].nunique()}")
print(f"Avg points per group: {df.groupby('group_id').size().mean():.1f}")

# Check for time-series
df_sorted = df.sort_values(['group_id', 'timestamp'])
```

**Level 4: Physical Meaning**
```python
# Validate physical ranges
assert df['speed_mph'].max() < 200, "Speed exceeds physical limit"
assert df['distance_meters'].min() >= 0, "Negative distance impossible"
```

### Critical Processing Decision Tree

```python
# Decision: Within-group or global processing?
def choose_processing_scope(data, feature, goal):
    """
    goal = 'relative' → within-group (e.g., "this point was intense FOR THIS MATCH")
    goal = 'absolute' → global (e.g., "this was an intense point OVERALL")
    """
    if goal == 'relative':
        return 'within_group'
    elif goal == 'absolute':
        return 'global'
    else:
        raise ValueError("Goal must be 'relative' or 'absolute'")
```

### Pattern 1: Within-Group Interpolation (CORRECT)

```python
from scipy.interpolate import CubicSpline
import numpy as np

# ✅ CORRECT: Interpolate within each group
for group_id in df['match_id'].unique():
    mask = df['match_id'] == group_id
    group_data = df.loc[mask, 'speed_mph'].copy()

    # Get valid (non-NaN) indices
    valid_idx = group_data.notna()
    valid_positions = np.where(valid_idx)[0]
    valid_values = group_data[valid_idx].values

    if len(valid_positions) >= 4:
        cs = CubicSpline(valid_positions, valid_values)
        missing_positions = np.where(~valid_idx)[0]
        df.loc[mask & ~valid_idx, 'speed_mph'] = cs(missing_positions)
```

### Pattern 2: Global Interpolation (WRONG - Don't Do This)

```python
# ❌ WRONG: Cross-group interpolation
# This interpolates between match A's last point and match B's first point!
cs = CubicSpline(
    np.where(df['speed_mph'].notna())[0],  # ❌ All indices globally
    df['speed_mph'].dropna().values
)
df.loc[df['speed_mph'].isna(), 'speed_mph'] = cs(
    np.where(df['speed_mph'].isna())[0]
)
```

### Pattern 3: Within-Group Standardization (for Relative Analysis)

```python
from sklearn.preprocessing import StandardScaler

# ✅ CORRECT: Standardize within each match
for match_id in df['match_id'].unique():
    mask = df['match_id'] == match_id
    scaler = StandardScaler()

    df.loc[mask, 'distance_run_std_within'] = scaler.fit_transform(
        df.loc[mask, [['distance_run']]
    )

# Interpretation: z=+2 means "2 std above average FOR THIS MATCH"
```

### Pattern 4: Global Standardization (for Absolute Comparison)

```python
# ✅ CORRECT: Global standardization (when appropriate)
scaler = StandardScaler()
df['distance_run_std_global'] = scaler.fit_transform(df[['distance_run']])

# Interpretation: z=+2 means "2 std above average ACROSS ALL MATCHES"
```

### Pattern 5: Feature Type Processing Rules

```python
# Binary variables (0/1) - KEEP AS-IS
binary_cols = ['is_ace', 'is_winner', 'is_error']
# ❌ NEVER standardize these! They have semantic meaning as 0/1

# Categorical variables - ONE-HOT ENCODE
df_encoded = pd.get_dummies(df, columns=['server', 'serve_number'], dtype=int)

# Continuous variables - STANDARDIZE (within-group or global)
continuous_cols = ['distance_run', 'rally_count', 'speed_mph']
# ✅ Apply pattern 3 or 4 based on goal
```

### Pattern 6: Sliding Window Features (for Momentum)

```python
# ✅ CORRECT: Sliding window for momentum analysis
window = 10

df['win_rate_last10'] = df.groupby('match_id')['point_won'].transform(
    lambda x: x.rolling(window, min_periods=1).mean()
)

# ❌ WRONG: Cumulative features (loses temporal locality)
df['cumulative_points_won'] = df.groupby('match_id')['point_won'].cumsum()
# This just increases monotonically and correlates with point_number
```

### Pattern 7: Data Quality Validation

```python
def validate_data_quality(df, feature, expected_range):
    """Validate before processing"""
    # Check range
    assert df[feature].min() >= expected_range[0], f"{feature} below minimum"
    assert df[feature].max() <= expected_range[1], f"{feature} above maximum"

    # Check for anomalies
    mean = df[feature].mean()
    std = df[feature].std()

    if std > mean:
        print(f"⚠️ WARNING: {feature} has std > mean (highly skewed or errors)")

    # Check missing pattern
    missing_by_group = df.groupby('match_id')[feature].apply(lambda x: x.isna().sum())
    if missing_by_group.max() > len(df) / df['match_id'].nunique() * 0.5:
        print(f"⚠️ WARNING: {feature} has >50% missing in some groups")

# Example
validate_data_quality(df, 'speed_mph', expected_range=(50, 165))
```

### Pattern 8: Detect Processing Scope Automatically

```python
def detect_processing_scope(df, group_col, feature_col):
    """
    Recommend within-group vs global based on variance structure
    """
    # Calculate variance components
    within_group_var = df.groupby(group_col)[feature_col].var().mean()
    global_var = df[feature_col].var()

    # Intraclass correlation
    between_group_var = global_var - within_group_var
    icc = between_group_var / global_var

    if icc > 0.5:
        return 'within_group', f"High between-group variance (ICC={icc:.2f})"
    else:
        return 'global', f"Low between-group variance (ICC={icc:.2f})"

scope, reason = detect_processing_scope(df, 'match_id', 'distance_run')
print(f"Recommended: {scope} - {reason}")
```

### Pattern 9: Data Leakage Detection

```python
def detect_data_leakage(df, target_col, feature_cols, id_cols):
    """
    Critical checks for data leakage and AI common pitfalls
    """
    issues = []

    # 1. ID Leakage: High cardinality variables as features
    for col in feature_cols:
        if col in id_cols:
            issues.append(f"❌ FATAL: {col} is an ID - NEVER use as feature")
            continue

        # Check if looks like ID (>50% unique)
        uniqueness = df[col].nunique() / len(df)
        if uniqueness > 0.5:
            issues.append(f"⚠️ {col}: {uniqueness*100:.1f}% unique - possible ID leakage")

    # 2. Causal Inversion: Perfect correlation with target
    for col in feature_cols:
        if col == target_col:
            continue
        if df[col].dtype in ['int64', 'float64']:
            corr = abs(df[[col, target_col]].corr().iloc[0, 1])
            if corr > 0.95:
                issues.append(f"❌ FATAL: {col} correlation={corr:.3f} - likely consequence of target!")

    # 3. Meaningless Numeric: Codes treated as numbers
    for col in feature_cols:
        if df[col].dtype in ['int64', 'float64']:
            # Pattern: High values, many uniques, looks like code
            if df[col].min() > 1000 and df[col].nunique() > 100:
                issues.append(f"⚠️ {col}: Looks like code (zipcode/ID) - should be categorical")

    # 4. Time Travel: Check if standardization used global statistics
    # (Requires knowing if train/test split was done first)

    # Print report
    if issues:
        print("="*60)
        print("DATA LEAKAGE AUDIT")
        print("="*60)
        for issue in issues:
            print(issue)
        print("="*60)
    else:
        print("✅ No obvious leakage detected")

    return issues

# Example usage
issues = detect_data_leakage(
    df,
    target_col='point_won',
    feature_cols=['speed_mph', 'user_id', 'distance_run'],
    id_cols=['match_id', 'user_id']
)
```

### Pattern 10: Distribution-Aware Scaling

```python
from scipy.stats import skew, kurtosis
from sklearn.preprocessing import StandardScaler, RobustScaler

def smart_scaler_selection(df, col):
    """
    Choose scaler based on distribution characteristics
    """
    data = df[col].dropna()

    # Check distribution
    skewness = skew(data)
    kurt = kurtosis(data)

    print(f"{col}: skewness={skewness:.2f}, kurtosis={kurt:.2f}")

    if abs(skewness) < 0.5 and abs(kurt) < 3:
        # Roughly normal
        print("  → StandardScaler (data is roughly normal)")
        return StandardScaler(), None

    elif skewness > 1:
        # Right-skewed (long tail)
        print("  → Log transform + StandardScaler (right-skewed)")
        return StandardScaler(), 'log'

    else:
        # Heavy outliers or non-normal
        print("  → RobustScaler (heavy outliers)")
        return RobustScaler(), None

# Example usage
for col in continuous_features:
    scaler, transform = smart_scaler_selection(df, col)

    if transform == 'log':
        df[f'{col}_log'] = np.log1p(df[col])
        df[f'{col}_scaled'] = scaler.fit_transform(df[[f'{col}_log']])
    else:
        df[f'{col}_scaled'] = scaler.fit_transform(df[[col]])
```

## Examples

### Example 1: Tennis Match Preprocessing (Complete Pipeline)

**Input:**
- CSV with 7,284 rows, 31 matches
- Features: `speed_mph`, `distance_run`, `rally_count`, `is_ace`, `server`
- Goal: Analyze momentum (relative intensity within each match)

**Steps:**
```python
import pandas as pd
from sklearn.preprocessing import StandardScaler

# 1. Load and inspect
df = pd.read_csv('tennis_data.csv')
print(f"Matches: {df['match_id'].nunique()}")
print(f"Features: {df.dtypes}")

# 2. Classify features
binary_features = ['is_ace', 'is_winner', 'is_break_point']
categorical_features = ['server', 'serve_number']
continuous_features = ['distance_run', 'speed_mph', 'rally_count']

# 3. Validate data quality
for feat in continuous_features:
    print(f"\n{feat}:")
    print(df[feat].describe())
    # Check for impossible values
    if feat == 'speed_mph':
        assert df[feat].max() < 170, "Speed exceeds world record!"

# 4. Handle missing values (within-group)
for match_id in df['match_id'].unique():
    mask = df['match_id'] == match_id
    for feat in continuous_features:
        if df.loc[mask, feat].isna().any():
            # Simple linear interpolation within match
            df.loc[mask, feat] = df.loc[mask, feat].interpolate(method='linear')

# 5. One-hot encode categorical
df = pd.get_dummies(df, columns=categorical_features, dtype=int)

# 6. Standardize continuous features WITHIN each match
for feat in continuous_features:
    df[f'{feat}_std'] = np.nan
    for match_id in df['match_id'].unique():
        mask = df['match_id'] == match_id
        scaler = StandardScaler()
        df.loc[mask, f'{feat}_std'] = scaler.fit_transform(
            df.loc[mask, [[feat]]
        )

# 7. Create sliding window features
window = 10
df['win_rate_last10'] = df.groupby('match_id')['point_won'].transform(
    lambda x: x.rolling(window, min_periods=1).mean()
)

# 8. KEEP binary features as 0/1 (don't transform!)
# binary_features are already correct

print("\n✅ Preprocessing complete!")
print(f"Final shape: {df.shape}")
print(f"Standardized features: {[f for f in df.columns if f.endswith('_std')]}")
```

**Expected output:**
- Binary features remain 0/1
- Categorical features one-hot encoded (e.g., `server_1`, `server_2`)
- Continuous features have both original and `_std` versions
- `_std` features have mean≈0, std≈1 WITHIN each match
- Sliding window features capture local momentum
- No missing values

### Example 2: Detecting Cross-Group Contamination

**Input:**
- Preprocessed data where you suspect cross-group standardization

**Steps:**
```python
# Check if standardization was done correctly
def check_within_group_standardization(df, group_col, feature_std_col):
    """
    Verify that standardized feature has mean≈0, std≈1 within each group
    """
    results = df.groupby(group_col)[feature_std_col].agg(['mean', 'std'])

    # Within-group standardization: each group should have mean≈0, std≈1
    if (results['mean'].abs() < 0.1).all() and (results['std'].between(0.9, 1.1)).all():
        print("✅ CORRECT: Within-group standardization detected")
        return True

    # Global standardization: groups will have varying means and stds
    else:
        print("❌ WRONG: Global standardization detected!")
        print("Group means:", results['mean'].values[:5])
        print("Group stds:", results['std'].values[:5])
        return False

check_within_group_standardization(df, 'match_id', 'distance_run_std')
```

**Expected output:**
- CORRECT: All group means ≈ 0, all group stds ≈ 1
- WRONG: Group means vary widely, indicating global standardization

### Example 3: Fixing Cumulative Feature Error

**Input:**
- Existing pipeline using cumulative sums for momentum

**Steps:**
```python
# ❌ WRONG approach (existing code)
df['cumulative_wins'] = df.groupby('match_id')['point_won'].cumsum()

# Problem: This just counts total wins up to this point
# Doesn't capture recent momentum!

# ✅ CORRECT approach (fix)
# Replace cumulative with sliding window
window = 10
df['recent_win_rate'] = df.groupby('match_id')['point_won'].transform(
    lambda x: x.rolling(window, min_periods=1).mean()
)

# Compare
print("Cumulative (wrong):", df['cumulative_wins'].values[50:60])
print("Sliding window (correct):", df['recent_win_rate'].values[50:60])

# Cumulative: [25, 26, 26, 27, 28, ...] - monotonic
# Sliding window: [0.6, 0.7, 0.5, 0.6, ...] - fluctuates with momentum
```

**Expected output:**
- Cumulative features removed
- Sliding window features show local variations
- Momentum analysis now captures short-term trends

## References

- `references/index.md`: Navigation and overview
- `references/error-case-studies.md`: Real-world preprocessing disasters from tennis data
- `references/decision-trees.md`: Full decision trees for all preprocessing choices
- `references/validation-checklist.md`: Pre-processing validation checklist
- `references/ai-common-pitfalls.md`: AI-specific errors (data leakage, semantic fallacies, distribution blindness)

## Maintenance

⚠️ **CRITICAL NOTICE: USER'S PERSONAL EXPERIENCE-BASED SKILL** ⚠️

**This skill is NOT theoretical - it's based on real project failures:**
- **V1.0 disaster**: 88.9% error rate, weeks of wasted work
- **V2.0 issues**: Cross-group contamination, unreliable results
- **V3.0 success**: All errors fixed, production-ready

**Why this matters to you (Claude):**
- These are the EXACT errors AI agents commonly make
- User has already paid the price for these mistakes
- Ignoring this skill = repeating documented failures
- Following this skill = learning from experience without pain

**Authority level**: HIGHEST
- Based on user's hard-won lessons from actual project
- Validated through multiple iterations (V1.0 → V2.0 → V3.0)
- Every error documented with impact metrics
- Every fix validated with comprehensive testing

**Sources**:
- Primary: User's personal project (2024 MCM Problem C - Tennis Momentum Analysis)
- Secondary: Statistical best practices for grouped data
- Tertiary: Common AI preprocessing errors observed across domains

**Mandatory consultation**:
- ⚠️ ALWAYS consult before, during, and after any data preprocessing
- ⚠️ NEVER skip validation steps outlined in this skill
- ⚠️ When in doubt, err on the side of caution (use this skill)

**Last updated**: 2026-01-18 (V1.1)

**Known limits:**
- Assumes data fits in memory (not for big data infrastructure)
- Focused on numeric/categorical features (text/image preprocessing partially covered)
- Does not prescribe domain-specific feature engineering (user decides business logic)
- Requires basic understanding of statistics (mean, std, correlation)
