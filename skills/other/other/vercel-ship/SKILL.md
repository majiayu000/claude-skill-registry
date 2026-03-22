---
name: vercel-ship
description: Vercel shipping gate for Next.js apps, Vercel Functions, Edge Middleware, env vars, preview-to-production promotion, domains, and rollout safety. Use when releasing on Vercel and you want a provider-specific read on runtime mismatch, env drift, routing surprises, caching behavior, or rollback realism.
user-invocable: true
argument-hint: "[Next.js app, Vercel deployment, middleware change, or Vercel release]"
---

Read `../_house-style/house-style.md` before starting.

## Anchor phrases

- Preview green does not mean production safe.
- Runtime mismatch is a deploy bug wearing a framework badge.
- If env vars drift, your route tests are fiction.
- Middleware, caching, and rewrites can turn a tiny change into a site-wide outage.

## What to interrogate

### 1. Release surface

State what is shipping:
- Next.js app or frontend deploy
- Vercel Function or Edge Function
- middleware, redirects, rewrites, or headers change
- domain, preview, or production config change
- env vars, secrets, or build settings change

### 2. Runtime and config realism

Check:
- Node versus Edge runtime assumptions
- env var completeness across preview and production
- build output and framework config assumptions
- image, ISR, or cache behavior
- region/runtime choices that affect live behavior

### 3. Routing and traffic risk

Review:
- middleware blast radius
- rewrite and redirect correctness
- auth/session assumptions across edge and server paths
- custom domain and preview-to-production behavior
- static versus dynamic route expectations

### 4. Rollout and rollback

Ask:
- is this a straight production deploy or a promote flow?
- can the prior deployment be restored cleanly?
- do data or env changes make rollback fake?
- what breaks first if middleware, cache, or runtime assumptions are wrong?

## Output format

### Vercel release surface

What actually changes in the platform.

### Platform blockers

Runtime, env, routing, caching, or domain blockers.

### Rollout risk

What fails during deploy, traffic cutover, or rollback.

### Mitigation and rollback plan

Concrete safer rollout steps.

### Verdict

- **Safe to release**
- **Fix before release**
- **Vercel release red flag**
