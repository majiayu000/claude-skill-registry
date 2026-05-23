---
name: twinmind-sdk-patterns
description: |
  Apply production-ready TwinMind SDK patterns for TypeScript and Python.
  Use when implementing TwinMind integrations, refactoring API usage,
  or establishing team coding standards for meeting AI integration.
  Trigger with phrases like "twinmind SDK patterns", "twinmind best practices",
  "twinmind code patterns", "idiomatic twinmind".
allowed-tools: Read, Write, Edit
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# TwinMind SDK Patterns

## Overview
Production-ready patterns for TwinMind API integration in TypeScript and Python.

## Prerequisites
- Completed `twinmind-install-auth` setup
- Familiarity with async/await patterns
- Understanding of error handling best practices
- TwinMind Pro or Enterprise API access

## Instructions

### Step 1: Implement Singleton Pattern (Recommended)

```typescript
// src/twinmind/client.ts
import axios, { AxiosInstance } from 'axios';

let instance: TwinMindClient | null = null;

export interface TwinMindConfig {
  apiKey: string;
  baseUrl?: string;
  timeout?: number;
  retries?: number;
}

export class TwinMindClient {
  private client: AxiosInstance;
  private config: TwinMindConfig;

  private constructor(config: TwinMindConfig) {
    this.config = config;
    this.client = axios.create({
      baseURL: config.baseUrl || 'https://api.twinmind.com/v1',
      headers: {
        'Authorization': `Bearer ${config.apiKey}`,
        'Content-Type': 'application/json',
      },
      timeout: config.timeout || 30000,
    });
  }

  static getInstance(config?: TwinMindConfig): TwinMindClient {
    if (!instance) {
      if (!config) {
        throw new Error('TwinMindClient must be initialized with config');
      }
      instance = new TwinMindClient(config);
    }
    return instance;
  }

  static resetInstance(): void {
    instance = null;
  }
}

// Usage
export function getTwinMindClient(): TwinMindClient {
  return TwinMindClient.getInstance({
    apiKey: process.env.TWINMIND_API_KEY!,
  });
}
```

### Step 2: Add Error Handling Wrapper

```typescript
// src/twinmind/errors.ts
export class TwinMindError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode?: number,
    public readonly retryable: boolean = false,
    public readonly originalError?: Error
  ) {
    super(message);
    this.name = 'TwinMindError';
  }
}

export class TranscriptionError extends TwinMindError {
  constructor(message: string, originalError?: Error) {
    super(message, 'TRANSCRIPTION_FAILED', 500, true, originalError);
  }
}

export class RateLimitError extends TwinMindError {
  constructor(retryAfter: number) {
    super(`Rate limited. Retry after ${retryAfter}s`, 'RATE_LIMITED', 429, true);
  }
}

export class AuthenticationError extends TwinMindError {
  constructor() {
    super('Invalid or expired API key', 'AUTH_FAILED', 401, false);
  }
}

// Safe wrapper function
async function safeTwinMindCall<T>(
  operation: () => Promise<T>
): Promise<{ data: T | null; error: TwinMindError | null }> {
  try {
    const data = await operation();
    return { data, error: null };
  } catch (err: any) {
    const error = mapToTwinMindError(err);
    console.error({
      code: error.code,
      message: error.message,
      statusCode: error.statusCode,
      retryable: error.retryable,
    });
    return { data: null, error };
  }
}

function mapToTwinMindError(err: any): TwinMindError {
  if (err.response?.status === 401) {
    return new AuthenticationError();
  }
  if (err.response?.status === 429) {
    return new RateLimitError(parseInt(err.response.headers['retry-after'] || '60'));
  }
  if (err.response?.status >= 500) {
    return new TranscriptionError(err.message, err);
  }
  return new TwinMindError(err.message, 'UNKNOWN', err.response?.status);
}
```

### Step 3: Implement Retry Logic with Backoff

```typescript
// src/twinmind/retry.ts
interface RetryConfig {
  maxRetries: number;
  baseDelayMs: number;
  maxDelayMs: number;
  jitterMs: number;
}

const defaultRetryConfig: RetryConfig = {
  maxRetries: 3,
  baseDelayMs: 1000,
  maxDelayMs: 30000,
  jitterMs: 500,
};

async function withRetry<T>(
  operation: () => Promise<T>,
  config: Partial<RetryConfig> = {}
): Promise<T> {
  const { maxRetries, baseDelayMs, maxDelayMs, jitterMs } = {
    ...defaultRetryConfig,
    ...config,
  };

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await operation();
    } catch (err: any) {
      if (attempt === maxRetries) throw err;

      // Only retry on retryable errors
      const status = err.response?.status;
      if (status && status !== 429 && status < 500) throw err;

      // Exponential backoff with jitter
      const delay = Math.min(
        baseDelayMs * Math.pow(2, attempt) + Math.random() * jitterMs,
        maxDelayMs
      );

      console.log(`Attempt ${attempt + 1} failed. Retrying in ${delay.toFixed(0)}ms...`);
      await new Promise(r => setTimeout(r, delay));
    }
  }
  throw new Error('Unreachable');
}
```

### Step 4: Implement Transcript Processing Pipeline

