---
name: 10-session-new-150
description: "[10] NEW. Start a NEW session for this project. Use when beginning a fresh task to load AGENTS.md, MEMORY.md, core project context (README), then create a NEW session log and confirm readiness."
---

# New-Session 150 Protocol

## Primary workflow

1. Read `AGENTS.md` in the repo root.

2. Read `MEMORY.md` in the repo root.
   - Load Long-Term Memory protocols first.
   - Check Lessons (Inbox) and Short-Term for active items.
   - Session State is deprecated; do not use or update it.

3. Read core project context files (if present):
   - `README.md` for project overview and commands.

4. **Auto-Detect & Create Session** (CRITICAL):
   - **If the user's intent is a clear NEW task** (e.g., "fix bug X", "implement feature Y", "investigate Z"):
     - **IMMEDIATELY generate** a descriptive `session_name` (e.g., `fix-time-picker-bug`).
     - **IMMEDIATELY create** the file `.sessions/SESSION_[date]-[name].md`.
     - **DO NOT ASK** for permission to create the session. Just do it.
   - **Ambiguity Check**: Only ask the user "New or Continue?" if the request implies continuity with the immediate prior context (e.g., "continue", "next step") and you are unsure.

5. Initialize the Session Log:
   - Insert structure: `## Meta`, `## Progress Log`, `## Investigations`, `## Decisions`, `## Next Steps`.
   - Log the initial User Request.

6. Summarize in 5-8 bullets:
   - Most relevant protocols that will affect the upcoming work.
   - Any active lessons or warnings.
   - Key project constraints (tests, tools, conventions).

7. present the Plan & Session:
   - State "Created session: `[session_filename]`".
   - Propose the plan for the task.
   - Ask for confirmation on the **Plan**, not the session creation.

## Notes

- If any file is missing, state it briefly and proceed with what is available.
- Keep the summary concise; focus on constraints that change behavior.
