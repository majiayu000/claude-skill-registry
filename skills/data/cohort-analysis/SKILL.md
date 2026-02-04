---
name: Cohort Analysis
description: Track and analyze user cohorts over time, calculate retention rates, and identify behavioral patterns for customer lifecycle and retention analysis
---

# Cohort Analysis

## Overview

Cohort analysis tracks groups of users with shared characteristics over time, revealing patterns in retention, engagement, and lifetime value.

## When to Use

- Measuring user retention rates and identifying when users churn
- Analyzing customer lifetime value (LTV) and payback periods
- Comparing performance across different user acquisition channels or campaigns
- Understanding how product changes affect different user groups over time
- Tracking engagement patterns and identifying early warning signs of churn
- Evaluating the long-term impact of onboarding improvements or feature releases

## Core Concepts

- **Cohort**: Group of users sharing a characteristic (signup date, region, etc.)
- **Cohort Size**: Initial group size
- **Retention Rate**: Percentage remaining active
- **Churn Rate**: Percentage who left
- **Retention Curve**: How cohort degrades over time

## Cohort Types

- **Acquisition Date**: Users grouped by signup period
- **Behavioral**: Users grouped by actions taken
- **Revenue**: Users grouped by purchase value
- **Geographic**: Users grouped by location
- **Demographic**: Users grouped by characteristics

## Implementation with Python

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Create sample user lifecycle data
np.random.seed(42)

# Generate user data
n_users = 5000
users = []

for user_id in range(n_users):
    signup_month = np.random.choice(range(1, 13))
    lifetime_months = np.random.poisson(6) + 1

    for month in range(1, lifetime_months + 1):
        users.append({
            'user_id': user_id,
            'signup_month': signup_month,
            'month': month,
            'active': 1,
        })

df = pd.DataFrame(users)

# Add derived columns
df['cohort_month'] = df['signup_month']
df['cohort_age'] = df['month']  # Could be day, week, etc.
df['date'] = pd.to_datetime('2023-01-01') + pd.to_timedelta(df['signup_month'] * 30, unit='D')

print("User Data Summary:")
print(df.head(10))

# 1. Cohort Table (Retention Matrix)
cohort_data = df.groupby(['cohort_month', 'cohort_age']).agg({
    'user_id': 'nunique'
}).reset_index()
cohort_data.columns = ['cohort_month', 'cohort_age', 'unique_users']

# Create pivot table
cohort_pivot = cohort_data.pivot(index='cohort_month', columns='cohort_age', values='unique_users')

print("\nCohort Sizes (Raw User Counts):")
print(cohort_pivot)

# 2. Cohort Retention (as percentage of cohort size)
cohort_size = cohort_pivot.iloc[:, 0]
retention_table = cohort_pivot.divide(cohort_size, axis=0) * 100

print("\nCohort Retention Rate (%):")
print(retention_table.round(1))

# 3. Visualize Retention Matrix
fig, axes = plt.subplots(2, 1, figsize=(14, 8))

# Heatmap of raw counts
sns.heatmap(cohort_pivot, annot=True, fmt='g', cmap='YlOrRd', ax=axes[0],
            cbar_kws={'label': 'User Count'})
axes[0].set_title('Cohort Sizes - User Counts')
axes[0].set_xlabel('Cohort Age (Months)')
axes[0].set_ylabel('Cohort Month')

# Heatmap of retention rates
sns.heatmap(retention_table, annot=True, fmt='.0f', cmap='RdYlGn', vmin=0, vmax=100,
            ax=axes[1], cbar_kws={'label': 'Retention %'})
axes[1].set_title('Cohort Retention Rates (%)')
axes[1].set_xlabel('Cohort Age (Months)')
axes[1].set_ylabel('Cohort Month')

plt.tight_layout()
plt.show()

# 4. Retention Curve
fig, ax = plt.subplots(figsize=(12, 6))

# Plot retention curves for each cohort
for cohort_month in cohort_pivot.index[:8]:  # First 8 cohorts
    cohort_retention = retention_table.loc[cohort_month]
    ax.plot(cohort_retention.index, cohort_retention.values, marker='o', label=f'Cohort {cohort_month}')

ax.set_xlabel('Cohort Age (Months)')
ax.set_ylabel('Retention Rate (%)')
ax.set_title('Retention Curves by Cohort')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True, alpha=0.3)
ax.set_ylim([0, 105])

plt.tight_layout()
plt.show()

# 5. Average Retention Curve
fig, ax = plt.subplots(figsize=(10, 6))

# Calculate average retention at each age
avg_retention = retention_table.mean()
ax.plot(avg_retention.index, avg_retention.values, marker='o', linewidth=2, markersize=8, color='navy')
ax.fill_between(avg_retention.index, avg_retention.values, alpha=0.3, color='navy')

# Add confidence interval
std_retention = retention_table.std()
ax.fill_between(std_retention.index,
                avg_retention - std_retention,
                avg_retention + std_retention,
                alpha=0.2, color='navy', label='±1 Std Dev')

ax.set_xlabel('Cohort Age (Months)')
ax.set_ylabel('Retention Rate (%)')
ax.set_title('Average Retention Curve with Confidence Band')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_ylim([0, 105])

plt.tight_layout()
plt.show()

# 6. Churn Rate
churn_rate = 100 - retention_table
print("\nChurn Rates (%):")
print(churn_rate.round(1).head())

