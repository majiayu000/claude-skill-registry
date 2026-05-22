---
name: ml-system-design
description: End-to-end ML system design for production. Use when designing ML pipelines, feature stores, model training infrastructure, or serving systems. Covers the complete lifecycle from data ingestion to model deployment and monitoring.
allowed-tools: Read, Glob, Grep
---

# ML System Design

This skill provides frameworks for designing production machine learning systems, from data pipelines to model serving.

## When to Use This Skill

**Keywords:** ML pipeline, machine learning system, feature store, model training, model serving, ML infrastructure, MLOps, A/B testing ML, feature engineering, model deployment

**Use this skill when:**

- Designing end-to-end ML systems for production
- Planning feature store architecture
- Designing model training pipelines
- Planning model serving infrastructure
- Preparing for ML system design interviews
- Evaluating ML platform tools and frameworks

## ML System Architecture Overview

### The ML System Lifecycle

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                        ML SYSTEM LIFECYCLE                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌────────┐ │
│  │  Data    │──▶│ Feature  │──▶│  Model   │──▶│  Model   │──▶│ Monitor│ │
│  │ Ingestion│   │ Pipeline │   │ Training │   │ Serving  │   │ & Eval │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   └────────┘ │
│       │              │              │              │              │      │
│       ▼              ▼              ▼              ▼              ▼      │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌────────┐ │
│  │  Data    │   │ Feature  │   │  Model   │   │ Inference│   │ Metrics│ │
│  │  Lake    │   │  Store   │   │ Registry │   │  Cache   │   │  Store │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   └────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Components

| Component | Purpose | Examples |
| --------- | ------- | -------- |
| **Data Ingestion** | Collect raw data from sources | Kafka, Kinesis, Pub/Sub |
| **Feature Pipeline** | Transform raw data to features | Spark, Flink, dbt |
| **Feature Store** | Store and serve features | Feast, Tecton, Vertex AI |
| **Model Training** | Train and validate models | SageMaker, Vertex AI, Kubeflow |
| **Model Registry** | Version and track models | MLflow, Weights & Biases |
| **Model Serving** | Serve predictions | TensorFlow Serving, Triton, vLLM |
| **Monitoring** | Track model performance | Evidently, WhyLabs, Arize |

## Feature Store Architecture

### Why Feature Stores?

**Problems without a feature store:**

- Training-serving skew (features computed differently)
- Duplicate feature computation across teams
- No feature versioning or lineage
- Slow feature experimentation

### Feature Store Components

```text
┌─────────────────────────────────────────────────────────────────┐
│                      FEATURE STORE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────┐       ┌─────────────────────┐          │
│  │   OFFLINE STORE     │       │   ONLINE STORE      │          │
│  │                     │       │                     │          │
│  │  - Historical data  │       │  - Low-latency      │          │
│  │  - Training queries │ ────▶ │  - Point lookups    │          │
│  │  - Batch features   │ sync  │  - Real-time serving│          │
│  │                     │       │                     │          │
│  │  (Data Warehouse)   │       │  (Redis, DynamoDB)  │          │
│  └─────────────────────┘       └─────────────────────┘          │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   FEATURE REGISTRY                          ││
│  │  - Feature definitions    - Version control                 ││
│  │  - Data lineage          - Access control                   ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### Feature Types

| Type | Computation | Storage | Example |
| ---- | ----------- | ------- | ------- |
| **Batch** | Scheduled (hourly/daily) | Offline → Online | User purchase count (30 days) |
| **Streaming** | Real-time event processing | Direct to online | Items in cart (current) |
| **On-demand** | Request-time computation | Not stored | Distance to nearest store |

### Training-Serving Consistency

```text
TRAINING (Historical):
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Historical   │───▶│ Point-in-Time│───▶│  Training    │
│ Events       │    │ Join         │    │  Dataset     │
└──────────────┘    └──────────────┘    └──────────────┘
                          │
                    Uses feature
                    definitions
                          │
SERVING (Real-time):      ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Online       │───▶│ Same Feature │───▶│  Prediction  │
│ Store        │    │ Definitions  │    │  Request     │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Model Training Infrastructure

### Training Pipeline Components

```text
┌───────────────────────────────────────────────────────────────────────┐
│                     TRAINING PIPELINE                                  │
├───────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐   │
│  │   Data     │──▶│   Feature  │──▶│   Model    │──▶│  Model     │   │
│  │   Loader   │   │   Transform│   │   Train    │   │  Validate  │   │
│  └────────────┘   └────────────┘   └────────────┘   └────────────┘   │
│        │               │                │                 │           │
│        ▼               ▼                ▼                 ▼           │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐   │
│  │ Experiment │   │ Hyperparameter│ │  Checkpoint │  │   Model    │   │
│  │  Tracking  │   │    Tuning     │ │   Storage  │   │  Registry  │   │
│  └────────────┘   └────────────┘   └────────────┘   └────────────┘   │
│                                                                        │
└───────────────────────────────────────────────────────────────────────┘
```

