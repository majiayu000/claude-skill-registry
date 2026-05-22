---
name: ml-pipeline
description: ML pipeline orchestrator — single entry point for ML-related tasks. Coordinates ML Engineer (analysis, modeling, recommendations), SRE Engineer (production data extraction), and Product Manager (task formulation). Domain context from CLAUDE.md. MVP flow: define data requirements → extract from prod → analyze → model → recommend → feature plan.
context: fork
argument-hint: [analysis goal or dataset description]
---

# ML Pipeline

Single entry point for ML-related tasks. Orchestrates three roles across a data-driven analysis pipeline: **Product Manager** formulates the task, **ML Engineer** owns analysis and modeling, **SRE Engineer** extracts production data. Domain specifics are read from the project's `CLAUDE.md`.

**Architecture note**: This workflow is extensible — future sub-flows (model training, prompt tuning, A/B testing) can be added as numbered branches in Step 2.

## 1. Receive ML Task

Gather the ML task from the user:

- **Objective**: What do you want to learn or improve? (e.g., "tune scoring weights", "improve data collection prompts", "analyze conversion funnel")
- **Data source**: Where is the data? (production database, logs, external API, local files)
- **Expected output**: What decisions will the analysis inform?
- **Constraints**: Timeline, data sensitivity, compute budget

If the user provides a vague request — proceed to Step 2 where `Agent(product-manager)` will help formulate it.

## 2. Determine Pipeline Type

Select the pipeline based on the ML task:

| Pipeline Type | When to Use | Status |
|---|---|---|
| **Data Analysis** | Extract prod data → analyze → model → recommend parameter/prompt changes | ✅ Active |
| **Model Training** | Train or retrain ML models on collected data | 🔮 Future |
| **Prompt Tuning** | Optimize LLM prompts based on output quality analysis | 🔮 Future |
| **A/B Test Analysis** | Analyze results of live experiments | 🔮 Future |

For MVP, proceed with **Data Analysis** pipeline (Steps 3–9). Future pipeline types will be added as parallel branches from this step.

## 3. Read Project Context

**Apply `Agent(product-manager)`.**

Read and internalize the project's domain:

1. **`CLAUDE.md`** (root) — tech stack, domain description, business context
2. **`ARCHITECTURE.md`** — system components, data flow, service boundaries
3. **`FEATURES.md`** (if exists) — current feature inventory, scoring/evaluation parameters

**Extract and summarize**:
- **Domain**: What does the product do? What data does it collect?
- **Evaluation parameters**: What metrics/weights/scores does the product use?
- **Data sources**: Where is production data stored? (database, logs, analytics)
- **Current prompts**: If the product uses LLM prompts for data collection — identify prompt locations and purpose

Present the domain summary to the user for confirmation before proceeding.

## 4. Formulate ML Task

**Continue with `Agent(product-manager)`.**

Transform the user's request into a structured ML task specification:

```
## ML Task Specification

### Objective
[What we want to learn or improve — measurable outcome]

### Business Context
[Why this matters — which product decisions depend on this analysis]

### Success Criteria
[How we know the analysis is complete and actionable]
- [ ] Data requirements defined and extracted
- [ ] Statistical analysis performed with confidence intervals
- [ ] Recommendations backed by evidence (not intuition)
- [ ] Action plan produced (parameter changes, prompt modifications, or feature work)

### Scope
- **In scope**: [specific parameters, data ranges, user segments]
- **Out of scope**: [what we explicitly skip]

### Constraints
- Data sensitivity: [PII handling, anonymization needs]
- Time range: [how far back to analyze]
- Compute budget: [any limits on processing]
```

Present to user for approval. Adjust based on feedback.

## 5. Define Data Requirements

**Apply `Agent(ml-engineer)`.**

Based on the ML task specification from Step 4, define exactly what data is needed:

<data_requirements>
- **Data points**: Which fields/columns/metrics are needed?
- **Granularity**: Per-record, aggregated, time-series?
- **Time range**: From when to when?
- **Filters**: Which segments, categories, statuses?
- **Volume estimate**: Expected row count / data size
- **Format**: CSV, JSON, Parquet, database query result?
- **Joins**: Which tables/sources need to be combined?
- **Anonymization**: Which fields contain PII and how to handle?
</data_requirements>

Produce a concrete **data extraction plan** — either SQL queries, API calls, or log extraction commands that `Agent(sre-engineer)` can execute.

Present the data requirements and extraction plan to the user for review.

## 6. Extract Production Data

**Apply `Agent(sre-engineer)`.**

Execute the data extraction plan from Step 5. This step uses SRE's production access and operational expertise.

**⚠️ SAFETY: All commands are READ-ONLY. No mutations to production data or systems.**

### 6a. Establish Production Access

Follow `/analyze-prod` Steps 3a–3b to verify cloud platform context. Consult `cloud-platforms` skill for platform-specific CLI commands.

### 6b. Execute Data Extraction

Based on the extraction plan:

