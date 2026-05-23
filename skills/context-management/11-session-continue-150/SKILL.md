---
name: 11-session-continue-150
description: "[11] CONTINUE. Resume an existing session. Use when continuing previous work to load AGENTS.md, MEMORY.md, and the chosen session log, then confirm readiness."
---

# Continue-Session 150 Protocol

## Primary workflow

1. Read `AGENTS.md` in the repo root.

2. Read `MEMORY.md` in the repo root.
   - Load Long-Term Memory protocols first.
   - Check Lessons (Inbox) and Short-Term for active items.
   - Session State is deprecated; do not use or update it.

3. Select the session log in `.sessions/SESSION_[date]-[name].md`.
   - Prefer explicit `session_name` from the user.
   - If not provided, choose the most recently modified log.
   - If no logs exist, switch to `10-session-new-150` and create a new session.

4. Read the selected session log.
   - Identify current state, open questions, and next steps.

5. Summarize in 5-8 bullets:
   - Most relevant protocols that will affect the upcoming work.
   - Active lessons or warnings.
   - The session log’s current status and next action.

6. Ask for confirmation before making changes:
   - Confirm the selected session log name.
   - Confirm the planned next steps.

## Notes

- If any file is missing, state it briefly and proceed with what is available.
- Keep the summary concise; focus on constraints that change behavior.