### Training Infrastructure Patterns

| Pattern | Use Case | Tools |
| ------- | -------- | ----- |
| **Single-node** | Small datasets, quick experiments | Jupyter, local GPU |
| **Distributed data-parallel** | Large datasets, same model | Horovod, PyTorch DDP |
| **Model-parallel** | Large models that don't fit in memory | DeepSpeed, FSDP, Megatron |
| **Hyperparameter tuning** | Automated model optimization | Optuna, Ray Tune |

### Experiment Tracking

Track for reproducibility:

| What to Track | Why |
| ------------- | --- |
| **Hyperparameters** | Reproduce training runs |
| **Metrics** | Compare model performance |
| **Artifacts** | Model files, datasets |
| **Code version** | Git commit hash |
| **Environment** | Docker image, dependencies |
| **Data version** | Dataset hash or snapshot |

## Model Serving Architecture

### Serving Patterns

| Pattern | Latency | Throughput | Use Case |
| ------- | ------- | ---------- | -------- |
| **Online (REST/gRPC)** | Low (<100ms) | Medium | Real-time predictions |
| **Batch** | High (hours) | Very high | Bulk scoring |
| **Streaming** | Medium | High | Event-driven predictions |
| **Embedded** | Very low | Varies | Edge/mobile inference |

### Online Serving Architecture

```text
┌─────────────────────────────────────────────────────────────────────┐
│                     MODEL SERVING SYSTEM                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌──────────────┐                                                  │
│   │   Clients    │                                                  │
│   └──────┬───────┘                                                  │
│          │                                                          │
│          ▼                                                          │
│   ┌──────────────┐                                                  │
│   │ Load Balancer│                                                  │
│   └──────┬───────┘                                                  │
│          │                                                          │
│          ▼                                                          │
│   ┌──────────────────────────────────────────────────────────────┐  │
│   │                    API Gateway                                │  │
│   │  - Authentication   - Rate limiting   - Request validation   │  │
│   └──────────────────────────────┬───────────────────────────────┘  │
│                                  │                                  │
│          ┌───────────────────────┼───────────────────────┐         │
│          ▼                       ▼                       ▼         │
│   ┌────────────┐          ┌────────────┐          ┌────────────┐  │
│   │  Model A   │          │  Model B   │          │  Model C   │  │
│   │  (v1.2)    │          │  (v2.0)    │          │  (v1.0)    │  │
│   └────────────┘          └────────────┘          └────────────┘  │
│          │                       │                       │         │
│          └───────────────────────┼───────────────────────┘         │
│                                  ▼                                  │
│                         ┌────────────────┐                         │
│                         │ Feature Store  │                         │
│                         │ (Online)       │                         │
│                         └────────────────┘                         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Latency Optimization

| Technique | Latency Impact | Trade-off |
| --------- | -------------- | --------- |
| **Batching** | Reduces per-request | Increases latency for first request |
| **Caching** | 10-100x faster | May serve stale predictions |
| **Quantization** | 2-4x faster | Slight accuracy loss |
| **Distillation** | Variable | Training overhead |
| **GPU inference** | 10-100x faster | Cost increase |

## A/B Testing ML Models

### Experiment Design

```text
┌─────────────────────────────────────────────────────────────────────┐
│                      A/B TESTING ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌──────────────┐                                                  │
│   │   Traffic    │                                                  │
│   └──────┬───────┘                                                  │
│          │                                                          │
│          ▼                                                          │
│   ┌──────────────────────┐                                          │
│   │ Experiment Assignment │ ◀─────── Experiment Config              │
│   │ - User bucketing      │          - Allocation %                 │
│   │ - Feature flags       │          - Target segments              │
│   └──────────┬───────────┘          - Guardrails                   │
│              │                                                       │
│     ┌────────┴────────┐                                             │
│     ▼                 ▼                                             │
│ ┌────────┐       ┌────────┐                                         │
│ │Control │       │Treatment│                                        │
│ │Model A │       │Model B  │                                        │
│ └────┬───┘       └────┬───┘                                         │
│      │                │                                              │
│      └────────┬───────┘                                             │
│               ▼                                                      │
│      ┌────────────────┐                                             │
│      │ Metrics Logger │                                             │
│      └────────┬───────┘                                             │
│               ▼                                                      │
│      ┌────────────────┐                                             │
│      │ Statistical    │ ─────▶ Decision: Ship / Iterate / Kill     │
│      │ Analysis       │                                             │
│      └────────────────┘                                             │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Metrics to Track

