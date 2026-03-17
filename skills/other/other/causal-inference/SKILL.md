---
name: Causal Inference
description: Determine cause-and-effect relationships using propensity scoring, instrumental variables, and causal graphs for policy evaluation and treatment effects
---

# Causal Inference

## Overview

Causal inference determines cause-and-effect relationships and estimates treatment effects, going beyond correlation to understand what causes what.

## When to Use

- Evaluating the impact of policy interventions or business decisions
- Estimating treatment effects when randomized experiments aren't feasible
- Controlling for confounding variables in observational data
- Determining if a marketing campaign or product change caused an outcome
- Analyzing heterogeneous treatment effects across different user segments
- Making causal claims from non-experimental data using propensity scores or instrumental variables

## Key Concepts

- **Treatment**: Intervention or exposure
- **Outcome**: Result or consequence
- **Confounding**: Variables affecting both treatment and outcome
- **Causal Graph**: Visual representation of relationships
- **Treatment Effect**: Impact of intervention
- **Selection Bias**: Non-random treatment assignment

## Causal Methods

- **Randomized Controlled Trials (RCT)**: Gold standard
- **Propensity Score Matching**: Balance treatment/control
- **Difference-in-Differences**: Before/after comparison
- **Instrumental Variables**: Handle endogeneity
- **Causal Forests**: Heterogeneous treatment effects

## Implementation with Python

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from scipy import stats

# Generate observational data with confounding
np.random.seed(42)

n = 1000

# Confounder: Age (affects both treatment and outcome)
age = np.random.uniform(25, 75, n)

# Treatment: Training program (more likely for younger people)
treatment_prob = 0.3 + 0.3 * (75 - age) / 50  # Inverse relationship with age
treatment = (np.random.uniform(0, 1, n) < treatment_prob).astype(int)

# Outcome: Salary (affected by both treatment and age)
# True causal effect of treatment: +$5000
salary = 40000 + 500 * age + 5000 * treatment + np.random.normal(0, 10000, n)

df = pd.DataFrame({
    'age': age,
    'treatment': treatment,
    'salary': salary,
})

print("Observational Data Summary:")
print(df.describe())
print(f"\nTreatment Rate: {df['treatment'].mean():.1%}")
print(f"Average Salary (Control): ${df[df['treatment']==0]['salary'].mean():.0f}")
print(f"Average Salary (Treatment): ${df[df['treatment']==1]['salary'].mean():.0f}")

# 1. Naive Comparison (BIASED - ignores confounding)
naive_effect = df[df['treatment']==1]['salary'].mean() - df[df['treatment']==0]['salary'].mean()
print(f"\n1. Naive Comparison: ${naive_effect:.0f} (BIASED)")

# 2. Regression Adjustment (Covariate Adjustment)
X = df[['treatment', 'age']]
y = df['salary']
model = LinearRegression()
model.fit(X, y)
regression_effect = model.coef_[0]

print(f"\n2. Regression Adjustment: ${regression_effect:.0f}")

# 3. Propensity Score Matching
# Estimate probability of treatment given covariates
ps_model = LogisticRegression()
ps_model.fit(df[['age']], df['treatment'])
df['propensity_score'] = ps_model.predict_proba(df[['age']])[:, 1]

print(f"\n3. Propensity Score Matching:")
print(f"PS range: [{df['propensity_score'].min():.3f}, {df['propensity_score'].max():.3f}]")

# Matching: find control for each treated unit
matched_pairs = []
treated_units = df[df['treatment'] == 1].index
for treated_idx in treated_units:
    treated_ps = df.loc[treated_idx, 'propensity_score']
    treated_age = df.loc[treated_idx, 'age']

    # Find closest control unit
    control_units = df[(df['treatment'] == 0) &
                      (df['propensity_score'] >= treated_ps - 0.1) &
                      (df['propensity_score'] <= treated_ps + 0.1)].index

    if len(control_units) > 0:
        closest_control = min(control_units,
                             key=lambda x: abs(df.loc[x, 'propensity_score'] - treated_ps))
        matched_pairs.append({
            'treated_idx': treated_idx,
            'control_idx': closest_control,
            'treated_salary': df.loc[treated_idx, 'salary'],
            'control_salary': df.loc[closest_control, 'salary'],
        })

