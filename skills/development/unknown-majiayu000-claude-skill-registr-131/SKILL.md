---
name: sse-resilience
description: Redis-backed SSE stream management with stream registry, heartbeat monitoring, completion store for terminal events, and automatic orphan cleanup via background guardian process.
license: MIT
compatibility: TypeScript/JavaScript
metadata:
  category: api
  time: 7h
  source: drift-masterguide
---

# SSE Stream Resilience

Redis-backed stream management with heartbeat monitoring and completion recovery.

## When to Use This Skill

- SSE streams can fail silently (client disconnects mid-stream)
- Completion events get lost and users never see results
- Need visibility into stream health
- Want to prevent resource leaks from abandoned streams

## Core Concepts

The solution provides:
- Stream registry (track all active streams in Redis)
- Heartbeat monitoring (detect orphaned streams)
- Completion store (persist terminal events for recovery)
- Stream guardian (background cleanup process)

```
Client ←→ SSE Endpoint ←→ Stream Registry (Redis)
                              ↓
                    Completion Store (Redis)
                              ↓
                    Stream Guardian (Background)
```

## Implementation

### TypeScript

```typescript
// lib/sse/types.ts
export enum StreamState {
  ACTIVE = 'active',
  COMPLETED = 'completed',
  FAILED = 'failed',
  ORPHANED = 'orphaned',
}

export interface StreamMetadata {
  streamId: string;
  streamType: string;
  userId: string;
  startedAt: Date;
  lastHeartbeat: Date;
  state: StreamState;
  metadata: Record<string, unknown>;
}

export interface CompletionData {
  streamId: string;
  terminalEventType: string;
  terminalEventData: Record<string, unknown>;
  completedAt: Date;
}

// lib/sse/stream-registry.ts
const STREAM_KEY_PREFIX = 'sse:stream:';
const ACTIVE_STREAMS_KEY = 'sse:active';
const STREAM_TTL = 3600;        // 1 hour max lifetime
const STALE_THRESHOLD = 30;     // 30 seconds = stale

export class StreamRegistry {
  constructor(private redis: Redis) {}

  async register(metadata: StreamMetadata): Promise<boolean> {
    const streamKey = `${STREAM_KEY_PREFIX}${metadata.streamId}`;

    if (await this.redis.exists(streamKey)) {
      return false;
    }

    const pipeline = this.redis.pipeline();

    pipeline.hset(streamKey, {
      streamId: metadata.streamId,
      streamType: metadata.streamType,
      userId: metadata.userId,
      startedAt: metadata.startedAt.toISOString(),
      lastHeartbeat: metadata.lastHeartbeat.toISOString(),
      state: metadata.state,
      metadata: JSON.stringify(metadata.metadata),
    });
    pipeline.expire(streamKey, STREAM_TTL);
    pipeline.zadd(ACTIVE_STREAMS_KEY, metadata.lastHeartbeat.getTime(), metadata.streamId);

    await pipeline.exec();
    return true;
  }

  async heartbeat(streamId: string): Promise<boolean> {
    const streamKey = `${STREAM_KEY_PREFIX}${streamId}`;
    const now = new Date();

    if (!await this.redis.exists(streamKey)) {
      return false;
    }

    const pipeline = this.redis.pipeline();
    pipeline.hset(streamKey, 'lastHeartbeat', now.toISOString());
    pipeline.zadd(ACTIVE_STREAMS_KEY, now.getTime(), streamId);
    await pipeline.exec();

    return true;
  }

  async unregister(streamId: string): Promise<boolean> {
    const streamKey = `${STREAM_KEY_PREFIX}${streamId}`;
    const userId = await this.redis.hget(streamKey, 'userId');

    if (!userId) return false;

    const pipeline = this.redis.pipeline();
    pipeline.del(streamKey);
    pipeline.zrem(ACTIVE_STREAMS_KEY, streamId);
    await pipeline.exec();

    return true;
  }

  async getStaleStreams(thresholdSeconds = STALE_THRESHOLD): Promise<StreamMetadata[]> {
    const cutoff = Date.now() - (thresholdSeconds * 1000);
    const staleIds = await this.redis.zrangebyscore(ACTIVE_STREAMS_KEY, 0, cutoff);

    const streams: StreamMetadata[] = [];
    for (const streamId of staleIds) {
      const stream = await this.getStream(streamId);
      if (stream && stream.state === StreamState.ACTIVE) {
        streams.push(stream);
      }
    }

    return streams;
  }

  async updateState(streamId: string, state: StreamState): Promise<boolean> {
    const streamKey = `${STREAM_KEY_PREFIX}${streamId}`;
    if (!await this.redis.exists(streamKey)) return false;
    await this.redis.hset(streamKey, 'state', state);
    return true;
  }
}

// lib/sse/completion-store.ts
const COMPLETION_KEY_PREFIX = 'sse:completion:';
const COMPLETION_TTL = 300;  // 5 minutes for recovery window

export class CompletionStore {
  constructor(private redis: Redis) {}

  async storeCompletion(data: CompletionData): Promise<void> {
    const key = `${COMPLETION_KEY_PREFIX}${data.streamId}`;

    await this.redis.hset(key, {
      streamId: data.streamId,
      terminalEventType: data.terminalEventType,
      terminalEventData: JSON.stringify(data.terminalEventData),
      completedAt: data.completedAt.toISOString(),
    });
    await this.redis.expire(key, COMPLETION_TTL);
  }

  async getCompletion(streamId: string): Promise<CompletionData | null> {
    const key = `${COMPLETION_KEY_PREFIX}${streamId}`;
    const data = await this.redis.hgetall(key);

    if (!data.streamId) return null;

    return {
      streamId: data.streamId,
      terminalEventType: data.terminalEventType,
      terminalEventData: JSON.parse(data.terminalEventData || '{}'),
      completedAt: new Date(data.completedAt),
    };
  }
}

// lib/sse/stream-guardian.ts
export class StreamGuardian {
  private intervalId: NodeJS.Timeout | null = null;

  constructor(
    private registry: StreamRegistry,
    private completionStore: CompletionStore,
    private checkIntervalMs = 30000
  ) {}

  start(): void {
    if (this.intervalId) return;

    this.intervalId = setInterval(
      () => this.runCheck(),
      this.checkIntervalMs
    );
  }

  stop(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }

  private async runCheck(): Promise<void> {
    try {
      const staleStreams = await this.registry.getStaleStreams();

      for (const stream of staleStreams) {
        await this.handleOrphanedStream(stream);
      }
    } catch (err) {
      console.error('Stream Guardian error:', err);
    }
  }

  private async handleOrphanedStream(stream: StreamMetadata): Promise<void> {
    console.log(`Handling orphaned stream: ${stream.streamId}`);
    await this.registry.updateState(stream.streamId, StreamState.ORPHANED);
  }
}
```

