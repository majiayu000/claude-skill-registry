---
name: cloudflare-cron-triggers
description: Cloudflare Cron Triggers for scheduled Workers execution. Use for periodic tasks, scheduled jobs, or encountering handler not found, invalid cron expression, timezone errors.

  Keywords: cloudflare cron, cron triggers, scheduled workers, scheduled handler, periodic tasks,
  background jobs, scheduled tasks, cron expression, wrangler crons, scheduled event, green compute,
  workflow triggers, maintenance tasks, scheduled() handler, ScheduledController, UTC timezone
license: MIT
---

# Cloudflare Cron Triggers

**Status**: Production Ready ✅
**Last Updated**: 2025-11-25
**Dependencies**: cloudflare-worker-base (for Worker setup)
**Latest Versions**: wrangler@4.50.0, @cloudflare/workers-types@4.20251125.0

---

## Quick Start (5 Minutes)

### 1. Add Scheduled Handler to Your Worker

**src/index.ts:**

```typescript
export default {
  async scheduled(
    controller: ScheduledController,
    env: Env,
    ctx: ExecutionContext
  ): Promise<void> {
    console.log('Cron job executed at:', new Date(controller.scheduledTime));
    console.log('Triggered by cron:', controller.cron);

    // Your scheduled task logic here
    await doPeriodicTask(env);
  },
};
```

**Why this matters:**
- Handler must be named exactly `scheduled` (not `scheduledHandler` or `onScheduled`)
- Must be exported in default export object
- Must use ES modules format (not Service Worker format)

### 2. Configure Cron Trigger in Wrangler

**wrangler.jsonc:**

```jsonc
{
  "name": "my-scheduled-worker",
  "main": "src/index.ts",
  "compatibility_date": "2025-10-23",
  "triggers": {
    "crons": [
      "0 * * * *"  // Every hour at minute 0
    ]
  }
}
```

**CRITICAL:**
- Cron expressions use 5 fields: `minute hour day-of-month month day-of-week`
- All times are **UTC only** (no timezone conversion)
- Changes take **up to 15 minutes** to propagate globally

### 3. Test Locally

```bash
# Enable scheduled testing
bunx wrangler dev --test-scheduled

# In another terminal, trigger the scheduled handler
curl "http://localhost:8787/__scheduled?cron=0+*+*+*+*"

# View output in wrangler dev terminal
```

**Testing tips:**
- `/__scheduled` endpoint is only available with `--test-scheduled` flag
- Can pass any cron expression in query parameter
- Python Workers use `/cdn-cgi/handler/scheduled` instead

### 4. Deploy

```bash
npm run deploy
# or
bunx wrangler deploy
```

**After deployment:**
- Changes may take up to 15 minutes to propagate
- Check dashboard: Workers & Pages > [Your Worker] > **Cron Triggers**
- View past executions in **Logs** tab

---

## When to Load References

**Load immediately when user mentions**:

- `cron-expressions-reference.md` → "cron syntax", "schedule format", "expression", "minute hour day", "every X minutes"
- `common-patterns.md` → "examples", "use cases", "patterns", "real-world", "database cleanup", "report generation", "how to"
- `integration-patterns.md` → "implement", "Hono", "multiple triggers", "bindings", "workflows", "error handling"
- `wrangler-config.md` → "configuration", "wrangler.jsonc", "multiple crons", "environment-specific", "dev staging production"
- `testing-guide.md` → "test", "local development", "__scheduled", "unit test", "curl", "debugging"

**Load proactively when**:
- Building new scheduled task → Load `integration-patterns.md`
- Configuring wrangler.jsonc → Load `wrangler-config.md`
- Debugging cron expression → Load `cron-expressions-reference.md`
- Testing locally → Load `testing-guide.md`
- Looking for examples → Load `common-patterns.md`

---

## Cron Expression Syntax

### Five-Field Format

```
* * * * *
│ │ │ │ │
│ │ │ │ └─── Day of Week (0-6, Sunday=0)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of Month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

### Special Characters

| Character | Meaning | Example |
|-----------|---------|---------|
| `*` | Every | `* * * * *` = every minute |
| `,` | List | `0,30 * * * *` = every hour at :00 and :30 |
| `-` | Range | `0 9-17 * * *` = every hour from 9am-5pm |
| `/` | Step | `*/15 * * * *` = every 15 minutes |

### Common Patterns

```bash
# Every minute
* * * * *

# Every 5 minutes
*/5 * * * *

# Every 15 minutes
*/15 * * * *

# Every hour at minute 0
0 * * * *

# Every hour at minute 30
30 * * * *

