---
name: nextjs-modal-integration
description: Modal.com integration patterns for Next.js applications. PROACTIVELY activate for: (1) Next.js + Modal backend setup, (2) AI inference from Next.js (LLMs, image generation), (3) Video/audio processing backends, (4) Heavy compute offloading from Vercel, (5) GPU workloads for Next.js apps, (6) Webhook integration between Next.js and Modal, (7) File upload processing, (8) Background job processing, (9) Serverless AI API endpoints, (10) Next.js + Modal authentication patterns. Provides: Architecture patterns, API route integration, webhook handling, file upload workflows, CORS configuration, warm container patterns, streaming responses, and production-ready examples.
---

## Quick Reference

| Pattern | Use Case | Cold Start |
|---------|----------|------------|
| API Route → Modal | Simple request/response | ~500ms |
| API Route → Modal (warm) | Production APIs | <100ms |
| Webhook + Spawn | Long-running jobs | N/A (async) |
| Streaming Response | LLM text generation | ~500ms first token |

## When to Use This Skill

Use for **Next.js + Modal integration**:
- AI inference that's too heavy for Edge/Vercel Functions
- Video/audio processing with FFmpeg
- Background jobs exceeding Vercel's 60s timeout
- GPU workloads (image generation, LLMs, embeddings)
- Cost-effective scaling for burst compute

**Architecture principle**: Next.js handles UI/auth/routing, Modal handles heavy compute.

---

# Next.js + Modal.com Integration (2025)

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Next.js (Vercel)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Pages/    │  │    API      │  │    Server           │ │
│  │   App       │  │   Routes    │  │    Actions          │ │
│  │   Router    │  │             │  │                     │ │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │
└─────────┼────────────────┼───────────────────┼─────────────┘
          │                │                   │
          └────────────────┼───────────────────┘
                           │ HTTPS
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Modal.com                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   FastAPI   │  │    GPU      │  │    Background       │ │
│  │   Endpoint  │  │   Functions │  │    Jobs             │ │
│  │             │  │   (A100)    │  │    (.spawn())       │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Modal Backend Setup

### Basic FastAPI Endpoint

```python
# modal_backend/app.py
import modal
from datetime import datetime

app = modal.App("nextjs-backend")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("fastapi", "pydantic")
)

@app.function(image=image)
@modal.concurrent(max_inputs=100, target_inputs=50)
@modal.asgi_app()
def api():
    """FastAPI endpoint for Next.js frontend"""
    from fastapi import FastAPI, HTTPException, Depends
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    from pydantic import BaseModel, Field

    web_app = FastAPI(title="Next.js Backend API")

    # CORS configuration for Next.js
    web_app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",           # Next.js dev
            "https://*.vercel.app",            # Vercel preview
            "https://yourdomain.com",          # Production
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Simple API key auth
    security = HTTPBearer()
    API_KEY = "your-secret-key"  # Use modal.Secret in production

    def verify_token(creds: HTTPAuthorizationCredentials = Depends(security)):
        if creds.credentials != API_KEY:
            raise HTTPException(status_code=401, detail="Invalid API key")
        return creds.credentials

    # === Endpoints ===

    class ProcessRequest(BaseModel):
        data: str = Field(..., min_length=1)
        options: dict = {}

    class ProcessResponse(BaseModel):
        result: str
        processed_at: str

    @web_app.post("/process", response_model=ProcessResponse)
    def process_endpoint(
        req: ProcessRequest,
        token: str = Depends(verify_token)
    ):
        # Your processing logic here
        result = f"Processed: {req.data}"

        return ProcessResponse(
            result=result,
            processed_at=datetime.utcnow().isoformat()
        )

    @web_app.get("/health")
    def health():
        return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

    return web_app
```

Deploy with:
```bash
modal deploy modal_backend/app.py
# Returns: https://your-workspace--nextjs-backend-api.modal.run
```

---

## Next.js API Route Integration

### Basic API Route (App Router)

