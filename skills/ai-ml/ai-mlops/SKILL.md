---
name: ai-mlops
description: Complete MLOps skill covering production ML lifecycle and security. Includes data ingestion, model deployment, drift detection, monitoring, plus ML security (prompt injection, jailbreak defense, RAG security, privacy, governance). Modern automation-first patterns with multi-layered defenses.
---

# MLOps & ML Security — Complete Reference

Production ML lifecycle with **modern security practices**.

This skill covers:

- **Production**: Data ingestion, deployment, drift detection, monitoring, incident response
- **Security**: Prompt injection, jailbreak defense, RAG security, output filtering
- **Governance**: Privacy protection, supply chain security, safety evaluation

1. **Data ingestion** (dlt): Load data from APIs, databases to warehouses
2. **Model deployment**: Batch jobs, real-time APIs, hybrid systems, event-driven automation
3. **Operations**: Real-time monitoring, drift detection, automated retraining, incident response

**Modern Best Practices (December 2025)**:

- Treat the model as a **versioned production artifact** with provenance, rollbacks, and audit logs (NIST SSDF: https://csrc.nist.gov/pubs/sp/800/218/final).
- Align governance and documentation to risk posture (EU AI Act: https://eur-lex.europa.eu/eli/reg/2024/1689/oj; NIST AI RMF: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf).
- Measure and manage drift with **clear triggers and playbooks**; “drift” is not one metric.
- Make incident response and change management first-class (runbooks, on-call, postmortems).

It is execution-focused:

- Data ingestion patterns (REST APIs, database replication, incremental loading)
- Deployment patterns (batch, online, hybrid, streaming, event-driven)
- **Automated monitoring** with real-time drift detection
- **Automated retraining** pipelines (monitor → detect → trigger → validate → deploy)
- Incident handling with validated rollback and postmortems
- Links to copy-paste templates in `templates/`

---

## Quick Reference

| Task | Tool/Framework | Command | When to Use |
|------|----------------|---------|-------------|
| Data Ingestion | dlt (data load tool) | `dlt pipeline run`, `dlt init` | Loading from APIs, databases to warehouses |
| Batch Deployment | Airflow, Dagster, Prefect | `airflow dags trigger`, `dagster job launch` | Scheduled predictions on large datasets |
| API Deployment | FastAPI, Flask, TorchServe | `uvicorn app:app`, `torchserve --start` | Real-time inference (<500ms latency) |
| Model Registry | MLflow, W&B | `mlflow.register_model()`, `wandb.log_model()` | Versioning and promoting models |
| Drift Detection | Statistical tests + monitors | PSI/KS, feature drift, prediction drift | Detect data/process changes and trigger review |
| Monitoring | Prometheus, Grafana | `prometheus.yml`, Grafana dashboards | Metrics, alerts, SLO tracking |
| Incident Response | Runbooks, PagerDuty | Documented playbooks, alert routing | Handling failures and degradation |

---

## When to Use This Skill

Claude should invoke this skill when the user asks for **deployment, operations, or data ingestion** help, e.g.:

- "How do I deploy this model to prod?"
- "Design a batch + online scoring architecture."
- "Add monitoring and drift detection to our model."
- "Write an incident runbook for this ML service."
- "Package this LLM/RAG pipeline as an API."
- "Plan our retraining and promotion workflow."
- "Load data from Stripe API to Snowflake."
- "Set up incremental database replication with dlt."
- "Build an ELT pipeline for warehouse loading."

If the user is asking only about **EDA, modelling, or theory**, prefer:

- `ai-ml-data-science` (EDA, features, modelling, SQL transformation with SQLMesh)
- `ai-llm` (prompting, fine-tuning, eval)
- `ai-rag` (retrieval pipeline design)
- `ai-llm-inference` (compression, spec decode, serving internals)

If the user is asking about **SQL transformation (after data is loaded)**, prefer:

- `ai-ml-data-science` (SQLMesh templates for staging, intermediate, marts layers)

---

## Decision Tree: Choosing Deployment Strategy

```text
User needs to deploy: [ML System]
    ├─ Data Ingestion?
    │   ├─ From REST APIs? → dlt REST API templates
    │   ├─ From databases? → dlt database sources (PostgreSQL, MySQL, MongoDB)
    │   └─ Incremental loading? → dlt incremental patterns (timestamp, ID-based)
    │
    ├─ Model Serving?
    │   ├─ Latency <500ms? → FastAPI real-time API
    │   ├─ Batch predictions? → Airflow/Dagster batch pipeline
    │   └─ Mix of both? → Hybrid (batch features + online scoring)
    │
    ├─ Monitoring & Ops?
    │   ├─ Drift detection? → Evidently + automated retraining triggers
    │   ├─ Performance tracking? → Prometheus + Grafana dashboards
    │   └─ Incident response? → Runbooks + PagerDuty alerts
    │
    └─ LLM/RAG Production?
        ├─ Cost optimization? → Caching, prompt templates, token budgets
        └─ Safety? → See ai-mlops skill
```

---

## Core Concepts (Vendor-Agnostic)

- **Lifecycle loop**: train → validate → deploy → monitor → respond → retrain/retire.
- **Risk controls**: access control, data minimization, logging, and change management (NIST AI RMF: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf).
- **Observability planes**: system metrics (latency/errors), data metrics (freshness/drift), quality metrics (model performance).
- **Incident readiness**: detection, containment, rollback, and root-cause analysis.

## Do / Avoid

**Do**
- Do gate deployments with repeatable checks: evaluation pass, load test, security review, rollback plan.
- Do version everything: code, data, features, model artifact, prompt templates, configuration.
- Do define SLOs and budgets (latency/cost/error rate) before optimizing.

**Avoid**
- Avoid manual “clickops” deployments without audit trail.
- Avoid silent upgrades; require eval + canary for model/prompt changes.
- Avoid drift dashboards without actions; every alert needs an owner and runbook.

## Core Patterns Overview

This skill provides 13 production-ready patterns organized into comprehensive guides:

### Data & Infrastructure Patterns

**Pattern 0: Data Contracts, Ingestion & Lineage**
→ See [Data Ingestion Patterns](resources/data-ingestion-patterns.md)

- Data contracts with SLAs and versioning
- Ingestion modes (CDC, batch, streaming)
- Lineage tracking and schema evolution
- Replay and backfill procedures

**Pattern 1: Choose Deployment Mode**
→ See [Deployment Patterns](resources/deployment-patterns.md)

- Decision table (batch, online, hybrid, streaming)
- When to use each mode
- Deployment mode selection checklist

**Pattern 2: Standard Deployment Lifecycle**
→ See [Deployment Lifecycle](resources/deployment-lifecycle.md)

- Pre-deploy, deploy, observe, operate, evolve phases
- Environment promotion (dev → staging → prod)
- Gradual rollout strategies (canary, blue-green)

**Pattern 3: Packaging & Model Registry**
→ See [Model Registry Patterns](resources/model-registry-patterns.md)

- Model registry structure and metadata
- Packaging strategies (Docker, ONNX, MLflow)
- Promotion flows (experimental → production)
- Versioning and governance

### Serving Patterns

**Pattern 4: Batch Scoring Pipeline**
→ See [Deployment Patterns](resources/deployment-patterns.md)

- Orchestration with Airflow/Dagster
- Idempotent scoring jobs
- Validation and backfill procedures

**Pattern 5: Real-Time API Scoring**
→ See [API Design Patterns](resources/api-design-patterns.md)

- Service design (HTTP/JSON, gRPC)
- Input/output schemas
- Rate limiting, timeouts, circuit breakers

**Pattern 6: Hybrid & Feature Store Integration**
→ See [Feature Store Patterns](resources/feature-store-patterns.md)

- Batch vs online features
- Feature store architecture
- Training-serving consistency
- Point-in-time correctness

### Operations Patterns

**Pattern 7: Monitoring & Alerting**
→ See [Monitoring Best Practices](resources/monitoring-best-practices.md)

- Data, performance, and technical metrics
- SLO definition and tracking
- Dashboard design and alerting strategies

**Pattern 8: Drift Detection & Automated Retraining**
→ See [Drift Detection Guide](resources/drift-detection-guide.md)

- Automated retraining triggers
- Event-driven retraining pipelines

**Pattern 9: Incidents & Runbooks**
→ See [Incident Response Playbooks](resources/incident-response-playbooks.md)

- Common failure modes
- Detection, diagnosis, resolution
- Post-mortem procedures

**Pattern 10: LLM / RAG in Production**
→ See [LLM & RAG Production Patterns](resources/llm-rag-production-patterns.md)

- Prompt and configuration management
- Safety and compliance (PII, jailbreaks)
- Cost optimization (token budgets, caching)
- Monitoring and fallbacks

**Pattern 11: Cross-Region, Residency & Rollback**
→ See [Multi-Region Patterns](resources/multi-region-patterns.md)

- Multi-region deployment architectures
- Data residency and tenant isolation
- Disaster recovery and failover
- Regional rollback procedures

**Pattern 12: Online Evaluation & Feedback Loops**
→ See [Online Evaluation Patterns](resources/online-evaluation-patterns.md)

- Feedback signal collection (implicit, explicit)
- Shadow and canary deployments
- A/B testing with statistical significance
- Human-in-the-loop labeling
- Automated retraining cadence

---

## Resources (Detailed Guides)

For comprehensive operational guides, see:

**Core Infrastructure:**

- **[Data Ingestion Patterns](resources/data-ingestion-patterns.md)** - Data contracts, CDC, batch/streaming ingestion, lineage, schema evolution
- **[Deployment Lifecycle](resources/deployment-lifecycle.md)** - Pre-deploy validation, environment promotion, gradual rollout, rollback
- **[Model Registry Patterns](resources/model-registry-patterns.md)** - Versioning, packaging, promotion workflows, governance
- **[Feature Store Patterns](resources/feature-store-patterns.md)** - Batch/online features, hybrid architectures, consistency, latency optimization

**Serving & APIs:**

- **[Deployment Patterns](resources/deployment-patterns.md)** - Batch, online, hybrid, streaming deployment strategies and architectures
- **[API Design Patterns](resources/api-design-patterns.md)** - ML/LLM/RAG API patterns, input/output schemas, reliability patterns, versioning

**Operations & Reliability:**

- **[Monitoring Best Practices](resources/monitoring-best-practices.md)** - Metrics collection, alerting strategies, SLO definition, dashboard design
- **[Drift Detection Guide](resources/drift-detection-guide.md)** - Statistical tests, automated detection, retraining triggers, recovery strategies
- **[Incident Response Playbooks](resources/incident-response-playbooks.md)** - Runbooks for common failure modes, diagnostics, resolution steps

**Advanced Patterns:**

- **[LLM & RAG Production Patterns](resources/llm-rag-production-patterns.md)** - Prompt management, safety, cost optimization, caching, monitoring
- **[Multi-Region Patterns](resources/multi-region-patterns.md)** - Multi-region deployment, data residency, disaster recovery, rollback
- **[Online Evaluation Patterns](resources/online-evaluation-patterns.md)** - A/B testing, shadow deployments, feedback loops, automated retraining

---

## Templates

Use these as copy-paste starting points for production artifacts:

### Data Ingestion (dlt)

For loading data into warehouses and pipelines:

- **[dlt basic pipeline setup](../data-lake-platform/templates/ingestion/dlt/template-dlt-pipeline.md)** - Install, configure, run basic extraction and loading
- **[dlt REST API sources](../data-lake-platform/templates/ingestion/dlt/template-dlt-rest-api.md)** - Extract from REST APIs with pagination, authentication, rate limiting
- **[dlt database sources](../data-lake-platform/templates/ingestion/dlt/template-dlt-database-source.md)** - Replicate from PostgreSQL, MySQL, MongoDB, SQL Server
- **[dlt incremental loading](../data-lake-platform/templates/ingestion/dlt/template-dlt-incremental.md)** - Timestamp-based, ID-based, merge/upsert patterns, lookback windows
- **[dlt warehouse loading](../data-lake-platform/templates/ingestion/dlt/template-dlt-warehouse-loading.md)** - Load to Snowflake, BigQuery, Redshift, Postgres, DuckDB

**Use dlt when:**

- Loading data from APIs (Stripe, HubSpot, Shopify, custom APIs)
- Replicating databases to warehouses
- Building ELT pipelines with incremental loading
- Managing data ingestion with Python

**For SQL transformation (after ingestion), use:**

→ `ai-ml-data-science` skill (SQLMesh templates for staging/intermediate/marts layers)

### Deployment & Packaging

- **[Deployment & MLOps template](templates/deployment/template-deployment-mlops.md)** - Complete MLOps lifecycle, model registry, promotion workflows
- **[Deployment readiness checklist](templates/deployment/deployment-readiness-checklist.md)** - Go/No-Go gate, monitoring, and rollback plan
- **[API service template](templates/deployment/template-api-service.md)** - Real-time REST/gRPC API with FastAPI, input validation, rate limiting
- **[Batch scoring pipeline template](templates/deployment/template-batch-pipeline.md)** - Orchestrated batch inference with Airflow/Dagster, validation, backfill

### Monitoring & Operations

- **[Monitoring & alerting template](templates/monitoring/template-monitoring-plan.md)** - Data/performance/technical metrics, dashboards, SLO definition
- **[Drift detection & retraining template](templates/monitoring/template-drift-retraining.md)** - Automated drift detection, retraining triggers, promotion pipelines
- **[Incident runbook template](templates/ops/template-incident-runbook.md)** - Failure mode playbooks, diagnosis steps, resolution procedures

## Navigation

**Resources**
- [resources/drift-detection-guide.md](resources/drift-detection-guide.md)
- [resources/model-registry-patterns.md](resources/model-registry-patterns.md)
- [resources/online-evaluation-patterns.md](resources/online-evaluation-patterns.md)
- [resources/monitoring-best-practices.md](resources/monitoring-best-practices.md)
- [resources/llm-rag-production-patterns.md](resources/llm-rag-production-patterns.md)
- [resources/api-design-patterns.md](resources/api-design-patterns.md)
- [resources/incident-response-playbooks.md](resources/incident-response-playbooks.md)
- [resources/deployment-patterns.md](resources/deployment-patterns.md)
- [resources/data-ingestion-patterns.md](resources/data-ingestion-patterns.md)
- [resources/deployment-lifecycle.md](resources/deployment-lifecycle.md)
- [resources/feature-store-patterns.md](resources/feature-store-patterns.md)
- [resources/multi-region-patterns.md](resources/multi-region-patterns.md)

**Templates**
- [template-dlt-pipeline.md](../data-lake-platform/templates/ingestion/dlt/template-dlt-pipeline.md)
- [template-dlt-rest-api.md](../data-lake-platform/templates/ingestion/dlt/template-dlt-rest-api.md)
- [template-dlt-database-source.md](../data-lake-platform/templates/ingestion/dlt/template-dlt-database-source.md)
- [template-dlt-incremental.md](../data-lake-platform/templates/ingestion/dlt/template-dlt-incremental.md)
- [template-dlt-warehouse-loading.md](../data-lake-platform/templates/ingestion/dlt/template-dlt-warehouse-loading.md)
- [templates/deployment/template-deployment-mlops.md](templates/deployment/template-deployment-mlops.md)
- [templates/deployment/deployment-readiness-checklist.md](templates/deployment/deployment-readiness-checklist.md)
- [templates/deployment/template-api-service.md](templates/deployment/template-api-service.md)
- [templates/deployment/template-batch-pipeline.md](templates/deployment/template-batch-pipeline.md)
- [templates/ops/template-incident-runbook.md](templates/ops/template-incident-runbook.md)
- [templates/monitoring/template-drift-retraining.md](templates/monitoring/template-drift-retraining.md)
- [templates/monitoring/template-monitoring-plan.md](templates/monitoring/template-monitoring-plan.md)

**Data**
- [data/sources.json](data/sources.json) — Curated external references

---

## External Resources

See `data/sources.json` for curated references on:

- Serving frameworks (FastAPI, Flask, gRPC, TorchServe, KServe, Ray Serve)
- Orchestration (Airflow, Dagster, Prefect)
- Model registries and MLOps (MLflow, W&B, Vertex AI, Sagemaker)
- Monitoring and observability (Prometheus, Grafana, OpenTelemetry, Evidently)
- Feature stores (Feast, Tecton, Vertex, Databricks)
- Streaming & messaging (Kafka, Pulsar, Kinesis)
- LLMOps & RAG infra (vector DBs, LLM gateways, safety tools)

---

## Data Lake & Lakehouse

For comprehensive data lake/lakehouse patterns (beyond dlt ingestion), see **[data-lake-platform](../data-lake-platform/SKILL.md)**:

- **Table formats:** Apache Iceberg, Delta Lake, Apache Hudi
- **Query engines:** ClickHouse, DuckDB, Apache Doris, StarRocks
- **Alternative ingestion:** Airbyte (GUI-based connectors)
- **Transformation:** dbt (alternative to SQLMesh)
- **Streaming:** Apache Kafka patterns
- **Orchestration:** Dagster, Airflow

This skill focuses on **ML-specific deployment, monitoring, and security**. Use data-lake-platform for general-purpose data infrastructure.

---

## Related Skills

For adjacent topics, reference these skills:

- **[ai-ml-data-science](../ai-ml-data-science/SKILL.md)** - EDA, feature engineering, modelling, evaluation, SQLMesh transformations
- **[ai-llm](../ai-llm/SKILL.md)** - Prompting, fine-tuning, evaluation for LLMs
- **[ai-agents](../ai-agents/SKILL.md)** - Agentic workflows, multi-agent systems, LLMOps
- **[ai-rag](../ai-rag/SKILL.md)** - RAG pipeline design, chunking, retrieval, evaluation
- **[ai-llm-inference](../ai-llm-inference/SKILL.md)** - Model serving optimization, quantization, batching
- **[ai-prompt-engineering](../ai-prompt-engineering/SKILL.md)** - Prompt design patterns and best practices
- **[data-lake-platform](../data-lake-platform/SKILL.md)** - Data lake/lakehouse infrastructure (ClickHouse, Iceberg, Kafka)

---

Use this skill to **turn trained models into reliable services**, not to derive the model itself.
