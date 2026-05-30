---
name: implementing-mlops
description: Strategic guidance for operationalizing machine learning models from experimentation to production. Covers experiment tracking (MLflow, Weights & Biases), model registry and versioning, feature stores (Feast, Tecton), model serving patterns (Seldon, KServe, BentoML), ML pipeline orchestration (Kubeflow, Airflow), and model monitoring (drift detection, observability). Use when designing ML infrastructure, selecting MLOps platforms, implementing continuous training pipelines, or establishing model governance.
---

# MLOps Patterns

Operationalize machine learning models from experimentation to production deployment and monitoring.

## Purpose

Provide strategic guidance for ML engineers and platform teams to build production-grade ML infrastructure. Cover the complete lifecycle: experiment tracking, model registry, feature stores, deployment patterns, pipeline orchestration, and monitoring.

## When to Use This Skill

Use this skill when:

- Designing MLOps infrastructure for production ML systems
- Selecting experiment tracking platforms (MLflow, Weights & Biases, Neptune)
- Implementing feature stores for online/offline feature serving
- Choosing model serving solutions (Seldon Core, KServe, BentoML, TorchServe)
- Building ML pipelines for training, evaluation, and deployment
- Setting up model monitoring and drift detection
- Establishing model governance and compliance frameworks
- Optimizing ML inference costs and performance
- Migrating from notebooks to production ML systems
- Implementing continuous training and automated retraining

## Core Concepts

### 1. Experiment Tracking

Track experiments systematically to ensure reproducibility and collaboration.

**Key Components:**
- Parameters: Hyperparameters logged for each training run
- Metrics: Performance measures tracked over time (accuracy, loss, F1)
- Artifacts: Model weights, plots, datasets, configuration files
- Metadata: Tags, descriptions, Git commit SHA, environment details

**Platform Comparison:**

**MLflow** (Open-source standard):
- Framework-agnostic (PyTorch, TensorFlow, scikit-learn, XGBoost)
- Self-hosted or cloud-agnostic deployment
- Integrated model registry
- Basic UI, adequate for most use cases
- Free, requires infrastructure management

**Weights & Biases** (SaaS, collaboration-focused):
- Advanced visualization and dashboards
- Integrated hyperparameter optimization (Sweeps)
- Excellent team collaboration features
- SaaS pricing scales with usage
- Best-in-class UI

**Neptune.ai** (Enterprise-grade):
- Enterprise features (RBAC, audit logs, compliance)
- Integrated production monitoring
- Higher cost than W&B
- Good for regulated industries

**Selection Criteria:**
- Open-source requirement → MLflow
- Team collaboration critical → Weights & Biases
- Enterprise compliance (RBAC, audits) → Neptune.ai
- Hyperparameter optimization primary → Weights & Biases (Sweeps)

For detailed comparison and decision framework, see [references/experiment-tracking.md](references/experiment-tracking.md).

### 2. Model Registry and Versioning

Centralize model artifacts with version control and stage management.

**Model Registry Components:**
- Model artifacts (weights, serialized models)
- Training metrics (accuracy, F1, AUC)
- Hyperparameters used during training
- Training dataset version
- Feature schema (input/output signatures)
- Model cards (documentation, use cases, limitations)

**Stage Management:**
- **None**: Newly registered model
- **Staging**: Testing in pre-production environment
- **Production**: Serving live traffic
- **Archived**: Deprecated, retained for compliance

**Versioning Strategies:**

**Semantic Versioning for Models:**
- Major version (v2.0.0): Breaking change in input/output schema
- Minor version (v1.1.0): New feature, backward-compatible
- Patch version (v1.0.1): Bug fix, model retrained on new data

**Git-Based Versioning:**
- Model code in Git (training scripts, configuration)
- Model weights in DVC (Data Version Control) or Git-LFS
- Reproducibility via commit SHA + data version hash

For model lineage tracking and registry patterns, see [references/model-registry.md](references/model-registry.md).

### 3. Feature Stores

Centralize feature engineering to ensure consistency between training and inference.

**Problem Addressed:** Training/serving skew
- Training: Features computed with future knowledge (data leakage)
- Inference: Features computed with only past data
- Result: Model performs well in training but fails in production

**Feature Store Solution:**

**Online Feature Store:**
- Purpose: Low-latency feature retrieval for real-time inference
- Storage: Redis, DynamoDB, Cassandra (key-value stores)
- Latency: Sub-10ms for feature lookup
- Use Case: Real-time predictions (fraud detection, recommendations)

**Offline Feature Store:**
- Purpose: Historical feature data for training and batch inference
- Storage: Parquet files (S3/GCS), data warehouses (Snowflake, BigQuery)
- Latency: Seconds to minutes (batch retrieval)
- Use Case: Model training, backtesting, batch predictions

