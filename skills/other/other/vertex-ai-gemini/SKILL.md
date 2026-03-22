---
name: vertex-ai-gemini
description: >-
  Google Cloud Vertex AI for enterprise Gemini deployments — production scaling,
  fine-tuning, and MLOps. Use when deploying Gemini in GCP-native environments,
  running fine-tuning jobs, needing enterprise IAM controls, VPC isolation,
  batch prediction at scale, or production ML pipelines on Google Cloud.
license: Apache-2.0
compatibility: "Python 3.9+ with google-cloud-aiplatform SDK and GCP credentials"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: data-ai
  tags: ["vertex-ai", "google-cloud", "gemini", "enterprise", "mlops"]
  use-cases:
    - "Deploy Gemini with enterprise IAM, VPC controls, and compliance requirements"
    - "Fine-tune Gemini on proprietary data for domain-specific use cases"
    - "Run batch predictions on millions of records with managed infrastructure"
  agents: [claude-code, openai-codex, gemini-cli, cursor]
---

# Vertex AI — Gemini on Google Cloud

## Overview

Vertex AI is Google Cloud's enterprise ML platform. It provides access to the same Gemini models as Google AI Studio, but with enterprise-grade features: IAM-based auth (no API keys), VPC Service Controls for data isolation, audit logging, fine-tuning capabilities, batch prediction jobs, and integration with GCP data services like BigQuery and Cloud Storage.

## Vertex AI vs Google AI Studio

| Feature | Google AI Studio | Vertex AI |
|---|---|---|
| Auth | API Key | Service Account / IAM |
| Data residency | Limited | GCP regions |
| VPC isolation | ❌ | ✅ |
| Audit logging | ❌ | ✅ Cloud Audit Logs |
| Fine-tuning | ❌ | ✅ |
| Batch prediction | ❌ | ✅ |
| Pricing | Per token | Per token (different rates) |
| Quotas | Shared | Project-level quotas |

## Setup

```bash
pip install google-cloud-aiplatform
```

```bash
# Authenticate
gcloud auth application-default login

# Or use service account
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

```bash
# Set project and location
export GOOGLE_CLOUD_PROJECT=my-project-id
export GOOGLE_CLOUD_LOCATION=us-central1
```

## Instructions

### Basic Gemini Inference

```python
import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="my-project-id", location="us-central1")

model = GenerativeModel("gemini-2.0-flash-001")
response = model.generate_content("Explain containerization in simple terms.")
print(response.text)
```

### Multi-Modal Inference

```python
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import base64

vertexai.init(project="my-project-id", location="us-central1")
model = GenerativeModel("gemini-2.0-flash-001")

# Analyze image from Cloud Storage
gcs_image = Part.from_uri(
    uri="gs://my-bucket/product-photo.jpg",
    mime_type="image/jpeg",
)
response = model.generate_content(["Describe this product:", gcs_image])
print(response.text)

# Analyze local image
with open("chart.png", "rb") as f:
    image_data = f.read()

local_image = Part.from_data(data=image_data, mime_type="image/png")
response = model.generate_content(["What trends does this chart show?", local_image])
print(response.text)
```

### Streaming Responses

```python
import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="my-project-id", location="us-central1")
model = GenerativeModel("gemini-2.0-flash-001")

for chunk in model.generate_content("Write a product description for a smartwatch.", stream=True):
    print(chunk.text, end="", flush=True)
print()
```

### Chat Session

```python
import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession

vertexai.init(project="my-project-id", location="us-central1")

model = GenerativeModel(
    model_name="gemini-2.0-flash-001",
    system_instruction="You are a GCP expert. Provide concise, actionable answers.",
)

chat = model.start_chat()
print(chat.send_message("How do I set up Cloud Run?").text)
print(chat.send_message("What about environment variables?").text)
```

### Function Calling

```python
import vertexai
from vertexai.generative_models import (
    FunctionDeclaration,
    GenerativeModel,
    Tool,
)

vertexai.init(project="my-project-id", location="us-central1")

