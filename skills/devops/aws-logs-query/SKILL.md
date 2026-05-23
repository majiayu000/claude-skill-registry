---
name: aws-logs-query
description: Query AWS CloudWatch logs for staging and production environments. Use for debugging errors, investigating incidents, or monitoring application behavior. PRIMARY - aws logs tail "/ecs/codel-staging" --follow --format short | grep -iE "error|exception"
---

# AWS Logs Query Skill

Query AWS CloudWatch logs for Codel staging and production environments using the AWS CLI.

## When to Use

Use this skill when you need to:
- Debug production or staging errors
- Investigate Evolution provider issues
- Monitor application behavior in real-time
- Search for specific error patterns or events
- Analyze log patterns over time windows
- Track down exceptions or failures

## Prerequisites

- AWS CLI installed (`brew install awscli` or `pip install awscli`)
- AWS credentials available (via profile, environment, or ECS task role)
- Access to `/ecs/codel-staging` and `/ecs/codel-prod` log groups

## Configuration

**🚨 CRITICAL: You MUST use `--profile codel --region us-east-2` for ALL commands!**

The Codel AWS infrastructure is in `us-east-2` with the `codel` profile.

**Local development (REQUIRED):**
```bash
# ALL commands need these flags:
--profile codel --region us-east-2
```

**ECS containers:** No configuration needed — uses the task role automatically.

## Profile and Region Handling

**MANDATORY:** When running AWS CLI commands locally:
- **ALWAYS** add `--profile codel --region us-east-2` to every command
- Without these flags, commands will fail or return empty results

```bash
# ✅ CORRECT - Always include profile and region
aws logs tail "/ecs/codel-staging" --profile codel --region us-east-2 --follow --format short

# ❌ WRONG - Will fail or return empty
aws logs tail "/ecs/codel-staging" --follow --format short
```

**All examples below include `--profile codel --region us-east-2`.** If you're in an ECS container, you can omit these flags.

## ⚡ Choosing Your Tool

**CRITICAL: Use the right tool for the job!**

### Use CloudWatch Insights for:
- ✅ **Historical searches** (> 1 hour ago)
- ✅ **Multi-day searches** (past week, past month)
- ✅ **Complex pattern matching** (multiple filters, aggregations)
- ✅ **Counting/statistics** (how many errors yesterday?)
- ✅ **ANY search beyond a few hours**

### Use `tail` for:
- ✅ **Real-time monitoring** (watching logs as they happen)
- ✅ **Recent logs** (last 15-60 minutes)
- ✅ **Simple grep patterns** (quick error checks)

### ❌ DON'T Use `tail` for:
- ❌ Multi-day searches (use CloudWatch Insights)
- ❌ Historical analysis (use CloudWatch Insights)
- ❌ Large time windows like `--since 7d` (extremely slow, will timeout)

## CloudWatch Insights (PRIMARY for Historical Searches)

For ANY search beyond the last hour, use CloudWatch Insights instead of `tail`.

### Basic Search Pattern

```bash
# Calculate timestamps
END_TIME=$(date -u +%s)
START_TIME=$((END_TIME - 604800))  # 7 days in seconds

# Start query
QUERY_ID=$(aws logs start-query \
  --profile codel --region us-east-2 \
  --log-group-name "/ecs/codel-prod" \
  --start-time "$START_TIME" \
  --end-time "$END_TIME" \
  --query-string 'fields @timestamp, @message | filter @message like /your_pattern_here/ | sort @timestamp desc | limit 100' \
  --output text --query 'queryId')

# Wait for results
sleep 5

# Get results
aws logs get-query-results --profile codel --region us-east-2 --query-id "$QUERY_ID" --output json
```

### Real-World Example: Search Past Week for Specific Error

```bash
# Search for Linq validation errors in the past 7 days
END_TIME=$(date -u +%s)
START_TIME=$((END_TIME - 604800))

QUERY='fields @timestamp, @message
| filter @message like /bool_type.*is_me.*Input should be a valid boolean/
| sort @timestamp desc
| limit 100'

QUERY_ID=$(aws logs start-query \
  --profile codel --region us-east-2 \
  --log-group-name "/ecs/codel-prod" \
  --start-time "$START_TIME" \
  --end-time "$END_TIME" \
  --query-string "$QUERY" \
  --output text --query 'queryId')

sleep 5
aws logs get-query-results --profile codel --region us-east-2 --query-id "$QUERY_ID" --output json
```

### Common CloudWatch Insights Queries

