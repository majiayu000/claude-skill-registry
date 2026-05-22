---
name: Data Visualization
description: Create effective visualizations using matplotlib and seaborn for exploratory analysis, presenting insights, and communicating findings with business stakeholders
---

# Data Visualization

## Overview

Data visualization transforms complex data into clear, compelling visual representations that reveal patterns, trends, and insights for storytelling and decision-making.

## When to Use

- Exploratory data analysis and pattern discovery
- Communicating insights to stakeholders
- Comparing distributions and relationships
- Presenting findings in reports and dashboards
- Identifying outliers and anomalies visually
- Creating publication-ready charts and graphs

## Visualization Types

- **Distributions**: Histograms, KDE, violin plots
- **Relationships**: Scatter plots, line plots, heatmaps
- **Comparisons**: Bar charts, box plots, ridge plots
- **Compositions**: Pie charts, stacked bars, treemaps
- **Temporal**: Line plots, area charts, time series
- **Multivariate**: Pair plots, correlation heatmaps

## Design Principles

- Choose appropriate chart type for data
- Minimize ink-to-data ratio
- Use color purposefully
- Label clearly and completely
- Maintain consistent scales
- Consider accessibility

## Implementation with Python

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Generate sample data
np.random.seed(42)
n = 500
data = pd.DataFrame({
    'age': np.random.uniform(20, 70, n),
    'income': np.random.exponential(50000, n),
    'education_years': np.random.uniform(12, 20, n),
    'category': np.random.choice(['A', 'B', 'C'], n),
    'region': np.random.choice(['North', 'South', 'East', 'West'], n),
    'satisfaction': np.random.uniform(1, 5, n),
    'purchased': np.random.choice([0, 1], n),
})

print(data.head())

# 1. Distribution Plots
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Histogram
axes[0, 0].hist(data['age'], bins=30, color='skyblue', edgecolor='black')
axes[0, 0].set_title('Age Distribution (Histogram)')
axes[0, 0].set_xlabel('Age')
axes[0, 0].set_ylabel('Frequency')

# KDE plot
data['income'].plot(kind='kde', ax=axes[0, 1], color='green', linewidth=2)
axes[0, 1].set_title('Income Distribution (KDE)')
axes[0, 1].set_xlabel('Income')

# Box plot
sns.boxplot(data=data, y='satisfaction', x='category', ax=axes[1, 0], palette='Set2')
axes[1, 0].set_title('Satisfaction by Category (Box Plot)')

# Violin plot
sns.violinplot(data=data, y='age', x='category', ax=axes[1, 1], palette='Set2')
axes[1, 1].set_title('Age by Category (Violin Plot)')

plt.tight_layout()
plt.show()

# 2. Relationship Plots
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Scatter plot
axes[0, 0].scatter(data['age'], data['income'], alpha=0.5, s=30)
axes[0, 0].set_title('Age vs Income (Scatter Plot)')
axes[0, 0].set_xlabel('Age')
axes[0, 0].set_ylabel('Income')

# Scatter with regression line
sns.regplot(x='age', y='income', data=data, ax=axes[0, 1], scatter_kws={'alpha': 0.5})
axes[0, 1].set_title('Age vs Income (with Regression Line)')

# Joint plot alternative
ax_hex = axes[1, 0]
hexbin = ax_hex.hexbin(data['age'], data['income'], gridsize=15, cmap='YlOrRd')
ax_hex.set_title('Age vs Income (Hex Bin)')
ax_hex.set_xlabel('Age')
ax_hex.set_ylabel('Income')

# Bubble plot
scatter = axes[1, 1].scatter(
    data['age'], data['income'], s=data['satisfaction']*50,
    c=data['satisfaction'], cmap='viridis', alpha=0.6, edgecolors='black'
)
axes[1, 1].set_title('Age vs Income (Bubble Plot)')
axes[1, 1].set_xlabel('Age')
axes[1, 1].set_ylabel('Income')
plt.colorbar(scatter, ax=axes[1, 1], label='Satisfaction')

