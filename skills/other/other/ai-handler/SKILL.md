---
name: ai-handler
description: Integrate Replicate AI models with background processing, S3 storage, and credit systems
tools: Read, Write, Edit
model: inherit
deps: ["inngest-handler", "s3-upload-handler", "credits-handler", "replicate-handler"]
---

# Replicate AI Handler Skill

This skill provides a production-ready pattern for integrating Replicate AI models. It handles long-running predictions using Inngest background jobs, stores results in S3, manages user credits, and updates database state.

## Architecture

1.  **Trigger**: User requests a generation via API (e.g., `/api/app/ai-images`).
2.  **Validation**: Check/deduct user credits.
3.  **State**: Create a database record with `status: "processing"`.
4.  **Queue**: Trigger an Inngest function to handle the Replicate API call.
5.  **Processing**:
    -   Call Replicate API.
    -   Wait for completion (polling or webhook).
    -   Download result and upload to S3 (server-side).
6.  **Completion**: Update database record with S3 URL and `status: "completed"`.
7.  **Failure**: Refund credits if failed (optional) and update status to `failed`.

## Prerequisites

-   `replicate` package installed (`npm install replicate`).
-   `REPLICATE_API_TOKEN` in `.env`.
-   S3 and Inngest configured.

## Implementation Steps

### 1. API Route (Trigger)
`src/app/api/app/generate/route.ts`

```typescript
import withAuthRequired from "@/lib/auth/withAuthRequired";
import { db } from "@/db";
import { generations } from "@/db/schema";
import { inngest } from "@/lib/inngest/client";
import { checkCredits, deductCredits } from "@/lib/credits"; // Hypothetical helpers

export const POST = withAuthRequired(async (req, { session }) => {
  const body = await req.json();
  
  // 1. Check Credits
  const hasCredits = await checkCredits(session.user.id, "image_generation", 1);
  if (!hasCredits) return new Response("Insufficient credits", { status: 403 });

  // 2. Create DB Record (Pending)
  const [record] = await db.insert(generations).values({
    userId: session.user.id,
    prompt: body.prompt,
    status: "processing",
  }).returning();

  // 3. Deduct Credits (Optimistic)
  await deductCredits(session.user.id, "image_generation", 1, { source: "api", refId: record.id });

  // 4. Trigger Background Job
  await inngest.send({
    name: "app/ai.generate",
    data: {
      generationId: record.id,
      prompt: body.prompt,
      userId: session.user.id
    }
  });

  return Response.json({ id: record.id, status: "processing" });
});
```

### 2. Inngest Function (Processor)
`src/lib/inngest/functions/app/ai/generate.ts`

```typescript
import { inngest } from "@/lib/inngest/client";
import Replicate from "replicate";
import uploadFromServer from "@/lib/s3/uploadFromServer";
import { db } from "@/db";
import { generations } from "@/db/schema";
import { eq } from "drizzle-orm";

const replicate = new Replicate({ auth: process.env.REPLICATE_API_TOKEN });

export const generateAI = inngest.createFunction(
  { id: "ai-generation-worker", concurrency: 5 },
  { event: "app/ai.generate" },
  async ({ event, step }) => {
    const { generationId, prompt } = event.data;

    try {
      // 1. Call Replicate (Step ensures retries on network error)
      const prediction = await step.run("call-replicate", async () => {
        return await replicate.predictions.create({
          version: "model-version-hash",
          input: { prompt }
        });
      });

      // 2. Wait for completion
      // Replicate usually takes time. We can use waitForEvent if using webhooks, 
      // or simple polling loop with sleep if webhooks aren't set up.
      // For simplicity, here is a polling pattern using sleep:
      let finalPrediction = prediction;
      while (finalPrediction.status !== "succeeded" && finalPrediction.status !== "failed") {
        await step.sleep("wait-for-gpu", "5s");
        finalPrediction = await step.run("check-status", () => 
          replicate.predictions.get(prediction.id)
        );
      }

      if (finalPrediction.status === "failed") {
        throw new Error(finalPrediction.error);
      }

      // 3. Upload to S3
      // Replicate returns a temporary URL. We must persist it.
      const outputUrl = finalPrediction.output[0]; // Adjust based on model output
      
      const s3Url = await step.run("upload-to-s3", async () => {
        // Fetch image buffer
        const response = await fetch(outputUrl);
        const arrayBuffer = await response.arrayBuffer();
        const base64 = Buffer.from(arrayBuffer).toString("base64");

        // Use existing S3 skill
        return await uploadFromServer({
          file: base64,
          path: `generations/${generationId}.png`,
          contentType: "image/png"
        });
      });

      // 4. Update DB
      await step.run("update-db", async () => {
        await db.update(generations)
          .set({ status: "completed", url: s3Url })
          .where(eq(generations.id, generationId));
      });

    } catch (error) {
      // Handle Failure
      await step.run("mark-failed", async () => {
        await db.update(generations)
          .set({ status: "failed" })
          .where(eq(generations.id, generationId));
        
        // Optional: Refund credits here
      });
      throw error; // Re-throw to show failure in Inngest dashboard
    }
  }
);
```
