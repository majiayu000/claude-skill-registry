---
name: nats-vigil-messaging
description: NATS JetStream messaging for Vigil Guard 2.0+ migration. Use when implementing message queues, detection workers, request-reply API, async processing, Dead Letter Queues, or migrating from n8n webhooks to NATS-based architecture.
version: 2.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# NATS JetStream Messaging (v2.0.0)

## Overview

NATS JetStream is the message backbone for Vigil Guard 2.0+, replacing n8n workflow engine. This skill covers the planned migration architecture from the 24-node n8n workflow to NATS-based TypeScript Workers with Public API.

## When to Use This Skill

- Implementing NATS JetStream streams and consumers
- Creating TypeScript detection workers
- Building Public API with request-reply pattern
- Migrating n8n webhooks to NATS messaging
- Implementing Dead Letter Queues (DLQ)
- Setting up NATS cluster (R3 replication)
- Auto-scaling workers with KEDA

---

## Migration Context: n8n → NATS

### Current State (v2.0.0 - n8n)

```
Browser Extension → n8n Workflow (24 nodes) → ClickHouse
                           │
     ┌─────────────────────┼─────────────────────┐
     ▼                     ▼                     ▼
Heuristics (:5005)   Semantic (:5006)   LLM Guard (:8000)
   30% weight           35% weight          35% weight
                           │
                     Arbiter v2 Decision
                           │
               ┌───────────┴───────────┐
               ▼           ▼           ▼
             ALLOW     SANITIZE      BLOCK
```

### Target State (v3.0.0 - NATS JetStream)

```
External Clients (SDK, LangChain, CrewAI, Browser Extension)
                           │
                      HTTPS (TLS)
                           ▼
            ┌─────────────────────────────┐
            │       vigil-api (HPA)       │
            │   • Auth (API Key)          │
            │   • Rate Limiting (Redis)   │
            │   • Request Validation      │
            └─────────────┬───────────────┘
                          │
                   NATS Request-Reply
                          ▼
            ┌─────────────────────────────┐
            │   NATS JetStream Cluster    │
            │      (R3 Replication)       │
            │                             │
            │   Streams:                  │
            │   • vigil.guard.input       │
            │   • vigil.guard.output      │
            │   • vigil.detection.*       │
            │   • vigil.pii.*             │
            │   • vigil.arbiter.*         │
            │   • vigil.logs.*            │
            └─────────────┬───────────────┘
                          │
     ┌────────────────────┼────────────────────┐
     ▼                    ▼                    ▼
Detection Workers    PII Workers       Arbiter Workers
  (HPA: 3+)           (HPA: 2+)          (HPA: 2+)
     │                    │                    │
     └────────────────────┼────────────────────┘
                          ▼
                 Logging Worker (1)
                          │
                          ▼
                    ClickHouse
```

### Performance Comparison

| Metric | n8n (v2.0.0) | NATS Fast mode | NATS Full mode |
|--------|--------------|----------------|----------------|
| Throughput | 50 req/s | 500 req/s | 100-150 req/s |
| Latency P99 | 310ms | <300ms | <600ms |
| Scaling | Manual (1 pod) | Auto (HPA) | Auto (HPA) |
| Public API | None | REST + SDK | REST + SDK |

---

## NATS JetStream Concepts

### Core vs JetStream

| Feature | Core NATS | JetStream |
|---------|-----------|-----------|
| Persistence | No (at-most-once) | Yes (at-least-once, exactly-once) |
| Message Replay | No | Yes |
| Acknowledgements | No | Yes (AckExplicit) |
| Queues | No | Work Queues |
| Retention | No | Configurable |
| Latency | <1ms | 1-5ms |

### Replication (R1, R3, R5)

| Replication | Description | Use Case |
|-------------|-------------|----------|
| **R1** | No replication | Development, tests |
| **R3** | 3 copies (1 leader + 2 replicas) | **Production (recommended)** |
| **R5** | 5 copies (1 leader + 4 replicas) | Mission-critical |

**For Vigil Guard:** R3 (tolerates 1 node failure)

---

## Stream Configuration

### Main Stream: VIGIL

