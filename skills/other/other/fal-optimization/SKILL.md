---
name: fal-optimization
description: Complete fal.ai optimization system. PROACTIVELY activate for: (1) Queue vs run performance, (2) Parallel request batching, (3) Streaming for real-time UI, (4) WebSocket for interactive apps, (5) Model cost comparison, (6) Image size optimization, (7) Inference step tuning, (8) Webhook vs polling, (9) Result caching by seed, (10) Serverless scaling config. Provides: Parallel patterns, cost strategies, caching examples, monitoring setup. Ensures optimal performance and cost-effective usage.
---

## Quick Reference

| Optimization | Technique | Impact |
|--------------|-----------|--------|
| Parallel requests | `Promise.all()` with batches | 5-10x throughput |
| Avoid polling | Use webhooks | Lower API calls |
| Cache by seed | Store `prompt+seed` results | Avoid regeneration |
| Right-size images | Use needed resolution | Lower cost |
| Fewer steps | Reduce inference steps | Faster, cheaper |

| Model Tier | Development | Production |
|------------|-------------|------------|
| Image | FLUX Schnell | FLUX.2 Pro |
| Video | Runway Turbo | Kling 2.6 Pro |

| Serverless Config | Cost-Optimized | Latency-Optimized |
|-------------------|----------------|-------------------|
| `min_concurrency` | `0` | `1+` |
| `keep_alive` | `120` | `600+` |
| `machine_type` | Smallest viable | Higher tier |

## When to Use This Skill

Use for **performance and cost optimization**:
- Reducing generation latency
- Lowering API costs
- Implementing parallel processing
- Choosing between polling and webhooks
- Configuring serverless scaling

**Related skills:**
- For API patterns: see `fal-api-reference`
- For model selection: see `fal-model-guide`
- For serverless config: see `fal-serverless-guide`

---

# fal.ai Performance and Cost Optimization

Strategies for optimizing performance, reducing costs, and scaling fal.ai integrations.

## Performance Optimization

### Client-Side Optimizations

#### 1. Use Queue-Based Execution

Always prefer `subscribe()` over `run()` for generation tasks:

```typescript
// Recommended: Queue-based with progress tracking
const result = await fal.subscribe("fal-ai/flux/dev", {
  input: { prompt: "test" },
  logs: true,
  onQueueUpdate: (update) => {
    // Show progress to users
    if (update.status === "IN_PROGRESS") {
      console.log("Generating...");
    }
  }
});

// Only use run() for fast endpoints (< 30s)
const quickResult = await fal.run("fal-ai/fast-sdxl", {
  input: { prompt: "quick test" }
});
```

#### 2. Parallel Requests

Process multiple requests concurrently:

```typescript
// JavaScript - Parallel execution
async function generateBatch(prompts: string[]) {
  const results = await Promise.all(
    prompts.map(prompt =>
      fal.subscribe("fal-ai/flux/dev", {
        input: { prompt }
      })
    )
  );
  return results;
}

// With rate limiting
async function generateBatchWithLimit(prompts: string[], limit = 5) {
  const results = [];
  for (let i = 0; i < prompts.length; i += limit) {
    const batch = prompts.slice(i, i + limit);
    const batchResults = await Promise.all(
      batch.map(prompt =>
        fal.subscribe("fal-ai/flux/dev", { input: { prompt } })
      )
    );
    results.push(...batchResults);
    // Small delay between batches
    if (i + limit < prompts.length) {
      await new Promise(r => setTimeout(r, 100));
    }
  }
  return results;
}
```

```python
# Python - Async parallel
import asyncio
import fal_client

async def generate_batch(prompts: list[str]) -> list[dict]:
    tasks = [
        fal_client.run_async("fal-ai/flux/dev", arguments={"prompt": p})
        for p in prompts
    ]
    return await asyncio.gather(*tasks)

# With semaphore for rate limiting
async def generate_batch_limited(prompts: list[str], limit: int = 5):
    semaphore = asyncio.Semaphore(limit)

    async def generate_one(prompt: str):
        async with semaphore:
            return await fal_client.run_async(
                "fal-ai/flux/dev",
                arguments={"prompt": prompt}
            )

    return await asyncio.gather(*[generate_one(p) for p in prompts])
```

#### 3. Streaming for Real-Time Feedback

Use streaming for progressive output:

