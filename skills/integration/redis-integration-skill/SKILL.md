---
name: redis-integration
description: Redis and Upstash Vector integration patterns for rate-limiting, vector search, embeddings, and memory systems. Use when implementing caching, rate-limiting, or semantic search features.
---

# Redis Integration Skill

## Overview

This project uses **dual Redis systems** for different purposes:

- **Upstash Redis**: Rate limiting, short-term memory (STM), general caching
- **Upstash Vector**: Episodic memory, semantic search with embeddings

## Architecture Decision: Dual-Path Vector Search

### System Selection

```typescript
Project Embeddings (1,536 dimensions)
├─> Redis FT.SEARCH (Redis Stack)
│   └─> Index: project_embeddings_idx
│   └─> Storage: HASH with VECTOR field
│   └─> Use Case: Project semantic search
│
Episodic Memory (OpenAI embeddings)
├─> Upstash Vector (Native vector DB)
    └─> No index name needed
    └─> Storage: Native vector format
    └─> Use Case: Conversation history search
```typescript

**Why Two Systems?**

- **Redis FT.SEARCH**: Already used for rate-limiting, good for structured data with metadata
- **Upstash Vector**: Purpose-built for vector operations, simpler API for pure vector search
- **No migration needed**: Each system serves its purpose optimally

## Core Files Reference

```typescript
src/lib/redis/
├── client.ts              # Redis client with FT.SEARCH extensions
├── vector-client.ts       # Upstash Vector client singleton
├── vector-search.ts       # Dual-path KNN search routing
├── embeddings.ts          # Project embedding generation & search
└── contact-storage.ts     # Contact form data storage

src/lib/
├── rate-limit.ts          # Rate limiting configurations
└── memory/
    ├── redis-memory.ts    # Memory manager (STM/LTM)
    ├── semantic-memory.ts # Facts/preferences storage
    └── types.ts           # Memory type definitions
```typescript

## 1. Redis Client with FT.SEARCH Extensions

### Location

`src/lib/redis/client.ts`

### Pattern: Extended Redis Client

**Problem:** Upstash Redis SDK doesn't natively support Redis Stack commands (FT.SEARCH, FT.CREATE)

**Solution:** Extend base client with custom command execution

```typescript
import { getRedisClient } from "@/lib/redis/client";

const redis = getRedisClient();

// ✅ Extended client supports Redis Stack commands
await redis.ft.create(indexName, schema, options);
await redis.ft.search(indexName, query, options);
await redis.call("FT.INFO", indexName);
```typescript

### Key Features

**1. Singleton Pattern**

```typescript
let cachedClient: RedisStackClient | null = null;

export function getRedisClient(): RedisStackClient {
  if (cachedClient) {
    return cachedClient;
  }
  // Create and cache client
  cachedClient = extendWithStackCommands(baseClient, url, token);
  return cachedClient;
}
```typescript

**2. FT.SEARCH Support**

```typescript
// Create vector index
await redis.ft.create(
  "project_embeddings_idx",
  {
    "$.slug": { type: "TEXT", AS: "slug" },
    "$.embedding": {
      type: "VECTOR",
      AS: "embedding",
    },
  },
  {
    ON: "HASH",
    PREFIX: "project:embedding:",
  }
);

// Search using KNN
const results = await redis.ft.search(
  "project_embeddings_idx",
  "*=>[KNN 5 @embedding $BLOB AS vector_score]",
  {
    PARAMS: ["BLOB", embeddingBuffer],
    RETURN: ["slug", "title", "vector_score"],
    LIMIT: { from: 0, size: 5 },
  }
);
```typescript

**3. Environment Variables Required**

```env
UPSTASH_REDIS_REST_URL=https://your-instance.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-token-here
```typescript

## 2. Upstash Vector Client

### Location

`src/lib/redis/vector-client.ts`

### Pattern: Separate Vector Database Client

**Why Separate?**

- Purpose-built for vector operations
- Simpler API for embeddings
- Optimized for semantic search
- No schema management needed

```typescript
import { getVectorClient } from "@/lib/redis/vector-client";

const vectorClient = getVectorClient();

// ✅ Simple vector operations
await vectorClient.upsert({
  id: "message-123",
  vector: embedding,
  metadata: { threadId, role, content },
});

const results = await vectorClient.query({
  vector: queryEmbedding,
  topK: 5,
  includeMetadata: true,
});
```typescript

### Environment Variables Required

```env
UPSTASH_VECTOR_REST_URL=https://your-vector-instance.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your-vector-token-here
```typescript

## 3. Dual-Path Vector Search Router

### Location

`src/lib/redis/vector-search.ts`

### Pattern: Intelligent Search Routing

### Routes searches to appropriate backend

```typescript
import { knnSearch } from "@/lib/redis/vector-search";

// ✅ Project search → Routes to Redis FT.SEARCH
const projectResults = await knnSearch(
  "project_embeddings_idx",  // Index name triggers Redis
  queryEmbedding,
  5,
  ["slug", "title", "description"]
);

// ✅ Memory search → Routes to Upstash Vector
const memoryResults = await knnSearch(
  undefined,  // No index = Upstash Vector
  queryEmbedding,
  3,
  ["threadId", "role", "content"]
);
```typescript

### Routing Logic

```typescript
export async function knnSearch(
  index: string | undefined,
  vector: number[],
  limit: number,
  returnFields: string[] = []
): Promise<VectorSearchResult[]> {
  // Route to Redis FT.SEARCH for project embeddings
  if (index === "project_embeddings_idx") {
    return knnSearchRedis(index, vector, limit, returnFields);
  }

  // Route to Upstash Vector for episodic memory
  return knnSearchVector(vector, limit, returnFields);
}
```typescript

