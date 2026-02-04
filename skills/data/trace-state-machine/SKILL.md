---
name: trace-state-machine
description: Parse PRStatus, trace all state transitions across source files, and flag anomalies.
user-invocable: true
---

You are a state machine analyzer for the claude-code-reviewer project. Your job is to extract all PR status transitions from the codebase, build a complete transition graph, and flag issues.

## Step 1: Extract PRStatus Values

Read `src/types.ts` and extract all values from the `PRStatus` type union:
- `pending_review`, `reviewing`, `reviewed`, `changes_pushed`, `error`, `skipped`, `closed`, `merged`

## Step 2: Find All Transitions

Search across all files in `src/` for status transitions. Look for:
- `setStatus(` calls — the third argument is the new status
- `store.update(` calls with `status:` in the updates object
- Direct `status:` assignments in object literals (e.g., in `getOrCreate`, `migrateV1`)

For each transition found, record:
- **From** status (the status the PR must be in, inferred from surrounding conditionals/context)
- **To** status (the new status being set)
- **Trigger** (what causes the transition — e.g., "review started", "webhook closed event", "crash recovery")
- **File:Line** (exact source location)

### Key files to search:

- `src/reviewer/reviewer.ts` — review cycle transitions:
  - →skipped (draft, wip_title, diff_too_large — can happen from multiple states including after entering `reviewing`)
  - pending_review/changes_pushed/error/reviewed(new SHA)→reviewing (review started)
  - reviewing→reviewed (review completed)
  - reviewing→error (failure during any phase)
  - reviewed→changes_pushed (new SHA detected in `evaluateTransitions`)
  - skipped→pending_review (skip condition cleared in `evaluateTransitions`)
- `src/webhook/server.ts` — lifecycle events: any→closed, any→merged, any→skipped (converted_to_draft when skipDrafts enabled)
- `src/state/store.ts` — crash recovery: reviewing→pending_review; initial creation: →pending_review; V1 migration: →reviewed
- `src/reviewer/comment-verifier.ts` — reviewed→pending_review (when review/comment is deleted or dismissed)
- `src/state/cleanup.ts` — deletion of closed/merged/stuck-error entries (not a status change, but removes from state)
- `src/polling/poller.ts` — `reconcileClosedPRs()` performs direct transitions: any non-terminal→merged, any non-terminal→closed (reconciles state when PRs are closed/merged between poll cycles). Also calls `processPR` and `evaluateTransitions` which trigger transitions listed under reviewer.ts.
- `src/state/decisions.ts` — does not set status directly but gates which transitions can happen

## Step 3: Build Transition Table

Present all transitions as a markdown table:

| From | To | Trigger | File:Line |
|------|-----|---------|-----------|
| pending_review | reviewing | Review started | reviewer.ts:XX |
| reviewing | reviewed | Review completed | reviewer.ts:XX |
| ... | ... | ... | ... |

Also note transitions from "any" state (e.g., →closed, →merged from lifecycle events).

## Step 4: Validate the Graph

Check these invariants:

1. **Every status has at least one inbound transition** — some state must lead to it
2. **Non-terminal states have outbound transitions** — pending_review, reviewing, reviewed, changes_pushed, error, skipped should all have at least one way out
3. **Terminal states have no outbound transitions** — `closed` and `merged` should never transition to another status (cleanup deletes them, but doesn't change status)
4. **No orphan states** — every PRStatus value appears in at least one transition

## Step 5: Compare with Documentation

Read the documented state flow from `CLAUDE.md`:

```
pending_review → reviewing → reviewed → changes_pushed → (cycle)
                    ↓
                  error → retry (exponential backoff) or stuck (max retries)
Any → closed / merged (terminal)
Any → skipped (draft, WIP, diff_too_large) → pending_review (when cleared)
```

Flag any transitions found in code that are NOT in the documentation, and any documented transitions NOT found in code.

## Step 6: Flag Anomalies

Report any issues:
- Unreachable states (no inbound transition)
- Dead-end non-terminal states (no outbound transition)
- Undocumented transitions
- Missing documented transitions
- Status values in `PRStatus` that never appear in any transition

## Output Format

Use clear section headers and the markdown table for transitions. Prefix anomalies with ⚠. End with a summary verdict: whether the state machine is consistent with documentation.
