---
name: mlops-basics
version: "2.0.0"
sasmp_version: "1.3.0"
description: Master MLOps fundamentals - lifecycle, principles, tools, practices, and organizational adoption
bonded_agent: 01-mlops-fundamentals
bond_type: PRIMARY_BOND

# SKILL METADATA
category: fundamentals
difficulty: beginner_to_intermediate
estimated_hours: 40
prerequisites: []

# VALIDATION
validation:
  pre_conditions:
    - "Basic understanding of ML concepts"
    - "Familiarity with version control (Git)"
  post_conditions:
    - "Can explain MLOps lifecycle phases"
    - "Can assess organizational MLOps maturity"
    - "Can recommend tooling strategy"
  parameter_schema:
    learning_path:
      type: string
      enum: [quick_start, comprehensive, enterprise_focused]
    focus_area:
      type: string
      enum: [lifecycle, tools, practices, all]

# RETRY LOGIC
retry:
  max_attempts: 3
  backoff_type: exponential
  initial_delay_ms: 500

# OBSERVABILITY
observability:
  log_inputs: true
  log_outputs: true
  metrics:
    - skill_completion_rate
    - exercise_success_rate
    - time_to_completion
---

# MLOps Basics Skill

> **Learn**: Master the foundations of Machine Learning Operations for production ML systems.

## Skill Overview

| Attribute | Value |
|-----------|-------|
| **Bonded Agent** | 01-mlops-fundamentals |
| **Difficulty** | Beginner to Intermediate |
| **Duration** | 40 hours |
| **Prerequisites** | Basic ML concepts, Git |

---

## Learning Objectives

After completing this skill, you will be able to:

1. **Explain** the complete ML lifecycle from data to production
2. **Assess** organizational MLOps maturity levels (0-4)
3. **Compare** and select appropriate MLOps tools
4. **Design** basic ML pipelines following best practices
5. **Implement** foundational MLOps practices in your team

---

## Topics Covered

### Module 1: ML Lifecycle Fundamentals (8 hours)

```
┌─────────────────────────────────────────────────────────────────┐
│                     ML LIFECYCLE PHASES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐     │
│  │   Data   │──▶│  Model   │──▶│  Deploy  │──▶│ Monitor  │     │
│  │Collection│   │ Training │   │          │   │          │     │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘     │
│       │                                              │          │
│       └──────────── Feedback Loop ◀──────────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Topics:**
- Data Engineering vs Data Science vs ML Engineering
- Feature Engineering lifecycle
- Model training and evaluation
- Deployment patterns
- Continuous monitoring and retraining

**Exercises:**
- [ ] Map an existing ML project to lifecycle phases
- [ ] Identify gaps in current workflow
- [ ] Create lifecycle documentation template

---

### Module 2: MLOps Principles (8 hours)

**Core Principles (2024-2025 Best Practices):**

| Principle | Description | Implementation |
|-----------|-------------|----------------|
| **Automation** | Reduce manual intervention | CI/CD pipelines, auto-retraining |
| **Reproducibility** | Same inputs → same outputs | Version everything, seed randomness |
| **Testing** | Validate at every stage | Data tests, model tests, integration tests |
| **Monitoring** | Observe production behavior | Drift detection, performance metrics |
| **Iteration** | Continuous improvement | Feedback loops, experimentation |

**Exercises:**
- [ ] Audit current project against principles
- [ ] Create reproducibility checklist
- [ ] Design testing strategy

---

### Module 3: Tool Ecosystem (12 hours)

**Tool Categories & Recommendations:**

```python
MLOPS_TOOLS = {
    "experiment_tracking": {
        "open_source": ["MLflow", "DVC"],
        "managed": ["Weights & Biases", "Neptune", "Comet"]
    },
    "feature_stores": {
        "open_source": ["Feast"],
        "managed": ["Tecton", "Hopsworks", "Vertex Feature Store"]
    },
    "orchestration": {
        "open_source": ["Airflow", "Prefect", "Dagster"],
        "managed": ["Kubeflow", "Vertex Pipelines", "SageMaker Pipelines"]
    },
    "model_serving": {
        "open_source": ["TorchServe", "BentoML", "Seldon"],
        "managed": ["Triton", "SageMaker Endpoints", "Vertex Endpoints"]
    },
    "monitoring": {
        "open_source": ["Evidently", "NannyML"],
        "managed": ["WhyLabs", "Arize", "Fiddler"]
    }
}
```

**Exercises:**
- [ ] Install and configure MLflow locally
- [ ] Track an experiment with parameters and metrics
- [ ] Register a model in the model registry

---

### Module 4: Best Practices & Patterns (12 hours)

**Design Patterns:**

1. **Training Pipeline Pattern**
   ```
   Data → Validate → Transform → Train → Evaluate → Register
   ```

2. **Serving Pipeline Pattern**
   ```
   Request → Preprocess → Predict → Postprocess → Response
   ```

3. **Monitoring Pattern**
   ```
   Production Data → Compare vs Reference → Detect Drift → Alert/Retrain
   ```

**Exercises:**
- [ ] Design a training pipeline for a sample project
- [ ] Implement basic data validation with Great Expectations
- [ ] Set up a simple monitoring dashboard

---

## Code Templates

### Template 1: MLflow Experiment Setup

```python
# templates/mlflow_setup.py
import mlflow
from mlflow.tracking import MlflowClient

