---
name: good-morning
description: Morning routine check-in. Use at start of day to review yesterday, set up today's journal, and check learning reviews due. Triggers on "good morning", "morning", "start my day", "what's on for today".
model: claude-haiku-4-5-20251001
allowed-tools: Bash(gh:*), Read, Write, Edit, Glob
---

Good morning! Run the morning check-in.

## Steps

1. **Get current date first**
   - Run `date +%Y-%m-%d` to confirm today's date
   - Calculate yesterday's date from this
   - DO NOT assume the date - always verify

2. **Check yesterday's journal** (`my-vault/02 Calendar/YYYY-MM-DD.md`)
   - If "What Did I Work On?" empty: offer to backfill from GitHub
   - If "What Did I Do?" empty: just note it

3. **Setup today's journal**
   - Check if today's entry exists
   - If not: create from template at `my-vault/09 System/Templates/Daily Template.md`
     - Note: Template uses Templater syntax - resolve `<% tp.date... %>` to actual dates
     - Set `created` and `modified` to today's date
   - Show today's highlight or ask: "What's your main focus today?"

4. **Check learning plan** (`.claude/learning-sessions/learning-plan.json`)
   - Find topics where `last_covered` + interval < today
   - If any due: "You have [topic] due for review"
   - Show next item in queue

5. **Quick status report**
   - Yesterday: Complete/Incomplete
   - Today's highlight: [highlight or "not set"]
   - Reviews due: [list or "none"]
   - Next in learning queue: [topic]

Keep it brief - quick morning orientation, not a deep dive.