```bash
# Count errors by type in past 24 hours
QUERY='fields @message
| filter @message like /error|Error|ERROR/
| stats count() by @message
| sort count desc
| limit 20'

# Find all Pydantic validation errors
QUERY='fields @timestamp, @message
| filter @message like /ValidationError/
| sort @timestamp desc
| limit 50'

# Search for specific phone number in logs
QUERY='fields @timestamp, @message
| filter @message like /\+16508997366/
| sort @timestamp desc
| limit 100'

# Get errors from specific time range
QUERY='fields @timestamp, @message
| filter @message like /error/
  and @timestamp >= "2025-11-07T00:00:00"
  and @timestamp <= "2025-11-08T00:00:00"
| sort @timestamp desc'
```

### Time Range Calculations

```bash
# Common time windows
END_TIME=$(date -u +%s)
HOUR_AGO=$((END_TIME - 3600))
DAY_AGO=$((END_TIME - 86400))
WEEK_AGO=$((END_TIME - 604800))
MONTH_AGO=$((END_TIME - 2592000))

# Use in queries
--start-time "$WEEK_AGO" --end-time "$END_TIME"
```

## Tail for Recent Logs (< 1 hour)

Use `tail` for real-time monitoring and quick checks of recent logs.

### Watch Logs in Real-Time

```bash
# Watch staging logs as they happen
aws logs tail "/ecs/codel-staging" --profile codel --region us-east-2 --follow --format short

# Watch production logs
aws logs tail "/ecs/codel-prod" --profile codel --region us-east-2 --follow --format short
```

### Quick Recent Searches

```bash
# Last 15 minutes only
aws logs tail "/ecs/codel-staging" --profile codel --region us-east-2 --since 15m --format short

# Find errors in last 30 min
aws logs tail "/ecs/codel-staging" --profile codel --region us-east-2 --since 30m --format short | grep -iE "error|exception|failed"

# Get full error context (10 lines before/after)
aws logs tail "/ecs/codel-staging" --profile codel --region us-east-2 --since 15m --format short | grep -iE -B 10 -A 10 "ValidationError"
```

## Available Log Groups

### Main Application Logs
**Staging:** `/ecs/codel-staging`
**Production:** `/ecs/codel-prod`
- **Services**: api, worker, voice, admin-api
- **Use for**: General application debugging, message processing, webhooks

### Evolution API Logs (WhatsApp Provider)
**Staging:** `/ecs/codel-staging-evolution`
**Production:** `/ecs/codel-prod-evolution`
- **Use for**: Evolution API issues, WhatsApp connectivity, instance management
- **When to use**: Evolution validation errors, disconnection issues, webhook problems

### Langfuse Logs (LLM Observability)
**Web:**
- Staging: `/ecs/codel-staging-langfuse-web`
- Production: `/ecs/codel-prod-langfuse-web`

**Worker:**
- Staging: `/ecs/codel-staging-langfuse-worker`
- Production: `/ecs/codel-prod-langfuse-worker`

**ClickHouse:**
- Staging: `/ecs/codel-staging-langfuse-clickhouse`
- Production: `/ecs/codel-prod-langfuse-clickhouse`

### Metabase Logs (Analytics)
**Staging:** `/ecs/codel-staging-metabase`
**Production:** `/ecs/codel-prod-metabase`

### Quick Reference
```bash
# Main application (default for most debugging)
STAGING_MAIN="/ecs/codel-staging"
PROD_MAIN="/ecs/codel-prod"

# Evolution API (WhatsApp provider)
STAGING_EVOLUTION="/ecs/codel-staging-evolution"
PROD_EVOLUTION="/ecs/codel-prod-evolution"

# Langfuse
STAGING_LANGFUSE_WEB="/ecs/codel-staging-langfuse-web"
PROD_LANGFUSE_WEB="/ecs/codel-prod-langfuse-web"

# Metabase
STAGING_METABASE="/ecs/codel-staging-metabase"
PROD_METABASE="/ecs/codel-prod-metabase"
```

## Common Use Cases

### Debug Evolution Errors

**Main app logs** (where Evolution webhooks are processed):
```bash
# Find recent Evolution validation errors in main app
aws logs tail "/ecs/codel-staging" --since 1h --format short | grep -i "evolution" | grep -i "error"

# Get full traceback for Evolution issues
aws logs tail "/ecs/codel-staging" --since 30m --format short | grep -B 20 -A 5 "EvolutionInstance"

# Watch Evolution webhooks being processed
aws logs tail "/ecs/codel-staging" --follow --format short | grep -i "evolution.*webhook"
```

**Evolution API logs** (Evolution service itself):
```bash
# Watch Evolution API directly
aws logs tail "/ecs/codel-staging-evolution" --follow --format short

# Find Evolution API errors
aws logs tail "/ecs/codel-prod-evolution" --since 1h --format short | grep -iE "error|exception|fail"

# Check Evolution instance disconnections
aws logs tail "/ecs/codel-prod-evolution" --since 30m --format short | grep -i "disconnect"

# Monitor Evolution health checks
aws logs tail "/ecs/codel-staging-evolution" --since 15m --format short | grep -i "health"
```

