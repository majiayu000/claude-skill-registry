---
name: github-controller
description: Controller skill for proactive GitHub automation. Run as a long-lived controller session, continuously consume events from HOLON_CONTROLLER_EVENT_CHANNEL, decide whether to run issue solve, PR review, PR fix, or no-op, then execute using existing GitHub skills.
---

# GitHub Controller Skill

Use this skill when running in proactive `holon serve` mode.

## Purpose

You are the decision layer for a persistent controller session.

Event stream input:

- `HOLON_CONTROLLER_EVENT_CHANNEL`: newline-delimited JSON events (required)
- `HOLON_CONTROLLER_EVENT_CURSOR`: byte offset cursor file (required)

Controller state:

- `HOLON_CONTROLLER_SESSION_STATE_PATH`: path to session metadata JSON (required)
- `/holon/state/controller-memory.md`: persistent controller memory across events/runs

## Required behavior

1. Start/continue a long-running loop:
   - Read current cursor offset from `HOLON_CONTROLLER_EVENT_CURSOR` (default `0` if missing).
   - Read new bytes from `HOLON_CONTROLLER_EVENT_CHANNEL` from that offset.
   - Split complete JSONL lines; for each parsed event, process sequentially.
   - After each successfully handled event, persist updated cursor offset immediately.
2. For each event, decide one of:
   - `no-op`
   - `issue-solve`
   - `pr-review`
   - `pr-fix`
3. If action is selected, invoke exactly one of these skills:
   - `github-issue-solve`
   - `github-review`
   - `github-pr-fix`
4. Maintain `summary.md` as rolling controller status with latest decision:
   - event type
   - decision
   - executed skill or why skipped
5. Update persistent controller memory:
   - Read `/holon/state/controller-memory.md` if present.
   - Write updated memory to `/holon/state/controller-memory.md`.
   - Keep it concise (priorities, open threads, recent outcomes), not full transcripts.
6. Keep session metadata in `HOLON_CONTROLLER_SESSION_STATE_PATH`:
   - Persist the current Claude session id as `session_id`.
   - Update metadata on startup and after notable state transitions.
7. Idle behavior:
   - If no new complete line is available, sleep briefly and continue polling.
   - Do not terminate only because there is no event right now.

## Decision guidance

- For issue events (`github.issue.*` or `github.issue.comment.*`), choose `issue-solve` when implementation work is requested.
- For PR opened/reopened/synchronize, prefer `pr-review`.
- For PR review changes requested or explicit fix requests in comments, prefer `pr-fix`.
- If event is irrelevant, duplicated, or lacks enough context, choose `no-op`.

Do not hard fail only because action is not required. `no-op` is a valid result.

## Notes

- Event channel data is append-only JSONL. Treat malformed trailing partial lines as incomplete and wait for more data.
- Cursor updates must be monotonic and durable to avoid replay loops after restart.
- Prefer idempotent behavior when the same event appears again.
