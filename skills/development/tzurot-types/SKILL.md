---
name: tzurot-types
description: Use when creating types, constants, Zod schemas, or working with data validation. Covers common-types package organization, runtime validation, and type guards across microservices.
lastUpdated: '2026-01-21'
---

# Tzurot v3 Types & Constants

**Use this skill when:** Creating new types, adding constants, validating data at service boundaries, or sharing code across microservices.

## Quick Reference

```typescript
// Import from common-types
import { TIMEOUTS, RETRY_CONFIG, PersonalityConfigSchema } from '@tzurot/common-types';

// Constants: SCREAMING_SNAKE_CASE + as const
export const MY_CONFIG = { VALUE: 123 } as const;

// Runtime validation at service boundaries
const validated = MySchema.parse(untrustedData);

// Type inference from Zod
type MyType = z.infer<typeof MySchema>;
```

## Package Structure

```
packages/common-types/src/
├── constants/        # Application constants by domain
│   ├── timing.ts     # TIMEOUTS, INTERVALS, RETRY_CONFIG
│   ├── queue.ts      # REDIS_KEY_PREFIXES, QUEUE_CONFIG
│   ├── discord.ts    # TEXT_LIMITS, DISCORD_LIMITS
│   └── ai.ts         # AI_DEFAULTS, MODEL_DEFAULTS
├── types/            # TypeScript interfaces + Zod schemas
│   ├── schemas.ts    # Zod schemas for validation
│   └── *.ts          # Domain-specific types
├── services/         # Shared service classes
└── utils/            # Utility functions
```

## When to Add to Common-Types

| Content                 | Add to Common-Types? | Location                 |
| ----------------------- | -------------------- | ------------------------ |
| Value used in 2+ files  | ✅ Yes               | `constants/<domain>.ts`  |
| BullMQ job payloads     | ✅ Yes               | `types/queue-types.ts`   |
| HTTP API contracts      | ✅ Yes               | `types/schemas.ts`       |
| Type guards for Discord | ✅ Yes               | `types/discord-types.ts` |
| Service-internal types  | ❌ No                | Keep in service          |
| Test-only values        | ❌ No                | Keep in test file        |

## Constants Patterns

### Create Constants For

```typescript
// ✅ Timeouts and delays
import { TIMEOUTS } from '@tzurot/common-types';
await delay(TIMEOUTS.CACHE_TTL);

// ✅ Redis key prefixes
import { REDIS_KEY_PREFIXES } from '@tzurot/common-types';
await redis.set(`${REDIS_KEY_PREFIXES.WEBHOOK_MESSAGE}${id}`, data);

// ✅ API limits
import { TEXT_LIMITS } from '@tzurot/common-types';
if (content.length > TEXT_LIMITS.MESSAGE_MAX_LENGTH) {
  /* chunk */
}
```

### Don't Create Constants For

```typescript
// ✅ FINE - One-off strings
logger.info('Personality cache initialized');

// ✅ FINE - Self-documenting values
const defaultTemperature = 0.8;

// ✅ FINE - Test-specific data
const mockUserId = 'test-user-123';
```

### Constant Naming

```typescript
export const RETRY_CONFIG = {
  /** Standard retry attempts */
  MAX_ATTEMPTS: 3,
  /** Initial delay (1 second) */
  INITIAL_DELAY_MS: 1000,
} as const; // Always use 'as const'
```

## Zod Schema Patterns

### Runtime Validation at Boundaries

```typescript
import { z } from 'zod';

// Define schema
export const PersonalityConfigSchema = z.object({
  name: z.string().min(1).max(100),
  systemPrompt: z.string().min(10),
  model: z.string(),
  temperature: z.number().min(0).max(2).optional(),
});

// Infer type
export type PersonalityConfig = z.infer<typeof PersonalityConfigSchema>;

// Validate at service boundary
app.post('/api/personality', (req, res) => {
  try {
    const config = PersonalityConfigSchema.parse(req.body);
    // config is now type-safe
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ errors: error.errors });
    }
    throw error;
  }
});
```

### Type Guards

```typescript
// packages/common-types/src/types/discord-types.ts
import type { Channel, TextChannel, DMChannel } from 'discord.js';

export function isTextChannel(channel: Channel): channel is TextChannel {
  return channel.type === 0; // ChannelType.GuildText
}

export function isDMChannel(channel: Channel): channel is DMChannel {
  return channel.type === 1; // ChannelType.DM
}

// Usage
if (isTextChannel(message.channel)) {
  // message.channel is now TextChannel
  const perms = message.channel.permissionsFor(client.user!);
}
```

## Anti-Patterns

### Constants Anti-Patterns

```typescript
// ❌ BAD - Magic number
await delay(300000);

// ✅ GOOD - Named constant
await delay(TIMEOUTS.CACHE_TTL);

// ❌ BAD - Too deeply nested
CONFIG.AI.PROVIDERS.OPENROUTER.TIMEOUTS.DEFAULT;

// ✅ GOOD - Flat structure
AI_TIMEOUTS.OPENROUTER_DEFAULT;
```

### Types Anti-Patterns

```typescript
// ❌ BAD - Trusts external data
const data = req.body as MyType; // Unsafe cast!

// ✅ GOOD - Validate at boundary
const data = MySchema.parse(req.body);

// ❌ BAD - Duplicate types across services
// bot-client/types.ts AND ai-worker/types.ts

// ✅ GOOD - Single source in common-types
import { MyType } from '@tzurot/common-types';

// ❌ BAD - Using 'any'
function process(data: any) {}

// ✅ GOOD - Proper typing
function process(data: ValidatedType) {}
```

## Adding New Constants

1. Determine domain (`timing.ts`, `queue.ts`, `discord.ts`, `ai.ts`)
2. Add with JSDoc documentation
3. Export from `constants/index.ts`
4. Import via `@tzurot/common-types`

```typescript
// packages/common-types/src/constants/timing.ts
export const TIMEOUTS = {
  /** Description of why this value */
  MY_NEW_TIMEOUT: 60000,
} as const;
```

## Adding New Schemas

1. Define Zod schema in `types/schemas.ts`
2. Export inferred TypeScript type
3. Use `.parse()` at service boundaries
4. Handle `z.ZodError` appropriately

```typescript
// packages/common-types/src/types/schemas.ts
export const MyNewSchema = z.object({
  /* ... */
});
export type MyNewType = z.infer<typeof MyNewSchema>;
```

## Related Skills

- **tzurot-code-quality** - no-explicit-any, type safety enforcement
- **tzurot-testing** - Type-safe test fixtures
- **tzurot-async-flow** - BullMQ job data types
- **tzurot-db-vector** - Prisma schema types
- **tzurot-architecture** - Service boundaries

## References

- Constants: `packages/common-types/src/constants/`
- Types: `packages/common-types/src/types/`
- Zod docs: https://zod.dev/
