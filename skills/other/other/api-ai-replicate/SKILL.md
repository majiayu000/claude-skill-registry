---
name: api-ai-replicate
description: Replicate SDK patterns for TypeScript/Node.js -- client setup, predictions, streaming, webhooks, file handling, model versioning, deployments, and training
---

# Replicate SDK Patterns

> **Quick Guide:** Use the `replicate` npm package to run open-source ML models on serverless GPUs. Use `replicate.run()` for synchronous execution that returns output directly, `replicate.stream()` for SSE-based streaming, or `replicate.predictions.create()` for async background jobs with webhook notifications. Models are referenced as `owner/model` (uses latest version) or `owner/model:version` (pinned). File outputs are `FileOutput` objects implementing `ReadableStream`. Cold starts are expected for infrequently-used models -- use deployments with `min_instances` to keep models warm.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST never hardcode API tokens -- always use environment variables via `process.env.REPLICATE_API_TOKEN`)**

**(You MUST handle `FileOutput` objects for models that return files -- do not assume outputs are plain strings or URLs)**

**(You MUST validate webhooks using `validateWebhook()` from the `replicate` package -- never trust unverified webhook payloads)**

**(You MUST account for cold starts when running infrequently-used models -- use deployments for latency-sensitive applications)**

**(You MUST specify model versions (`owner/model:version`) in production to ensure reproducible results -- unversioned references use the latest, which can change)**

</critical_requirements>

---

**Auto-detection:** Replicate, replicate, replicate.run, replicate.stream, replicate.predictions, replicate.deployments, replicate.trainings, replicate.models, FileOutput, validateWebhook, REPLICATE_API_TOKEN, serverless GPU, cold start, webhook_events_filter

**When to use:**

- Running open-source ML models (Llama, Stable Diffusion, Whisper, etc.) without managing GPU infrastructure
- Generating images, transcribing audio, running LLMs, or any ML inference via API
- Streaming LLM output in real-time with server-sent events
- Processing predictions asynchronously with webhook notifications
- Fine-tuning models with custom training data
- Running models on dedicated hardware with custom scaling via deployments

**Key patterns covered:**

- Client initialization and configuration (auth, user agent, file encoding)
- Running predictions (`replicate.run()`, `replicate.predictions.create()`, `replicate.wait()`)
- Streaming output (`replicate.stream()` with SSE events)
- Model versioning (`owner/model` vs `owner/model:version`)
- File input/output handling (`FileOutput`, file uploads, `Buffer` inputs)
- Webhooks (setup, event filtering, signature validation)
- Deployments (custom hardware, scaling, keeping models warm)
- Training / fine-tuning

**When NOT to use:**

- You need a unified multi-provider LLM SDK (OpenAI, Anthropic, Google) -- use a provider-agnostic SDK
- You want to run models locally -- Replicate is a cloud-only serverless platform
- You need sub-second latency guarantees without deployments -- cold starts can take minutes

---

## Examples Index

- [Core: Setup, Predictions & Files](examples/core.md) -- Client init, run(), predictions.create(), wait(), file I/O, error handling
- [Streaming & Webhooks](examples/streaming-webhooks.md) -- stream(), SSE events, webhook setup, signature validation
- [Deployments & Training](examples/deployments-training.md) -- Custom hardware, scaling, fine-tuning, model management
- [Quick API Reference](reference.md) -- Method signatures, constructor options, error types, model reference format

---

<philosophy>

## Philosophy

Replicate provides **serverless GPU infrastructure** for running open-source ML models. You send inputs, Replicate allocates GPU hardware, runs the model, and returns outputs. No Docker, no CUDA drivers, no GPU provisioning.

**Core principles:**

1. **Serverless execution** -- Models run on-demand on Replicate's infrastructure. You pay only for compute time. Cold starts are a trade-off for not maintaining always-on GPUs.
2. **Model marketplace** -- Thousands of community and official models available at `replicate.com/explore`. Run any public model with just its identifier.
3. **Version pinning for reproducibility** -- Models are versioned with SHA-256 hashes. Pin to a version in production (`owner/model:abc123...`) to guarantee identical behavior across deploys.
4. **Three execution modes** -- `replicate.run()` for synchronous wait, `replicate.stream()` for real-time SSE output, `replicate.predictions.create()` for fire-and-forget with webhooks.
5. **File-first I/O** -- Many models accept and produce files (images, audio, video). The SDK handles file uploads automatically and returns `FileOutput` objects for file outputs.

**When to use Replicate:**

- You want to run open-source models without managing infrastructure
- You need access to a wide variety of models (image gen, LLMs, audio, video)
- You want pay-per-second pricing with no idle costs
- You need to fine-tune models on custom data