# Every 6 hours
0 */6 * * *

# Every day at midnight (00:00 UTC)
0 0 * * *

# Every day at noon (12:00 UTC)
0 12 * * *

# Every day at 3:30am UTC
30 3 * * *

# Every Monday at 9am UTC
0 9 * * 1

# Every weekday at 9am UTC
0 9 * * 1-5

# Every Sunday at midnight UTC
0 0 * * 0

# First day of every month at midnight UTC
0 0 1 * *

# Twice a day (6am and 6pm UTC)
0 6,18 * * *

# Every 30 minutes during business hours (9am-5pm UTC, weekdays)
*/30 9-17 * * 1-5
```

**CRITICAL: UTC Timezone Only**
- All cron triggers execute on **UTC time**
- No timezone conversion available
- Convert your local time to UTC manually
- Example: 9am PST = 5pm UTC (next day during DST)

---

## ScheduledController Interface

```typescript
interface ScheduledController {
  readonly cron: string;           // The cron expression that triggered this execution
  readonly type: string;           // Always "scheduled"
  readonly scheduledTime: number;  // Unix timestamp (ms) when scheduled
}
```

### Properties

#### `controller.cron` (string)

The cron expression that triggered this execution.

```typescript
export default {
  async scheduled(controller: ScheduledController, env: Env): Promise<void> {
    console.log(`Triggered by: ${controller.cron}`);
    // Output: "Triggered by: 0 * * * *"
  },
};
```

**Use case:** Differentiate between multiple cron schedules (see Multiple Cron Triggers pattern).

#### `controller.type` (string)

Always returns `"scheduled"` for cron-triggered executions.

```typescript
if (controller.type === 'scheduled') {
  // This is a cron-triggered execution
}
```

#### `controller.scheduledTime` (number)

Unix timestamp (milliseconds since epoch) when this execution was scheduled to run.

```typescript
export default {
  async scheduled(controller: ScheduledController): Promise<void> {
    const scheduledDate = new Date(controller.scheduledTime);
    console.log(`Scheduled for: ${scheduledDate.toISOString()}`);
    // Output: "Scheduled for: 2025-10-23T15:00:00.000Z"
  },
};
```

**Note:** This is the **scheduled** time, not the actual execution time. Due to system load, actual execution may be slightly delayed (usually <1 second).

---

## Execution Context

```typescript
export default {
  async scheduled(
    controller: ScheduledController,
    env: Env,
    ctx: ExecutionContext  // ← Execution context
  ): Promise<void> {
    // Use ctx.waitUntil() for async operations that should complete
    ctx.waitUntil(logToAnalytics(env));
  },
};
```

### `ctx.waitUntil(promise: Promise<any>)`

Extends the execution context to wait for async operations to complete after the handler returns.

**Use cases:**
- Logging to external services
- Analytics tracking
- Cleanup operations
- Non-critical background tasks

```typescript
export default {
  async scheduled(controller: ScheduledController, env: Env, ctx: ExecutionContext): Promise<void> {
    // Critical task - must complete before handler exits
    await processData(env);

    // Non-critical tasks - can complete in background
    ctx.waitUntil(sendMetrics(env));
    ctx.waitUntil(cleanupOldData(env));
    ctx.waitUntil(notifySlack({ message: 'Cron completed' }));
  },
};
```

**Important:** First `waitUntil()` that fails will be reported as the status in dashboard logs.

---

## Integration Patterns

**6 production-ready cron patterns**:

1. **Standalone Worker with Cron** - Single scheduled function for background tasks (database cleanup, report generation)
2. **Hono + Cron Combination** - HTTP endpoints + scheduled tasks in one Worker, sharing bindings and reducing costs
3. **Multiple Cron Triggers** - Different schedules for different tasks using `controller.cron` to route execution
4. **Accessing Bindings** - Use D1, KV, R2, AI, Vectorize, Queues, Workflows, Durable Objects in scheduled functions
5. **Integrating with Workflows** - Trigger complex, long-running multi-step workflows on schedule
6. **Error Handling Best Practices** - Comprehensive error handling with retry logic, alerting (Slack/email), failure logging, and monitoring

**Load `references/integration-patterns.md` for complete implementations with code examples, configuration details, and best practices.**

---

## Wrangler Configuration

Add cron triggers to `wrangler.jsonc` in the `triggers.crons` array. Each trigger requires a `cron` expression. Supports multiple crons (Free: 3 max, Paid: higher limits) and environment-specific configurations for dev/staging/production deployments.

**Load `references/wrangler-config.md` for complete configuration examples including multiple triggers, environment-specific schedules, timezone handling, and removal procedures.**

---

## Testing & Development

Test scheduled functions locally using the `/__scheduled` endpoint by running `bunx wrangler dev --test-scheduled`, then triggering handlers with `curl "http://localhost:8787/__scheduled?cron=0+*+*+*+*"` (use `+` instead of spaces in cron expressions).

**Load `references/testing-guide.md` for complete testing strategies, local development setup, unit testing examples, integration testing patterns, and production monitoring techniques.**

---

## Green Compute

Run cron triggers only in data centers powered by renewable energy.

### Enable Green Compute

**Via Dashboard:**

1. Go to [Workers & Pages](https://dash.cloudflare.com/?to=/:account/workers-and-pages)
2. In **Account details** section, find **Compute Setting**
3. Click **Change**
4. Select **Green Compute**
5. Click **Confirm**

**Applies to:**
- All cron triggers in your account
- Reduces carbon footprint
- No additional cost
- May introduce slight delays in some regions

**How it works:**
- Cloudflare routes cron executions to green-powered data centers
- Uses renewable energy: wind, solar, hydroelectric
- Verified through Power Purchase Agreements (PPAs) and Renewable Energy Credits (RECs)

---

## Known Issues Prevention

This skill prevents **6** documented issues:

### Issue #1: Cron Changes Not Propagating

**Error:** Cron triggers updated in wrangler.jsonc but not executing

**Source:** [Cloudflare Docs - Cron Triggers](https://developers.cloudflare.com/workers/configuration/cron-triggers/)

**Why It Happens:**
- Changes to cron triggers take up to **15 minutes** to propagate globally
- Cloudflare network needs time to update edge nodes
- No instant propagation like regular deploys

**Prevention:**
- Wait 15 minutes after deploy before expecting execution
- Check dashboard: Workers & Pages > [Worker] > Cron Triggers
- Use `wrangler triggers deploy` for trigger-only changes

```bash
# If you only changed triggers (not code), use:
bunx wrangler triggers deploy

