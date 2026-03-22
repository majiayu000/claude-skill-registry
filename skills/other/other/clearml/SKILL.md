---
name: clearml
description: Expert guidance for ClearML, the open-source MLOps platform for experiment tracking, pipeline orchestration, data management, and model deployment. Helps developers set up ML experiment tracking with minimal code, build reproducible pipelines, and manage the full ML lifecycle from training to serving.
license: Apache-2.0
compatibility: No special requirements
metadata:
  author: terminal-skills
  version: 1.0.0
  category: data-ai
  tags:
  - ml-ops
  - experiment-tracking
  - pipeline
  - orchestration
  - data-management
---

# ClearML — Open-Source ML Operations


## Overview


ClearML, the open-source MLOps platform for experiment tracking, pipeline orchestration, data management, and model deployment. Helps developers set up ML experiment tracking with minimal code, build reproducible pipelines, and manage the full ML lifecycle from training to serving.


## Instructions

### Experiment Tracking (Two Lines of Code)

```python
# train.py — Automatic experiment tracking
from clearml import Task

# Just these two lines auto-capture everything:
# - Git repo, branch, and diff
# - All installed packages
# - CLI arguments
# - stdout/stderr
# - Framework metrics (PyTorch, TensorFlow, scikit-learn)
task = Task.init(project_name="NLP", task_name="sentiment-classifier-v2")

# All print statements, matplotlib plots, and framework metrics
# are automatically captured — zero additional code needed

import torch
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments

model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=3)

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=32,
    learning_rate=2e-5,
    evaluation_strategy="epoch",
    logging_steps=50,
    # ClearML auto-captures all these parameters
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

# Training metrics automatically logged to ClearML dashboard
trainer.train()

# Explicitly log additional data
task.get_logger().report_scalar("custom", "metric", value=0.95, iteration=100)
task.upload_artifact("model_weights", artifact_object="./results/pytorch_model.bin")
```

### Pipeline Orchestration

```python
# pipeline.py — ML pipeline with ClearML
from clearml import PipelineController

pipe = PipelineController(
    name="Training Pipeline",
    project="NLP",
    version="1.0",
)

# Step 1: Data preprocessing
pipe.add_step(
    name="preprocess",
    base_task_project="NLP",
    base_task_name="data-preprocess",       # Reference an existing task template
    parameter_override={
        "General/dataset_version": "v2.1",
        "General/max_samples": 50000,
    },
)

# Step 2: Training (depends on preprocessing)
pipe.add_step(
    name="train",
    parents=["preprocess"],
    base_task_project="NLP",
    base_task_name="train-model",
    parameter_override={
        "General/epochs": 5,
        "General/learning_rate": "${preprocess.learning_rate}",  # Reference parent output
    },
)

# Step 3: Evaluation
pipe.add_step(
    name="evaluate",
    parents=["train"],
    base_task_project="NLP",
    base_task_name="evaluate-model",
)

# Step 4: Deploy if metrics meet threshold
pipe.add_step(
    name="deploy",
    parents=["evaluate"],
    base_task_project="NLP",
    base_task_name="deploy-model",
    pre_execute_callback=lambda pipeline, node, params: {
        # Only deploy if accuracy > 0.9
        pipeline.get_step("evaluate").get_metric("accuracy") > 0.9
    },
)

# Run the pipeline
pipe.start()
```

### Data Management

```python
# data_versioning.py — Version and manage datasets
from clearml import Dataset

# Create a versioned dataset
dataset = Dataset.create(
    dataset_name="customer-reviews-v2",
    dataset_project="NLP",
    description="Customer reviews with sentiment labels, cleaned and deduplicated",
)

# Add files
dataset.add_files(path="./data/reviews.parquet")
dataset.add_files(path="./data/labels.csv")

# Upload and finalize (creates immutable version)
dataset.upload()
dataset.finalize()
print(f"Dataset ID: {dataset.id}")

# Use the dataset in training
dataset = Dataset.get(
    dataset_name="customer-reviews-v2",
    dataset_project="NLP",
)
local_path = dataset.get_local_copy()    # Downloads and caches locally
# local_path now points to a directory with reviews.parquet and labels.csv

# Create a new version (inherits from parent)
new_version = Dataset.create(
    dataset_name="customer-reviews-v3",
    dataset_project="NLP",
    parent_datasets=[dataset.id],         # Inherits files from v2
)
new_version.add_files("./data/new_reviews.parquet")  # Add new data
new_version.remove_files("data/old_labels.csv")      # Remove outdated files
new_version.upload()
new_version.finalize()
```