plt.tight_layout()
plt.show()

# 3. Comparison Plots
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Bar plot
category_counts = data['category'].value_counts()
axes[0, 0].bar(category_counts.index, category_counts.values, color='skyblue', edgecolor='black')
axes[0, 0].set_title('Category Distribution (Bar Chart)')
axes[0, 0].set_ylabel('Count')

# Grouped bar plot
grouped_data = data.groupby(['category', 'region']).size().unstack()
grouped_data.plot(kind='bar', ax=axes[0, 1], edgecolor='black')
axes[0, 1].set_title('Category by Region (Grouped Bar)')
axes[0, 1].set_ylabel('Count')
axes[0, 1].legend(title='Region')

# Stacked bar plot
grouped_data.plot(kind='bar', stacked=True, ax=axes[1, 0], edgecolor='black')
axes[1, 0].set_title('Category by Region (Stacked Bar)')
axes[1, 0].set_ylabel('Count')

# Horizontal bar plot
region_counts = data['region'].value_counts()
axes[1, 1].barh(region_counts.index, region_counts.values, color='lightcoral', edgecolor='black')
axes[1, 1].set_title('Region Distribution (Horizontal Bar)')
axes[1, 1].set_xlabel('Count')

plt.tight_layout()
plt.show()

# 4. Correlation and Heatmaps
numeric_cols = data[['age', 'income', 'education_years', 'satisfaction']].corr()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Correlation heatmap
sns.heatmap(numeric_cols, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, ax=axes[0], cbar_kws={'label': 'Correlation'})
axes[0].set_title('Correlation Matrix Heatmap')

# Clustermap alternative
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist, squareform

# Create a simpler heatmap for category averages
category_avg = data.groupby('category')[['age', 'income', 'education_years', 'satisfaction']].mean()
sns.heatmap(category_avg.T, annot=True, fmt='.1f', cmap='YlGnBu', ax=axes[1],
            cbar_kws={'label': 'Average Value'})
axes[1].set_title('Average Values by Category')

plt.tight_layout()
plt.show()

# 5. Pair Plot
pair_cols = ['age', 'income', 'education_years', 'satisfaction']
plt.figure(figsize=(12, 10))
pair_plot = sns.pairplot(data[pair_cols], diag_kind='hist', corner=False)
pair_plot.fig.suptitle('Pair Plot Matrix', y=1.00)
plt.show()

# 6. Multi-dimensional Visualization
fig = plt.figure(figsize=(14, 6))
gs = GridSpec(2, 3, figure=fig)

# Subplots with different aspects
ax1 = fig.add_subplot(gs[0, 0])
ax1.scatter(data['age'], data['income'], c=data['satisfaction'], cmap='viridis', alpha=0.6)
ax1.set_title('Age vs Income (colored by Satisfaction)')
ax1.set_xlabel('Age')
ax1.set_ylabel('Income')

ax2 = fig.add_subplot(gs[0, 1])
for cat in data['category'].unique():
    subset = data[data['category'] == cat]
    ax2.scatter(subset['age'], subset['income'], label=cat, alpha=0.6)
ax2.set_title('Age vs Income (by Category)')
ax2.set_xlabel('Age')
ax2.set_ylabel('Income')
ax2.legend()

ax3 = fig.add_subplot(gs[0, 2])
sns.boxplot(data=data, x='region', y='income', ax=ax3, palette='Set2')
ax3.set_title('Income Distribution by Region')

ax4 = fig.add_subplot(gs[1, 0])
data.groupby('category')['satisfaction'].mean().plot(kind='bar', ax=ax4, color='skyblue', edgecolor='black')
ax4.set_title('Average Satisfaction by Category')
ax4.set_ylabel('Satisfaction')
ax4.set_xlabel('Category')

ax5 = fig.add_subplot(gs[1, 1:])
region_category = pd.crosstab(data['region'], data['category'])
region_category.plot(kind='bar', ax=ax5, edgecolor='black')
ax5.set_title('Region vs Category Distribution')
ax5.set_ylabel('Count')
ax5.set_xlabel('Region')
ax5.legend(title='Category')

