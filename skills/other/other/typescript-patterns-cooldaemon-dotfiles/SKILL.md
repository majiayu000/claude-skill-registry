---
name: typescript-patterns
description: TypeScript and JavaScript development patterns including package manager detection (npm, pnpm, bun, yarn), project structure, and Node.js backend/tooling. Use when writing, reviewing, or refactoring TypeScript/JavaScript application or library code. Do NOT use for test code -- use typescript-testing instead.
durability: encoded-preference
---

# TypeScript/JavaScript Patterns

Patterns for TypeScript and JavaScript development (Node.js, tooling).

## Package Manager Detection (CRITICAL)

**Before running ANY npm/package commands, detect the package manager:**

| File | Package Manager | Install | Run Script |
|------|-----------------|---------|------------|
| `bun.lockb` or `bun.lock` | bun | `bun install` | `bun run` |
| `pnpm-lock.yaml` | pnpm | `pnpm install` | `pnpm run` |
| `yarn.lock` | yarn | `yarn install` | `yarn` |
| `package-lock.json` | npm | `npm install` | `npm run` |
| None (new project) | npm | `npm init -y` | `npm run` |

**NEVER use `npm install` directly when a non-npm lock file exists.**

**Follow the existing project's lock file. Never mix package managers.**

## Async/Await Patterns

### Parallel Execution
```typescript
// GOOD: Parallel when independent
const [users, markets, stats] = await Promise.all([
  fetchUsers(),
  fetchMarkets(),
  fetchStats()
])

// BAD: Sequential when unnecessary
const users = await fetchUsers()
const markets = await fetchMarkets()
const stats = await fetchStats()
```

## Type Safety

```typescript
// GOOD: Proper types with union for status
interface Market {
  id: string
  name: string
  status: 'active' | 'resolved' | 'closed'
  created_at: Date
}

function getMarket(id: string): Promise<Market> { }
```

## Module Organization

```
src/
├── index.ts           # Entry point
├── types/             # TypeScript types
├── lib/               # Utilities and helpers
├── services/          # Business logic
└── handlers/          # Request handlers
```
