---
name: modal-knowledge
description: Comprehensive Modal.com platform knowledge covering all features, pricing, and best practices
---

# Modal Knowledge Skill

Comprehensive Modal.com platform knowledge covering all features, pricing, and best practices. Activate this skill when users need detailed information about Modal's serverless cloud platform.

## Activation Triggers

Activate this skill when users ask about:
- Modal.com platform features and capabilities
- GPU-accelerated Python functions
- Serverless container configuration
- Modal pricing and billing
- Modal CLI commands
- Web endpoints and APIs on Modal
- Scheduled/cron jobs on Modal
- Modal volumes, secrets, and storage
- Parallel processing with Modal
- Modal deployment and CI/CD

---

## Platform Overview

Modal is a serverless cloud platform for running Python code, optimized for AI/ML workloads with:

- **Zero Configuration**: Everything defined in Python code
- **Fast GPU Startup**: ~1 second container spin-up
- **Automatic Scaling**: Scale to zero, scale to thousands
- **Per-Second Billing**: Only pay for active compute
- **Multi-Cloud**: AWS, GCP, Oracle Cloud Infrastructure

---

## Core Components Reference

### Apps and Functions

```python
import modal

app = modal.App("app-name")

@app.function()
def basic_function(arg: str) -> str:
    return f"Result: {arg}"

@app.local_entrypoint()
def main():
    result = basic_function.remote("test")
    print(result)
```

### Function Decorator Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `image` | Image | Container image configuration |
| `gpu` | str/list | GPU type(s): "T4", "A100", ["H100", "A100"] |
| `cpu` | float | CPU cores (0.125 to 64) |
| `memory` | int | Memory in MB (128 to 262144) |
| `timeout` | int | Max execution seconds |
| `retries` | int | Retry attempts on failure |
| `secrets` | list | Secrets to inject |
| `volumes` | dict | Volume mount points |
| `schedule` | Cron/Period | Scheduled execution |
| `concurrency_limit` | int | Max concurrent executions |
| `container_idle_timeout` | int | Seconds to keep warm |
| `include_source` | bool | Auto-sync source code |

---

## GPU Reference

### Available GPUs

| GPU | Memory | Use Case | ~Cost/hr |
|-----|--------|----------|----------|
| T4 | 16 GB | Small inference | $0.59 |
| L4 | 24 GB | Medium inference | $0.80 |
| A10G | 24 GB | Inference/fine-tuning | $1.10 |
| L40S | 48 GB | Heavy inference | $1.50 |
| A100-40GB | 40 GB | Training | $2.00 |
| A100-80GB | 80 GB | Large models | $3.00 |
| H100 | 80 GB | Cutting-edge | $5.00 |
| H200 | 141 GB | Largest models | $5.00 |
| B200 | 180+ GB | Latest gen | $6.25 |

### GPU Configuration

```python
# Single GPU
@app.function(gpu="A100")

# Specific memory variant
@app.function(gpu="A100-80GB")

# Multi-GPU
@app.function(gpu="H100:4")

# Fallbacks (tries in order)
@app.function(gpu=["H100", "A100", "any"])

# "any" = L4, A10G, or T4
@app.function(gpu="any")
```

---

## Image Building

### Base Images

```python
# Debian slim (recommended)
modal.Image.debian_slim(python_version="3.11")

# From Dockerfile
modal.Image.from_dockerfile("./Dockerfile")

# From Docker registry
modal.Image.from_registry("nvidia/cuda:12.1.0-base-ubuntu22.04")
```

### Package Installation

```python
# pip (standard)
image.pip_install("torch", "transformers")

# uv (FASTER - 10-100x)
image.uv_pip_install("torch", "transformers")

# System packages
image.apt_install("ffmpeg", "libsm6")

# Shell commands
image.run_commands("apt-get update", "make install")
```

### Adding Files

```python
# Single file
image.add_local_file("./config.json", "/app/config.json")

# Directory
image.add_local_dir("./models", "/app/models")

# Python source
image.add_local_python_source("my_module")

# Environment variables
image.env({"VAR": "value"})
```

### Build-Time Function

```python
def download_model():
    from huggingface_hub import snapshot_download
    snapshot_download("model-name")

image.run_function(download_model, secrets=[...])
```

---

## Storage

### Volumes

```python
# Create/reference volume
vol = modal.Volume.from_name("my-vol", create_if_missing=True)

# Mount in function
@app.function(volumes={"/data": vol})
def func():
    # Read/write to /data
    vol.commit()  # Persist changes
```

### Secrets

```python
# From dashboard (recommended)
modal.Secret.from_name("secret-name")

# From dictionary
modal.Secret.from_dict({"KEY": "value"})

# From local env
modal.Secret.from_local_environ(["KEY1", "KEY2"])

# From .env file
modal.Secret.from_dotenv()

# Usage
@app.function(secrets=[modal.Secret.from_name("api-keys")])
def func():
    import os
    key = os.environ["API_KEY"]
```

### Dict and Queue

```python
# Distributed dict
d = modal.Dict.from_name("cache", create_if_missing=True)
d["key"] = "value"
d.put("key", "value", ttl=3600)

# Distributed queue
q = modal.Queue.from_name("jobs", create_if_missing=True)
q.put("task")
item = q.get()
```

---

## Web Endpoints

### FastAPI Endpoint (Simple)

