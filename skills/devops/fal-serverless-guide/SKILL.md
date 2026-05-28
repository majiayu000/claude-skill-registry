---
name: fal-serverless-guide
description: Complete fal.ai serverless deployment system. PROACTIVELY activate for: (1) Creating fal.App class, (2) GPU machine selection (T4/A10G/A100/H100), (3) setup() for model loading, (4) @fal.endpoint decorators, (5) Persistent volumes for weights, (6) Secrets management, (7) Scaling configuration (min/max concurrency), (8) Multi-GPU deployment, (9) fal deploy commands, (10) Local development with fal run. Provides: App structure, Dockerfile patterns, deployment commands, scaling config. Ensures production-ready serverless ML deployment.
---

## Quick Reference

| Machine Type | GPU | VRAM | Use Case |
|--------------|-----|------|----------|
| `GPU-T4` | T4 | 16GB | Dev, small models |
| `GPU-A10G` | A10G | 24GB | 7B-13B models |
| `GPU-A100` | A100 | 40/80GB | 13B-70B models |
| `GPU-H100` | H100 | 80GB | Cutting-edge |

| App Attribute | Purpose | Example |
|---------------|---------|---------|
| `machine_type` | GPU selection | `"GPU-A100"` |
| `requirements` | Dependencies | `["torch", "transformers"]` |
| `keep_alive` | Warm duration | `300` (5 min) |
| `min_concurrency` | Min instances | `0` (scale to zero) |
| `max_concurrency` | Max parallel | `4` |

| Command | Purpose |
|---------|---------|
| `fal deploy app.py::MyApp` | Deploy to fal |
| `fal run app.py::MyApp` | Run locally |
| `fal logs <app-id>` | View logs |
| `fal secrets set KEY=value` | Set secrets |

## When to Use This Skill

Use for **custom model deployment**:
- Deploying custom ML models on fal infrastructure
- Configuring GPU instances and scaling
- Setting up persistent storage for model weights
- Creating multi-endpoint apps
- Managing secrets and environment variables

**Related skills:**
- For API integration: see `fal-api-reference`
- For optimization: see `fal-optimization`
- For using hosted models: see `fal-model-guide`

---

# fal.ai Serverless Deployment Guide

Complete guide to deploying custom ML models on fal.ai's serverless infrastructure.

## Overview

fal serverless provides:
- Automatic scaling from zero to thousands of instances
- GPU support (T4, A10G, A100, H100, H200, B200)
- Persistent storage for model weights
- Secrets management
- Real-time logs and monitoring
- Pay-per-use pricing

## Installation

```bash
pip install fal
```

## Authentication

```bash
# Login to fal
fal auth login

# Or set API key
export FAL_KEY="your-api-key"
```

## Basic App Structure

```python
import fal
from pydantic import BaseModel

class RequestModel(BaseModel):
    """Input schema for your endpoint"""
    prompt: str
    max_tokens: int = 100

class ResponseModel(BaseModel):
    """Output schema for your endpoint"""
    text: str
    tokens: int

class MyApp(fal.App):
    # Machine configuration
    machine_type = "GPU-A100"
    num_gpus = 1

    # Dependencies
    requirements = [
        "torch>=2.0.0",
        "transformers>=4.35.0",
        "accelerate"
    ]

    # Scaling configuration
    keep_alive = 300        # Keep instance warm (seconds)
    min_concurrency = 0     # Scale to zero when idle
    max_concurrency = 4     # Max concurrent requests

    def setup(self):
        """
        Called once when container starts.
        Load models and heavy resources here.
        """
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained("model-name")
        self.model = AutoModelForCausalLM.from_pretrained(
            "model-name",
            torch_dtype=torch.float16
        ).to(self.device)

    @fal.endpoint("/predict")
    def predict(self, request: RequestModel) -> ResponseModel:
        """
        Main inference endpoint.
        Called for each request.
        """
        inputs = self.tokenizer(request.prompt, return_tensors="pt")
        inputs = inputs.to(self.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=request.max_tokens
        )

        text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        return ResponseModel(text=text, tokens=len(outputs[0]))

    @fal.endpoint("/health")
    def health(self):
        """Health check endpoint"""
        return {"status": "healthy", "device": self.device}

    def teardown(self):
        """Called when container shuts down (optional)"""
        if hasattr(self, 'model'):
            del self.model
        import torch
        torch.cuda.empty_cache()
```

## Machine Types