```typescript
// Show incremental progress
const stream = await fal.stream("fal-ai/flux/dev", {
  input: { prompt: "A landscape" }
});

for await (const event of stream) {
  updateProgressUI(event);
}

const result = await stream.done();
```

#### 4. WebSockets for Interactive Apps

For real-time applications with continuous input:

```typescript
const connection = fal.realtime.connect("fal-ai/lcm-sd15-i2i", {
  connectionKey: `user-${userId}`,
  throttleInterval: 128,  // Debounce rapid inputs
  onResult: (result) => {
    displayImage(result.images[0].url);
  }
});

// Send updates as user types/draws
inputElement.addEventListener('input', (e) => {
  connection.send({
    prompt: e.target.value,
    image_url: currentImage
  });
});
```

### Server-Side Optimizations (Serverless)

#### 1. Efficient Model Loading

```python
class OptimizedApp(fal.App):
    machine_type = "GPU-A100"
    requirements = ["torch", "transformers", "accelerate"]

    volumes = {
        "/data": fal.Volume("model-cache")
    }

    def setup(self):
        import torch
        from transformers import AutoModelForCausalLM

        # Use fp16 for faster inference and less memory
        self.model = AutoModelForCausalLM.from_pretrained(
            "model-name",
            torch_dtype=torch.float16,
            device_map="auto",
            cache_dir="/data/models"  # Persistent cache
        )

        # Enable optimizations
        if hasattr(self.model, 'enable_attention_slicing'):
            self.model.enable_attention_slicing()
```

#### 2. Reduce Cold Starts

```python
class WarmApp(fal.App):
    machine_type = "GPU-A100"
    keep_alive = 600      # 10 minutes warm
    min_concurrency = 1   # Always keep one ready

    # Use lightweight health check
    @fal.endpoint("/health")
    def health(self):
        return {"status": "ok"}
```

#### 3. Memory Management

```python
class MemoryEfficientApp(fal.App):
    def setup(self):
        import torch

        # Use mixed precision
        self.model = load_model(torch_dtype=torch.float16)

        # Enable memory-efficient attention (if using transformers)
        self.model.enable_xformers_memory_efficient_attention()

    def teardown(self):
        # Clean up GPU memory
        import torch
        if hasattr(self, 'model'):
            del self.model
        torch.cuda.empty_cache()

    @fal.endpoint("/generate")
    def generate(self, request):
        import torch

        with torch.inference_mode():  # Disable gradient tracking
            result = self.model(request.input)

        return result
```

## Cost Optimization

### 1. Choose the Right Model

| Need | Cheaper Option | Premium Option |
|------|---------------|----------------|
| Quick iteration | FLUX Schnell ($) | FLUX.1 Dev ($$) |
| Production | FLUX.1 Dev ($$) | FLUX.2 Pro ($$$) |
| Video preview | Runway Turbo ($$) | Kling Pro ($$$) |

```typescript
// Development: Use fast/cheap models
const preview = await fal.subscribe("fal-ai/flux/schnell", {
  input: { prompt: "test", num_inference_steps: 4 }
});

// Production: Use quality models
const final = await fal.subscribe("fal-ai/flux-2-pro", {
  input: { prompt: "test" }
});
```

### 2. Optimize Image Sizes

Generate at the size you need, not larger:

```typescript
// Don't generate larger than needed
const result = await fal.subscribe("fal-ai/flux/dev", {
  input: {
    prompt: "test",
    // Use preset sizes
    image_size: "square_hd",  // 1024x1024

    // Or specific dimensions
    image_size: { width: 800, height: 600 }
  }
});
```

### 3. Reduce Inference Steps

Find the minimum steps for acceptable quality:

```typescript
// Quick previews: fewer steps
const preview = await fal.subscribe("fal-ai/flux/dev", {
  input: {
    prompt: "test",
    num_inference_steps: 15  // Faster, slightly lower quality
  }
});

// Final render: more steps
const final = await fal.subscribe("fal-ai/flux/dev", {
  input: {
    prompt: "test",
    num_inference_steps: 28  // Default, high quality
  }
});
```

### 4. Use Webhooks for High Volume

Avoid polling overhead with webhooks:

```typescript
// Instead of polling
const result = await fal.subscribe("fal-ai/flux/dev", {
  input: { prompt: "test" },
  pollInterval: 1000  // Polling = more API calls
});

// Use webhooks
const { request_id } = await fal.queue.submit("fal-ai/flux/dev", {
  input: { prompt: "test" },
  webhookUrl: "https://your-server.com/webhook"
});
// No polling needed - result delivered to webhook
```

