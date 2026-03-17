---
name: Workflows Patterns
description: Use when asking about "Workflows", "durable workflows", "multi-step processing", "WorkflowEntrypoint", "WorkflowStep", "data pipelines", "background jobs", "ingestion pipeline", or orchestrating multiple operations that need durability and error recovery.
version: 0.1.0
---

# Cloudflare Workflows

## Purpose

This skill provides guidance on Cloudflare Workflows, a durable execution engine for multi-step background processing. Use Workflows when you need guaranteed completion of complex operations that span multiple bindings (D1, R2, Vectorize, AI) with automatic retry and state persistence.

## When to Use Workflows

**Good use cases**:
- Data ingestion pipelines (fetch → store → process → index)
- Document processing (upload → chunk → embed → vectorize)
- Multi-step AI operations (generate → validate → store)
- Background jobs that must complete even if Workers restart
- Operations that need transaction-like guarantees

**Not needed for**:
- Simple request/response handlers
- Single-step operations
- Real-time operations where latency matters
- Operations that can safely fail silently

## Core Concepts

### WorkflowEntrypoint

The main class that defines your workflow:

```typescript
import { WorkflowEntrypoint, WorkflowStep, WorkflowEvent } from 'cloudflare:workers';

interface Env {
  DATABASE: D1Database;
  STORAGE: R2Bucket;
  AI: Ai;
  VECTOR_INDEX: VectorizeIndex;
}

interface WorkflowParams {
  documentId: string;
  content: string;
}

export class MyWorkflow extends WorkflowEntrypoint<Env, WorkflowParams> {
  async run(event: WorkflowEvent<WorkflowParams>, step: WorkflowStep) {
    const { documentId, content } = event.payload;

    // Steps go here...
  }
}
```

### WorkflowStep

Each `step.do()` call is a durable checkpoint:

```typescript
// Step 1: Store in R2
const storedPath = await step.do('store-document', async () => {
  const path = `documents/${documentId}.txt`;
  await this.env.STORAGE.put(path, content);
  return path;
});

// Step 2: Create D1 record
const recordId = await step.do('create-record', async () => {
  const result = await this.env.DATABASE
    .prepare('INSERT INTO documents (id, path) VALUES (?, ?)')
    .bind(documentId, storedPath)
    .run();
  return documentId;
});
```

**Key properties**:
- Steps are named with unique strings
- Step results are persisted automatically
- If a step fails, workflow pauses and can retry
- Completed steps are not re-executed on retry

## Data Ingestion Pipeline Pattern

Complete example based on real-world usage:

```typescript
import { WorkflowEntrypoint, WorkflowStep, WorkflowEvent } from 'cloudflare:workers';

interface Env {
  DATABASE: D1Database;
  ARTICLES_BUCKET: R2Bucket;
  AI: Ai;
  VECTOR_INDEX: VectorizeIndex;
  DEFAULT_CHUNK_SIZE: number;
  DEFAULT_CHUNK_OVERLAP: number;
}

interface IngestionParams {
  articleId: string;
  title: string;
  content: string;
}

export class IngestionWorkflow extends WorkflowEntrypoint<Env, IngestionParams> {
  async run(event: WorkflowEvent<IngestionParams>, step: WorkflowStep) {
    const { articleId, title, content } = event.payload;

    try {
      // Step 1: Store raw article in R2
      await step.do('store-article', async () => {
        await this.env.ARTICLES_BUCKET.put(
          `articles/${articleId}.json`,
          JSON.stringify({ id: articleId, title, content }),
          { httpMetadata: { contentType: 'application/json' } }
        );
        return { success: true };
      });

      // Step 2: Create document record in D1
      const documentId = await step.do('create-document', async () => {
        const id = crypto.randomUUID();
        await this.env.DATABASE
          .prepare('INSERT INTO documents (id, article_id, title) VALUES (?, ?, ?)')
          .bind(id, articleId, title)
          .run();
        return id;
      });

      // Step 3: Split into chunks
      const chunks = await step.do('split-text', async () => {
        return this.splitIntoChunks(content, title);
      });

      // Step 4: Store chunks in D1
      const chunkRecords = await step.do('store-chunks', async () => {
        const records = [];
        for (const [index, text] of chunks.entries()) {
          const chunkId = crypto.randomUUID();
          await this.env.DATABASE
            .prepare('INSERT INTO chunks (id, document_id, text, chunk_index) VALUES (?, ?, ?, ?)')
            .bind(chunkId, documentId, text, index)
            .run();
          records.push({ id: chunkId, text, index });
        }
        return records;
      });

      // Step 5: Generate embeddings
      const embeddings = await step.do('generate-embeddings', async () => {
        const texts = chunkRecords.map(c => c.text);
        const result = await this.env.AI.run('@cf/baai/bge-base-en-v1.5', {
          text: texts
        }) as { data: number[][] };
        return result.data;
      });

      // Step 6: Insert vectors into Vectorize
      await step.do('insert-vectors', async () => {
        const vectors = chunkRecords.map((chunk, idx) => ({
          id: chunk.id,
          values: embeddings[idx],
          metadata: { documentId, chunkId: chunk.id, title }
        }));
        await this.env.VECTOR_INDEX.upsert(vectors);
        return { count: vectors.length };
      });

      return {
        success: true,
        documentId,
        chunksCreated: chunkRecords.length,
        vectorsInserted: embeddings.length
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  private splitIntoChunks(content: string, title: string): string[] {
    const chunkSize = this.env.DEFAULT_CHUNK_SIZE || 500;
    const overlap = this.env.DEFAULT_CHUNK_OVERLAP || 100;
    const chunks: string[] = [];

    let start = 0;
    while (start < content.length) {
      const end = Math.min(start + chunkSize, content.length);
      chunks.push(content.slice(start, end));
      start = end - overlap;
      if (start >= content.length) break;
    }

    return chunks;
  }
}
```

