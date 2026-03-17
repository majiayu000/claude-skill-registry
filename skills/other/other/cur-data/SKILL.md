---
name: cur-data
description: Knowledge about AWS Cost and Usage Report data structure, column formats, and analysis patterns
---

# AWS CUR Data Skill

## CUR File Formats

The project supports three CUR file formats:
- **CSV**: Plain text, largest file size
- **CSV.GZ**: Gzip compressed CSV, smaller
- **Parquet**: Columnar format, fastest and smallest (recommended)

## Column Name Variants

AWS CUR has two naming conventions. The data processor handles both:

| Canonical Name | Old Format | New Format |
|----------------|------------|------------|
| cost | `lineItem/UnblendedCost` | `line_item_unblended_cost` |
| account_id | `lineItem/UsageAccountId` | `line_item_usage_account_id` |
| service | `product/ProductName` | `product_product_name` |
| date | `lineItem/UsageStartDate` | `line_item_usage_start_date` |
| region | `product/Region` | `product_region` |
| line_item_type | `lineItem/LineItemType` | `line_item_line_item_type` |

## Key Cost Columns

```python
# Unblended cost - actual cost before discounts
line_item_unblended_cost

# Blended cost - averaged across organization
line_item_blended_cost

# Net cost - after discounts applied
line_item_net_unblended_cost

# Usage amount
line_item_usage_amount
```

## Line Item Types

```python
LINE_ITEM_TYPES = {
    'Usage': 'Normal usage charges',
    'Tax': 'Tax charges',
    'Fee': 'AWS fees',
    'Refund': 'Refunds/credits',
    'Credit': 'Applied credits',
    'RIFee': 'Reserved Instance fees',
    'DiscountedUsage': 'RI/SP discounted usage',
    'SavingsPlanCoveredUsage': 'Savings Plan usage',
    'SavingsPlanNegation': 'SP cost adjustment',
    'SavingsPlanUpfrontFee': 'SP upfront payment',
    'SavingsPlanRecurringFee': 'SP monthly fee',
    'BundledDiscount': 'Free tier/bundled',
    'EdpDiscount': 'Enterprise discount',
}
```

## Discount Analysis

To identify discounts and credits:
```python
discount_types = ['Credit', 'Refund', 'EdpDiscount', 'BundledDiscount']
discounts = df[df['line_item_type'].isin(discount_types)]
```

## Savings Plan Analysis

Key columns for savings plans:
```python
savings_plan_columns = [
    'savings_plan_savings_plan_arn',
    'savings_plan_savings_plan_rate',
    'savings_plan_used_commitment',
    'savings_plan_total_commitment_to_date',
]
```

## Common Aggregations

```python
# Cost by service
df.groupby('service').agg({'cost': 'sum'}).sort_values('cost', ascending=False)

# Cost by account and service
df.groupby(['account_id', 'service']).agg({'cost': 'sum'})

# Daily trends
df.groupby(df['date'].dt.date).agg({'cost': 'sum'})

# Monthly summary
df.groupby(df['date'].dt.to_period('M')).agg({'cost': 'sum'})
```

## Anomaly Detection

The project uses z-score based detection:
```python
mean = daily_costs.mean()
std = daily_costs.std()
z_scores = (daily_costs - mean) / std
anomalies = daily_costs[abs(z_scores) > 2]  # 2 std deviations
```

## Mock Data Reference

Test fixtures provide 6 months of data:
- **Production (111111111111)**: 87% of costs, steady growth
- **Development (210987654321)**: 13% of costs, spiky (load testing)
- **Services**: EC2, RDS, S3, CloudFront, DynamoDB, Lambda
- **Regions**: us-east-1, us-west-2, eu-west-1, ap-northeast-1, etc.
- **Total**: ~$6.2M over 182 days
