---
name: data-science
description: Data science and analytics expertise for statistical analysis, machine learning pipelines, data governance, business intelligence, predictive modeling, and analytics strategy. Use when building ML models, analyzing data, creating dashboards, or designing data architectures.
---

# Data Science Expert

Comprehensive data science frameworks for analytics, machine learning, and data-driven decision making.

## Data Strategy

### Data Maturity Model

| Level | Name                | Characteristics                           |
| ----- | ------------------- | ----------------------------------------- |
| 1     | **Ad Hoc**          | Manual, inconsistent, siloed              |
| 2     | **Opportunistic**   | Some automation, point solutions          |
| 3     | **Systematic**      | Defined processes, governance emerging    |
| 4     | **Differentiating** | Data-driven decisions, advanced analytics |
| 5     | **Transformative**  | AI-first, competitive advantage           |

### Analytics Value Chain

```
DATA → INFORMATION → INSIGHT → ACTION → VALUE

PROGRESSION:
Descriptive: What happened?
Diagnostic: Why did it happen?
Predictive: What will happen?
Prescriptive: What should we do?
Autonomous: Self-optimizing systems
```

## Statistical Analysis

### Descriptive Statistics

```
CENTRAL TENDENCY:
- Mean: Sum / Count (sensitive to outliers)
- Median: Middle value (robust to outliers)
- Mode: Most frequent value

DISPERSION:
- Range: Max - Min
- Variance: Average squared deviation
- Standard Deviation: √Variance
- IQR: Q3 - Q1 (robust)

DISTRIBUTION SHAPE:
- Skewness: Asymmetry (0 = symmetric)
- Kurtosis: Tail heaviness (3 = normal)
```

For detailed inferential statistics and hypothesis testing, see [Statistical Methods Reference](references/statistical-methods.md).

## Machine Learning

### Algorithm Selection

| Task                         | Algorithms                                                   | When to Use                      |
| ---------------------------- | ------------------------------------------------------------ | -------------------------------- |
| **Classification**           | Logistic Regression, Random Forest, XGBoost, Neural Networks | Categorical outcomes             |
| **Regression**               | Linear Regression, Ridge/Lasso, Random Forest, XGBoost       | Continuous outcomes              |
| **Clustering**               | K-Means, Hierarchical, DBSCAN                                | Group discovery                  |
| **Dimensionality Reduction** | PCA, t-SNE, UMAP                                             | Feature reduction, visualization |
| **Anomaly Detection**        | Isolation Forest, One-Class SVM, Autoencoders                | Outlier detection                |
| **Time Series**              | ARIMA, Prophet, LSTM                                         | Sequential data                  |
| **Recommendation**           | Collaborative Filtering, Content-Based, Matrix Factorization | Personalization                  |
| **NLP**                      | Transformers, BERT, GPT                                      | Text understanding/generation    |

For detailed ML pipelines, feature engineering, and model monitoring, see [ML Pipelines Reference](references/ml-pipelines.md).

## Data Governance

### Data Governance Framework

```
GOVERNANCE PILLARS:

POLICIES:
- Data ownership
- Data classification
- Data retention
- Data access
- Data quality standards

ROLES:
- Data Owner: Accountable for data domain
- Data Steward: Day-to-day quality management
- Data Custodian: Technical implementation
- Data Consumer: End user

PROCESSES:
- Data cataloging
- Metadata management
- Data lineage
- Issue resolution
- Change management

METRICS:
- Data quality scores
- Policy compliance
- Data access requests
- Issue resolution time
```

### Data Quality Dimensions

| Dimension        | Definition                        | Measurement               |
| ---------------- | --------------------------------- | ------------------------- |
| **Accuracy**     | Correct representation of reality | % records matching source |
| **Completeness** | All required data present         | % non-null values         |
| **Consistency**  | Same across systems               | % matching across sources |
| **Timeliness**   | Available when needed             | Latency, freshness        |
| **Validity**     | Conforms to format/rules          | % passing validation      |
| **Uniqueness**   | No unwanted duplicates            | Duplicate rate            |

## Business Intelligence

### BI Architecture

```
ARCHITECTURE LAYERS:

DATA SOURCES:
- Operational systems
- External data
- IoT/streaming

DATA INTEGRATION:
- ETL/ELT pipelines
- Data lakes
- Data warehouses

SEMANTIC LAYER:
- Business definitions
- Calculated metrics
- Hierarchies
- Relationships

PRESENTATION:
- Dashboards
- Reports
- Ad-hoc analysis
- Embedded analytics
```