```typescript
// streams/vigil.ts
import { JetStreamManager, RetentionPolicy, StorageType, StoreCompression } from 'nats';

const vigilStreamConfig = {
  name: "VIGIL",
  subjects: [
    "vigil.guard.>",      // Input/Output moderation
    "vigil.detection.>",  // Detection pipeline
    "vigil.pii.>",        // PII detection
    "vigil.arbiter.>",    // Final decisions
    "vigil.logs.>"        // Async logging
  ],

  // Retention
  retention: RetentionPolicy.Workqueue,  // Delete after ACK
  max_age: 7 * 24 * 3600 * 1e9,          // 7 days (nanoseconds)
  max_bytes: 10 * 1024 * 1024 * 1024,    // 10GB
  max_msgs: 10_000_000,                   // 10M messages

  // Storage
  storage: StorageType.File,              // Persistent on disk
  num_replicas: 3,                        // R3 replication

  // Deduplication
  duplicate_window: 120 * 1e9,            // 2 minutes

  // Compression
  compression: StoreCompression.S2,       // S2 fast compression
};
```

### Dead Letter Queue Stream

```typescript
const dlqStreamConfig = {
  name: "VIGIL_DLQ",
  subjects: ["vigil.dlq.>"],

  retention: RetentionPolicy.Limits,
  max_age: 30 * 24 * 3600 * 1e9,  // 30 days
  max_bytes: 1 * 1024 * 1024 * 1024,  // 1GB

  storage: StorageType.File,
  num_replicas: 3,
};
```

---

## Consumer Configuration

### Detection Worker Consumer

```typescript
const detectionConsumerConfig = {
  durable_name: "detection-worker",
  filter_subjects: ["vigil.guard.*", "vigil.detection.>"],

  // Delivery
  deliver_policy: DeliverPolicy.New,
  ack_policy: AckPolicy.Explicit,

  // Retry
  max_deliver: 3,
  ack_wait: 30 * 1e9,  // 30s timeout

  // Backoff (exponential)
  backoff: [
    5 * 1e9,   // 5s after 1st failure
    30 * 1e9,  // 30s after 2nd failure
    60 * 1e9,  // 60s after 3rd failure → DLQ
  ],

  // Batching
  max_batch: 10,
  max_expires: 5 * 1e9,  // 5s max wait
};
```

### PII Worker Consumer

```typescript
const piiConsumerConfig = {
  durable_name: "pii-worker",
  filter_subjects: ["vigil.pii.>"],

  deliver_policy: DeliverPolicy.New,
  ack_policy: AckPolicy.Explicit,

  max_deliver: 3,
  ack_wait: 60 * 1e9,  // 60s (Presidio can be slow)

  backoff: [10 * 1e9, 30 * 1e9, 120 * 1e9],
};
```

### Arbiter Worker Consumer

```typescript
const arbiterConsumerConfig = {
  durable_name: "arbiter-worker",
  filter_subjects: ["vigil.arbiter.>"],

  deliver_policy: DeliverPolicy.New,
  ack_policy: AckPolicy.Explicit,

  max_deliver: 3,
  ack_wait: 10 * 1e9,  // 10s (fast decisions)

  backoff: [2 * 1e9, 5 * 1e9, 10 * 1e9],
};
```

---

## TypeScript Worker Template

### Base Worker Class

