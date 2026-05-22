---
name: google-sheets-api-coordinator
version: 1.0.0
category: coordination
tags: [google-sheets, api-coordination, rate-limiting, quota-management]
status: approved
author: CFN Team
description: Manages Google Sheets API calls with rate limiting and quota enforcement
dependencies: [jq, bash, curl]
created: 2025-11-18
updated: 2025-11-18
complexity: Medium
keywords: [api-coordination, rate-limiting, quota, batch-operations]
triggers: [api-rate-limit, quota-exceeded, batch-operations, api-calls]
performance_targets:
  execution_time_ms: 2000
  success_rate: 0.97
  quota_violations: 0
---

# Google Sheets API Coordinator Skill

## Purpose

Manages and coordinates Google Sheets API calls with automatic rate limiting, quota tracking, and batch operation support. Prevents quota exhaustion, enforces API rate limits, and provides automatic retry logic with exponential backoff.

## Problem Solved

Google Sheets API has strict quotas (300 requests/min for most users). Without coordination, multiple agents making concurrent API calls quickly exceed limits, causing cascading failures. This skill provides centralized quota management with rate limiting and batch operations enabling safe parallel execution.

## When to Use

- Before making any Google Sheets API call
- When performing batch operations (multiple cells, multiple rows)
- When quota exhaustion is possible
- During multi-agent coordination with shared quotas
- For monitoring API usage and quota health
- When implementing exponential backoff for retries

## Interface

### Primary Script: `api-call.sh`

**Required Parameters:**
- `--api-endpoint`: Google Sheets API endpoint path
- `--method`: HTTP method: GET, POST, PUT, DELETE (default: GET)
- `--spreadsheet-id`: Spreadsheet ID for quota tracking

**Optional Parameters:**
- `--batch-size`: Batch operations size (default: 50)
- `--max-retries`: Max retry attempts (default: 3)
- `--quota-limit`: Requests per minute limit (default: 300)
- `--payload`: JSON payload for POST/PUT requests
- `--timeout`: Request timeout in seconds (default: 10)
- `--api-key`: Google API key (or GOOGLE_API_KEY env var)

**Usage:**

```bash
# Single API call with rate limiting
./.claude/cfn-extras/skills/google-sheets-api-coordinator/api-call.sh \
  --api-endpoint "spreadsheets.values:get" \
  --spreadsheet-id abc123def456

# Batch operation
./.claude/cfn-extras/skills/google-sheets-api-coordinator/api-call.sh \
  --api-endpoint "spreadsheets.values:batchUpdate" \
  --spreadsheet-id abc123def456 \
  --batch-size 100 \
  --payload '{"data": [...]}'

# With custom quota limit and retries
./.claude/cfn-extras/skills/google-sheets-api-coordinator/api-call.sh \
  --api-endpoint "spreadsheets:create" \
  --spreadsheet-id abc123def456 \
  --quota-limit 60 \
  --max-retries 5
```

## Rate Limiting Strategy

### Quota Management

- **Default limit**: 300 requests/minute
- **Tracking**: Requests tracked per spreadsheet ID
- **Enforcement**: Automatic delays to respect quota
- **Backoff**: Exponential backoff (100ms, 200ms, 400ms, 800ms, 1600ms)

### Rate Limit Handling

```bash
# Request rate tracking
./.claude/cfn-extras/skills/google-sheets-api-coordinator/api-call.sh \
  --quota-limit 60  # Custom limit for restricted account
```

### Quota State Format

```json
{
  "quota_window": {
    "start_time": "2025-11-18T10:00:00Z",
    "end_time": "2025-11-18T10:01:00Z",
    "requests_made": 45,
    "quota_limit": 300,
    "available_requests": 255,
    "time_until_reset_seconds": 42
  },
  "spreadsheet_quota": {
    "spreadsheet_id": "abc123def456",
    "requests_this_minute": 12,
    "average_response_time_ms": 250
  }
}
```

## Output Format

```json
{
  "success": true,
  "confidence": 0.97,
  "api_call": {
    "endpoint": "spreadsheets.values:get",
    "method": "GET",
    "status_code": 200
  },
  "quota_usage": {
    "requests_made": 1,
    "quota_remaining": 299,
    "rate_limited": false,
    "next_request_delay_ms": 100
  },
  "response": {
    "data": {...}
  },
  "metrics": {
    "execution_time_ms": 245,
    "retries_attempted": 0
  },
  "deliverables": ["api_response"],
  "errors": []
}
```

