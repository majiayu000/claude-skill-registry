---
name: modal
description: Guide for building serverless Python applications on Modal - a cloud platform for running AI/ML workloads, GPU-accelerated code, web endpoints, scheduled jobs, and batch processing with minimal configuration. Use when deploying Python code to Modal's infrastructure, running GPU inference, creating web APIs, processing data at scale, or building AI applications.
license: Complete terms in LICENSE.txt
---

# Modal Development Guide

## Overview

Modal is a serverless cloud platform for running Python code with minimal configuration. It excels at:

- **GPU-accelerated AI/ML inference** (supports T4, L4, A10, A100, L40S, H100, H200, B200)
- **Serverless web APIs and endpoints**
- **Scheduled jobs (cron)**
- **High-performance batch processing**
- **Sandboxed code execution**

Key benefits:
- Pay only for resources used (billed per second)
- Containers spin up in seconds
- No infrastructure management required
- Built-in autoscaling from zero to thousands of containers

---

# Quick Start

## Installation & Setup

```bash
pip install modal
modal setup  # Authenticate with Modal
```

## Basic App Structure

```python
import modal

# Create an App (groups Functions for deployment)
app = modal.App("my-app")

# Define a container image with dependencies
image = modal.Image.debian_slim(python_version="3.12").pip_install("numpy", "pandas")

# Create a serverless function
@app.function(image=image)
def process_data(x: int) -> int:
    import numpy as np
    return int(np.square(x))

# Local entrypoint for running the app
@app.local_entrypoint()
def main():
    result = process_data.remote(5)
    print(f"Result: {result}")
```

## Running Your App

```bash
# Run ephemeral (for development/testing)
modal run my_app.py

# Deploy persistently
modal deploy my_app.py

# Serve with hot-reload (for web endpoints)
modal serve my_app.py
```

---

# Core Concepts

## Apps and Functions

An **App** groups related Functions for atomic deployment. A **Function** is an independent unit that scales up/down automatically.

```python
import modal

app = modal.App("my-app")

@app.function()
def hello(name: str) -> str:
    return f"Hello, {name}!"

@app.function()
def goodbye(name: str) -> str:
    return f"Goodbye, {name}!"
```

## Container Images

Define custom environments using method chaining:

```python
image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("git", "ffmpeg")              # System packages
    .pip_install("torch", "transformers")       # Python packages (pip)
    .uv_pip_install("numpy", "pandas")          # Python packages (uv - faster)
    .env({"MY_VAR": "value"})                   # Environment variables
    .run_commands("echo 'setup complete'")      # Shell commands
    .add_local_python_source("my_module")       # Local Python code
)

@app.function(image=image)
def my_function():
    ...
```

### Using Existing Images

```python
# From Docker registry
image = modal.Image.from_registry("pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime")

# From Dockerfile
image = modal.Image.from_dockerfile("./Dockerfile")

# From NVIDIA CUDA
image = modal.Image.from_registry("nvidia/cuda:12.8.1-devel-ubuntu24.04", add_python="3.12")
```

### Handling Remote-Only Imports

When packages exist only in the container:

```python
image = modal.Image.debian_slim().pip_install("pandas")

# Option 1: Import inside function body
@app.function(image=image)
def my_function():
    import pandas as pd  # Import inside function
    return pd.DataFrame()

# Option 2: Use Image.imports() context manager
with image.imports():
    import pandas as pd
    import numpy as np

@app.function(image=image)
def my_function():
    return pd.DataFrame()
```

---

# GPU Acceleration

## Requesting GPUs

```python
# Single GPU
@app.function(gpu="A100")
def train_model():
    import torch
    assert torch.cuda.is_available()
    ...

# Multiple GPUs (same machine)
@app.function(gpu="H100:8")
def train_large_model():
    ...

# GPU fallbacks (tries in order)
@app.function(gpu=["H100", "A100-80GB", "A100-40GB"])
def flexible_inference():
    ...
```

## Available GPU Types

| GPU | Memory | Best For |
|-----|--------|----------|
| `T4` | 16 GB | Budget inference |
| `L4` | 24 GB | Inference |
| `A10` | 24 GB | Inference (up to 4x) |
| `A100-40GB` | 40 GB | Training/Inference |
| `A100-80GB` | 80 GB | Large models |
| `L40S` | 48 GB | Best cost/performance |
| `H100` | 80 GB | High-performance training |
| `H200` | 141 GB | Large models |
| `B200` | 192 GB | Largest models |

