---
name: 10-init-session-150
description: "[10] INIT. Session-start routine for this project. Use when beginning a new session or onboarding to this repo to load AGENTS.md, MEMORY.md and core project context (README), then summarize context and confirm readiness."
---

# Init-Session 150 Protocol

## Primary workflow

1. Read `AGENTS.md` in the repo root.

2. Read `MEMORY.md` in the repo root.
   - Load Long-Term Memory protocols first.
   - Check Lessons (Inbox) and Short-Term for active items.
   - Treat Session State as volatile; update it only after confirming with the user.

3. Read core project context files (if present):
   - `README.md` for project overview and commands.

4. Summarize in 5-8 bullets:
   - Most relevant protocols that will affect the upcoming work.
   - Any active lessons or warnings.
   - Key project constraints (tests, tools, conventions).

5. Ask for confirmation before making changes:
   - Confirm the planned next steps.
   - Ask whether to update or clear Session State.

## Notes

- If any file is missing, state it briefly and proceed with what is available.
- Keep the summary concise; focus on constraints that change behavior.