### 5. Cache Results

Use seeds for reproducible outputs:

```typescript
// Cache key based on prompt + seed
const cacheKey = `${prompt}-${seed}`;
const cached = await cache.get(cacheKey);

if (cached) {
  return cached;
}

const result = await fal.subscribe("fal-ai/flux/dev", {
  input: { prompt, seed }
});

await cache.set(cacheKey, result);
return result;
```

### 6. Serverless Cost Optimization

```python
class CostOptimizedApp(fal.App):
    machine_type = "GPU-A10G"   # Cheaper than A100 if sufficient
    min_concurrency = 0         # Scale to zero when not used
    keep_alive = 120            # Shorter keep-alive

    # Use appropriate GPU for model size
    # T4: < 16GB VRAM models
    # A10G: 16-24GB VRAM models
    # A100: 24-80GB VRAM models
```

## Scaling Strategies

### 1. Horizontal Scaling

```python
class ScalableApp(fal.App):
    machine_type = "GPU-A100"
    min_concurrency = 2    # Always have 2 instances
    max_concurrency = 20   # Scale up to 20

    # fal handles auto-scaling based on queue depth
```

### 2. Request Batching

```python
class BatchApp(fal.App):
    @fal.endpoint("/batch")
    def batch_generate(self, prompts: list[str]) -> list[dict]:
        # Process multiple prompts in one request
        results = []
        for prompt in prompts:
            result = self.model(prompt)
            results.append(result)
        return results
```

### 3. Priority Queues

Use different endpoints for different priorities:

```python
class PriorityApp(fal.App):
    machine_type = "GPU-A100"

    @fal.endpoint("/high-priority")
    def high_priority(self, request):
        # Separate endpoint for important requests
        return self.process(request)

    @fal.endpoint("/standard")
    def standard(self, request):
        # Standard processing
        return self.process(request)
```

## Monitoring and Debugging

### 1. Add Logging

```python
import logging

class MonitoredApp(fal.App):
    def setup(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info("App starting up")
        # Load model
        self.logger.info("Model loaded successfully")

    @fal.endpoint("/generate")
    def generate(self, request):
        import time
        start = time.time()

        result = self.process(request)

        elapsed = time.time() - start
        self.logger.info(f"Request processed in {elapsed:.2f}s")

        return result
```

### 2. Track Metrics

```typescript
// Client-side timing
const start = Date.now();

const result = await fal.subscribe("fal-ai/flux/dev", {
  input: { prompt: "test" },
  onQueueUpdate: (update) => {
    if (update.status === "IN_QUEUE") {
      console.log(`Queue position: ${update.queue_position}`);
    }
  }
});

const elapsed = Date.now() - start;
console.log(`Total time: ${elapsed}ms`);

// Track in your analytics
analytics.track("fal_generation", {
  model: "flux/dev",
  elapsed_ms: elapsed,
  queue_time_ms: result.timings?.queue,
  inference_time_ms: result.timings?.inference
});
```

### 3. Error Monitoring

```typescript
try {
  const result = await fal.subscribe("fal-ai/flux/dev", {
    input: { prompt: "test" }
  });
} catch (error) {
  // Log to error tracking service
  errorTracker.captureException(error, {
    tags: {
      model: "flux/dev",
      type: error.constructor.name
    },
    extra: {
      status: error.status,
      body: error.body
    }
  });

  // Handle gracefully
  return fallbackResult();
}
```

## Checklist

### Before Production

- [ ] Using queue-based execution (`subscribe`)
- [ ] Appropriate model selected for use case
- [ ] Image sizes optimized
- [ ] Error handling implemented
- [ ] Rate limiting in place
- [ ] Caching strategy defined

### Serverless Deployment

- [ ] Correct machine type for model size
- [ ] Models loaded in `setup()`, not per-request
- [ ] Persistent volumes for large models
- [ ] Secrets properly configured
- [ ] Health check endpoint
- [ ] Logging enabled

### Cost Management

- [ ] Scale-to-zero enabled (`min_concurrency = 0`)
- [ ] Appropriate `keep_alive` setting
- [ ] Using cheaper models for development
- [ ] Batch processing where possible
- [ ] Webhook callbacks instead of polling

### Monitoring

- [ ] Latency tracking
- [ ] Error rate monitoring
- [ ] Cost tracking
- [ ] Queue depth alerts
