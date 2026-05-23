---
name: gpu
description: |
  GPU monitoring and performance metrics for Ollama inference. Check GPU
  status, VRAM usage, loaded models, and inference performance metrics
  like tokens per second.
---

# GPU Monitoring for Ollama

## Overview

Monitor GPU usage and performance when running Ollama with GPU acceleration. This skill covers checking GPU status, VRAM usage, models loaded in GPU memory, and inference performance metrics.

## Quick Reference

| Check | Method |
|-------|--------|
| GPU status | `nvidia-smi` / `rocm-smi` |
| Models in memory | `GET /api/ps` |
| Inference metrics | Response metadata |
| VRAM usage | Both nvidia-smi and /api/ps |

## GPU Status Check

### NVIDIA

```python
import subprocess

def check_nvidia_gpu():
    """Check NVIDIA GPU status."""
    try:
        result = subprocess.run(
            ["nvidia-smi",
             "--query-gpu=name,memory.used,memory.total,utilization.gpu",
             "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            for i, line in enumerate(lines):
                parts = line.split(", ")
                if len(parts) >= 4:
                    name, mem_used, mem_total, util = parts
                    print(f"GPU {i}: {name}")
                    print(f"  Memory: {mem_used} MB / {mem_total} MB")
                    print(f"  Utilization: {util}%")
    except FileNotFoundError:
        print("nvidia-smi not found - NVIDIA GPU may not be available")
    except subprocess.TimeoutExpired:
        print("nvidia-smi timed out")

check_nvidia_gpu()
```

### AMD

```python
import subprocess

def check_amd_gpu():
    """Check AMD GPU status."""
    try:
        result = subprocess.run(
            ["rocm-smi", "--showmeminfo", "vram"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print(result.stdout)
    except FileNotFoundError:
        print("rocm-smi not found - AMD GPU may not be available")

check_amd_gpu()
```

## Models Loaded in GPU Memory

```python
import os
import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

response = requests.get(f"{OLLAMA_HOST}/api/ps")
running = response.json()

if running.get("models"):
    print("=== Models Loaded in GPU Memory ===")
    for model in running["models"]:
        name = model.get("name", "Unknown")
        size = model.get("size", 0) / (1024**3)
        vram = model.get("size_vram", 0) / (1024**3)
        expires = model.get("expires_at", "N/A")
        print(f"  - {name}")
        print(f"    Total Size: {size:.2f} GB")
        print(f"    VRAM Usage: {vram:.2f} GB")
        print(f"    Expires: {expires}")
else:
    print("No models currently loaded in memory")
```

## Inference Performance Metrics

```python
import os
import time
import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Run inference
start_time = time.perf_counter()
response = requests.post(
    f"{OLLAMA_HOST}/api/generate",
    json={
        "model": "llama3.2:latest",
        "prompt": "Write a haiku about computers.",
        "stream": False
    }
)
end_time = time.perf_counter()

result = response.json()

print(f"Response: {result['response']}")
print()
print("=== Inference Metrics ===")
print(f"Wall clock time: {end_time - start_time:.2f}s")
print(f"Prompt eval count: {result.get('prompt_eval_count', 'N/A')}")
print(f"Prompt eval duration: {result.get('prompt_eval_duration', 0) / 1e9:.3f}s")
print(f"Eval count (tokens generated): {result.get('eval_count', 'N/A')}")
print(f"Eval duration: {result.get('eval_duration', 0) / 1e9:.3f}s")
print(f"Total duration: {result.get('total_duration', 0) / 1e9:.3f}s")

if result.get('eval_count') and result.get('eval_duration'):
    tokens_per_sec = result['eval_count'] / (result['eval_duration'] / 1e9)
    print(f"Tokens/second: {tokens_per_sec:.1f}")
```

## GPU Usage During Inference

