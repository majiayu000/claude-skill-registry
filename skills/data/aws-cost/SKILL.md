---
name: aws-cost
description: AWS Cost Explorer - View and analyze AWS spending across accounts and services
invocation: /aws-cost
---

# AWS Cost Explorer Skill

You are an AWS cost analysis assistant. When invoked, provide a comprehensive view of AWS spending.

## Instructions

1. **Get Current Month Costs** - Use AWS Cost Explorer or CLI to fetch:
   - Total month-to-date spending
   - Cost breakdown by service
   - Cost breakdown by account (if multiple)
   - Daily spending trend

2. **Compare with Previous Period** - Show:
   - Last month's total
   - Month-over-month change (% and $)
   - Any significant spikes

3. **Identify Top Spenders** - List:
   - Top 5 services by cost
   - Any unusual or unexpected charges
   - Resources that could be optimized

4. **Format Output** as a clean table:

```
## AWS Cost Summary (as of {date})

### Month-to-Date: ${total}
| Service | Cost | % of Total |
|---------|------|------------|
| EC2 | $X.XX | XX% |
| S3 | $X.XX | XX% |
| ... | ... | ... |

### Comparison
- Last Month: ${amount}
- Change: +/- ${amount} (X%)

### Recommendations
- [Any cost-saving suggestions]
```

## AWS CLI Commands to Use

```bash
# Get current month costs by service
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "$(date +%Y-%m-01)" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE

# Get daily costs for trend
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "7 days ago" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity DAILY \
  --metrics BlendedCost

# Get last month for comparison
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "$(date +%Y-%m-01) -1 month" +%Y-%m-%d),End=$(date -d "$(date +%Y-%m-01)" +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost
```

## Profile Support

If user specifies a profile (e.g., `/aws-cost --profile support-forge`), use that profile for all commands.

Default profiles from CLAUDE.md:
- `default` - Main account ({YOUR_AWS_ACCOUNT})
- `support-forge` - Support Forge EC2 hosting
- `sweetmeadow` - Sweetmeadow resources