### Dashboard Design Principles

```
DESIGN PRINCIPLES:

PURPOSE:
- One clear objective per dashboard
- Know your audience
- Enable decisions

LAYOUT:
- Most important top-left
- Related items grouped
- Progressive disclosure
- Whitespace for clarity

VISUALS:
- Right chart for data type
- Consistent formatting
- Minimal decoration
- Color with purpose

INTERACTIVITY:
- Filters for exploration
- Drill-down capability
- Cross-filtering
- Tooltip details
```

### Metric Design

```
METRIC DEFINITION TEMPLATE:

NAME: [Metric name]
DEFINITION: [Clear business definition]
FORMULA: [Precise calculation]
OWNER: [Responsible person]
DATA SOURCE: [Where it comes from]
GRAIN: [Level of detail]
FREQUENCY: [Update cadence]
DIMENSIONS: [Slicing attributes]
TARGETS: [Goals/benchmarks]
RELATED: [Related metrics]
```

## Predictive Modeling

### Use Case Framework

| Use Case                  | Business Application | Approach                |
| ------------------------- | -------------------- | ----------------------- |
| **Churn Prediction**      | Retention programs   | Classification          |
| **Demand Forecasting**    | Inventory planning   | Time series             |
| **Lead Scoring**          | Sales prioritization | Classification          |
| **Price Optimization**    | Revenue management   | Regression/RL           |
| **Fraud Detection**       | Risk mitigation      | Anomaly detection       |
| **Recommendation**        | Personalization      | Collaborative filtering |
| **Customer Segmentation** | Marketing targeting  | Clustering              |
| **Lifetime Value**        | Customer investment  | Regression              |

## Data Ethics & Privacy

### Ethical AI Framework

```
PRINCIPLES:

FAIRNESS:
- No discriminatory outcomes
- Bias testing across groups
- Regular auditing

ACCOUNTABILITY:
- Clear ownership
- Decision audit trails
- Escalation process

TRANSPARENCY:
- Explainable decisions
- Clear documentation
- User communication

PRIVACY:
- Data minimization
- Consent management
- Security controls
```

### Bias Detection

```
BIAS TYPES:

HISTORICAL: Reflects past discrimination
REPRESENTATION: Training data not representative
MEASUREMENT: Proxy variables correlate with protected attributes
AGGREGATION: Single model for diverse populations
EVALUATION: Inappropriate benchmarks

FAIRNESS METRICS:
- Demographic Parity: Equal positive rates
- Equalized Odds: Equal TPR and FPR
- Individual Fairness: Similar inputs, similar outputs
- Calibration: Equal accuracy across groups
```

## Analytics Team Structure

### Team Roles

| Role                   | Focus                      | Skills                      |
| ---------------------- | -------------------------- | --------------------------- |
| **Data Engineer**      | Pipelines, infrastructure  | SQL, Python, Spark, Cloud   |
| **Data Analyst**       | Reporting, ad-hoc analysis | SQL, BI tools, Statistics   |
| **Data Scientist**     | Modeling, ML               | Python/R, ML, Statistics    |
| **ML Engineer**        | Model deployment           | MLOps, Software Engineering |
| **Analytics Engineer** | Data modeling              | dbt, SQL, Data Modeling     |

### Operating Models

| Model             | Description                   | Best For                |
| ----------------- | ----------------------------- | ----------------------- |
| **Centralized**   | Single analytics team         | Consistency, efficiency |
| **Decentralized** | Embedded in business units    | Business alignment      |
| **Hub & Spoke**   | Central CoE + embedded        | Balance of both         |
| **Federated**     | Shared platform, domain teams | Scale with autonomy     |

## References

- [ML Pipelines Reference](references/ml-pipelines.md) - Detailed ML pipeline, feature engineering, model development
- [Statistical Methods Reference](references/statistical-methods.md) - Inferential statistics, hypothesis testing, evaluation metrics

## See Also

- [Fortune 50 Product Management](../fortune50-product-management/SKILL.md)
- [Fortune 50 Business Strategy](../fortune50-business-strategy/SKILL.md)
- [Fortune 50 Finance](../fortune50-finance/SKILL.md)