# Wait 15 minutes, then verify in dashboard
```

---

### Issue #2: Handler Does Not Export

**Error:** `Handler does not export a 'scheduled' method`

**Source:** Common deployment error

**Why It Happens:**
- Handler not named exactly `scheduled`
- Handler not exported in default export object
- Using Service Worker format instead of ES modules

**Prevention:**

```typescript
// ❌ Wrong: Incorrect handler name
export default {
  async scheduledHandler(controller, env, ctx) { }
};

// ❌ Wrong: Not in default export
export async function scheduled(controller, env, ctx) { }

// ✅ Correct: Named 'scheduled' in default export
export default {
  async scheduled(controller, env, ctx) { }
};
```

---

### Issue #3: UTC Timezone Confusion

**Error:** Cron runs at wrong time

**Source:** User expectation vs. reality

**Why It Happens:**
- All cron triggers run on **UTC time only**
- No timezone conversion available
- Users expect local timezone

**Prevention:**

Convert your local time to UTC manually:

```typescript
// Want to run at 9am PST (UTC-8)?
// 9am PST = 5pm UTC (17:00)
{
  "triggers": {
    "crons": ["0 17 * * *"]  // 9am PST = 5pm UTC
  }
}

// Want to run at 6pm EST (UTC-5)?
// 6pm EST = 11pm UTC (23:00)
{
  "triggers": {
    "crons": ["0 23 * * *"]  // 6pm EST = 11pm UTC
  }
}

// Remember: DST changes affect conversion!
// PST is UTC-8, PDT is UTC-7
```

**Tools:**
- [Time Zone Converter](https://www.timeanddate.com/worldclock/converter.html)
- [Cron Expression Generator](https://crontab.guru/)

---

### Issue #4: Invalid Cron Expression

**Error:** Cron doesn't execute, no error shown

**Source:** Silent validation failure

**Why It Happens:**
- Invalid cron syntax silently fails
- Validation happens at deploy, but may not be obvious
- Common mistakes: wrong field order, invalid ranges

**Prevention:**

```bash
# ❌ Wrong: Too many fields (6 fields instead of 5)
"crons": ["0 0 * * * *"]  # Has seconds field - not supported

# ❌ Wrong: Invalid minute range
"crons": ["65 * * * *"]  # Minute must be 0-59

# ❌ Wrong: Invalid day of week
"crons": ["0 0 * * 7"]  # Day of week is 0-6 (use 0 for Sunday)

