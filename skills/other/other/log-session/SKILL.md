---
name: log-session
description: Log entries to the current learning session. Use mid-session to save progress, capture concepts learned, or record corrections. Triggers on "log this", "save progress", "record what we learned".
model: claude-haiku-4-5-20251001
allowed-tools: Read, Write, Glob
---

Log recent learning to the current session.

## Steps

1. Find active session in `.claude/learning-sessions/index.json`
   - If none: tell user to run `/start-session` first
2. Read the session file
3. Review conversation since session started (or last log)
4. Add entries per `references/entry-types.md`
5. Write updated session file
6. Confirm: "Logged X concepts, Y corrections, etc."

## Guidelines

- Keep entries atomic and concise
- Don't duplicate existing entries
- Capture misconceptions (valuable for review)
- Note elaborations (show deep understanding)
- Track confidence vs accuracy
