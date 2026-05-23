---
name: data-exploration
description: Explore and analyze pilot data sets to uncover patterns, anomalies, and initial insights. Use when performing ad-hoc data investigations, validating data quality, or preparing exploratory visualizations for hypothesis generation.
---

# Data Exploration

## Overview

The data-exploration skill enables systematic investigation of datasets to uncover patterns, validate quality, and surface insights that inform decision-making. This skill is used when you need to understand a new dataset, validate data quality before analysis, or generate initial findings for hypothesis formation.

## Quick Start

Use this skill when you need to:
- **Understand a new dataset**: Get initial feel for structure, quality, and contents
- **Validate data quality**: Check for completeness, accuracy, and consistency
- **Find patterns**: Identify trends, correlations, or anomalies
- **Generate insights**: Surface findings that could inform strategic decisions
- **Prepare for hypothesis testing**: Establish baseline understanding before formal analysis

## Workflow Decision Tree

```
New Dataset → Data Profiling → Quality Assessment → Pattern Discovery → Insight Generation
                    ↓                  ↓                    ↓                  ↓
            [Statistical Summary] [Quality Report]  [Visual Analysis]  [Intelligence Brief]
```

## Data Profiling

### Step 1: Initial Assessment

When you receive a new dataset, start with basic profiling:

```python
import pandas as pd
import numpy as np

def profile_dataset(df: pd.DataFrame) -> dict:
    """Generate initial dataset profile."""
    profile = {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "memory_usage": df.memory_usage(deep=True).sum() / 1024**2,  # MB
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": df.duplicated().sum()
    }
    return profile
```

**Output**: Dataset profile with shape, columns, types, memory usage, missing values

### Step 2: Statistical Summary

Generate descriptive statistics for numerical and categorical columns:

```python
def generate_statistical_summary(df: pd.DataFrame) -> dict:
    """Create statistical summary of dataset."""
    summary = {}

    # Numerical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        summary['numerical'] = df[numeric_cols].describe().to_dict()

    # Categorical columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(categorical_cols) > 0:
        summary['categorical'] = {
            col: {
                'unique_values': df[col].nunique(),
                'top_5_values': df[col].value_counts().head(5).to_dict(),
                'missing': df[col].isnull().sum()
            }
            for col in categorical_cols
        }

    # Temporal columns
    datetime_cols = df.select_dtypes(include=['datetime64']).columns
    if len(datetime_cols) > 0:
        summary['temporal'] = {
            col: {
                'min': df[col].min(),
                'max': df[col].max(),
                'range_days': (df[col].max() - df[col].min()).days
            }
            for col in datetime_cols
        }

    return summary
```

**Output**: Statistical summary organized by column type

## Quality Assessment

### Data Quality Checks

Apply systematic quality checks to identify issues:

```python
def assess_data_quality(df: pd.DataFrame) -> dict:
    """Assess data quality and identify issues."""
    quality_report = {
        "completeness": {},
        "consistency": {},
        "accuracy": {},
        "issues": []
    }

    # Completeness: Missing values
    missing_pct = (df.isnull().sum() / len(df) * 100).to_dict()
    quality_report["completeness"] = {
        col: f"{pct:.2f}%"
        for col, pct in missing_pct.items() if pct > 0
    }

    # Flag columns with >20% missing
    for col, pct in missing_pct.items():
        if pct > 20:
            quality_report["issues"].append({
                "type": "completeness",
                "severity": "high" if pct > 50 else "medium",
                "column": col,
                "message": f"{col} has {pct:.2f}% missing values"
            })

    # Consistency: Duplicate rows
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        dup_pct = dup_count / len(df) * 100
        quality_report["consistency"]["duplicate_rows"] = f"{dup_count} ({dup_pct:.2f}%)"
        if dup_pct > 5:
            quality_report["issues"].append({
                "type": "consistency",
                "severity": "high" if dup_pct > 10 else "medium",
                "message": f"{dup_count} duplicate rows found ({dup_pct:.2f}%)"
            })

    # Consistency: Data type mismatches
    for col in df.columns:
        if df[col].dtype == 'object':
            # Check if numeric values are stored as strings
            try:
                pd.to_numeric(df[col], errors='coerce')
                numeric_pct = df[col].apply(lambda x: str(x).replace('.', '').replace('-', '').isdigit()).sum() / len(df)
                if numeric_pct > 0.8:  # If >80% could be numeric
                    quality_report["issues"].append({
                        "type": "consistency",
                        "severity": "low",
                        "column": col,
                        "message": f"{col} appears to contain numeric values but is stored as text"
                    })
            except:
                pass

    # Accuracy: Outliers in numerical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1 - 3*IQR) | (df[col] > Q3 + 3*IQR)][col]

        if len(outliers) > 0:
            outlier_pct = len(outliers) / len(df) * 100
            quality_report["accuracy"][col] = f"{len(outliers)} outliers ({outlier_pct:.2f}%)"

            if outlier_pct > 5:
                quality_report["issues"].append({
                    "type": "accuracy",
                    "severity": "medium" if outlier_pct < 10 else "high",
                    "column": col,
                    "message": f"{col} has {len(outliers)} potential outliers ({outlier_pct:.2f}%)"
                })

    return quality_report
```

