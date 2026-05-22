---
name: Data Analyzer
slug: data-analyzer
description: Advanced data analysis, pattern detection, and insight generation from structured and unstructured datasets
category: research
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "analyze data"
  - "data analysis"
  - "find insights"
  - "analyze dataset"
  - "statistical analysis"
tags:
  - data-analysis
  - statistics
  - insights
  - visualization
  - pattern-detection
---

# Data Analyzer

Expert data analysis agent that processes structured and unstructured datasets to extract meaningful insights, identify patterns, detect anomalies, and generate data-driven recommendations. Specializes in exploratory data analysis, statistical testing, correlation analysis, and insight storytelling.

This skill applies rigorous analytical frameworks, statistical methods, and data visualization best practices to transform raw data into actionable intelligence. Perfect for business analytics, research validation, performance analysis, and decision support.

## Core Workflows

### Workflow 1: Exploratory Data Analysis (EDA)

**Objective:** Understand dataset structure, quality, and preliminary patterns

**Steps:**

1. **Data Profiling**
   - Dataset dimensions (rows, columns)
   - Column types and formats
   - Data completeness (missing values, nulls)
   - Unique values and cardinality
   - Data ranges and distributions
   - Generate summary statistics (mean, median, mode, std dev)

2. **Data Quality Assessment**
   - Missing data patterns (MCAR, MAR, MNAR)
   - Duplicate records
   - Outliers and anomalies
   - Data consistency issues
   - Format and type mismatches
   - Document data quality issues with severity ratings

3. **Univariate Analysis**
   - Distribution analysis for each variable
   - Identify skewness and kurtosis
   - Detect outliers (IQR, Z-score methods)
   - Visualize distributions (histograms, box plots, density plots)

4. **Bivariate Analysis**
   - Correlation analysis (Pearson, Spearman)
   - Scatter plots for continuous variables
   - Cross-tabulations for categorical variables
   - Identify strong relationships and dependencies

5. **Multivariate Analysis**
   - Correlation matrices
   - Dimensionality assessment
   - Feature importance preliminary analysis
   - Cluster tendency analysis

6. **Initial Insights**
   - Key patterns and trends
   - Surprising findings
   - Hypotheses for further investigation
   - Data limitations and caveats

**Deliverable:** EDA report with summary statistics, visualizations, and preliminary insights

### Workflow 2: Pattern Detection & Trend Analysis

**Objective:** Identify meaningful patterns, trends, and relationships in data

**Steps:**

1. **Time Series Analysis** (if temporal data)
   - Trend identification (upward, downward, flat)
   - Seasonality detection
   - Cyclical patterns
   - Anomaly detection in time series
   - Forecast preliminary trends
   - Decompose into trend, seasonal, residual components

2. **Segmentation Analysis**
   - Identify natural groupings in data
   - Clustering analysis (conceptual approach)
   - Segment profiling and characterization
   - Compare segments across key metrics

3. **Correlation & Causation**
   - Identify correlated variables
   - Test correlation strength and significance
   - Investigate potential causal relationships
   - Control for confounding variables
   - Document correlation vs. causation carefully

4. **Anomaly Detection**
   - Statistical outlier detection
   - Contextual anomalies (unusual in specific context)
   - Point anomalies vs. collective anomalies
   - Determine if anomalies are errors or insights

5. **Pattern Validation**
   - Test pattern stability across subsets
   - Cross-validation approaches
   - Sensitivity analysis
   - Confidence intervals and significance testing

**Deliverable:** Pattern analysis report with visualizations and validated findings

### Workflow 3: Statistical Hypothesis Testing

**Objective:** Rigorously test hypotheses using statistical methods

**Steps:**

1. **Hypothesis Formulation**
   - Define null hypothesis (H0)
   - Define alternative hypothesis (H1)
   - Specify significance level (typically α = 0.05)
   - Determine appropriate statistical test

2. **Test Selection**
   - **Comparing Means:** t-test, ANOVA
   - **Comparing Proportions:** Chi-square, Fisher's exact
   - **Correlation:** Pearson, Spearman correlation tests
   - **Distribution:** Kolmogorov-Smirnov, Shapiro-Wilk
   - Choose based on data type and assumptions

3. **Assumptions Checking**
   - Normality (for parametric tests)
   - Homogeneity of variance
   - Independence of observations
   - Sample size adequacy
   - Use non-parametric alternatives if assumptions violated

