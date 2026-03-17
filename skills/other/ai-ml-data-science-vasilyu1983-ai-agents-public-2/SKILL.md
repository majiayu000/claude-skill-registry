---
name: ai-ml-data-science
description: "End-to-end data science and ML engineering workflows: problem framing, data/EDA, feature engineering (feature stores), modelling, evaluation/reporting, plus SQL transformations with SQLMesh. Use for dataset exploration, feature design, model selection, metrics and slice analysis, model cards/eval reports, experiment reproducibility, and production handoff (monitoring and retraining)."
---

# Data Science Engineering Suite - Quick Reference

This skill turns **raw data and questions** into **validated, documented models** ready for production:

- **EDA workflows**: Structured exploration with drift detection
- **Feature engineering**: Reproducible feature pipelines with leakage prevention and train/serve parity
- **Model selection**: Baselines first; strong tabular defaults; escalate complexity only when justified
- **Evaluation & reporting**: Slice analysis, uncertainty, model cards, production metrics
- **SQL transformation**: SQLMesh for staging/intermediate/marts layers
- **MLOps**: CI/CD, CT (continuous training), CM (continuous monitoring)
- **Production patterns**: Data contracts, lineage, feedback loops, streaming features

**Modern emphasis (2026):** Feature stores, automated retraining, drift monitoring (Evidently), train-serve parity, and agentic ML loops (plan -> execute -> evaluate -> improve). Tools: LightGBM, CatBoost, scikit-learn, PyTorch, Polars (lazy eval for larger-than-RAM datasets), lakeFS for data versioning.

---

## Quick Reference

| Task | Tool/Framework | Command | When to Use |
|------|----------------|---------|-------------|
| EDA & Profiling | Pandas, Great Expectations | `df.describe()`, `ge.validate()` | Initial data exploration and quality checks |
| Feature Engineering | Pandas, Polars, Feature Stores | `df.transform()`, Feast materialization | Creating lag, rolling, categorical features |
| Model Training | Gradient boosting, linear models, scikit-learn | `lgb.train()`, `model.fit()` | Strong baselines for tabular ML |
| Hyperparameter Tuning | Optuna, Ray Tune | `optuna.create_study()`, `tune.run()` | Optimizing model parameters |
| SQL Transformation | SQLMesh | `sqlmesh plan`, `sqlmesh run` | Building staging/intermediate/marts layers |
| Experiment Tracking | MLflow, W&B | `mlflow.log_metric()`, `wandb.log()` | Versioning experiments and models |
| Model Evaluation | scikit-learn, custom metrics | `metrics.roc_auc_score()`, slice analysis | Validating model performance |

---

## Data Lake & Lakehouse

For comprehensive data lake/lakehouse patterns (beyond SQLMesh transformation), see **[data-lake-platform](../data-lake-platform/SKILL.md)**:

- **Table formats:** Apache Iceberg, Delta Lake, Apache Hudi
- **Query engines:** ClickHouse, DuckDB, Apache Doris, StarRocks
- **Alternative transformation:** dbt (alternative to SQLMesh)
- **Ingestion:** dlt, Airbyte (connectors)
- **Streaming:** Apache Kafka patterns
- **Orchestration:** Dagster, Airflow

This skill focuses on **ML feature engineering and modeling**. Use data-lake-platform for general-purpose data infrastructure.

---

## Related Skills

For adjacent topics, reference:

- **[ai-mlops](../ai-mlops/SKILL.md)** - APIs, batch jobs, monitoring, drift, data ingestion (dlt)
- **[ai-llm](../ai-llm/SKILL.md)** - LLM prompting, fine-tuning, evaluation
- **[ai-rag](../ai-rag/SKILL.md)** - RAG pipelines, chunking, retrieval
- **[ai-llm-inference](../ai-llm-inference/SKILL.md)** - LLM inference optimization, quantization
- **[ai-ml-timeseries](../ai-ml-timeseries/SKILL.md)** - Time series forecasting, backtesting
- **[qa-testing-strategy](../qa-testing-strategy/SKILL.md)** - Test-driven development, coverage
- **[data-sql-optimization](../data-sql-optimization/SKILL.md)** - SQL optimization, index patterns (complements SQLMesh)
- **[data-lake-platform](../data-lake-platform/SKILL.md)** - Data lake/lakehouse infrastructure (ClickHouse, Iceberg, Kafka)

---

## Decision Tree: Choosing Data Science Approach

