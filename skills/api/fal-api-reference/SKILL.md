---
name: fal-api-reference
description: Complete fal.ai API reference system. PROACTIVELY activate for: (1) @fal-ai/client JavaScript setup, (2) fal_client Python setup, (3) fal.subscribe/run/stream methods, (4) Queue management (submit/status/result), (5) Webhook configuration, (6) File upload to fal.media, (7) REST API endpoints, (8) Real-time WebSocket connections, (9) Error handling patterns. Provides: Client configuration, method signatures, queue workflow, webhook payloads, common parameters. Ensures correct API usage with proper authentication and error handling.
---

## Quick Reference

| Method | Use Case | Code |
|--------|----------|------|
| `fal.subscribe()` | Queue-based (recommended) | `await fal.subscribe("model", { input })` |
| `fal.run()` | Fast endpoints (<30s) | `await fal.run("model", { input })` |
| `fal.stream()` | Progressive output | `for await (const event of stream) {}` |
| `fal.realtime.connect()` | WebSocket interactive | `fal.realtime.connect("model", callbacks)` |

| Queue Method | Purpose |
|--------------|---------|
| `fal.queue.submit()` | Submit job, get request_id |
| `fal.queue.status()` | Check job status |
| `fal.queue.result()` | Get completed result |
| `fal.queue.cancel()` | Cancel pending job |

| Auth | Header | Format |
|------|--------|--------|
| API Key | `Authorization` | `Key YOUR_FAL_KEY` |

## When to Use This Skill

Use for **API integration fundamentals**:
- Setting up fal.ai client in JavaScript/TypeScript
- Setting up fal_client in Python
- Choosing between subscribe, run, and stream methods
- Implementing webhook callbacks
- Uploading files to fal.media CDN

**Related skills:**
- For model selection: see `fal-model-guide`
- For performance optimization: see `fal-optimization`
- For custom model deployment: see `fal-serverless-guide`

---

# fal.ai API Reference

Complete API reference for fal.ai client libraries and REST endpoints.

## Client Libraries

### JavaScript/TypeScript (@fal-ai/client)

```bash
npm install @fal-ai/client
```

#### Configuration

```typescript
import { fal } from "@fal-ai/client";

// Configure credentials (reads FAL_KEY from environment by default)
fal.config({
  credentials: process.env.FAL_KEY,
  // Optional: custom proxy URL for browser apps
  proxyUrl: "https://your-server.com/api/fal-proxy"
});
```

#### Core Methods

**fal.subscribe(endpoint, options)**
Queue-based execution with automatic polling. Recommended for most use cases.

```typescript
const result = await fal.subscribe("fal-ai/flux/dev", {
  input: {
    prompt: "A beautiful landscape"
  },
  logs: true,
  pollInterval: 1000,  // Poll every second (default: 1000)
  onQueueUpdate: (update) => {
    // update.status: "IN_QUEUE" | "IN_PROGRESS" | "COMPLETED"
    if (update.status === "IN_PROGRESS") {
      update.logs?.forEach(log => console.log(log.message));
    }
  }
});
```

**fal.run(endpoint, options)**
Direct/synchronous execution. Use only for fast endpoints (< 30 seconds).

```typescript
const result = await fal.run("fal-ai/fast-sdxl", {
  input: { prompt: "A cat" }
});
```

**fal.stream(endpoint, options)**
Server-sent events for progressive output.

```typescript
const stream = await fal.stream("fal-ai/flux/dev", {
  input: { prompt: "A landscape" }
});

for await (const event of stream) {
  console.log("Progress:", event);
}

const finalResult = await stream.done();
```

**fal.realtime.connect(endpoint, callbacks)**
WebSocket connection for real-time interactive applications.

```typescript
const connection = fal.realtime.connect("fal-ai/lcm-sd15-i2i", {
  connectionKey: "unique-session-id",
  throttleInterval: 128,  // Debounce inputs (ms)
  onResult: (result) => console.log("Generated:", result),
  onError: (error) => console.error("Error:", error),
  onOpen: () => console.log("Connected"),
  onClose: () => console.log("Disconnected")
});

// Send inputs
connection.send({
  prompt: "A cute cat",
  image_url: "https://example.com/base.jpg"
});

// Close when done
connection.close();
```