## Error Handling

Automatic retry logic with exponential backoff:

```json
{
  "error_code": "RATE_LIMIT_EXCEEDED",
  "status_code": 429,
  "action": "backoff",
  "wait_time_ms": 2000,
  "retry_attempt": 1,
  "max_retries": 3
}
```

### Error Scenarios

1. **QUOTA_EXCEEDED** - Request would exceed quota, delayed
2. **RATE_LIMIT** - Too many requests in window, backoff applied
3. **TIMEOUT** - Request timeout, automatic retry
4. **INVALID_API_KEY** - Authentication failed, fatal
5. **MALFORMED_REQUEST** - Invalid request structure, fatal
6. **SERVER_ERROR** - 5xx errors, retry with backoff

## Integration with CFN Loop

### Loop 3 Agents (Implementation)

Coordinate API calls with automatic rate limiting:

```bash
# Make API call with automatic quota management
RESPONSE=$(./.claude/cfn-extras/skills/google-sheets-api-coordinator/api-call.sh \
  --api-endpoint "spreadsheets.values:get" \
  --spreadsheet-id "$SHEET_ID" \
  --quota-limit 300)

STATUS=$(echo "$RESPONSE" | jq -r '.success')
REMAINING=$(echo "$RESPONSE" | jq -r '.quota_usage.quota_remaining')

if [ "$STATUS" = "true" ]; then
  echo "API call successful, $REMAINING requests remaining"
else
  echo "API call failed"
fi
```

### Batch Operations

```bash
# Batch update with automatic batching
./.claude/cfn-extras/skills/google-sheets-api-coordinator/api-call.sh \
  --api-endpoint "spreadsheets.values:batchUpdate" \
  --spreadsheet-id "$SHEET_ID" \
  --batch-size 100 \
  --payload "$BATCH_DATA"
```

### Multi-Agent Coordination

All agents share quota pool:

```bash
# Agent 1 makes call (uses 1 of 300)
AGENT1=$(./.claude/cfn-extras/skills/google-sheets-api-coordinator/api-call.sh ...)

# Agent 2 makes call (automatically delayed to respect shared quota)
AGENT2=$(./.claude/cfn-extras/skills/google-sheets-api-coordinator/api-call.sh ...)

# Both complete without quota exhaustion
```

## Success Criteria

- **Pass rate**: ≥0.97 (standard mode)
- **Quota violations**: 0 (never exceed quota)
- **Rate limit accuracy**: ±50ms delay variance
- **Retry success rate**: ≥95% recover from transient errors
- **Performance**: Batch operations complete <2000ms

## Best Practices

1. **Always use coordinator** - Never call API directly
2. **Batch when possible** - Reduce total requests
3. **Share quota pool** - Don't duplicate tracking
4. **Monitor quota** - Log quota warnings
5. **Implement backoff** - Use exponential backoff for retries

## Anti-Patterns

❌ **Direct API calls** - Always use coordinator script
❌ **Hardcoded delays** - Use automatic rate limiting
❌ **No retry logic** - Implement exponential backoff
❌ **Per-agent quotas** - Use shared quota pool
❌ **Ignoring rate limits** - Always respect 429 responses

## Configuration

### Environment Variables

```bash
export GOOGLE_API_KEY="your-api-key"
export GOOGLE_SHEETS_QUOTA_LIMIT=300        # Requests per minute
export GOOGLE_SHEETS_QUOTA_WINDOW_MINUTES=1 # Quota window duration
export GOOGLE_API_TIMEOUT_SECONDS=10        # Request timeout
```

### Quota File

Rate limit state stored in: `.claude/cfn-extras/.gs-api-quota.json`

```json
{
  "quota_limit": 300,
  "window_start": "2025-11-18T10:00:00Z",
  "requests": [
    {"timestamp": "2025-11-18T10:00:15Z", "endpoint": "spreadsheets.values:get", "status": 200}
  ]
}
```

## References

- **Google Sheets API**: https://developers.google.com/sheets/api
- **Rate Limiting Guide**: https://developers.google.com/sheets/api/guides/limits
- **Quota Documentation**: `google-sheets-validation` skill
- **CFN Loop Guide**: `.claude/commands/CFN_LOOP_TASK_MODE.md`
