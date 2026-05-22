---
name: using-ml-production
description: Router skill directing to deployment, optimization, MLOps, and monitoring guides.
---

# Using ML Production

## Overview

This meta-skill routes you to the right production deployment skill based on your concern. Load this when you need to move ML models to production but aren't sure which specific aspect to address.

**Core Principle**: Production concerns fall into four categories. Identify the concern first, then route to the appropriate skill. Tools and infrastructure choices are implementation details, not routing criteria.

## When to Use

Load this skill when:
- Deploying ML models to production
- Optimizing model inference (speed, size, cost)
- Setting up MLOps workflows (tracking, automation, CI/CD)
- Monitoring or debugging production models
- User mentions: "production", "deploy", "serve model", "MLOps", "monitoring", "optimize inference"

**Don't use for**: Training optimization (use `training-optimization`), model architecture selection (use `neural-architectures`), PyTorch infrastructure (use `pytorch-engineering`)

---

## How to Access Reference Sheets

**IMPORTANT**: All reference sheets are located in the SAME DIRECTORY as this SKILL.md file.

When this skill is loaded from:
  `skills/using-ml-production/SKILL.md`

Reference sheets like `quantization-for-inference.md` are at:
  `skills/using-ml-production/quantization-for-inference.md`

NOT at:
  `skills/quantization-for-inference.md` ← WRONG PATH

When you see a link like `[quantization-for-inference.md](quantization-for-inference.md)`, read the file from the same directory as this SKILL.md.

---

## Routing by Concern

### Category 1: Model Optimization

**Symptoms**: "Model too slow", "inference latency high", "model too large", "need to optimize for edge", "reduce model size", "speed up inference"

**When to route here**:
- Model itself is the bottleneck (not infrastructure)
- Need to reduce model size or increase inference speed
- Deploying to resource-constrained hardware (edge, mobile)
- Cost optimization through model efficiency

**Routes to**:
- [quantization-for-inference.md](quantization-for-inference.md) - Reduce precision (INT8/INT4), speed up inference
- [model-compression-techniques.md](model-compression-techniques.md) - Pruning, distillation, architecture optimization
- [hardware-optimization-strategies.md](hardware-optimization-strategies.md) - GPU/CPU/edge tuning, batch sizing

**Key question to ask**: "Is the MODEL the bottleneck, or is it infrastructure/serving?"

---

### Category 2: Serving Infrastructure

**Symptoms**: "How to serve model", "need API endpoint", "deploy to production", "containerize model", "scale serving", "load balancing", "traffic management"

**When to route here**:
- Need to expose model as API or service
- Questions about serving patterns (REST, gRPC, batch)
- Deployment strategies (gradual rollout, A/B testing)
- Scaling concerns (traffic, replicas, autoscaling)

**Routes to**:
- [model-serving-patterns.md](model-serving-patterns.md) - FastAPI, TorchServe, gRPC, ONNX, batching, containerization
- [deployment-strategies.md](deployment-strategies.md) - A/B testing, canary, shadow mode, rollback procedures
- [scaling-and-load-balancing.md](scaling-and-load-balancing.md) - Horizontal scaling, autoscaling, load balancing, cost optimization

**Key distinction**:
- Serving patterns = HOW to expose model (API, container, batching)
- Deployment strategies = HOW to roll out safely (gradual, testing, rollback)
- Scaling = HOW to handle traffic (replicas, autoscaling, balancing)

---

### Category 3: MLOps Tooling

**Symptoms**: "Track experiments", "version models", "automate deployment", "reproducibility", "CI/CD for ML", "feature store", "model registry", "experiment management"

**When to route here**:
- Need workflow/process improvements
- Want to track experiments or version models
- Need to automate training-to-deployment pipeline
- Team collaboration and reproducibility concerns

**Routes to**:
- [experiment-tracking-and-versioning.md](experiment-tracking-and-versioning.md) - MLflow, Weights & Biases, model registries, reproducibility, lineage
- [mlops-pipeline-automation.md](mlops-pipeline-automation.md) - CI/CD for ML, feature stores, data validation, automated retraining, orchestration

**Key distinction**:
- Experiment tracking = Research/development phase (track runs, version models)
- Pipeline automation = Production phase (automate workflows, CI/CD)

**Multi-concern**: Queries like "track experiments AND automate deployment" → route to BOTH skills

---

### Category 4: Observability