```typescript
// app/api/process/route.ts
import { NextRequest, NextResponse } from 'next/server';

const MODAL_API_URL = process.env.MODAL_API_URL!;
const MODAL_API_KEY = process.env.MODAL_API_KEY!;

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();

    const response = await fetch(`${MODAL_API_URL}/process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${MODAL_API_KEY}`,
      },
      body: JSON.stringify({
        data: body.data,
        options: body.options || {},
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Modal API error: ${response.status} - ${error}`);
    }

    const result = await response.json();
    return NextResponse.json(result);

  } catch (error) {
    console.error('Processing error:', error);
    return NextResponse.json(
      { error: 'Processing failed' },
      { status: 500 }
    );
  }
}
```

### Environment Variables

```env
# .env.local
MODAL_API_URL=https://your-workspace--nextjs-backend-api.modal.run
MODAL_API_KEY=your-secret-key
```

---

## AI Image Generation Example

### Modal Backend

```python
# modal_backend/image_gen.py
import modal

app = modal.App("image-generator")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "fastapi",
        "torch",
        "diffusers",
        "transformers",
        "accelerate",
        "pydantic",
    )
)

models_volume = modal.Volume.from_name("sd-models", create_if_missing=True)

@app.cls(
    image=image,
    gpu="A100-40GB",
    volumes={"/models": models_volume},
    min_containers=1,  # Keep warm for fast response
    max_containers=5,
    container_idle_timeout=300,
)
class ImageGenerator:
    @modal.enter()
    def setup(self):
        import torch
        from diffusers import StableDiffusionXLPipeline

        print("Loading SDXL model...")
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16,
            cache_dir="/models",
        )
        self.pipe.to("cuda")
        print("Model ready!")

    @modal.method()
    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        steps: int = 30,
    ) -> bytes:
        """Generate image and return as PNG bytes"""
        import io

        image = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=steps,
        ).images[0]

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()


@app.function(image=image)
@modal.concurrent(max_inputs=50)
@modal.asgi_app()
def api():
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import Response
    from pydantic import BaseModel, Field

    web_app = FastAPI()

    web_app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "https://*.vercel.app"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    class GenerateRequest(BaseModel):
        prompt: str = Field(..., min_length=1, max_length=1000)
        negative_prompt: str = ""
        width: int = Field(1024, ge=512, le=2048)
        height: int = Field(1024, ge=512, le=2048)
        steps: int = Field(30, ge=20, le=50)

    @web_app.post("/generate")
    def generate_endpoint(req: GenerateRequest):
        generator = ImageGenerator()

        try:
            image_bytes = generator.generate.remote(
                prompt=req.prompt,
                negative_prompt=req.negative_prompt,
                width=req.width,
                height=req.height,
                steps=req.steps,
            )
            return Response(content=image_bytes, media_type="image/png")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return web_app
```

### Next.js API Route

```typescript
// app/api/generate-image/route.ts
import { NextRequest, NextResponse } from 'next/server';