**Output**: Quality report with completeness, consistency, accuracy issues

### Duke Data Governance Alignment

When working with Duke data, ensure alignment with data governance standards:

**Check**:
- [ ] Data classification identified (Public, Internal, Confidential, Restricted)
- [ ] Privacy requirements assessed (PII, FERPA, HIPAA)
- [ ] Data retention policy noted
- [ ] Access controls documented
- [ ] Data lineage tracked

**Reference**: [references/duke_data_governance.md](references/duke_data_governance.md)

## Pattern Discovery

### Visual Analysis

Create exploratory visualizations to identify patterns:

```python
import matplotlib.pyplot as plt
import seaborn as sns

def explore_patterns_visual(df: pd.DataFrame, output_dir: str = "./outputs"):
    """Generate exploratory visualizations."""

    # Distribution plots for numerical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        fig, axes = plt.subplots(len(numeric_cols), 1, figsize=(10, 3*len(numeric_cols)))
        if len(numeric_cols) == 1:
            axes = [axes]

        for idx, col in enumerate(numeric_cols):
            axes[idx].hist(df[col].dropna(), bins=30, edgecolor='black')
            axes[idx].set_title(f'Distribution of {col}')
            axes[idx].set_xlabel(col)
            axes[idx].set_ylabel('Frequency')

        plt.tight_layout()
        plt.savefig(f"{output_dir}/distributions.png")
        plt.close()

    # Correlation heatmap
    if len(numeric_cols) > 1:
        plt.figure(figsize=(10, 8))
        correlation = df[numeric_cols].corr()
        sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
        plt.title('Correlation Heatmap')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/correlation_heatmap.png")
        plt.close()

    # Time series if datetime column exists
    datetime_cols = df.select_dtypes(include=['datetime64']).columns
    if len(datetime_cols) > 0 and len(numeric_cols) > 0:
        for date_col in datetime_cols:
            for num_col in numeric_cols[:3]:  # First 3 numeric columns
                plt.figure(figsize=(12, 4))
                df.sort_values(date_col).plot(x=date_col, y=num_col, ax=plt.gca())
                plt.title(f'{num_col} over time')
                plt.tight_layout()
                plt.savefig(f"{output_dir}/timeseries_{num_col}.png")
                plt.close()
```

**Output**: Distribution plots, correlation heatmap, time series visualizations

### Anomaly Detection

Identify unusual patterns or outliers:

```python
from sklearn.ensemble import IsolationForest

def detect_anomalies(df: pd.DataFrame, contamination: float = 0.1) -> pd.DataFrame:
    """Detect anomalies using Isolation Forest."""

    # Select numerical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        return pd.DataFrame()

    # Prepare data
    X = df[numeric_cols].fillna(df[numeric_cols].median())

    # Detect anomalies
    clf = IsolationForest(contamination=contamination, random_state=42)
    anomaly_labels = clf.fit_predict(X)

    # Add anomaly flag to dataframe
    df_with_anomalies = df.copy()
    df_with_anomalies['is_anomaly'] = anomaly_labels == -1

    return df_with_anomalies[df_with_anomalies['is_anomaly']]
```

**Output**: Dataframe containing detected anomalies

## Insight Generation

### Generate Intelligence Brief

Synthesize findings into actionable intelligence:

**Template Structure**:

```markdown
# Data Exploration Report: [Dataset Name]
**Date**: [YYYY-MM-DD]
**Analyst**: Mayuri - Captain of Intelligence
**Dataset**: [description]

## Executive Summary
[2-3 sentences: Key findings and recommendations]

## Dataset Overview
- **Rows**: [count]
- **Columns**: [count]
- **Time Period**: [date range if applicable]
- **Data Quality Score**: [High/Medium/Low]

## Key Findings

### 1. [Finding Title]
**Observation**: [What was found]
**Evidence**: [Supporting statistics/visualizations]
**Implication**: [What this means for Duke]

### 2. [Finding Title]
...

## Data Quality Assessment
- **Completeness**: [summary of missing values]
- **Consistency**: [summary of duplicates, format issues]
- **Accuracy**: [summary of outliers, validation results]

### Issues Requiring Attention
- [ ] **High Priority**: [Issue description and recommended action]
- [ ] **Medium Priority**: [Issue description and recommended action]

## Patterns & Trends
- [Pattern 1]: [Description with supporting data]
- [Pattern 2]: [Description with supporting data]

## Anomalies Detected
- [Anomaly 1]: [Description, potential cause, recommended follow-up]
- [Anomaly 2]: [Description, potential cause, recommended follow-up]

## Recommendations
1. [Action item with rationale]
2. [Action item with rationale]
3. [Action item with rationale]

## Next Steps
- [ ] [Follow-up analysis needed]
- [ ] [Data quality improvements]
- [ ] [Stakeholder review required]

## Appendix
- Data Governance Classification: [Public/Internal/Confidential/Restricted]
- Privacy Considerations: [PII/FERPA/HIPAA notes]
- Data Sources: [List with access dates]
```