```text
User needs ML for: [Problem Type]
  - Tabular data?
    - Small-medium (<1M rows)? -> LightGBM (fast, efficient)
    - Large and complex (>1M rows)? -> LightGBM first, then NN if needed
    - High-dim sparse (text, counts)? -> Linear models, then shallow NN

  - Time series?
    - Seasonality? -> LightGBM, then see ai-ml-timeseries
    - Long-term dependencies? -> Transformers (see ai-ml-timeseries)

  - Text or mixed modalities?
    - LLMs/Transformers -> See ai-llm

  - SQL transformations?
    - SQLMesh (staging/intermediate/marts layers)
```

**Rule of thumb:** For tabular data, tree-based gradient boosting is a strong baseline, but must be validated against alternatives and constraints.

---

## Core Concepts (Vendor-Agnostic)

- **Problem framing**: define success metrics, baselines, and decision thresholds before modeling.
- **Leakage prevention**: ensure all features are available at prediction time; split by time/group when appropriate.
- **Uncertainty**: report confidence intervals and stability (fold variance, bootstrap) rather than single-point metrics.
- **Reproducibility**: version code/data/features, fix seeds, and record the environment.
- **Operational handoff**: define monitoring, retraining triggers, and rollback criteria with MLOps.

## Implementation Practices (Tooling Examples)