matched_df = pd.DataFrame(matched_pairs)
psm_effect = (matched_df['treated_salary'] - matched_df['control_salary']).mean()
print(f"PSM Effect: ${psm_effect:.0f}")
print(f"Matched pairs: {len(matched_df)}")

# 4. Stratification by Propensity Score
df['ps_stratum'] = pd.qcut(df['propensity_score'], q=5, labels=False, duplicates='drop')

stratified_effects = []
for stratum in df['ps_stratum'].unique():
    stratum_data = df[df['ps_stratum'] == stratum]
    if (stratum_data['treatment'] == 0).sum() > 0 and (stratum_data['treatment'] == 1).sum() > 0:
        treated_mean = stratum_data[stratum_data['treatment'] == 1]['salary'].mean()
        control_mean = stratum_data[stratum_data['treatment'] == 0]['salary'].mean()
        effect = treated_mean - control_mean
        stratified_effects.append(effect)

stratified_effect = np.mean(stratified_effects)
print(f"\n4. Stratification by PS: ${stratified_effect:.0f}")

# 5. Visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Treatment distribution by age
ax = axes[0, 0]
treated = df[df['treatment'] == 1]
control = df[df['treatment'] == 0]
ax.hist(control['age'], bins=20, alpha=0.6, label='Control', color='blue')
ax.hist(treated['age'], bins=20, alpha=0.6, label='Treated', color='red')
ax.set_xlabel('Age')
ax.set_ylabel('Frequency')
ax.set_title('Age Distribution by Treatment')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

# Salary vs Age (colored by treatment)
ax = axes[0, 1]
ax.scatter(control['age'], control['salary'], alpha=0.5, label='Control', s=30)
ax.scatter(treated['age'], treated['salary'], alpha=0.5, label='Treated', s=30, color='red')
ax.set_xlabel('Age')
ax.set_ylabel('Salary')
ax.set_title('Salary vs Age by Treatment')
ax.legend()
ax.grid(True, alpha=0.3)

# Propensity Score Distribution
ax = axes[1, 0]
ax.hist(df[df['treatment'] == 0]['propensity_score'], bins=20, alpha=0.6, label='Control', color='blue')
ax.hist(df[df['treatment'] == 1]['propensity_score'], bins=20, alpha=0.6, label='Treated', color='red')
ax.set_xlabel('Propensity Score')
ax.set_ylabel('Frequency')
ax.set_title('Propensity Score Distribution')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

# Treatment Effect Comparison
ax = axes[1, 1]
methods = ['Naive', 'Regression', 'PSM', 'Stratified']
effects = [naive_effect, regression_effect, psm_effect, stratified_effect]
true_effect = 5000

ax.bar(methods, effects, color=['red', 'orange', 'yellow', 'lightgreen'], alpha=0.7, edgecolor='black')
ax.axhline(y=true_effect, color='green', linestyle='--', linewidth=2, label=f'True Effect (${true_effect:.0f})')
ax.set_ylabel('Treatment Effect ($)')
ax.set_title('Treatment Effect Estimates by Method')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

for i, effect in enumerate(effects):
    ax.text(i, effect + 200, f'${effect:.0f}', ha='center', va='bottom')

plt.tight_layout()
plt.show()

# 6. Doubly Robust Estimation
from sklearn.ensemble import RandomForestRegressor

# Propensity score model
ps_model_dr = LogisticRegression().fit(df[['age']], df['treatment'])
ps_scores = ps_model_dr.predict_proba(df[['age']])[:, 1]

# Outcome model
outcome_model = RandomForestRegressor(n_estimators=50, random_state=42)
outcome_model.fit(df[['treatment', 'age']], df['salary'])