```python
@app.function()
@modal.fastapi_endpoint()
def hello(name: str = "World"):
    return {"message": f"Hello, {name}!"}
```

### ASGI App (Full FastAPI)

```python
from fastapi import FastAPI
web_app = FastAPI()

@web_app.post("/predict")
def predict(text: str):
    return {"result": process(text)}

@app.function()
@modal.asgi_app()
def fastapi_app():
    return web_app
```

### WSGI App (Flask)

```python
from flask import Flask
flask_app = Flask(__name__)

@app.function()
@modal.wsgi_app()
def flask_endpoint():
    return flask_app
```

### Custom Web Server

```python
@app.function()
@modal.web_server(port=8000)
def custom_server():
    subprocess.run(["python", "-m", "http.server", "8000"])
```

### Custom Domains

```python
@modal.asgi_app(custom_domains=["api.example.com"])
```

---

## Scheduling

### Cron

```python
# Daily at 8 AM UTC
@app.function(schedule=modal.Cron("0 8 * * *"))

# With timezone
@app.function(schedule=modal.Cron("0 6 * * *", timezone="America/New_York"))
```

### Period

```python
@app.function(schedule=modal.Period(hours=5))
@app.function(schedule=modal.Period(days=1))
```

**Note:** Scheduled functions only run with `modal deploy`, not `modal run`.

---

## Parallel Processing

### Map

```python
# Parallel execution (up to 1000 concurrent)
results = list(func.map(items))

# Unordered (faster)
results = list(func.map(items, order_outputs=False))
```

### Starmap

```python
# Spread args
pairs = [(1, 2), (3, 4)]
results = list(add.starmap(pairs))
```

### Spawn

```python
# Async job (returns immediately)
call = func.spawn(data)
result = call.get()  # Get result later

# Spawn many
calls = [func.spawn(item) for item in items]
results = [call.get() for call in calls]
```

---

## Container Lifecycle (Classes)

```python
@app.cls(gpu="A100", container_idle_timeout=300)
class Server:

    @modal.enter()
    def load(self):
        self.model = load_model()

    @modal.method()
    def predict(self, text):
        return self.model(text)

    @modal.exit()
    def cleanup(self):
        del self.model
```

### Concurrency

```python
@modal.concurrent(max_inputs=100, target_inputs=80)
@modal.method()
def batched(self, item):
    pass
```

---

## CLI Commands

### Development

```bash
modal run app.py              # Run function
modal serve app.py            # Hot-reload dev server
modal shell app.py            # Interactive shell
modal shell app.py --gpu A100 # Shell with GPU
```

### Deployment

```bash
modal deploy app.py           # Deploy
modal app list                # List apps
modal app logs app-name       # View logs
modal app stop app-name       # Stop app
```

### Resources

```bash
# Volumes
modal volume create name
modal volume list
modal volume put name local remote
modal volume get name remote local

# Secrets
modal secret create name KEY=value
modal secret list

# Environments
modal environment create staging
```

---

## Pricing (2025)

### Plans

| Plan | Price | Containers | GPU Concurrency |
|------|-------|------------|-----------------|
| Starter | Free ($30 credits) | 100 | 10 |
| Team | $250/month | 1000 | 50 |
| Enterprise | Custom | Unlimited | Custom |

### Compute

- **CPU**: $0.0000131/core/sec
- **Memory**: $0.00000222/GiB/sec
- **GPUs**: See GPU table above

### Special Programs

- Startups: Up to $25k credits
- Researchers: Up to $10k credits

---

## Best Practices

1. **Use `@modal.enter()`** for model loading
2. **Use `uv_pip_install`** for faster builds
3. **Use GPU fallbacks** for availability
4. **Set appropriate timeouts** and retries
5. **Use environments** (dev/staging/prod)
6. **Download models during build**, not runtime
7. **Use `order_outputs=False`** when order doesn't matter
8. **Set `container_idle_timeout`** to balance cost/latency
9. **Monitor costs** in Modal dashboard
10. **Test with `modal run`** before `modal deploy`

---

## Common Patterns

### LLM Inference

```python
@app.cls(gpu="A100", container_idle_timeout=300)
class LLM:
    @modal.enter()
    def load(self):
        from vllm import LLM
        self.llm = LLM(model="...")

    @modal.method()
    def generate(self, prompt):
        return self.llm.generate([prompt])
```

### Batch Processing

```python
@app.function(volumes={"/data": vol})
def process(file):
    # Process file
    vol.commit()

# Parallel
results = list(process.map(files))
```

### Scheduled ETL

```python
@app.function(
    schedule=modal.Cron("0 6 * * *"),
    secrets=[modal.Secret.from_name("db")]
)
def daily_etl():
    extract()
    transform()
    load()
```

---

## Quick Reference

| Task | Code |
|------|------|
| Create app | `app = modal.App("name")` |
| Basic function | `@app.function()` |
| With GPU | `@app.function(gpu="A100")` |
| With image | `@app.function(image=img)` |
| Web endpoint | `@modal.asgi_app()` |
| Scheduled | `schedule=modal.Cron("...")` |
| Mount volume | `volumes={"/path": vol}` |
| Use secret | `secrets=[modal.Secret.from_name("x")]` |
| Parallel map | `func.map(items)` |
| Async spawn | `func.spawn(arg)` |
| Class pattern | `@app.cls()` with `@modal.enter()` |