- Track experiments and artifacts (run id, commit hash, data version).
- Add data validation gates in pipelines (schema + distribution + freshness).
- Prefer reproducible, testable feature code (shared transforms, point-in-time correctness).
- Use datasheets/model cards and eval reports as deployment prerequisites (Datasheets for Datasets: https://arxiv.org/abs/1803.09010; Model Cards: https://arxiv.org/abs/1810.03993).

## Do / Avoid

**Do**
- Do start with baselines and a simple model to expose leakage and data issues early.
- Do run slice analysis and document failure modes before recommending deployment.
- Do keep an immutable eval set; refresh training data without contaminating evaluation.

**Avoid**
- Avoid random splits for temporal or user-correlated data.
- Avoid "metric gaming" (optimizing the number without validating business impact).
- Avoid training on labels created after the prediction timestamp (silent future leakage).

# Core Patterns (Overview)

## Pattern 1: End-to-End DS Project Lifecycle

**Use when:** Starting or restructuring any DS/ML project.

**Stages:**

1. **Problem framing** - Business objective, success metrics, baseline
2. **Data & feasibility** - Sources, coverage, granularity, label quality
3. **EDA & data quality** - Schema, missingness, outliers, leakage checks
4. **Feature engineering** - Per data type with feature store integration
5. **Modelling** - Baselines first, then LightGBM, then complexity as needed
6. **Evaluation** - Offline metrics, slice analysis, error analysis
7. **Reporting** - Model evaluation report + model card
8. **MLOps** - CI/CD, CT (continuous training), CM (continuous monitoring)

**Detailed guide:** [EDA Best Practices](references/eda-best-practices.md)

---

## Pattern 2: Feature Engineering

**Use when:** Designing features before modelling or during model improvement.

**By data type:**

- **Numeric:** Standardize, handle outliers, transform skew, scale
- **Categorical:** One-hot/ordinal (low cardinality), target/frequency/hashing (high cardinality)
  - **Feature Store Integration:** Store encoders, mappings, statistics centrally
- **Text:** Cleaning, TF-IDF, embeddings, simple stats
- **Time:** Calendar features, recency, rolling/lag features

**Key Modern Practice:** Use feature stores (Feast, Tecton, Databricks) for versioning, sharing, and train-serve parity.

**Detailed guide:** [Feature Engineering Patterns](references/feature-engineering-patterns.md)

---

## Pattern 3: Data Contracts & Lineage

**Use when:** Building production ML systems with data quality requirements.

**Components:**

- **Contracts:** Schema + ranges/nullability + freshness SLAs
- **Lineage:** Track source -> feature store -> train -> serve
- **Feature store hygiene:** Materialization cadence, backfill/replay, encoder versioning
- **Schema evolution:** Backward/forward-compatible migrations with shadow runs

**Detailed guide:** [Data Contracts & Lineage](references/data-contracts-lineage.md)

---

## Pattern 4: Model Selection & Training

**Use when:** Picking model families and starting experiments.

**Decision guide (modern benchmarks):**

- **Tabular:** Start with a **strong baseline** (linear/logistic, then gradient boosting) and iterate based on error analysis
- **Baselines:** Always implement simple baselines first (majority class, mean, naive forecast)
- **Train/val/test splits:** Time-based (forecasting), group-based (user/item leakage), or random (IID)
- **Hyperparameter tuning:** Start manual, then Bayesian optimization (Optuna, Ray Tune)
- **Overfitting control:** Regularization, early stopping, cross-validation

**Detailed guide:** [Modelling Patterns](references/modelling-patterns.md)

---

## Pattern 5: Evaluation & Reporting

**Use when:** Finalizing a model candidate or handing over to production.

**Key components:**

- **Metric selection:** Primary (ROC-AUC, PR-AUC, RMSE) + guardrails (calibration, fairness)
- **Threshold selection:** ROC/PR curves, cost-sensitive, F1 maximization
- **Slice analysis:** Performance by geography, user segments, product categories
- **Error analysis:** Collect high-error examples, cluster by error type, identify systematic failures
- **Uncertainty:** Confidence intervals (bootstrap where appropriate), variance across folds, and stability checks
- **Evaluation report:** 8-section report (objective, data, features, models, metrics, slices, risks, recommendation)
- **Model card:** Documentation for stakeholders (intended use, data, performance, ethics, operations)

**Detailed guide:** [Evaluation Patterns](references/evaluation-patterns.md)

---

## Pattern 6: Reproducibility & MLOps

**Use when:** Ensuring experiments are reproducible and production-ready.

**Modern MLOps (CI/CD/CT/CM):**

- **CI (Continuous Integration):** Automated testing, data validation, code quality
- **CD (Continuous Delivery):** Environment-specific promotion (dev -> staging -> prod), canary deployment
- **CT (Continuous Training):** Drift-triggered and scheduled retraining
- **CM (Continuous Monitoring):** Real-time data drift, performance, system health

**Versioning:**
- Code (git commit), data (DVC, LakeFS), features (feature store), models (MLflow Registry)
- Seeds (reproducibility), hyperparameters (experiment tracker)

**Detailed guide:** [Reproducibility Checklist](references/reproducibility-checklist.md)

---

## Pattern 7: Feature Freshness & Streaming

**Use when:** Managing real-time features and streaming pipelines.

**Components:**

- **Freshness contracts:** Define freshness SLAs per feature, monitor lag, alert on breaches
- **Batch + stream parity:** Same feature logic across batch/stream, idempotent upserts
- **Schema evolution:** Version schemas, add forward/backward-compatible parsers, backfill with rollback
- **Data quality gates:** PII/format checks, range checks, distribution drift (KL, KS, PSI)

**Detailed guide:** [Feature Freshness & Streaming](references/feature-freshness-streaming.md)

---

## Pattern 8: Production Feedback Loops

**Use when:** Capturing production signals and implementing continuous improvement.

**Components:**

- **Signal capture:** Log predictions + user edits/acceptance/abandonment (scrub PII)
- **Labeling:** Route failures/edge cases to human review, create balanced sets
- **Dataset refresh:** Periodic refresh (weekly/monthly) with lineage, protect eval set
- **Online eval:** Shadow/canary new models, track solve rate, calibration, cost, latency

**Detailed guide:** [Production Feedback Loops](references/production-feedback-loops.md)

---

## Resources (Detailed Guides)

For comprehensive operational patterns and checklists, see:

- [EDA Best Practices](references/eda-best-practices.md) - Structured workflow for exploratory data analysis
- [Feature Engineering Patterns](references/feature-engineering-patterns.md) - Operational patterns by data type
- [Data Contracts & Lineage](references/data-contracts-lineage.md) - Data quality, versioning, feature store ops
- [Modelling Patterns](references/modelling-patterns.md) - Model selection, hyperparameter tuning, train/test splits
- [Evaluation Patterns](references/evaluation-patterns.md) - Metrics, slice analysis, evaluation reports, model cards
- [Reproducibility Checklist](references/reproducibility-checklist.md) - Experiment tracking, MLOps (CI/CD/CT/CM)
- [Feature Freshness & Streaming](references/feature-freshness-streaming.md) - Real-time features, schema evolution
- [Production Feedback Loops](references/production-feedback-loops.md) - Online learning, labeling, canary deployment

---

## Templates

Use these as copy-paste starting points:

### Project & Workflow Templates

- **Standard DS project template:** `assets/project/template-standard.md`
- **Quick DS experiment template:** `assets/project/template-quick.md`

### Feature Engineering & EDA

- **Feature engineering template:** `assets/features/template-feature-engineering.md`
- **EDA checklist & notebook template:** `assets/eda/template-eda.md`

### Evaluation & Reporting

- **Model evaluation report:** `assets/evaluation/template-evaluation-report.md`
- **Model card:** `assets/evaluation/template-model-card.md`
- **ML experiment review:** `assets/review/experiment-review-template.md`

### SQL Transformation (SQLMesh)

For SQL-based data transformation and feature engineering:

- **SQLMesh project setup:** `../data-lake-platform/assets/transformation/sqlmesh/template-sqlmesh-project.md`
- **SQLMesh model types:** `../data-lake-platform/assets/transformation/sqlmesh/template-sqlmesh-model.md` (FULL, INCREMENTAL, VIEW)
- **Incremental models:** `../data-lake-platform/assets/transformation/sqlmesh/template-sqlmesh-incremental.md`
- **DAG and dependencies:** `../data-lake-platform/assets/transformation/sqlmesh/template-sqlmesh-dag.md`
- **Testing and data quality:** `../data-lake-platform/assets/transformation/sqlmesh/template-sqlmesh-testing.md`

**Use SQLMesh when:**
- Building SQL-based feature pipelines
- Managing incremental data transformations
- Creating staging/intermediate/marts layers
- Testing SQL logic with unit tests and audits

**For data ingestion (loading raw data), use:**
- [ai-mlops](../ai-mlops/SKILL.md) skill (dlt templates for REST APIs, databases, warehouses)

## Navigation

**Resources**
- [references/reproducibility-checklist.md](references/reproducibility-checklist.md)
- [references/evaluation-patterns.md](references/evaluation-patterns.md)
- [references/feature-engineering-patterns.md](references/feature-engineering-patterns.md)
- [references/modelling-patterns.md](references/modelling-patterns.md)
- [references/feature-freshness-streaming.md](references/feature-freshness-streaming.md)
- [references/eda-best-practices.md](references/eda-best-practices.md)
- [references/data-contracts-lineage.md](references/data-contracts-lineage.md)
- [references/production-feedback-loops.md](references/production-feedback-loops.md)

**Templates**
- [assets/project/template-standard.md](assets/project/template-standard.md)
- [assets/project/template-quick.md](assets/project/template-quick.md)
- [assets/features/template-feature-engineering.md](assets/features/template-feature-engineering.md)
- [assets/eda/template-eda.md](assets/eda/template-eda.md)
- [assets/evaluation/template-evaluation-report.md](assets/evaluation/template-evaluation-report.md)
- [assets/evaluation/template-model-card.md](assets/evaluation/template-model-card.md)
- [assets/review/experiment-review-template.md](assets/review/experiment-review-template.md)
- [template-sqlmesh-project.md](../data-lake-platform/assets/transformation/sqlmesh/template-sqlmesh-project.md)
- [template-sqlmesh-model.md](../data-lake-platform/assets/transformation/sqlmesh/template-sqlmesh-model.md)
- [template-sqlmesh-incremental.md](../data-lake-platform/assets/transformation/sqlmesh/template-sqlmesh-incremental.md)
- [template-sqlmesh-dag.md](../data-lake-platform/assets/transformation/sqlmesh/template-sqlmesh-dag.md)
- [template-sqlmesh-testing.md](../data-lake-platform/assets/transformation/sqlmesh/template-sqlmesh-testing.md)

**Data**
- [data/sources.json](data/sources.json) - Curated external references

---

## External Resources

See [data/sources.json](data/sources.json) for curated foundational and implementation references:

- **Core ML/DL**: scikit-learn, XGBoost, LightGBM, PyTorch, TensorFlow, JAX
- **Data processing**: pandas, NumPy, Polars, DuckDB, Spark, Dask
- **SQL transformation**: SQLMesh, dbt (staging/marts/incremental patterns)
- **Feature stores**: Feast, Tecton, Databricks Feature Store (centralized feature management)
- **Data validation**: Pydantic, Great Expectations, Pandera, Evidently (quality + drift)
- **Visualization**: Matplotlib, Seaborn, Plotly, Streamlit, Dash
- **MLOps**: MLflow, W&B, DVC, Neptune (experiment tracking + model registry)
- **Hyperparameter tuning**: Optuna, Ray Tune, Hyperopt
- **Model serving**: BentoML, FastAPI, TorchServe, Seldon, Ray Serve
- **Orchestration**: Kubeflow, Metaflow, Prefect, Airflow, ZenML
- **Cloud platforms**: AWS SageMaker, Google Vertex AI, Azure ML, Databricks, Snowflake

Use this skill to **execute data science projects end-to-end**: concrete checklists, patterns, and templates, not theory.