## Wrangler Configuration

```jsonc
// wrangler.jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2024-01-15",

  "workflows": [
    {
      "name": "ingestion-workflow",
      "binding": "INGESTION_WORKFLOW",
      "class_name": "IngestionWorkflow"
    }
  ],

  "d1_databases": [
    { "binding": "DATABASE", "database_name": "my-db", "database_id": "..." }
  ],
  "r2_buckets": [
    { "binding": "ARTICLES_BUCKET", "bucket_name": "articles" }
  ],
  "vectorize": [
    { "binding": "VECTOR_INDEX", "index_name": "embeddings" }
  ],
  "ai": { "binding": "AI" }
}
```

## Triggering Workflows

### From a Worker

```typescript
export default {
  async fetch(request: Request, env: Env) {
    const { articleId, title, content } = await request.json();

    // Create a workflow instance
    const instance = await env.INGESTION_WORKFLOW.create({
      id: `ingest-${articleId}`,
      params: { articleId, title, content }
    });

    return Response.json({
      workflowId: instance.id,
      status: 'started'
    });
  }
};
```

### Checking Workflow Status

```typescript
// Get workflow status
const status = await env.INGESTION_WORKFLOW.get(workflowId);

console.log({
  status: status.status,  // 'running', 'complete', 'error'
  output: status.output   // Result from run() if complete
});
```

## Error Handling

### Step-Level Retry

Steps automatically retry on failure. Control retry behavior:

```typescript
await step.do('risky-operation', {
  retries: { limit: 3, delay: '10 seconds', backoff: 'exponential' }
}, async () => {
  // This will retry up to 3 times with exponential backoff
  return await riskyOperation();
});
```

### Workflow-Level Error Handling

```typescript
async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
  try {
    // All steps...
    return { success: true, result: '...' };
  } catch (error) {
    // Log error for debugging
    console.error('Workflow failed:', error);

    // Return failure result
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    };
  }
}
```

## Best Practices

### Step Naming

Use descriptive, unique step names:
- `store-article` (good)
- `step-1` (bad - not descriptive)
- `store-${articleId}` (bad - step names should be static)

### Step Granularity

- Make steps atomic (do one thing)
- Don't put retryable and non-retryable operations in same step
- Keep steps focused for better retry behavior

### Idempotency

Steps should be idempotent (safe to retry):
```typescript
// Good: Use upsert instead of insert
await this.env.VECTOR_INDEX.upsert(vectors);

// Bad: Insert might fail on retry
await this.env.VECTOR_INDEX.insert(vectors);
```

### Batching

Batch operations within steps for efficiency:
```typescript
// Good: Batch embedding generation
const embeddings = await step.do('generate-embeddings', async () => {
  const batchSize = 10;
  const allEmbeddings = [];

  for (let i = 0; i < texts.length; i += batchSize) {
    const batch = texts.slice(i, i + batchSize);
    const result = await this.env.AI.run(model, { text: batch });
    allEmbeddings.push(...result.data);
  }

  return allEmbeddings;
});
```

## Common Patterns

### Conditional Steps

```typescript
const needsProcessing = await step.do('check-exists', async () => {
  const existing = await this.env.DATABASE
    .prepare('SELECT id FROM documents WHERE article_id = ?')
    .bind(articleId)
    .first();
  return !existing;
});

if (needsProcessing) {
  await step.do('process-new', async () => {
    // Only runs for new documents
  });
}
```

### Parallel Steps

```typescript
// Steps must be sequential, but you can parallelize within a step
await step.do('parallel-operations', async () => {
  const [result1, result2] = await Promise.all([
    this.env.DATABASE.prepare('...').run(),
    this.env.STORAGE.put('...', data)
  ]);
  return { result1, result2 };
});
```

### Cleanup on Failure

```typescript
try {
  // ... workflow steps ...
} catch (error) {
  // Cleanup step runs even on failure
  await step.do('cleanup', async () => {
    await this.env.STORAGE.delete(`temp/${workflowId}`);
  });
  throw error;  // Re-throw to mark workflow as failed
}
```

## Monitoring

Check workflow status via the Cloudflare dashboard or API:
- Workflow runs in progress
- Completed workflows
- Failed workflows with error details
- Step-by-step execution logs

## Additional Resources

- Cloudflare Workflows documentation: https://developers.cloudflare.com/workflows/
- Use the cloudflare-docs-specialist agent to search for latest Workflows docs
- Reference the workers-development skill for general Workers patterns