```typescript
// workers/base-worker.ts
import { connect, JetStreamClient, JetStreamManager, NatsConnection, ConsumerConfig } from 'nats';

export interface WorkerConfig {
  name: string;
  subjects: string[];
  consumerGroup: string;
  concurrency: number;
}

export abstract class BaseWorker {
  protected nc: NatsConnection;
  protected js: JetStreamClient;
  protected jsm: JetStreamManager;

  constructor(protected config: WorkerConfig) {}

  async start(): Promise<void> {
    // Connect to NATS
    this.nc = await connect({
      servers: process.env.NATS_SERVERS?.split(',') || ['nats://localhost:4222'],
      user: process.env.NATS_USER,
      pass: process.env.NATS_PASS,
    });

    this.js = this.nc.jetstream();
    this.jsm = await this.nc.jetstreamManager();

    console.log(`[${this.config.name}] Connected to NATS`);

    // Start consuming
    await this.consume();
  }

  protected async consume(): Promise<void> {
    const consumer = await this.js.consumers.get("VIGIL", this.config.consumerGroup);

    const messages = await consumer.consume({
      max_messages: this.config.concurrency,
    });

    for await (const msg of messages) {
      try {
        await this.process(msg);
        msg.ack();
      } catch (error) {
        console.error(`[${this.config.name}] Error processing message:`, error);

        if (msg.info.redeliveryCount >= 3) {
          // Move to DLQ
          await this.moveToDLQ(msg, error);
          msg.ack();  // Ack to prevent redelivery
        } else {
          msg.nak();  // Negative ack for retry
        }
      }
    }
  }

  protected async moveToDLQ(msg: any, error: Error): Promise<void> {
    const dlqSubject = `vigil.dlq.${this.config.name}`;
    const dlqPayload = {
      original_subject: msg.subject,
      original_data: msg.json(),
      error: error.message,
      redelivery_count: msg.info.redeliveryCount,
      timestamp: new Date().toISOString(),
    };

    await this.js.publish(dlqSubject, JSON.stringify(dlqPayload));
    console.error(`[${this.config.name}] Message moved to DLQ:`, dlqSubject);
  }

  abstract process(msg: any): Promise<void>;

  async shutdown(): Promise<void> {
    await this.nc.drain();
    console.log(`[${this.config.name}] Disconnected from NATS`);
  }
}
```

### Detection Worker Implementation

```typescript
// workers/detection-worker.ts
import { BaseWorker } from './base-worker';
import { HeuristicsClient } from '../clients/heuristics';
import { SemanticClient } from '../clients/semantic';
import { LLMGuardClient } from '../clients/llm-guard';

interface DetectionResult {
  branch_a_score: number;  // Heuristics (30%)
  branch_b_score: number;  // Semantic (35%)
  branch_c_score: number;  // LLM Guard (35%)
  weighted_score: number;
  categories: string[];
}

export class DetectionWorker extends BaseWorker {
  private heuristics: HeuristicsClient;
  private semantic: SemanticClient;
  private llmGuard: LLMGuardClient;

  constructor() {
    super({
      name: 'detection-worker',
      subjects: ['vigil.guard.*', 'vigil.detection.>'],
      consumerGroup: 'detection-worker',
      concurrency: 10,
    });

    this.heuristics = new HeuristicsClient('http://heuristics-service:5005');
    this.semantic = new SemanticClient('http://semantic-service:5006');
    this.llmGuard = new LLMGuardClient('http://prompt-guard-api:8000');
  }

  async process(msg: any): Promise<void> {
    const data = msg.json();
    const { request_id, text, mode = 'full' } = data;

    console.log(`[detection-worker] Processing ${request_id}, mode: ${mode}`);

    // 3-Branch Parallel Detection
    const [branchA, branchB, branchC] = await Promise.all([
      this.heuristics.analyze(text, 1000),      // 1s timeout
      this.semantic.analyze(text, 2000),        // 2s timeout
      mode === 'full'
        ? this.llmGuard.analyze(text, 3000)     // 3s timeout
        : Promise.resolve({ score: 0, categories: [] }),  // Skip in fast mode
    ]);

    // Weighted fusion (Arbiter v2 logic)
    const weightedScore = mode === 'full'
      ? (branchA.score * 0.30) + (branchB.score * 0.35) + (branchC.score * 0.35)
      : (branchA.score * 0.462) + (branchB.score * 0.538);  // Recalculate without C

    const result: DetectionResult = {
      branch_a_score: branchA.score,
      branch_b_score: branchB.score,
      branch_c_score: branchC.score,
      weighted_score: weightedScore,
      categories: [...new Set([
        ...branchA.categories,
        ...branchB.categories,
        ...branchC.categories,
      ])],
    };

    // Publish to arbiter
    await this.js.publish('vigil.arbiter.decision', JSON.stringify({
      request_id,
      text,
      detection: result,
    }));
  }
}
```

### PII Worker Implementation