### Find Specific Error Types
```bash
# Pydantic validation errors
aws logs tail "/ecs/codel-staging" --since 1h --format short | grep -i "ValidationError"

# Database errors
aws logs tail "/ecs/codel-staging" --since 1h --format short | grep -iE "sqlalchemy|database|postgres"

# OpenAI/LLM errors
aws logs tail "/ecs/codel-staging" --since 1h --format short | grep -iE "openai|anthropic|llm"

# Worker job failures
aws logs tail "/ecs/codel-staging" --since 1h --format short | grep -iE "job.*failed|exception raised while executing"
```

### Monitor Specific Services
```bash
# API logs only (look for api/ prefix in log stream)
aws logs tail "/ecs/codel-staging" --follow --format short | grep "api/api/"

# Worker logs only
aws logs tail "/ecs/codel-staging" --follow --format short | grep "worker/worker/"

# Voice service logs
aws logs tail "/ecs/codel-staging" --follow --format short | grep "voice/voice/"
```


## Time Windows

The `--since` flag accepts various formats:
- `5m` - Last 5 minutes
- `15m` - Last 15 minutes
- `1h` - Last hour
- `6h` - Last 6 hours
- `1d` - Last day
- `2h30m` - Last 2 hours 30 minutes

## Log Stream Patterns

Each ECS task creates its own log stream with this pattern:
```
{service}/{service}/{task-id}

Examples:
api/api/4ffc8e0fd7c54c76a00873409a1a01c4
worker/worker/e9bdd10c0cd3424283c16ffa24fca756
voice/voice/7c8088a63fbc442091d7ebbb04235523
admin-api/admin-api/348f846767d34f90913d145b9533eda8
```

### List Active Log Streams
```bash
# See which tasks are currently logging
aws logs describe-log-streams \
  --log-group-name "/ecs/codel-staging" \
   \
  --order-by LastEventTime \
  --descending \
  --max-items 10
```

## Debugging Workflows

### When Tests Fail
```bash
# 1. Check recent errors
aws logs tail "/ecs/codel-staging" --since 15m --format short | grep -iE "error|exception|failed"

# 2. Look for specific test failures
aws logs tail "/ecs/codel-staging" --since 30m --format short | grep -i "test"

# 3. Check worker job processing
aws logs tail "/ecs/codel-staging" --since 15m --format short | grep -i "worker"
```

### When Evolution Errors Occur
```bash
# 1. Find the error message
aws logs tail "/ecs/codel-staging" --since 1h --format short | grep -i "evolution.*error"

# 2. Get full context (20 lines before/after)
aws logs tail "/ecs/codel-staging" --since 1h --format short | grep -iE -B 20 -A 10 "EvolutionInstance|evolution.*validation"

# 3. Check webhook processing
aws logs tail "/ecs/codel-staging" --since 1h --format short | grep -i "evolution.*webhook"
```

### When Messages Aren't Sending
```bash
# 1. Check message sending errors
aws logs tail "/ecs/codel-staging" --since 30m --format short | grep -iE "send.*message|messaging"

# 2. Look for provider errors
aws logs tail "/ecs/codel-staging" --since 30m --format short | grep -iE "evolution|linq|sendblue"

# 3. Check for API errors
aws logs tail "/ecs/codel-staging" --since 30m --format short | grep -E "(400|401|403|404|500|502|503)"
```

## Common Error Patterns

| Error Pattern | What It Means | How to Search |
|--------------|---------------|---------------|
| `ValidationError: 2 validation errors for EvolutionInstance` | Evolution API response doesn't match Pydantic model | `grep -i "ValidationError.*Evolution"` |
| `disconnectionReasonCode.*should be a valid string` | Evolution API returned int instead of string | `grep "disconnectionReasonCode"` |
| `failed to send, dropping.*traces` | Datadog agent not reachable (not critical) | `grep "failed to send.*traces"` |
| `Database session error` | SQLAlchemy session issue, usually followed by real error | `grep -B 5 -A 10 "Database session error"` |
| `Job.*exception raised while executing` | RQ worker job failed | `grep "exception raised while executing"` |

## Output Formats

### Short Format (Recommended)
```bash
--format short
# Output: timestamp message
# Example: 2025-11-14T01:34:06 [error] Database session error
```

### Detailed Format
```bash
--format detailed
# Output: timestamp log-stream message
# More verbose, useful for debugging specific tasks
```

## Filtering and Post-Processing

### Save Logs for Analysis
```bash
# Save last hour of logs to file
aws logs tail "/ecs/codel-staging" --since 1h --format short > staging-logs.txt

# Save only errors
aws logs tail "/ecs/codel-staging" --since 1h --format short | grep -iE "error|exception" > staging-errors.txt
```

