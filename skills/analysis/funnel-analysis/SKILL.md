---
name: funnel-analysis
description: Analyze user conversion funnels, calculate step-by-step conversion rates, create interactive visualizations, and identify optimization opportunities. Use when working with multi-step user journey data, conversion analysis, or when user mentions funnels, conversion rates, or user flow analysis.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Funnel Analysis Skill

Analyze user behavior through multi-step conversion funnels to identify bottlenecks and optimization opportunities in marketing campaigns, user journeys, and business processes.

## Quick Start

This skill helps you:
1. **Build conversion funnels** from multi-step user data
2. **Calculate conversion rates** between each step
3. **Perform segmentation analysis** by different user attributes
4. **Create interactive visualizations** with Plotly
5. **Generate business insights** and optimization recommendations

## When to Use

- Marketing campaign analysis (promotion → purchase)
- User onboarding flow analysis
- Website conversion funnel optimization
- App user journey analysis
- Sales pipeline analysis
- Lead nurturing process analysis

## Key Requirements

Install required packages:
```bash
pip install pandas plotly matplotlib numpy seaborn
```

## Core Workflow

### 1. Data Preparation
Your data should include:
- User journey steps (clicks, page views, actions)
- User identifiers (customer_id, user_id, etc.)
- Timestamps or step indicators
- Optional: user attributes for segmentation (gender, device, location)

### 2. Analysis Process
1. Load and merge user journey data
2. Define funnel steps and calculate metrics
3. Perform segmentations (by device, gender, etc.)
4. Create visualizations
5. Generate insights and recommendations

### 3. Output Deliverables
- Funnel visualization charts
- Conversion rate tables
- Segmented analysis reports
- Optimization recommendations

## Example Usage Scenarios

### E-commerce Purchase Funnel
```python
# Steps: Promotion → Search → Product View → Add to Cart → Purchase
# Analyze by device type and customer segment
```

### User Registration Funnel
```python
# Steps: Landing Page → Sign Up → Email Verification → Profile Complete
# Identify where users drop off most
```

### Content Consumption Funnel
```python
# Steps: Article View → Comment → Share → Subscribe
# Measure engagement conversion rates
```

## Common Analysis Patterns

1. **Bottleneck Identification**: Find steps with highest drop-off rates
2. **Segment Comparison**: Compare conversion across user groups
3. **Temporal Analysis**: Track conversion over time
4. **A/B Testing**: Compare different funnel variations
5. **Optimization Impact**: Measure changes before/after improvements

## Integration Examples

See [examples/](examples/) directory for:
- `basic_funnel.py` - Simple funnel analysis
- `segmented_funnel.py` - Advanced segmentation analysis
- Sample datasets for testing

## Best Practices

- Ensure data quality and consistency
- Define clear funnel steps
- Consider user journey time windows
- Validate statistical significance
- Focus on actionable insights