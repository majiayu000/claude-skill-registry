---
name: pm-ralph
description: Session capture — at the end of a session, capture what happened into structured session notes and update self/goals.md. The "put the room back in order" operation. Named for the habit of leaving a tidy workspace. Triggers on "/pm-ralph", "end session", "capture session", "session wrap-up", "what did we do today".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` for vocabulary.
Read `self/goals.md` for active threads to update.

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- If empty: capture the current session with auto-detection of what happened
- If summary text provided: use that text as the session summary (skip auto-detection)

**START NOW.**

---

## Philosophy

**Sessions without capture are sessions that never happened — for the next session.**

The Orient phase at session start reads self/goals.md and ops/reminders.md. If the end-of-session capture was skipped, the next session starts with stale goals and no record of what was accomplished. Over multiple sessions, this compounds: the PM agent loses track of which threads are progressing, which are stalled, and what was decided.

/pm-ralph is the closing ritual. It is fast — 5-10 minutes — and it prevents the most common PM system failure: context loss at session boundaries.

The name "ralph" is not an acronym. It refers to the habit of tidying a workspace before leaving: putting tools back where they belong, updating the status board, leaving notes for the next shift. In a PM system, that means: session notes written, goals updated, queue status current, and one line in the health log.

---

## What Gets Captured

### 1. Session Summary

A brief narrative of what happened this session:
- Which teams were deployed? With what mandate?
- What deliverables were received and processed?
- What decisions were created or updated?
- What was rejected and why?
- What remains incomplete?

### 2. Goals Update

Read self/goals.md. For each active thread:
- Did this session make progress? Update the thread.
- Was the thread completed? Mark complete, move to "Deferred" or remove.
- Did a new thread emerge? Add it.
- Was a thread stalled? Note the stall and reason.

### 3. Health Update

If this session involved sprint work with health metrics, add a line to ops/health/health-log.md.

### 4. Queue Update

Update queue.json with any pipeline state changes from this session.

### 5. Reminders Update

If any new standing directives emerged from this session (e.g., new enforcement rule, new team pattern), add to ops/reminders.md.

---

## Session Note Format

```markdown
---
date: YYYY-MM-DD
session_number: N
health_at_session_start: N/100
health_at_session_end: N/100
teams_deployed: []
decisions_created: []
decisions_updated: []
---

# Session N — YYYY-MM-DD

## What Happened

[2-4 sentences: what was the work, what teams ran, what was the outcome]

## Decisions Created

- [[decision-a]] — [one-line description]
- [[decision-b]] — [one-line description]

## Validation Status

- Validation block embedded in agent prompts: YES / NO
- Deliverables with full CLAIM/SOURCE/VALIDATION: N/N
- Deliverables rejected: N

## Open Threads Carried Forward

- [Thread A] — [where it stands]
- [Thread B] — [where it stands]

## Next Session Should Start With

[One specific recommendation for the next session's first action]
```

---

## Workflow

### 1. Auto-Detect Session Activity

```bash
# Find recently modified files to understand session scope
ls -lt decisions/ | head -20
ls -lt ops/observations/ | head -5
ls -lt ops/tensions/ | head -5
```

### 2. Draft Session Summary

Based on file modifications and conversation context, draft the session note.

### 3. Update Goals

Read self/goals.md. For each thread, determine the updated state and edit accordingly.

### 4. Write Session Note

Write to ops/sessions/session-YYYY-MM-DD.md using the session note format.

### 5. Update Health Log

```bash
# Append to health log if health changed this session
echo "| Sprint N | [before] | [after] | +N | [key change] |" >> ops/health/health-log.md
```

### 6. Confirm Completion

```
## Session Captured

Session note: ops/sessions/session-YYYY-MM-DD.md
Goals updated: self/goals.md
Health log updated: [yes/no]
Queue updated: [yes/no]

Active threads carried forward: N
New threads opened: N
Threads completed: N

Next session recommendation: [/pm-command or action]
```
