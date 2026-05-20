---
name: variance-analysis
description: Compare actuals vs budget with narrative
role_groups: [finance, leadership]
jtbd: |
  Variances happen every month but documenting them takes time. This prompts for 
  key variances, helps you document explanations with context, links to supporting 
  materials, and prepares a board-ready narrative so you're ready for leadership 
  reviews.
time_investment: "20-30 minutes per analysis"
---

## Purpose

Document budget variances with clear explanations and supporting context for leadership review.

## Usage

- `/variance-analysis [period]` - Document variances for specific period

---

## Steps

1. **Prompt for variance data:**
   - Budget category
   - Budgeted amount
   - Actual amount
   - Variance ($and %)

2. **For each material variance, ask:**
   - What caused this variance?
   - Is it timing or permanent?
   - What corrective actions if needed?
   - Supporting context

3. **Search for supporting context:**
   - Meeting notes mentioning the category
   - Project files
   - Relevant decisions made

4. **Create variance analysis document** with:
   - Executive summary
   - Variance details by category
   - Explanations with context
   - Outlook for rest of period

---

## Output Format

```markdown
# Variance Analysis: [Period]

## Executive Summary
- Total variance: $[X] ([X]%)
- Key drivers: [Top 2-3 factors]

## Material Variances

### [Category] - $[Variance]
- **Budget:** $[Amount]
- **Actual:** $[Amount]
- **Variance:** $[Amount] ([X]%)
- **Explanation:** [Reason]
- **Type:** Timing / Permanent
- **Outlook:** [Impact on rest of year]
```