```python
import os
import subprocess
import requests
import threading
import time

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

def monitor_gpu(stop_event, readings):
    """Monitor GPU usage in background."""
    while not stop_event.is_set():
        try:
            result = subprocess.run(
                ["nvidia-smi",
                 "--query-gpu=utilization.gpu,memory.used",
                 "--format=csv,noheader,nounits"],
                capture_output=True,
                text=True,
                timeout=1
            )
            if result.returncode == 0:
                parts = result.stdout.strip().split(", ")
                if len(parts) >= 2:
                    readings.append({
                        "util": int(parts[0]),
                        "mem": int(parts[1])
                    })
        except:
            pass
        time.sleep(0.5)

# Start monitoring
stop_event = threading.Event()
readings = []
monitor_thread = threading.Thread(target=monitor_gpu, args=(stop_event, readings))
monitor_thread.start()

# Run inference
response = requests.post(
    f"{OLLAMA_HOST}/api/generate",
    json={
        "model": "llama3.2:latest",
        "prompt": "Write a short story about AI.",
        "stream": False
    }
)

# Stop monitoring
stop_event.set()
monitor_thread.join()

# Report
if readings:
    avg_util = sum(r["util"] for r in readings) / len(readings)
    max_mem = max(r["mem"] for r in readings)
    print(f"Average GPU utilization: {avg_util:.1f}%")
    print(f"Peak memory usage: {max_mem} MB")
```

## Complete Health Check

```python
import os
import subprocess
import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = "llama3.2:latest"

def complete_gpu_health_check():
    """Complete GPU and Ollama health check."""
    print("=== GPU Health Check ===")
    print()

    # 1. Check GPU hardware
    print("1. GPU Hardware:")
    try:
        result = subprocess.run(
            ["nvidia-smi",
             "--query-gpu=name,memory.total",
             "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"   {result.stdout.strip()}")
        else:
            print("   nvidia-smi failed")
    except FileNotFoundError:
        print("   NVIDIA GPU not detected")

    # 2. Check Ollama server
    print()
    print("2. Ollama Server:")
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if response.status_code == 200:
            print("   Server is running")
            models = response.json()
            model_names = [m.get("name", "") for m in models.get("models", [])]
            if DEFAULT_MODEL in model_names:
                print(f"   Model '{DEFAULT_MODEL}' available")
            else:
                print(f"   Model '{DEFAULT_MODEL}' NOT available")
        else:
            print(f"   Server error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   Cannot connect to server")

    # 3. Check models in GPU memory
    print()
    print("3. Models in GPU Memory:")
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/ps")
        running = response.json()
        if running.get("models"):
            for model in running["models"]:
                vram = model.get("size_vram", 0) / (1024**3)
                print(f"   {model['name']}: {vram:.2f} GB VRAM")
        else:
            print("   No models loaded")
    except:
        print("   Cannot check running models")

complete_gpu_health_check()
```

## Model Size Guide

| Model | Parameters | VRAM Needed | Tokens/sec (typical) |
|-------|------------|-------------|----------------------|
| phi3 | 3B | 4GB | 60-80 |
| llama3.2 | 8B | 8GB | 40-60 |
| mistral | 7B | 8GB | 40-60 |
| codellama | 7B | 8GB | 40-60 |
| llama3.2:70b | 70B | 48GB+ | 10-20 |

## Troubleshooting

### GPU Not Used

**Symptom:** Low tokens/second, nvidia-smi shows 0% utilization

**Check:**

```bash
# Check GPU inside container (adjust container name as needed)
docker exec -it ollama nvidia-smi
# or
podman exec -it ollama nvidia-smi
```

**Fix:**

```bash
# Restart Ollama container with GPU access
# Refer to bazzite-ai-pod-ollama documentation for container setup
```

### Out of Memory

**Symptom:** "out of memory" error during model loading

**Fix:**

```python
# Use smaller/quantized model via API
import requests
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

response = requests.post(
    f"{OLLAMA_HOST}/api/pull",
    json={"name": "llama3.2:7b-q4_0"},
    stream=True
)
for line in response.iter_lines():
    if line:
        print(line.decode())
```

### Slow Inference

**Symptom:** Very low tokens/second

**Possible causes:**
1. Model too large for VRAM (using CPU fallback)
2. Wrong GPU type configured
3. Driver issues

**Check:**

```python
# Check VRAM usage vs model size
response = requests.get(f"{OLLAMA_HOST}/api/ps")
# If size_vram << size, model is partially on CPU
```

## When to Use This Skill

Use when:
- Debugging slow inference
- Checking if GPU is being utilized
- Monitoring VRAM usage
- Benchmarking different models
- Troubleshooting GPU issues

## Cross-References

- `bazzite-ai-jupyter:chat` - API for running inference
- `bazzite-ai-jupyter:ollama` - Python library for inference
