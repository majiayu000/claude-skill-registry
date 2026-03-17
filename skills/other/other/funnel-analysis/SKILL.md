---
name: Funnel Analysis
description: Analyze user conversion funnels, identify drop-off points, and optimize conversion rates for conversion optimization and user flow analysis
---

# Funnel Analysis

## Overview

Funnel analysis tracks user progression through sequential steps, identifying where users drop off and optimizing each stage for better conversion.

## When to Use

- When optimizing user conversion paths and improving conversion rates
- When identifying bottlenecks and drop-off points in user flows
- When comparing performance across different segments or traffic sources
- When measuring product feature adoption or onboarding effectiveness
- When improving customer journey efficiency and user experience
- When A/B testing different funnel configurations or designs

## Funnel Structure

- **Stage 1**: Initial entry (landing page, app open)
- **Stage 2-N**: Intermediate steps (signup, selection, payment)
- **Final Stage**: Goal completion (purchase, subscription, sign-up)
- **Drop-off**: Users not progressing to next stage
- **Conversion Rate**: % progressing to next step

## Key Metrics

- **Drop-off Rate**: % leaving at each stage
- **Conversion Rate**: % progressing per stage
- **Funnel Efficiency**: Overall conversion (Stage 1 to Final)
- **Friction Score**: Identifying problem areas

## Implementation with Python

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Create sample funnel data
np.random.seed(42)

funnel_stages = ['Landing Page', 'Sign Up', 'Product Selection', 'Add to Cart', 'Checkout', 'Payment', 'Confirmation']

# Simulate user journey (progressive drop-off)
data = []
users_at_stage = 100000
for i, stage in enumerate(funnel_stages):
    # Progressively lower retention
    drop_off_rate = 0.15 + (i * 0.05)  # Increasing drop-off
    users_at_stage = int(users_at_stage * (1 - drop_off_rate))

    for _ in range(users_at_stage):
        data.append({
            'user_id': f'user_{np.random.randint(0, 1000000)}',
            'stage': stage,
            'timestamp': np.random.randint(0, 365),
        })

df = pd.DataFrame(data)

# 1. Funnel Counts
funnel_counts = df['stage'].value_counts().reindex(funnel_stages)
print("Funnel Counts by Stage:")
print(funnel_counts)

# 2. Funnel Metrics
funnel_metrics = pd.DataFrame({
    'Stage': funnel_stages,
    'Users': funnel_counts.values,
})

funnel_metrics['Drop-off'] = funnel_metrics['Users'].shift(1) - funnel_metrics['Users']
funnel_metrics['Drop-off %'] = (funnel_metrics['Drop-off'] / funnel_metrics['Users'].shift(1) * 100).round(2)
funnel_metrics['Conversion %'] = (funnel_metrics['Users'] / funnel_metrics['Users'].iloc[0] * 100).round(2)

print("\nFunnel Metrics:")
print(funnel_metrics)

# 3. Visualization - Funnel Chart
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Traditional funnel visualization
ax = axes[0]
colors = plt.cm.RdYlGn_r(np.linspace(0.3, 0.7, len(funnel_metrics)))

for idx, (stage, users) in enumerate(zip(funnel_metrics['Stage'], funnel_metrics['Users'])):
    # Create trapezoid-like bars
    width = users / funnel_metrics['Users'].max()
    y_pos = len(funnel_metrics) - idx - 1
    ax.barh(y_pos, width, left=(1 - width) / 2, height=0.6, color=colors[idx], edgecolor='black')
    ax.text(-0.05, y_pos, stage, ha='right', va='center', fontsize=10)
    ax.text(0.5, y_pos, f"{users:,}", ha='center', va='center', fontsize=9, fontweight='bold')

ax.set_xlim(0, 1)
ax.set_ylim(-0.5, len(funnel_metrics) - 0.5)
ax.set_xticks([])
ax.set_yticks([])
ax.set_title('Conversion Funnel')

# Step-by-step conversion
ax2 = axes[1]
x_pos = np.arange(len(funnel_stages))
colors2 = plt.cm.Spectral(np.linspace(0, 1, len(funnel_stages)))