**When NOT to use:**

- You need guaranteed sub-100ms latency (cold starts are unpredictable without deployments)
- You want to use proprietary models (OpenAI, Anthropic) -- use their SDKs directly
- You need to run models locally or in your own cloud -- consider self-hosting with Cog

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client Setup

Initialize the Replicate client. It auto-reads `REPLICATE_API_TOKEN` from the environment.

```typescript
// lib/replicate.ts -- basic setup
import Replicate from "replicate";

const replicate = new Replicate();

export { replicate };
```

```typescript
// lib/replicate.ts -- explicit auth + custom user agent
import Replicate from "replicate";

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN, // Auto-reads from env if omitted
  userAgent: "my-app/1.0.0",
});

export { replicate };
```

**Why good:** Minimal setup, env var auto-detected, explicit auth optional but useful for clarity

```typescript
// BAD: Hardcoded token
const replicate = new Replicate({
  auth: "r8_abc123...",
});
```

**Why bad:** Hardcoded API token is a security risk, will leak in version control

**See:** [examples/core.md](examples/core.md) for full constructor options, error handling patterns

---

### Pattern 2: Running Predictions

Use `replicate.run()` for synchronous execution. Returns the model output directly.

```typescript
// Run an image generation model
const [output] = await replicate.run("black-forest-labs/flux-schnell", {
  input: {
    prompt: "a serene mountain landscape at sunset",
  },
});

// output is a FileOutput object for image models
console.log(output.url()); // URL of generated image
```

```typescript
// Run an LLM -- output is a string for text models
const output = await replicate.run("meta/meta-llama-3-70b-instruct", {
  input: {
    prompt: "Explain TypeScript generics in 3 sentences.",
    max_tokens: 512,
  },
});

console.log(output); // Text response
```

**Why good:** Simple API, returns output directly, destructuring works for array outputs (images)

```typescript
// BAD: Not pinning version in production
const output = await replicate.run("community-user/experimental-model", {
  input: { prompt: "hello" },
});
```

**Why bad:** Community models without version pinning can change behavior unexpectedly when authors push updates

**See:** [examples/core.md](examples/core.md) for version pinning, `predictions.create()` + `wait()`, and progress callbacks

---

### Pattern 3: Streaming

Use `replicate.stream()` for real-time SSE output from language models.

```typescript
const stream = replicate.stream("meta/meta-llama-3-70b-instruct", {
  input: {
    prompt: "Write a short poem about TypeScript.",
    max_tokens: 512,
  },
});

for await (const event of stream) {
  if (event.event === "output") {
    process.stdout.write(event.data);
  }
}
```

**Why good:** Progressive output for better UX, event-based with typed `event` and `data` fields

```typescript
// BAD: Using replicate.run() for user-facing LLM output
const output = await replicate.run("meta/meta-llama-3-70b-instruct", {
  input: { prompt: "Write a long essay..." },
});
// User waits for entire generation to complete before seeing anything
```

**Why bad:** No progressive feedback, user sees a blank screen for seconds

**See:** [examples/streaming-webhooks.md](examples/streaming-webhooks.md) for event types, error handling, cancellation

---

### Pattern 4: Model Versioning

Models are referenced as `owner/model` (latest version) or `owner/model:sha256hash` (pinned version).

```typescript
// Development: use latest version for convenience
const output = await replicate.run("stability-ai/sdxl", {
  input: { prompt: "a cat" },
});

// Production: pin to a specific version for reproducibility
const VERSION_HASH =
  "39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b";
const output = await replicate.run(`stability-ai/sdxl:${VERSION_HASH}`, {
  input: { prompt: "a cat" },
});
```

**Why good:** Pinned version guarantees identical behavior, hash is immutable

**See:** [examples/core.md](examples/core.md) for listing model versions, getting version details

---

### Pattern 5: File Handling

Models that output files return `FileOutput` objects implementing `ReadableStream`.

```typescript
import { writeFile } from "node:fs/promises";

const [output] = await replicate.run("black-forest-labs/flux-schnell", {
  input: { prompt: "a sunset over mountains" },
});

// FileOutput has .url() and .blob() methods
console.log(output.url()); // Underlying URL

// Save to disk
const blob = await output.blob();
const buffer = Buffer.from(await blob.arrayBuffer());
await writeFile("./output.png", buffer);
```

```typescript
// File inputs: pass URLs, Buffers, or ReadStreams
import { readFile } from "node:fs/promises";

const imageBuffer = await readFile("./input.png");

const output = await replicate.run("some-user/image-model", {
  input: {
    image: imageBuffer, // Auto-uploaded (max 100 MiB)
  },
});
```

