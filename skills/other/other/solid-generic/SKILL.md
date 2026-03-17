---
name: solid-generic
description: SOLID principles for generic TypeScript, Bun, and Node.js projects. Files < 100 lines, interfaces separated, JSDoc mandatory. Use for CLI tools, libraries, scripts, hooks, and non-framework TypeScript code.
version: 1.0.0
user-invocable: true
references: references/solid-principles.md, references/single-responsibility.md, references/open-closed.md, references/liskov-substitution.md, references/interface-segregation.md, references/dependency-inversion.md, references/architecture-patterns.md, references/templates/module.md, references/templates/service.md, references/templates/interface.md, references/templates/validator.md, references/templates/factory.md, references/templates/error.md, references/templates/test.md
related-skills: solid-react, solid-nextjs, solid-php, solid-swift
---

# SOLID Generic - TypeScript / Bun / Node.js

## Agent Workflow (MANDATORY)

Before ANY implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Analyze project structure and existing patterns
2. **fuse-ai-pilot:research-expert** - Verify latest TypeScript/Bun docs via Context7
3. **mcp__context7__query-docs** - Check integration compatibility

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## DRY - Reuse Before Creating (MANDATORY)

**Before writing ANY new code:**
1. **Grep the codebase** for similar function names, patterns, or logic
2. Check shared locations: `modules/cores/lib/`, `modules/cores/interfaces/`, `modules/cores/errors/`
3. If similar code exists -> extend/reuse instead of duplicate
4. If code will be used by 2+ modules -> create in `modules/cores/`
5. Extract repeated logic (3+ occurrences) into shared helpers

---

## Absolute Rules (MANDATORY)

### 1. Files < 100 lines
- **Split at 90 lines** - Never exceed 100
- Modules < 80 lines
- Services < 60 lines
- Validators < 40 lines

### 2. Interfaces Separated (Modular MANDATORY)
```text
modules/[feature]/src/interfaces/   # Feature types
  |- user.interface.ts
  \- service.interface.ts
modules/cores/interfaces/            # Shared types
  \- shared.interface.ts
```
**NEVER put interfaces in implementation files.**
**NEVER use flat `src/` structure - always `modules/`.**

### 3. JSDoc Mandatory
```typescript
/**
 * Parse configuration from file path.
 *
 * @param filePath - Absolute path to config file
 * @returns Parsed configuration object
 * @throws ConfigError if file is invalid
 */
export function parseConfig(filePath: string): Config
```

---

## SOLID Principles (Detailed Guides)

| # | Principle | Reference | Key Rule |
|---|-----------|-----------|----------|
| S | Single Responsibility | [single-responsibility.md](references/single-responsibility.md) | One file = one reason to change |
| O | Open/Closed | [open-closed.md](references/open-closed.md) | Extend via composition, not modification |
| L | Liskov Substitution | [liskov-substitution.md](references/liskov-substitution.md) | Implementations honor interface contracts |
| I | Interface Segregation | [interface-segregation.md](references/interface-segregation.md) | Many focused interfaces > one fat interface |
| D | Dependency Inversion | [dependency-inversion.md](references/dependency-inversion.md) | Depend on abstractions, inject dependencies |

See [solid-principles.md](references/solid-principles.md) for overview and [architecture-patterns.md](references/architecture-patterns.md) for project structure.

---

## Code Templates

| Template | Usage | Max Lines |
|----------|-------|-----------|
| [module.md](references/templates/module.md) | TypeScript/Bun module | 80 |
| [service.md](references/templates/service.md) | Service with DI | 60 |
| [interface.md](references/templates/interface.md) | TypeScript interfaces | - |
| [validator.md](references/templates/validator.md) | Zod validation schemas | 40 |
| [factory.md](references/templates/factory.md) | Factory pattern | 60 |
| [error.md](references/templates/error.md) | Custom error classes | 40 |
| [test.md](references/templates/test.md) | Bun test / Vitest | - |

---

## Forbidden

- Files > 100 lines
- Interfaces in implementation files
- Business logic in entry points
- Missing JSDoc on exports
- `any` type
- Barrel exports (index.ts re-exports)
- Duplicating existing utility without Grep search first
- Copy-pasting logic blocks instead of extracting shared function
- Concrete dependencies without interface abstraction