# Doubly robust estimator
treated_mask = df['treatment'] == 1
control_mask = df['treatment'] == 0

# Adjust for propensity score
treated_adjusted = (treated_mask.astype(int) * df['salary']) / (ps_scores + 0.01)
control_adjusted = (control_mask.astype(int) * df['salary']) / (1 - ps_scores + 0.01)

# Outcome predictions
pred_treated = outcome_model.predict(df[['treatment', 'age']].replace({'treatment': 0, 1: 1}))
pred_control = outcome_model.predict(df[['treatment', 'age']].replace({'treatment': 1, 0: 0}))

dr_effect = treated_adjusted.sum() / treated_mask.sum() - control_adjusted.sum() / control_mask.sum()
print(f"\n6. Doubly Robust Estimation: ${dr_effect:.0f}")

# 7. Heterogeneous Treatment Effects
print(f"\n7. Heterogeneous Treatment Effects (by Age Quartile):")

for age_q in pd.qcut(df['age'], q=4, duplicates='drop').unique():
    mask = (df['age'] >= age_q.left) & (df['age'] < age_q.right)
    stratum_data = df[mask]

    if (stratum_data['treatment'] == 0).sum() > 0 and (stratum_data['treatment'] == 1).sum() > 0:
        treated_mean = stratum_data[stratum_data['treatment'] == 1]['salary'].mean()
        control_mean = stratum_data[stratum_data['treatment'] == 0]['salary'].mean()
        effect = treated_mean - control_mean

        print(f"  Age {age_q.left:.0f}-{age_q.right:.0f}: ${effect:.0f}")

# 8. Sensitivity Analysis
print(f"\n8. Sensitivity Analysis (Hidden Confounder Impact):")

# Vary hidden confounder correlation with outcome
for hidden_effect in [1000, 2000, 5000, 10000]:
    adjusted_effect = regression_effect - hidden_effect * 0.1
    print(f"  If hidden confounder worth ${hidden_effect}: Effect = ${adjusted_effect:.0f}")

# 9. Summary Table
print(f"\n" + "="*60)
print("CAUSAL INFERENCE SUMMARY")
print("="*60)
print(f"True Treatment Effect: ${true_effect:,.0f}")
print(f"\nEstimates:")
print(f"  Naive (BIASED): ${naive_effect:,.0f}")
print(f"  Regression Adjustment: ${regression_effect:,.0f}")
print(f"  Propensity Score Matching: ${psm_effect:,.0f}")
print(f"  Stratification: ${stratified_effect:,.0f}")
print(f"  Doubly Robust: ${dr_effect:,.0f}")
print("="*60)

# 10. Causal Graph (Text representation)
print(f"\n10. Causal Graph (DAG):")
print(f"""
Age → Treatment ← (Selection Bias)
  ↓        ↓
  └─→ Salary

Interpretation:
- Age is a confounder
- Treatment causally affects Salary
- Age directly affects Salary
- Age affects probability of Treatment
""")
```

## Causal Assumptions

- **Unconfoundedness**: No unmeasured confounders
- **Overlap**: Common support on propensity scores
- **SUTVA**: No interference between units
- **Consistency**: Single version of treatment

## Treatment Effect Types

- **ATE**: Average Treatment Effect (overall)
- **ATT**: Average Treatment on Treated
- **CATE**: Conditional Average Treatment Effect
- **HTE**: Heterogeneous Treatment Effects

## Method Strengths

- **RCT**: Gold standard, controls all confounders
- **Matching**: Balances groups, preserves overlap
- **Regression**: Adjusts for covariates
- **Instrumental Variables**: Handles endogeneity
- **Causal Forests**: Learns heterogeneous effects

## Deliverables

- Causal graph visualization
- Treatment effect estimates
- Sensitivity analysis
- Heterogeneous treatment effects
- Covariate balance assessment
- Propensity score diagnostics
- Final causal inference report
