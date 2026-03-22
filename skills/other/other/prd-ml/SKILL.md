---
name: prd-ml
description: "Generate a Product Requirements Document (PRD) for a data science, machine learning, or MLOps feature/project. Use when planning an ML experiment, model deployment, data pipeline, or MLOps process. Triggers on: create a prd for ml, write prd for model, plan this ml feature, spec out pipeline, mlops prd."
---

# ML/DS/MLOps PRD Generator

Create detailed Product Requirements Documents for data science, machine learning, and MLOps initiatives. Covers the full lifecycle: data acquisition, experimentation, model development, evaluation, deployment, and monitoring.

---

## The Job

1. Receive a feature/project description from the user
2. Identify whether this is primarily a **DS experiment**, **ML model**, **data pipeline**, or **MLOps infrastructure** task
3. Ask 4-6 essential clarifying questions (with lettered options)
4. Generate a structured PRD based on answers
5. Save to `docs/tasks/prd-[feature-name].md`

**Important:** Do NOT start implementing. Just create the PRD.

---

## Step 1: Identify Project Type

Before asking questions, classify the request into one or more of:

- **Experiment/Research**: Exploratory analysis, hypothesis testing, prototyping
- **Model Development**: Building, training, and evaluating a supervised/unsupervised model
- **Data Pipeline**: ETL/ELT, feature engineering, data quality
- **MLOps/Deployment**: Serving, monitoring, CI/CD for models, retraining pipelines
- **Evaluation Framework**: Metrics, ground truth, benchmarking

This determines which clarifying questions to ask.

---

## Step 2: Clarifying Questions

Ask only critical questions where the initial prompt is ambiguous. Adjust per project type.

### Universal Questions

```
1. What is the primary objective?
   A. Validate a hypothesis / explore feasibility
   B. Build a model for production use
   C. Improve an existing model or pipeline
   D. Create infrastructure for future ML work

2. Who consumes the output?
   A. Downstream ML model (training dataset / features)
   B. Internal analysts or data scientists
   C. End users via a product/API
   D. Automated systems / other pipelines
```

### Experiment / Research Questions

```
3. What is the success criterion for this experiment?
   A. Quantitative metric threshold (e.g., F1 > 0.85)
   B. Directional improvement over baseline
   C. Feasibility assessment (yes/no answer)
   D. Exploratory — no strict criteria yet

4. What is the expected output?
   A. Notebook + findings report
   B. Trained model artifact
   C. Labeled / processed dataset
   D. Decision recommendation document
```

### Model Development Questions

```
3. What type of task is this?
   A. Binary / multi-class classification
   B. Regression
   C. Sequence labeling / NLP
   D. Ranking, clustering, or other

4. What is the evaluation strategy?
   A. Hold-out test set
   B. Cross-validation
   C. Temporal split (time-series)
   D. Human evaluation / annotation

5. Is ground truth / labeled data available?
   A. Yes, fully labeled
   B. Partially labeled — active learning or weak supervision needed
   C. No labels — must be created (annotation task)
   D. Proxy labels from production signals
```

### Data Pipeline Questions

```
3. What is the data source?
   A. Internal database / data warehouse
   B. External API or third-party feed
   C. Raw files (CSV, Parquet, logs)
   D. Real-time stream

4. What is the expected data volume and freshness?
   A. Batch, daily or less frequent
   B. Batch, hourly
   C. Near real-time (minutes)
   D. Real-time streaming
```

### MLOps / Deployment Questions

```
3. What is the serving pattern?
   A. Batch scoring (scheduled job)
   B. Online inference (REST API / gRPC)
   C. Embedded in application logic
   D. Edge / device deployment

4. What are the latency / throughput requirements?
   A. Offline — no latency constraint
   B. Soft real-time (< 1 second)
   C. Hard real-time (< 100 ms)
   D. Unknown / TBD

5. What monitoring is needed?
   A. Data drift only
   B. Model performance / concept drift
   C. Full observability (data + model + infrastructure)
   D. Not required initially
```

Format responses with lettered options. Let users respond with "1A, 2C, 3B" for quick iteration.

---

## Step 3: PRD Structure

Generate the PRD with the sections below. Omit sections that are clearly not applicable, but keep most of them.

### 1. Introduction / Overview

Brief description of the project, the problem it solves, and its place in the broader ML system or product.

### 2. Goals

Specific, measurable objectives. For ML projects this means:
- Quantitative metric targets (precision, recall, F1, RMSE, etc.)
- Business KPIs impacted
- Dataset size / coverage targets
- Latency / throughput requirements (if deployment)

