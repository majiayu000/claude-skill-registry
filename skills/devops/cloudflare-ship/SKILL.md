---
name: cloudflare-ship
description: Cloudflare shipping gate for Workers, Pages, KV, R2, D1, Queues, Durable Objects, routes, bindings, and edge config. Use when releasing to Cloudflare and you want a provider-specific read on binding mistakes, env drift, route blast radius, cache surprises, rollback realism, or platform-specific production risks.
user-invocable: true
argument-hint: "[worker, pages app, route, or Cloudflare release]"
---

Read `../_house-style/house-style.md` before starting.

## Anchor phrases

- Edge deploys fail fast and fail weird.
- A missing binding is a production outage wearing a config badge.
- If the route is wrong, the code quality does not matter.
- No rollback story means you are testing in public.

## What to interrogate

### 1. Deployment surface

State exactly what is shipping:
- Worker
- Pages app
- route change
- KV/R2/D1/Queue/Durable Object config
- secrets or env vars

### 2. Binding realism

Check every runtime dependency:
- bindings exist
- names match code
- prod and preview are not drifting
- secrets are not assumed to exist magically

### 3. Route and traffic blast radius

Ask:
- which hostname/path gets this code?
- what traffic moves immediately?
- can the old path still serve if this goes bad?

### 4. Data and state risks

Review:
- KV consistency assumptions
- D1 migration safety
- Durable Object compatibility
- Queue retry/idempotency behavior
- cache invalidation and stale edge responses

### 5. Rollback honesty

Name the real rollback:
- version rollback
- route rollback
- binding rollback
- schema/data incompatibility that makes rollback fake

## Output format

### Cloudflare release surface

What is actually changing.

### Platform blockers

File/config, failure mode, fix.

### Binding and route audit

What can break due to config, routes, or edge state.

### Rollback reality

How to back out. If rollback is not truly safe, say so.

### Verdict

- **Safe to deploy**
- **Fix before deploy**
- **Cloudflare red flag**
