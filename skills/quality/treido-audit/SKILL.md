---
name: treido-audit
description: Review code for Treido project compliance, security issues, and best practices. Use when reviewing changes, checking for violations of project rules, or validating code before merge. Triggers include code review requests, security audits, pre-merge validation, or checking compliance with AGENTS.md rules.
deprecated: true
---

# Treido Audit

> Deprecated (2026-01-29). Use `treido-orchestrator` (bundle-based) + specialist auditors `treido-audit-*`, then validate with `treido-verify`.

## Quick Start

1. Identify scope (changed files, specific paths, or full codebase)
2. Run automated checks: `pnpm -s typecheck && pnpm -s lint && pnpm -s styles:gate`
3. Review findings against rules below
4. Report issues with severity and fix suggestions

## Automated Verification

Run these on every change:

```bash
# Type checking
pnpm -s typecheck

# Linting
pnpm -s lint

# Tailwind v4 compliance
pnpm -s styles:gate
```

For high-risk changes (auth, payments):

```bash
# E2E smoke tests
REUSE_EXISTING_SERVER=true pnpm -s test:e2e:smoke

# Unit tests
pnpm -s test:unit
```

## Critical Rules (Must Pass)

### 1. No Secrets/PII in Logs
```tsx
// ❌ CRITICAL - leaks sensitive data
console.log('User:', user);
console.log('Token:', accessToken);
console.log('Headers:', request.headers);

// ✅ CORRECT
console.log('Processing user:', user.id);
console.log('Request completed');
```

### 2. Tailwind v4 Compliance
```tsx
// ❌ FAIL styles:gate
className="bg-[#ff0000]"    // arbitrary color
className="p-[13px]"        // arbitrary spacing
className="bg-gradient-to-r" // gradient
className="text-blue-500"   // palette color

// ✅ PASS
className="bg-destructive"  // semantic token
className="p-4"             // standard spacing
className="text-foreground" // semantic token
```

### 3. i18n Coverage
```tsx
// ❌ FAIL - hardcoded user-facing string
<p>Welcome to Treido</p>
<button>Add to Cart</button>

// ✅ PASS - using next-intl
<p>{t('welcome')}</p>
<button>{t('addToCart')}</button>
```

### 4. Caching Rules
```tsx
'use cache';

// ❌ FAIL - forbidden in cached functions
const session = await cookies();
const ua = await headers();

// ✅ PASS - pass data as parameters
export async function getData(userId: string) {
  cacheLife('hours');
  cacheTag('data', `user:${userId}`);
  // ...
}
```

### 5. File Boundaries
```tsx
// ❌ FAIL - cross-route import
// In app/[locale]/(main)/products/_components/card.tsx
import { SellerBadge } from '@/app/[locale]/(seller)/dashboard/_components/badge';

// ✅ PASS - use shared components
import { SellerBadge } from '@/components/shared/seller-badge';
```

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| **Critical** | Security risk, data leak, broken functionality | Block merge |
| **High** | Violates core rules, causes bugs | Fix before merge |
| **Medium** | Suboptimal pattern, minor violation | Fix soon |
| **Low** | Style preference, suggestion | Consider |

## Audit Report Format

```markdown
## Audit: [scope]

### Summary
- Files reviewed: X
- Critical: X
- High: X
- Medium: X
- Low: X

### Critical Issues
1. **[file:line]** - Description
   - Problem: [what's wrong]
   - Impact: [security/performance/correctness]
   - Fix: [specific suggestion]

### High Issues
...

### Verification
- [ ] `pnpm -s typecheck` passes
- [ ] `pnpm -s lint` passes
- [ ] `pnpm -s styles:gate` passes
- [ ] No secrets in logs
- [ ] All user strings use next-intl
```

## Common Violations

### Supabase Query Patterns
```tsx
// ❌ High - select(*) in hot paths
const { data } = await supabase.from('products').select('*');

// ✅ PASS - explicit projection
const { data } = await supabase
  .from('products')
  .select('id, title, price, images');
```

### Client Component Boundaries
```tsx
// ❌ Medium - unnecessary client boundary
'use client';
export function StaticCard() {
  // No interactivity, no hooks - shouldn't be client
  return <div>Static content</div>;
}

// ✅ PASS - server component (default)
export function StaticCard() {
  return <div>Static content</div>;
}
```

### Stripe Webhook Security
```tsx
// ❌ Critical - missing signature verification
export async function POST(req: Request) {
  const event = await req.json(); // NO! Must verify signature
}

// ✅ PASS - signature verified
export async function POST(req: Request) {
  const body = await req.text();
  const sig = headers.get('stripe-signature');
  const event = stripe.webhooks.constructEvent(body, sig!, secret);
}
```

## Quick Audit Scripts

Run the full audit pipeline:

```bash
# Run all automated checks
pnpm -s typecheck && pnpm -s lint && pnpm -s styles:gate

# Check for dead code (weekly)
pnpm -s knip

# Check for duplicate dependencies
pnpm -s dupes
```

## References

**For Tailwind rules:** See treido-frontend skill → references/tailwind.md
**For caching rules:** See treido-backend skill → references/caching.md
**For security checklist:** See [references/security.md](references/security.md)
