---
name: api-ai-modal
description: Serverless GPU compute platform for AI model deployment — web endpoints, GPU functions, model serving, and TypeScript client patterns
---

# Modal Patterns

> **Quick Guide:** Modal is a serverless GPU compute platform where you define Python functions with decorators and Modal handles containers, scaling, and GPU provisioning. TypeScript apps interact with Modal via HTTP endpoints (calling `@modal.fastapi_endpoint` or `@modal.asgi_app` functions) or the `modal` npm SDK (calling functions directly via gRPC). Define container images, secrets, and volumes as code -- no YAML config files. Use `modal deploy` for production, `modal serve` for dev.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST define Modal functions in Python -- the TypeScript SDK can call functions and manage resources but cannot define them)**

**(You MUST use `@modal.fastapi_endpoint` (not the old `@modal.web_endpoint`) for simple web endpoints -- renamed in Modal 1.0)**

**(You MUST use `modal.Volume` for model weight caching -- `@modal.build` is deprecated in Modal 1.0)**

**(You MUST never hardcode secrets in Modal code -- use `modal.Secret.from_name()` and access via `os.environ`)**

**(You MUST bind to `0.0.0.0` (not `127.0.0.1`) when using `@modal.web_server`)**

</critical_requirements>

---

**Auto-detection:** Modal, modal, modal.App, modal.Image, modal.Volume, modal.Secret, modal.gpu, modal.fastapi_endpoint, modal.asgi_app, modal.web_server, modal.Cron, modal.Period, modal deploy, modal serve, MODAL_TOKEN_ID, MODAL_TOKEN_SECRET, ModalClient

**When to use:**

- Deploying ML models (vLLM, Hugging Face, custom PyTorch) on serverless GPUs
- Creating HTTP API endpoints backed by GPU compute for TypeScript apps to consume
- Running scheduled GPU jobs (fine-tuning, batch inference, data processing)
- Calling Modal functions from TypeScript using the `modal` npm SDK
- Building AI inference pipelines with auto-scaling and pay-per-second billing

**Key patterns covered:**

- Web endpoints (`@modal.fastapi_endpoint`, `@modal.asgi_app`, `@modal.web_server`) for HTTP access
- TypeScript client patterns (fetch-based and `modal` npm SDK)
- Container images, secrets, volumes, and GPU configuration
- Model serving with vLLM and custom inference
- Scheduled functions and deployment

**When NOT to use:**

- Pure Python ML workloads with no TypeScript consumer -- this skill focuses on the TypeScript interaction surface
- Simple CPU-only tasks where a regular server or cloud function suffices
- When you need persistent long-running servers (Modal scales to zero by default)

---

## Examples Index

- [Core: Web Endpoints & TypeScript Client](examples/core.md) -- Defining endpoints, calling from TypeScript, authentication, GPU functions, images, secrets, volumes
- [Quick API Reference](reference.md) -- CLI commands, decorator parameters, URL patterns, GPU types

---

<philosophy>

## Philosophy

Modal eliminates infrastructure management for GPU workloads. Everything is code -- container images, GPU allocation, secrets, volumes, scaling rules. There are no YAML configs, Dockerfiles, or Kubernetes manifests.

**Core principles:**

1. **Infrastructure as Python code** -- Container images, GPU types, secrets, and volumes are all declared as Python decorators and objects. No separate config files.
2. **Serverless GPU scaling** -- Functions scale from zero to hundreds of GPUs automatically. You pay per second of compute, not for idle capacity.
3. **Two interaction models for TypeScript** -- Call Modal via HTTP endpoints (most common) or via the `modal` npm SDK for direct function invocation without HTTP overhead.
4. **Immutable deployments** -- `modal deploy` creates a named, persistent deployment with stable URLs. `modal serve` creates ephemeral dev endpoints.

**When to use Modal:**

- GPU inference endpoints that your TypeScript app calls via fetch
- Batch processing jobs (fine-tuning, embeddings generation, data pipelines)
- Model serving with auto-scaling (vLLM, TGI, custom PyTorch)
- Scheduled GPU tasks (cron-based retraining, periodic inference)

**When NOT to use:**

