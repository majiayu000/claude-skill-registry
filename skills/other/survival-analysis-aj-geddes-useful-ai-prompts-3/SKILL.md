---
name: Survival Analysis
description: Analyze time-to-event data, calculate survival probabilities, and compare groups using Kaplan-Meier and Cox proportional hazards models
---

# Survival Analysis

## Overview

Survival analysis studies time until an event occurs, handling censored data where events haven't happened for some subjects, enabling prediction of lifetimes and risk assessment.

## Key Concepts

- **Survival Time**: Time until event
- **Censoring**: Event not observed (subject dropped out)
- **Hazard**: Instantaneous risk at time t
- **Survival Curve**: Probability of surviving past time t
- **Hazard Ratio**: Relative risk between groups

## Common Models

- **Kaplan-Meier**: Non-parametric survival curves
- **Cox Proportional Hazards**: Semi-parametric regression
- **Weibull/Exponential**: Parametric models
- **Log-rank Test**: Comparing survival curves
- **Competing Risks**: Multiple event types

## Implementation with Python

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from lifelines import KaplanMeierFitter, CoxPHFitter, WeibullAFTFitter
from lifelines.statistics import logrank_test
import warnings
warnings.filterwarnings('ignore')

# Generate sample survival data
np.random.seed(42)
n_patients = 200

# Time to event (in months)
event_times = np.random.exponential(scale=24, size=n_patients)
# Censoring indicator (1 = event occurred, 0 = censored)
event_observed = np.random.binomial(1, 0.7, n_patients)
# Group assignment (0 = control, 1 = treatment)
group = np.random.binomial(1, 0.5, n_patients)
# Age at baseline
age = np.random.uniform(30, 80, n_patients)
# Risk score
risk_score = np.random.uniform(0, 100, n_patients)

# Adjust event times based on group (simulate treatment effect)
event_times = event_times * (1 + group * 0.3)

df = pd.DataFrame({
    'time': event_times,
    'event': event_observed,
    'group': group,
    'age': age,
    'risk_score': risk_score,
})

print("Survival Data Summary:")
print(df.head(10))
print(f"\nTotal subjects: {len(df)}")
print(f"Events: {df['event'].sum()} ({df['event'].sum()/len(df)*100:.1f}%)")
print(f"Censored: {(1-df['event']).sum()} ({(1-df['event']).sum()/len(df)*100:.1f}%)")

# 1. Kaplan-Meier Estimation
kmf = KaplanMeierFitter()
kmf.fit(df['time'], df['event'], label='Overall')

print("\n1. Kaplan-Meier Survival Estimates:")
print(f"Median survival time: {kmf.median_survival_time_:.1f} months")
print(f"6-month survival: {kmf.predict(6):.1%}")
print(f"12-month survival: {kmf.predict(12):.1%}")
print(f"24-month survival: {kmf.predict(24):.1%}")

# 2. Group Comparison
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Overall survival curve
ax = axes[0, 0]
kmf.plot_survival_function(ax=ax, linewidth=2)
ax.set_xlabel('Time (months)')
ax.set_ylabel('Survival Probability')
ax.set_title('Kaplan-Meier Survival Curve (Overall)')
ax.grid(True, alpha=0.3)

# Survival curves by group
ax = axes[0, 1]
for group_val in [0, 1]:
    mask = df['group'] == group_val
    kmf.fit(df[mask]['time'], df[mask]['event'],
           label=f'{"Control" if group_val == 0 else "Treatment"}')
    kmf.plot_survival_function(ax=ax, linewidth=2)

ax.set_xlabel('Time (months)')
ax.set_ylabel('Survival Probability')
ax.set_title('Kaplan-Meier Curves by Group')
ax.grid(True, alpha=0.3)

# 3. Log-Rank Test
mask_control = df['group'] == 0
mask_treatment = df['group'] == 1

results = logrank_test(
    df[mask_control]['time'],
    df[mask_treatment]['time'],
    df[mask_control]['event'],
    df[mask_treatment]['event']
)

print(f"\n3. Log-Rank Test:")
print(f"Test statistic: {results.test_statistic:.4f}")
print(f"P-value: {results.p_value:.4f}")
print(f"Significant: {'Yes' if results.p_value < 0.05 else 'No'}")

# 4. Risk Groups (by quartiles)
df['risk_quartile'] = pd.qcut(df['risk_score'], q=4, labels=['Low', 'Medium-Low', 'Medium-High', 'High'])

ax = axes[1, 0]
for risk_group in ['Low', 'Medium-Low', 'Medium-High', 'High']:
    mask = df['risk_quartile'] == risk_group
    kmf.fit(df[mask]['time'], df[mask]['event'], label=risk_group)
    kmf.plot_survival_function(ax=ax, linewidth=2)

ax.set_xlabel('Time (months)')
ax.set_ylabel('Survival Probability')
ax.set_title('Kaplan-Meier Curves by Risk Quartile')
ax.legend()
ax.grid(True, alpha=0.3)

