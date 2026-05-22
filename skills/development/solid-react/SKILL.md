---
name: solid-react
description: SOLID principles for React 19. Files < 100 lines, hooks separated, interfaces in src/interfaces/, JSDoc mandatory. Use for React architecture and code quality.
version: 1.0.0
user-invocable: true
references: references/solid-principles.md, references/single-responsibility.md, references/open-closed.md, references/liskov-substitution.md, references/interface-segregation.md, references/dependency-inversion.md, references/architecture-patterns.md, references/templates/component.md, references/templates/hook.md, references/templates/service.md, references/templates/store.md, references/templates/interface.md, references/templates/validator.md, references/templates/factory.md, references/templates/adapter.md, references/templates/error.md, references/templates/test.md
---

# SOLID React - Component Architecture

## Codebase Analysis (MANDATORY)

**Before ANY implementation:**
1. Explore project structure to understand architecture
2. Read existing related files to follow established patterns
3. Identify naming conventions, coding style, and patterns used
4. Understand data flow and dependencies

## DRY - Reuse or Create Shared (MANDATORY)

**Before writing ANY new code:**
1. Search existing codebase for similar functionality
2. Check shared locations: `modules/cores/lib/`, `modules/cores/components/`
3. If similar code exists → extend/reuse instead of duplicate
4. If code will be used by 2+ features → create it in `modules/cores/` directly

---

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Analyze project structure and existing patterns
2. **fuse-ai-pilot:research-expert** - Verify latest docs for all stack technologies
3. **mcp__context7__query-docs** - Check integration compatibility

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Absolute Rules (MANDATORY)

### 1. Files < 100 lines

- **Split at 90 lines** - Never exceed 100
- Components < 50 lines (use composition)
- Hooks < 30 lines each
- Services < 40 lines each

### 2. Modular Architecture

See `references/architecture-patterns.md` for complete structure with feature modules and cores directory.

### 3. JSDoc Mandatory

```typescript
/**
 * Fetch user by ID from API.
 *
 * @param id - User unique identifier
 * @returns User object or null if not found
 */
export async function getUserById(id: string): Promise<User | null>
```

### 4. Interfaces Separated

```text
modules/[feature]/src/interfaces/
├── user.interface.ts
├── post.interface.ts
└── api.interface.ts
```

**NEVER put interfaces in component files.**

---

## SOLID Principles (Detailed Guides)

Each SOLID principle has a dedicated reference guide:

1. **`references/single-responsibility.md`** - One function = one reason to change
   - File splitting at 90 lines (components < 50, hooks < 30)
   - Component composition patterns
   - Split strategy

2. **`references/open-closed.md`** - Extend via composition, not modification
   - Plugin architecture patterns
   - Render props and slots
   - Strategy patterns

3. **`references/liskov-substitution.md`** - Contract compliance & behavioral subtyping
   - Interface contracts
   - Swappable implementations
   - Testing compliance

4. **`references/interface-segregation.md`** - Many focused interfaces beat one fat interface
   - Role-based interfaces
   - Props segregation
   - Context splitting

5. **`references/dependency-inversion.md`** - Depend on abstractions, not implementations
   - Constructor injection patterns
   - Factory patterns
   - Context for DI

See `references/solid-principles.md` for overview and quick reference.

---

## Code Templates

Ready-to-copy code in `references/templates/`:

| Template | Usage | Max Lines |
|----------|-------|-----------|
| `component.md` | React functional component | 50 |
| `hook.md` | Custom hook with TanStack Query | 30 |
| `service.md` | Service with dependency injection | 40 |
| `store.md` | Zustand store with persistence | 40 |
| `interface.md` | TypeScript interfaces | - |
| `validator.md` | Zod validation schemas | 30 |
| `factory.md` | Factory pattern | 40 |
| `adapter.md` | Adapter pattern | 40 |
| `error.md` | Custom error classes | 30 |
| `test.md` | Vitest + Testing Library | - |

---

## Response Guidelines

1. **Research first** - MANDATORY: Search Context7 + Exa before ANY code
2. **Show complete code** - Working examples, not snippets
3. **Explain decisions** - Why this pattern over alternatives
4. **Include tests** - Always suggest test cases
5. **Handle errors** - Never ignore, use error boundaries
6. **Type everything** - Full TypeScript, no `any`
7. **Document code** - JSDoc for complex functions

---

## Forbidden

- Coding without researching docs first (ALWAYS research)
- Using outdated APIs without checking current year docs
- Files > 100 lines
- Interfaces in component files
- Business logic in components
- Class components
- Missing JSDoc on exports
- `any` type
- Barrel exports (index.ts re-exports)
- `useEffect` for data fetching (use TanStack Query or Router loaders)
- Module importing another module (except cores)