- You need sub-100ms cold starts (Modal cold starts are 2-4 seconds)
- You need persistent WebSocket connections beyond request/response
- Your workload is CPU-only and doesn't benefit from GPU acceleration

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Web Endpoint (TypeScript Consumption)

The most common pattern: define a Python endpoint on Modal, call it from TypeScript via fetch.

#### Python Side

```python
# inference.py
import modal

app = modal.App("my-inference-api")

image = modal.Image.debian_slim().uv_pip_install(["transformers", "torch"])

@app.function(image=image, gpu="A10G")
@modal.fastapi_endpoint(method="POST")
def predict(payload: dict):
    # GPU-accelerated inference
    text = payload["text"]
    result = run_model(text)
    return {"prediction": result}
```

#### TypeScript Side

```typescript
// lib/modal-client.ts
const MODAL_ENDPOINT =
  "https://your-workspace--my-inference-api-predict.modal.run";
const REQUEST_TIMEOUT_MS = 30_000;

interface PredictionRequest {
  text: string;
}

interface PredictionResponse {
  prediction: string;
}

async function predict(input: PredictionRequest): Promise<PredictionResponse> {
  const response = await fetch(MODAL_ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
    signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
  });

  if (!response.ok) {
    throw new Error(
      `Modal API error [${response.status}]: ${await response.text()}`,
    );
  }

  return response.json() as Promise<PredictionResponse>;
}

export { predict };
```

**Why good:** Clean separation -- Python handles GPU compute, TypeScript handles the app. Named constants for config, typed request/response, timeout handling, proper error checking.

```typescript
// BAD: No timeout, no error handling, hardcoded URL in call site
const res = await fetch("https://workspace--app-fn.modal.run", {
  method: "POST",
  body: JSON.stringify({ text: "hello" }),
});
const data = await res.json();
```

**Why bad:** No Content-Type header (may fail), no timeout (hangs on cold start), no error checking, URL scattered across codebase

---

### Pattern 2: Authenticated Endpoints

Modal supports proxy auth tokens that protect endpoints without spinning up containers for unauthorized requests.

#### Python Side

```python
@app.function(image=image, gpu="A10G")
@modal.fastapi_endpoint(method="POST", requires_proxy_auth=True)
def predict_secure(payload: dict):
    return {"prediction": run_model(payload["text"])}
```

#### TypeScript Side

```typescript
// lib/modal-client.ts
const MODAL_KEY = process.env.MODAL_PROXY_KEY;
const MODAL_SECRET = process.env.MODAL_PROXY_SECRET;

async function predictSecure(
  input: PredictionRequest,
): Promise<PredictionResponse> {
  if (!MODAL_KEY || !MODAL_SECRET) {
    throw new Error("Missing MODAL_PROXY_KEY or MODAL_PROXY_SECRET env vars");
  }

  const response = await fetch(MODAL_ENDPOINT, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Modal-Key": MODAL_KEY,
      "Modal-Secret": MODAL_SECRET,
    },
    body: JSON.stringify(input),
    signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
  });

  if (response.status === 401) {
    throw new Error(
      "Modal proxy auth failed -- check MODAL_PROXY_KEY and MODAL_PROXY_SECRET",
    );
  }

  if (!response.ok) {
    throw new Error(
      `Modal API error [${response.status}]: ${await response.text()}`,
    );
  }

  return response.json() as Promise<PredictionResponse>;
}
```

**Why good:** Auth handled at Modal's proxy layer (no container spin-up for bad requests), env vars for credentials, explicit 401 handling

---

### Pattern 3: Modal npm SDK (Direct Function Calls)

For TypeScript apps that need to call Modal functions without HTTP overhead. Requires Node 22+.

```typescript
import { ModalClient } from "modal";
const modal = new ModalClient(); // Create once, reuse
const fn = await modal.functions.fromName("my-inference-api", "predict");
const result = await fn.remote([text]); // sync call
const call = await fn.spawn([text]); // async (fire-and-forget)
const later = await call.get(); // retrieve result later
```

**Why good:** No HTTP serialization overhead, typed SDK, supports async spawn for long-running jobs

See [examples/core.md](examples/core.md) for complete TypeScript SDK patterns including error handling and fire-and-forget job IDs.