**Why good:** `FileOutput` is a `ReadableStream`, works with Node.js stream APIs, `.url()` for the underlying URL

```typescript
// BAD: Treating file output as a plain URL string
const [output] = await replicate.run("black-forest-labs/flux-schnell", {
  input: { prompt: "hello" },
});
const url = output; // WRONG: output is a FileOutput object, not a string
```

**Why bad:** `FileOutput` is an object, not a string -- use `.url()` to get the URL

**See:** [examples/core.md](examples/core.md) for file uploads, large file handling, encoding strategies

---

### Pattern 6: Async Predictions with Webhooks

Use `replicate.predictions.create()` for background jobs with webhook notifications.

```typescript
const prediction = await replicate.predictions.create({
  version: "27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478",
  input: { prompt: "a painting of a cat" },
  webhook: "https://my.app/webhooks/replicate",
  webhook_events_filter: ["completed"],
});

console.log(prediction.id); // Use to track status
console.log(prediction.status); // "starting"
```

```typescript
// Webhook signature validation (CRITICAL for security)
import { validateWebhook } from "replicate";

async function handleWebhook(request: Request): Promise<Response> {
  const secret = process.env.REPLICATE_WEBHOOK_SIGNING_SECRET;
  const isValid = await validateWebhook(request, secret);

  if (!isValid) {
    return new Response("Invalid signature", { status: 401 });
  }

  const prediction = await request.json();
  // Process prediction.output safely
  return new Response("OK", { status: 200 });
}
```

**Why good:** Decoupled processing, secure signature validation, filtered events reduce noise

**See:** [examples/streaming-webhooks.md](examples/streaming-webhooks.md) for webhook event types, polling alternative

---

### Pattern 7: Deployments

Deployments give you a private, fixed endpoint with custom hardware and scaling.

```typescript
// Create a prediction on a deployment (no cold start if min_instances > 0)
const prediction = await replicate.deployments.predictions.create(
  "my-org/my-deployment",
  {
    input: { prompt: "hello world" },
  },
);

const result = await replicate.wait(prediction);
console.log(result.output);
```

**Why good:** Predictable latency with `min_instances`, private endpoint, custom hardware selection

**See:** [examples/deployments-training.md](examples/deployments-training.md) for creating/managing deployments, training API

---

### Pattern 8: Error Handling

Catch API errors with status codes. The SDK auto-retries on 429 and 5xx errors (5 retries by default with exponential backoff).

```typescript
try {
  const output = await replicate.run("owner/model", {
    input: { prompt: "hello" },
  });
} catch (error) {
  if (error instanceof Error) {
    console.error(`Replicate error: ${error.message}`);

    // Check for specific HTTP status codes in the error
    if ("status" in error) {
      const status = (error as { status: number }).status;
      if (status === 401) {
        throw new Error("Invalid API token. Check REPLICATE_API_TOKEN.");
      }
      if (status === 422) {
        console.error("Invalid input parameters");
      }
      if (status === 429) {
        console.error(
          "Rate limited -- SDK auto-retries (5 attempts) exhausted",
        );
      }
    }
  }
  throw error;
}
```

**Why good:** Checks error type, handles specific status codes, re-throws unexpected errors

**See:** [examples/core.md](examples/core.md) for full error handling example with status code handling

</patterns>

---

<performance>

## Performance Optimization

### Cold Start Mitigation

```
Frequent model with varying load   -> Use deployments with min_instances >= 1
One-off batch jobs                  -> Use predictions.create() with webhooks (no waiting)
Popular public models               -> Usually warm, replicate.run() is fine
Custom/niche models                 -> Expect 30s-5min cold start on first run
```

### Key Optimization Patterns

- **Use deployments** for latency-sensitive applications -- set `min_instances: 1` to eliminate cold starts
- **Use webhooks** instead of polling for async jobs -- reduces API calls and latency
- **Batch file inputs as URLs** instead of uploading buffers -- avoids 100 MiB upload limit and is faster
- **Pin model versions** in production -- avoids unexpected behavior changes and enables caching
- **Use `replicate.stream()`** for LLMs -- progressive output feels faster than waiting for full completion
- **Cancel unneeded predictions** with `replicate.predictions.cancel()` -- stops billing immediately

</performance>

---

<decision_framework>

## Decision Framework

### Which Execution Method to Use

```
Is this a user-facing LLM response?
+-- YES -> Use replicate.stream() for real-time SSE output
+-- NO -> Do you need the result immediately?
    +-- YES -> Use replicate.run() (blocks until complete)
    +-- NO -> Use replicate.predictions.create() + webhook
        +-- Need to poll instead? -> Use replicate.wait(prediction)
```

