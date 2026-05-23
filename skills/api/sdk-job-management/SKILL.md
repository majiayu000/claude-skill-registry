---
name: Bankr x402 SDK - Job Management
description: This skill should be used when the user asks about "job status", "check if request completed", "cancel request", "why is my request taking so long", "poll for result", "batch requests", "retry failed request", "request timeout", "async operations", "job lifecycle", "manual polling", or needs advanced control over SDK async operations, manual job polling, batch processing, retry logic, or job cancellation.
version: 1.1.0
---

# SDK Job Management

Manage asynchronous jobs: submit, poll, check status, cancel, and batch operations.

## SDK Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| `promptAndWait()` | Submit and wait for result | **Recommended** for most cases |
| `prompt()` | Submit, return immediately | Background processing |
| `pollJob()` | Poll until job completes | Manual job tracking |
| `getJobStatus()` | Check status once | Custom polling logic |
| `cancelJob()` | Cancel pending/processing job | Stop unwanted jobs |

## Job Lifecycle

```
pending → processing → completed
                    ↘ failed
                    ↘ cancelled
```

| State | Cancellable | Description |
|-------|-------------|-------------|
| pending | Yes | Awaiting processing |
| processing | Yes | Actively processing |
| completed | No | Finished successfully |
| failed | No | Encountered error |
| cancelled | No | Cancelled by user |

## Usage Examples

### Recommended: promptAndWait

```typescript
const result = await client.promptAndWait({
  prompt: "Swap 0.1 ETH to USDC",
  timeout: 60000,
});

if (result.status === "completed") {
  console.log(result.response);
}
```

### Manual Job Control

```typescript
// Submit without waiting
const { jobId } = await client.prompt({ prompt: "What are trending tokens?" });

// Check status later
const status = await client.getJobStatus(jobId);

// Or poll until complete
const result = await client.pollJob({ jobId, timeout: 60000 });
```

### Cancel Job

```typescript
const { jobId } = await client.prompt({ prompt: "..." });
await client.cancelJob(jobId);
```

### Batch Processing

```typescript
const prompts = ["Price of ETH", "Price of BTC", "Price of SOL"];

// Submit all in parallel
const jobs = await Promise.all(
  prompts.map(prompt => client.prompt({ prompt }))
);

// Wait for all to complete
const results = await Promise.all(
  jobs.map(job => client.pollJob({ jobId: job.jobId }))
);
```

## Timing Guidelines

| Operation | Typical Time | Recommended Timeout |
|-----------|--------------|---------------------|
| Price queries | 2-5s | 15s |
| Balance checks | 2-5s | 15s |
| Token swaps | 5-15s | 60s |
| Cross-chain bridges | 10-30s | 120s |
| NFT operations | 5-15s | 60s |

## Related Skills

- **sdk-wallet-operations**: Client setup and configuration
- **sdk-capabilities**: Full list of supported operations