# 7. Revenue Cohort Analysis
# Add revenue data
np.random.seed(42)
df['revenue'] = np.random.exponential(50, len(df))

# Revenue by cohort
revenue_data = df.groupby(['cohort_month', 'cohort_age']).agg({
    'revenue': 'sum',
    'user_id': 'nunique'
}).reset_index()
revenue_data['revenue_per_user'] = revenue_data['revenue'] / revenue_data['user_id']

revenue_pivot = revenue_data.pivot(index='cohort_month', columns='cohort_age', values='revenue')
rpu_pivot = revenue_data.pivot(index='cohort_month', columns='cohort_age', values='revenue_per_user')

# Visualize revenue
fig, axes = plt.subplots(2, 1, figsize=(14, 8))

sns.heatmap(revenue_pivot, annot=True, fmt='.0f', cmap='YlGnBu', ax=axes[0],
            cbar_kws={'label': 'Total Revenue ($)'})
axes[0].set_title('Total Revenue by Cohort')
axes[0].set_xlabel('Cohort Age (Months)')
axes[0].set_ylabel('Cohort Month')

sns.heatmap(rpu_pivot, annot=True, fmt='.2f', cmap='YlGnBu', ax=axes[1],
            cbar_kws={'label': 'Revenue per User ($)'})
axes[1].set_title('Revenue per User by Cohort')
axes[1].set_xlabel('Cohort Age (Months)')
axes[1].set_ylabel('Cohort Month')

plt.tight_layout()
plt.show()

# 8. Lifetime Value Calculation
df['month_since_signup'] = df['cohort_age']
ltv_data = df.groupby('user_id').agg({
    'revenue': 'sum',
    'cohort_month': 'first',
    'month_since_signup': 'max',
}).reset_index()
ltv_data.columns = ['user_id', 'lifetime_value', 'cohort_month', 'lifetime_months']

# Average LTV by cohort
ltv_by_cohort = ltv_data.groupby('cohort_month')['lifetime_value'].agg(['mean', 'median', 'std'])

print("\nLifetime Value by Cohort:")
print(ltv_by_cohort.round(2))

fig, ax = plt.subplots(figsize=(10, 6))
ltv_by_cohort['mean'].plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
ax.set_title('Average Lifetime Value by Cohort')
ax.set_xlabel('Cohort Month')
ax.set_ylabel('Lifetime Value ($)')
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()

# 9. Cohort Composition Over Time
fig, ax = plt.subplots(figsize=(12, 6))

# Active users per month by cohort
active_by_month = df.groupby(['date', 'cohort_month']).size().reset_index(name='active_users')
pivot_active = active_by_month.pivot(index='date', columns='cohort_month', values='active_users')

pivot_active.plot(ax=ax, marker='o')
ax.set_title('Active Users Per Month by Cohort')
ax.set_xlabel('Month')
ax.set_ylabel('Active Users')
ax.legend(title='Cohort Month', bbox_to_anchor=(1.05, 1))
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 10. Cohort Summary Metrics
summary_metrics = pd.DataFrame({
    'Cohort Month': cohort_size.index,
    'Initial Size': cohort_size.values,
    'Month 1 Retention': retention_table.iloc[:, 0].values,
    'Month 3 Retention': retention_table.iloc[:, min(2, retention_table.shape[1]-1)].values,
    'Avg LTV': ltv_by_cohort['mean'].values,
})

print("\nCohort Summary Metrics:")
print(summary_metrics.round(2))

# 11. Visualization comparison
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Month 1 vs Month 3 retention
ax_plot = axes[0]
months = ['Month 1', 'Month 3']
month_1_ret = retention_table.iloc[:, 0].mean()
month_3_ret = retention_table.iloc[:, min(2, retention_table.shape[1]-1)].mean()
ax_plot.bar(months, [month_1_ret, month_3_ret], color=['#1f77b4', '#ff7f0e'], edgecolor='black')
ax_plot.set_ylabel('Retention Rate (%)')
ax_plot.set_title('Average Retention by Milestone')
ax_plot.set_ylim([0, 100])
for i, v in enumerate([month_1_ret, month_3_ret]):
    ax_plot.text(i, v + 2, f'{v:.1f}%', ha='center')

# Cohort size trend
axes[1].plot(cohort_size.index, cohort_size.values, marker='o', linewidth=2, markersize=8)
axes[1].set_xlabel('Cohort Month')
axes[1].set_ylabel('Cohort Size')
axes[1].set_title('Cohort Sizes Over Time')
axes[1].grid(True, alpha=0.3)

# LTV trend
axes[2].plot(ltv_by_cohort.index, ltv_by_cohort['mean'].values, marker='o', linewidth=2, markersize=8, color='green')
axes[2].set_xlabel('Cohort Month')
axes[2].set_ylabel('Average Lifetime Value ($)')
axes[2].set_title('LTV Trend by Cohort')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\nCohort analysis complete!")
```

## Key Metrics

- **Retention Rate**: % of cohort active
- **Churn Rate**: % of cohort lost
- **Day/Month 1 Retention**: Early engagement
- **Lifetime Value**: Total revenue per user
- **Payback Period**: Time to recover CAC

## Insights to Look For

- Early retention predictors
- Differences between cohorts
- Seasonal patterns
- Engagement degradation
- Revenue trends

## Deliverables

- Cohort retention matrix
- Retention curve visualization
- Churn rate analysis
- Lifetime value calculations
- Revenue per cohort
- Executive summary with insights
- Actionable recommendations
