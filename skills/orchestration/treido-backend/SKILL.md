---
name: treido-backend
description: Backend orchestrator for Treido. Use to route data/auth/payments work to the right specialist (Supabase, auth, Stripe, caching/Next.js server patterns).
---

# treido-backend

This is a routing/orchestration skill. It does not duplicate specialist guidance.

## Use These Specialists

- Next.js server patterns + caching rules: `treido-nextjs-16`
- Supabase/Postgres schema + performance: `treido-supabase`
- Supabase Auth + session patterns: `treido-auth-supabase`
- Stripe integration/webhooks: `treido-stripe`
- Global pause conditions / PII rules: `treido-rails`

## Output Format

```md
## Specialist
- <which skill is primary and why>

## Plan
- <2–6 bullets>

## Risks
- <auth/rls/idempotency/caching pitfalls>
```