| Data Source | Method |
|---|---|
| **Managed DB (SQL)** | Platform-specific connection (see `cloud-platforms` skill CLI Reference → Data Extraction) + `psql`/`mysql` query |
| **Application logs** | Platform-specific log query (see `cloud-platforms` skill Observability → Diagnostic Commands) |
| **Monitoring metrics** | Platform-specific metrics API (see `cloud-platforms` skill Observability) |
| **Data warehouse** | Platform-specific query tool (BigQuery / Synapse / Athena) |
| **Object storage** | Platform-specific CLI (gsutil / az storage / aws s3) |
| **Kubernetes pod data** | `kubectl logs` or `kubectl exec` (read-only) |

For each extraction:
1. Show the exact command/query to the user before execution
2. Execute after approval
3. Save results to a local working directory (e.g., `data/raw/`)
4. Verify data completeness — row counts, date ranges, null percentages

### 6c. Data Handoff

Present extraction summary:

```
## Data Extraction Summary
- Source: [database/logs/metrics]
- Records extracted: [count]
- Time range: [from — to]
- Files: [local paths]
- Data quality notes: [nulls, anomalies, gaps]
```

## 7. Analyze Data and Build Models

**Apply `Agent(ml-engineer)`.**

Perform the analysis following ML Engineer's reasoning protocol:

### 7a. Exploratory Data Analysis (EDA)

- Profile the extracted data: distributions, correlations, outliers, missing values
- Visualize key patterns (histograms, scatter plots, time series, heatmaps)
- Identify data quality issues that could affect analysis
- Document findings and assumptions

### 7b. Statistical Analysis

- Hypothesis testing for differences between segments/groups
- Correlation analysis between parameters and outcomes
- Time-series analysis for trends and seasonality (if applicable)
- Confidence intervals for all key metrics — never report point estimates without uncertainty

### 7c. Modeling (if applicable)

- Establish a baseline (current parameter weights, simple heuristic, or mean prediction)
- Train models to identify optimal parameters: regression, classification, or optimization
- Evaluate against baseline with appropriate metrics
- Feature importance analysis — which parameters matter most?
- Cross-validation for robust estimates

### 7d. Document Results

Present analysis as a structured report:

```
## Analysis Report

### Data Summary
- Records analyzed: [count]
- Time period: [range]
- Segments: [if applicable]

### Key Findings
1. [Finding with statistical evidence]
2. [Finding with statistical evidence]
3. [Finding with statistical evidence]

### Visualizations
[Charts, plots, tables illustrating findings]

### Model Performance (if applicable)
- Baseline: [metric = value]
- Proposed: [metric = value]
- Improvement: [delta with confidence interval]
```

## 8. Produce Recommendations

**Continue with `Agent(ml-engineer)`, consult `Agent(product-manager)` for business framing.**

Translate analysis findings into actionable recommendations:

```
## ML Recommendations

### Summary
[One paragraph: what the analysis revealed and what should change]

### Recommended Changes

#### Parameter/Weight Changes
| Parameter | Current Value | Recommended Value | Expected Impact | Confidence |
|---|---|---|---|---|
| [param] | [current] | [recommended] | [metric improvement] | [high/medium/low] |

#### Prompt Modifications (if applicable)
| Prompt | Current Issue | Recommended Change | Expected Improvement |
|---|---|---|---|
| [prompt location] | [what's wrong] | [specific edit] | [quality metric] |

When recommendations include prompt or context pipeline changes (RAG, memory, agent harness, token budget), consult `context-engineering` skill for architecture patterns and production checklists.

#### Other Recommendations
- [Infrastructure, data pipeline, monitoring changes]

### Evidence
[Reference to analysis report, key metrics, statistical tests]

### Risks
| Risk | Mitigation |
|---|---|
| [what could go wrong] | [how to handle it] |

### Validation Plan
- [ ] A/B test for [specific changes] over [duration]
- [ ] Monitor [metrics] for regression
- [ ] Rollback criteria: [threshold]
```

Present recommendations to the user. Wait for approval before proceeding.

## 9. Generate Feature Plan

After user approves the recommendations, invoke `/feature-plan` with the following input:

**Feature specification** (auto-generated from Step 8):
- **Goal**: Implement ML-recommended changes to [parameters/prompts/models]
- **Requirements**: Each recommended change from Step 8 becomes a functional requirement
- **Acceptance criteria**: Metrics improve by the predicted amounts (with tolerance)
- **Constraints**: Include validation plan (A/B test, monitoring) as non-functional requirements

`/feature-plan` will decompose the work into role-scoped work packages and produce an implementation plan.

## 10. Summary

Present the completed ML pipeline run:

- **ML task**: original objective
- **Domain**: project context used
- **Roles applied**: `Agent(product-manager)`, `Agent(ml-engineer)`, `Agent(sre-engineer)`
- **Data**: source, volume, time range
- **Key findings**: top 3 insights
- **Recommendations**: summary of proposed changes
- **Feature plan**: link to generated plan or status
- **Next step**: `/feature-dev` per work package

## Integration

- **Sub-workflows**: `/analyze-prod` (production data access, Steps 6a–6b)
- **Followed by**: `/feature-plan` (Step 9), then `/feature-dev` (implementation)
- **Roles**: `Agent(product-manager)` (task formulation), `Agent(ml-engineer)` (analysis, modeling), `Agent(sre-engineer)` (data extraction)
- **Skills**: `testing-procedures` skill (validation plan), `context-engineering` skill (context pipeline design, RAG, memory engineering, agent harness — for LLM/prompt recommendations), `prompt-engineering` skill (technique selection, eval strategy)
