---
name: convex-http-actions
description: Implement Convex HTTP actions and webhook endpoints with explicit validation, auth, and clear public/internal boundaries.
version: 1.0.0
metadata:
  author: agentforge
  source: waynesutton/convexskills
---

# Convex HTTP Actions

Use this when building webhooks, inbound HTTP integrations, or externally callable HTTP endpoints.

## Checklist

- validate payload shape and origin,
- keep secrets out of logs,
- use internal functions for follow-up mutations when appropriate,
- make retry behavior and idempotency explicit.

## Repo fit

- Prefer runtime HTTP channels in `packages/runtime/` for agent messaging flows.
- Use Convex HTTP actions for data-layer or webhook responsibilities, not as a substitute for the daemon.