### 3. Background & Context

- Why does this exist? What does a manual or rule-based approach look like today?
- Prior work or related experiments
- Relevant constraints (regulatory, privacy, latency)

### 4. Data Requirements

- **Sources**: Where does the data come from?
- **Schema**: Key fields, types, expected distributions
- **Volume**: Row counts, time range, expected growth
- **Quality**: Known issues, missing values, label noise
- **Splits**: Train / validation / test strategy (temporal, stratified, etc.)
- **Ground Truth**: How labels are defined and obtained
- **PII / Compliance**: Any data sensitivity constraints

### 5. Model / Algorithm Requirements (if applicable)

- Task type and output format
- Baseline to beat (rule-based, heuristic, or prior model)
- Model family considerations (interpretability, latency, size constraints)
- Feature engineering expectations
- Known hard cases or edge cases to handle

### 6. Evaluation Framework

For each metric:
- **Name**: e.g., Macro F1, Precision@K, RMSE
- **Threshold**: What constitutes "good enough"?
- **Slice Analysis**: Any subgroups that need separate evaluation (e.g., by category, time period, data source)
- **Human Evaluation**: If automated metrics are insufficient

```markdown
| Metric        | Threshold | Priority |
|---------------|-----------|----------|
| Macro F1      | ≥ 0.80    | Must-have |
| Precision     | ≥ 0.85    | Must-have |
| Recall        | ≥ 0.75    | Nice-to-have |
| Latency P99   | ≤ 200 ms  | Must-have (if serving) |
```

### 7. User Stories

Scope stories to the ML lifecycle stages relevant to this project. Each story must be implementable independently.

**Lifecycle stages to consider:**
- Data acquisition / query
- Data validation / quality checks
- Feature engineering
- Model training / experimentation
- Evaluation & analysis
- Artifact packaging
- Deployment / serving
- Monitoring & alerting
- Retraining triggers

**Format:**
```markdown
### US-001: [Title]
**Description:** As a [data scientist / ML engineer / analyst], I want [action] so that [outcome].

**Acceptance Criteria:**
- [ ] Specific verifiable criterion
- [ ] Metric threshold met on validation set
- [ ] Reproducible: running the same script twice gives same result (fixed seeds)
- [ ] Artifacts saved to expected location
- [ ] Tests pass / lint passes
```

**Important acceptance criteria to consider for ML stories:**
- Reproducibility (fixed seeds, versioned data)
- Artifact versioning (model saved with metadata: date, dataset version, metrics)
- Schema validation on inputs/outputs
- Performance regression check vs. baseline
- No data leakage verified

### 8. Functional Requirements

Numbered, unambiguous list:

- `FR-1`: The pipeline must accept a date range parameter and query data from [source]
- `FR-2`: Features must be computed without look-ahead (no future data leakage)
- `FR-3`: Model artifacts must be saved with metadata (timestamp, dataset hash, evaluation metrics)
- `FR-4`: Evaluation report must include per-class metrics and confusion matrix
- `FR-5`: The serving endpoint must return predictions within 200 ms at P99

### 9. Non-Goals (Out of Scope)

What this will NOT include. Critical for managing scope.

Examples:
- No real-time retraining in this iteration
- No A/B testing infrastructure
- No explainability / SHAP values in v1
- No multi-language support

### 10. Technical Considerations

