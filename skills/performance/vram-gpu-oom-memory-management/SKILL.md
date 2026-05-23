---
name: Vram-GPU-OOM
description: GPU VRAM management patterns for sharing memory across services (Ollama, Whisper, ComfyUI). OOM retry logic, auto-unload on idle, and service signaling protocol.
---

# GPU OOM Retry Pattern

Simple pattern for sharing GPU memory across multiple services without coordination.

## Strategy
1. All services try to load models normally
2. Catch OOM errors
3. Wait 30-60 seconds (for other services to auto-unload)
4. Retry up to 3 times
5. Configure all services to unload quickly when idle

## Python (PyTorch / Transformers)

```python
import torch
import time

def load_model_with_retry(max_retries=3, retry_delay=30):
    for attempt in range(max_retries):
        try:
            # Your model loading code
            model = MyModel.from_pretrained("model-name")
            model.to("cuda")
            return model

        except RuntimeError as e:
            if "out of memory" in str(e).lower():
                if attempt < max_retries - 1:
                    print(f"OOM on attempt {attempt+1}, waiting {retry_delay}s...")
                    torch.cuda.empty_cache()  # Clean up
                    time.sleep(retry_delay)
                else:
                    raise  # Give up after max retries
            else:
                raise  # Not OOM, raise immediately
```

## ComfyUI / Flux (Python-based)

Add to your workflow/node:

```python
# In your model loading function
import torch
import time

def load_flux_model(path, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Your Flux/ComfyUI loading code
            model = comfy.utils.load_torch_file(path)
            return model
        except RuntimeError as e:
            if "out of memory" in str(e).lower():
                if attempt < max_retries - 1:
                    print(f"GPU busy, retrying in 30s...")
                    torch.cuda.empty_cache()
                    time.sleep(30)
                else:
                    raise
            else:
                raise
```

## Ollama

Ollama already handles this! Just configure quick unloading:

```bash
# In /etc/systemd/system/ollama.service.d/override.conf
Environment="OLLAMA_KEEP_ALIVE=30s"
```

## Shell Scripts

For any GPU command:

```bash
#!/bin/bash
MAX_RETRIES=3
RETRY_DELAY=30

for i in $(seq 1 $MAX_RETRIES); do
    if your-gpu-command; then
        exit 0
    fi

    if [ $i -lt $MAX_RETRIES ]; then
        echo "GPU busy, retrying in ${RETRY_DELAY}s..."
        sleep $RETRY_DELAY
    fi
done

echo "Failed after $MAX_RETRIES attempts"
exit 1
```

## Service Signaling Protocol (Optional Enhancement)

For better coordination, services can implement these endpoints:

### 1. Auto-Unload on Idle

Services can automatically unload models after idle timeout:

```python
# FastAPI example
import asyncio
import time

last_request_time = None
auto_unload_minutes = 5  # configurable

async def auto_unload_task():
    """Background task that unloads model after idle timeout."""
    while True:
        await asyncio.sleep(60)  # Check every minute

        if current_handler is None:
            continue

        idle = time.time() - last_request_time
        if idle > (auto_unload_minutes * 60):
            logger.info(f"Auto-unloading model after {idle/60:.1f} minutes")
            current_handler.unload()
            current_handler = None

@app.on_event("startup")
async def startup():
    asyncio.create_task(auto_unload_task())
```

### 2. Request-Unload Endpoint

Allow other services to politely request unload:

```python
@app.post("/request-unload")
async def request_unload():
    """Request model unload if idle."""
    if current_handler is None:
        return {"status": "ok", "unloaded": False, "message": "No model loaded"}

    idle = time.time() - last_request_time

    # Only unload if idle for at least 30 seconds
    if idle < 30:
        return {
            "status": "busy",
            "unloaded": False,
            "message": f"Model in use (idle {idle:.0f}s)",
            "idle_seconds": idle,
        }

    # Unload the model
    logger.info("Unloading on request from another service")
    current_handler.unload()
    current_handler = None

    return {
        "status": "ok",
        "unloaded": True,
        "message": "Model unloaded",
        "idle_seconds": idle,
    }
```

### 3. Enhanced Status Endpoint

```python
@app.get("/status")
async def get_status():
    idle = time.time() - last_request_time if last_request_time else None
    return {
        "status": "ok",
        "model_loaded": current_handler is not None,
        "idle_seconds": idle,
        "auto_unload_enabled": auto_unload_minutes is not None,
        "auto_unload_minutes": auto_unload_minutes,
    }
```

### 4. Using the Protocol

Before loading a large model, request other services to unload:

```python
import requests

SERVICES = [
    "http://10.99.0.3:8765",  # Invoice OCR
    # Add other services here
]

for service in SERVICES:
    try:
        resp = requests.post(f"{service}/request-unload", timeout=5)
        result = resp.json()
        if result.get("unloaded"):
            print(f"✓ {service} unloaded")
        elif result.get("status") == "busy":
            print(f"⏱ {service} busy, will retry OOM")
    except:
        pass  # Service not available

# Now try to load your model (with OOM retry as backup)
```

**Helper script:** See `request_gpu_unload.py` in OneCuriousRabbit repo.

## Key Settings

### Invoice OCR (Qwen2-VL)
✅ OOM retry: 3x with 30s delays
✅ Auto-unload: 5 minutes idle (configurable via `--auto-unload-minutes`)
✅ Request-unload endpoint: `POST http://10.99.0.3:8765/request-unload`

### Ollama
✅ Auto-unload: `OLLAMA_KEEP_ALIVE=30s` in systemd override

### Your Other Services
1. Implement OOM retry pattern (required)
2. Optionally implement signaling protocol (auto-unload + request-unload endpoints)

## How It Works

### Passive (OOM Retry Only)

**12:00** - Scheduled Qwen task starts, loads 4GB
**12:01** - User uploads invoice, tries to load 18GB → OOM
**12:01** - Invoice OCR waits 30s
**12:01:30** - Qwen task finishes, auto-unloads after 30s
**12:02** - Invoice OCR retry succeeds, loads 18GB
**12:03** - Invoice processing completes, unloads
**12:03:30** - GPU is free again

### Active (With Signaling)

**12:00** - User starts Flux generation
**12:00** - Flux calls `POST /request-unload` on Invoice OCR
**12:00** - Invoice OCR idle for 4 minutes → unloads immediately
**12:00** - Flux loads its model (22GB) successfully
**12:05** - Flux completes, auto-unloads after 5 minutes

**Benefits of signaling:**
- Faster starts (no waiting for OOM retry delays)
- More predictable behavior
- Can request unload proactively before attempting load
- OOM retry still works as fallback if service is busy
