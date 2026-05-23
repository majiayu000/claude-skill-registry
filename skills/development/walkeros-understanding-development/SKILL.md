---
name: walkeros-understanding-development
description:
  Use when contributing to walkerOS, before writing code, or when unsure about
  project conventions. Covers build/test/lint workflow, XP principles, folder
  structure, and package usage.
---

# Understanding walkerOS Development

## Overview

walkerOS follows extreme programming principles with strict conventions. This
skill is your foundation before writing any code.

**Core principle:** DRY, KISS, YAGNI. Test first. Verify before claiming
complete.

## Commands

| Command          | Purpose                     |
| ---------------- | --------------------------- |
| `npm install`    | Install all dependencies    |
| `npm run dev`    | Watch mode for all packages |
| `npm run build`  | Build all packages          |
| `npm run test`   | Run all tests               |
| `npm run lint`   | ESLint + TypeScript check   |
| `npm run format` | Prettier formatting         |

**Validation before commit:** `npm run build && npm run test && npm run lint`

## XP Principles (Non-Negotiable)

| Principle    | In Practice                                              |
| ------------ | -------------------------------------------------------- |
| **DRY**      | Use `@walkeros/core` utilities, don't reimplement        |
| **KISS**     | Minimal code to solve the problem                        |
| **YAGNI**    | Only implement what's requested                          |
| **TDD**      | Test first, watch it fail, then implement                |
| **No `any`** | Never use `any` in production code (tests are exception) |

## Folder Structure

```
packages/
├── core/           # Platform-agnostic types, utilities, schemas
├── collector/      # Central event processing engine
├── config/         # Shared config (eslint, jest, tsconfig, tsup)
├── web/
│   ├── core/       # Web-specific utilities
│   ├── sources/    # browser, dataLayer
│   └── destinations/ # gtag, meta, api, piwikpro, plausible
└── server/
    ├── core/       # Server-specific utilities
    ├── sources/    # gcp
    └── destinations/ # aws, gcp, meta

apps/
├── walkerjs/       # Ready-to-use browser bundle
├── quickstart/     # Code examples (source of truth for patterns)
└── demos/          # Demo applications
```

## Core Package Usage

**Always import from `@walkeros/core`:**

```typescript
// Types
import type { WalkerOS } from '@walkeros/core';

// Utilities
import {
  getEvent,
  createEvent, // Event creation
  getMappingEvent,
  getMappingValue, // Transformations
  isString,
  isObject,
  isDefined, // Type checking
  assign,
  clone, // Object operations
  tryCatch,
  tryCatchAsync, // Error handling
} from '@walkeros/core';
```

**Config package for shared tooling:**

- ESLint config: `@walkeros/config/eslint`
- Jest config: `@walkeros/config/jest`
- TSConfig: `@walkeros/config/tsconfig`
- Tsup config: `@walkeros/config/tsup`

## Testing

**REQUIRED SKILL:** Use `testing-strategy` for detailed testing patterns.

Quick reference:

- Use `env` pattern for mocking (not Jest mocks)
- Import from `dev.ts` for examples
- Test first, watch it fail
- Verify before claiming complete

## Related Skills

- [walkeros-testing-strategy](../walkeros-testing-strategy/SKILL.md) - Testing
  patterns and env mocking

**Source Files:**

- [packages/core/](../../packages/core/) - Core utilities
- [packages/config/](../../packages/config/) - Shared configuration
- [apps/quickstart/](../../apps/quickstart/) - Validated examples