**Point-in-Time Correctness:**
- Ensures no future data leakage during training
- Feature values at time T only use data available before time T
- Critical for avoiding overly optimistic training metrics

**Platform Comparison:**

**Feast** (Open-source, cloud-agnostic):
- Most popular open-source feature store
- Supports Redis, DynamoDB, Datastore (online) and Parquet, BigQuery, Snowflake (offline)
- Cloud-agnostic, no vendor lock-in
- Active community, growing adoption

**Tecton** (Managed, production-grade):
- Feast-compatible API
- Fully managed service
- Integrated monitoring and governance
- Higher cost, enterprise-focused

**SageMaker Feature Store** (AWS):
- Integrated with AWS ecosystem
- Managed online/offline stores
- AWS lock-in

**Databricks Feature Store** (Databricks):
- Unity Catalog integration
- Delta Lake for offline storage
- Databricks ecosystem lock-in

**Selection Criteria:**
- Open-source, cloud-agnostic → Feast
- Managed solution, production-grade → Tecton
- AWS ecosystem → SageMaker Feature Store
- Databricks users → Databricks Feature Store

For feature engineering patterns and implementation, see [references/feature-stores.md](references/feature-stores.md).

### 4. Model Serving Patterns

Deploy models for synchronous, asynchronous, batch, or streaming inference.

**Serving Patterns:**

**REST API Deployment:**
- Pattern: HTTP endpoint for synchronous predictions
- Latency: <100ms acceptable
- Use Case: Request-response applications
- Tools: Flask, FastAPI, BentoML, Seldon Core

**gRPC Deployment:**
- Pattern: High-performance RPC for low-latency inference
- Latency: <10ms target
- Use Case: Microservices, latency-critical applications
- Tools: TensorFlow Serving, TorchServe, Seldon Core

**Batch Inference:**
- Pattern: Process large datasets offline
- Latency: Minutes to hours acceptable
- Use Case: Daily/hourly predictions for millions of records
- Tools: Spark, Dask, Ray

**Streaming Inference:**
- Pattern: Real-time predictions on streaming data
- Latency: Milliseconds
- Use Case: Fraud detection, anomaly detection, real-time recommendations
- Tools: Kafka + Flink/Spark Streaming

**Platform Comparison:**

**Seldon Core** (Kubernetes-native, advanced):
- Advanced deployment strategies (canary, A/B testing, multi-armed bandits)
- Multi-framework support
- Integrated explainability (Alibi)
- High complexity, steep learning curve

**KServe** (CNCF standard):
- Standardized InferenceService API
- Serverless scaling (scale-to-zero with Knative)
- Kubernetes-native
- Growing adoption, CNCF backing

**BentoML** (Python-first, simplicity):
- Easiest to get started
- Excellent developer experience
- Local testing → cloud deployment
- Lower complexity than Seldon/KServe

**TorchServe** (PyTorch official):
- PyTorch-specific serving
- Production-grade, optimized for PyTorch models
- Less flexible for multi-framework use

**TensorFlow Serving** (TensorFlow official):
- TensorFlow-specific serving
- Production-grade, optimized for TensorFlow models
- Less flexible for multi-framework use

**Selection Criteria:**
- Kubernetes, advanced deployments → Seldon Core or KServe
- Python-first, simplicity → BentoML
- PyTorch-specific → TorchServe
- TensorFlow-specific → TensorFlow Serving
- Managed solution → SageMaker/Vertex AI/Azure ML

For model optimization and serving infrastructure, see [references/model-serving.md](references/model-serving.md).

### 5. Deployment Strategies

Deploy models safely with rollback capabilities.

**Blue-Green Deployment:**
- Two identical environments (Blue: current, Green: new)
- Deploy to Green, test, switch 100% traffic instantly
- Instant rollback (switch back to Blue)
- Trade-off: Requires 2x infrastructure, all-or-nothing switch

**Canary Deployment:**
- Gradual rollout to subset of traffic
- Route 5% → 10% → 25% → 50% → 100% over time
- Monitor metrics at each stage, rollback if degradation
- Trade-off: Complex routing logic, longer deployment time

**Shadow Deployment:**
- New model receives traffic but predictions not used
- Compare new model vs old model offline
- Zero risk to production
- Trade-off: Requires 2x compute, delayed feedback

**A/B Testing:**
- Split traffic between model versions
- Measure business metrics (conversion rate, revenue)
- Statistical significance testing
- Use Case: Optimize for business outcomes, not just ML metrics

**Multi-Armed Bandit (MAB):**
- Epsilon-greedy: Explore (try new models) vs Exploit (use best model)
- Thompson Sampling: Bayesian approach to exploration
- Use Case: Continuous optimization, faster convergence than A/B