**When to use:** Backend-to-Modal calls where you control the Node.js runtime (Node 22+). Not for browser or edge runtimes.

---

### Pattern 4: GPU Functions and Container Images

Modal functions define their compute environment inline.

```python
import modal

app = modal.App("gpu-inference")

# Container image with ML dependencies
inference_image = (
    modal.Image.debian_slim(python_version="3.11")
    .uv_pip_install(["torch==2.5.0", "transformers==4.47.0", "accelerate"])
    .apt_install(["libgl1"])
)

MODEL_ID = "meta-llama/Llama-3.1-8B-Instruct"

@app.function(
    image=inference_image,
    gpu="A100",                   # GPU type: "T4", "A10G", "A100", "H100", etc.
    secrets=[modal.Secret.from_name("huggingface-secret")],
    volumes={"/models": modal.Volume.from_name("model-cache", create_if_missing=True)},
    min_containers=1,             # Keep warm to avoid cold starts
    scaledown_window=300,         # Seconds before scaling to zero
)
def generate(prompt: str) -> str:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    # Load from volume cache
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, cache_dir="/models")
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, cache_dir="/models")
    # ... generate and return
```

**Why good:** Pinned dependency versions, volume-based model caching (avoids re-download), `min_containers` for warm starts, secrets for HF token

```python
# BAD: No version pinning, no volume cache, model re-downloads every cold start
@app.function(gpu="A100")
def generate(prompt: str):
    from transformers import pipeline
    pipe = pipeline("text-generation", model="meta-llama/Llama-3.1-8B-Instruct")
    return pipe(prompt)[0]["generated_text"]
```

**Why bad:** Unpinned deps break reproducibility, no volume means multi-GB model download on every cold start (30-60s+ delay), no secret for gated models

---

### Pattern 5: Full ASGI App (FastAPI)

For endpoints that need routing, middleware, or multiple routes.

```python
import modal
from fastapi import FastAPI

app = modal.App("my-api")
web_app = FastAPI()

@web_app.post("/predict")
async def predict(payload: dict):
    return {"result": "prediction"}

@web_app.get("/health")
async def health():
    return {"status": "ok"}

@app.function(image=modal.Image.debian_slim().uv_pip_install(["fastapi"]))
@modal.asgi_app()
def serve():
    return web_app
```

**Why good:** Full FastAPI capabilities (routing, middleware, validation), multiple endpoints under one function

---

### Pattern 6: Secrets and Environment Variables

```python
# Creating secrets via CLI
# modal secret create my-api-keys API_KEY=sk-xxx DB_URL=postgres://...

@app.function(
    secrets=[
        modal.Secret.from_name("my-api-keys"),
        modal.Secret.from_name("huggingface-secret"),
    ]
)
def my_function():
    import os
    api_key = os.environ["API_KEY"]  # Injected by Modal
    hf_token = os.environ["HF_TOKEN"]
```

**Why good:** Secrets created via dashboard or CLI, referenced by name in code, accessed as standard env vars, multiple secrets composable

---

### Pattern 7: Scheduled Functions

```python
@app.function(
    schedule=modal.Cron("0 2 * * *"),  # 2 AM daily
    image=inference_image,
    gpu="A10G",
    volumes={"/data": modal.Volume.from_name("training-data")},
)
def nightly_batch_inference():
    # Process accumulated data
    # Write results to volume
    pass

@app.function(schedule=modal.Period(hours=6))
def periodic_health_check():
    # Check model freshness, data quality, etc.
    pass
```

**Why good:** `modal.Cron` for precise scheduling, `modal.Period` for intervals. Scheduled functions cannot accept arguments -- use volumes or secrets for input data.

</patterns>

---

<decision_framework>

## Decision Framework

### How to Expose Modal to TypeScript

```
Does your TypeScript app need to call Modal?
+-- Via HTTP (most common)
|   +-- Single endpoint? -> @modal.fastapi_endpoint
|   +-- Multiple routes? -> @modal.asgi_app with FastAPI
|   +-- Non-Python server (vLLM, TGI)? -> @modal.web_server(port=8000)
|   +-- Need auth? -> Add requires_proxy_auth=True
+-- Via SDK (direct gRPC)
|   +-- Node 22+ backend? -> npm install modal, use ModalClient
|   +-- Browser/edge? -> Use HTTP endpoints instead
+-- Async job?
    +-- Fire-and-forget? -> SDK spawn() + later get()
    +-- Webhook callback? -> Modal calls your endpoint on completion
```

