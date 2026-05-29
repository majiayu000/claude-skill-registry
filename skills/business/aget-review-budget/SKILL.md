---
name: aget-review-budget
description: Review budget allocation and ROI
archetype: executive
allowed-tools:
  - Read
  - Glob
  - Grep
---

# aget-review-budget

Review budget allocation, ROI, and resource distribution. Provides financial analysis and optimization recommendations.

## Instructions

When this skill is invoked:

1. **Gather Budget Data**
   - Planned allocation
   - Actual expenditure
   - Time period scope

2. **Categorize Expenditures**
   - By type (operational, capital, etc.)
   - By department/project
   - By priority

3. **Calculate ROI**
   - Investment amount
   - Return measurement
   - ROI percentage

4. **Variance Analysis**
   - Planned vs. actual
   - Significant variances
   - Root causes

5. **Optimization Opportunities**
   - Cost reduction areas
   - Reallocation suggestions
   - Efficiency improvements

## Output Format

```markdown
## Budget Review: [Period/Scope]

### Overview

| Metric | Value |
|--------|-------|
| Total Budget | $[X] |
| Total Spent | $[Y] |
| Variance | $[Z] ([N]%) |
| Period | [Date range] |

---

### Expenditure by Category

| Category | Planned | Actual | Variance |
|----------|---------|--------|----------|
| [Cat 1] | $[X] | $[Y] | $[Z] |
| [Cat 2] | $[X] | $[Y] | $[Z] |
| **Total** | $[X] | $[Y] | $[Z] |

---

### ROI Analysis

| Investment | Cost | Return | ROI |
|------------|------|--------|-----|
| [Project 1] | $[X] | $[Y] | [N]% |
| [Project 2] | $[X] | $[Y] | [N]% |

---

### Variance Analysis

#### Significant Variances

1. **[Category]**: $[Amount] ([N]%)
   - Root cause: [Explanation]
   - Action: [Recommended response]

---

### Optimization Recommendations

1. **[Area]**: [Recommendation]
   - Potential savings: $[X]
   - Implementation effort: [Low/Med/High]

---

### Risks

- [Financial risk to monitor]
```

## Constraints

- **C1**: NEVER fabricate financial data — financial integrity essential
- **C2**: NEVER make spending decisions — executive reviews, doesn't automate decisions
- **C3**: NEVER expose sensitive financial details in logs — financial data requires confidentiality

## Related

- SKILL-026: aget-review-budget specification
- ONTOLOGY_executive.yaml: Budget, ROI, Delegation concepts
- CAP-EXE-002: Budget Review capability