const MODAL_API_URL = process.env.MODAL_IMAGE_GEN_URL!;

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();

    const response = await fetch(`${MODAL_API_URL}/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: body.prompt,
        negative_prompt: body.negativePrompt || '',
        width: body.width || 1024,
        height: body.height || 1024,
        steps: body.steps || 30,
      }),
    });

    if (!response.ok) {
      throw new Error(`Generation failed: ${response.statusText}`);
    }

    const imageBuffer = await response.arrayBuffer();

    return new NextResponse(imageBuffer, {
      headers: {
        'Content-Type': 'image/png',
        'Cache-Control': 'public, max-age=31536000, immutable',
      },
    });
  } catch (error) {
    console.error('Image generation error:', error);
    return NextResponse.json({ error: 'Generation failed' }, { status: 500 });
  }
}
```

### React Component

```tsx
// components/ImageGenerator.tsx
'use client';

import { useState } from 'react';

export default function ImageGenerator() {
  const [prompt, setPrompt] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const generateImage = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/generate-image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        throw new Error('Generation failed');
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setImageUrl(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">AI Image Generator</h1>

      <textarea
        className="w-full p-4 border rounded-lg mb-4 min-h-[100px]"
        placeholder="Describe the image you want to generate..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />

      <button
        className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-medium
                   disabled:opacity-50 disabled:cursor-not-allowed
                   hover:bg-blue-700 transition-colors"
        onClick={generateImage}
        disabled={loading || !prompt.trim()}
      >
        {loading ? 'Generating...' : 'Generate Image'}
      </button>

      {error && (
        <div className="mt-4 p-4 bg-red-100 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {imageUrl && (
        <div className="mt-6">
          <img
            src={imageUrl}
            alt="Generated image"
            className="w-full rounded-lg shadow-lg"
          />
        </div>
      )}
    </div>
  );
}
```

---

## Long-Running Jobs with Webhooks

For jobs exceeding Vercel's 60-second timeout, use webhooks.

### Modal Backend with Webhooks

```python
# modal_backend/jobs.py
import modal
import httpx

app = modal.App("job-processor")

image = modal.Image.debian_slim().pip_install("fastapi", "httpx", "pydantic")

@app.function(image=image, timeout=3600)  # 1 hour max
def process_long_job(job_id: str, data: dict, callback_url: str):
    """Long-running job that calls back when complete"""
    import time

    # Simulate long processing
    print(f"Processing job {job_id}...")
    time.sleep(60)  # Your actual processing here

    result = {"job_id": job_id, "status": "completed", "output": "processed data"}

    # Callback to Next.js webhook
    httpx.post(
        callback_url,
        json=result,
        headers={"X-Webhook-Secret": "your-webhook-secret"},
        timeout=30,
    )

    return result


@app.function(image=image)
@modal.asgi_app()
def api():
    from fastapi import FastAPI, BackgroundTasks
    from pydantic import BaseModel
    import uuid

    web_app = FastAPI()

    class JobRequest(BaseModel):
        data: dict
        callback_url: str

    @web_app.post("/submit-job")
    def submit_job(req: JobRequest):
        job_id = str(uuid.uuid4())

        # Spawn async job (returns immediately)
        process_long_job.spawn(job_id, req.data, req.callback_url)

        return {
            "job_id": job_id,
            "status": "processing",
            "message": "Job submitted successfully"
        }

    return web_app
```

### Next.js Webhook Handler

```typescript
// app/api/webhooks/job-complete/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma'; // Your database client

const WEBHOOK_SECRET = process.env.WEBHOOK_SECRET!;

export async function POST(req: NextRequest) {
  // Verify webhook signature
  const signature = req.headers.get('X-Webhook-Secret');
  if (signature !== WEBHOOK_SECRET) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
  }

  try {
    const body = await req.json();
    const { job_id, status, output } = body;

    // Update job in database
    await prisma.job.update({
      where: { id: job_id },
      data: {
        status,
        output,
        completedAt: new Date(),
      },
    });

    // Optional: Send notification to user
    // await sendNotification(job.userId, `Job ${job_id} completed!`);

    return NextResponse.json({ received: true });
  } catch (error) {
    console.error('Webhook error:', error);
    return NextResponse.json({ error: 'Processing failed' }, { status: 500 });
  }
}
```

### Job Submission from Next.js

```typescript
// app/api/jobs/submit/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { auth } from '@/lib/auth';

const MODAL_API_URL = process.env.MODAL_JOBS_URL!;
const APP_URL = process.env.NEXT_PUBLIC_APP_URL!;

export async function POST(req: NextRequest) {
  const session = await auth();
  if (!session?.user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    const body = await req.json();

    // Create job record
    const job = await prisma.job.create({
      data: {
        userId: session.user.id,
        status: 'pending',
        input: body,
      },
    });

    // Submit to Modal
    const response = await fetch(`${MODAL_API_URL}/submit-job`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        data: body,
        callback_url: `${APP_URL}/api/webhooks/job-complete`,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to submit job');
    }

    return NextResponse.json({
      jobId: job.id,
      status: 'processing',
    });
  } catch (error) {
    console.error('Job submission error:', error);
    return NextResponse.json({ error: 'Submission failed' }, { status: 500 });
  }
}
```

---

## File Upload Processing

### Modal Backend for File Processing

```python
# modal_backend/files.py
import modal

app = modal.App("file-processor")

image = modal.Image.debian_slim().pip_install(
    "fastapi",
    "python-multipart",
    "pillow",
)

@app.function(image=image, timeout=300)
@modal.asgi_app()
def api():
    from fastapi import FastAPI, UploadFile, File, HTTPException
    from fastapi.responses import Response
    from PIL import Image
    import io

    web_app = FastAPI()

    @web_app.post("/resize-image")
    async def resize_image(
        file: UploadFile = File(...),
        width: int = 800,
        height: int = 600,
    ):
        if not file.content_type.startswith('image/'):
            raise HTTPException(400, "File must be an image")

        contents = await file.read()

        # Process image
        img = Image.open(io.BytesIO(contents))
        img = img.resize((width, height), Image.Resampling.LANCZOS)

        # Return processed image
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")

        return Response(
            content=buffer.getvalue(),
            media_type="image/png",
        )

    return web_app
```

### Next.js File Upload Handler

```typescript
// app/api/resize/route.ts
import { NextRequest, NextResponse } from 'next/server';

const MODAL_API_URL = process.env.MODAL_FILES_URL!;

export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData();
    const file = formData.get('file') as File;
    const width = formData.get('width') || '800';
    const height = formData.get('height') || '600';

    if (!file) {
      return NextResponse.json({ error: 'No file provided' }, { status: 400 });
    }

    // Forward to Modal
    const modalFormData = new FormData();
    modalFormData.append('file', file);

    const response = await fetch(
      `${MODAL_API_URL}/resize-image?width=${width}&height=${height}`,
      {
        method: 'POST',
        body: modalFormData,
      }
    );

    if (!response.ok) {
      throw new Error('Processing failed');
    }

    const imageBuffer = await response.arrayBuffer();

    return new NextResponse(imageBuffer, {
      headers: { 'Content-Type': 'image/png' },
    });
  } catch (error) {
    console.error('Resize error:', error);
    return NextResponse.json({ error: 'Processing failed' }, { status: 500 });
  }
}
```

---

## Streaming LLM Responses

### Modal Backend with Streaming

```python
# modal_backend/llm.py
import modal

app = modal.App("llm-api")

image = modal.Image.debian_slim().pip_install(
    "fastapi",
    "transformers",
    "torch",
    "accelerate",
    "sse-starlette",
)

@app.cls(image=image, gpu="A100", min_containers=1)
class LLMServer:
    @modal.enter()
    def setup(self):
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch

        self.tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
        self.model = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Llama-2-7b-chat-hf",
            torch_dtype=torch.float16,
        ).to("cuda")

    @modal.method()
    def generate_stream(self, prompt: str, max_tokens: int = 512):
        """Generator that yields tokens one at a time"""
        from transformers import TextIteratorStreamer
        from threading import Thread

        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")

        streamer = TextIteratorStreamer(self.tokenizer, skip_special_tokens=True)

        generation_kwargs = dict(
            **inputs,
            max_new_tokens=max_tokens,
            streamer=streamer,
        )

        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        for token in streamer:
            yield token

        thread.join()


@app.function(image=image)
@modal.asgi_app()
def api():
    from fastapi import FastAPI
    from sse_starlette.sse import EventSourceResponse
    from pydantic import BaseModel

    web_app = FastAPI()

    class GenerateRequest(BaseModel):
        prompt: str
        max_tokens: int = 512

    @web_app.post("/generate-stream")
    async def generate_stream_endpoint(req: GenerateRequest):
        llm = LLMServer()

        async def event_generator():
            for token in llm.generate_stream.remote_gen(req.prompt, req.max_tokens):
                yield {"data": token}

        return EventSourceResponse(event_generator())

    return web_app
```

### Next.js Streaming Handler

```typescript
// app/api/chat/route.ts
import { NextRequest } from 'next/server';

const MODAL_API_URL = process.env.MODAL_LLM_URL!;

export async function POST(req: NextRequest) {
  const { prompt } = await req.json();

  const response = await fetch(`${MODAL_API_URL}/generate-stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt }),
  });

  // Stream the response directly to client
  return new Response(response.body, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

### React Component with Streaming

```tsx
// components/Chat.tsx
'use client';

import { useState } from 'react';

export default function Chat() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    setLoading(true);
    setResponse('');

    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });

    const reader = res.body?.getReader();
    const decoder = new TextDecoder();

    while (reader) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      // Parse SSE format
      const lines = chunk.split('\n');
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const token = line.slice(6);
          setResponse(prev => prev + token);
        }
      }
    }

    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <textarea
        className="w-full p-4 border rounded-lg mb-4"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Ask something..."
      />

      <button
        className="bg-blue-600 text-white py-2 px-6 rounded-lg"
        onClick={sendMessage}
        disabled={loading}
      >
        {loading ? 'Generating...' : 'Send'}
      </button>

      {response && (
        <div className="mt-6 p-4 bg-gray-100 rounded-lg whitespace-pre-wrap">
          {response}
        </div>
      )}
    </div>
  );
}
```

---

## Best Practices

### 1. Keep Modal API Keys Server-Side

```typescript
// GOOD: API key in server-side API route
// app/api/process/route.ts
const MODAL_API_KEY = process.env.MODAL_API_KEY; // Server only

// BAD: Exposing API key to client
// NEXT_PUBLIC_MODAL_API_KEY=... // Never do this!
```

### 2. Use Warm Containers for Production

```python
@app.cls(
    min_containers=1,           # Always keep 1 warm
    max_containers=10,          # Scale up to 10
    container_idle_timeout=300, # Keep warm for 5 min after use
)
class MyService:
    pass
```

### 3. Handle Vercel Timeouts

```typescript
// Vercel timeout limits:
// - Hobby: 60 seconds
// - Pro: 300 seconds
// - Enterprise: 900 seconds

// For longer jobs, use webhooks instead of waiting
```

### 4. Implement Request Timeouts

```typescript
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 55000); // 55s

try {
  const response = await fetch(url, { signal: controller.signal });
} finally {
  clearTimeout(timeoutId);
}
```

### 5. Cache Modal Responses

```typescript
// Next.js 15 cache pattern
import { unstable_cache } from 'next/cache';

const getCachedResult = unstable_cache(
  async (id: string) => {
    const response = await fetch(`${MODAL_API_URL}/process/${id}`);
    return response.json();
  },
  ['modal-result'],
  { revalidate: 3600 } // Cache for 1 hour
);
```

---

## Common Pitfalls

### 1. CORS Errors

```python
# Make sure CORS allows your Next.js domains
web_app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",  # All Vercel preview URLs
        "https://yourdomain.com",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Cold Start Latency

```python
# Use min_containers=1 for production APIs
@app.function(min_containers=1)  # ~$1-2/day idle cost
def api():
    pass
```

### 3. Large Payloads

```typescript
// For large files, upload directly to Modal or use signed URLs
// Don't pass >4MB through Next.js API routes

// Better: Use Modal's CloudBucketMount
```

### 4. Error Handling

```typescript
// Always handle Modal errors gracefully
try {
  const response = await fetch(MODAL_API_URL);
  if (!response.ok) {
    // Log for debugging
    console.error(`Modal error: ${response.status}`, await response.text());
    // Return user-friendly error
    return NextResponse.json(
      { error: 'Service temporarily unavailable' },
      { status: 503 }
    );
  }
} catch (error) {
  // Handle network errors
  console.error('Network error:', error);
  return NextResponse.json(
    { error: 'Could not connect to service' },
    { status: 503 }
  );
}
```

---

## Deployment Checklist

1. **Deploy Modal backend first**
   ```bash
   modal deploy modal_backend/app.py
   ```

2. **Set environment variables in Vercel**
   ```
   MODAL_API_URL=https://your-workspace--app-api.modal.run
   MODAL_API_KEY=your-secret-key
   WEBHOOK_SECRET=your-webhook-secret
   ```

3. **Update CORS for production domain**

4. **Enable warm containers for production**
   ```python
   @app.function(min_containers=1)
   ```

5. **Monitor costs**
   ```bash
   modal app stats your-app-name
   ```

---

## Related Skills

- `nextjs-server-actions` - Server Actions patterns
- `nextjs-caching` - Caching strategies
- `nextjs-deployment` - Deployment configurations
