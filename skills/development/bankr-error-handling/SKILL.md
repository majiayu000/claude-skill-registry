---
name: Bankr Agent - Error Handling
description: This skill should be used when encountering authentication errors, API key errors, 401 errors, "invalid API key", "BANKR_API_KEY not set", job failures, or any Bankr API errors. Provides setup instructions and troubleshooting guidance for resolving Bankr configuration issues.
version: 1.0.0
---

# Bankr Error Handling

Resolve Bankr API errors and authentication issues.

## Authentication Errors (401)

### Symptoms
- HTTP 401 status code
- "Invalid API key" or "Unauthorized" message

### Resolution

Present these setup instructions to the user:

**Step 1: Create an API Key**
```
Visit https://bankr.bot/api to create a new API key
```

**Step 2: Set Environment Variable**
```bash
# Add to shell profile (~/.zshrc or ~/.bashrc)
export BANKR_API_KEY=bk_your_api_key_here
```

**Step 3: Restart Claude Code**
```
Close and reopen the terminal/Claude Code session
```

**Important**: Do NOT retry when authentication fails. User must fix API key first.

## Common Job Failures

| Error | Cause | Resolution |
|-------|-------|------------|
| Insufficient balance | Not enough tokens | Check balance, reduce amount |
| Token not found | Invalid symbol/address | Verify token exists on chain |
| Slippage exceeded | Price moved too much | Retry or try smaller amount |
| Transaction reverted | On-chain failure | Check transaction details |
| Rate limit exceeded | Too many requests | Wait and retry |

## HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 400 | Bad request | Check prompt format |
| 401 | Unauthorized | Fix API key (see above) |
| 402 | Payment required | Ensure wallet has BNKR on Base |
| 429 | Rate limited | Wait and retry |
| 500 | Server error | Retry after delay |

## Troubleshooting Checklist

1. **API Key**: Set, starts with `bk_`, Claude Code restarted after setting
2. **Network**: Internet working, api.bankr.bot reachable
3. **For Trading**: Wallet has sufficient balance, token exists on chain

## Reporting Errors to Users

1. State what went wrong simply
2. Provide specific fix steps
3. Avoid technical jargon
4. Suggest alternatives

**Example**:
```
Your Bankr API key is not configured. To set it up:
1. Visit https://bankr.bot/api to create an API key
2. Set BANKR_API_KEY in your environment
3. Restart Claude Code
```