## Duke-Specific Considerations

### Alignment with 2026 Goals

When exploring data, always consider alignment with Duke's 2026 goals:

- **Goal**: Improve student service response times by 30%
  - **Data to explore**: Service desk tickets, response times, resolution times
  - **Look for**: Patterns in request types, peak times, staff utilization

- **Goal**: Enhance research computing capabilities
  - **Data to explore**: HPC usage, grant activity, researcher feedback
  - **Look for**: Utilization trends, capacity constraints, service gaps

### OIT Priority Alignment

Connect findings to OIT priorities:
- Infrastructure modernization
- Security posture improvement
- User experience enhancement
- Operational efficiency

**Reference**: [references/duke_2026_goals.md](references/duke_2026_goals.md)

## Common Use Cases

### Use Case 1: Pilot Data Validation

**Scenario**: Strategy Captain requests validation of data for AI service desk pilot

**Workflow**:
1. Load service desk ticket data
2. Profile dataset (shape, columns, types)
3. Assess quality (missing values, duplicates, consistency)
4. Explore patterns (common issues, peak times, resolution patterns)
5. Detect anomalies (unusual tickets, outlier response times)
6. Generate intelligence brief for Strategy Captain

### Use Case 2: Hypothesis Support

**Scenario**: Need data to support hypothesis about student service improvement

**Workflow**:
1. Load relevant datasets (tickets, surveys, usage logs)
2. Calculate baseline metrics (current response times, satisfaction scores)
3. Identify patterns (what's working, what's not)
4. Find correlations (factors affecting response time)
5. Generate findings to inform hypothesis testing

### Use Case 3: Early Warning Detection

**Scenario**: Monitor ongoing pilot for data quality degradation

**Workflow**:
1. Establish baseline data quality metrics
2. Set monitoring thresholds
3. Regular quality checks (daily/weekly)
4. Detect anomalies and trends
5. Generate early warning signal if thresholds crossed

## Tools & Libraries

### Required Python Libraries
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

### Recommended Tools
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical operations
- **Matplotlib/Seaborn**: Visualization
- **Scikit-learn**: Anomaly detection, statistical analysis
- **Jupyter**: Interactive exploration

## Resources

### scripts/
- [explore_dataset.py](scripts/explore_dataset.py): Main exploration script
- [quality_checks.py](scripts/quality_checks.py): Data quality assessment utilities
- [anomaly_detection.py](scripts/anomaly_detection.py): Anomaly detection implementations

### references/
- [duke_data_governance.md](references/duke_data_governance.md): Duke data governance standards
- [duke_2026_goals.md](references/duke_2026_goals.md): 2026 strategic goals
- [privacy_requirements.md](references/privacy_requirements.md): Privacy and compliance requirements
- [statistical_methods.md](references/statistical_methods.md): Reference for statistical techniques

### assets/
- [exploration_template.ipynb](assets/exploration_template.ipynb): Jupyter notebook template
- [quality_report_template.md](assets/quality_report_template.md): Quality report template
- [intelligence_brief_template.md](assets/intelligence_brief_template.md): Brief template

## Best Practices

1. **Start Broad, Then Focus**: Begin with overall profiling, then drill into interesting areas
2. **Document Assumptions**: Note any assumptions made during exploration
3. **Visualize Early**: Create visualizations to spot patterns humans can see but stats might miss
4. **Check Quality First**: Don't analyze bad data - validate quality before deep analysis
5. **Align with Goals**: Always connect findings back to Duke's strategic objectives
6. **Maintain Provenance**: Log data sources, access dates, and transformations applied
7. **Privacy First**: Be mindful of PII and sensitive data throughout exploration
8. **Iterate**: Exploration is iterative - new findings lead to new questions

## Decision Log Integration

Every data exploration should generate a decision log entry:

```python
from agents.mayuri_intelligence import MayuriIntelligence

mayuri = MayuriIntelligence()

# After exploration
mayuri.log_decision(
    decision_type="data_exploration_completed",
    inputs={
        "dataset": "service_desk_tickets_2025.csv",
        "rows": 15234,
        "date_range": "2025-01-01 to 2025-12-31"
    },
    outputs={
        "quality_score": "Medium",
        "issues_found": 3,
        "patterns_identified": 5,
        "brief_path": "./outputs/intelligence/BRIEF-20260105-143022.md"
    },
    rationale="Explored service desk data to establish baseline for AI chatbot pilot",
    metadata={
        "alignment": "2026 Goal: Improve student service response times",
        "stakeholder": "Strategy Captain (Kisuke)"
    }
)
```

## Remember

- **Quality over speed**: Thorough exploration prevents bad decisions later
- **Context matters**: Duke's environment, goals, and constraints shape what's important
- **Communicate findings**: Insights are useless if not shared in actionable format
- **Stay curious**: The best insights often come from unexpected patterns
- **Respect privacy**: Duke data governance and privacy standards are non-negotiable