```typescript
// workers/pii-worker.ts
import { BaseWorker } from './base-worker';
import { PresidioClient } from '../clients/presidio';
import { LanguageDetectorClient } from '../clients/language-detector';

export class PIIWorker extends BaseWorker {
  private presidio: PresidioClient;
  private langDetector: LanguageDetectorClient;

  constructor() {
    super({
      name: 'pii-worker',
      subjects: ['vigil.pii.>'],
      consumerGroup: 'pii-worker',
      concurrency: 5,
    });

    this.presidio = new PresidioClient('http://presidio-pii-api:5001');
    this.langDetector = new LanguageDetectorClient('http://language-detector:5002');
  }

  async process(msg: any): Promise<void> {
    const { request_id, text, sanitize_text } = msg.json();

    // Detect language
    const { language } = await this.langDetector.detect(text);

    // Dual-language PII detection (Polish first for PESEL)
    const languages = language === 'pl' ? ['pl', 'en'] : ['en', 'pl'];

    const [plResult, enResult] = await Promise.all([
      this.presidio.analyze(text, languages[0]),
      this.presidio.analyze(text, languages[1]),
    ]);

    // Deduplicate entities
    const entities = this.deduplicateEntities([...plResult.entities, ...enResult.entities]);

    // Sanitize if requested
    let sanitized_text = text;
    if (sanitize_text && entities.length > 0) {
      sanitized_text = await this.presidio.anonymize(text, entities);
    }

    // Publish result
    await this.js.publish('vigil.pii.result', JSON.stringify({
      request_id,
      pii_detected: entities.length > 0,
      entity_count: entities.length,
      entities,
      sanitized_text,
      language,
    }));
  }

  private deduplicateEntities(entities: any[]): any[] {
    // Sort by score (highest first), then by length (longest first)
    const sorted = entities.sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score;
      return (b.end - b.start) - (a.end - a.start);
    });

    // Remove overlapping entities
    const result: any[] = [];
    for (const entity of sorted) {
      const overlaps = result.some(e =>
        (entity.start >= e.start && entity.start < e.end) ||
        (entity.end > e.start && entity.end <= e.end)
      );
      if (!overlaps) {
        result.push(entity);
      }
    }
    return result;
  }
}
```

---

## Request-Reply Pattern (vigil-api)

### API Request Handler

```typescript
// api/handlers/guard.ts
import { Request, Response } from 'express';
import { connect, StringCodec, JSONCodec } from 'nats';

const sc = StringCodec();
const jc = JSONCodec();

export async function guardInputHandler(req: Request, res: Response) {
  const { text, mode = 'full', return_decision_process = false } = req.body;
  const request_id = `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

  try {
    const nc = await connect({ servers: process.env.NATS_SERVERS });

    // Publish to NATS with reply subject
    const response = await nc.request(
      'vigil.guard.input',
      jc.encode({ request_id, text, mode, return_decision_process }),
      { timeout: 5000 }  // 5s timeout
    );

    const result = jc.decode(response.data);

    await nc.close();

    return res.json({
      request_id,
      decision: result.decision,  // ALLOW | SANITIZE | BLOCK
      threat_score: result.threat_score,
      categories: result.categories,
      pii_detected: result.pii_detected,
      ...(return_decision_process && { decision_process: result.decision_process }),
    });

  } catch (error) {
    if (error.code === 'TIMEOUT') {
      return res.status(504).json({
        error: 'Gateway Timeout',
        message: 'Detection pipeline timeout',
        request_id,
      });
    }
    throw error;
  }
}
```

---

## Docker Compose Configuration

### NATS JetStream Cluster

```yaml
# docker-compose.nats.yml
version: '3.8'

services:
  nats-0:
    image: nats:2.10-alpine
    container_name: vigil-nats-0
    command:
      - "--name=nats-0"
      - "--cluster_name=vigil-cluster"
      - "--cluster=nats://0.0.0.0:6222"
      - "--routes=nats://nats-1:6222,nats://nats-2:6222"
      - "--http_port=8222"
      - "--js"
      - "--sd=/data/jetstream"
    volumes:
      - nats-0-data:/data/jetstream
    networks:
      - vigil-net
    ports:
      - "4222:4222"   # Client
      - "8222:8222"   # Monitoring
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:8222/healthz"]
      interval: 5s
      timeout: 3s
      retries: 3

  nats-1:
    image: nats:2.10-alpine
    container_name: vigil-nats-1
    command:
      - "--name=nats-1"
      - "--cluster_name=vigil-cluster"
      - "--cluster=nats://0.0.0.0:6222"
      - "--routes=nats://nats-0:6222,nats://nats-2:6222"
      - "--http_port=8222"
      - "--js"
      - "--sd=/data/jetstream"
    volumes:
      - nats-1-data:/data/jetstream
    networks:
      - vigil-net
    depends_on:
      nats-0:
        condition: service_healthy

  nats-2:
    image: nats:2.10-alpine
    container_name: vigil-nats-2
    command:
      - "--name=nats-2"
      - "--cluster_name=vigil-cluster"
      - "--cluster=nats://0.0.0.0:6222"
      - "--routes=nats://nats-0:6222,nats://nats-1:6222"
      - "--http_port=8222"
      - "--js"
      - "--sd=/data/jetstream"
    volumes:
      - nats-2-data:/data/jetstream
    networks:
      - vigil-net
    depends_on:
      nats-0:
        condition: service_healthy

