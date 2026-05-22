---
name: solid-nextjs
description: This skill should be used when the user asks about "SOLID principles", "Next.js architecture", "modular structure", "code organization", "file size limits", "interface separation", or "JSDoc documentation". Enforces files < 150 lines with mandatory JSDoc and separated interfaces.
version: 1.0.0
user-invocable: true
references: references/solid-principles.md, references/single-responsibility.md, references/open-closed.md, references/liskov-substitution.md, references/interface-segregation.md, references/dependency-inversion.md, references/architecture-patterns.md, references/templates/server-component.md, references/templates/client-component.md, references/templates/service.md, references/templates/hook.md, references/templates/interface.md, references/templates/store.md, references/templates/action.md, references/templates/api-route.md, references/templates/validator.md, references/templates/factory.md, references/templates/adapter.md, references/templates/error.md, references/templates/test.md, references/templates/middleware.md, references/templates/prisma.md, references/templates/i18n.md, references/templates/query.md
---

# SOLID Next.js - Modular Architecture

## Current Date (CRITICAL)

**Today: January 2026** - ALWAYS use the current year for your searches.
Search with "2025" or "2026", NEVER with past years.

## MANDATORY: Research Before Coding

**CRITICAL: Check today's date first, then search documentation and web BEFORE writing any code.**

1. **Use Context7** to query Next.js/React official documentation
2. **Use Exa web search** with current year for latest trends
3. **Check Vercel Blog** of current year for new features
4. **Verify package versions** for Next.js 16 compatibility

**Search queries (replace YYYY with current year):**
- `Next.js [feature] YYYY best practices`
- `React 19 [component] YYYY`
- `TypeScript [pattern] YYYY`
- `Prisma 7 [feature] YYYY`

---

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

### 1. Files < 150 lines

- **Split at 90 lines** - Never exceed 150
- Page components < 50 lines (use composition)
- Server Components < 80 lines
- Client Components < 60 lines
- Server Actions < 30 lines each

### 2. Modular Architecture

See `references/architecture-patterns.md` for complete structure with feature modules and cores directory.

### 3. JSDoc Mandatory

```typescript
/**
 * Fetch user by ID from database.
 *
 * @param id - User unique identifier
 * @returns User object or null if not found
 * @throws DatabaseError on connection failure
 */
export async function getUserById(id: string): Promise<User | null>
```

### 4. Interfaces Separated

```text
modules/auth/src/
├── interfaces/          # Types ONLY
│   ├── user.interface.ts
│   └── session.interface.ts
├── services/            # NO types here
└── components/          # NO types here
```

---

## SOLID Principles (Detailed Guides)

Each SOLID principle has a dedicated reference guide:

1. **`references/single-responsibility.md`** - One class/function = one reason to change
   - File splitting at 90 lines (pages < 50, components < 60, services < 80)
   - Component composition patterns
   - Next.js page & server action examples

2. **`references/open-closed.md`** - Extend via composition, not modification
   - Plugin architecture patterns
   - Provider patterns for multiple implementations
   - Adapter and strategy patterns
   - Adding features without changing existing code

3. **`references/liskov-substitution.md`** - Contract compliance & behavioral subtyping
   - Subtypes must be substitutable for base types
   - Exception and return type contracts
   - Testing LSP compliance

4. **`references/interface-segregation.md`** - Many focused interfaces beat one fat interface
   - Role-based interfaces
   - Avoiding bloated contracts
   - Client-specific interfaces

5. **`references/dependency-inversion.md`** - Depend on abstractions, not implementations
   - Constructor injection patterns
   - Factory patterns for creation
   - IoC containers
   - Easy mocking for tests

See `references/solid-principles.md` for overview and quick reference.

---

## Code Templates

Ready-to-copy code in `references/templates/`:

| Template | Usage |
|----------|-------|
| `server-component.md` | Server Component with data fetching |
| `client-component.md` | Client Component with hooks |
| `service.md` | Service with dependency injection |
| `hook.md` | React hook with state |
| `interface.md` | TypeScript interfaces |
| `store.md` | Zustand store with persistence |
| `action.md` | Server Action with validation |
| `api-route.md` | API Route Handler |
| `validator.md` | Zod validation schemas |
| `factory.md` | Factory pattern |
| `adapter.md` | Adapter pattern |
| `error.md` | Custom error classes |
| `test.md` | Test templates |
| `middleware.md` | Auth middleware |
| `prisma.md` | Prisma singleton |
| `i18n.md` | Feature/global translations |
| `query.md` | Database queries (Prisma 7) |

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

- ❌ Coding without researching docs first (ALWAYS research)
- ❌ Using outdated APIs without checking current year docs
- ❌ Files > 150 lines
- ❌ Interfaces in component files
- ❌ Business logic in `app/` pages
- ❌ Direct DB calls in components
- ❌ Module importing another module (except cores)
- ❌ `'use client'` by default
- ❌ `useEffect` for data fetching
- ❌ Missing JSDoc on exports
- ❌ `any` type
- ❌ Barrel exports
