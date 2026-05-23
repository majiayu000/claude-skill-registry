---
name: tzurot-observability
description: Logging and debugging patterns for Tzurot v3. Use when adding logs, debugging production, or analyzing Railway logs. Covers structured logging and correlation IDs.
lastUpdated: '2026-01-21'
---

# Tzurot v3 Observability & Operations

**Use this skill when:** Adding logging, debugging production issues, checking health, performing database/Redis operations, or adding new personalities.

## Quick Reference

```bash
# Check service health
curl https://api-gateway-development-83e8.up.railway.app/health

# View logs
railway logs --service api-gateway
railway logs --service ai-worker | grep "ERROR"

# Find request across services
railway logs | grep "requestId\":\"abc-123"
```

```typescript
// Structured logging pattern
logger.info({ requestId, userId, personalityId }, 'Processing request');
logger.error({ err: error, context: 'additional data' }, 'Operation failed');
```

## Structured Logging

### The Golden Pattern

```typescript
logger.info(
  { contextObject }, // First param: structured data
  'Human readable message' // Second param: message string
);

// ✅ GOOD
logger.info({ personalityId, model }, 'Loaded personality');
logger.error({ err: error, requestId }, 'Failed to process');

// ❌ BAD - String interpolation loses structure
logger.info(`Loaded personality ${personalityId}`);
```

### Log Levels

| Level   | When to Use                      |
| ------- | -------------------------------- |
| `error` | Errors needing attention         |
| `warn`  | Potential issues, retries        |
| `info`  | Normal operations                |
| `debug` | Debugging details                |
| `trace` | Very detailed (disabled in prod) |

### Error Logging

```typescript
// Use 'err' key for Pino's special error serialization
logger.error({ err: error, requestId, userId }, 'Request failed');
```

## Privacy Rules

**NEVER log:** API keys, tokens, passwords, email, IP, message content, DM content

**SAFE to log:** User IDs, channel IDs, counts, durations, error types

## Correlation IDs

Track requests across services with `requestId`:

```typescript
// bot-client: Generate and include in request
const requestId = randomUUID();
await fetch(url, { headers: { 'X-Request-ID': requestId } });

// All services: Include in logs
logger.info({ requestId, jobId }, 'Processing');

// Search across services
railway logs | grep "requestId\":\"abc-123"
```

## Health & Metrics

**Health endpoint:** `GET /health`

```bash
curl https://api-gateway-development-83e8.up.railway.app/health
```

**Check all services:**

```bash
railway status
railway logs --service api-gateway --tail 50
```

## Common Operations

### Adding a Personality

1. Create `personalities/name.json`:

```json
{
  "name": "PersonalityName",
  "systemPrompt": "Your description...",
  "model": "anthropic/claude-sonnet-4.5",
  "temperature": 0.8
}
```

2. Commit and push (Railway auto-deploys)

### Database Quick Commands

```bash
# Using the ops CLI (local inspection)
pnpm ops db:inspect              # Show tables, indexes, migrations
pnpm ops db:inspect --table users # Inspect specific table
pnpm ops db:check-drift          # Check for migration drift

# Railway database operations
railway run npx prisma migrate status
railway run npx prisma migrate deploy
railway run psql

# Open Prisma Studio
npx prisma studio
```

### Redis Queue Status

```bash
railway run redis-cli
LLEN bull:ai-generation:wait
LLEN bull:ai-generation:active
LLEN bull:ai-generation:failed
```

### Debugging Checklist

1. **Check logs:** `railway logs --service <name>`
2. **Check health:** `curl .../health`
3. **Check env vars:** `railway variables --service <name>`
4. **Find errors:** `railway logs | grep '"level":"error"'`
5. **Trace request:** `railway logs | grep "requestId\":\"..."`

### Common Issues

| Symptom            | Likely Cause        | Check                       |
| ------------------ | ------------------- | --------------------------- |
| Bot not responding | bot-client crashed  | Logs, DISCORD_TOKEN         |
| Slow responses     | AI worker overload  | ai-worker logs, queue depth |
| 500 errors         | Database connection | DATABASE_URL, migrations    |
| Jobs stuck         | Redis connection    | REDIS_URL, ai-worker status |

## Anti-Patterns

```typescript
// ❌ BAD - console.log
console.log('Processing');

// ✅ GOOD - structured logger
logger.info({ messageId }, 'Processing');

// ❌ BAD - logging in loops
for (const item of items) {
  logger.info({ item }, 'Processing'); // Spams logs!
}

// ✅ GOOD - log summary
logger.info({ count: items.length }, 'Processing items');

// ❌ BAD - swallowing errors
try {
  doSomething();
} catch (e) {
  /* nothing */
}

// ✅ GOOD - log and handle
try {
  doSomething();
} catch (e) {
  logger.error({ err: e }, 'Failed');
  throw e;
}
```

## Railway Log Commands

```bash
# Recent logs
railway logs --service api-gateway

# Follow in real-time
railway logs --service ai-worker --tail

# Since time
railway logs --since 1h

# Find errors
railway logs | grep '"level":"error"'

# Count error types
railway logs --since 24h | grep error | jq '.msg' | sort | uniq -c
```

## Related Skills

- **tzurot-deployment** - Railway service management, rollbacks
- **tzurot-db-vector** - Database migrations, pgvector
- **tzurot-security** - Privacy in logging
- **tzurot-async-flow** - Job correlation, BullMQ

## References

- Pino docs: https://getpino.io/
- Railway CLI: `docs/reference/RAILWAY_CLI_REFERENCE.md`
- Logger utility: `packages/common-types/src/utils/logger.ts`
