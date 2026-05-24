---
name: typescript-debugging
description: Debugging TypeScript build errors in Next.js and Supabase projects. Use when encountering tsc --noEmit failures, type mismatches, 'never' type errors, or Supabase generic issues. Keywords: TypeScript, tsc, build error, type error, never, any, CookieOptions, Database generic.
compatibility: Antigravity, Claude Code, Cursor
metadata:
  version: "1.0"
  project: "stepleague"
---

# TypeScript Debugging Skill

## Overview

TypeScript errors can cascade and become confusing. This skill covers the most common patterns in StepLeague.

---

## ⚠️ Critical Rule: No `<Database>` Generics

```typescript
// ❌ WRONG - Causes cascading 'never' type errors
const supabase = createServerClient<Database>(...);

// ✅ CORRECT - Untyped
const supabase = await createServerSupabaseClient();
const { data } = await supabase.from("leagues").select("*");
const leagues = (data || []).map((l: any) => ({ ... }));
```

**Why?** Supabase generated types often become stale and cause `Property 'x' does not exist on type 'never'` errors.

---

## Common Errors & Fixes

### 1. "Parameter implicitly has 'any' type"

**Error:**
```
Parameter 'options' implicitly has an 'any' type.
```

**Fix:** Add explicit type (see `src/lib/supabase/server.ts`):
```typescript
// ❌ WRONG
setAll(options) { ... }

// ✅ CORRECT - Import from @supabase/ssr
import { CookieOptions } from '@supabase/ssr';
setAll(options: { name: string; value: string; options?: CookieOptions }[]) { ... }
```

---

### 2. "Property does not exist on type 'never'"

**Cause:** Usually from `<Database>` generics or empty array inference.

**Fix:**
```typescript
// ❌ WRONG - TypeScript infers never[]
const items = [];
items.push({ id: 1 });  // Error!

// ✅ CORRECT - Explicit type
const items: Item[] = [];
items.push({ id: 1 });  // Works!
```

---

### 3. "Type 'X' is not assignable to type 'Y'"

**Common in:** Supabase query results

**Fix:** Use type assertion or `any`:
```typescript
// ❌ WRONG
const user: User = data;  // Type mismatch

// ✅ CORRECT - Assert or cast
const user = data as User;
// OR use any for Supabase data
const users = (data || []).map((u: any) => ({
  id: u.id,
  name: u.display_name,
}));
```

---

### 4. "Cannot find module" / Import Errors

**Fix:** Check these in order:
1. File exists at path?
2. Using correct extension? (`.ts` vs `.tsx`)
3. `tsconfig.json` paths correct?
4. Run `npm install` for missing packages

---

### 5. React Component Type Errors

**Error:** `Type '{ children: Element; }' has no properties in common`

**Fix:** Ensure component accepts children:
```typescript
// ❌ WRONG
function MyComponent() { ... }

// ✅ CORRECT
function MyComponent({ children }: { children: React.ReactNode }) { ... }
// OR
function MyComponent(props: React.PropsWithChildren) { ... }
```

---

## Build Verification

Always verify with:
```bash
npx tsc --noEmit
```

Run this before committing to catch type errors early.

---

## Debugging Workflow

1. **Run `npx tsc --noEmit`** - Get full error list
2. **Fix root errors first** - Cascading errors often fix themselves
3. **Check recent changes** - What did you just modify?
4. **Search for `<Database>`** - Remove if present
5. **Use `: any` sparingly** - For Supabase data, it's acceptable

---

## Project-Specific Patterns

### StepLeague Type Conventions

| Pattern | Where | Why |
|---------|-------|-----|
| `(data \|\| []).map((x: any) => ...)` | Supabase queries | Avoids Database generic issues |
| `CookieOptions[]` | Supabase SSR | Required for cookie handling |
| `React.ReactNode` | Component children | Standard children prop type |

---

## Related Skills

- `react-debugging` - Runtime errors vs compile-time
- `supabase-patterns` - Database type handling