# ✅ Correct: 5 fields, valid ranges
"crons": ["0 0 * * 0"]  # Sunday at midnight UTC
```

**Validation:**
- Use [Crontab Guru](https://crontab.guru/) to validate expressions
- Check wrangler deploy output for errors
- Test locally with `--test-scheduled`

---

### Issue #5: Missing ES Modules Format

**Error:** `Worker must use ES modules format`

**Source:** Legacy Service Worker format

**Why It Happens:**
- Scheduled handler requires ES modules format
- Old Service Worker format not supported
- Mixed format in codebase

**Prevention:**

```typescript
// ❌ Wrong: Service Worker format
addEventListener('scheduled', (event) => {
  event.waitUntil(handleScheduled(event));
});

// ✅ Correct: ES modules format
export default {
  async scheduled(controller, env, ctx) {
    await handleScheduled(controller, env, ctx);
  },
};
```

---

### Issue #6: CPU Time Limits Exceeded

**Error:** `CPU time limit exceeded`

**Source:** Long-running scheduled tasks

**Why It Happens:**
- Default CPU limit: 30 seconds
- Long-running tasks exceed limit
- No automatic timeout extension

**Prevention:**

**Option 1: Increase CPU limit in wrangler.jsonc**

```jsonc
{
  "limits": {
    "cpu_ms": 300000  // 5 minutes (max for Standard plan)
  }
}
```

**Option 2: Use Workflows for long-running tasks**

```typescript
// Instead of long task in cron:
export default {
  async scheduled(controller, env, ctx) {
    // Trigger Workflow that can run for hours
    await env.MY_WORKFLOW.create({
      params: { task: 'long-running-job' },
    });
  },
};
```

**Option 3: Break into smaller chunks**

```typescript
export default {
  async scheduled(controller, env, ctx) {
    // Process in batches
    const batch = await getNextBatch(env.DB);

    for (const item of batch) {
      await processItem(item);
    }

    // If more work, send to Queue for next batch
    const hasMore = await hasMoreWork(env.DB);
    if (hasMore) {
      await env.MY_QUEUE.send({ type: 'continue-processing' });
    }
  },
};
```

---

## Always Do ✅

1. **Use exact handler name** - Must be `scheduled`, not `scheduledHandler` or variants
2. **Use ES modules format** - Export in default object, not addEventListener
3. **Convert to UTC** - All cron times are UTC, convert from local timezone
4. **Wait 15 minutes** - Cron changes take up to 15 min to propagate
5. **Test locally first** - Use `wrangler dev --test-scheduled`
6. **Validate cron syntax** - Use [Crontab Guru](https://crontab.guru/)
7. **Handle errors gracefully** - Log, alert, and optionally re-throw
8. **Use ctx.waitUntil()** - For non-critical async operations
9. **Consider Workflows** - For tasks that need >30 seconds CPU time
10. **Monitor executions** - Check dashboard logs regularly

---

## Never Do ❌

1. **Never assume local timezone** - All crons run on UTC
2. **Never use 6-field cron expressions** - Cloudflare uses 5-field format (no seconds)
3. **Never rely on instant propagation** - Changes take up to 15 minutes
4. **Never use Service Worker format** - Must use ES modules format
5. **Never forget error handling** - Uncaught errors fail silently
6. **Never run CPU-intensive tasks without limit increase** - Default 30s limit
7. **Never use day-of-week 7** - Use 0 for Sunday (0-6 range only)
8. **Never deploy without testing** - Always test with `--test-scheduled` first
9. **Never ignore execution logs** - Dashboard shows past failures
10. **Never hardcode schedules for testing** - Use environment-specific configs

---

## Common Use Cases

**Load `references/common-patterns.md` for 10 real-world cron patterns including database cleanup, API data collection, daily reports generation, cache warming, monitoring & health checks, data synchronization, backup automation, sitemap generation, webhook processing, and scheduled notifications.**

---

## TypeScript Types

```typescript
// Scheduled event controller
interface ScheduledController {
  readonly cron: string;
  readonly type: string;
  readonly scheduledTime: number;
}

// Execution context
interface ExecutionContext {
  waitUntil(promise: Promise<any>): void;
  passThroughOnException(): void;
}

