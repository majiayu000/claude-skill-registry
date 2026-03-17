---
name: "runpod-deployment"
description: "Deploy GPU workloads to RunPod serverless and pods - vLLM endpoints, A100/H100 setup, scale-to-zero, cost optimization. Use when: deploy to RunPod, GPU serverless, vLLM endpoint, scale to zero, A100 deployment, H100 setup, serverless handler, GPU cost optimization."
---

<objective>
Deploy and manage GPU workloads on RunPod infrastructure:

1. **Serverless Workers** - Scale-to-zero handlers with pay-per-second billing
2. **vLLM Endpoints** - OpenAI-compatible LLM serving with 2-3x throughput
3. **Pod Management** - Dedicated GPU instances for development/training
4. **Cost Optimization** - GPU selection, spot instances, budget controls

Key deliverables:
- Production-ready serverless handlers with streaming
- vLLM deployment with OpenAI API compatibility
- Cost-optimized GPU selection for any model size
- Health monitoring and auto-scaling configuration
</objective>

<quick_start>
**Minimal Serverless Handler (v1.8.1):**
```python
import runpod

def handler(job):
    """Basic handler - receives job, returns result."""
    job_input = job["input"]
    prompt = job_input.get("prompt", "")

    # Your inference logic here
    result = process(prompt)

    return {"output": result}

runpod.serverless.start({"handler": handler})
```

**Streaming Handler:**
```python
import runpod

def streaming_handler(job):
    """Generator for streaming responses."""
    for chunk in generate_chunks(job["input"]):
        yield {"token": chunk, "finished": False}
    yield {"token": "", "finished": True}

runpod.serverless.start({
    "handler": streaming_handler,
    "return_aggregate_stream": True
})
```

**vLLM OpenAI-Compatible Client:**
```python
from openai import OpenAI

client = OpenAI(
    api_key="RUNPOD_API_KEY",
    base_url="https://api.runpod.ai/v2/ENDPOINT_ID/openai/v1",
)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=100,
)
```
</quick_start>

<success_criteria>
A RunPod deployment is successful when:
- Handler processes requests without errors
- Endpoint scales appropriately (0 → N workers)
- Cold start time is acceptable for use case
- Cost stays within budget projections
- Health checks pass consistently
</success_criteria>

<m1_mac_critical>
## M1/M2 Mac: Cannot Build Docker Locally

ARM architecture is incompatible with RunPod's x86 GPUs.

**Solution: GitHub Actions builds for you:**
```bash
# Push code - Actions builds x86 image
git add . && git commit -m "Deploy" && git push
```

> See `reference/cicd.md` for complete GitHub Actions workflow.

**Never run `docker build` locally for RunPod on Apple Silicon.**
</m1_mac_critical>

<gpu_selection>
## GPU Selection Matrix (January 2025)

| GPU | VRAM | Secure $/hr | Spot $/hr | Best For |
|-----|------|-------------|-----------|----------|
| RTX A4000 | 16GB | $0.36 | $0.18 | Embeddings, small models |
| RTX 4090 | 24GB | $0.44 | $0.22 | 7B-8B inference |
| A40 | 48GB | $0.65 | $0.39 | 13B-30B, fine-tuning |
| A100 80GB | 80GB | $1.89 | $0.89 | 70B models, production |
| H100 80GB | 80GB | $4.69 | $1.88 | 70B+ training |

**Quick Selection:**
```python
def select_gpu(model_params_b: float, quantized: bool = False) -> str:
    effective = model_params_b * (0.5 if quantized else 1.0)
    if effective <= 3: return "RTX_A4000"      # $0.36/hr
    if effective <= 8: return "RTX_4090"       # $0.44/hr
    if effective <= 30: return "A40"           # $0.65/hr
    if effective <= 70: return "A100_80GB"     # $1.89/hr
    return "H100_80GB"                         # $4.69/hr
```

> See `reference/cost-optimization.md` for detailed pricing and budget controls.
</gpu_selection>

<handler_patterns>
## Handler Patterns

### Progress Updates (Long-Running Tasks)
```python
import runpod

def long_task_handler(job):
    total_steps = job["input"].get("steps", 10)

    for step in range(total_steps):
        process_step(step)
        runpod.serverless.progress_update(
            job_id=job["id"],
            progress=int((step + 1) / total_steps * 100)
        )

    return {"status": "complete", "steps": total_steps}

runpod.serverless.start({"handler": long_task_handler})
```

