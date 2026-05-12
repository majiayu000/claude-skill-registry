# Gastown Origin: Mail Async

## Where This Comes From

The mail-async skill adapts Gastown's filesystem-based message passing system. In the original Gastown Go codebase, agents communicate by writing JSON files to per-agent directories. The mayor sends work assignments, polecats send completion reports, and the witness sends health escalations -- all through the filesystem.

## Key Mapping: Gastown to Skill-Creator

| Gastown Concept | Mail-Async Equivalent | Adaptation Notes |
|----------------|---------------------|------------------|
| Agent mail directory | `.chipset/state/mail/{agent-id}/` | Same per-agent directory pattern |
| Message file naming | `{timestamp}-{from-agent}.json` | Preserves chronological ordering |
| Work assignment message | `type: "work_assignment"` | Formalized as typed message |
| Completion report | `type: "completion_report"` | Explicit lifecycle tracking |
| Directory polling | `readdir()` + filter + sort | Same scan pattern, TypeScript async |
| File-based durability | Atomic write-then-rename | POSIX atomic rename preserved |

## Design Decisions

### Why Write-Once Read-Many

Gastown treats messages as facts -- once a message is sent, its content is immutable. This makes the mail directory an append-only log that git can track meaningfully. The only mutable field is `read`, which tracks processing state without altering the message content.

### Why Directory-Per-Agent

Each agent owns its mailbox directory. This provides natural isolation:
- Agents only scan their own directory (no cross-agent interference)
- Concurrent senders to the same agent are safe (unique filenames)
- Directory listing is the only "query" needed (no index files)
- Cleanup and archival operate on a single directory

### Why Timestamp-Based Filenames

Using ISO 8601 timestamps in filenames gives chronological ordering for free. A simple `readdir().sort()` returns messages in send order. The sender ID suffix prevents collisions when two agents send to the same recipient at the same timestamp.

## What Changed From Gastown

1. **Language:** Go to TypeScript -- `fs.promises` replaces Go's `os` package
2. **Message schema:** Formalized with typed fields (was loosely structured in Gastown)
3. **Read tracking:** Explicit `read` boolean (was implicit in Gastown's processing)
4. **Archival:** 24-hour automatic archival (Gastown relied on git history for old messages)
5. **Priority field:** Added `urgent`, `normal`, `low` levels (Gastown treated all messages equally)
6. **Serialization:** Sorted-key JSON for git-friendly diffs (consistent with beads-state)