**Symptoms**: "Monitor production", "model degrading", "detect drift", "production debugging", "alert on failures", "model not working in prod", "performance issues in production"

**When to route here**:
- Model already deployed, need to monitor or debug
- Detecting production issues (drift, errors, degradation)
- Setting up alerts and dashboards
- Root cause analysis for production failures

**Routes to**:
- [production-monitoring-and-alerting.md](production-monitoring-and-alerting.md) - Metrics, drift detection, dashboards, alerts, SLAs
- [production-debugging-techniques.md](production-debugging-techniques.md) - Error analysis, profiling, rollback procedures, post-mortems

**Key distinction**:
- Monitoring = Proactive (set up metrics, alerts, detect issues early)
- Debugging = Reactive (diagnose and fix existing issues)

**"Performance" ambiguity**:
- If "performance" = speed/latency → might be Category 1 (optimization) or Category 2 (serving/scaling)
- If "performance" = accuracy degradation → Category 4 (observability - drift detection)
- **Ask clarifying question**: "By performance, do you mean inference speed or model accuracy?"

---

## Routing Decision Tree

```
User query → Identify primary concern

Is model THE problem (size/speed)?
  YES → Category 1: Model Optimization
  NO → Continue

Is it about HOW to expose/deploy model?
  YES → Category 2: Serving Infrastructure
  NO → Continue

Is it about workflow/process/automation?
  YES → Category 3: MLOps Tooling
  NO → Continue

Is it about monitoring/debugging in production?
  YES → Category 4: Observability
  NO → Ask clarifying question

Ambiguous? → Ask ONE question to clarify concern category
```

---

## Clarification Questions for Ambiguous Queries

### Query: "My model is too slow"

**Ask**: "Is this inference latency (how fast predictions are), or training time?"
- Training → Route to `training-optimization` (wrong pack)
- Inference → Follow-up: "Have you profiled to find bottlenecks?"
  - Model is bottleneck → Category 1 (optimization)
  - Infrastructure/batching issue → Category 2 (serving)

### Query: "I need to deploy my model"

**Ask**: "What's your deployment target - cloud server, edge device, or batch processing?"
- Cloud/server → Category 2 (serving-patterns, then maybe deployment-strategies if gradual rollout needed)
- Edge/mobile → Category 1 (optimization first for size/speed) + Category 2 (serving)
- Batch → Category 2 (serving-patterns - batch processing)

### Query: "My model isn't performing well in production"

**Ask**: "By performance, do you mean inference speed or prediction accuracy?"
- Speed → Category 1 (optimization) or Category 2 (serving/scaling)
- Accuracy → Category 4 (observability - drift detection, monitoring)

### Query: "Set up MLOps for my team"

**Ask**: "What's the current pain point - experiment tracking, automated deployment, or both?"
- Tracking/versioning → Category 3 (experiment-tracking-and-versioning)
- Automation/CI/CD → Category 3 (mlops-pipeline-automation)
- Both → Route to BOTH skills

---

## Multi-Concern Scenarios

Some queries span multiple categories. Route to ALL relevant skills in logical order:

| Scenario | Route Order | Why |
|----------|-------------|-----|
| "Optimize and deploy model" | 1. Optimization → 2. Serving | Optimize BEFORE deploying |
| "Deploy and monitor model" | 1. Serving → 2. Observability | Deploy BEFORE monitoring |
| "Track experiments and automate deployment" | 1. Experiment tracking → 2. Pipeline automation | Track BEFORE automating |
| "Quantize model and serve with TorchServe" | 1. Quantization → 2. Serving patterns | Optimize BEFORE serving |
| "Deploy with A/B testing and monitor" | 1. Deployment strategies → 2. Monitoring | Deploy strategy BEFORE monitoring |

**Principle**: Route in execution order (what needs to happen first).

---

## Relationship with Other Packs

### With llm-specialist

**ml-production covers**: General serving, quantization, deployment, monitoring (universal patterns)

**llm-specialist covers**: LLM-specific optimization (KV cache, prompt caching, speculative decoding, token streaming)

**When to use both**:
- "Deploy LLM to production" → llm-specialist (for inference-optimization) + ml-production (for serving, monitoring)
- "Quantize LLM" → llm-specialist (LLM-specific quantization patterns) OR ml-production (general quantization)

**Rule of thumb**: LLM-specific optimization stays in llm-specialist. General production patterns use ml-production.

### With training-optimization

