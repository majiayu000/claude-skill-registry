---
name: walkeros-using-logger
description:
  Use when working with walkerOS sources/destinations to understand standard
  logging patterns, replace console.log, or add logging to external API calls.
  Covers DRY principles, when to log, and migration patterns.
---

# Using the walkerOS Logger

## Overview

The logger is walkerOS's standard logging system, available in all sources and
destinations via `env.logger` or `logger` parameter. It provides scoped,
level-aware logging that replaces console.log.

**Core principle:** Don't log what the collector already logs. Only log
meaningful operations like external API calls, transformations, and validation
errors.

## Logger Access

### In Sources

```typescript
export const sourceFetch = async (
  config: PartialConfig,
  env: Types['env'], // env.logger is available here
): Promise<FetchSource> => {
  // Logger is scoped automatically by collector: [type:sourceId]
  env.logger.info('Server listening on port 3000');
};
```

### In Destinations

```typescript
export const destinationDataManager: DestinationInterface = {
  async init({ config, env, logger }) {
    // logger parameter is scoped automatically: [datamanager]
    logger.debug('Auth client created');
  },

  async push(event, { config, data, env, logger }) {
    // logger parameter is scoped: [datamanager]
    logger.debug('API response', { status: 200 });
  },
};
```

**Note:** You don't need to create or configure the logger—it's provided
automatically with proper scoping.

## Logger Methods

```typescript
interface Logger.Instance {
  error(message: string | Error, context?: unknown | Error): void;
  info(message: string | Error, context?: unknown | Error): void;
  debug(message: string | Error, context?: unknown | Error): void;
  throw(message: string | Error, context?: unknown): never;
  scope(name: string): Logger.Instance;
}
```

### Log Levels

- **ERROR (0)**: Always visible—use for errors only
- **INFO (1)**: High-level operations (server startup, event processed)
- **DEBUG (2)**: Low-level details (API calls, transformations)

**Default**: ERROR only (must configure to see INFO/DEBUG)

### Context Parameter

All methods accept optional structured context:

```typescript
logger.debug('Sending to API', {
  endpoint: '/events',
  method: 'POST',
  eventCount: 5,
});
// Output: DEBUG [datamanager] Sending to API { endpoint: '/events', method: 'POST', eventCount: 5 }
```

## When to Log (and When NOT to)

### ❌ DON'T Log These (Collector Handles)

- **Init status**: "Initializing...", "Init started", "Init complete"
- **Push status**: "Processing event...", "Event received"
- **Generic status**: "Settings validated", "Config loaded"
- **Duplicate scoping**: Don't add source/dest name (already in scope)

**Why:** Collector can log these automatically since it calls init/push and has
scoped logger.

### ✅ DO Log These (Meaningful Operations)

- **External API calls**: Before/after with request/response details
- **Auth operations**: Token refresh, client creation/failures
- **Transformations**: Complex mappings or data processing
- **Validation errors**: Always use `logger.throw` for fatal errors

## Usage Patterns

### Pattern 1: Validation Errors (Always Use logger.throw)

```typescript
// ✅ GOOD - Fatal configuration error
async init({ config, logger }) {
  const { apiKey, projectId } = config.settings || {};

  if (!apiKey) {
    logger.throw('Config settings apiKey missing');
  }

  if (!projectId) {
    logger.throw('Config settings projectId missing');
  }
}
```

**Why logger.throw:**

- Logs the error at ERROR level (always visible)
- Throws Error automatically (no separate throw needed)
- Collector catches and handles gracefully
- Never returns (TypeScript type: `never`)

### Pattern 2: External API Calls

```typescript
// ✅ GOOD - Log external calls with context
async push(event, { config, logger }) {
  const endpoint = 'https://api.vendor.com/events';

  // Log before call
  logger.debug('Calling API', {
    endpoint,
    method: 'POST',
    eventId: event.id,
  });

  const response = await fetch(endpoint, {
    method: 'POST',
    body: JSON.stringify(event),
  });

  // Log after call
  logger.debug('API response', {
    status: response.status,
    ok: response.ok,
  });

  if (!response.ok) {
    const errorText = await response.text();
    logger.throw(`API error (${response.status}): ${errorText}`);
  }
}
```

### Pattern 3: Auth Operations

