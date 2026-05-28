---
name: python-cloudflare
description: Complete Python Cloudflare deployment system. PROACTIVELY activate for: (1) Python Workers with Pyodide, (2) FastAPI on Workers, (3) Cloudflare Containers for heavy compute, (4) Service bindings (RPC), (5) Environment variables in Workers, (6) Cold start optimization, (7) Workflows for durable execution, (8) GPU containers for AI. Provides: Worker code patterns, wrangler config, Dockerfile templates, FastAPI integration. Ensures edge deployment with proper architecture choices.
---

## Quick Reference

| Platform | Cold Start | Packages | Best For |
|----------|------------|----------|----------|
| Workers (Pyodide) | ~50ms | Limited | API endpoints |
| Containers | ~10s | Any | Heavy compute, AI |

| Worker Pattern | Code |
|----------------|------|
| Basic handler | `class Default(WorkerEntrypoint):` |
| FastAPI | `await asgi.fetch(app, request, self.env)` |
| Env vars | `self.env.API_KEY` |
| Service binding | `await self.env.WORKER_B.method()` |

| Command | Purpose |
|---------|---------|
| `pywrangler init` | Create Python Worker |
| `pywrangler dev` | Local development |
| `pywrangler deploy` | Deploy to Cloudflare |

| Container vs Worker | Recommendation |
|---------------------|----------------|
| Simple API | Worker |
| pandas/numpy | Container |
| GPU/AI | Container |
| <50ms latency | Worker |

## When to Use This Skill

Use for **Cloudflare edge deployment**:
- Deploying Python APIs to Cloudflare Workers
- Running FastAPI on Cloudflare edge
- Using Containers for heavy compute
- Setting up service-to-service RPC
- Optimizing cold starts

**Related skills:**
- For FastAPI: see `python-fastapi`
- For async patterns: see `python-asyncio`
- For Docker: see `python-github-actions`

---

# Python on Cloudflare (Workers & Containers)

## Overview

Cloudflare provides two ways to run Python:
1. **Python Workers** - Serverless functions using Pyodide (WebAssembly)
2. **Cloudflare Containers** - Full Docker containers (beta, June 2025)

## Python Workers

### How It Works

- Python runs via **Pyodide** (CPython compiled to WebAssembly)
- Executes inside V8 isolates on Cloudflare's edge network
- Memory snapshots enable fast cold starts
- Supports many pure Python packages

### Quick Start

```bash
# Install pywrangler (Python Workers CLI)
pip install pywrangler

# Create new Python Worker
pywrangler init my-worker
cd my-worker

# Project structure
my-worker/
├── src/
│   └── entry.py
├── pyproject.toml
└── wrangler.toml
```

### Basic Worker

```python
# src/entry.py
from workers import Response, WorkerEntrypoint

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return Response("Hello from Python Worker!")
```

### Configuration

```toml
# wrangler.toml
name = "my-python-worker"
main = "src/entry.py"
compatibility_date = "2024-12-01"

[build]
command = ""
```

```toml
# pyproject.toml
[project]
name = "my-python-worker"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi",
    "pydantic",
]

[dependency-groups]
dev = ["workers-py"]
```

### FastAPI on Workers

```python
# src/entry.py
from workers import WorkerEntrypoint
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        import asgi
        return await asgi.fetch(app, request, self.env)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI on Cloudflare!"}

@app.get("/env")
async def get_env(req: Request):
    env = req.scope.get("env")
    if env and hasattr(env, "API_KEY"):
        return {"has_api_key": True}
    return {"has_api_key": False}

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

### Using Environment Variables

```python
from workers import WorkerEntrypoint, Response

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        # Access environment variables via self.env
        api_key = self.env.API_KEY
        database_url = self.env.DATABASE_URL

        return Response(f"API Key exists: {bool(api_key)}")
```

```toml
# wrangler.toml
[vars]
API_KEY = "your-api-key"
DATABASE_URL = "your-database-url"
```

### Service Bindings (RPC)

```python
# Worker A - Caller
from workers import WorkerEntrypoint, Response

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        # Call Worker B's add method
        result = await self.env.WORKER_B.add(1, 2)
        return Response(f"Result: {result}")
```

```python
# Worker B - Callee
from workers import WorkerEntrypoint, Response

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return Response("Hello from Worker B")

    def add(self, a: int, b: int) -> int:
        return a + b
```

```toml
# Worker A wrangler.toml
[[services]]
binding = "WORKER_B"
service = "worker-b"
```

### Caching

```python
from workers import WorkerEntrypoint
from pyodide.ffi import to_js as _to_js
from js import Response, URL, Object, fetch

def to_js(x):
    return _to_js(x, dict_converter=Object.fromEntries)

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        request_url = URL.new(request.url)
        params = request_url.searchParams
        tags = params["tags"].split(",") if "tags" in params else []
        url = params["uri"] or None

        if url is None:
            return Response.json(to_js({"error": "URL required"}), status=400)

        # Fetch with cache tags
        options = {"cf": {"cacheTags": tags}}
        result = await fetch(url, to_js(options))

        cache_status = result.headers["cf-cache-status"]
        return Response.json(to_js({
            "cache": cache_status,
            "status": result.status
        }))
