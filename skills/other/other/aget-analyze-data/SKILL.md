---
name: aget-analyze-data
description: Analyze datasets to discover patterns and generate insights
archetype: analyst
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# aget-analyze-data

Perform analysis on datasets to discover patterns, trends, and anomalies. Generate actionable insights from data.

## Instructions

When this skill is invoked:

1. **Profile the Dataset**
   - Identify data structure (fields, types, record count)
   - Assess data quality (completeness, consistency)
   - Note any limitations or caveats

2. **Compute Statistics**
   - For numerical fields: mean, median, range, distribution
   - For categorical fields: frequency counts, top values
   - For temporal fields: trends, seasonality

3. **Discover Patterns**
   - Identify correlations between fields
   - Detect outliers and anomalies
   - Find trends over time (if applicable)

4. **Generate Insights**
   - Translate findings into actionable statements
   - Prioritize by potential impact
   - Distinguish correlation from causation

## Output Format

```markdown
## Data Analysis: [Dataset/Topic]

### Dataset Profile

| Attribute | Value |
|-----------|-------|
| Records | [N] |
| Fields | [N] |
| Date Range | [Start - End] |
| Quality | [Good/Fair/Poor] |

### Key Statistics

| Field | Type | Summary |
|-------|------|---------|
| [Field 1] | Numeric | Mean: X, Median: Y, Range: [A-B] |
| [Field 2] | Categorical | Top: [Value] (N%), [Value] (N%) |

### Patterns Discovered

1. **[Pattern Name]**: [Description]
   - Evidence: [Data points supporting this]
   - Confidence: [High/Medium/Low]

### Anomalies

- [Anomaly 1]: [Description and potential significance]

### Actionable Insights

1. **[Insight]**: [Recommended action based on finding]

### Limitations

- [Limitation 1]: [How it affects conclusions]
```

## Constraints

- **C1**: NEVER present correlation as causation — statistical rigor required
- **C2**: NEVER ignore outliers without explicit justification — anomalies may be valuable
- **C3**: NEVER overfit conclusions to limited data — acknowledge sample limitations

## Related

- SKILL-016: aget-analyze-data specification
- ONTOLOGY_analyst.yaml: Dataset, Analysis, Insight concepts
- CAP-ANL-001: Data Analysis capability
