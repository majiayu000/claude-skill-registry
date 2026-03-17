---
name: sync
description: Real-time sync with Supabase, Loro CRDT, and IndexedDB. Use when working on files in src/lib/sync/.
---

# Sync Guidelines

## Core Principles

1. **Server is source of truth** - IndexedDB is a cache
2. **All ops kept forever** - no pruning, enables full audit trail
3. **Shallow snapshots for fast start** - performance only, not compaction
4. **Encryption at rest** - server sees encrypted blobs + plaintext version metadata

## Persistence Flow

| Event            | IndexedDB              | Server                    |
| ---------------- | ---------------------- | ------------------------- |
| Local change     | **Immediate**          | **Throttled** (~2s)       |
| Tab hidden/close | Immediate              | Flush pending             |
| Cold start       | Load snapshot → usable | Background sync           |

## Critical Rules

1. **IndexedDB writes immediate** - crash safety
2. **Server pushes throttled** - use `lodash-es` throttle, ~2s
3. **Encrypt before storage** - never plaintext in IndexedDB or server
4. **Version vector plaintext** - enables server filtering without decryption
5. **`has_unpushed` flag critical** - server must send ops (not snapshot) if client has local changes
6. **Flush on visibility change** - don't lose data on tab switch

## Key Details

- loro-mirror auto-commits on `setState()` - no manual debouncing
- `subscribeLocalUpdates` fires after each commit with binary update
- Snapshot refresh: ops > 1000 OR bytes > 1MB (not time-based)

## Conflict Resolution

Loro handles automatically: last-write-wins per field, set union for arrays.

## UI States

- **Saved** - all pushed
- **Saving...** - pending in buffer
- **Offline** - can't reach server
