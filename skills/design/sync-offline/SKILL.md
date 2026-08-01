---
name: sync-offline
description: 'Implement offline-first sync for the widget host app: caching, sync
  queues, conflict resolution, background refresh, and retry policies. Use when designing
  local persistence, background sync workers,'
---

---
name: sync-offline
description: Implement offline-first sync for the widget host app: caching, sync queues, conflict resolution, background refresh, and retry policies. Use when designing local persistence, background sync workers, or reconciling local/remote data.
---

# Sync Offline

## Overview

Provide a predictable offline-first sync pipeline for widgets that must appear immediately and reconcile later.

## Core components

- Local cache/read model
- Outbound sync queue
- Conflict detection and resolution policy
- Background refresh worker

## Definition of done (DoD)

- App works fully offline with local data
- Sync queue persists across app restarts
- Retry policy with exponential backoff implemented
- Conflicts detected and surfaced (not silently overwritten)
- Sync status visible to user (last sync time, pending count)
- Network calls never block UI thread

## Workflow

1. Decide the local persistence model (cache vs source of truth).
2. Define the sync queue and retry policy.
3. Add conflict detection (version, timestamp, or hash).
4. Implement background refresh with backoff and connectivity checks.
5. Surface sync state to the UI (last sync time, errors).

## Guidance

- Prefer idempotent sync operations.
- Keep queue items small and serialize minimal payloads.
- Never block UI on network calls.

## References

- `references/cache-strategy.md` for cache policies.
- `references/sync-queue.md` for queue structure and retry rules.
- `references/conflict-resolution.md` for resolution patterns.