// Scheduled handler
export default {
  async scheduled(
    controller: ScheduledController,
    env: Env,
    ctx: ExecutionContext
  ): Promise<void>;
}
```

---

## Limits & Pricing

### Limits

| Feature | Free Plan | Paid Plan |
|---------|-----------|-----------|
| **Cron triggers per Worker** | 3 | Higher (check docs) |
| **CPU time per execution** | 10 ms (avg) | 30 seconds (default), 5 min (max) |
| **Wall clock time** | 30 seconds | 15 minutes |
| **Memory** | 128 MB | 128 MB |

### Pricing

Cron triggers use **Standard Workers pricing**:

- **Workers Paid Plan**: $5/month required
- **Requests**: $0.30 per million requests (after 10M free)
- **CPU Time**: $0.02 per million CPU-ms (after 30M free)

**Cron execution = 1 request**

**Example:**
- Cron runs every hour (24 times/day)
- 30 days × 24 executions = 720 executions/month
- Average 50ms CPU time per execution

**Cost:**
- Requests: 720 (well under 10M free)
- CPU time: 720 × 50ms = 36,000ms (under 30M free)
- **Total: $5/month (just subscription)**

**High frequency example:**
- Cron runs every minute (1440 times/day)
- 30 days × 1440 = 43,200 executions/month
- Still under free tier limits
- **Total: $5/month**

---

## Troubleshooting

### Issue: Cron not executing

**Possible causes:**
1. Changes not propagated yet (wait 15 minutes)
2. Invalid cron expression
3. Handler not exported correctly
4. Worker not deployed

**Solution:**

```bash
# Re-deploy
bunx wrangler deploy

# Wait 15 minutes

# Check dashboard
# Workers & Pages > [Worker] > Cron Triggers

# Check logs
# Workers & Pages > [Worker] > Logs > Real-time Logs
```

---

### Issue: Handler executes but fails

**Possible causes:**
1. Uncaught error in handler
2. CPU time limit exceeded
3. Missing environment bindings
4. Network timeout

**Solution:**

```typescript
export default {
  async scheduled(controller, env, ctx) {
    try {
      await yourTask(env);
    } catch (error) {
      // Log detailed error
      console.error('Handler failed:', {
        error: error.message,
        stack: error.stack,
        cron: controller.cron,
        time: new Date(controller.scheduledTime),
      });

      // Send alert
      ctx.waitUntil(sendAlert(error));

      // Re-throw to mark as failed
      throw error;
    }
  },
};
```

Check logs in dashboard for error details.

---

### Issue: Wrong execution time

**Cause:** UTC vs. local timezone confusion

**Solution:**

Convert your desired local time to UTC:

```typescript
// Want 9am PST (UTC-8)?
// 9am PST = 5pm UTC (17:00)

{
  "triggers": {
    "crons": ["0 17 * * *"]
  }
}
```

**Tools:**
- [World Clock Converter](https://www.timeanddate.com/worldclock/converter.html)
- Remember DST changes (PST vs PDT)

---

### Issue: Local testing not working

**Possible causes:**
1. Missing `--test-scheduled` flag
2. Wrong endpoint (should be `/__scheduled`)
3. Python Worker (use `/cdn-cgi/handler/scheduled`)

**Solution:**

```bash
# Correct: Start with flag
bunx wrangler dev --test-scheduled

# In another terminal
curl "http://localhost:8787/__scheduled?cron=0+*+*+*+*"
```

---

## Production Checklist

Before deploying cron triggers to production:

- [ ] Cron expression validated on [Crontab Guru](https://crontab.guru/)
- [ ] Handler named exactly `scheduled` in default export
- [ ] ES modules format used (not Service Worker)
- [ ] Local timezone converted to UTC
- [ ] Error handling implemented with logging
- [ ] Alerts configured for failures
- [ ] CPU limits increased if needed (`limits.cpu_ms`)
- [ ] Environment bindings tested
- [ ] Tested locally with `--test-scheduled`
- [ ] Deployment tested in staging environment
- [ ] Waited 15 minutes after deploy for propagation
- [ ] Verified execution in dashboard logs
- [ ] Monitoring and alerting configured
- [ ] Documentation updated with schedule details

---

## Related Documentation

- **Cloudflare Cron Triggers**: https://developers.cloudflare.com/workers/configuration/cron-triggers/
- **Scheduled Handler API**: https://developers.cloudflare.com/workers/runtime-apis/handlers/scheduled/
- **Cron Trigger Examples**: https://developers.cloudflare.com/workers/examples/cron-trigger/
- **Multiple Cron Triggers**: https://developers.cloudflare.com/workers/examples/multiple-cron-triggers/
- **Wrangler Triggers Command**: https://developers.cloudflare.com/workers/wrangler/commands/#triggers
- **Workers Pricing**: https://developers.cloudflare.com/workers/platform/pricing/
- **Workflows Integration**: https://developers.cloudflare.com/workflows/
- **Crontab Guru** (validator): https://crontab.guru/
- **Time Zone Converter**: https://www.timeanddate.com/worldclock/converter.html

---

**Last Updated**: 2025-10-23
**Version**: 1.0.0
**Maintainer**: Claude Skills Maintainers | maintainers@example.com