## GPU Image Setup

For libraries requiring CUDA toolkit:

```python
image = (
    modal.Image.from_registry("nvidia/cuda:12.8.1-devel-ubuntu24.04", add_python="3.12")
    .entrypoint([])
    .pip_install("torch", "transformers")
)

@app.function(gpu="A100", image=image)
def gpu_function():
    ...
```

---

# Web Endpoints

## FastAPI Endpoints

```python
from fastapi import FastAPI
import modal

image = modal.Image.debian_slim().pip_install("fastapi[standard]")
app = modal.App("web-app", image=image)

@app.function()
@modal.fastapi_endpoint()
def hello(name: str = "World") -> dict:
    return {"message": f"Hello, {name}!"}

# With custom configuration
@app.function()
@modal.fastapi_endpoint(method="POST", docs=True)
def process(data: dict) -> dict:
    return {"processed": data}
```

## Full ASGI/WSGI Apps

```python
# ASGI (FastAPI, Starlette)
@app.function()
@modal.asgi_app()
def fastapi_app():
    from fastapi import FastAPI
    web_app = FastAPI()
    
    @web_app.get("/")
    def root():
        return {"status": "ok"}
    
    return web_app

# WSGI (Flask, Django)
@app.function()
@modal.wsgi_app()
def flask_app():
    from flask import Flask
    web_app = Flask(__name__)
    
    @web_app.route("/")
    def root():
        return {"status": "ok"}
    
    return web_app
```

## Web Server (Custom Ports)

```python
@app.function()
@modal.web_server(port=8080)
def custom_server():
    import subprocess
    subprocess.run(["python", "-m", "http.server", "8080"])
```

## Custom Domains

```python
@app.function()
@modal.fastapi_endpoint(custom_domains=["api.example.com"])
def my_api():
    return {"message": "Hello from custom domain!"}
```

---

# Persistent Storage

## Volumes (High-Performance Storage)

```python
# Create or reference a Volume
volume = modal.Volume.from_name("my-volume", create_if_missing=True)

@app.function(volumes={"/data": volume})
def save_data():
    with open("/data/output.txt", "w") as f:
        f.write("Hello, Volume!")

@app.function(volumes={"/data": volume})
def read_data():
    with open("/data/output.txt", "r") as f:
        return f.read()
```

### Volume Operations

```python
# Upload files
with volume.batch_upload() as batch:
    batch.put_file("local.txt", "/remote.txt")
    batch.put_directory("./local_dir", "/remote_dir")

# Read files
for chunk in volume.read_file("output.txt"):
    print(chunk)

# List contents
for entry in volume.listdir("/"):
    print(entry)
```

## Cloud Bucket Mounts

```python
bucket_mount = modal.CloudBucketMount(
    bucket_name="my-s3-bucket",
    secret=modal.Secret.from_name("aws-secret"),
)

@app.function(volumes={"/s3": bucket_mount})
def process_s3_data():
    import os
    files = os.listdir("/s3")
    ...
```

---

# Secrets Management

## Creating Secrets

```python
# From Modal dashboard (recommended for production)
secret = modal.Secret.from_name("my-secret")

# From dictionary (inline)
secret = modal.Secret.from_dict({"API_KEY": "xxx", "DB_PASSWORD": "yyy"})

# From .env file
secret = modal.Secret.from_dotenv()
```

## Using Secrets

```python
@app.function(secrets=[modal.Secret.from_name("openai-secret")])
def call_openai():
    import os
    api_key = os.environ["OPENAI_API_KEY"]
    ...
```

---

# Scheduling (Cron Jobs)

```python
# Run every hour
@app.function(schedule=modal.Period(hours=1))
def hourly_task():
    print("Running hourly task")

# Run daily at specific time
@app.function(schedule=modal.Cron("0 9 * * *"))  # 9 AM UTC daily
def daily_report():
    print("Generating daily report")

# Run every 5 minutes
@app.function(schedule=modal.Period(minutes=5))
def frequent_check():
    print("Checking...")
```

Deploy with `modal deploy` to activate schedules.

---

# Parallel Processing

## Using `.map()` for Batch Processing

