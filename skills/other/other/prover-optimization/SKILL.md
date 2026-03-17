---
name: midnight-proofs:prover-optimization
description: Use when optimizing prover performance, reducing proof generation memory usage, configuring prover infrastructure in Docker or Kubernetes, implementing parallel proof generation, or diagnosing prover bottlenecks.
---

# Prover Optimization

Tune ZK prover performance for production workloads through memory optimization, parallelization, and infrastructure configuration.

## When to Use

- Optimizing proof generation speed for high-throughput services
- Reducing memory usage during proof generation
- Configuring prover infrastructure (Docker, Kubernetes)
- Implementing parallel proof generation with worker pools
- Diagnosing and fixing prover performance bottlenecks

## Key Concepts

### Performance Factors

| Factor | Impact | Optimization |
|--------|--------|--------------|
| **Circuit complexity** | High | Simplify circuit if possible |
| **Memory allocation** | High | Tune JVM/Node memory settings |
| **CPU cores** | Medium | Scale workers to available cores |
| **Disk I/O** | Low | Use SSD for circuit keys |
| **Network** | Low | Co-locate with dependent services |

### Memory Requirements

Proof generation is memory-intensive. Typical requirements:

| Circuit Complexity | Memory (per proof) |
|--------------------|--------------------|
| Simple (< 1000 constraints) | 512MB - 1GB |
| Medium (1000-10000 constraints) | 1GB - 4GB |
| Complex (> 10000 constraints) | 4GB - 16GB |

### Throughput Estimation

```
Proofs/hour = (Cores / Proofs-per-Core) * 3600 / Avg-Proof-Time-Seconds
```

Example: 8 cores, 2 proofs per core, 15 second proof time:
```
(8 / 2) * 3600 / 15 = 960 proofs/hour
```

## References

| Document | Description |
|----------|-------------|
| [memory-tuning.md](references/memory-tuning.md) | Memory configuration and optimization |
| [parallelization.md](references/parallelization.md) | Worker pools and concurrent proof generation |

## Examples

| Example | Description |
|---------|-------------|
| [docker-config/](examples/docker-config/) | Optimized Docker configuration |
| [worker-pool/](examples/worker-pool/) | Multi-process worker pool |

## Quick Start

### 1. Basic Memory Configuration

```typescript
import { createProver } from '@midnight-ntwrk/midnight-js-prover';

const prover = await createProver({
  circuitKeysPath: './circuit-keys',
  memoryLimit: 8192,  // 8GB
  threads: 4,         // Number of worker threads
});
```

### 2. Environment Variables

```bash
# Node.js memory settings
export NODE_OPTIONS="--max-old-space-size=8192"

# Prover-specific settings
export PROVER_MEMORY_LIMIT=8192
export PROVER_THREADS=4
export PROVER_PRELOAD_CIRCUITS="transfer,mint,burn"
```

### 3. Docker Resource Limits

```yaml
# docker-compose.yml
services:
  prover:
    image: prover-service:latest
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
```

## Common Patterns

### Circuit Key Preloading

```typescript
// Preload at startup to avoid load-time latency
const prover = await createProver({
  circuitKeysPath: './circuit-keys',
  preloadCircuits: ['transfer', 'mint', 'burn'],
});

// Verify circuits are loaded
const status = await prover.getStatus();
console.log('Loaded circuits:', status.loadedCircuits);
```

### Memory Monitoring

```typescript
import v8 from 'v8';

function getMemoryUsage(): {
  heapUsed: number;
  heapTotal: number;
  external: number;
} {
  const stats = v8.getHeapStatistics();
  return {
    heapUsed: Math.round(stats.used_heap_size / 1024 / 1024),
    heapTotal: Math.round(stats.total_heap_size / 1024 / 1024),
    external: Math.round(stats.external_memory / 1024 / 1024),
  };
}

// Log memory before/after proof generation
console.log('Before:', getMemoryUsage());
await prover.prove(circuitId, witness);
console.log('After:', getMemoryUsage());
```

### Backpressure Control

```typescript
class BackpressureController {
  private activeProofs = 0;
  private maxConcurrent: number;
  private waitQueue: Array<() => void> = [];

  constructor(maxConcurrent: number) {
    this.maxConcurrent = maxConcurrent;
  }

  async acquire(): Promise<void> {
    if (this.activeProofs < this.maxConcurrent) {
      this.activeProofs++;
      return;
    }

    // Wait for a slot
    await new Promise<void>((resolve) => {
      this.waitQueue.push(resolve);
    });
    this.activeProofs++;
  }

  release(): void {
    this.activeProofs--;
    const next = this.waitQueue.shift();
    if (next) next();
  }

  async withBackpressure<T>(fn: () => Promise<T>): Promise<T> {
    await this.acquire();
    try {
      return await fn();
    } finally {
      this.release();
    }
  }
}

// Usage
const controller = new BackpressureController(4); // Max 4 concurrent proofs

await controller.withBackpressure(async () => {
  return await prover.prove(circuitId, witness);
});
```

### Graceful Degradation

```typescript
async function proveWithFallback(
  circuitId: string,
  witness: WitnessData
): Promise<Proof> {
  const memoryUsage = getMemoryUsage();

  // If memory is high, wait before starting new proof
  if (memoryUsage.heapUsed > 6000) {
    console.warn('High memory usage, waiting...');
    await new Promise((r) => setTimeout(r, 5000));

    // Force garbage collection if available
    if (global.gc) {
      global.gc();
    }
  }

  try {
    return await prover.prove(circuitId, witness);
  } catch (error) {
    if (error.message.includes('out of memory')) {
      // Retry with reduced concurrency
      console.warn('OOM error, retrying after GC...');
      if (global.gc) global.gc();
      await new Promise((r) => setTimeout(r, 2000));
      return await prover.prove(circuitId, witness);
    }
    throw error;
  }
}
```

### Performance Metrics

```typescript
import { Counter, Histogram, Gauge } from 'prom-client';

const proofDuration = new Histogram({
  name: 'proof_generation_duration_seconds',
  help: 'Proof generation duration',
  labelNames: ['circuit_id'],
  buckets: [1, 5, 10, 15, 30, 60],
});

const proofCounter = new Counter({
  name: 'proofs_generated_total',
  help: 'Total proofs generated',
  labelNames: ['circuit_id', 'status'],
});

const memoryGauge = new Gauge({
  name: 'prover_memory_usage_bytes',
  help: 'Current prover memory usage',
});

// Instrument proof generation
async function proveWithMetrics(
  circuitId: string,
  witness: WitnessData
): Promise<Proof> {
  const end = proofDuration.startTimer({ circuit_id: circuitId });
  memoryGauge.set(process.memoryUsage().heapUsed);

  try {
    const proof = await prover.prove(circuitId, witness);
    proofCounter.inc({ circuit_id: circuitId, status: 'success' });
    return proof;
  } catch (error) {
    proofCounter.inc({ circuit_id: circuitId, status: 'error' });
    throw error;
  } finally {
    end();
  }
}
```

## Performance Considerations

| Concern | Mitigation |
|---------|------------|
| Memory fragmentation | Restart workers periodically |
| CPU throttling | Use dedicated prover nodes |
| GC pauses | Tune GC settings, limit heap size |
| Circuit load time | Preload circuits at startup |

## Related Skills

- `proof-generation` - Server-side proof generation
- `proof-caching` - Cache proofs to reduce generation load
- `proof-verification` - Verify generated proofs

## Related Commands

None currently defined.