| Metric Type | Examples | Purpose |
| ----------- | -------- | ------- |
| **Model metrics** | AUC, RMSE, precision/recall | Model quality |
| **Business metrics** | CTR, conversion, revenue | Business impact |
| **Guardrail metrics** | Latency, error rate, engagement | Prevent regressions |
| **Segment metrics** | Metrics by user segment | Detect heterogeneous effects |

### Statistical Considerations

- **Sample size**: Calculate power before experiment
- **Duration**: Account for novelty effects and time patterns
- **Multiple testing**: Adjust for multiple metrics (Bonferroni, FDR)
- **Early stopping**: Use sequential testing methods

## Model Monitoring

### What to Monitor

| Category | Metrics | Alert Threshold |
| -------- | ------- | --------------- |
| **Data quality** | Missing values, schema drift | >1% change |
| **Feature drift** | Distribution shift (PSI, KL) | PSI >0.2 |
| **Prediction drift** | Output distribution shift | Depends on use case |
| **Model performance** | Accuracy, AUC (when labels available) | >5% degradation |
| **Operational** | Latency, throughput, errors | SLO violations |

### Drift Detection

```text
┌─────────────────────────────────────────────────────────────────────┐
│                      DRIFT DETECTION PIPELINE                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Training Data                 Production Data                       │
│  ┌──────────────┐              ┌──────────────┐                     │
│  │ Reference    │              │   Current    │                     │
│  │ Distribution │              │ Distribution │                     │
│  └──────┬───────┘              └──────┬───────┘                     │
│         │                             │                              │
│         └──────────────┬──────────────┘                              │
│                        ▼                                             │
│              ┌──────────────────┐                                   │
│              │ Statistical Test │                                   │
│              │ - PSI (Population Stability Index)                   │
│              │ - KS Test                                            │
│              │ - Chi-squared                                        │
│              └────────┬─────────┘                                   │
│                       ▼                                              │
│              ┌──────────────────┐                                   │
│              │  Drift Score     │                                   │
│              └────────┬─────────┘                                   │
│                       │                                              │
│           ┌───────────┼───────────┐                                 │
│           ▼           ▼           ▼                                 │
│      No Drift    Warning     Critical                               │
│      (< 0.1)    (0.1-0.2)    (> 0.2)                               │
│         │           │           │                                   │
│         ▼           ▼           ▼                                   │
│      Continue    Investigate   Retrain                              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Common ML System Design Patterns

### Pattern 1: Recommendation System

```text
Components needed:
- Candidate Generation (retrieve 100s-1000s)
- Ranking Model (score and sort)
- Feature Store (user features, item features)
- Real-time personalization (recent behavior)
- A/B testing infrastructure
```

### Pattern 2: Fraud Detection

```text
Components needed:
- Real-time feature computation
- Low-latency model serving (<50ms)
- High recall focus (can't miss fraud)
- Explainability for compliance
- Human-in-the-loop review
- Feedback loop for labels
```

### Pattern 3: Search Ranking

```text
Components needed:
- Two-stage ranking (retrieval + ranking)
- Feature store for query/document features
- Low latency (<200ms end-to-end)
- Learning to rank models
- Click-through rate prediction
- A/B testing with interleaving
```

## Estimation for ML Systems

### Training Infrastructure

```text
Training time estimation:
- Dataset size: 100M examples
- Model: Transformer (100M params)
- GPU: A100 (80GB, 312 TFLOPS)
- Batch size: 32
- Training steps: Dataset / batch = 3.1M steps
- Time per step: ~100ms
- Total time: ~86 hours single GPU
- With 8 GPUs (data parallel): ~11 hours
```

### Serving Infrastructure

```text
Inference estimation:
- QPS: 10,000
- Model latency: 20ms
- Batch size: 1 (real-time)
- GPU utilization: 50% (latency constraint)
- Requests per GPU/sec: 25
- GPUs needed: 10,000 / 25 = 400 GPUs
- With batching (batch 8): 100 GPUs (4x reduction)
```

## Related Skills

- `llm-serving-patterns` - LLM-specific serving and optimization
- `rag-architecture` - Retrieval-Augmented Generation patterns
- `vector-databases` - Vector search and embeddings
- `ml-inference-optimization` - Latency and cost optimization
- `estimation-techniques` - Back-of-envelope calculations
- `quality-attributes-taxonomy` - NFR definitions

## Related Commands

- `/sd:ml-pipeline <problem>` - Design ML system interactively
- `/sd:estimate <scenario>` - Capacity calculations

## Related Agents

- `ml-systems-designer` - Design ML architectures
- `ml-interviewer` - Mock ML system design interviews

---

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