### Error Handling
```python
import runpod
import traceback

def safe_handler(job):
    try:
        # Validate input
        if "prompt" not in job["input"]:
            return {"error": "Missing required field: prompt"}

        result = process(job["input"])
        return {"output": result}

    except torch.cuda.OutOfMemoryError:
        return {"error": "GPU OOM - reduce input size", "retry": False}
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}

runpod.serverless.start({"handler": safe_handler})
```

> See `reference/serverless-workers.md` for async patterns, batching, and advanced handlers.
</handler_patterns>

<vllm_deployment>
## vLLM Deployment

> **Note:** vLLM uses OpenAI-compatible API FORMAT but connects to YOUR RunPod endpoint,
> NOT OpenAI servers. Models run on your GPU (Llama, Qwen, Mistral, etc.)

### Environment Configuration
```python
vllm_env = {
    "MODEL_NAME": "meta-llama/Llama-3.1-70B-Instruct",
    "HF_TOKEN": "${HF_TOKEN}",
    "TENSOR_PARALLEL_SIZE": "2",        # Multi-GPU
    "MAX_MODEL_LEN": "16384",
    "GPU_MEMORY_UTILIZATION": "0.95",
    "QUANTIZATION": "awq",              # Optional: awq, gptq
}
```

### OpenAI-Compatible Streaming
```python
from openai import OpenAI

client = OpenAI(
    api_key="RUNPOD_API_KEY",
    base_url="https://api.runpod.ai/v2/ENDPOINT_ID/openai/v1",
)

stream = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[{"role": "user", "content": "Write a poem"}],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Direct RunPod Streaming
```python
import requests

url = "https://api.runpod.ai/v2/ENDPOINT_ID/run"
headers = {"Authorization": "Bearer RUNPOD_API_KEY"}

response = requests.post(url, headers=headers, json={
    "input": {"prompt": "Hello", "stream": True}
})
job_id = response.json()["id"]

# Stream results
stream_url = f"https://api.runpod.ai/v2/ENDPOINT_ID/stream/{job_id}"
with requests.get(stream_url, headers=headers, stream=True) as r:
    for line in r.iter_lines():
        if line: print(line.decode())
```

> See `reference/model-deployment.md` for HuggingFace, TGI, and custom model patterns.
</vllm_deployment>

<auto_scaling>
## Auto-Scaling Configuration

### Scaler Types
| Type | Best For | Config |
|------|----------|--------|
| QUEUE_DELAY | Variable traffic | `scaler_value=2` (2s target) |
| REQUEST_COUNT | Predictable load | `scaler_value=5` (5 req/worker) |

### Configuration Patterns
```python
configs = {
    "interactive_api": {
        "workers_min": 1,      # Always warm
        "workers_max": 5,
        "idle_timeout": 120,
        "scaler_type": "QUEUE_DELAY",
        "scaler_value": 1,     # 1s latency target
    },
    "batch_processing": {
        "workers_min": 0,
        "workers_max": 20,
        "idle_timeout": 30,
        "scaler_type": "REQUEST_COUNT",
        "scaler_value": 5,
    },
    "cost_optimized": {
        "workers_min": 0,
        "workers_max": 3,
        "idle_timeout": 15,    # Aggressive scale-down
        "scaler_type": "QUEUE_DELAY",
        "scaler_value": 5,
    },
}
```

> See `reference/pod-management.md` for pod lifecycle and scaling details.
</auto_scaling>

<health_monitoring>
## Health & Monitoring

### Quick Health Check
```python
import runpod

async def check_health(endpoint_id: str):
    endpoint = runpod.Endpoint(endpoint_id)
    health = await endpoint.health()

    return {
        "status": health.status,
        "workers_ready": health.workers.ready,
        "queue_depth": health.queue.in_queue,
        "avg_latency_ms": health.metrics.avg_execution_time,
    }
