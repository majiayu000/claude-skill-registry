---
name: replicate-handler
description: Integrate with Replicate AI for running models (image generation, LLMs, etc.).
---

# Replicate Handler

## Setup

1.  **Install**: `npm install replicate`
2.  **Environment**: Add `REPLICATE_API_TOKEN` to `.env` (and `.env.local`).

## Usage Patterns

### 1. Quick Run (Short Tasks)
For models that complete quickly (seconds), use `replicate.run`.

```typescript
import Replicate from "replicate";

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,
});

// Run a model
const output = await replicate.run(
  "owner/model:version",
  {
    input: {
      prompt: "..."
    }
  }
);
```

### 2. Long-Running Tasks (with Inngest)
For tasks that might timeout (video generation, large models), use Inngest's `step.sleep` to poll for completion.

```typescript
// In an Inngest function
export const generateVideo = inngest.createFunction(
  { id: "generate-video" },
  { event: "video.generate" },
  async ({ event, step }) => {
    
    // 1. Create Prediction
    const prediction = await step.run("create-prediction", async () => {
      return await replicate.predictions.create({
        version: "model-version-hash",
        input: { prompt: event.data.prompt }
      });
    });

    let status = prediction.status;
    let result = prediction;

    // 2. Poll for Completion
    while (status !== "succeeded" && status !== "failed" && status !== "canceled") {
      // Sleep for 5s (Inngest handles this without consuming server time)
      await step.sleep("wait-for-model", "5s");

      // Check status
      result = await step.run("check-status", async () => {
        return await replicate.predictions.get(prediction.id);
      });
      status = result.status;
    }

    // 3. Handle Result
    if (status === "failed") {
      throw new Error(`Replicate failed: ${result.error}`);
    }
    
    return result.output;
  }
);
```

## Types Reference
See [reference.md](reference.md) for the full type definitions of the Replicate SDK.
