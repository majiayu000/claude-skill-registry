---
name: debugging
description: Systematic debugging with four-phase framework + Makerkit-specific patterns. ALWAYS use when encountering bugs, errors, crashes, test failures, or unexpected behavior. Triggers include "bug", "error", "crash", "not working", "fails", "broken", "ça marche pas", "ne fonctionne pas", "erreur", "plantage", "cassé", "supabase error", "drizzle error", "migration fail", "rls fail", "hydration", "turborepo fail". Covers Supabase, Drizzle, Next.js App Router, and Turborepo debugging.
---

# Debugging

Systematic debugging framework with Makerkit-specific patterns.

## Overview

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

This skill orchestrates four sub-skills:
1. **systematic-debugging/** - Four-phase framework (mandatory)
2. **root-cause-tracing/** - Backward tracing technique
3. **verification-before-completion/** - Evidence gates
4. **defense-in-depth/** - Validation layers after fix

## Quick Start

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

**The Four Phases:**
1. **Root Cause** - Read errors, reproduce, check changes, gather evidence
2. **Pattern** - Find working examples, compare, identify differences
3. **Hypothesis** - Form theory, test minimally, verify
4. **Implementation** - Create failing test, fix root cause, verify

**If 3+ fixes failed:** Question the architecture, not another fix.

---

## Makerkit-Specific Debugging

### Supabase Issues

#### RLS Policy Failures
```bash
# Check if RLS is the issue
pnpm supabase:web:start  # Start local Supabase

# In Supabase Studio (localhost:54323):
# 1. SQL Editor → Run query with service_role (bypasses RLS)
# 2. If works with service_role but not anon/authenticated → RLS issue

# Debug specific policy
SELECT * FROM pg_policies WHERE tablename = 'your_table';

# Test policy logic
SET LOCAL ROLE authenticated;
SET LOCAL request.jwt.claims = '{"sub": "user-uuid-here"}';
SELECT * FROM your_table;
```

**Common RLS issues:**
- Missing `auth.uid()` check in policy
- Policy using wrong column for user ownership
- Missing policy for specific operation (SELECT exists but INSERT missing)

#### Migration Conflicts
```bash
# Reset local DB and reapply migrations
pnpm supabase:web:reset

# If migration fails, check:
# 1. supabase/migrations/ folder for conflicting files
# 2. Order of migrations (timestamps)
# 3. Dependencies between migrations

# Generate diff to see pending changes
pnpm supabase:web:diff
```

#### Type Sync Issues (Supabase ↔ Drizzle)
```bash
# Regenerate Supabase types
pnpm supabase:web:typegen

# Pull schema into Drizzle
pnpm drizzle:pull

# If types mismatch:
# 1. Check supabase/schemas/*.sql matches actual DB
# 2. Verify packages/supabase/src/ reflects latest schema
# 3. Run both commands in sequence
```

### Drizzle ORM Issues

#### Schema Drift
```bash
# Compare Drizzle schema vs actual DB
# 1. Check supabase/schemas/ folder
# 2. Compare with packages/supabase/src/schema/

# Pull fresh from DB
pnpm drizzle:pull

# If conflict: Trust supabase/schemas/ as source of truth
```

#### Query Builder Errors
```typescript
// Common issue: Wrong import
// ❌ Wrong
import { eq } from 'drizzle-orm';
import { users } from '@kit/supabase';

// ✅ Correct
import { eq } from 'drizzle-orm';
import { users } from '@kit/supabase/schema';
```

#### Type Inference Issues
```typescript
// If Drizzle types are wrong after schema change:
// 1. pnpm supabase:web:typegen
// 2. pnpm drizzle:pull
// 3. Restart TypeScript server (VS Code: Cmd+Shift+P → "Restart TS Server")
```

### Next.js App Router Issues

#### Server Component Errors
```
Error: You're importing a component that needs useState/useEffect...
```

**Fix:** Add `"use client"` directive to the component or its parent.

**Debug strategy:**
```bash
# Find the boundary
# 1. Error shows which component needs client
# 2. Check if it uses: useState, useEffect, useContext, event handlers
# 3. Add "use client" at the top of that file
```

#### Hydration Mismatches
```
Warning: Text content did not match. Server: "..." Client: "..."
```

**Common causes:**
1. Date/time rendering (server vs client timezone)
2. Random values generated on render
3. Browser-only APIs used during SSR
4. Extension injecting content

**Fix pattern:**
```typescript
// Use useEffect for client-only values
const [mounted, setMounted] = useState(false);
useEffect(() => setMounted(true), []);
if (!mounted) return <Skeleton />;
```

#### Route Conflicts
```
apps/web/app/
├── (marketing)/     ← Route group (no URL segment)
├── [account]/       ← Dynamic segment
└── admin/           ← Static segment
```

**Priority:** Static > Dynamic > Catch-all

**Debug:**
```bash
# Check for conflicting routes
ls -la apps/web/app/

# Common issues:
# 1. (group) folder accidentally has page.tsx
# 2. [dynamic] conflicts with static route
# 3. [...catchAll] catches too much
```

#### Server Actions Failing
```typescript
// Check enhanceAction wrapper
export const myAction = enhanceAction(async (data) => {
  // If fails silently, add logging:
  console.log('Action input:', data);

  // Check auth context
  const { user } = await requireUser();
  console.log('User:', user?.id);
}, {
  schema: mySchema,
});
```

### Turborepo Issues

#### Cache Invalidation
```bash
# Force rebuild without cache
turbo run build --force

# Clear all caches
pnpm clean

# Check what's cached
turbo run build --dry-run
```

#### Task Dependency Issues
```json
// turbo.json - Check dependsOn
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"],  // ← Depends on workspace deps
      "outputs": [".next/**", "dist/**"]
    }
  }
}
```

**Debug:**
```bash
# See task graph
turbo run build --graph

# Run specific package
turbo run build --filter=web
```

#### Parallel Task Failures
```bash
# If parallel tasks fail randomly:
# 1. Check for shared state (files, ports)
# 2. Run sequentially to isolate
turbo run build --concurrency=1
```

### Stripe Integration Issues

#### Webhook Failures
```bash
# Start Stripe webhook listener
pnpm stripe:listen

# Check webhook logs in Stripe Dashboard
# Common issues:
# 1. Wrong webhook secret in .env
# 2. Event type not handled
# 3. Handler throws before acknowledging
```

**Debug pattern:**
```typescript
// In webhook handler, always acknowledge first
export async function POST(request: Request) {
  const body = await request.text();
  const sig = request.headers.get('stripe-signature');

  try {
    const event = stripe.webhooks.constructEvent(body, sig!, webhookSecret);

    // Acknowledge immediately
    // Process async if needed
    switch (event.type) {
      case 'checkout.session.completed':
        // Handle...
        break;
    }

    return new Response('OK', { status: 200 });
  } catch (err) {
    console.error('Webhook error:', err);
    return new Response('Webhook Error', { status: 400 });
  }
}
```

---

## Debugging Workflow

### Phase 1: Root Cause Investigation

**BEFORE any fix:**

1. **Read error messages carefully**
   - Stack traces completely
   - Line numbers, file paths
   - Don't skip warnings

2. **Reproduce consistently**
   - Exact steps?
   - Every time or intermittent?

3. **Check recent changes**
   ```bash
   git diff HEAD~5
   git log --oneline -10
   ```

4. **Gather evidence in multi-component systems**
   ```
   For EACH component boundary:
     - Log what enters
     - Log what exits
     - Verify env/config
   ```

**Reference**: [systematic-debugging/SKILL.md](systematic-debugging/SKILL.md)

### Phase 2: Pattern Analysis

1. **Find working examples** in same codebase
2. **Compare** against references (read completely, don't skim)
3. **Identify differences** (list all, don't assume "can't matter")

### Phase 3: Hypothesis Testing

1. **Form single hypothesis**: "I think X because Y"
2. **Test minimally**: Smallest possible change
3. **Verify**: Yes → Phase 4, No → New hypothesis

### Phase 4: Implementation

1. **Create failing test** (if possible)
2. **Implement single fix** (no "while I'm here")
3. **Verify fix** (tests pass, no regressions)
4. **If 3+ fixes failed**: Question the architecture

---

## Quick Reference Commands

### Makerkit Stack

```bash
# Database
pnpm supabase:web:start     # Start local Supabase
pnpm supabase:web:reset     # Reset and remigrate
pnpm supabase:web:typegen   # Regenerate types
pnpm supabase:web:diff      # See pending changes

# Drizzle
pnpm drizzle:pull           # Pull schema from DB
pnpm drizzle:studio         # Open Drizzle Studio

# Build
pnpm typecheck              # TypeScript check
pnpm lint                   # ESLint
pnpm build                  # Full build
turbo run build --force     # Force rebuild

# Stripe
pnpm stripe:listen          # Start webhook listener
```

---

## Red Flags - STOP

If you catch yourself:
- "Quick fix for now, investigate later"
- "Just try changing X and see"
- "I don't fully understand but this might work"
- Proposing solutions before tracing data flow
- **Already tried 2+ fixes** → Question architecture

**ALL of these mean: STOP. Return to Phase 1.**

---

## Sub-Skills Reference

| Sub-Skill | When to Use | Link |
|-----------|-------------|------|
| **systematic-debugging** | Any bug - start here | [systematic-debugging/SKILL.md](systematic-debugging/SKILL.md) |
| **root-cause-tracing** | Deep in call stack | [root-cause-tracing/SKILL.md](root-cause-tracing/SKILL.md) |
| **verification-before-completion** | Before claiming "fixed" | [verification-before-completion/SKILL.md](verification-before-completion/SKILL.md) |
| **defense-in-depth** | Adding validation after fix | [defense-in-depth/SKILL.md](defense-in-depth/SKILL.md) |

---

## Success Criteria

A debugging session is complete when:
- Root cause identified (not just symptom)
- Fix addresses root cause
- Tests pass (new + existing)
- No regressions introduced
- Evidence gathered before claiming success
