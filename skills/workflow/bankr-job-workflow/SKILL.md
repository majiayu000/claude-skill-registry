---
name: Bankr Agent - Job Workflow
description: This skill should be used when executing Bankr requests, submitting prompts to Bankr API, polling for job status, checking job progress, using Bankr MCP tools, or understanding the submit-poll-complete workflow pattern. Provides the core asynchronous job pattern for all Bankr API operations.
version: 1.0.0
---

# Bankr Job Workflow

Execute Bankr API operations using MCP tools with the asynchronous job pattern.

## Core Pattern: Submit-Poll-Complete

1. **Submit** - Send prompt via `bankr_agent_submit_prompt`, receive job ID
2. **Poll** - Check status via `bankr_agent_get_job_status` every 2 seconds
3. **Complete** - Report results when status is terminal

## MCP Tools

### `bankr_agent_submit_prompt`
Submit a natural language prompt to start a job.
- **Input**: Natural language request (e.g., "Buy $50 of ETH on Base")
- **Output**: Job ID for tracking

### `bankr_agent_get_job_status`
Check job status. Response includes:
- `status`: pending | processing | completed | failed | cancelled
- `response`: Text answer (when completed)
- `transactions`: Array of executed transactions
- `statusUpdates`: Progress messages during execution
- `error`: Error message (when failed)

### `bankr_agent_cancel_job`
Cancel a running job.

## Job Status States

| Status | Action |
|--------|--------|
| `pending` | Keep polling |
| `processing` | Keep polling, report statusUpdates |
| `completed` | Read response and transactions |
| `failed` | Check error field |
| `cancelled` | No further action |

## Timing

- **Poll interval**: 2 seconds
- **Typical completion**: 30 seconds to 2 minutes
- **Suggest cancellation**: After 3+ minutes for simple queries

## Output Guidelines

| Query Type | Output Format |
|------------|---------------|
| Price queries | State price clearly (e.g., "ETH is $3,245.67") |
| Trades | Confirm amounts and transaction details |
| Market analysis | Summarize key insights concisely |
| Polymarket | State odds with context |
| Balances | List holdings with USD values |
| Errors | Explain clearly, suggest alternatives |

## Status Update Handling

- Track last reported update count
- Only report NEW updates to avoid repetition
- Updates show agent progress (e.g., "Analyzing market data...")

## Error Recovery

If polling fails:
1. Retry after brief delay
2. Job continues server-side regardless
3. Can resume polling with same jobId