**Clear boundary**:
- training-optimization = Training phase (convergence, hyperparameters, training speed)
- ml-production = Inference phase (deployment, serving, monitoring)

**"Too slow" disambiguation**:
- Training slow → training-optimization
- Inference slow → ml-production

### With pytorch-engineering

**pytorch-engineering covers**: Foundation (distributed training, profiling, memory management)

**ml-production covers**: Production-specific (serving APIs, deployment patterns, MLOps)

**When to use both**:
- "Profile production inference" → pytorch-engineering (profiling techniques) + ml-production (production context)
- "Optimize serving performance" → ml-production (serving patterns) + pytorch-engineering (if need low-level profiling)

---

## Common Routing Mistakes

| Query | Wrong Route | Correct Route | Why |
|-------|-------------|---------------|-----|
| "Model too slow in production" | Immediately to quantization | Ask: inference or training? Then model vs infrastructure? | Could be serving/batching issue, not model |
| "Deploy with Kubernetes" | Defer to Kubernetes docs | Category 2: serving-patterns or deployment-strategies | Kubernetes is tool choice, not routing concern |
| "Set up MLOps" | Route to one skill | Ask about specific pain point, might be both tracking AND automation | MLOps spans multiple skills |
| "Performance issues" | Assume accuracy | Ask: speed or accuracy? | Performance is ambiguous |
| "We use TorchServe" | Skip routing | Still route to serving-patterns | Tool choice doesn't change routing |

---

## Common Rationalizations (Don't Do These)

| Excuse | Reality |
|--------|---------|
| "User mentioned Kubernetes, route to deployment" | Tools are implementation details. Route by concern first. |
| "Slow = optimization, route to quantization" | Slow could be infrastructure. Clarify model vs serving bottleneck. |
| "They said deploy, must be serving-patterns" | Could need serving + deployment-strategies + monitoring. Don't assume single concern. |
| "MLOps = experiment tracking" | MLOps spans tracking AND automation. Ask which pain point. |
| "Performance obviously means speed" | Could mean accuracy. Clarify inference speed vs prediction quality. |
| "They're technical, skip clarification" | Technical users still benefit from clarifying questions. |

---

## Red Flags Checklist

If you catch yourself thinking ANY of these, STOP and clarify:

- "I'll guess optimization vs serving" → ASK which is the bottleneck
- "Performance probably means speed" → ASK speed or accuracy
- "Deploy = serving-patterns only" → Consider deployment-strategies and monitoring too
- "They mentioned [tool], route based on tool" → Route by CONCERN, not tool
- "MLOps = one skill" → Could span experiment tracking AND automation
- "Skip question to save time" → Clarifying prevents wrong routing

**When in doubt**: Ask ONE clarifying question. 10 seconds of clarification prevents minutes of wrong-skill loading.

---

## Routing Summary Table

| User Concern | Ask Clarifying | Route To | Also Consider |
|--------------|----------------|----------|---------------|
| Model slow/large | Inference or training? | Optimization skills | If inference, check serving too |
| Deploy model | Target (cloud/edge/batch)? | Serving patterns | Deployment strategies for gradual rollout |
| Production monitoring | Proactive or reactive? | Monitoring OR debugging | Both if setting up + fixing issues |
| MLOps setup | Tracking or automation? | Experiment tracking AND/OR automation | Often both needed |
| Performance issues | Speed or accuracy? | Optimization OR observability | Depends on clarification |
| Scale serving | Traffic pattern? | Scaling-and-load-balancing | Serving patterns if not set up yet |

---

## Integration Examples

### Example 1: Full Production Pipeline

**Query**: "I trained a model, now I need to put it in production"

**Routing**:
1. Ask: "What's your deployment target and are there performance concerns?"
2. If "cloud deployment, model is fast enough":
   - [model-serving-patterns.md](model-serving-patterns.md) (expose as API)
   - [deployment-strategies.md](deployment-strategies.md) (if gradual rollout needed)
   - [production-monitoring-and-alerting.md](production-monitoring-and-alerting.md) (set up observability)
3. If "edge device, model too large":
   - [quantization-for-inference.md](quantization-for-inference.md) (reduce size first)
   - [model-serving-patterns.md](model-serving-patterns.md) (edge deployment pattern)
   - [production-monitoring-and-alerting.md](production-monitoring-and-alerting.md) (if possible on edge)

### Example 2: Optimization Decision

**Query**: "My inference is slow"