### When to Use Each Endpoint Type

```
What are you serving?
+-- Simple function -> @modal.fastapi_endpoint (auto-wraps in FastAPI)
+-- Full web app -> @modal.asgi_app (FastAPI, Starlette, FastHTML)
+-- Legacy sync app -> @modal.wsgi_app (Flask, Django)
+-- Custom server binary -> @modal.web_server(port=8000) (vLLM, TGI, Ollama)
```

### HTTP vs SDK

```
How should TypeScript call Modal?
+-- Browser/edge runtime? -> HTTP (fetch)
+-- Server-side Node 22+? -> Either works
|   +-- Need simplicity? -> HTTP
|   +-- Need speed (no serialization overhead)? -> SDK
|   +-- Need async spawn? -> SDK
+-- Multiple providers? -> HTTP (vendor-agnostic)
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using deprecated `@modal.web_endpoint` instead of `@modal.fastapi_endpoint` (renamed in Modal 1.0)
- Using `@modal.build` for downloading model weights (deprecated -- use `modal.Volume` instead)
- Using `.lookup()` for object references (deprecated -- use `.from_name()`)
- Hardcoding secrets in Python source (use `modal.Secret.from_name()` + `os.environ`)
- Binding `@modal.web_server` to `127.0.0.1` instead of `0.0.0.0` (endpoint unreachable)

**Medium Priority Issues:**

- Not pinning dependency versions in `uv_pip_install()` (breaks reproducibility)
- No `min_containers` for latency-sensitive endpoints (2-4s cold starts)
- Missing `signal: AbortSignal.timeout()` on TypeScript fetch calls (hangs on cold starts)
- Not using volumes for model weight caching (re-downloads multi-GB models on cold starts)
- Using `modal.Period` when you need exact times (use `modal.Cron` -- Period resets on redeploy)

**Common Mistakes:**

- Confusing `modal serve` (ephemeral dev) with `modal deploy` (persistent production)
- Using `messages` parameter with `@modal.fastapi_endpoint` (it is not OpenAI -- it is a plain HTTP endpoint)
- Forgetting that scheduled functions cannot accept arguments -- use volumes, secrets, or global variables for input
- Not setting `Content-Type: application/json` header from TypeScript (FastAPI endpoints may reject the request)
- Using the `modal` npm SDK in browser or edge runtimes (requires Node 22+, native modules)

**Gotchas & Edge Cases:**

- Web endpoint max request timeout is 150 seconds (enforced by Modal's proxy)
- Rate limit: 200 requests/second default with 5-second burst multiplier
- Request bodies up to 4 GiB, response bodies unlimited
- `modal serve` URLs get a `-dev` suffix to avoid production conflicts
- URL pattern: `https://<workspace>--<app-name>-<function-name>.modal.run`
- Labels exceeding 63 characters are truncated with a SHA-256 hash suffix
- Volumes v1 limited to 500,000 files; v2 has no limit (use `version=2`)
- `modal.Cron` maintains schedule across redeploys; `modal.Period` resets
- Container class parameters are limited to primitives: `str`, `int`, `bool`, `bytes`
- Local Python files require `Image.add_local_python_source()` (automounting removed in 1.0)

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST define Modal functions in Python -- the TypeScript SDK can call functions and manage resources but cannot define them)**

**(You MUST use `@modal.fastapi_endpoint` (not the old `@modal.web_endpoint`) for simple web endpoints -- renamed in Modal 1.0)**

**(You MUST use `modal.Volume` for model weight caching -- `@modal.build` is deprecated in Modal 1.0)**

**(You MUST never hardcode secrets in Modal code -- use `modal.Secret.from_name()` and access via `os.environ`)**

**(You MUST bind to `0.0.0.0` (not `127.0.0.1`) when using `@modal.web_server`)**

**Failure to follow these rules will produce broken deployments, security vulnerabilities, or unreachable endpoints.**

</critical_reminders>