- **Stack**: Python version, key libraries (scikit-learn, PyTorch, Polars, etc.)
- **Infrastructure**: Where does training run? (local, EC2, managed service)
- **Experiment Tracking**: MLflow, [trackio](https://github.com/gradio-app/trackio), or other
- **Artifact Storage**: Local path, S3, model registry
- **Orchestration**: How is the pipeline triggered? (cron, Airflow, manual)
- **Dependencies**: Upstream data dependencies, downstream consumers
- **Reproducibility**: Random seed strategy, data versioning approach

### 11. MLOps Considerations (if deploying)

- **Serving pattern**: Batch vs. online
- **Model versioning & rollback**: How to roll back a bad model
- **Drift detection**: Data drift, concept drift, label drift
- **Retraining trigger**: Schedule, performance degradation, data volume threshold
- **Observability**: Logs, metrics, alerts

### 12. Experiment Tracking Plan (if research/experimentation)

- What parameters will be tracked? (hyperparameters, data versions, feature sets)
- What artifacts will be logged? (model, metrics, plots, confusion matrix)
- Naming convention for experiment runs
- Comparison strategy (how will runs be ranked/compared?)

### 13. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Insufficient labeled data | Medium | High | Start with weak supervision / rules |
| Data leakage in features | Low | High | Temporal split + leakage unit tests |
| Model underperforms on rare classes | High | Medium | Oversample / focal loss |
| Latency SLA not met | Low | High | Profile early, consider lighter model |

### 14. Success Metrics

How will success be measured at project completion?

- Quantitative: metric thresholds on held-out test set
- Operational: pipeline runs without manual intervention for N days
- Business: KPI movement (if measurable)

### 15. Open Questions

Remaining unknowns that need resolution before or during implementation.

---

## Writing for Implementers

The PRD reader may be a junior data scientist, ML engineer, or AI agent. Therefore:

- Be explicit about train/val/test splits and how to construct them
- Specify what "a trained model artifact" means (file format, metadata, location)
- Clarify whether features must be recomputed at inference or can be precomputed
- Number all requirements for easy reference
- Include concrete metric thresholds, not vague goals like "improve accuracy"

---

## Output

- **Format:** Markdown (`.md`)
- **Location:** `docs/tasks/`
- **Filename:** `prd-[feature-name].md` (kebab-case)

---

## Example PRD (Excerpt)

```markdown
# PRD: Automated Clinical Note Tagging Model

## Introduction

Train a multi-label classification model to tag clinical notes across 49 categories
(falls, elopement, medication errors, CiC indicators). This model will replace the
current regex-only system, using the regex-generated labels as ground truth training data.

## Goals

- Achieve Macro F1 ≥ 0.80 across all 49 tags on held-out test set
- Reduce false positive rate vs. regex baseline by ≥ 20%
- Serve predictions in < 200 ms P99 for online inference
- Fully reproducible training pipeline (fixed seeds, versioned dataset)

## Data Requirements

- **Source**: Regex-tagged dataset generated by current pipeline
- **Volume**: ~500K clinical notes, 2023–2025
- **Labels**: Multi-label binary matrix (49 columns)
- **Split**: Temporal — train on 2023–2024, validate on Q1 2025, test on Q2 2025
- **Label noise**: Expected ~5% noise from regex false positives; document impact
- **PII**: Notes contain PHI — no data leaves secure environment

## Evaluation Framework

| Metric        | Threshold | Priority   |
|---------------|-----------|------------|
| Macro F1      | ≥ 0.80    | Must-have  |
| Micro F1      | ≥ 0.85    | Must-have  |
| Precision     | ≥ 0.82    | Must-have  |
| Recall        | ≥ 0.78    | Must-have  |
| Latency P99   | ≤ 200 ms  | Must-have  |

Per-tag breakdown required. Tags with < 100 training examples flagged separately.

## User Stories

### US-001: Build training dataset from regex labels
**Description:** As a data scientist, I want to export the regex-tagged dataset as a
versioned parquet file so that training is reproducible.

**Acceptance Criteria:**
- [ ] Script outputs `data/train.parquet`, `data/val.parquet`, `data/test.parquet`
- [ ] Each file includes `note_id`, `text`, and 49 binary label columns
- [ ] Split is temporal: train ≤ 2024-12-31, val = Q1 2025, test = Q2 2025
- [ ] Dataset metadata saved: row counts, label prevalence per split, dataset hash
- [ ] No notes appear in more than one split
- [ ] Tests pass

### US-002: Train baseline model
**Description:** As a data scientist, I want a TF-IDF + logistic regression baseline
so that I have a reference point for deep learning models.

**Acceptance Criteria:**
- [ ] Baseline trained and evaluated on val set
- [ ] Per-tag F1, precision, recall logged to MLflow
- [ ] Model artifact saved with metadata (dataset version, val metrics, timestamp)
- [ ] Macro F1 ≥ 0.65 on val set (sanity check)
- [ ] Reproducible with fixed random seed

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Label noise from regex FPs | High | Medium | Analyze noise rate; consider confidence weighting |
| Class imbalance (rare tags) | High | High | Oversample rare classes; use weighted loss |
| Data leakage | Low | High | Enforce temporal split; add leakage unit test |
```

---

## Checklist

Before saving the PRD:

- [ ] Asked clarifying questions with lettered options
- [ ] Identified project type (experiment / model / pipeline / MLOps)
- [ ] Incorporated user's answers
- [ ] Data requirements section is concrete (source, volume, split strategy)
- [ ] Evaluation framework has numeric thresholds
- [ ] User stories cover relevant lifecycle stages
- [ ] Reproducibility requirements are explicit
- [ ] Risks table populated
- [ ] Non-goals section defines clear boundaries
- [ ] Saved to `docs/tasks/prd-[feature-name].md`
