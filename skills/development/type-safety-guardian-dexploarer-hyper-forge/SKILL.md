---
name: Type Safety Guardian
description: Autonomously enforces TypeScript strict typing standards (ADR-0006)
trigger: Writing TypeScript code, reviewing code, fixing type errors
---

# Type Safety Guardian Skill

I autonomously enforce strict TypeScript typing per **ADR-0006**. I activate whenever TypeScript code is being written or reviewed.

## Core Mission

**ZERO TOLERANCE FOR `any` OR `unknown` TYPES**

## When I Activate

I trigger when:
- Writing new TypeScript code
- Reviewing existing code
- Fixing TypeScript compiler errors
- Refactoring code
- Integrating third-party libraries

## What I Check

### Forbidden Patterns (Auto-Reject)
- `any` types
- `as any` casts
- `unknown` types (except external APIs)
- Property existence checks (`'property' in object`)
- Optional chaining for type narrowing
- Missing return types on public methods

### Required Patterns (Auto-Enforce)
- Explicit return types on public methods
- Strong type assumptions based on context
- Non-null assertions when safe (`value!`)
- Discriminated unions for variant types
- `import type { }` for type imports
- Classes over interfaces for entities
- Shared types from types/core.ts

## How I Help

### 1. Proactive Detection
```typescript
// ❌ I CATCH THIS
function process(data: any) { // FORBIDDEN!
  return data.value;
}

// ✅ I SUGGEST THIS
function process<T extends { value: string }>(data: T): string {
  return data.value;
}
```

### 2. Context-Based Typing
```typescript
// ❌ I CATCH THIS
if ('position' in entity) { // Weak typing!
  entity.position.x = 0;
}

// ✅ I SUGGEST THIS
const player = entity as PlayerEntity; // Strong assumption
player.position.x = 0;
```

### 3. Proper Generics
```typescript
// ❌ I CATCH THIS
function findItem(items: any[], id: string) {
  return items.find(i => i.id === id);
}

// ✅ I SUGGEST THIS
function findItem<T extends { id: string }>(items: T[], id: string): T | undefined {
  return items.find(i => i.id === id);
}
```

## Automatic Actions

When I detect violations:

1. **Immediate alert** - Flag the violation clearly
2. **Root cause analysis** - Why did this happen?
3. **Proper solution** - Show correctly typed version
4. **Fix immediately** - Don't defer, fix now
5. **Educate** - Explain why it matters

## Integration with Project

- Enforces ADR-0006 standards
- Uses eslint rule: `@typescript-eslint/no-explicit-any: 'error'`
- References shared types from `@hyperscape/shared`
- Checks all packages in monorepo
- Fails builds on violations

## Success Metrics

Target: **ZERO `any` types in production code**

Current violations get fixed immediately, not deferred.

## References

- ADR-0006: Enforce TypeScript Strict Typing Standards
- CLAUDE.md coding-standards.mdc
- eslint.config.js

I use Deepwiki to research advanced TypeScript patterns when needed.