| Type | GPU | VRAM | Use Case |
|------|-----|------|----------|
| `CPU` | None | - | Preprocessing, lightweight |
| `GPU-T4` | NVIDIA T4 | 16GB | Development, small models |
| `GPU-A10G` | NVIDIA A10G | 24GB | Medium models (7B-13B) |
| `GPU-A100` | NVIDIA A100 | 40/80GB | Large models (13B-70B) |
| `GPU-H100` | NVIDIA H100 | 80GB | Cutting-edge performance |
| `GPU-H200` | NVIDIA H200 | 141GB | Very large models |
| `GPU-B200` | NVIDIA B200 | 192GB | Frontier models (100B+) |

### Multi-GPU Configuration

```python
class MultiGPUApp(fal.App):
    machine_type = "GPU-H100"
    num_gpus = 4  # Use 4 H100s

    def setup(self):
        import torch
        from transformers import AutoModelForCausalLM

        self.model = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Llama-2-70b-hf",
            torch_dtype=torch.float16,
            device_map="auto"  # Distribute across GPUs
        )
```

## Persistent Storage

Use volumes to persist data across restarts:

```python
class AppWithStorage(fal.App):
    machine_type = "GPU-A100"
    requirements = ["torch", "transformers"]

    # Define persistent volumes
    volumes = {
        "/data": fal.Volume("model-cache"),
        "/outputs": fal.Volume("generated-outputs")
    }

    def setup(self):
        import os
        from transformers import AutoModel

        cache_dir = "/data/models"
        os.makedirs(cache_dir, exist_ok=True)

        # Model weights persist across cold starts
        self.model = AutoModel.from_pretrained(
            "large-model",
            cache_dir=cache_dir
        )

    @fal.endpoint("/generate")
    def generate(self, request):
        output_path = "/outputs/result.png"
        # Save to persistent storage
        return {"path": output_path}
```

## Secrets Management

```bash
# Set secrets via CLI
fal secrets set HF_TOKEN=hf_xxx API_KEY=sk_xxx

# List secrets
fal secrets list

# Delete secret
fal secrets delete HF_TOKEN
```

```python
import os

class SecureApp(fal.App):
    def setup(self):
        # Access secrets as environment variables
        hf_token = os.environ["HF_TOKEN"]

        from huggingface_hub import login
        login(token=hf_token)

        # Now can access gated models
        self.model = load_gated_model()
```

## Deployment Commands

```bash
# Deploy application
fal deploy app.py::MyApp

# Deploy with options
fal deploy app.py::MyApp \
  --machine-type GPU-A100 \
  --num-gpus 2 \
  --min-concurrency 1 \
  --max-concurrency 8

# View deployments
fal list

# View logs
fal logs <app-id>

# View real-time logs
fal logs <app-id> --follow

# Delete deployment
fal delete <app-id>

# Run locally for testing
fal run app.py::MyApp
```

## Advanced Patterns

### Image Generation App

```python
import fal
from pydantic import BaseModel
from typing import Optional
import io

class ImageRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = None
    width: int = 1024
    height: int = 1024
    steps: int = 28
    seed: Optional[int] = None

class ImageResponse(BaseModel):
    image_url: str
    seed: int

class ImageGenerator(fal.App):
    machine_type = "GPU-A100"
    requirements = [
        "torch",
        "diffusers",
        "transformers",
        "accelerate",
        "safetensors"
    ]
    keep_alive = 600
    max_concurrency = 2

    volumes = {
        "/data": fal.Volume("diffusion-models")
    }

    def setup(self):
        import torch
        from diffusers import StableDiffusionXLPipeline

        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16,
            cache_dir="/data/models"
        ).to("cuda")

        # Optimize
        self.pipe.enable_model_cpu_offload()

    @fal.endpoint("/generate")
    def generate(self, request: ImageRequest) -> ImageResponse:
        import torch
        import random

        seed = request.seed or random.randint(0, 2**32 - 1)
        generator = torch.Generator("cuda").manual_seed(seed)

        image = self.pipe(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            width=request.width,
            height=request.height,
            num_inference_steps=request.steps,
            generator=generator
        ).images[0]

        # Save and upload to CDN
        path = f"/tmp/output_{seed}.png"
        image.save(path)
        url = fal.upload_file(path)

        return ImageResponse(image_url=url, seed=seed)
```

### Streaming Response

```python
import fal
from typing import Generator

class StreamingApp(fal.App):
    machine_type = "GPU-A100"
    requirements = ["torch", "transformers"]

    def setup(self):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("model")
        self.model = AutoModelForCausalLM.from_pretrained("model")

    @fal.endpoint("/stream")
    def stream(self, prompt: str) -> Generator[str, None, None]:
        from transformers import TextIteratorStreamer
        from threading import Thread

        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)

        thread = Thread(
            target=self.model.generate,
            kwargs={**inputs, "streamer": streamer, "max_new_tokens": 256}
        )
        thread.start()

        for text in streamer:
            yield text
```