**Routing**:
1. Ask: "Have you profiled to find the bottleneck - is it the model or serving infrastructure?"
2. If "not profiled yet":
   - [production-debugging-techniques.md](production-debugging-techniques.md) (profile first to diagnose)
   - Then route based on findings
3. If "model is bottleneck":
   - [hardware-optimization-strategies.md](hardware-optimization-strategies.md) (check if hardware tuning helps)
   - If not enough → [quantization-for-inference.md](quantization-for-inference.md) or [model-compression-techniques.md](model-compression-techniques.md)
4. If "infrastructure/batching is bottleneck":
   - [model-serving-patterns.md](model-serving-patterns.md) (batching strategies)
   - [scaling-and-load-balancing.md](scaling-and-load-balancing.md) (if traffic-related)

### Example 3: MLOps Maturity

**Query**: "We need better ML workflows"

**Routing**:
1. Ask: "What's the current pain point - can't reproduce experiments, manual deployment, or both?"
2. If "can't reproduce, need to track experiments":
   - [experiment-tracking-and-versioning.md](experiment-tracking-and-versioning.md)
3. If "manual deployment is slow":
   - [mlops-pipeline-automation.md](mlops-pipeline-automation.md)
4. If "both reproducibility and automation":
   - [experiment-tracking-and-versioning.md](experiment-tracking-and-versioning.md) (establish tracking first)
   - [mlops-pipeline-automation.md](mlops-pipeline-automation.md) (then automate workflow)

---

## When NOT to Use ml-production Skills

**Skip ml-production when:**
- Still designing/training model → Use neural-architectures, training-optimization
- PyTorch infrastructure issues → Use pytorch-engineering
- LLM-specific optimization only → Use llm-specialist (unless also need serving)
- Classical ML deployment → ml-production still applies but consider if gradient boosting/sklearn instead

**Red flag**: If model isn't trained yet, probably don't need ml-production. Finish training first.

---

## Success Criteria

You've routed correctly when:
- ✅ Identified concern category (optimization, serving, MLOps, observability)
- ✅ Asked clarifying question for ambiguous queries
- ✅ Routed to appropriate skill(s) in logical order
- ✅ Didn't let tool choices (Kubernetes, TorchServe) dictate routing
- ✅ Recognized multi-concern scenarios and routed to multiple skills

---

## ML Production Specialist Skills Catalog

After routing, load the appropriate specialist skill for detailed guidance:

1. [quantization-for-inference.md](quantization-for-inference.md) - INT8/INT4 quantization, post-training quantization, quantization-aware training, precision reduction for inference speed
2. [model-compression-techniques.md](model-compression-techniques.md) - Pruning (structured/unstructured), knowledge distillation, architecture optimization, model size reduction
3. [hardware-optimization-strategies.md](hardware-optimization-strategies.md) - GPU/CPU/edge tuning, batch sizing, memory optimization, hardware-specific acceleration (TensorRT, ONNX Runtime)
4. [model-serving-patterns.md](model-serving-patterns.md) - FastAPI, TorchServe, gRPC, ONNX, batching strategies, containerization (Docker), REST/gRPC APIs
5. [deployment-strategies.md](deployment-strategies.md) - A/B testing, canary deployment, shadow mode, gradual rollout, rollback procedures, blue-green deployment
6. [scaling-and-load-balancing.md](scaling-and-load-balancing.md) - Horizontal scaling, autoscaling, load balancing, traffic management, cost optimization, replica management
7. [experiment-tracking-and-versioning.md](experiment-tracking-and-versioning.md) - MLflow, Weights & Biases, model registries, experiment reproducibility, model lineage, versioning
8. [mlops-pipeline-automation.md](mlops-pipeline-automation.md) - CI/CD for ML, feature stores, data validation, automated retraining, orchestration (Airflow, Kubeflow)
9. [production-monitoring-and-alerting.md](production-monitoring-and-alerting.md) - Metrics tracking, drift detection, dashboards, alerting, SLAs, proactive monitoring
10. [production-debugging-techniques.md](production-debugging-techniques.md) - Error analysis, production profiling, rollback procedures, post-mortems, root cause analysis

---

## References

- See design doc: `docs/plans/2025-10-30-ml-production-pack-design.md`
- Primary router: `yzmir/ai-engineering-expert/using-ai-engineering`
- Related packs: `llm-specialist/using-llm-specialist`, `training-optimization/using-training-optimization`