```python
@app.function()
def process_item(item: int) -> int:
    return item * 2

@app.local_entrypoint()
def main():
    items = list(range(1000))
    
    # Process all items in parallel
    results = list(process_item.map(items))
    print(f"Processed {len(results)} items")
```

## Using `.starmap()` for Multiple Arguments

```python
@app.function()
def add(x: int, y: int) -> int:
    return x + y

@app.local_entrypoint()
def main():
    pairs = [(1, 2), (3, 4), (5, 6)]
    results = list(add.starmap(pairs))
```

## Fire-and-Forget with `.spawn()`

```python
@app.function()
def background_task(task_id: int):
    # Long-running task
    ...

@app.local_entrypoint()
def main():
    # Spawn without waiting for results
    for i in range(100):
        background_task.spawn(i)
    print("All tasks spawned")
```

---

# Sandboxes (Dynamic Code Execution)

Execute arbitrary code in isolated containers:

```python
import modal

app = modal.App.lookup("sandbox-app", create_if_missing=True)

# Create a sandbox
sb = modal.Sandbox.create(
    image=modal.Image.debian_slim().pip_install("numpy"),
    app=app,
)

# Execute commands
p = sb.exec("python", "-c", "import numpy; print(numpy.__version__)")
print(p.stdout.read())

# Clean up
sb.terminate()
```

## LLM Code Execution

```python
@app.function(
    restrict_modal_access=True,  # Security: restrict Modal API access
    single_use_containers=True,   # Fresh container per request
    timeout=30,
    block_network=True,           # No network access
)
def run_untrusted_code(code: str):
    try:
        exec_globals = {}
        exec(code, exec_globals)
        return exec_globals.get("result")
    except Exception as e:
        return f"Error: {e}"
```

---

# Classes with Lifecycle

Use `@app.cls()` for stateful services with initialization:

```python
@app.cls(gpu="A100", image=image)
class ModelService:
    @modal.enter()
    def load_model(self):
        # Runs once when container starts
        from transformers import pipeline
        self.model = pipeline("text-generation", model="gpt2", device="cuda")
    
    @modal.method()
    def generate(self, prompt: str) -> str:
        return self.model(prompt, max_length=100)[0]["generated_text"]
    
    @modal.exit()
    def cleanup(self):
        # Runs when container shuts down
        del self.model

# Usage
@app.local_entrypoint()
def main():
    service = ModelService()
    result = service.generate.remote("Hello, world!")
    print(result)
```

---

# Resource Configuration

## CPU and Memory

```python
@app.function(
    cpu=4.0,           # 4 CPU cores
    memory=8192,       # 8 GB RAM
)
def heavy_computation():
    ...

# With limits
@app.function(
    cpu=(1.0, 4.0),           # Request 1 core, limit 4
    memory=(2048, 8192),      # Request 2GB, limit 8GB
)
def flexible_function():
    ...
```

## Timeouts and Retries

```python
@app.function(
    timeout=600,              # 10 minute timeout
    retries=modal.Retries(
        max_retries=3,
        initial_delay=1.0,
        backoff_coefficient=2.0,
    ),
)
def reliable_function():
    ...
```

## Container Configuration

```python
@app.function(
    concurrency_limit=10,         # Max containers
    allow_concurrent_inputs=5,    # Inputs per container
    container_idle_timeout=300,   # Keep warm for 5 min
)
def optimized_function():
    ...
```

---

# Common Patterns

## AI Model Inference Service

```python
import modal

app = modal.App("llm-service")

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("vllm", "torch")
)

@app.cls(gpu="A100", image=image, container_idle_timeout=300)
class LLMService:
    @modal.enter()
    def load(self):
        from vllm import LLM
        self.llm = LLM(model="meta-llama/Llama-3.1-8B-Instruct")
    
    @modal.method()
    def generate(self, prompt: str) -> str:
        from vllm import SamplingParams
        params = SamplingParams(temperature=0.7, max_tokens=256)
        outputs = self.llm.generate([prompt], params)
        return outputs[0].outputs[0].text

@app.function()
@modal.fastapi_endpoint(method="POST")
def inference(body: dict) -> dict:
    service = LLMService()
    result = service.generate.remote(body["prompt"])
    return {"response": result}
```

## Data Processing Pipeline

