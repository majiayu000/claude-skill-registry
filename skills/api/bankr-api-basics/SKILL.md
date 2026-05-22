---
name: Bankr Dev - API Basics
description: This skill should be used when the user asks about "Bankr API", "Bankr Agent API", "how does Bankr work", "Bankr job status", "Bankr response format", or "building on Bankr". Provides endpoint documentation, job patterns, and TypeScript interfaces.
version: 1.0.0
---

# Bankr Agent API Essentials

When answering questions about the Bankr API:
1. Explain the asynchronous job pattern (submit-poll-complete)
2. Reference the endpoint documentation and TypeScript examples below
3. For detailed response structures, consult `references/job-response-schema.md`
4. Point developers to working examples in `examples/` directory

---

The Bankr Agent API enables programmatic access to crypto trading, market analysis, and prediction markets through a simple asynchronous job pattern.

## Core Concept: Asynchronous Job Pattern

All Bankr operations follow a submit-poll-complete pattern:

1. **Submit** a natural language prompt to start a job
2. **Poll** the job status every 2 seconds
3. **Receive** results when status is terminal (completed/failed/cancelled)

This pattern handles operations that may take 30 seconds to 2+ minutes (trades, complex analysis).

## API Endpoints

### Base URL
```
https://api.bankr.bot
```

### Authentication
All requests require the `x-api-key` header:
```
x-api-key: bk_your_api_key_here
```

The API key is tied to a specific user's Bankr account and wallet.

### Endpoint 1: Submit Prompt
```
POST /agent/prompt
Content-Type: application/json

{
  "prompt": "Buy $50 of ETH on Base"
}
```

**Response:**
```json
{
  "success": true,
  "jobId": "job_abc123",
  "status": "pending"
}
```

**Code example:**
```typescript
async function submitPrompt(prompt: string): Promise<{ jobId: string }> {
  const response = await fetch(`${API_URL}/agent/prompt`, {
    method: "POST",
    headers: {
      "x-api-key": API_KEY,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt }),
  });
  const data = await response.json();
  if (!data.success) throw new Error(data.error || "Failed to submit");
  return { jobId: data.jobId };
}
```

### Endpoint 2: Get Job Status
```
GET /agent/job/{jobId}
```

**Response:**
```json
{
  "success": true,
  "jobId": "job_abc123",
  "status": "completed",
  "prompt": "What is the price of ETH?",
  "response": "Ethereum (ETH) is currently trading at $3,245.67...",
  "transactions": [],
  "statusUpdates": [
    { "message": "Fetching price data...", "timestamp": "2024-01-15T10:00:02Z" }
  ],
  "createdAt": "2024-01-15T10:00:00Z",
  "completedAt": "2024-01-15T10:00:05Z",
  "processingTime": 5000
}
```

**Code example:**
```typescript
async function getJobStatus(jobId: string): Promise<JobStatusResponse> {
  const response = await fetch(`${API_URL}/agent/job/${jobId}`, {
    headers: { "x-api-key": API_KEY },
  });
  return response.json();
}
```

For complete TypeScript interfaces, see `references/job-response-schema.md`.

### Endpoint 3: Cancel Job
```
POST /agent/job/{jobId}/cancel
Content-Type: application/json
```

**Response:**
```json
{
  "success": true,
  "jobId": "job_abc123",
  "status": "cancelled",
  "prompt": "Buy $50 of ETH on Base",
  "cancelledAt": "2024-01-15T10:00:15Z"
}
```

**When to cancel:**
- User requests to stop a long-running operation
- Timeout exceeded and want to abort cleanly
- Detected an error condition that makes the job unnecessary

**Code example:**
```typescript
async function cancelJob(jobId: string): Promise<JobStatusResponse> {
  const response = await fetch(`${API_URL}/agent/job/${jobId}/cancel`, {
    method: "POST",
    headers: {
      "x-api-key": API_KEY,
      "Content-Type": "application/json",
    },
  });
  return response.json();
}

// Usage: Cancel if job takes too long
const timeout = setTimeout(async () => {
  console.log("Job taking too long, cancelling...");
  await cancelJob(jobId);
}, 60000); // Cancel after 60 seconds
```

## Job Status States

| Status | Meaning | Action |
|--------|---------|--------|
| `pending` | Job queued, not started | Keep polling |
| `processing` | Job running | Keep polling, check statusUpdates |
| `completed` | Job finished successfully | Read response and transactions |
| `failed` | Job encountered error | Check error field |
| `cancelled` | Job was cancelled | No further action |

## What You Can Do

The Bankr API accepts natural language prompts for:

**Crypto Trading:**
- "Buy $50 of ETH on Base"
- "Sell 100 USDC for SOL on Solana"
- "Swap 0.1 ETH for BNKR"

**Price & Market Data:**
- "What is the price of Bitcoin?"
- "Show me ETH price chart"
- "What are the top gainers today?"

**Polymarket Predictions:**
- "What are the odds on the next election?"
- "Bet $10 on the Eagles to win"
- "Show me trending prediction markets"

**DeFi Operations:**
- "What's the TVL on Aave?"
- "Show me best yields for USDC"
- "Check my portfolio balance"

## Polling Best Practices

```typescript
async function waitForCompletion(jobId: string): Promise<JobStatus> {
  const POLL_INTERVAL = 2000; // 2 seconds
  const MAX_POLLS = 120; // 4 minutes max

  for (let i = 0; i < MAX_POLLS; i++) {
    const status = await getJobStatus(jobId);

    // Terminal states
    if (['completed', 'failed', 'cancelled'].includes(status.status)) {
      return status;
    }

    // Log progress updates
    if (status.statusUpdates?.length) {
      console.log('Progress:', status.statusUpdates.at(-1)?.message);
    }

    await new Promise(r => setTimeout(r, POLL_INTERVAL));
  }

  throw new Error('Job timed out');
}
```

## Key Response Fields

When a job completes, the response includes:

- **`response`**: The text answer from Bankr
- **`transactions`**: Array of executed transactions with chain/token details
- **`richData`**: Images or charts (base64 or URL)
- **`statusUpdates`**: Progress messages during execution
- **`processingTime`**: Duration in milliseconds

For complete field documentation, see `references/job-response-schema.md`.

## Error Handling

Handle these error cases:

1. **Missing API key**: Check `BANKR_API_KEY` before making requests
2. **HTTP errors**: API returns 4xx/5xx with error text
3. **Job failures**: Check `status === 'failed'` and read `error` field
4. **Timeouts**: Implement max poll count (recommended: 4 minutes)

## Example: Complete Flow

```typescript
// 1. Submit prompt
const { jobId } = await submitPrompt("What is the price of ETH?");

// 2. Poll until complete
const result = await waitForCompletion(jobId);

// 3. Handle result
if (result.status === 'completed') {
  console.log(result.response);
  // "Ethereum (ETH) is currently trading at $3,245.67..."
} else if (result.status === 'failed') {
  console.error('Error:', result.error);
}
```

## Additional Resources

### Reference Files

- **`references/job-response-schema.md`** - Complete TypeScript interfaces and field documentation

### Example Files

- **`examples/basic-client.ts`** - Simple API client implementation
- **`examples/polling-with-updates.ts`** - Polling with status update handling