#### Queue Methods

Manual queue management for advanced control.

```typescript
// Submit to queue
const { request_id } = await fal.queue.submit("fal-ai/flux/dev", {
  input: { prompt: "Test" },
  webhookUrl: "https://your-server.com/webhook"  // Optional
});

// Check status
const status = await fal.queue.status("fal-ai/flux/dev", {
  requestId: request_id,
  logs: true
});
// status.status: "IN_QUEUE" | "IN_PROGRESS" | "COMPLETED"

// Get result (blocks until complete)
const result = await fal.queue.result("fal-ai/flux/dev", {
  requestId: request_id
});

// Cancel request
await fal.queue.cancel("fal-ai/flux/dev", {
  requestId: request_id
});
```

#### Storage Methods

Upload files to fal.media CDN.

```typescript
// Upload File object
const file = new File([blob], "image.png", { type: "image/png" });
const url = await fal.storage.upload(file);

// Upload from URL
const response = await fetch("https://example.com/image.jpg");
const blob = await response.blob();
const url = await fal.storage.upload(new File([blob], "image.jpg"));
```

### Python (fal-client)

```bash
pip install fal-client
```

#### Synchronous API

```python
import fal_client

# Simple run
result = fal_client.run(
    "fal-ai/flux/dev",
    arguments={
        "prompt": "A beautiful landscape",
        "image_size": "landscape_16_9"
    }
)

# Subscribe with status updates
def on_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(log["message"])

result = fal_client.subscribe(
    "fal-ai/flux/dev",
    arguments={"prompt": "Test"},
    with_logs=True,
    on_queue_update=on_update
)

# Manual queue management
handler = fal_client.submit(
    "fal-ai/flux/dev",
    arguments={"prompt": "Test"}
)
print(f"Request ID: {handler.request_id}")
status = handler.status()  # Check status
result = handler.get()     # Block until complete
```

#### Async API

```python
import asyncio
import fal_client

async def generate():
    # Async run
    result = await fal_client.run_async(
        "fal-ai/flux/dev",
        arguments={"prompt": "Test"}
    )

    # Async subscribe
    result = await fal_client.subscribe_async(
        "fal-ai/flux/dev",
        arguments={"prompt": "Test"},
        with_logs=True
    )

    # Async queue management
    handler = await fal_client.submit_async(
        "fal-ai/flux/dev",
        arguments={"prompt": "Test"}
    )
    status = await handler.status_async()
    result = await handler.get_async()

    return result

result = asyncio.run(generate())
```

#### File Upload

```python
# Upload file from path
url = fal_client.upload_file("path/to/image.png")

# Upload bytes
with open("image.png", "rb") as f:
    url = fal_client.upload(f.read(), "image/png")

# Encode as data URL (small files only)
data_url = fal_client.encode_file("small_image.png")
```

## REST API

### Base URLs

| Purpose | URL Pattern |
|---------|------------|
| Queue Submit | `https://queue.fal.run/{model_id}` |
| Queue Status | `https://queue.fal.run/{model_id}/requests/{request_id}/status` |
| Queue Result | `https://queue.fal.run/{model_id}/requests/{request_id}` |
| Queue Cancel | `https://queue.fal.run/{model_id}/requests/{request_id}/cancel` |
| Direct Run | `https://fal.run/{model_id}` |
| WebSocket | `wss://fal.run/{model_id}` |

### Authentication

```
Authorization: Key YOUR_FAL_KEY
```

### Queue Workflow