### Count Error Occurrences
```bash
# Count how many validation errors
aws logs tail "/ecs/codel-staging" --since 1h --format short | grep -c "ValidationError"

# Count errors by type
aws logs tail "/ecs/codel-staging" --since 1h --format short | grep -iE "error|exception" | sort | uniq -c | sort -rn
```

### Follow Specific Flow
```bash
# Track a specific webhook through the system
aws logs tail "/ecs/codel-staging" --follow --format short | grep "webhook_id_here"

# Follow a user's messages
aws logs tail "/ecs/codel-staging" --follow --format short | grep "person_id.*123"
```

## Integration with Claude Code

When using this skill, **choose the right tool based on time range**:

### For Historical Searches (> 1 hour ago)
1. **Use CloudWatch Insights** (not tail!)
2. **Calculate time range** using epoch timestamps
3. **Build query** with proper filters
4. **Report findings** with timestamps and counts

**Example workflow for past week search:**
```bash
# 1. Calculate time range
END_TIME=$(date -u +%s)
START_TIME=$((END_TIME - 604800))  # 7 days

# 2. Build and run query (note: profile and region REQUIRED)
QUERY='fields @timestamp, @message | filter @message like /ValidationError/ | sort @timestamp desc | limit 100'
QUERY_ID=$(aws logs start-query --profile codel --region us-east-2 \
  --log-group-name "/ecs/codel-prod" \
  --start-time "$START_TIME" --end-time "$END_TIME" --query-string "$QUERY" \
  --output text --query 'queryId')

# 3. Wait and get results
sleep 5
aws logs get-query-results --profile codel --region us-east-2 --query-id "$QUERY_ID" --output json

# 4. Report: "Found 47 validation errors in the past 7 days, first occurred on Nov 7..."
```

### For Recent Logs (< 1 hour ago)
1. **Use tail** for quick checks
2. **Pipe to grep** for pattern matching
3. **Use -B/-A** for context
4. **Report findings** concisely

**Example workflow for recent errors:**
```bash
# 1. Check last 15 minutes
aws logs tail "/ecs/codel-staging" --since 15m --format short | grep -i "error"

# 2. Get full context
aws logs tail "/ecs/codel-staging" --since 30m --format short | grep -B 20 -A 5 "EvolutionInstance"

# 3. Report: "Found 2 Evolution errors in the last 15 minutes..."
```

## Troubleshooting

### Query returns empty results (0 bytes scanned)
**Most common cause:** Missing `--profile codel --region us-east-2`
```bash
# ❌ WRONG - returns empty results
aws logs start-query --log-group-name "/ecs/codel-prod" ...

# ✅ CORRECT - returns actual data
aws logs start-query --profile codel --region us-east-2 --log-group-name "/ecs/codel-prod" ...
```

### "The specified log group does not exist"
- Verify log group name (should be `/ecs/codel-staging` or `/ecs/codel-prod`)
- **Check you're using `--profile codel --region us-east-2`**
- Confirm AWS credentials are configured

### "Invalid --since value"
- Use format like `15m`, `1h`, `30m`
- Don't use spaces: `15 m` ❌ `15m` ✅

### No output when tailing
- Try expanding time window: `--since 1h` or `--since 6h`
- Check log streams exist: `aws logs describe-log-streams --log-group-name "/ecs/codel-staging" --max-items 5`
- Verify services are running and generating logs

### Query times out
- Reduce time window (try `--since 1h` instead of `--since 1d`)
- Use more specific filters
- Consider CloudWatch Insights for complex queries

## Quick Reference Card

```bash
# 🚨 ALWAYS include: --profile codel --region us-east-2

# Watch logs live
aws logs tail "/ecs/codel-staging" --profile codel --region us-east-2 --follow --format short

# Last 15 minutes
aws logs tail "/ecs/codel-staging" --profile codel --region us-east-2 --since 15m --format short

# Find errors
aws logs tail "/ecs/codel-staging" --profile codel --region us-east-2 --since 30m --format short | grep -iE "error|exception"

# Evolution issues
aws logs tail "/ecs/codel-staging" --profile codel --region us-east-2 --since 1h --format short | grep -i "evolution" | grep -i "error"

# Get context around errors
aws logs tail "/ecs/codel-staging" --profile codel --region us-east-2 --since 30m --format short | grep -B 20 -A 10 "ValidationError"

# Production (same commands, different log group)
aws logs tail "/ecs/codel-prod" --profile codel --region us-east-2 --since 15m --format short
```

## Best Practices

✅ **Do:**
- Start with staging when debugging
- Use `--since` to limit time window (faster queries)
- Pipe to `grep` for pattern matching
- Use `-B` and `-A` for context around matches
- Save interesting logs to files for analysis

❌ **Don't:**
- Query production unless investigating live issues
- Use very large time windows (> 6h) without filters
- Run queries without ``
- Forget to use `--format short` for readable output