### SSE Endpoint

```typescript
// app/api/stream/[streamId]/route.ts
export async function GET(req: Request, { params }: { params: { streamId: string } }) {
  const userId = req.headers.get('x-user-id')!;
  const streamId = params.streamId;

  // Check for existing completion (recovery)
  const existingCompletion = await completionStore.getCompletion(streamId);
  if (existingCompletion) {
    return new Response(
      `data: ${JSON.stringify({
        type: existingCompletion.terminalEventType,
        data: existingCompletion.terminalEventData,
      })}\n\n`,
      { headers: { 'Content-Type': 'text/event-stream' } }
    );
  }

  // Register new stream
  await registry.register({
    streamId,
    streamType: 'generation',
    userId,
    startedAt: new Date(),
    lastHeartbeat: new Date(),
    state: StreamState.ACTIVE,
    metadata: {},
  });

  const encoder = new TextEncoder();
  let heartbeatInterval: NodeJS.Timeout;

  const stream = new ReadableStream({
    start(controller) {
      controller.enqueue(
        encoder.encode(`data: ${JSON.stringify({ type: 'connected', streamId })}\n\n`)
      );

      // Heartbeat every 15 seconds
      heartbeatInterval = setInterval(async () => {
        try {
          await registry.heartbeat(streamId);
          controller.enqueue(encoder.encode(`: heartbeat\n\n`));
        } catch {}
      }, 15000);
    },

    cancel() {
      clearInterval(heartbeatInterval);
      registry.unregister(streamId);
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'X-Stream-Id': streamId,
    },
  });
}
```

### Client-Side Recovery

```typescript
function useResilientSSE(streamId: string) {
  const [status, setStatus] = useState<'connecting' | 'connected' | 'completed' | 'error'>('connecting');
  const [data, setData] = useState<unknown>(null);
  const reconnectAttempts = useRef(0);

  useEffect(() => {
    let eventSource: EventSource | null = null;

    const connect = async () => {
      // First, check for existing completion
      try {
        const recovery = await fetch(`/api/stream/${streamId}/recover`);
        const result = await recovery.json();

        if (result.status === 'completed') {
          setStatus('completed');
          setData(result.terminalEventData);
          return;
        }
      } catch {}

      // Connect to SSE
      eventSource = new EventSource(`/api/stream/${streamId}`);

      eventSource.onmessage = (event) => {
        const parsed = JSON.parse(event.data);
        
        if (parsed.type === 'completed' || parsed.type === 'failed') {
          setStatus('completed');
          setData(parsed.data);
          eventSource?.close();
        } else {
          setData(parsed);
        }
      };

      eventSource.onerror = () => {
        eventSource?.close();
        
        if (reconnectAttempts.current < 3) {
          reconnectAttempts.current++;
          setTimeout(connect, 1000 * reconnectAttempts.current);
        } else {
          setStatus('error');
        }
      };
    };

    connect();
    return () => eventSource?.close();
  }, [streamId]);

  return { status, data };
}
```

## Best Practices

1. Heartbeat every 15 seconds - Keeps stream alive and detects orphans
2. Store completions for recovery - 5 minute window for client reconnection
3. Background guardian process - Clean up orphaned streams automatically
4. Client-side reconnection - Retry with exponential backoff
5. Check for completion on connect - Recover missed terminal events

## Common Mistakes

- No heartbeat mechanism (can't detect orphaned streams)
- Not storing completion data (lost terminal events)
- Missing recovery endpoint (clients can't recover)
- No background cleanup (resource leaks)
- Forgetting to unregister on clean disconnect

## Related Patterns

- websocket-management - WebSocket alternative
- graceful-shutdown - Drain streams on shutdown
- checkpoint-resume - Track stream progress
