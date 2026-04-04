---
name: error-tracking
description: Add error tracking and performance monitoring to your project services. Use this skill when adding error handling, creating new controllers/routes, instrumenting background jobs, or tracking performance. Supports Sentry, Datadog, and other monitoring solutions. ALL ERRORS MUST BE CAPTURED - no exceptions.
---

# Error Tracking Integration Skill

## Purpose

This skill enforces comprehensive error tracking and performance monitoring across all services. Customize the patterns below for your specific monitoring solution (Sentry, Datadog, New Relic, etc.).

## When to Use This Skill

- Adding error handling to any code
- Creating new controllers or routes
- Instrumenting background jobs / cron tasks
- Tracking database or API performance
- Adding performance spans
- Handling async operation errors

## CRITICAL RULE

**ALL ERRORS MUST BE CAPTURED TO YOUR MONITORING SERVICE** - No exceptions. Never use console.error alone.

---

## Integration Patterns

### 1. Controller/Route Error Handling

#### Python (FastAPI)
```python
import logging
import sentry_sdk  # or your monitoring library

logger = logging.getLogger(__name__)

@router.get("/items/{item_id}")
async def get_item(item_id: str):
    try:
        result = await item_service.get_item(item_id)
        return result
    except ItemNotFoundError as e:
        logger.warning("Item not found", extra={"item_id": item_id})
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error", extra={"item_id": item_id, "error": str(e)}, exc_info=True)
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Internal server error")
```

#### TypeScript (Express/Node.js)
```typescript
import * as Sentry from '@sentry/node';

router.get('/items/:id', async (req, res) => {
    try {
        const result = await itemService.getItem(req.params.id);
        res.json(result);
    } catch (error) {
        Sentry.captureException(error, {
            tags: { route: '/items/:id', method: 'GET' },
            extra: { itemId: req.params.id, userId: req.user?.id }
        });
        res.status(500).json({ error: 'Internal server error' });
    }
});
```

### 2. Service Layer Error Handling

```python
# Python
class ItemService:
    async def create_item(self, data: ItemCreate) -> Item:
        try:
            item = await self.repository.create(data)
            return item
        except IntegrityError as e:
            logger.warning("Duplicate item", extra={"data": data.model_dump()})
            raise DuplicateItemError("Item already exists")
        except Exception as e:
            logger.error("Failed to create item", extra={"error": str(e)}, exc_info=True)
            sentry_sdk.capture_exception(e)
            raise
```

```typescript
// TypeScript
class ItemService {
    async createItem(data: CreateItemDto): Promise<Item> {
        try {
            return await this.repository.create(data);
        } catch (error) {
            if (error instanceof DuplicateKeyError) {
                logger.warn('Duplicate item', { data });
                throw new ConflictError('Item already exists');
            }
            logger.error('Failed to create item', { error, data });
            Sentry.captureException(error);
            throw error;
        }
    }
}
```

### 3. Background Jobs / Cron Tasks

```typescript
#!/usr/bin/env node
// CRITICAL: Import monitoring first!
import './instrument';
import * as Sentry from '@sentry/node';

async function main() {
    return await Sentry.startSpan({
        name: 'cron.job-name',
        op: 'cron',
        attributes: {
            'cron.job': 'job-name',
            'cron.startTime': new Date().toISOString(),
        }
    }, async () => {
        try {
            // Your job logic here
            await processItems();
        } catch (error) {
            Sentry.captureException(error, {
                tags: {
                    'cron.job': 'job-name',
                    'error.type': 'execution_error'
                }
            });
            console.error('[Job] Error:', error);
            process.exit(1);
        }
    });
}

main()
    .then(() => {
        console.log('[Job] Completed successfully');
        process.exit(0);
    })
    .catch((error) => {
        console.error('[Job] Fatal error:', error);
        process.exit(1);
    });
```

```python
# Python (Celery)
import sentry_sdk
from celery import Celery

@celery_app.task(bind=True, max_retries=3)
def process_items(self):
    try:
        # Your task logic here
        result = do_processing()
        return result
    except TransientError as e:
        logger.warning("Transient error, retrying", extra={"error": str(e)})
        raise self.retry(exc=e, countdown=60)
    except Exception as e:
        logger.error("Task failed", extra={"error": str(e)}, exc_info=True)
        sentry_sdk.capture_exception(e)
        raise
```