### Background Tasks

```python
import fal
from typing import Optional
import asyncio

class BackgroundApp(fal.App):
    machine_type = "GPU-A100"

    @fal.endpoint("/process")
    async def process(self, data: str) -> dict:
        # Submit background work
        task_id = await self.start_background_task(data)
        return {"task_id": task_id, "status": "processing"}

    async def start_background_task(self, data: str) -> str:
        # Implement your background logic
        import uuid
        task_id = str(uuid.uuid4())
        # Save task to queue/database
        return task_id
```

### Multiple Endpoints

```python
import fal
from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str

class ImageRequest(BaseModel):
    image_url: str

class MultiModalApp(fal.App):
    machine_type = "GPU-A100"
    requirements = ["torch", "transformers", "Pillow"]

    def setup(self):
        self.text_model = self.load_text_model()
        self.vision_model = self.load_vision_model()

    @fal.endpoint("/analyze-text")
    def analyze_text(self, request: TextRequest) -> dict:
        result = self.text_model(request.text)
        return {"analysis": result}

    @fal.endpoint("/analyze-image")
    def analyze_image(self, request: ImageRequest) -> dict:
        result = self.vision_model(request.image_url)
        return {"analysis": result}

    @fal.endpoint("/")
    def info(self) -> dict:
        return {
            "name": "MultiModal Analyzer",
            "endpoints": ["/analyze-text", "/analyze-image"]
        }

    @fal.endpoint("/health")
    def health(self) -> dict:
        return {"status": "healthy"}
```

## Scaling Configuration

```python
class ScaledApp(fal.App):
    machine_type = "GPU-A100"

    # Scaling options
    min_concurrency = 0     # Scale to zero (cost savings)
    max_concurrency = 10    # Max parallel requests
    keep_alive = 300        # Keep warm for 5 minutes

    # For always-on endpoints
    # min_concurrency = 1   # Always have one instance ready
```

### Concurrency Guidelines

| GPU Memory per Request | Suggested max_concurrency |
|-----------------------|---------------------------|
| < 4GB | 8-10 |
| 4-8GB | 4-6 |
| 8-16GB | 2-4 |
| 16-40GB | 1-2 |
| > 40GB | 1 |

## Error Handling

```python
import fal
from pydantic import BaseModel

class MyApp(fal.App):
    @fal.endpoint("/predict")
    def predict(self, request: dict):
        try:
            result = self.process(request)
            return {"result": result}
        except ValueError as e:
            # Client error
            raise fal.HTTPException(400, f"Invalid input: {e}")
        except RuntimeError as e:
            # Server error
            raise fal.HTTPException(500, f"Processing failed: {e}")
        except Exception as e:
            # Unexpected error
            raise fal.HTTPException(500, "Internal error")
```

## Local Development

```bash
# Run locally
fal run app.py::MyApp

# Test endpoint
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test"}'

# Run with environment variables
FAL_KEY=xxx HF_TOKEN=yyy fal run app.py::MyApp
```

## Calling Deployed Apps

### JavaScript/TypeScript

```typescript
import { fal } from "@fal-ai/client";

fal.config({ credentials: process.env.FAL_KEY });

const result = await fal.subscribe("your-username/your-app/predict", {
  input: {
    prompt: "Hello world",
    max_tokens: 100
  }
});
```

### Python

```python
import fal_client

result = fal_client.subscribe(
    "your-username/your-app/predict",
    arguments={
        "prompt": "Hello world",
        "max_tokens": 100
    }
)
```

### REST API

```bash
curl -X POST "https://queue.fal.run/your-username/your-app/predict" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello world", "max_tokens": 100}'
```

## Best Practices

1. **Load models in setup()**
   - Heavy initialization once, not per request
   - Use persistent volumes for large weights

2. **Use appropriate machine type**
   - Match GPU memory to model size
   - Consider cost vs performance trade-offs

3. **Handle cold starts**
   - Use `keep_alive` for frequently accessed endpoints
   - Use `min_concurrency=1` for latency-critical apps

4. **Optimize memory**
   - Use fp16/bf16 where possible
   - Enable memory-efficient attention
   - Clear GPU cache in teardown

5. **Monitor and debug**
   - Check logs regularly: `fal logs <app-id> --follow`
   - Implement health checks
   - Use structured logging

6. **Security**
   - Use secrets for API keys
   - Validate all inputs
   - Don't expose internal errors

## Pricing

- Pay per second of compute used
- Different rates for different GPU types
- No charge when scaled to zero
- Check https://fal.ai/pricing for current rates