plt.tight_layout()
plt.show()

# 7. Time Series Visualization (if temporal data)
dates = pd.date_range('2023-01-01', periods=len(data))
data['date'] = dates
data['cumulative_income'] = data['income'].cumsum()

fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Line plot
axes[0].plot(data['date'], data['income'], linewidth=1, alpha=0.7, label='Income')
axes[0].fill_between(data['date'], data['income'], alpha=0.3)
axes[0].set_title('Income Over Time')
axes[0].set_ylabel('Income')
axes[0].grid(True, alpha=0.3)
axes[0].legend()

# Area plot
axes[1].plot(data['date'], data['cumulative_income'], linewidth=2, color='green')
axes[1].fill_between(data['date'], data['cumulative_income'], alpha=0.3, color='green')
axes[1].set_title('Cumulative Income Over Time')
axes[1].set_ylabel('Cumulative Income')
axes[1].set_xlabel('Date')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 8. Composition Visualization
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Pie chart
category_counts = data['category'].value_counts()
colors = ['#ff9999', '#66b3ff', '#99ff99']
axes[0].pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%',
            colors=colors, startangle=90)
axes[0].set_title('Category Distribution (Pie Chart)')

# Donut chart
axes[1].pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%',
            colors=colors, startangle=90, wedgeprops=dict(width=0.5, edgecolor='white'))
axes[1].set_title('Category Distribution (Donut Chart)')

plt.tight_layout()
plt.show()

# 9. Dashboard-style Visualization
fig = plt.figure(figsize=(16, 10))
gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)

# Key metrics
ax_metric = fig.add_subplot(gs[0, :])
ax_metric.axis('off')
metrics_text = f"""
Average Age: {data['age'].mean():.1f} | Average Income: ${data['income'].mean():.0f} |
Average Satisfaction: {data['satisfaction'].mean():.2f} | Purchase Rate: {(data['purchased'].mean()*100):.1f}%
"""
ax_metric.text(0.5, 0.5, metrics_text, ha='center', va='center', fontsize=12,
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

# Subplots
ax1 = fig.add_subplot(gs[1, 0])
data['age'].hist(bins=20, ax=ax1, color='skyblue', edgecolor='black')
ax1.set_title('Age Distribution')

ax2 = fig.add_subplot(gs[1, 1])
category_counts.plot(kind='bar', ax=ax2, color='lightcoral', edgecolor='black')
ax2.set_title('Category Counts')

ax3 = fig.add_subplot(gs[1, 2])
data.groupby('category')['satisfaction'].mean().plot(kind='bar', ax=ax3, color='lightgreen', edgecolor='black')
ax3.set_title('Avg Satisfaction by Category')

ax4 = fig.add_subplot(gs[2, :2])
sns.boxplot(data=data, x='region', y='income', ax=ax4, palette='Set2')
ax4.set_title('Income by Region')

ax5 = fig.add_subplot(gs[2, 2])
data['satisfaction'].value_counts().sort_index().plot(kind='bar', ax=ax5, color='orange', edgecolor='black')
ax5.set_title('Satisfaction Scores')

plt.suptitle('Data Analytics Dashboard', fontsize=16, fontweight='bold', y=0.995)
plt.show()

print("Visualization examples completed!")
```

## Visualization Best Practices

- Choose chart type based on data type and question
- Use consistent color schemes
- Label axes clearly with units
- Include title and legend
- Avoid 3D charts when 2D suffices
- Make fonts large and readable
- Consider colorblind-friendly palettes

## Common Chart Types

- **Bar charts**: Categorical comparisons
- **Line plots**: Trends over time
- **Scatter plots**: Relationships between variables
- **Histograms**: Distributions
- **Heatmaps**: Matrix data
- **Box plots**: Distribution with quartiles

## Deliverables

- Exploratory visualizations
- Publication-ready charts
- Interactive dashboard mockups
- Statistical plots with annotations
- Trend analysis visualizations
- Comparative analysis charts
- Summary infographics