volumes:
  nats-0-data:
  nats-1-data:
  nats-2-data:

networks:
  vigil-net:
    external: true
```

### Workers Configuration

```yaml
# docker-compose.workers.yml
version: '3.8'

services:
  detection-worker:
    image: vigil-guard/detection-worker:2.0.0
    container_name: vigil-detection-worker
    environment:
      - NATS_SERVERS=nats://nats-0:4222,nats://nats-1:4222,nats://nats-2:4222
      - HEURISTICS_URL=http://heuristics-service:5005
      - SEMANTIC_URL=http://semantic-service:5006
      - LLM_GUARD_URL=http://prompt-guard-api:8000
      - WORKER_CONCURRENCY=10
    networks:
      - vigil-net
    depends_on:
      nats-0:
        condition: service_healthy
    deploy:
      replicas: 3

  pii-worker:
    image: vigil-guard/pii-worker:2.0.0
    container_name: vigil-pii-worker
    environment:
      - NATS_SERVERS=nats://nats-0:4222,nats://nats-1:4222,nats://nats-2:4222
      - PRESIDIO_URL=http://presidio-pii-api:5001
      - LANGUAGE_DETECTOR_URL=http://language-detector:5002
      - WORKER_CONCURRENCY=5
    networks:
      - vigil-net
    depends_on:
      nats-0:
        condition: service_healthy
    deploy:
      replicas: 2

  arbiter-worker:
    image: vigil-guard/arbiter-worker:2.0.0
    container_name: vigil-arbiter-worker
    environment:
      - NATS_SERVERS=nats://nats-0:4222,nats://nats-1:4222,nats://nats-2:4222
      - BLOCK_THRESHOLD=70
      - SANITIZE_THRESHOLD=30
    networks:
      - vigil-net
    depends_on:
      nats-0:
        condition: service_healthy
    deploy:
      replicas: 2

  logging-worker:
    image: vigil-guard/logging-worker:2.0.0
    container_name: vigil-logging-worker
    environment:
      - NATS_SERVERS=nats://nats-0:4222,nats://nats-1:4222,nats://nats-2:4222
      - CLICKHOUSE_HOST=clickhouse
      - CLICKHOUSE_PORT=8123
      - CLICKHOUSE_DATABASE=n8n_logs
      - BATCH_SIZE=100
      - FLUSH_INTERVAL_MS=5000
    networks:
      - vigil-net
    depends_on:
      nats-0:
        condition: service_healthy
    deploy:
      replicas: 1
```

---

## NATS CLI Commands

### Stream Management

```bash
# Connect to NATS
nats context add vigil --server nats://localhost:4222

# Create VIGIL stream
nats stream add VIGIL \
  --subjects "vigil.>" \
  --retention work \
  --storage file \
  --replicas 3 \
  --max-age 7d \
  --max-bytes 10GB \
  --discard old

# Create DLQ stream
nats stream add VIGIL_DLQ \
  --subjects "vigil.dlq.>" \
  --retention limits \
  --storage file \
  --replicas 3 \
  --max-age 30d

# View stream info
nats stream info VIGIL
nats stream info VIGIL_DLQ
```

### Consumer Management

```bash
# Create detection worker consumer
nats consumer add VIGIL detection-worker \
  --filter "vigil.guard.*,vigil.detection.>" \
  --deliver new \
  --ack explicit \
  --max-deliver 3 \
  --wait 30s \
  --pull