def setup_experiment(
    experiment_name: str,
    tracking_uri: str = "sqlite:///mlflow.db"
) -> str:
    """Initialize MLflow experiment with best practices."""
    mlflow.set_tracking_uri(tracking_uri)

    # Create or get experiment
    client = MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)

    if experiment is None:
        experiment_id = client.create_experiment(
            name=experiment_name,
            tags={"version": "1.0", "team": "ml-platform"}
        )
    else:
        experiment_id = experiment.experiment_id

    mlflow.set_experiment(experiment_name)
    return experiment_id


def log_run(params: dict, metrics: dict, model_path: str):
    """Log a complete training run."""
    with mlflow.start_run():
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)
        mlflow.log_artifact(model_path)
```

### Template 2: MLOps Maturity Assessment

```python
# templates/maturity_assessment.py
from dataclasses import dataclass
from enum import IntEnum
from typing import List

class MaturityLevel(IntEnum):
    AD_HOC = 0
    REPEATABLE = 1
    RELIABLE = 2
    SCALABLE = 3
    OPTIMIZED = 4

@dataclass
class AssessmentQuestion:
    dimension: str
    question: str
    level_0: str
    level_1: str
    level_2: str
    level_3: str
    level_4: str

ASSESSMENT_QUESTIONS = [
    AssessmentQuestion(
        dimension="Data Management",
        question="How do you manage training data?",
        level_0="Ad-hoc file storage",
        level_1="Versioned with DVC/Git LFS",
        level_2="Data validation in place",
        level_3="Feature store implemented",
        level_4="Automated data quality monitoring"
    ),
    # Add more questions for each dimension
]

def calculate_maturity_score(responses: List[int]) -> tuple:
    """Calculate overall maturity score."""
    avg_score = sum(responses) / len(responses)
    level = MaturityLevel(int(avg_score))
    return avg_score, level
```

---

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| MLflow UI not loading | Connection refused | Check tracking URI, start server |
| Experiment not found | Experiment doesn't exist | Verify experiment name, create if needed |
| Artifact upload fails | Storage permission denied | Check artifact location permissions |
| Model registration fails | Model name conflict | Use unique names or versioning |

### Debug Checklist

```
□ 1. Verify MLflow server is running
□ 2. Check tracking URI configuration
□ 3. Confirm artifact storage accessible
□ 4. Validate experiment exists
□ 5. Test with minimal example first
```

---

## Knowledge Check

### Self-Assessment Questions

1. What are the 5 main phases of the ML lifecycle?
2. How does MLOps differ from DevOps?
3. When would you use MLflow vs Weights & Biases?
4. What's the difference between Level 1 and Level 2 MLOps maturity?
5. What should you version in an ML project?

### Practical Exercises

1. **Beginner**: Set up MLflow tracking for an existing notebook
2. **Intermediate**: Create a reproducible training script with environment capture
3. **Advanced**: Design an end-to-end pipeline diagram for a real use case

---

## Resources

### Official Documentation
- [MLflow Documentation](https://mlflow.org/docs/latest/)
- [Google MLOps Guide](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)

### Recommended Reading
- "Designing Machine Learning Systems" by Chip Huyen
- "Machine Learning Engineering" by Andriy Burkov

### Related Skills
- [See: experiment-tracking] - Deep dive into experiment tracking
- [See: training-pipelines] - Build production training pipelines
- [See: ml-infrastructure] - Set up ML infrastructure

---

## Skill Completion Criteria

To mark this skill as complete, you must:

- [ ] Complete all 4 modules
- [ ] Finish at least 80% of exercises
- [ ] Pass the knowledge check (4/5 correct)
- [ ] Complete one practical project

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2024-12 | Production-grade upgrade with exercises and templates |
| 1.0.0 | 2024-11 | Initial release |
