---
name: tzurot-architecture
description: Microservices architecture patterns for Tzurot v3. Use when creating services, deciding where code belongs, or understanding service boundaries. Covers dependencies and anti-patterns from v2.
lastUpdated: '2026-01-21'
---

# Tzurot v3 Architecture

**Use this skill when:** Adding new features, deciding where code belongs, designing system interactions, or refactoring service boundaries.

## Quick Reference

```
Discord User
    ↓
bot-client (Discord.js)
    ↓ HTTP
api-gateway (Express + BullMQ)
    ↓ Redis Queue
ai-worker (AI + pgvector)
    ↓
OpenRouter/Gemini API
```

## Core Principles

1. **Simple, clean classes** - No DDD over-engineering (learned from v2)
2. **Clear service boundaries** - Each service has single responsibility
3. **No circular dependencies** - Services can't import from each other
4. **Shared code in common-types** - Cross-service types, utils, services
5. **Constructor injection** - Simple dependency passing, no DI containers

## Three Microservices

| Service         | Responsibility    | Does                                   | Does NOT                            |
| --------------- | ----------------- | -------------------------------------- | ----------------------------------- |
| **bot-client**  | Discord interface | Events, webhooks, commands, formatting | Business logic, AI calls, direct DB |
| **api-gateway** | HTTP API + queue  | Endpoints, validation, job creation    | AI processing, Discord interaction  |
| **ai-worker**   | AI + memory       | Jobs, memory, AI calls, embeddings     | HTTP endpoints, Discord interaction |

## Where to Put New Code

| Type                       | Location               |
| -------------------------- | ---------------------- |
| Webhook/message formatting | `bot-client/`          |
| Slash commands             | `bot-client/commands/` |
| HTTP endpoints             | `api-gateway/routes/`  |
| Job creation               | `api-gateway/queue.ts` |
| AI provider clients        | `ai-worker/providers/` |
| Memory/embeddings          | `ai-worker/services/`  |
| Shared types/constants     | `common-types/`        |
| Discord type guards        | `common-types/types/`  |

## Autocomplete Utilities (CRITICAL)

**ALWAYS check for existing utilities before writing autocomplete handlers.**

Available in `bot-client/src/utils/autocomplete/`:

| Utility                         | Purpose                   | Option Names               |
| ------------------------------- | ------------------------- | -------------------------- |
| `handlePersonalityAutocomplete` | Personality selection     | `personality`, `character` |
| `handlePersonaAutocomplete`     | Profile/persona selection | `profile`, `persona`       |

```typescript
// ✅ GOOD - Delegate to shared utility
import { handlePersonalityAutocomplete } from '../../utils/autocomplete/personalityAutocomplete.js';

await handlePersonalityAutocomplete(interaction, {
  optionName: 'personality',
  showVisibility: true,
  ownedOnly: false,
});

// ❌ BAD - Duplicating 50+ lines of autocomplete logic
```

## Error Message Patterns

| Layer           | Pattern               | Example                                                    |
| --------------- | --------------------- | ---------------------------------------------------------- |
| **api-gateway** | Clean JSON, NO emojis | `{ "error": "NOT_FOUND", "message": "Persona not found" }` |
| **bot-client**  | ADD emojis for users  | `'❌ Profile not found.'`                                  |

```typescript
// ✅ Gateway - clean for programmatic use
sendError(res, ErrorResponses.notFound('Persona'));

// ✅ Bot - emoji for users
await interaction.editReply({ content: '❌ Profile not found.' });
```

## Anti-Patterns from v2 (DON'T DO)

| Pattern                                     | Why Not         | v3 Alternative               |
| ------------------------------------------- | --------------- | ---------------------------- |
| Generic `IRepository<T>`                    | Too abstract    | Concrete service methods     |
| DI containers                               | Over-engineered | Direct instantiation         |
| `Controller→UseCase→Service→Repository→ORM` | Too many layers | `Route→Service→Prisma`       |
| Complex event bus                           | Unnecessary     | Redis pub/sub for cache only |
| Value objects everywhere                    | Overhead        | Simple validation functions  |

```typescript
// ❌ v2 - Container hell
container.bind('PersonalityService').to(PersonalityService);
const service = container.get('PersonalityService');

// ✅ v3 - Simple
const service = new PersonalityService(prisma);
```

## Dependency Injection

```typescript
// ✅ GOOD - Simple constructor injection
class MyService {
  constructor(
    private prisma: PrismaClient,
    private redis: Redis
  ) {}
}

const service = new MyService(prisma, redis);
```

## When to Extract a Service

**Extract when:**

- Shared across multiple microservices → common-types
- Complex business logic
- Stateful operations
- Easier testability needed

**Keep inline when:**

- Used in one place only
- Stateless utility function
- Very simple logic

## Complexity Signals (ESLint Warnings)

ESLint warnings indicate when to refactor:

| Warning                  | Threshold | Action                     |
| ------------------------ | --------- | -------------------------- |
| `max-statements`         | >30       | Extract helper functions   |
| `complexity`             | >15       | Use data-driven patterns   |
| `max-lines-per-function` | >100      | Split responsibilities     |
| `max-params`             | >5        | Use options object pattern |

**📚 See**: `tzurot-code-quality` skill for refactoring patterns

## Database Access

**Direct Prisma in services** - No repository pattern

```typescript
// ✅ Direct Prisma
async getPersonality(id: string) {
  return this.prisma.personality.findUnique({ where: { id } });
}

// ❌ Generic repository
interface PersonalityRepository {
  findById(id: string): Promise<Personality>;
}
```

## Configuration

- **Environment variables**: Secrets (tokens, DB URLs)
- **common-types constants**: Application config (timeouts, limits)

```typescript
import { TIMEOUTS, RETRY_CONFIG } from '@tzurot/common-types';
const timeout = TIMEOUTS.LLM_INVOCATION;
```

## Related Skills

- **tzurot-code-quality** - Refactoring patterns for complexity
- **tzurot-async-flow** - BullMQ job patterns
- **tzurot-db-vector** - Database patterns
- **tzurot-types** - Type definitions
- **tzurot-council-mcp** - Major design decisions

## References

- Full architecture: `CLAUDE.md#architecture`
- Project structure: `CLAUDE.md#project-structure`
- Architecture decisions: `docs/architecture/ARCHITECTURE_DECISIONS.md`
