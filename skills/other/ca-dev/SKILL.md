---
name: ca-dev
description: Maintainer override — suspend orchestration to edit codeArbiter itself. Env-gated (CODEARBITER_DEV=1), entry/exit logged to overrides.log.
argument-hint: "[note]"
---

# /ca-dev — maintainer override

Suspends orchestration for working ON codeArbiter — skill, agent, command, and hook bodies,
`ORCHESTRATOR.md`, settings. Not for project work; for that, use the normal commands or
`/ca-override`.

## Flow

1. **Env gate** — check the `CODEARBITER_DEV` environment variable. Not set to `1` → refuse in one
   line ("dev mode requires CODEARBITER_DEV=1") and remain in orchestration. This keeps the mode a
   deliberate maintainer posture, not a casual bypass.
2. **Log entry** — detect identity from `git config user.email`; append to
   `<project-root>/.codearbiter/overrides.log` (append-only, `>>`):

   ```
   [ISO-8601 timestamp] | BY: <email> | DEV: enter | NOTE: <note or —>
   ```

3. **Marker** — drop `<project-root>/.codearbiter/.markers/dev-active` (gitignored UI flag).
4. **Mode** — plain, direct coding assistant: no routing, no skills, no gates, no `[CONFIRM-NN]`
   surfacing, no redirect. Persists until `/ca-arbiter` or a new session.

Note (#271): if another session starts in this repo while this marker is live, SessionStart no longer
unconditionally clears it out from under you — it is session-scoped now, so a concurrently-running dev
session's marker survives a different session's startup. See `/ca-arbiter` for the exit-path detail.

## Hard gate

MUST refuse without `CODEARBITER_DEV=1`. MUST write the `DEV: enter` log line before suspending
orchestration. Even in dev mode, `overrides.log` is never rewritten — the append-only rule has no
dev exception.

## When NOT to use

- Bypassing a single gate on project work → `/ca-override "reason"`.
- Asking a question → `/ca-btw`.