```

### GraphQL Metrics Query
```graphql
query GetEndpoint($id: String!) {
    endpoint(id: $id) {
        status
        workers { ready running pending throttled }
        queue { inQueue inProgress completed failed }
        metrics {
            requestsPerMinute
            avgExecutionTimeMs
            p95ExecutionTimeMs
            successRate
        }
    }
}
```

> See `reference/monitoring.md` for structured logging, alerts, and dashboards.
</health_monitoring>

<dockerfile_pattern>
## Dockerfile Template

```dockerfile
FROM runpod/pytorch:2.1.0-py3.10-cuda12.1.1-devel-ubuntu22.04

WORKDIR /app

# Install dependencies (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# RunPod entrypoint
CMD ["python", "-u", "handler.py"]
```

> See `reference/templates.md` for runpod.toml, requirements.txt patterns.
</dockerfile_pattern>

<file_locations>
## Reference Files

**Core Patterns:**
- `reference/serverless-workers.md` - Handler patterns, streaming, async
- `reference/model-deployment.md` - vLLM, TGI, HuggingFace deployment
- `reference/pod-management.md` - GPU types, scaling, lifecycle

**Operations:**
- `reference/cost-optimization.md` - Budget controls, right-sizing
- `reference/monitoring.md` - Health checks, logging, GraphQL
- `reference/troubleshooting.md` - Common issues and solutions

**DevOps:**
- `reference/cicd.md` - GitHub Actions for M1 Mac builds
- `reference/templates.md` - Dockerfile, runpod.toml configs
- `templates/runpod-worker.py` - Production handler template
</file_locations>

<routing>
## Request Routing

**User wants serverless deployment:**
→ Provide handler pattern, Dockerfile, deployment steps
→ Reference: `reference/serverless-workers.md`

**User wants vLLM endpoint:**
→ Provide vLLM env config, OpenAI client setup
→ Reference: `reference/model-deployment.md`

**User wants cost optimization:**
→ Provide GPU selection matrix, spot pricing, budget controls
→ Reference: `reference/cost-optimization.md`

**User on M1/M2 Mac:**
→ CRITICAL: Must use GitHub Actions for builds
→ Reference: `reference/cicd.md`

**User has deployment issues:**
→ Check health endpoint, review logs
→ Reference: `reference/troubleshooting.md`
</routing>

<cost_quick_ref>
## Cost Quick Reference

**Storage Costs:**
- Container disk: $0.10/GB/month (billed in 5-min intervals)
- Network volumes: $0.07/GB/month (first 1TB), $0.05/GB after

**Cost Estimation:**
```python
def estimate_monthly_cost(gpu_type, daily_requests, avg_time_s):
    rates = {"RTX_4090": 0.44, "A40": 0.65, "A100_80GB": 1.89}
    daily_hours = (daily_requests * avg_time_s) / 3600
    return daily_hours * 30 * rates.get(gpu_type, 1.0)

# Example: 1000 requests/day, 5s each, RTX 4090
# = (1000 * 5) / 3600 * 30 * 0.44 = $18.33/month
```
</cost_quick_ref>

<cli_commands>
## Quick CLI Commands

```bash
# Install
pip install runpod

# Deploy endpoint
runpodctl project deploy --name my-endpoint --gpu-type "NVIDIA RTX 4090"

# Health check
runpod endpoint health ENDPOINT_ID

# View logs
runpod endpoint logs ENDPOINT_ID

# Scale workers
runpod endpoint scale ENDPOINT_ID --min 1 --max 10

# Local testing
python handler.py --rp_serve_api
```
</cli_commands>

<example_session>
## Example Session

**User:** "Deploy a Llama 3.1 8B model to RunPod serverless"

**Claude:**
1. First, select GPU - 8B model fits on RTX 4090 ($0.44/hr):
```python
gpu_type = "NVIDIA GeForce RTX 4090"
```

2. Use vLLM for 2-3x throughput. Create endpoint with:
```python
env = {
    "MODEL_NAME": "meta-llama/Llama-3.1-8B-Instruct",
    "MAX_MODEL_LEN": "8192",
    "GPU_MEMORY_UTILIZATION": "0.95",
}
```

3. Access via OpenAI-compatible API:
```python
from openai import OpenAI
client = OpenAI(
    api_key="YOUR_KEY",
    base_url="https://api.runpod.ai/v2/ENDPOINT_ID/openai/v1",
)
```

4. Cost estimate: ~$0.44/hr compute, scale-to-zero when idle.
</example_session>