```bash
# 1. Submit to queue
curl -X POST "https://queue.fal.run/fal-ai/flux/dev" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful landscape",
    "image_size": "landscape_16_9"
  }'

# Response:
# {
#   "request_id": "abc123-def456",
#   "status": "IN_QUEUE",
#   "queue_position": 0
# }

# 2. Check status
curl "https://queue.fal.run/fal-ai/flux/dev/requests/abc123-def456/status" \
  -H "Authorization: Key $FAL_KEY"

# Response (in progress):
# {
#   "status": "IN_PROGRESS",
#   "logs": [{"message": "Loading model...", "timestamp": "..."}]
# }

# Response (completed):
# {
#   "status": "COMPLETED"
# }

# 3. Get result
curl "https://queue.fal.run/fal-ai/flux/dev/requests/abc123-def456" \
  -H "Authorization: Key $FAL_KEY"

# Response:
# {
#   "images": [{"url": "https://fal.media/...", "width": 1024, "height": 576}],
#   "seed": 12345,
#   "prompt": "A beautiful landscape"
# }
```

### Webhooks

Submit with webhook URL to receive results via POST:

```bash
curl -X POST "https://queue.fal.run/fal-ai/flux/dev" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Test",
    "webhook_url": "https://your-server.com/webhook"
  }'
```

Webhook payload:
```json
{
  "request_id": "abc123",
  "status": "COMPLETED",
  "payload": {
    "images": [{"url": "https://fal.media/..."}]
  }
}
```

### Direct Execution

For fast endpoints (< 30 seconds):

```bash
curl -X POST "https://fal.run/fal-ai/fast-sdxl" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A cat"}'
```

## Common Model Parameters

### FLUX Models

```typescript
interface FluxInput {
  prompt: string;                    // Required
  image_size?:
    | "square_hd"      // 1024x1024
    | "square"         // 512x512
    | "portrait_4_3"   // 768x1024
    | "portrait_16_9"  // 576x1024
    | "landscape_4_3"  // 1024x768
    | "landscape_16_9" // 1024x576
    | { width: number; height: number };
  num_inference_steps?: number;      // 1-50, default: 28
  guidance_scale?: number;           // 1-20, default: 3.5
  num_images?: number;               // 1-4, default: 1
  seed?: number;                     // For reproducibility
  enable_safety_checker?: boolean;   // Default: true
  output_format?: "jpeg" | "png";    // Default: jpeg
  sync_mode?: boolean;               // Wait for completion
}

interface FluxOutput {
  images: Array<{
    url: string;
    width: number;
    height: number;
    content_type: string;
  }>;
  seed: number;
  prompt: string;
  has_nsfw_concepts?: boolean[];
  timings?: {
    inference: number;
  };
}
```

### Video Models

```typescript
interface VideoInput {
  prompt: string;
  negative_prompt?: string;
  duration?: number;          // seconds
  aspect_ratio?: "16:9" | "9:16" | "1:1" | "4:3" | "21:9";
  cfg_scale?: number;         // 0.0-1.0
  seed?: number;
  // Model-specific options...
}

interface VideoOutput {
  video: {
    url: string;
    content_type: string;
    file_size?: number;
  };
  audio?: {
    url: string;
  };
  seed: number;
}
```

### Audio Models (Whisper)

```typescript
interface WhisperInput {
  audio_url: string;
  task?: "transcribe" | "translate";
  language?: string;         // ISO code
  chunk_level?: "segment";
  version?: "3";
}

interface WhisperOutput {
  text: string;
  chunks?: Array<{
    text: string;
    timestamp: [number, number];
  }>;
}
```

## Error Responses

```typescript
// 400 Bad Request - Validation error
{
  "detail": "Invalid input",
  "errors": [
    {"field": "prompt", "message": "Field is required"}
  ]
}

// 401 Unauthorized
{
  "detail": "Invalid API key"
}

// 429 Too Many Requests
{
  "detail": "Rate limit exceeded",
  "retry_after": 60
}

// 500 Internal Server Error
{
  "detail": "Internal server error",
  "request_id": "abc123"
}
```

## Rate Limits

- Rate limits vary by subscription tier
- Implement exponential backoff for 429 responses
- Use webhooks for high-volume applications
- Contact fal.ai for enterprise rate limits

## SDK Versions

| Library | Latest Version | Install |
|---------|---------------|---------|
| @fal-ai/client | 0.15+ | `npm install @fal-ai/client` |
| fal-client (Python) | 0.4+ | `pip install fal-client` |
| fal (Serverless) | 0.13+ | `pip install fal` |

Always check https://docs.fal.ai for the latest API documentation and updates.