bars = ax2.bar(x_pos, funnel_metrics['Users'], color=colors2, edgecolor='black', alpha=0.7)

# Add value labels
for i, (bar, users, conv) in enumerate(zip(bars, funnel_metrics['Users'], funnel_metrics['Conversion %'])):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width() / 2., height,
             f'{int(users):,}\n({conv:.1f}%)',
             ha='center', va='bottom', fontsize=9)

ax2.set_ylabel('User Count')
ax2.set_title('Users by Stage')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(funnel_stages, rotation=45, ha='right')
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# 4. Drop-off Analysis
fig, ax = plt.subplots(figsize=(12, 6))

# Filter out first stage (no drop-off from before)
drop_off_data = funnel_metrics[1:].copy()
drop_off_data = drop_off_data[drop_off_data['Drop-off'] > 0]

colors_drop = ['#d62728' if x > drop_off_data['Drop-off'].median() else '#2ca02c'
               for x in drop_off_data['Drop-off']]

bars = ax.barh(drop_off_data['Stage'], drop_off_data['Drop-off %'], color=colors_drop, edgecolor='black')

# Add value labels
for i, (bar, drop_pct) in enumerate(zip(bars, drop_off_data['Drop-off %'])):
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height() / 2.,
            f'{drop_pct:.1f}%',
            ha='left', va='center', fontsize=10, fontweight='bold')

ax.set_xlabel('Drop-off Rate (%)')
ax.set_title('Drop-off Rates by Stage')
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.show()

# 5. Funnel Efficiency Matrix
efficiency_matrix = funnel_metrics[['Stage', 'Conversion %']].copy()
print("\nFunnel Efficiency (% of Initial Users):")
print(efficiency_matrix)

# 6. Stage-to-stage conversion
fig, ax = plt.subplots(figsize=(12, 6))

stage_conversion = []
for i in range(len(funnel_metrics) - 1):
    conversion = (funnel_metrics.iloc[i + 1]['Users'] / funnel_metrics.iloc[i]['Users'] * 100)
    stage_conversion.append({
        'Transition': f"{funnel_metrics.iloc[i]['Stage']}\n→ {funnel_metrics.iloc[i+1]['Stage']}",
        'Conversion %': conversion
    })

stage_conv_df = pd.DataFrame(stage_conversion)
colors_stage = ['#2ca02c' if x > 80 else '#ff7f0e' if x > 60 else '#d62728'
                for x in stage_conv_df['Conversion %']]

bars = ax.bar(range(len(stage_conv_df)), stage_conv_df['Conversion %'], color=colors_stage, edgecolor='black')

# Add value labels
for bar, conv in zip(bars, stage_conv_df['Conversion %']):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2., height,
            f'{conv:.1f}%',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_ylabel('Conversion Rate (%)')
ax.set_title('Stage-to-Stage Conversion Rates')
ax.set_xticks(range(len(stage_conv_df)))
ax.set_xticklabels(stage_conv_df['Transition'], fontsize=9)
ax.set_ylim([0, 105])
ax.axhline(y=80, color='green', linestyle='--', alpha=0.5, label='Good (80%+)')
ax.axhline(y=60, color='orange', linestyle='--', alpha=0.5, label='Acceptable (60%+)')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# 7. Funnel by Segment (e.g., traffic source)
np.random.seed(42)
df['traffic_source'] = np.random.choice(['Organic', 'Paid', 'Direct'], len(df))

# Create funnel for each segment
fig, axes = plt.subplots(1, 3, figsize=(15, 6))

for idx, source in enumerate(['Organic', 'Paid', 'Direct']):
    df_segment = df[df['traffic_source'] == source]
    segment_counts = df_segment['stage'].value_counts().reindex(funnel_stages)

    segment_metrics = pd.DataFrame({
        'Stage': funnel_stages,
        'Users': segment_counts.values,
    })
    segment_metrics['Conversion %'] = (segment_metrics['Users'] / segment_metrics['Users'].iloc[0] * 100).round(2)

    ax = axes[idx]
    x_pos = np.arange(len(funnel_stages))
    bars = ax.bar(x_pos, segment_metrics['Users'], color='steelblue', edgecolor='black', alpha=0.7)

    for bar, conv in zip(bars, segment_metrics['Conversion %']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height,
                f'{conv:.1f}%',
                ha='center', va='bottom', fontsize=8)

    ax.set_title(f'Funnel: {source}')
    ax.set_ylabel('Users')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(funnel_stages, rotation=45, ha='right', fontsize=8)
    ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# 8. Comparison table of segments
