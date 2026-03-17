---
name: end-session
description: End the current learning session. Use when done studying to generate summary, update learning plan, and log final entries. Triggers on "end session", "done learning", "finish studying", "wrap up".
model: claude-haiku-4-5-20251001
allowed-tools: Read, Write, Glob
---

End the current learning session.

## Steps

1. Find active session in `.claude/learning-sessions/index.json`
   - If none: tell user there's no active session
2. Read the session file
3. Review conversation since last log, add remaining entries
4. Generate 1-2 sentence summary
5. Update session file:
   - `ended`: current ISO timestamp
   - `status`: `"completed"`
   - `summary`: generated summary
6. Update index.json status
7. Update learning plan (`.claude/learning-sessions/learning-plan.json`):
   - Set `last_covered` to today
   - Add session ID to topic's `sessions` array
   - Adjust proficiency per `references/proficiency.md`
   - Update queue: remove covered, add discovered topics
   - Handle struggles per `references/proficiency.md`

## Report

- Confirm session ended
- Show summary
- Show entries logged (by type)
- Show proficiency updates
- If review: show retention score and calibration
- Suggest next topic from queue