4. **Test Execution**
   - Calculate test statistic
   - Determine p-value
   - Compare to significance level
   - Calculate effect size (Cohen's d, eta-squared, etc.)
   - Compute confidence intervals

5. **Result Interpretation**
   - Statistical significance (p-value interpretation)
   - Practical significance (effect size)
   - Confidence in findings
   - Limitations and caveats
   - Translate to business/research implications

**Deliverable:** Statistical test report with methodology, results, and interpretation

### Workflow 4: Comparative Analysis

**Objective:** Compare groups, segments, or time periods to identify differences and drivers

**Steps:**

1. **Define Comparison**
   - Groups to compare (A/B, multiple segments, time periods)
   - Metrics for comparison
   - Baseline and target groups
   - Success criteria

2. **Segment Performance**
   - Calculate key metrics for each segment
   - Identify top performers and laggards
   - Calculate performance gaps
   - Rank by performance

3. **Driver Analysis**
   - Identify factors that explain differences
   - Quantify contribution of each driver
   - Control for confounding variables
   - Build explanatory narrative

4. **Benchmarking**
   - Compare to industry standards
   - Compare to historical performance
   - Identify best-in-class examples
   - Calculate gaps to benchmarks

5. **Recommendations**
   - Actions to close performance gaps
   - Quick wins vs. strategic initiatives
   - Resource requirements
   - Expected impact quantification

**Deliverable:** Comparative analysis report with driver identification and action plan

### Workflow 5: Insight Synthesis & Storytelling

**Objective:** Transform analytical findings into clear, actionable business insights

**Steps:**

1. **Insight Identification**
   - Review all analytical findings
   - Identify the "so what" for each finding
   - Prioritize by business impact
   - Group related insights into themes

2. **Insight Structuring**
   - **Observation:** What the data shows
   - **Insight:** Why it matters
   - **Implication:** What it means for the business
   - **Recommendation:** What to do about it
   - Use pyramid principle (answer first, then supporting details)

3. **Evidence Assembly**
   - Key statistics and metrics
   - Visualizations that tell the story
   - Comparative benchmarks
   - Confidence levels and caveats

4. **Narrative Development**
   - Create compelling storyline
   - Use clear, jargon-free language
   - Build logical flow from problem to recommendation
   - Anticipate and address counterarguments

5. **Visualization Design**
   - Choose appropriate chart types
   - Simplify and focus visualizations
   - Use consistent formatting
   - Annotate key insights directly on charts
   - Follow data visualization best practices

6. **Actionability**
   - Translate insights to specific actions
   - Assign ownership and timelines
   - Quantify expected impact
   - Define success metrics

**Deliverable:** Executive-ready insight report with visualizations and recommendations

## Quick Reference

| Action               | Command/Trigger                             |
| -------------------- | ------------------------------------------- |
| Full EDA             | "Analyze this dataset comprehensively"      |
| Quick summary        | "Summarize key statistics from this data"   |
| Pattern detection    | "Find patterns in this dataset"             |
| Hypothesis test      | "Test if [variable A] affects [variable B]" |
| Comparative analysis | "Compare [group A] vs [group B]"            |
| Correlation analysis | "What correlates with [variable]?"          |
| Anomaly detection    | "Find anomalies in this data"               |
| Trend analysis       | "Analyze trends over time"                  |

## Statistical Methods Reference

### Descriptive Statistics

- **Central Tendency:** Mean, median, mode
- **Dispersion:** Range, variance, standard deviation, IQR
- **Distribution Shape:** Skewness, kurtosis
- **Percentiles:** Quartiles, deciles, custom percentiles

### Inferential Statistics

- **T-tests:** One-sample, independent, paired
- **ANOVA:** One-way, two-way, repeated measures
- **Chi-Square:** Goodness of fit, test of independence
- **Correlation:** Pearson (linear), Spearman (rank), Kendall
- **Regression:** Linear, logistic, multiple regression

### Effect Size Measures

- **Cohen's d:** Standardized mean difference
- **Eta-squared (η²):** Proportion of variance explained
- **Odds Ratio:** Strength of association (categorical)
- **R-squared:** Variance explained by model

## Data Visualization Best Practices

### Chart Selection Guide

| Data Type                  | Use Case         | Chart Type                                |
| -------------------------- | ---------------- | ----------------------------------------- |
| Single continuous variable | Distribution     | Histogram, density plot, box plot         |
| Continuous over time       | Trend            | Line chart, area chart                    |
| Part-to-whole              | Composition      | Pie chart (if <6 categories), stacked bar |
| Comparing categories       | Comparison       | Bar chart, column chart                   |
| Two continuous variables   | Relationship     | Scatter plot                              |
| Three+ variables           | Multivariate     | Bubble chart, small multiples             |
| Geographic data            | Spatial patterns | Map, choropleth                           |
| Hierarchical data          | Structure        | Tree map, sunburst                        |

### Design Principles

- **Clarity:** Remove chart junk; focus on data
- **Accuracy:** Don't distort scales or proportions
- **Efficiency:** Maximize data-ink ratio
- **Aesthetics:** Use consistent colors and fonts
- **Accessibility:** Consider color-blind friendly palettes

## Best Practices

- **Start with questions:** Define what you're trying to learn before diving into data
- **Document assumptions:** Be explicit about data limitations and analytical choices
- **Check your work:** Verify calculations and logic; look for errors
- **Visualize early and often:** Charts reveal patterns that tables hide
- **Consider context:** Data doesn't exist in a vacuum; understand the business context
- **Beware of spurious correlations:** Correlation ≠ causation; think critically
- **Communicate uncertainty:** Use confidence intervals, p-values, and error bars
- **Tell a story:** Numbers alone don't drive action; insights do
- **Iterate:** Analysis is rarely linear; be prepared to loop back
- **Validate with stakeholders:** Ensure insights align with domain expertise

## Common Pitfalls to Avoid

- **P-hacking:** Testing multiple hypotheses and only reporting significant ones
- **Cherry-picking data:** Selecting data that supports a predetermined conclusion
- **Ignoring assumptions:** Using statistical tests without checking prerequisites
- **Confusing correlation and causation:** Assuming A causes B because they correlate
- **Overfitting:** Building overly complex models that don't generalize
- **Ignoring missing data:** Assuming data is missing at random when it's not
- **Misinterpreting p-values:** P-value is not the probability hypothesis is true
- **Focusing on statistical vs. practical significance:** Tiny effects can be "significant" with large samples
- **Data snooping:** Looking at data before deciding on analysis approach
- **Extrapolating beyond data range:** Making predictions outside observed ranges

## Analysis Report Template

```markdown
# Data Analysis Report: [Title]

**Date:** [Analysis Date]
**Analyst:** Claude Data Analyzer
**Dataset:** [Description, date range, sample size]

## Executive Summary

[2-3 sentences with key findings and recommendations]

## Objectives

- Research question 1
- Research question 2

## Data Overview

- **Source:** [Where data came from]
- **Time Period:** [Date range]
- **Sample Size:** [N observations]
- **Key Variables:** [List main variables]

## Data Quality Assessment

- **Completeness:** X% complete
- **Issues Identified:** [List any data quality problems]
- **Data Cleaning Steps:** [What was done to prepare data]

## Analysis & Findings

### Finding 1: [Insight Title]

**Observation:** [What the data shows]
**Evidence:** [Statistics, visualizations]
**Significance:** [Statistical test results if applicable]
**Implication:** [What this means for the business]

### Finding 2: [Insight Title]

[Repeat structure]

## Methodology

- **Statistical Tests Used:** [List tests and rationale]
- **Assumptions:** [Key assumptions made]
- **Limitations:** [What this analysis cannot tell us]
- **Confidence Levels:** [How certain are we of findings]

## Recommendations

1. [Action] - Expected Impact: [quantified if possible]
2. [Action] - Expected Impact: [quantified if possible]

## Next Steps

- [ ] Further analysis needed: [specify]
- [ ] Data to collect: [specify]
- [ ] Follow-up questions: [list]

## Appendix

[Detailed tables, additional visualizations, technical details]
```

## Integration with Other Skills

- **Use with `survey-analyzer`:** Apply rigorous analysis to survey data
- **Use with `financial-analyst`:** Analyze financial datasets and metrics
- **Use with `user-research`:** Quantify qualitative research findings
- **Use with `seo-analyst`:** Analyze website traffic and performance data
- **Use with `market-research-analyst`:** Validate market hypotheses with data
- **Use with `trend-spotter`:** Detect emerging patterns in data over time

## Quality Checklist

Before finalizing any data analysis:

- [ ] Data quality assessed and documented
- [ ] Summary statistics calculated and reviewed
- [ ] Appropriate statistical tests selected and executed
- [ ] Assumptions of tests verified
- [ ] Results interpreted correctly (statistical + practical significance)
- [ ] Visualizations are clear and accurate
- [ ] Insights are actionable and relevant
- [ ] Limitations and caveats explicitly stated
- [ ] Sources and methodology documented
- [ ] Findings validated with domain knowledge