**Selection Criteria:**
- Low-risk model → Blue-green (instant cutover)
- Medium-risk model → Canary (gradual rollout)
- High-risk model → Shadow (test in production, no impact)
- Business optimization → A/B testing or MAB

For deployment architecture and examples, see [references/deployment-strategies.md](references/deployment-strategies.md).

### 6. ML Pipeline Orchestration

Automate training, evaluation, and deployment workflows.

**Training Pipeline Stages:**
1. Data Validation (Great Expectations, schema checks)
2. Feature Engineering (transform raw data)
3. Data Splitting (train/validation/test)
4. Model Training (hyperparameter tuning)
5. Model Evaluation (accuracy, fairness, explainability)
6. Model Registration (push to registry if metrics pass thresholds)
7. Deployment (promote to staging/production)

**Continuous Training Pattern:**
- Monitor production data for drift
- Detect data distribution changes (KS test, PSI)
- Trigger automated retraining when drift detected
- Validate new model before deployment
- Deploy via canary or shadow strategy

**Platform Comparison:**

**Kubeflow Pipelines** (ML-native, Kubernetes):
- ML-specific pipeline orchestration
- Kubernetes-native (scales with K8s)
- Component-based (reusable pipeline steps)
- Integrated with Katib (hyperparameter tuning)

**Apache Airflow** (Mature, general-purpose):
- Most mature orchestration platform
- Large ecosystem, extensive integrations
- Python-based DAGs
- Not ML-specific but widely used for ML workflows

**Metaflow** (Netflix, data science-friendly):
- Human-centric design, easy for data scientists
- Excellent local development experience
- Versioning built-in
- Simpler than Kubeflow/Airflow

**Prefect** (Modern, Python-native):
- Dynamic workflows, not static DAGs
- Better error handling than Airflow
- Modern UI and developer experience
- Growing community

**Dagster** (Asset-based, testing-focused):
- Asset-based thinking (not just task dependencies)
- Strong testing and data quality features
- Modern approach, good for data teams
- Smaller community than Airflow

**Selection Criteria:**
- ML-specific, Kubernetes → Kubeflow Pipelines
- Mature, battle-tested → Apache Airflow
- Data scientists, ease of use → Metaflow
- Software engineers, testing → Dagster
- Modern, simpler than Airflow → Prefect

For pipeline architecture and examples, see [references/ml-pipelines.md](references/ml-pipelines.md).

### 7. Model Monitoring and Observability

Monitor production models for drift, performance, and quality.

**Data Drift Detection:**
- Definition: Input feature distributions change over time
- Impact: Model trained on old distribution, predictions degrade
- Detection Methods:
  - Kolmogorov-Smirnov (KS) Test: Compare distributions
  - Population Stability Index (PSI): Measure distribution shift
  - Chi-Square Test: For categorical features
- Action: Trigger automated retraining when drift detected

**Model Drift Detection:**
- Definition: Model prediction quality degrades over time
- Impact: Accuracy, precision, recall decrease
- Detection Methods:
  - Ground truth accuracy (delayed labels)
  - Prediction distribution changes
  - Calibration drift (predicted probabilities vs actual outcomes)
- Action: Alert team, trigger retraining

**Performance Monitoring:**
- Metrics:
  - Latency: P50, P95, P99 inference time
  - Throughput: Predictions per second
  - Error Rate: Failed predictions / total predictions
  - Resource Utilization: CPU, memory, GPU usage
- Alerting Thresholds:
  - P95 latency > 100ms → Alert
  - Error rate > 1% → Alert
  - Accuracy drop > 5% → Trigger retraining

**Business Metrics Monitoring:**
- Downstream impact: Conversion rate, revenue, user satisfaction
- Model predictions → business outcomes correlation
- Use Case: Optimize models for business value, not just ML metrics

**Tools:**
- Evidently AI: Data drift, model drift, data quality reports
- Prometheus + Grafana: Performance metrics, custom dashboards
- Arize AI: ML observability platform
- Fiddler: Model monitoring and explainability

For monitoring architecture and implementation, see [references/model-monitoring.md](references/model-monitoring.md).

### 8. Model Optimization Techniques

Reduce model size and inference latency.

**Quantization:**
- Convert model weights from float32 to int8
- Model size reduction: 4x smaller
- Inference speed: 2-3x faster
- Accuracy impact: Minimal (<1% degradation typically)
- Tools: PyTorch quantization, TensorFlow Lite, ONNX Runtime