# Create PII worker consumer
nats consumer add VIGIL pii-worker \
  --filter "vigil.pii.>" \
  --deliver new \
  --ack explicit \
  --max-deliver 3 \
  --wait 60s \
  --pull

# View consumer info
nats consumer info VIGIL detection-worker
nats consumer ls VIGIL
```

### Monitoring

```bash
# Watch messages in real-time
nats sub "vigil.>"

# View stream stats
nats stream report

# View consumer stats
nats consumer report VIGIL

# Check DLQ
nats stream view VIGIL_DLQ --last 10
```

---

## Integration Points

### With detection workers:
```yaml
when: vigil.guard.input message received
action:
  1. Detection worker consumes message
  2. Parallel calls to Branch A, B, C
  3. Weighted score calculation (30%/35%/35%)
  4. Publish to vigil.arbiter.decision
```

### With PII workers:
```yaml
when: vigil.pii.detect message received
action:
  1. Language detection
  2. Dual-language Presidio calls (Polish + English)
  3. Entity deduplication
  4. Publish to vigil.pii.result
```

### With arbiter workers:
```yaml
when: vigil.arbiter.decision message received
action:
  1. Apply threshold logic (BLOCK >= 70, SANITIZE >= 30)
  2. Handle sanitization if needed
  3. Reply to original request
  4. Publish to vigil.logs.event
```

### With ClickHouse logging:
```yaml
when: vigil.logs.* message received
action:
  1. Batch messages (100 max, 5s flush)
  2. Insert to n8n_logs.vigil_events
  3. Include branch_a/b/c_score, arbiter_decision
```

---

## Troubleshooting

### NATS cluster not forming

```bash
# Check cluster status
nats server info

# Verify routes
docker logs vigil-nats-0 | grep "Route"

# Check JetStream
nats server js
```

### Messages stuck in stream

```bash
# Check pending messages
nats consumer info VIGIL detection-worker

# Force NAK all pending
nats consumer next VIGIL detection-worker --count 100 --nak

# Purge stream (DANGEROUS!)
nats stream purge VIGIL
```

### DLQ growing

```bash
# View DLQ messages
nats stream view VIGIL_DLQ --last 50

# Analyze failure patterns
nats sub "vigil.dlq.>" --count 10 | jq '.error'
```

---

## Quick Reference

```bash
# Start NATS cluster
docker-compose -f docker-compose.nats.yml up -d

# Start workers
docker-compose -f docker-compose.workers.yml up -d

# Scale detection workers
docker-compose -f docker-compose.workers.yml up -d --scale detection-worker=5

# Monitor streams
nats stream report

# Publish test message
nats pub vigil.guard.input '{"request_id":"test-1","text":"Test input"}'

# View worker logs
docker logs -f vigil-detection-worker

# Check NATS health
curl http://localhost:8222/healthz
```

---

## Reference Documentation

### Vigil Roadmap Documents
- [PRD_ETAP1.md](/Vigil-Roadmap/n8n-migration/etap1-nats-api/PRD_ETAP1.md) - Product Requirements
- [VIGIL_2.0_COMPLETE_ARCHITECTURE.md](/Vigil-Roadmap/n8n-migration/etap1-nats-api/architecture/VIGIL_2.0_COMPLETE_ARCHITECTURE.md) - Full Architecture
- [NATS_JETSTREAM_TECHNICAL_GUIDE.md](/Vigil-Roadmap/n8n-migration/etap1-nats-api/architecture/NATS_JETSTREAM_TECHNICAL_GUIDE.md) - NATS Deep-Dive

### External Documentation
- [NATS JetStream](https://docs.nats.io/nats-concepts/jetstream)
- [NATS TypeScript Client](https://github.com/nats-io/nats.js)
- [KEDA NATS Scaler](https://keda.sh/docs/scalers/nats-jetstream/)

---

**Version:** 2.0.0 (Migration Planning)
**Status:** PLANNED (Etap 1 - Week 0 + 5 tygodni)
**Architecture:** n8n → NATS JetStream + TypeScript Workers
**Target Throughput:** 500 req/s (Fast mode) / 150 req/s (Full mode)
**Target Latency:** P99 <300ms (Fast) / <600ms (Full)