get_bq_query = FunctionDeclaration(
    name="run_bigquery_query",
    description="Run a SQL query on BigQuery and return results",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "SQL query to execute"},
            "dataset": {"type": "string", "description": "BigQuery dataset name"},
        },
        "required": ["query"],
    },
)

tool = Tool(function_declarations=[get_bq_query])
model = GenerativeModel("gemini-2.0-flash-001", tools=[tool])

response = model.generate_content("How many users signed up last week?")

if response.candidates[0].function_calls:
    fc = response.candidates[0].function_calls[0]
    print(f"Function: {fc.name}, Args: {dict(fc.args)}")
```

### Fine-Tuning Gemini

```python
import vertexai
from vertexai.tuning import sft

vertexai.init(project="my-project-id", location="us-central1")

# Prepare training data in JSONL format in GCS:
# {"messages": [{"role": "user", "content": "..."}, {"role": "model", "content": "..."}]}

tuning_job = sft.train(
    source_model="gemini-2.0-flash-001",
    train_dataset="gs://my-bucket/training-data.jsonl",
    validation_dataset="gs://my-bucket/validation-data.jsonl",
    tuned_model_display_name="my-fine-tuned-gemini",
    epochs=3,
    learning_rate_multiplier=1.0,
)

print(f"Tuning job: {tuning_job.resource_name}")
print(f"State: {tuning_job.state}")

# Wait for completion
tuning_job.wait()
print(f"Tuned model: {tuning_job.tuned_model_name}")
```

### Batch Prediction

```python
import vertexai
from vertexai.generative_models import GenerativeModel
from vertexai.preview.batch_prediction import BatchPredictionJob

vertexai.init(project="my-project-id", location="us-central1")

# Input JSONL format in GCS:
# {"request": {"contents": [{"role": "user", "parts": [{"text": "Translate: Hello"}]}]}}

job = BatchPredictionJob.submit(
    source_model="gemini-2.0-flash-001",
    input_dataset="gs://my-bucket/batch-inputs.jsonl",
    output_uri_prefix="gs://my-bucket/batch-outputs/",
)

print(f"Batch job: {job.resource_name}")
job.wait()
print(f"Output: {job.output_location}")
```

### IAM Setup for Service Account

```bash
# Create a service account for your app
gcloud iam service-accounts create gemini-app-sa \
    --display-name="Gemini App Service Account"

# Grant Vertex AI User role
gcloud projects add-iam-policy-binding my-project-id \
    --member="serviceAccount:gemini-app-sa@my-project-id.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Download key (for non-GCP environments)
gcloud iam service-accounts keys create key.json \
    --iam-account=gemini-app-sa@my-project-id.iam.gserviceaccount.com
```

### VPC Service Controls (Enterprise Isolation)

```python
# When VPC SC is enabled, all API calls must originate from within the perimeter
# Configure the SDK to use private endpoints:

import vertexai

vertexai.init(
    project="my-project-id",
    location="us-central1",
    api_endpoint="us-central1-aiplatform.googleapis.com",  # Regional endpoint
)
```

### Available Gemini Models on Vertex AI

| Model ID | Notes |
|---|---|
| `gemini-2.0-flash-001` | Latest Flash, fast + capable |
| `gemini-1.5-pro-002` | 2M context, most capable |
| `gemini-1.5-flash-002` | 1M context, balanced |
| `text-embedding-005` | Latest embeddings (768 dims) |

Use `gemini-2.0-flash-001` (version pinned) in production to avoid unexpected model changes.

## Guidelines

- Always pin model versions (e.g., `gemini-2.0-flash-001` not `gemini-2.0-flash`) in production for stability.
- Use Application Default Credentials (`gcloud auth application-default login`) during development.
- In GKE or Cloud Run, use Workload Identity — no service account keys needed.
- Fine-tuning requires a training JSONL with `messages` format and at least 100 examples.
- Batch prediction is cost-effective for offline bulk inference (no streaming).
- Enable Cloud Audit Logs on the `aiplatform.googleapis.com` service for compliance.
- Vertex AI supports regional endpoints — choose a region to ensure data residency compliance.