```typescript
// src/twinmind/pipeline.ts
import { z } from 'zod';

// Zod schemas for validation
const SegmentSchema = z.object({
  start: z.number(),
  end: z.number(),
  text: z.string(),
  confidence: z.number().min(0).max(1),
  speaker_id: z.string().optional(),
});

const TranscriptSchema = z.object({
  id: z.string(),
  text: z.string(),
  duration_seconds: z.number().positive(),
  language: z.string(),
  segments: z.array(SegmentSchema),
  speakers: z.array(z.object({
    id: z.string(),
    name: z.string().optional(),
  })),
  created_at: z.string().datetime(),
});

export type Transcript = z.infer<typeof TranscriptSchema>;
export type Segment = z.infer<typeof SegmentSchema>;

// Pipeline processing
export class TranscriptPipeline {
  private processors: Array<(t: Transcript) => Transcript> = [];

  addProcessor(processor: (t: Transcript) => Transcript): this {
    this.processors.push(processor);
    return this;
  }

  process(transcript: Transcript): Transcript {
    return this.processors.reduce((t, processor) => processor(t), transcript);
  }
}

// Built-in processors
export const filterLowConfidence = (threshold: number) =>
  (transcript: Transcript): Transcript => ({
    ...transcript,
    segments: transcript.segments.filter(s => s.confidence >= threshold),
  });

export const mergeShortSegments = (minDurationMs: number) =>
  (transcript: Transcript): Transcript => {
    const merged: Segment[] = [];
    let buffer: Segment | null = null;

    for (const segment of transcript.segments) {
      const duration = (segment.end - segment.start) * 1000;

      if (duration < minDurationMs && buffer) {
        buffer = {
          ...buffer,
          end: segment.end,
          text: `${buffer.text} ${segment.text}`,
          confidence: (buffer.confidence + segment.confidence) / 2,
        };
      } else {
        if (buffer) merged.push(buffer);
        buffer = { ...segment };
      }
    }
    if (buffer) merged.push(buffer);

    return { ...transcript, segments: merged };
  };

// Usage example
const pipeline = new TranscriptPipeline()
  .addProcessor(filterLowConfidence(0.8))
  .addProcessor(mergeShortSegments(500));
```

### Step 5: Implement Caching Layer

```typescript
// src/twinmind/cache.ts
interface CacheEntry<T> {
  data: T;
  expiresAt: number;
}

class TranscriptCache {
  private cache = new Map<string, CacheEntry<any>>();
  private defaultTtlMs: number;

  constructor(defaultTtlMs = 3600000) { // 1 hour default
    this.defaultTtlMs = defaultTtlMs;
  }

  set<T>(key: string, data: T, ttlMs?: number): void {
    this.cache.set(key, {
      data,
      expiresAt: Date.now() + (ttlMs ?? this.defaultTtlMs),
    });
  }

  get<T>(key: string): T | null {
    const entry = this.cache.get(key);
    if (!entry) return null;
    if (Date.now() > entry.expiresAt) {
      this.cache.delete(key);
      return null;
    }
    return entry.data as T;
  }

  async getOrFetch<T>(
    key: string,
    fetcher: () => Promise<T>,
    ttlMs?: number
  ): Promise<T> {
    const cached = this.get<T>(key);
    if (cached) return cached;

    const data = await fetcher();
    this.set(key, data, ttlMs);
    return data;
  }

  invalidate(key: string): void {
    this.cache.delete(key);
  }

  clear(): void {
    this.cache.clear();
  }
}

export const transcriptCache = new TranscriptCache();
```

## Output
- Type-safe client singleton
- Robust error handling with custom error classes
- Automatic retry with exponential backoff
- Transcript processing pipeline
- Caching layer for API responses

## Error Handling

| Pattern | Use Case | Benefit |
|---------|----------|---------|
| Safe wrapper | All API calls | Prevents uncaught exceptions |
| Retry logic | Transient failures | Improves reliability |
| Pipeline processing | Transcript cleanup | Flexible data transformation |
| Caching | Repeated queries | Reduces API calls |
| Zod validation | Response parsing | Runtime type safety |

## Examples

### Python Context Manager

```python
# twinmind/client.py
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import httpx

class TwinMindClient:
    def __init__(self, api_key: str, base_url: str = "https://api.twinmind.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=30.0,
        )
        return self

    async def __aexit__(self, *args):
        if self._client:
            await self._client.aclose()

    async def transcribe(self, audio_url: str) -> dict:
        response = await self._client.post("/transcribe", json={"audio_url": audio_url})
        response.raise_for_status()
        return response.json()


@asynccontextmanager
async def get_twinmind_client() -> AsyncGenerator[TwinMindClient, None]:
    async with TwinMindClient(os.environ["TWINMIND_API_KEY"]) as client:
        yield client


# Usage
async def process_meeting(audio_url: str):
    async with get_twinmind_client() as client:
        transcript = await client.transcribe(audio_url)
        return transcript
```

### Multi-Tenant Factory Pattern

```typescript
// src/twinmind/factory.ts
const clients = new Map<string, TwinMindClient>();

export function getClientForOrganization(orgId: string): TwinMindClient {
  if (!clients.has(orgId)) {
    const apiKey = getOrganizationApiKey(orgId);
    clients.set(orgId, TwinMindClient.getInstance({
      apiKey,
      baseUrl: process.env.TWINMIND_API_URL,
    }));
  }
  return clients.get(orgId)!;
}

function getOrganizationApiKey(orgId: string): string {
  // Fetch from secrets manager or database
  return process.env[`TWINMIND_API_KEY_${orgId}`] ||
         process.env.TWINMIND_API_KEY!;
}
```

## Resources
- [TwinMind API Reference](https://twinmind.com/docs/api)
- [Zod Documentation](https://zod.dev/)
- [Axios Best Practices](https://axios-http.com/docs/intro)

## Next Steps
Apply patterns in `twinmind-core-workflow-a` for meeting transcription workflows.