```typescript
// ✅ GOOD - Log auth client creation
async init({ config, logger }) {
  try {
    const authClient = await createAuthClient(config.settings);
    logger.debug('Auth client created');

    return {
      env: { authClient },
    };
  } catch (error) {
    logger.throw(
      `Authentication failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
    );
  }
}
```

### Pattern 4: Server Startup (Sources)

```typescript
// ✅ GOOD - Log server listening (high-level info)
if (settings.port !== undefined) {
  server = app.listen(settings.port, () => {
    env.logger.info(
      `Express source listening on port ${settings.port}\n` +
        `   POST ${settings.path} - Event collection (JSON body)\n` +
        `   GET ${settings.path} - Pixel tracking (query params)\n` +
        `   OPTIONS ${settings.path} - CORS preflight`,
    );
  });
}
```

## Anti-Patterns (What NOT to Do)

### ❌ BAD: Verbose Init Logging

```typescript
async init({ logger }) {
  logger.debug('Data Manager init started'); // Redundant
  logger.info('Data Manager initializing...'); // Redundant
  logger.debug('Settings validated'); // Redundant

  const authClient = await createAuthClient();
  logger.debug('Auth client created'); // OK

  logger.info('Data Manager ready'); // Redundant
}
```

**Problem:** Collector knows when init is called. Only log meaningful operations
(auth client creation).

### ❌ BAD: Redundant Push Logging

```typescript
async push(event, { logger }) {
  logger.debug('Processing event', {
    // Redundant
    name: event.name,
    id: event.id,
  });

  // Do work...

  logger.info('Event processed'); // Redundant
}
```

**Problem:** Collector knows when push is called and can log automatically.

### ❌ BAD: Using console.log

```typescript
// ❌ NEVER use console.log in sources/destinations
console.log('Processing event:', event.name);

// ✅ Use logger instead
logger.debug('API call', { endpoint });
```

## Migration Checklist

When updating a source/destination to use the logger:

- [ ] Remove all `console.log`, `console.warn`, `console.error` statements
- [ ] Remove verbose init/push status logging (let collector handle)
- [ ] Add `logger.throw` for all validation errors (apiKey missing, etc.)
- [ ] Add `logger.debug` before external API calls (with endpoint, method)
- [ ] Add `logger.debug` after external API calls (with response status)
- [ ] Add `logger.debug` for auth operations (client creation, token refresh)
- [ ] Use structured context (objects) instead of string concatenation
- [ ] Verify tests still pass with logger mocked

## Testing with Logger

Use `createMockLogger` from `@walkeros/core` in tests:

```typescript
import { createMockLogger } from '@walkeros/core';

test('throws on missing apiKey', () => {
  const logger = createMockLogger();

  expect(() => {
    destination.init({ config: {}, logger });
  }).toThrow('Config settings apiKey missing');

  expect(logger.throw).toHaveBeenCalledWith('Config settings apiKey missing');
});
```

## Log Level Configuration

Default log level is ERROR. To see INFO/DEBUG logs:

```typescript
import { startFlow } from '@walkeros/collector';

const { elb } = await startFlow({
  logger: {
    level: 'DEBUG', // Show all logs
  },
  destinations: {
    /* ... */
  },
});
```

**Levels:**

- `'ERROR'`: Only errors (default)
- `'INFO'`: Errors + info
- `'DEBUG'`: Everything (errors + info + debug)

## Related Skills

- [walkeros-understanding-destinations](../walkeros-understanding-destinations/SKILL.md) -
  Destination interface
- [walkeros-understanding-sources](../walkeros-understanding-sources/SKILL.md) -
  Source interface

**Key Files:**

- [packages/core/src/logger.ts](../../packages/core/src/logger.ts) - Logger
  implementation
- [packages/core/src/types/logger.ts](../../packages/core/src/types/logger.ts) -
  Logger types
- [packages/core/src/mockLogger.ts](../../packages/core/src/mockLogger.ts) -
  Testing utilities

**Best Practice Examples:**

- [packages/server/destinations/datamanager/src/push.ts](../../packages/server/destinations/datamanager/src/push.ts) -
  API logging patterns
- [packages/server/sources/express/src/index.ts](../../packages/server/sources/express/src/index.ts) -
  Server startup logging

**Needs Improvement:**

- [packages/server/sources/fetch/src/index.ts](../../packages/server/sources/fetch/src/index.ts) -
  Missing all logging
- [packages/server/destinations/meta/src/push.ts](../../packages/server/destinations/meta/src/push.ts) -
  Missing push logging
- [packages/server/destinations/aws/src/firehose/push.ts](../../packages/server/destinations/aws/src/firehose/push.ts) -
  Missing push logging
