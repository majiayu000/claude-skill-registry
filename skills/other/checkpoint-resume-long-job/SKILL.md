---
name: checkpoint-resume-long-job
description: "Persist progress for long-running jobs (batched LLM calls, large ingestions, multi-hour syncs) so that a context reset, crash, or interrupt doesn't lose work. Use whenever a job iterates over N items and completing item K matters independently. Provides a resumable.mjs library pattern plus the skill's invocation heuristics."
format: 2025-10-02
version: 1.0.0
status: ACTIVE
updated: 2026-04-17
triggers:
  - a job iterates over N items and completing item K matters independently
---

# Checkpoint & Resume for Long Jobs

Any job that takes longer than 5 minutes and iterates over N independent
items should checkpoint its progress. Context can reset, processes can
crash, users can Ctrl-C. A re-run shouldn't redo completed work.

## Triggers

Activate when a job:

- Iterates over **≥ 20 items** AND each item takes **≥ 5 seconds**, OR
- Is expected to run **≥ 10 minutes** total, OR
- Calls **external APIs** with rate limits or cost per call (LLM, HTTP), OR
- Is **not naturally idempotent** at the whole-job level

## Shape

The simplest checkpoint is a file listing completed item IDs. On job start:
read the file; on each item completion: append its ID; on job restart: skip
any ID in the file.

### Reference library: `tools/checkpoint-resume/resumable.mjs`

```javascript
import { processBatches } from './tools/checkpoint-resume/resumable.mjs';

await processBatches({
  items: [...1713 lessons...],
  keyFn: l => l.id,
  checkpointFile: '.planning/sessions/tiebreaker-checkpoint.jsonl',
  batchSize: 5,
  async handler(batch) {
    // your per-batch work
    return batch.map(l => ({ id: l.id, status: 'done' }));
  },
  onProgress({ completed, total, skipped }) {
    console.error(`${completed + skipped}/${total} (${skipped} resumed)`);
  },
});
```

On first run, processes all items and appends IDs to the checkpoint file.
On resume, reads the file and skips already-processed items.

## Checkpoint Formats

| Format | When |
|--------|------|
| Append-only JSONL | Most jobs. One line = one completed item. Easy to read, easy to resume. |
| Database column | When items already live in a DB — add `processed_at TIMESTAMP` and `WHERE processed_at IS NULL` at start. |
| Snapshot file | When checkpoint state is a complex structure (progress trees, partial outputs). Write a whole-state JSON every N items. |

Prefer append-only JSONL. Crash-safe by design.

## The Trade-off

Checkpointing adds file I/O per item. Usually negligible compared to the work
itself. The cost of NOT checkpointing, however, is:

- Wasted LLM calls (money)
- Wasted API quota
- User has to manually figure out where the job stopped
- Worst case: job silently half-completes and corrupts DB state

## Anti-patterns

- **Checkpointing to in-memory arrays only.** If the process dies, so does
  the checkpoint.
- **Non-atomic writes.** Use append-only (fsync-safe) or write-temp-then-rename.
- **Checkpoint file in `/tmp`.** It WILL get cleaned up. Put it under
  `.planning/sessions/` or a project-local cache dir.
- **Not logging the checkpoint file path at start.** If the user needs to
  resume manually, they need to know where to look.

## Invocation Heuristic

Before starting any long job, ask:

- "If my process dies halfway, is the user's work gone?"
- "If I'm Ctrl-C'd at item 500 of 1000, can I pick up at 501?"
- "Does item K depend on item K-1, or are they independent?"

If answers are "yes, no, independent" → use checkpointing.

## Example — LLM Tiebreaker (v1.49 release-history work)

Situation: 681 lessons to classify via `claude -p`, 5 per batch, ~30 sec per
batch. Total: ~70 minutes. No checkpointing was in place.

Worst-case loss: 136 wasted LLM calls at batch 137 if context broke.
Actual loss: 0 — but only because the run happened to complete first time.

Fix: wrap the batch loop in `processBatches()` from `resumable.mjs`.
On resume, only unprocessed lessons get classified.

## Related

- `session-observatory-live` — log a `checkpoint` event at every completion
- `decision-framework-invoker` — long jobs often produce irreversible state
- `batch-rewrite-pattern` — similar batching shape, different domain