print("\nFunnel Comparison by Traffic Source:")
comparison_data = []
for source in ['Organic', 'Paid', 'Direct']:
    df_segment = df[df['traffic_source'] == source]
    segment_counts = df_segment['stage'].value_counts().reindex(funnel_stages)
    comparison_data.append({
        'Traffic Source': source,
        'Landing': segment_counts.iloc[0],
        'Sign Up': segment_counts.iloc[1],
        'Product': segment_counts.iloc[2],
        'Cart': segment_counts.iloc[3],
        'Final Conv %': (segment_counts.iloc[-1] / segment_counts.iloc[0] * 100),
    })

comparison_df = pd.DataFrame(comparison_data)
print(comparison_df.round(2))

# 9. Sankey diagram representation (text-based)
print("\nFunnel Flow Summary:")
print("="*60)
for i in range(len(funnel_metrics) - 1):
    current = funnel_metrics.iloc[i]
    next_stage = funnel_metrics.iloc[i + 1]
    drop = current['Users'] - next_stage['Users']
    conv_pct = (next_stage['Users'] / current['Users'] * 100)

    print(f"{current['Stage']}")
    print(f"  ├─ Continue: {next_stage['Users']:>7,} ({conv_pct:>5.1f}%)")
    print(f"  └─ Drop-off: {drop:>7,} ({100-conv_pct:>5.1f}%)")
print(f"\n{funnel_metrics.iloc[-1]['Stage']}")
print("  └─ Completed: {0:,}".format(int(funnel_metrics.iloc[-1]['Users'])))

# 10. Key insights visualization
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('off')

insights = f"""
FUNNEL ANALYSIS SUMMARY

Total Users: {int(funnel_metrics['Users'].iloc[0]):,}
Conversions: {int(funnel_metrics['Users'].iloc[-1]):,}
Overall Conversion Rate: {funnel_metrics['Conversion %'].iloc[-1]:.2f}%

BOTTLENECKS (Highest Drop-off):
1. {funnel_metrics[funnel_metrics['Drop-off %'].idxmax()]['Stage']} - {funnel_metrics['Drop-off %'].max():.1f}%
2. {funnel_metrics[funnel_metrics['Drop-off %'].nlargest(2).index[1]]['Stage']}

BEST PERFORMERS (Highest Conversion):
1. {stage_conv_df.nlargest(2, 'Conversion %').iloc[0]['Transition'].split(chr(10))[1][2:]} - {stage_conv_df['Conversion %'].nlargest(2).iloc[0]:.1f}%
2. {stage_conv_df.nlargest(2, 'Conversion %').iloc[1]['Transition'].split(chr(10))[1][2:]} - {stage_conv_df['Conversion %'].nlargest(2).iloc[1]:.1f}%

RECOMMENDATIONS:
• Focus optimization on highest drop-off stages
• Benchmark against industry standards
• A/B test improvements at each stage
• Monitor segment performance separately
"""

ax.text(0.05, 0.95, insights, transform=ax.transAxes, fontfamily='monospace',
        fontsize=11, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.show()
```

## Funnel Analysis Steps

1. Define all stages in customer journey
2. Count users at each stage
3. Calculate drop-off and conversion rates
4. Identify biggest bottlenecks
5. Analyze by segments (traffic source, device, etc.)
6. Benchmark against goals
7. Prioritize optimization efforts

## Common Drop-off Points

- Complex signup forms
- Unexpected fees
- Confusing navigation
- Payment issues
- Technical errors

## Deliverables

- Funnel visualization chart
- Drop-off analysis table
- Stage-to-stage conversion rates
- Segmented funnel analysis
- Bottleneck identification
- Actionable optimization recommendations
- Benchmark comparison report
