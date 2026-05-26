---
name: typescript-project
description: Modern TypeScript project architecture guide for 2025. Use when creating new TS projects, setting up configurations, or designing project structure. Covers tech stack selection, layered architecture, and best practices.
---
# TypeScript Project Architecture

## Core Principles

- **Type safety first** — Strict mode, no `any`, Zod for runtime validation
- **ESM native** — ES Modules by default, Node 22+ / Bun
- **Layered architecture** — Separate lib/services/adapters
- **200-line limit** — No file exceeds 200 lines (see elegant-architecture skill)
- **Test reality** — Vitest/Bun test, minimal mocks
- **No backwards compatibility** — Delete, don't deprecate. Change directly, no shims
- **LiteLLM for LLM APIs** — Use LiteLLM proxy for all LLM integrations, unless specific SDK required

---

## No Backwards Compatibility

> **Delete unused code. Change directly. No compatibility layers.**

### Why

- Dead code is tech debt
- Compatibility shims add complexity
- Old patterns spread through copy-paste
- "Temporary" workarounds become permanent

### Anti-Patterns to Avoid

```typescript
// ❌ BAD: Renaming but keeping old export
export { newName };
export { newName as oldName }; // "for backwards compatibility"

// ❌ BAD: Unused parameter with underscore
function process(_legacyParam: string, data: Data) { ... }

// ❌ BAD: Deprecated comments instead of deletion
/** @deprecated Use newMethod instead */
export function oldMethod() { ... }

// ❌ BAD: Re-exporting removed functionality
export { removed } from './legacy'; // Keep for existing consumers

// ❌ BAD: Feature flags for old behavior
if (config.useLegacyMode) { ... }
```

### Correct Approach

```typescript
// ✅ GOOD: Just delete and update all usages
// Old: export { fetchData as getData }
// New: export { fetchData }
// Then: Find & replace all getData → fetchData

// ✅ GOOD: Remove unused parameters entirely
function process(data: Data) { ... }

// ✅ GOOD: Delete deprecated code, update callers
// Don't mark as deprecated, just remove it

// ✅ GOOD: Breaking changes are fine in active development
// Semantic versioning handles this for libraries
```

### When Changing Interfaces

```typescript
// ❌ BAD: Adding optional fields "for compatibility"
interface User {
  id: string;
  name: string;
  firstName?: string; // New field, name kept for compatibility
  lastName?: string;
}

// ✅ GOOD: Clean break, update all usages
interface User {
  id: string;
  firstName: string;
  lastName: string;
}
// Then update ALL code that uses User.name
```

### Migration Strategy

1. **Find all usages** — `grep -r "oldName" src/`
2. **Update all at once** — Single commit, no transition period
3. **Delete old code** — No deprecation warnings, just remove
4. **Run tests** — Ensure nothing breaks

---

## LiteLLM for LLM APIs

> **Use LiteLLM proxy for all LLM integrations. Don't call provider APIs directly.**

### Why LiteLLM

- **Unified interface** — One API for 100+ LLM providers (OpenAI, Anthropic, Azure, Bedrock, etc.)
- **Provider agnostic** — Switch models without code changes
- **Cost tracking** — Built-in usage and cost monitoring
- **Load balancing** — Automatic failover between providers
- **Rate limiting** — Protect against quota exhaustion

### Setup

```bash
# Run LiteLLM proxy (Docker)
docker run -p 4000:4000 ghcr.io/berriai/litellm:main-stable

# Or install locally
pip install litellm[proxy]
litellm --model gpt-4o
```

### TypeScript Usage