### Model Reference Format

```
Are you in development/prototyping?
+-- YES -> Use owner/model (latest version, convenient)
+-- NO -> Are you in production?
    +-- YES -> Use owner/model:version_hash (pinned, reproducible)
    +-- Does the model change frequently?
        +-- YES -> Pin version, test updates explicitly
        +-- NO -> Either format works, prefer pinned
```

### Deployments vs Direct API

```
Do you need consistent low latency?
+-- YES -> Create a deployment with min_instances >= 1
+-- NO -> Do you need custom hardware (A100, H100)?
    +-- YES -> Create a deployment with specific hardware
    +-- NO -> Use replicate.run() / replicate.stream() directly
        (Replicate auto-allocates hardware)
```

### When to Use This SDK vs Other AI SDKs

```
Are you running open-source models on serverless GPUs?
+-- YES -> Use Replicate SDK
+-- NO -> Are you calling proprietary APIs (OpenAI, Anthropic)?
    +-- YES -> Not this skill's scope -- use provider-specific SDKs
    +-- NO -> Do you need to switch between multiple providers?
        +-- YES -> Not this skill's scope -- use a unified provider SDK
        +-- NO -> Do you want to self-host models?
            +-- YES -> Not this skill's scope -- consider Cog or vLLM
            +-- NO -> Replicate SDK is appropriate
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Hardcoding `REPLICATE_API_TOKEN` in source code (security breach risk)
- Treating `FileOutput` as a string (it is a `ReadableStream` object -- use `.url()` or `.blob()`)
- Not validating webhook signatures with `validateWebhook()` (allows forged webhook payloads)
- Using `replicate.run()` for long-running models in request handlers (blocks the response, can timeout)

**Medium Priority Issues:**

- Not pinning model versions in production (`owner/model` uses latest, which can change without notice)
- Relying solely on default retry behavior for production (5 retries with exponential backoff may be too aggressive for some use cases)
- Uploading large files as `Buffer` instead of hosting them at a URL (100 MiB limit on uploads)
- Ignoring cold start latency for infrequently-used models (first request can take minutes)

**Common Mistakes:**

- Confusing `replicate.run()` (returns output directly) with `replicate.predictions.create()` (returns a prediction object with status/id)
- Destructuring image output incorrectly: `const output = await replicate.run(...)` instead of `const [output] = await replicate.run(...)` (image models return arrays)
- Using `replicate.stream()` with models that do not support streaming (only language models with SSE support)
- Forgetting that `replicate.predictions.create()` requires a `version` hash, not just `owner/model` (use `replicate.run()` for the simpler format)
- Not consuming the async iterator from `replicate.stream()` (events are lost)

**Gotchas & Edge Cases:**

- Prediction inputs and outputs are automatically deleted after one hour -- persist outputs via webhooks or download immediately
- The SDK auto-retries on 429 (rate limit) and 5xx errors -- 5 retries by default with exponential backoff. GET requests retry on 429 and 5xx; non-GET requests retry only on 429
- `replicate.stream()` returns `ServerSentEvent` objects with `.event` (`"output"`, `"error"`, `"done"`) and `.data` (string) properties
- File uploads are limited to 100 MiB -- for larger files, host them at a URL and pass the URL as input
- Browser usage is not supported -- the SDK requires a server-side environment (Node.js 18+, Bun, Deno, Cloudflare Workers)
- `webhook_events_filter` accepts `["start", "output", "logs", "completed"]` -- use `["completed"]` unless you need intermediate status updates
- The `Prefer: wait` header enables sync mode on the HTTP API (up to 60s), but `replicate.run()` already handles this automatically
- Community models may disappear or change without warning -- pin versions and maintain fallbacks for critical workflows
- `replicate.wait()` polls the API until the prediction completes -- use webhooks for production to avoid polling overhead
- `FileOutput.url()` returns the underlying URL, but these URLs are temporary -- download or persist the file before it expires

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST never hardcode API tokens -- always use environment variables via `process.env.REPLICATE_API_TOKEN`)**

**(You MUST handle `FileOutput` objects for models that return files -- do not assume outputs are plain strings or URLs)**

**(You MUST validate webhooks using `validateWebhook()` from the `replicate` package -- never trust unverified webhook payloads)**

**(You MUST account for cold starts when running infrequently-used models -- use deployments for latency-sensitive applications)**

**(You MUST specify model versions (`owner/model:version`) in production to ensure reproducible results -- unversioned references use the latest, which can change)**

**Failure to follow these rules will produce insecure, unreliable, or unpredictable AI integrations.**

</critical_reminders>
