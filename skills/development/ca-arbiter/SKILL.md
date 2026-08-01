---
name: ca-arbiter
description: Exit maintainer dev mode — restore orchestration, remove the dev marker, log the exit.
argument-hint: (none)
---

# /ca-arbiter — restore orchestration

The exit door for `/ca-dev`. No-op if dev mode is not active.

## Flow

1. **Log exit** — append to `<project-root>/.codearbiter/overrides.log` (append-only, `>>`):

   ```
   [ISO-8601 timestamp] | BY: <email> | DEV: exit
   ```

2. **Marker** — remove `<project-root>/.codearbiter/.markers/dev-active`.
3. **Resume** — re-present the startup state (stage, blocking `CONFIRM-NN`, in-flight tasks) and
   await a slash command. Orchestration, routing, and all gates are back in force.

## Hard gate

MUST write the `DEV: exit` line to `overrides.log` and remove the `dev-active` marker before resuming
orchestration — the exit is on the audit trail like the entry. MUST NOT rewrite or truncate
`overrides.log` — the append-only rule has no dev exception, on entry or exit. If a prior session
ended mid-dev, SessionStart has already appended the synthetic `BY: session-cleanup | DEV: exit` close
line and cleared the marker (`session-start.py`, observability-001). In that case MUST NOT write a
second `DEV: exit` for that orphaned entry — the close is already on the trail.

Session-scoped clearing (#271): SessionStart's synthetic close is now conditional on the marker
plausibly being abandoned rather than owned by a different, still-live session — it will NOT clobber
another concurrently-running session's live `/dev` marker or write a false `DEV: exit` for it.
`/ca-arbiter` remains the ONLY way to cleanly close your OWN `/dev` session's audit pair; do not
rely on a future SessionStart to do it for you.