```typescript
// adapters/llm.adapter.ts
import { OpenAI } from 'openai';

// Connect to LiteLLM proxy using OpenAI SDK
const llm = new OpenAI({
  baseURL: process.env.LITELLM_URL || 'http://localhost:4000',
  apiKey: process.env.LITELLM_API_KEY || 'sk-1234', // Proxy API key
});

export async function complete(prompt: string, model = 'gpt-4o'): Promise<string> {
  const response = await llm.chat.completions.create({
    model, // Can be any model: gpt-4o, claude-3-opus, gemini-pro, etc.
    messages: [{ role: 'user', content: prompt }],
  });
  return response.choices[0]?.message?.content ?? '';
}
```

### When NOT to Use LiteLLM

- Streaming with provider-specific features (e.g., Anthropic's tool use streaming)
- Provider-specific APIs not in OpenAI format (embeddings with metadata, etc.)
- Direct SDK required for compliance/security reasons

### Anti-Patterns

```typescript
// ❌ BAD: Direct provider SDKs everywhere
import Anthropic from '@anthropic-ai/sdk';
import OpenAI from 'openai';
import { GoogleGenerativeAI } from '@google/generative-ai';

// ❌ BAD: Provider-specific code scattered across codebase
if (provider === 'anthropic') { ... }
else if (provider === 'openai') { ... }

// ✅ GOOD: Single LiteLLM adapter, switch models via config
const response = await llm.chat.completions.create({
  model: config.llmModel, // "gpt-4o" or "claude-3-opus" or "gemini-pro"
  messages,
});
```

---

## Quick Start

### 1. Initialize Project

```bash
# Using Bun (recommended)
bun init
bun add zod
bun add -d typescript @types/bun @biomejs/biome

# Using Node.js
npm init -y
npm i zod
npm i -D typescript @types/node tsx @biomejs/biome
```

### 2. Apply Tech Stack

| Layer | Recommendation |
|-------|----------------|
| Runtime | Bun / Node 22+ |
| Language | TypeScript (latest) |
| Validation | Zod (latest) |
| Testing | Bun test / Vitest |
| Build | bun build / tsup |
| Linting | Biome (latest) |

### Version Strategy

> **Always use latest. Never pin versions in templates.**

```json
{
  "dependencies": {
    "zod": "latest"
  },
  "devDependencies": {
    "@biomejs/biome": "latest",
    "typescript": "latest"
  }
}
```

- `bun add` / `npm i` automatically fetches latest
- Use `bun update --latest` to upgrade all dependencies
- Lock files (`bun.lockb`, `package-lock.json`) ensure reproducible builds
- Breaking changes are handled by reading changelogs, not by avoiding updates

### 3. Use Standard Structure

```
project/
├── src/
│   ├── index.ts           # Entry point
│   ├── lib/               # Core utilities
│   │   ├── config.ts      # Configuration management
│   │   ├── errors.ts      # Custom error classes
│   │   ├── logger.ts      # Logging infrastructure
│   │   └── types.ts       # Shared type definitions
│   ├── services/          # Business logic
│   │   └── *.service.ts
│   └── adapters/          # External integrations
│       └── *.adapter.ts
├── tests/                 # Test files
│   └── *.test.ts
├── tsconfig.json
├── package.json
└── biome.json             # or eslint.config.js
```

---

## Architecture Layers

### lib/ — Core Infrastructure

Foundational code used across the entire application:

```typescript
// lib/types.ts — Shared type definitions
export interface Result<T, E = Error> {
  ok: boolean;
  data?: T;
  error?: E;
}

// lib/errors.ts — Custom errors
export class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = 'AppError';
  }
}

// lib/config.ts — Configuration
export const config = {
  env: process.env.NODE_ENV || 'development',
  port: Number(process.env.PORT) || 3000,
  db: {
    url: process.env.DATABASE_URL!,
  },
} as const;

// lib/logger.ts — Logging (see structured-logging skill)
```

### services/ — Business Logic

Pure business logic with injected dependencies:

```typescript
// services/user.service.ts
export class UserService {
  constructor(private readonly userRepo: UserRepository) {}

  async create(input: CreateUserInput): Promise<User> {
    const existing = await this.userRepo.findByEmail(input.email);
    if (existing) throw new AppError('Email exists', 'USER_EXISTS', 409);
    return this.userRepo.save(User.create(input));
  }
}
```

### adapters/ — External Integrations

Interface with external systems (DB, APIs, file system):

```typescript
// adapters/postgres.adapter.ts
export class PostgresUserRepository implements UserRepository {
  constructor(private readonly db: Database) {}

  async findByEmail(email: string): Promise<User | null> {
    const row = await this.db.query('SELECT * FROM users WHERE email = $1', [email]);
    return row ? User.fromRow(row) : null;
  }
}
```

---

## Configuration Files

### tsconfig.json (2025)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "declaration": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### package.json

```json
{
  "name": "my-project",
  "version": "1.0.0",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "dev": "bun run --watch src/index.ts",
    "build": "bun build src/index.ts --outdir dist --target bun",
    "start": "bun dist/index.js",
    "test": "bun test",
    "typecheck": "tsc --noEmit"
  }
}
```

---

## Validation with Zod

```typescript
import { z } from 'zod';

// Define schemas
export const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  age: z.number().int().positive().optional(),
});

// Infer types from schemas
export type CreateUserInput = z.infer<typeof CreateUserSchema>;

// Validate at boundaries
export function validateInput<T>(schema: z.ZodType<T>, data: unknown): T {
  return schema.parse(data);
}
```

---

## Error Handling Pattern

```typescript
// lib/errors.ts
export class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500,
    public readonly context?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'AppError';
    Error.captureStackTrace(this, this.constructor);
  }

  static notFound(resource: string, id: string) {
    return new AppError(`${resource} not found: ${id}`, 'NOT_FOUND', 404);
  }

  static validation(message: string, context?: Record<string, unknown>) {
    return new AppError(message, 'VALIDATION_ERROR', 400, context);
  }
}

// Usage
throw AppError.notFound('User', userId);
```

---

## Testing Strategy

```typescript
// tests/user.service.test.ts
import { describe, it, expect, beforeEach } from 'bun:test';
import { UserService } from '../src/services/user.service';
import { InMemoryUserRepository } from './helpers/in-memory-repo';

describe('UserService', () => {
  let service: UserService;
  let repo: InMemoryUserRepository;

  beforeEach(() => {
    repo = new InMemoryUserRepository();
    service = new UserService(repo);
  });

  it('creates user with valid input', async () => {
    const user = await service.create({
      email: 'test@example.com',
      name: 'Test User',
    });

    expect(user.email).toBe('test@example.com');
    expect(await repo.findByEmail('test@example.com')).toEqual(user);
  });

  it('rejects duplicate email', async () => {
    await service.create({ email: 'test@example.com', name: 'User 1' });

    expect(
      service.create({ email: 'test@example.com', name: 'User 2' })
    ).rejects.toThrow('Email exists');
  });
});
```

---

## Checklist

```markdown
## Project Setup
- [ ] TypeScript strict mode enabled
- [ ] ESM modules configured
- [ ] Biome/ESLint configured
- [ ] Testing framework ready

## Architecture
- [ ] lib/ for core utilities
- [ ] services/ for business logic
- [ ] adapters/ for external integrations
- [ ] Clear module boundaries

## Quality
- [ ] Zod schemas for validation
- [ ] Custom error classes
- [ ] Structured logging
- [ ] Tests for critical paths

## Build
- [ ] Build script configured
- [ ] Type checking in CI
- [ ] Tests in CI
```

---

## See Also

- [reference/architecture.md](reference/architecture.md) — Detailed architecture patterns
- [reference/tech-stack.md](reference/tech-stack.md) — Tech stack comparison
- [reference/patterns.md](reference/patterns.md) — Design patterns
- [elegant-architecture skill](../elegant-architecture.SKILL.md) — 200-line file limit
- [structured-logging skill](../structured-logging/) — Logging setup