### Remote Execution (ClearML Agent)

```python
# Run any task on remote machines with ClearML Agent
from clearml import Task

task = Task.init(project_name="NLP", task_name="train-large-model")

# This task was created locally, but we can clone and run it remotely
task.execute_remotely(queue_name="gpu-queue")

# Everything after this line runs on the remote machine
# ClearML Agent handles:
# - Setting up the environment (pip install, git clone)
# - Downloading datasets
# - Running the code
# - Uploading results and artifacts
```

```bash
# Start a ClearML Agent on a GPU machine
clearml-agent daemon --queue gpu-queue --gpus 0

# Or with Docker isolation
clearml-agent daemon --queue gpu-queue --docker --gpus all
```

### Hyperparameter Optimization

```python
# hpo.py — Automated hyperparameter search
from clearml import Task
from clearml.automation import HyperParameterOptimizer, UniformParameterRange, DiscreteParameterRange

optimizer = HyperParameterOptimizer(
    base_task_id="<template-task-id>",     # Task to optimize
    hyper_parameters=[
        UniformParameterRange("General/learning_rate", min_value=1e-5, max_value=1e-3),
        UniformParameterRange("General/weight_decay", min_value=0, max_value=0.1),
        DiscreteParameterRange("General/batch_size", values=[16, 32, 64]),
        DiscreteParameterRange("General/epochs", values=[3, 5, 10]),
    ],
    objective_metric_title="eval",
    objective_metric_series="f1",
    objective_metric_sign="max",            # Maximize F1 score
    max_number_of_concurrent_tasks=4,
    optimizer_class="OptimizerBOHB",        # Bayesian optimization
    execution_queue="gpu-queue",
    total_max_jobs=50,
)

optimizer.start()
optimizer.wait()

# Get the best configuration
best = optimizer.get_top_experiments(top_k=1)[0]
print(f"Best F1: {best.get_metric('eval', 'f1')}")
print(f"Best params: {best.get_parameters()}")
```

## Installation

```bash
# Python SDK
pip install clearml

# Configure (interactive — sets API credentials)
clearml-init

# Self-hosted server (Docker Compose)
docker compose -f docker-compose.yml up -d
# Dashboard at http://localhost:8080

# Or use ClearML Cloud (free tier available)
# https://app.clear.ml
```


## Examples


### Example 1: Setting up an evaluation pipeline for a RAG application

**User request:**

```
I have a RAG chatbot that answers questions from our docs. Set up Clearml to evaluate answer quality.
```

The agent creates an evaluation suite with appropriate metrics (faithfulness, relevance, answer correctness), configures test datasets from real user questions, runs baseline evaluations, and sets up CI integration so evaluations run on every prompt or retrieval change.

### Example 2: Comparing model performance across prompts

**User request:**

```
We're testing GPT-4o vs Claude on our customer support prompts. Set up a comparison with Clearml.
```

The agent creates a structured experiment with the existing prompt set, configures both model providers, defines scoring criteria specific to customer support (accuracy, tone, completeness), runs the comparison, and generates a summary report with statistical significance indicators.


## Guidelines

1. **Two lines to start** — `Task.init()` auto-captures everything; add explicit logging only for custom metrics
2. **Use dataset versioning** — Version your training data alongside code; reproducibility requires both
3. **Remote execution for GPU work** — Develop locally, run on GPU machines with `execute_remotely()`; no SSH needed
4. **Pipeline for reproducibility** — Define training pipelines as code; each run is fully reproducible with tracked inputs/outputs
5. **Queue-based execution** — Use queues to route tasks to appropriate hardware (CPU queue, GPU queue, high-memory queue)
6. **HPO with Bayesian optimization** — Use BOHB optimizer for efficient hyperparameter search; better than grid/random search
7. **Self-host for privacy** — Run the ClearML server on your own infrastructure; all data stays in your network
8. **Compare experiments in dashboard** — Use the web UI to overlay training curves, compare hyperparameters, and identify winners
