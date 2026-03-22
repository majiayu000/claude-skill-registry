---
name: convex-cron-jobs
description: Schedule recurring Convex jobs safely using internal functions, batch processing, and observable retry-friendly patterns.
version: 1.0.0
metadata:
  author: agentforge
  source: waynesutton/convexskills and get-convex/convex-agent-plugins
---

# Convex Cron Jobs

Use this when adding recurring cleanup, sync, digest, monitoring, or maintenance jobs.

## Rules

- Schedule `internal.*` functions only.
- Keep jobs idempotent where possible.
- Batch work instead of scanning whole tables in one run.
- Make time-zone and schedule semantics explicit in docs or code comments.