# 5. Cumulative Hazard
ax = axes[1, 1]
kmf.fit(df['time'], df['event'])
kmf.plot_cumulative_density(ax=ax, linewidth=2)
ax.set_xlabel('Time (months)')
ax.set_ylabel('Cumulative Event Probability')
ax.set_title('Cumulative Event Probability')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 6. Cox Proportional Hazards Model
cph = CoxPHFitter()
cph.fit(df[['time', 'event', 'group', 'age', 'risk_score']], duration_col='time', event_col='event')

print(f"\n6. Cox Proportional Hazards Model:")
print(cph.summary)

# Hazard ratios
print(f"\nHazard Ratios:")
for var in ['group', 'age', 'risk_score']:
    hr = np.exp(cph.params_[var])
    print(f"  {var}: {hr:.3f}")

# 7. Model Diagnostics
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Partial effects plot
ax = axes[0, 0]
df_partial = df.copy()
df_partial['partial_hazard'] = cph.predict_partial_hazard(df_partial)

for group_val in [0, 1]:
    mask = df_partial['group'] == group_val
    ax.scatter(df_partial[mask]['risk_score'], df_partial[mask]['partial_hazard'],
              alpha=0.6, label=f'{"Control" if group_val == 0 else "Treatment"}')

ax.set_xlabel('Risk Score')
ax.set_ylabel('Partial Hazard')
ax.set_title('Partial Hazard by Risk Score and Group')
ax.legend()
ax.grid(True, alpha=0.3)

# Concordance index over time
ax = axes[0, 1]
concordance_index = cph.concordance_index_
ax.text(0.5, 0.5, f'Concordance Index: {concordance_index:.3f}',
       ha='center', va='center', fontsize=14,
       bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
ax.axis('off')
ax.set_title('Model Performance')

# Survival curves by predicted risk
ax = axes[1, 0]
df['predicted_hazard'] = cph.predict_partial_hazard(df)
df['hazard_quartile'] = pd.qcut(df['predicted_hazard'], q=4, labels=['Low', 'Medium-Low', 'Medium-High', 'High'])

for hazard_group in ['Low', 'Medium-Low', 'Medium-High', 'High']:
    mask = df['hazard_quartile'] == hazard_group
    kmf.fit(df[mask]['time'], df[mask]['event'], label=hazard_group)
    kmf.plot_survival_function(ax=ax, linewidth=2)

ax.set_xlabel('Time (months)')
ax.set_ylabel('Survival Probability')
ax.set_title('Survival by Predicted Risk Quartile')
ax.grid(True, alpha=0.3)

# Variable importance
ax = axes[1, 1]
coef_df = cph.summary[['coef', 'exp(coef)']].copy()
coef_df = coef_df.sort_values('coef')

colors = ['red' if x < 0 else 'green' for x in coef_df['coef']]
ax.barh(coef_df.index, coef_df['coef'], color=colors, alpha=0.7, edgecolor='black')
ax.set_xlabel('Coefficient')
ax.set_title('Variable Coefficients')
ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.show()

# 8. Survival Prediction
new_patient = pd.DataFrame({
    'group': [1],
    'age': [65],
    'risk_score': [75],
})

survival_prob = cph.predict_survival_function(new_patient, times=[6, 12, 24])
print(f"\n8. Survival Prediction for New Patient (age 65, treatment, risk 75):")
print(f"6-month survival: {survival_prob.iloc[0, 0]:.1%}")
print(f"12-month survival: {survival_prob.iloc[1, 0]:.1%}")
print(f"24-month survival: {survival_prob.iloc[2, 0]:.1%}")

# 9. Proportional Hazards Assumption
print(f"\n9. Proportional Hazards Test:")
from lifelines.statistics import proportional_hazard_assumption

ph_test = proportional_hazard_assumption(cph, df[['time', 'event', 'group', 'age', 'risk_score']],
                                         time_transform='rank')
print(ph_test)

# 10. Summary Statistics
print(f"\n" + "="*50)
print("SURVIVAL ANALYSIS SUMMARY")
print("="*50)
print(f"Control median survival: {df[df['group']==0]['time'].median():.1f} months")
print(f"Treatment median survival: {df[df['group']==1]['time'].median():.1f} months")
print(f"Log-rank p-value: {results.p_value:.4f}")
print(f"Concordance index: {concordance_index:.3f}")
print("="*50)
```

## Censoring Types

- **Right censoring**: Event hasn't occurred (most common)
- **Left censoring**: Event occurred before observation
- **Interval censoring**: Event in unknown time interval

## Model Comparison

- **Kaplan-Meier**: Describes, doesn't explain
- **Cox Model**: Adjusts for covariates, proportional hazards
- **Parametric**: Assumes distribution
- **Competing Risks**: Multiple event types

## Applications

- Clinical trials
- Equipment reliability
- Customer churn
- Employee retention
- Product lifetime

## Deliverables

- Kaplan-Meier survival curves
- Survival probability estimates
- Log-rank test results
- Cox model coefficients
- Hazard ratios
- Risk stratification groups
- Survival predictions
- Model diagnostics