```

### Supported Packages

```python
# HTTP clients (async only)
import aiohttp
import httpx

# Data processing
import numpy  # Limited support
import pandas  # Limited support

# Standard library works well
import json
import re
import urllib
import base64
import hashlib

# Check Pyodide package list for full support
# https://pyodide.org/en/stable/usage/packages-in-pyodide.html
```

### Cold Start Optimization

```python
# Imports at module level are cached in memory snapshot
import json
import hashlib
from pydantic import BaseModel

# This code runs during snapshot creation
CACHED_CONFIG = load_config()

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        # Fast access to pre-loaded modules and data
        return Response(json.dumps(CACHED_CONFIG))
```

## Cloudflare Containers (Beta)

### Overview (June 2025)

- Full Docker container support
- Run any language/runtime (Python, Go, Java, etc.)
- FFmpeg, Pandas, AI toolchains supported
- Pay-per-use pricing
- Global edge deployment

### When to Use Containers vs Workers

| Feature | Workers | Containers |
|---------|---------|------------|
| Cold start | ~50ms | ~10s (with prewarming) |
| Package support | Pyodide-compatible | Any |
| Memory | Limited | Configurable |
| File system | No | Yes |
| Native binaries | No | Yes |
| Best for | API endpoints | Batch jobs, AI, heavy compute |

### Container Setup

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run application
CMD ["python", "main.py"]
```

```python
# main.py
import pandas as pd
import numpy as np
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/process")
async def process_data():
    # Heavy computation that wouldn't work in Workers
    df = pd.DataFrame(np.random.randn(10000, 4))
    result = df.describe().to_dict()
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

### Wrangler Commands

```bash
# Build container
wrangler containers build . --tag my-app:latest

# Push to registry
wrangler containers push my-app:latest

# Deploy
wrangler containers deploy my-app

# List containers
wrangler containers list

# Delete
wrangler containers delete my-app
```

### Container Optimization

```dockerfile
# Multi-stage build for smaller images
FROM python:3.12-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target=/app/deps

FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /app/deps /app/deps
COPY . .

ENV PYTHONPATH=/app/deps
CMD ["python", "main.py"]
```

```python
# Optimize for container cold starts
import asyncio

# Lazy imports for faster startup
def get_pandas():
    import pandas as pd
    return pd

async def process_large_data():
    pd = get_pandas()  # Import only when needed
    # Process data...
```

### GPU Support (Preview)

```python
# Container with GPU support
import torch

def run_inference(data):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = load_model().to(device)

    with torch.no_grad():
        result = model(data.to(device))

    return result.cpu().numpy()
```

## Python Workflows (Durable Execution)

### Overview

Cloudflare Workflows now supports Python for multi-step, long-running applications with automatic retries and state persistence.

```python
from cloudflare.workflows import Workflow, step

class DataPipeline(Workflow):
    @step
    async def fetch_data(self, url: str) -> dict:
        """Fetch data from external API."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    @step
    async def process_data(self, data: dict) -> dict:
        """Process the fetched data."""
        # Heavy processing - will retry if fails
        processed = transform(data)
        return processed

    @step
    async def save_results(self, data: dict) -> str:
        """Save to database."""
        result_id = await save_to_db(data)
        return result_id

    async def run(self, input_url: str) -> str:
        data = await self.fetch_data(input_url)
        processed = await self.process_data(data)
        result_id = await self.save_results(processed)
        return f"Saved as {result_id}"
```

## Best Practices

### 1. Minimize Cold Starts

```python
# Do expensive imports at module level
import json
import hashlib
from pydantic import BaseModel

# Pre-compute static data
STATIC_CONFIG = {"version": "1.0", "features": ["a", "b"]}

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        # Fast path - no initialization needed
        return Response(json.dumps(STATIC_CONFIG))
```

### 2. Use Async HTTP Clients

```python
# Workers only support async HTTP
import httpx

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.example.com/data")
            return Response(response.text)
```

### 3. Handle Errors Gracefully

```python
from workers import WorkerEntrypoint, Response

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        try:
            result = await self.process_request(request)
            return Response(json.dumps(result), headers={
                "Content-Type": "application/json"
            })
        except ValueError as e:
            return Response(json.dumps({"error": str(e)}), status=400)
        except Exception as e:
            # Log error (sent to Workers Logs)
            print(f"Error: {e}")
            return Response(json.dumps({"error": "Internal error"}), status=500)
```

### 4. Structure for Testability

```python
# src/handlers.py - Pure Python logic
async def handle_create_item(data: dict) -> dict:
    # Testable without Worker runtime
    validated = validate_item(data)
    return {"id": generate_id(), **validated}

# src/entry.py - Worker entrypoint
from workers import WorkerEntrypoint, Response
from handlers import handle_create_item

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        if request.method == "POST":
            data = await request.json()
            result = await handle_create_item(data)
            return Response(json.dumps(result))
```

### 5. Local Development

```bash
# Start local development server
pywrangler dev

# Test locally
curl http://localhost:8787/

# Deploy to Cloudflare
pywrangler deploy
```