**Model Distillation:**
- Train small student model to mimic large teacher model
- Transfer knowledge from teacher (BERT-large) to student (DistilBERT)
- Size reduction: 2-10x smaller
- Speed improvement: 2-10x faster
- Use Case: Deploy small model on edge devices, reduce inference cost

**ONNX Conversion:**
- Convert models to Open Neural Network Exchange (ONNX) format
- Cross-framework compatibility (PyTorch → ONNX → TensorFlow)
- Optimized inference with ONNX Runtime
- Speed improvement: 1.5-3x faster than native framework

**Model Pruning:**
- Remove less important weights from neural networks
- Sparsity: 30-90% of weights set to zero
- Size reduction: 2-10x smaller
- Accuracy impact: Minimal with structured pruning

For optimization techniques and examples, see [references/model-serving.md](references/model-serving.md#optimization).

### 9. LLMOps Patterns

Operationalize Large Language Models with specialized patterns.

**LLM Fine-Tuning Pipelines:**
- LoRA (Low-Rank Adaptation): Parameter-efficient fine-tuning
- QLoRA: Quantized LoRA (4-bit quantization)
- Pipeline: Base model → Fine-tuning dataset → LoRA adapters → Merged model
- Tools: Hugging Face PEFT, Axolotl

**Prompt Versioning:**
- Version control for prompts (Git, prompt management platforms)
- A/B testing prompts for quality and cost optimization
- Monitoring prompt effectiveness over time

**RAG System Monitoring:**
- Retrieval quality: Relevance of retrieved documents
- Generation quality: Answer accuracy, hallucination detection
- End-to-end latency: Retrieval + generation time
- Tools: LangSmith, Arize Phoenix

**LLM Inference Optimization:**
- vLLM: High-throughput LLM serving
- TensorRT-LLM: NVIDIA-optimized LLM inference
- Text Generation Inference (TGI): Hugging Face serving
- Batching: Dynamic batching for throughput

**Embedding Model Management:**
- Version embeddings alongside models
- Monitor embedding drift (distribution changes)
- Update embeddings when underlying model changes

For LLMOps patterns and implementation, see [references/llmops-patterns.md](references/llmops-patterns.md).

### 10. Model Governance and Compliance

Establish governance for model risk management and regulatory compliance.

**Model Cards:**
- Documentation: Model purpose, training data, performance metrics
- Limitations: Known biases, failure modes, out-of-scope use cases
- Ethical considerations: Fairness, privacy, societal impact
- Template: Model Card Toolkit (Google)

**Bias and Fairness Detection:**
- Measure disparate impact across demographic groups
- Tools: Fairlearn, AI Fairness 360 (IBM)
- Metrics: Demographic parity, equalized odds, calibration
- Mitigation: Reweighting, adversarial debiasing, threshold optimization

**Regulatory Compliance:**
- EU AI Act: High-risk AI systems require documentation, monitoring
- Model Risk Management (SR 11-7): Banking industry requirements
- GDPR: Right to explanation for automated decisions
- HIPAA: Healthcare data privacy

**Audit Trails:**
- Log all model versions, training runs, deployments
- Track who approved model transitions (staging → production)
- Retain historical predictions for compliance audits
- Tools: MLflow, Neptune.ai (audit logs)

For governance frameworks and compliance, see [references/governance.md](references/governance.md).

## Decision Frameworks

### Framework 1: Experiment Tracking Platform Selection

**Decision Tree:**

Start with primary requirement:
- Open-source, self-hosted requirement → **MLflow**
- Team collaboration, advanced visualization (budget available) → **Weights & Biases**
- Team collaboration, advanced visualization (no budget) → **MLflow**
- Enterprise compliance (audit logs, RBAC) → **Neptune.ai**
- Hyperparameter optimization primary use case → **Weights & Biases** (Sweeps)

**Detailed Criteria:**

| Criteria | MLflow | Weights & Biases | Neptune.ai |
|----------|--------|------------------|------------|
| Cost | Free | $200/user/month | $300/user/month |
| Collaboration | Basic | Excellent | Good |
| Visualization | Basic | Excellent | Good |
| Hyperparameter Tuning | External (Optuna) | Integrated (Sweeps) | Basic |
| Model Registry | Included | Add-on | Included |
| Self-Hosted | Yes | No (paid only) | Limited |
| Enterprise Features | No | Limited | Excellent |

**Recommendation by Organization:**
- Startup (<50 people): MLflow (free, adequate) or W&B (if budget)
- Growth (50-500 people): Weights & Biases (team collaboration)
- Enterprise (>500 people): Neptune.ai (compliance) or MLflow (cost)

For detailed decision framework, see [references/decision-frameworks.md](references/decision-frameworks.md#experiment-tracking).

### Framework 2: Feature Store Selection

**Decision Matrix:**

Primary requirement:
- Open-source, cloud-agnostic → **Feast**
- Managed solution, production-grade, multi-cloud → **Tecton**
- AWS ecosystem → **SageMaker Feature Store**
- GCP ecosystem → **Vertex AI Feature Store**
- Azure ecosystem → **Azure ML Feature Store**
- Databricks users → **Databricks Feature Store**
- Self-hosted with UI → **Hopsworks**

**Criteria Comparison:**

| Factor | Feast | Tecton | Hopsworks | SageMaker FS |
|--------|-------|--------|-----------|--------------|
| Cost | Free | $$$$ | Free (self-host) | $$$ |
| Online Serving | Redis, DynamoDB | Managed | RonDB | Managed |
| Offline Store | Parquet, BigQuery, Snowflake | Managed | Hive, S3 | S3 |
| Point-in-Time | Yes | Yes | Yes | Yes |
| Monitoring | External | Integrated | Basic | External |
| Cloud Lock-in | No | No | No | AWS |

**Recommendation:**
- Open-source, self-managed → Feast
- Managed, production-grade → Tecton
- AWS ecosystem → SageMaker Feature Store
- Databricks users → Databricks Feature Store

For detailed decision framework, see [references/decision-frameworks.md](references/decision-frameworks.md#feature-store).

### Framework 3: Model Serving Platform Selection

**Decision Tree:**

Infrastructure:
- Kubernetes-based → Advanced deployment patterns needed?
  - Yes → **Seldon Core** (most features) or **KServe** (CNCF standard)
  - No → **BentoML** (simpler, Python-first)
- Cloud-native (managed) → Cloud provider?
  - AWS → **SageMaker Endpoints**
  - GCP → **Vertex AI Endpoints**
  - Azure → **Azure ML Endpoints**
- Framework-specific → Framework?
  - PyTorch → **TorchServe**
  - TensorFlow → **TensorFlow Serving**
- Serverless / minimal infrastructure → **BentoML** or Cloud Functions

**Detailed Criteria:**

| Feature | Seldon Core | KServe | BentoML | TorchServe |
|---------|-------------|--------|---------|------------|
| Kubernetes-Native | Yes | Yes | Optional | No |
| Multi-Framework | Yes | Yes | Yes | PyTorch-only |
| Deployment Strategies | Excellent | Good | Basic | Basic |
| Explainability | Integrated | Integrated | External | No |
| Complexity | High | Medium | Low | Low |
| Learning Curve | Steep | Medium | Gentle | Gentle |

**Recommendation:**
- Kubernetes, advanced deployments → Seldon Core or KServe
- Python-first, simplicity → BentoML
- PyTorch-specific → TorchServe
- TensorFlow-specific → TensorFlow Serving
- Managed solution → SageMaker/Vertex AI/Azure ML

For detailed decision framework, see [references/decision-frameworks.md](references/decision-frameworks.md#model-serving).

### Framework 4: ML Pipeline Orchestration Selection

**Decision Matrix:**

Primary use case:
- ML-specific pipelines, Kubernetes-native → **Kubeflow Pipelines**
- General-purpose orchestration, mature ecosystem → **Apache Airflow**
- Data science workflows, ease of use → **Metaflow**
- Modern approach, asset-based thinking → **Dagster**
- Dynamic workflows, Python-native → **Prefect**

**Criteria Comparison:**

| Factor | Kubeflow | Airflow | Metaflow | Dagster | Prefect |
|--------|----------|---------|----------|---------|---------|
| ML-Specific | Excellent | Good | Excellent | Good | Good |
| Kubernetes | Native | Compatible | Optional | Compatible | Compatible |
| Learning Curve | Steep | Steep | Gentle | Medium | Medium |
| Maturity | High | Very High | Medium | Medium | Medium |
| Community | Large | Very Large | Growing | Growing | Growing |

**Recommendation:**
- ML-specific, Kubernetes → Kubeflow Pipelines
- Mature, battle-tested → Apache Airflow
- Data scientists → Metaflow
- Software engineers → Dagster
- Modern, simpler than Airflow → Prefect

For detailed decision framework, see [references/decision-frameworks.md](references/decision-frameworks.md#orchestration).

## Implementation Patterns

### Pattern 1: End-to-End ML Pipeline

Automate the complete ML workflow from data to deployment.

**Pipeline Stages:**
1. Data Validation (Great Expectations)
2. Feature Engineering (transform raw data)
3. Data Splitting (train/validation/test)
4. Model Training (with hyperparameter tuning)
5. Model Evaluation (accuracy, fairness, explainability)
6. Model Registration (push to MLflow registry)
7. Deployment (promote to staging/production)

**Architecture:**
```
Data Lake → Data Validation → Feature Engineering → Training → Evaluation
    ↓
Model Registry (staging) → Testing → Production Deployment
```

For implementation details and code examples, see [references/ml-pipelines.md](references/ml-pipelines.md#end-to-end).

### Pattern 2: Continuous Training

Automate model retraining based on drift detection.

**Workflow:**
1. Monitor production data for distribution changes
2. Detect data drift (KS test, PSI)
3. Trigger automated retraining pipeline
4. Validate new model (accuracy, fairness)
5. Deploy via canary strategy (5% → 100%)
6. Monitor new model performance
7. Rollback if metrics degrade

**Trigger Conditions:**
- Scheduled: Daily/weekly retraining
- Data drift: KS test p-value < 0.05
- Model drift: Accuracy drop > 5%
- Data volume: New training data exceeds threshold (10K samples)

For implementation details, see [references/ml-pipelines.md](references/ml-pipelines.md#continuous-training).

### Pattern 3: Feature Store Integration

Ensure consistent features between training and inference.

**Architecture:**
```
Offline Store (Training):
  Parquet/BigQuery → Point-in-Time Join → Training Dataset

Online Store (Inference):
  Redis/DynamoDB → Low-Latency Lookup → Real-Time Prediction
```

**Point-in-Time Correctness:**
- Training: Fetch features as of specific timestamps (no future data)
- Inference: Fetch latest features (only past data)
- Guarantee: Same feature logic in training and inference

For implementation details and code examples, see [references/feature-stores.md](references/feature-stores.md#integration).

### Pattern 4: Shadow Deployment Testing

Test new models in production without risk.

**Workflow:**
1. Deploy new model (v2) in shadow mode
2. v2 receives copy of production traffic
3. v1 predictions used for responses (no user impact)
4. Compare v1 and v2 predictions offline
5. Analyze differences, measure v2 accuracy
6. Promote v2 to production if performance acceptable

**Use Cases:**
- High-risk models (financial, healthcare, safety-critical)
- Need extensive testing before cutover
- Compare model behavior on real production data

For deployment architecture, see [references/deployment-strategies.md](references/deployment-strategies.md#shadow).

## Tool Recommendations

### Production-Ready Tools (High Adoption)

**MLflow** - Experiment Tracking & Model Registry
- GitHub Stars: 20,000+
- Trust Score: 95/100
- Use Cases: Experiment tracking, model registry, model serving
- Strengths: Open-source, framework-agnostic, self-hosted option
- Getting Started: `pip install mlflow && mlflow server`

**Feast** - Feature Store
- GitHub Stars: 5,000+
- Trust Score: 85/100
- Use Cases: Online/offline feature serving, point-in-time correctness
- Strengths: Cloud-agnostic, most popular open-source feature store
- Getting Started: `pip install feast && feast init`

**Seldon Core** - Model Serving (Advanced)
- GitHub Stars: 4,000+
- Trust Score: 85/100
- Use Cases: Kubernetes-native serving, advanced deployment patterns
- Strengths: Canary, A/B testing, MAB, explainability
- Limitation: High complexity, steep learning curve

**KServe** - Model Serving (CNCF Standard)
- GitHub Stars: 3,500+
- Trust Score: 85/100
- Use Cases: Standardized serving API, serverless scaling
- Strengths: CNCF project, Knative integration, growing adoption
- Limitation: Kubernetes required

**BentoML** - Model Serving (Simplicity)
- GitHub Stars: 6,000+
- Trust Score: 80/100
- Use Cases: Easy packaging, Python-first deployment
- Strengths: Lowest learning curve, excellent developer experience
- Limitation: Fewer advanced features than Seldon/KServe

**Kubeflow Pipelines** - ML Orchestration
- GitHub Stars: 14,000+ (Kubeflow project)
- Trust Score: 90/100
- Use Cases: ML-specific pipelines, Kubernetes-native workflows
- Strengths: ML-native, component reusability, Katib integration
- Limitation: Kubernetes required, steep learning curve

**Weights & Biases** - Experiment Tracking (SaaS)
- Trust Score: 90/100
- Use Cases: Team collaboration, advanced visualization, hyperparameter tuning
- Strengths: Best-in-class UI, integrated Sweeps, strong community
- Limitation: SaaS pricing, no self-hosted free tier

For detailed tool comparisons, see [references/tool-recommendations.md](references/tool-recommendations.md).

### Tool Stack Recommendations by Organization

**Startup (Cost-Optimized, Simple):**
- Experiment Tracking: MLflow (free, self-hosted)
- Feature Store: None initially → Feast when needed
- Model Serving: BentoML (easy) or cloud functions
- Orchestration: Prefect or cron jobs
- Monitoring: Basic logging + Prometheus

**Growth Company (Balanced):**
- Experiment Tracking: Weights & Biases or MLflow
- Feature Store: Feast (open-source, production-ready)
- Model Serving: BentoML or KServe (Kubernetes-based)
- Orchestration: Kubeflow Pipelines or Airflow
- Monitoring: Evidently + Prometheus + Grafana

**Enterprise (Full Stack):**
- Experiment Tracking: MLflow (self-hosted) or Neptune.ai (compliance)
- Feature Store: Tecton (managed) or Feast (self-hosted)
- Model Serving: Seldon Core (advanced) or KServe
- Orchestration: Kubeflow Pipelines or Airflow
- Monitoring: Evidently + Prometheus + Grafana + PagerDuty

**Cloud-Native (Managed Services):**
- AWS: SageMaker (end-to-end platform)
- GCP: Vertex AI (end-to-end platform)
- Azure: Azure ML (end-to-end platform)

For scenario-specific recommendations, see [references/scenarios.md](references/scenarios.md).

## Common Scenarios

### Scenario 1: Startup MLOps Stack

**Context:** 20-person startup, 5 data scientists, 3 models (fraud detection, recommendation, churn), limited budget.

**Recommendation:**
- Experiment Tracking: MLflow (free, self-hosted)
- Model Serving: BentoML (simple, fast iteration)
- Orchestration: Prefect (simpler than Airflow)
- Monitoring: Prometheus + basic drift detection
- Feature Store: Skip initially, use database tables

**Rationale:**
- Minimize cost (all open-source, self-hosted)
- Fast iteration (BentoML easy to deploy)
- Don't over-engineer (no Kubeflow for 3 models)
- Add feature store (Feast) when scaling to 10+ models

For detailed scenario, see [references/scenarios.md](references/scenarios.md#startup).

### Scenario 2: Enterprise ML Platform

**Context:** 500-person company, 50 data scientists, 100+ models, regulatory compliance, multi-cloud.

**Recommendation:**
- Experiment Tracking: Neptune.ai (compliance, audit logs) or MLflow (cost)
- Feature Store: Feast (self-hosted, cloud-agnostic)
- Model Serving: Seldon Core (advanced deployment patterns)
- Orchestration: Kubeflow Pipelines (ML-native, Kubernetes)
- Monitoring: Evidently + Prometheus + Grafana + PagerDuty

**Rationale:**
- Compliance required (Neptune audit logs, RBAC)
- Multi-cloud (Feast cloud-agnostic)
- Advanced deployments (Seldon canary, A/B testing)
- Scale (Kubernetes for 100+ models)

For detailed scenario, see [references/scenarios.md](references/scenarios.md#enterprise).

### Scenario 3: LLM Fine-Tuning Pipeline

**Context:** Fine-tune LLM for domain-specific use case, deploy for production serving.

**Recommendation:**
- Experiment Tracking: MLflow (track fine-tuning runs)
- Pipeline Orchestration: Kubeflow Pipelines (GPU scheduling)
- Model Serving: vLLM (high-throughput LLM serving)
- Prompt Versioning: Git + LangSmith
- Monitoring: Arize Phoenix (RAG monitoring)

**Rationale:**
- Track fine-tuning experiments (LoRA adapters, hyperparameters)
- GPU orchestration (Kubeflow on Kubernetes)
- Efficient LLM serving (vLLM optimized for throughput)
- Monitor RAG systems (retrieval + generation quality)

For detailed scenario, see [references/scenarios.md](references/scenarios.md#llmops).

## Integration with Other Skills

**Direct Dependencies:**
- `ai-data-engineering`: Feature engineering, ML algorithms, data preparation
- `kubernetes-operations`: K8s cluster management, GPU scheduling for ML workloads
- `observability`: Monitoring, alerting, distributed tracing for ML systems

**Complementary Skills:**
- `data-architecture`: Data pipelines, data lakes feeding ML models
- `data-transformation`: dbt for feature transformation pipelines
- `streaming-data`: Kafka, Flink for real-time ML inference
- `designing-distributed-systems`: Scalability patterns for ML workloads
- `api-design-principles`: ML model APIs, REST/gRPC serving patterns

**Downstream Skills:**
- `building-ai-chat`: LLM-powered applications consuming ML models
- `visualizing-data`: Dashboards for ML metrics and monitoring

## Best Practices

1. **Version Everything:**
   - Code: Git commit SHA for reproducibility
   - Data: DVC or data version hash
   - Models: Semantic versioning (v1.2.3)
   - Features: Feature store versioning

2. **Automate Testing:**
   - Unit tests: Model loads, accepts input, produces output
   - Integration tests: End-to-end pipeline execution
   - Model validation: Accuracy thresholds, fairness checks

3. **Monitor Continuously:**
   - Data drift: Distribution changes over time
   - Model drift: Accuracy degradation
   - Performance: Latency, throughput, error rates

4. **Start Simple:**
   - Begin with MLflow + basic serving (BentoML)
   - Add complexity as needed (feature store, Kubeflow)
   - Avoid over-engineering (don't build Kubeflow for 2 models)

5. **Point-in-Time Correctness:**
   - Use feature stores to avoid training/serving skew
   - Ensure no future data leakage in training
   - Consistent feature logic in training and inference

6. **Deployment Strategies:**
   - Use canary for medium-risk models (gradual rollout)
   - Use shadow for high-risk models (zero production impact)
   - Always have rollback plan (instant switch to previous version)

7. **Governance:**
   - Model cards: Document model purpose, limitations, biases
   - Audit trails: Track all model versions, deployments, approvals
   - Compliance: EU AI Act, model risk management (SR 11-7)

8. **Cost Optimization:**
   - Quantization: Reduce model size 4x, inference speed 2-3x
   - Spot instances: Train on preemptible VMs (60-90% cost reduction)
   - Autoscaling: Scale inference endpoints based on load

## Anti-Patterns

❌ **Notebooks in Production:**
- Never deploy Jupyter notebooks to production
- Use notebooks for experimentation only
- Production: Use scripts, Docker containers, CI/CD pipelines

❌ **Manual Model Deployment:**
- Automate deployment with CI/CD pipelines
- Use model registry stage transitions (staging → production)
- Eliminate human error, ensure reproducibility

❌ **No Monitoring:**
- Production models without monitoring will degrade silently
- Implement drift detection (data drift, model drift)
- Set up alerting for accuracy drops, latency spikes

❌ **Training/Serving Skew:**
- Different feature logic in training vs inference
- Use feature stores to ensure consistency
- Test feature parity before production deployment

❌ **Ignoring Data Quality:**
- Garbage in, garbage out (GIGO)
- Validate data schema, ranges, distributions
- Use Great Expectations for data validation

❌ **Over-Engineering:**
- Don't build Kubeflow for 2 models
- Start simple (MLflow + BentoML)
- Add complexity only when necessary (10+ models)

❌ **No Rollback Plan:**
- Always have ability to rollback to previous model version
- Blue-green, canary, shadow deployments enable instant rollback
- Test rollback procedure before production deployment

## Further Reading

**Reference Files:**
- [Experiment Tracking](references/experiment-tracking.md) - MLflow, W&B, Neptune deep dive
- [Model Registry](references/model-registry.md) - Versioning, lineage, stage transitions
- [Feature Stores](references/feature-stores.md) - Feast, Tecton, online/offline patterns
- [Model Serving](references/model-serving.md) - Seldon, KServe, BentoML, optimization
- [Deployment Strategies](references/deployment-strategies.md) - Blue-green, canary, shadow, A/B
- [ML Pipelines](references/ml-pipelines.md) - Kubeflow, Airflow, training pipelines
- [Model Monitoring](references/model-monitoring.md) - Drift detection, observability
- [LLMOps Patterns](references/llmops-patterns.md) - LLM fine-tuning, RAG, prompts
- [Decision Frameworks](references/decision-frameworks.md) - Tool selection frameworks
- [Tool Recommendations](references/tool-recommendations.md) - Detailed comparisons
- [Scenarios](references/scenarios.md) - Startup, enterprise, LLMOps use cases
- [Governance](references/governance.md) - Model cards, compliance, fairness

**Example Projects:**
- [examples/mlflow-experiment/](examples/mlflow-experiment/) - Complete MLflow setup
- [examples/feast-feature-store/](examples/feast-feature-store/) - Feast online/offline
- [examples/seldon-deployment/](examples/seldon-deployment/) - Canary, A/B testing
- [examples/kubeflow-pipeline/](examples/kubeflow-pipeline/) - End-to-end pipeline
- [examples/monitoring-dashboard/](examples/monitoring-dashboard/) - Evidently + Prometheus

**Scripts:**
- [scripts/setup_mlflow_server.sh](scripts/setup_mlflow_server.sh) - MLflow with PostgreSQL + S3
- [scripts/feast_feature_definition_generator.py](scripts/feast_feature_definition_generator.py) - Generate Feast features
- [scripts/model_validation_suite.py](scripts/model_validation_suite.py) - Automated model tests
- [scripts/drift_detection_monitor.py](scripts/drift_detection_monitor.py) - Scheduled drift detection
- [scripts/kubernetes_model_deploy.py](scripts/kubernetes_model_deploy.py) - Deploy to Seldon/KServe
