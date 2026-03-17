---
name: midnight-proofs:proof-generation
description: Use when generating ZK proofs server-side, building proof-as-a-service backends, offloading proof computation from clients, creating proof generation queues, or implementing async proof generation.
---

# Proof Generation

Generate ZK proofs server-side to offload computation from client devices and build scalable proof-as-a-service backends.

## When to Use

- Building a backend service that generates proofs for clients
- Offloading proof computation from mobile or low-power devices
- Creating a proof generation queue for high-throughput applications
- Implementing async proof generation with status polling
- Handling proof generation timeouts and errors

## Key Concepts

### Server-Side vs Client-Side Proving

| Aspect | Client-Side | Server-Side |
|--------|-------------|-------------|
| **Privacy** | Witness data stays local | Witness sent to server (encrypted) |
| **Latency** | Limited by device power | Fast dedicated hardware |
| **Scalability** | One proof at a time | Parallel proof generation |
| **Use Case** | Privacy-critical apps | High-throughput services |

### Proof Generation Flow

1. **Receive Request** - Accept witness data and circuit identifier
2. **Load Circuit** - Retrieve proving key for the circuit
3. **Generate Proof** - Execute the prover with witness inputs
4. **Return Proof** - Send proof bytes back to client

```typescript
// Server-side proof generation overview
async function generateProof(request: ProofRequest): Promise<ProofResponse> {
  const { circuitId, witness } = request;

  // Load circuit proving key
  const provingKey = await loadProvingKey(circuitId);

  // Generate the proof (CPU intensive)
  const proof = await prover.prove(provingKey, witness);

  return { proof, circuitId };
}
```

### Witness Data Handling

Witness data contains private inputs to the circuit. When handling server-side:

- **Encrypt in transit** - Use TLS and consider additional encryption
- **Minimize retention** - Delete witness data immediately after proof generation
- **Audit logging** - Log proof requests (not witness content) for debugging
- **Access control** - Authenticate and authorize proof requests

## References

| Document | Description |
|----------|-------------|
| [prover-api.md](references/prover-api.md) | Prover SDK setup and API reference |
| [witness-formatting.md](references/witness-formatting.md) | Witness input structure and validation |

## Examples

| Example | Description |
|---------|-------------|
| [rest-endpoint/](examples/rest-endpoint/) | Express REST API for proof generation |
| [queue-worker/](examples/queue-worker/) | Redis queue-based proof worker |

## Quick Start

### 1. Set Up Prover Service

```typescript
import { createProver } from '@midnight-ntwrk/midnight-js-prover';

const prover = await createProver({
  // Path to circuit proving keys
  circuitKeysPath: './circuit-keys',
  // Memory limit for proof generation
  memoryLimit: 4096, // MB
});
```

### 2. Create Proof Endpoint

```typescript
import express from 'express';

const app = express();
app.use(express.json());

app.post('/api/prove', async (req, res) => {
  const { circuitId, witness } = req.body;

  try {
    const proof = await prover.prove(circuitId, witness);
    res.json({ success: true, proof: proof.toString('base64') });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});
```

### 3. Handle Async Requests

```typescript
// For long-running proofs, use async pattern
app.post('/api/prove/async', async (req, res) => {
  const { circuitId, witness } = req.body;

  // Create job ID
  const jobId = crypto.randomUUID();

  // Queue proof generation
  await proofQueue.add({ jobId, circuitId, witness });

  // Return immediately with job ID
  res.json({ jobId, status: 'queued' });
});

// Poll for status
app.get('/api/prove/status/:jobId', async (req, res) => {
  const job = await proofQueue.getJob(req.params.jobId);

  if (!job) {
    return res.status(404).json({ error: 'Job not found' });
  }

  if (job.status === 'completed') {
    return res.json({ status: 'completed', proof: job.result });
  }

  res.json({ status: job.status });
});
```

## Common Patterns

### Request Validation

```typescript
import { z } from 'zod';

const ProofRequestSchema = z.object({
  circuitId: z.string().min(1),
  witness: z.record(z.unknown()),
  timeout: z.number().optional().default(60000),
});

function validateProofRequest(body: unknown) {
  return ProofRequestSchema.parse(body);
}
```

### Timeout Handling

```typescript
async function proveWithTimeout(
  circuitId: string,
  witness: WitnessData,
  timeoutMs = 60000
): Promise<Proof> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    return await prover.prove(circuitId, witness, {
      signal: controller.signal,
    });
  } finally {
    clearTimeout(timeout);
  }
}
```

### Health Check Endpoint

```typescript
app.get('/health', async (req, res) => {
  try {
    // Verify prover is ready
    const isReady = await prover.isReady();

    res.json({
      status: isReady ? 'healthy' : 'degraded',
      proverReady: isReady,
      uptime: process.uptime(),
    });
  } catch (error) {
    res.status(503).json({ status: 'unhealthy', error: error.message });
  }
});
```

### Error Categories

```typescript
enum ProofErrorCode {
  INVALID_WITNESS = 'INVALID_WITNESS',
  CIRCUIT_NOT_FOUND = 'CIRCUIT_NOT_FOUND',
  PROOF_GENERATION_FAILED = 'PROOF_GENERATION_FAILED',
  TIMEOUT = 'TIMEOUT',
  OUT_OF_MEMORY = 'OUT_OF_MEMORY',
}

class ProofError extends Error {
  constructor(
    public code: ProofErrorCode,
    message: string,
    public details?: unknown
  ) {
    super(message);
    this.name = 'ProofError';
  }
}
```

## Performance Considerations

| Concern | Mitigation |
|---------|------------|
| CPU-intensive proof generation | Use worker threads or separate processes |
| Memory spikes during proving | Set memory limits, monitor usage |
| Long request timeouts | Use async job queue pattern |
| Circuit key loading time | Pre-load keys at startup |

## Related Skills

- `proof-verification` - Verify generated proofs
- `proof-caching` - Cache proof components for performance
- `prover-optimization` - Tune prover for production workloads

## Related Commands

None currently defined.