### Benefits

- ✅ Single API for all vector searches
- ✅ Automatic backend selection
- ✅ Consistent result format
- ✅ Easy to add new indices

## 4. Rate Limiting Configuration

### Location

`src/lib/rate-limit.ts`

### Pattern: Sliding Window Rate Limits

### Multiple rate limiters for different endpoints

```typescript
import {
  chatRateLimit,
  toolsRateLimit,
  contactFormRateLimit,
  textEditorRateLimit,
} from "@/lib/rate-limit";

// ✅ In API route
export async function POST(request: Request) {
  const ip = request.headers.get("x-forwarded-for") || "anonymous";

  if (chatRateLimit) {
    const result = await chatRateLimit.limit(ip);
    if (!result.success) {
      return new Response("Rate limit exceeded", { status: 429 });
    }
  }

  // Process request...
}
```typescript

### Rate Limit Configurations

| Limiter                      | Rate    | Window   | Prefix                         | Use Case         |
| ---------------------------- | ------- | -------- | ------------------------------ | ---------------- |
| `chatRateLimit`              | 30 req  | 1 minute | `ratelimit:chat`               | OpenAI API calls |
| `toolsRateLimit`             | 60 req  | 1 minute | `ratelimit:tools`              | Tool endpoints   |
| `apiRateLimit`               | 100 req | 1 minute | `ratelimit:api`                | Generic APIs     |
| `contactCollectionRateLimit` | 5 req   | 24 hours | `ratelimit:contact-collection` | Contact sharing  |
| `textEditorRateLimit`        | 10 req  | 1 minute | `ratelimit:text-editor`        | AI text editing  |
| `contactFormRateLimit`       | 5 req   | 24 hours | `ratelimit:contact-form`       | Form submissions |

### Development Mode Fallback

```typescript
// ✅ Gracefully degrades in development
const redis =
  process.env.UPSTASH_REDIS_REST_URL && process.env.UPSTASH_REDIS_REST_TOKEN
    ? new Redis({
        url: process.env.UPSTASH_REDIS_REST_URL,
        token: process.env.UPSTASH_REDIS_REST_TOKEN,
      })
    : null;

export const chatRateLimit = redis
  ? new Ratelimit({
      redis,
      limiter: Ratelimit.slidingWindow(30, "1 m"),
    })
  : null;  // ← No rate-limiting in dev without credentials
```typescript

### Usage Pattern

```typescript
// Check rate limit
if (chatRateLimit) {
  const { success, reset } = await chatRateLimit.limit(identifier);

  if (!success) {
    return Response.json(
      {
        error: "Rate limit exceeded",
        resetAt: new Date(reset).toISOString(),
      },
      { status: 429 }
    );
  }
}
```typescript

## 5. Project Embeddings & Semantic Search

### Location

`src/lib/redis/embeddings.ts`

### Pattern: Generate + Store + Search

### Complete workflow for project semantic search

```typescript
import { generateProjectEmbedding, searchProjects } from "@/lib/redis/embeddings";

// ✅ Generate embedding for a project
const embedding = await generateProjectEmbedding(project);

// ✅ Search for similar projects
const results = await searchProjects(queryEmbedding, topK = 5);
```typescript

### Implementation Details

**1. Generate Embeddings**

```typescript
export async function generateProjectEmbedding(project: Project): Promise<number[]> {
  const text = `${project.title} ${project.description} ${project.tags.join(" ")}`;
  
  const embedding = await openai.embeddings.create({
    model: "text-embedding-3-small",
    input: text,
    dimensions: 1536,
  });
  
  return embedding.data[0].embedding;
}
```typescript

**2. Store in Redis with Vector Index**

```typescript
export async function storeProjectEmbedding(project: Project): Promise<void> {
  const redis = getRedisClient();
  const embedding = await generateProjectEmbedding(project);
  
  // Store as HASH with VECTOR field for FT.SEARCH
  await redis.hset(`project:embedding:${project.slug}`, {
    slug: project.slug,
    title: project.title,
    embedding: Buffer.from(new Float32Array(embedding)),
  });
}
```typescript

**3. Semantic Search**

```typescript
export async function searchProjects(
  queryEmbedding: number[],
  topK: number = 5
): Promise<Project[]> {
  const redis = getRedisClient();
  
  // KNN search via FT.SEARCH
  const results = await redis.ft.search(
    "project_embeddings_idx",
    "*=>[KNN 5 @embedding $BLOB AS vector_score]",
    {
      PARAMS: ["BLOB", Buffer.from(new Float32Array(queryEmbedding))],
      RETURN: ["slug", "title", "vector_score"],
      LIMIT: { from: 0, size: topK },
    }
  );
  
  return results.documents.map(doc => ({
    slug: doc.slug,
    similarity: parseFloat(doc.vector_score),
  }));
}
```typescript

## Summary & Decision Matrix

| System | Use Case | Backend | Pros | Cons |
|--------|----------|---------|------|------|
| **Redis FT.SEARCH** | Project embeddings | Redis Stack | Structured + vector search, metadata support | More complex setup |
| **Upstash Vector** | Episodic memory | Vector DB | Purpose-built, simple API | Pure vectors only |
| **Ratelimit** | API protection | Redis | Sliding window, flexible | Requires redis |

**Decision: Use both systems** - Each solves a specific problem optimally without overcomplicating the other.
