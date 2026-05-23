---
name: quick-journal
description: Quick update to today's journal without full review. Use when user wants to quickly log something they did, add a journal entry, or note an activity. Triggers on "log this", "add to journal", "I just did", "quick note".
model: claude-haiku-4-5-20251001
argument-hint: [what you did]
allowed-tools: Read, Edit, Glob
---

Add this to today's journal (`my-vault/02 Calendar/YYYY-MM-DD.md`):

$ARGUMENTS

## Steps

1. Read today's journal
2. Add as bullet under appropriate section:
   - "What Did I Do?" for personal activities
   - "What Did I Work On?" for technical/coding work
   - "What Did I Study?" for learning sessions, courses
3. If journal doesn't exist: create from template first

Keep it brief, just add the entry.