### 4. Performance Monitoring

```typescript
import * as Sentry from '@sentry/node';

// Wrap slow operations with spans
const result = await Sentry.startSpan({
    name: 'database.query',
    op: 'db.query',
    attributes: {
        'db.operation': 'findMany',
        'db.table': 'items'
    }
}, async () => {
    return await prisma.item.findMany({ take: 100 });
});
```

```python
# Python with Sentry
import sentry_sdk

with sentry_sdk.start_span(op="db.query", description="Find items") as span:
    span.set_tag("db.table", "items")
    result = await db.items.find_many(limit=100)
```

---

## Error Levels

Use appropriate severity levels:

| Level | When to Use |
|-------|-------------|
| **fatal** | System is unusable (database down, critical service failure) |
| **error** | Operation failed, needs immediate attention |
| **warning** | Recoverable issues, degraded performance |
| **info** | Informational messages, successful operations |
| **debug** | Detailed debugging information (dev only) |

---

## Required Context

Always include relevant context with errors:

```typescript
import * as Sentry from '@sentry/node';

Sentry.withScope((scope) => {
    // User context
    scope.setUser({ id: userId, email: userEmail });

    // Service/environment tags
    scope.setTag('service', 'api');
    scope.setTag('environment', process.env.NODE_ENV);

    // Operation-specific context
    scope.setContext('operation', {
        type: 'item.create',
        itemId: itemId,
        timestamp: new Date().toISOString()
    });

    Sentry.captureException(error);
});
```

```python
import sentry_sdk

with sentry_sdk.push_scope() as scope:
    scope.set_user({"id": user_id, "email": user_email})
    scope.set_tag("service", "api")
    scope.set_context("operation", {
        "type": "item.create",
        "item_id": item_id,
    })
    sentry_sdk.capture_exception(error)
```

---

## Configuration Templates

### Sentry (Node.js)

```typescript
// instrument.ts - Import this FIRST in your app
import * as Sentry from '@sentry/node';
import { nodeProfilingIntegration } from '@sentry/profiling-node';

Sentry.init({
    dsn: process.env.SENTRY_DSN,
    environment: process.env.NODE_ENV || 'development',
    integrations: [
        nodeProfilingIntegration(),
    ],
    tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,
    profilesSampleRate: 0.1,
});
```

### Sentry (Python)

```python
# instrument.py - Import this FIRST in your app
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("ENVIRONMENT", "development"),
    integrations=[
        FastApiIntegration(),
        CeleryIntegration(),
    ],
    traces_sample_rate=0.1 if os.environ.get("ENVIRONMENT") == "production" else 1.0,
)
```

### Environment Variables

```bash
# .env
SENTRY_DSN=https://your-dsn@sentry.io/project
ENVIRONMENT=development
```

---

## Common Mistakes to Avoid

| Don't | Do Instead |
|-------|------------|
| `console.error(error)` only | `logger.error() + captureException()` |
| Swallow errors silently | Always log + capture |
| Expose internal errors to clients | Return generic error messages |
| Generic error messages without context | Add meaningful context to all errors |
| Skip error handling in async operations | Always wrap async with try-catch |
| Forget to import instrument first | Import monitoring setup as first import |

---

## Implementation Checklist

When adding error tracking to new code:

- [ ] Imported monitoring library or helper
- [ ] All try/catch blocks capture to monitoring service
- [ ] Added meaningful context to errors
- [ ] Used appropriate error level (fatal/error/warning/info)
- [ ] No sensitive data in error messages
- [ ] Added performance tracking for slow operations
- [ ] Tested error handling paths
- [ ] For cron jobs: instrument file imported first

---

## Customization Notes

**Replace these for your project:**

1. **Monitoring Service**: Replace `Sentry` with your solution (Datadog, New Relic, etc.)
2. **Import Statements**: Update import paths for your project structure
3. **Environment Variables**: Match your configuration pattern
4. **Service Names**: Use your actual service names in tags
5. **Framework Integrations**: Add integrations for your frameworks

---

## Related Skills

- **backend-dev-guidelines** - General backend patterns
- **frontend-dev-guidelines** - Frontend error boundaries
- **skill-developer** - Creating monitoring-specific skills
