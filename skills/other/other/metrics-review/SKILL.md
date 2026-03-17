---
name: metrics-review
description: Review key metrics and anomalies
role_groups: [operations, leadership]
jtbd: |
  Metrics drift and anomalies get missed. This checks recent metric mentions in 
  meetings, identifies trends or anomalies, prompts for context and analysis, and 
  documents insights so you stay on top of performance indicators.
time_investment: "10-15 minutes per review"
---

## Purpose

Monitor key metrics, identify anomalies, and document analysis.

## Usage

- `/metrics-review` - Review all tracked metrics
- `/metrics-review [metric]` - Focus on specific metric

---

## Steps

1. **Identify tracked metrics:**
   - Search meeting notes for metric discussions
   - Check 01-Quarter_Goals/Quarter_Goals.md for success metrics
   - Review project files for KPIs

2. **For each metric:**
   - Current value
   - Trend (up/down/stable)
   - vs. Target
   - vs. Previous period

3. **Flag anomalies:**
   - Unexpected changes
   - Missing data
   - Concerning trends

4. **Prompt for context:**
   - What's driving this trend?
   - Is this expected?
   - Action needed?

5. **Document insights**

---

## Output Format

```markdown
# Metrics Review: [Date]

## Key Metrics

### [Metric Name]
- **Current:** [Value]
- **vs. Target:** [On track / Behind / Ahead]
- **Trend:** ↑/→/↓
- **Analysis:** [Context]

## Anomalies
- [Metric]: [Anomaly description] - Cause: [Explanation]

## Action Items
- [ ] [Action based on metric insight]
```
