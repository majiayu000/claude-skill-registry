---
name: daily-review
description: Complete daily journal review. Use at end of day or next morning to fill in journal sections, review highlights, and plan tomorrow. Triggers on "daily review", "end of day", "journal review", "what did I do today".
model: claude-haiku-4-5-20251001
allowed-tools: Bash(gh:*), Read, Write, Edit, Glob
---

Run the Daily Review Workflow. Keep it conversational - ask one thing at a time.

## Steps

1. **Get current date first**
   - Run `date +%Y-%m-%d` to confirm today's date
   - DO NOT assume the date - always verify

2. **Journal Entry Setup**
   - Check if today's entry exists (`my-vault/02 Calendar/YYYY-MM-DD.md`)
   - Create from template if not (see `references/template.md`)
   - If morning reviewing yesterday: use yesterday's date

3. **What Did I Work On?**
   - Pull GitHub commits: `gh search commits --author=TaylorHuston --committer-date=YYYY-MM-DD`
   - Summarize into meaningful bullets (not raw commit messages)
   - Ask: "Any other technical work? (studying, courses, side projects not on GitHub)"

4. **What Did I Do?**
   - Ask: "How about personal stuff? (errands, social, health, appointments, etc.)"

5. **Daily Highlight Check**
   - Review the day's highlight if set
   - Ask: "Did you accomplish your highlight? Want to carry it to tomorrow?"

6. **Quick Inbox Scan** (offer, don't force)
   - "Want me to check your inbox for anything to quickly process?"

7. **Tomorrow's Highlight** (offer, don't force)
   - "Do you know what tomorrow's focus should be?"

8. **Memory Capture Check**
   - Review the conversation for anything memory-worthy:
     - New preferences expressed
     - Corrections to how you understood something
     - Life/job updates
     - Workflow insights
     - Project decisions
   - If anything qualifies, create a memory file in `.claude/memories/`
   - Check if `about-taylor.md` needs updating (job status, current focus, etc.)
   - Do this silently unless there's something significant to confirm

Use bulleted lists in the journal.