```python
import modal

app = modal.App("data-pipeline")
volume = modal.Volume.from_name("pipeline-data", create_if_missing=True)

image = modal.Image.debian_slim().pip_install("pandas", "pyarrow")

@app.function(image=image, volumes={"/data": volume})
def extract(source: str) -> str:
    import pandas as pd
    df = pd.read_csv(source)
    output_path = f"/data/extracted_{source.split('/')[-1]}"
    df.to_parquet(output_path)
    return output_path

@app.function(image=image, volumes={"/data": volume})
def transform(input_path: str) -> str:
    import pandas as pd
    df = pd.read_parquet(input_path)
    # Transform logic
    df["processed"] = True
    output_path = input_path.replace("extracted", "transformed")
    df.to_parquet(output_path)
    return output_path

@app.function(image=image, volumes={"/data": volume})
def load(input_path: str):
    import pandas as pd
    df = pd.read_parquet(input_path)
    # Load to destination
    print(f"Loaded {len(df)} rows")

@app.local_entrypoint()
def run_pipeline():
    sources = ["data1.csv", "data2.csv", "data3.csv"]
    
    # Extract in parallel
    extracted = list(extract.map(sources))
    
    # Transform in parallel
    transformed = list(transform.map(extracted))
    
    # Load in parallel
    list(load.map(transformed))
```

## Job Queue Pattern

```python
import modal

app = modal.App("job-queue")

@app.function()
def process_job(data: dict) -> dict:
    # Long-running processing
    import time
    time.sleep(10)
    return {"status": "complete", "data": data}

# Submit job and get call ID
def submit_job(data: dict) -> str:
    process_job_fn = modal.Function.from_name("job-queue", "process_job")
    call = process_job_fn.spawn(data)
    return call.object_id

# Poll for result
def get_result(call_id: str):
    call = modal.FunctionCall.from_id(call_id)
    try:
        return call.get(timeout=0)  # Non-blocking
    except TimeoutError:
        return {"status": "pending"}
```

---

# Deployment Best Practices

## Project Structure

```
my-modal-app/
├── app.py           # Main Modal app
├── models/          # ML models
│   └── inference.py
├── utils/           # Shared utilities
│   └── helpers.py
├── requirements.txt
└── Dockerfile       # Optional
```

## Image Optimization

```python
# Order layers by change frequency (least changing first)
image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("ffmpeg")                    # Rarely changes
    .pip_install("torch==2.1.0")              # Pin versions
    .pip_install("transformers==4.35.0")      # Pin versions
    .add_local_python_source("utils")         # Changes more often
)
```

## CI/CD Integration

```yaml
# .github/workflows/deploy.yml
name: Deploy to Modal
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      MODAL_TOKEN_ID: ${{ secrets.MODAL_TOKEN_ID }}
      MODAL_TOKEN_SECRET: ${{ secrets.MODAL_TOKEN_SECRET }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install modal
      - run: modal deploy app.py
```

---

# Debugging & Monitoring

## View Logs

```bash
# Stream logs from deployed app
modal app logs my-app

# View specific function logs
modal container logs <container-id>
```

## Interactive Debugging

```python
# Add breakpoint for debugging
@app.function()
def debug_function():
    import pdb; pdb.set_trace()
    ...
```

## Force Image Rebuild

```bash
# Rebuild all images
MODAL_FORCE_BUILD=1 modal run app.py

# Ignore cache (doesn't break cache for others)
MODAL_IGNORE_CACHE=1 modal run app.py
```

---

# Reference

## CLI Commands

| Command | Description |
|---------|-------------|
| `modal run app.py` | Run ephemeral app |
| `modal deploy app.py` | Deploy persistently |
| `modal serve app.py` | Serve with hot-reload |
| `modal app list` | List deployed apps |
| `modal app stop <name>` | Stop deployed app |
| `modal secret list` | List secrets |
| `modal volume list` | List volumes |

## Pricing

- **CPU**: ~$0.192/core/hour
- **Memory**: ~$0.024/GB/hour
- **GPUs**: Varies by type (see [modal.com/pricing](https://modal.com/pricing))
- Billed per second, only for resources used

## Links

- Documentation: https://modal.com/docs
- Examples: https://github.com/modal-labs/modal-examples
- Pricing: https://modal.com/pricing
- Dashboard: https://modal.com/apps
