---
name: localsetup-backlog-and-reminders
description: "Record deferred ideas, to-dos, and reminders (with optional due date or 'whenever'); show due/overdue when user starts a session or asks. Use when user says 'add to backlog', 'remind me', 'I'll do this later', 'what's due?', 'show my backlog', 'start my session', or wants to capture ideas for later."
metadata:
  version: "1.1"
---

# Backlog and reminders

**Purpose:** Let users record things they want to do later (repo features, tasks, free-form reminders) with an optional due date or no date ("whenever"). Surfaces due and overdue items when they start a session or ask. AI condenses free-form input into clear, actionable backlog items.

## When to use this skill

- User wants to record an idea, to-do, or reminder for later (with or without a date).
- User says "add to backlog", "remind me", "I'll do this later", "save this for later", "don't have time now", "set a reminder", "what's on my backlog?", "what's due?", "show my backlog", "start my session", "what should I work on?".
- User gives free-form text that should become one or more concrete backlog items.

## When not to use

- User names a different skill or tool (e.g. external Todoist, Apple Reminders). Use what they asked for.
- Simple one-off reminder at a specific time with no need to store in repo: you can still add it to the backlog with that date.

## Backlog file location

- Prefer: `_localsetup/backlog.md` (when the framework is deployed and `_localsetup/` exists).
- Fallback: `BACKLOG.md` at repo root.
- If the file does not exist, create it with the structure below.

## File format (backlog.md / BACKLOG.md)

Use Markdown with these sections. Preserve any extra sections or comments the user (or you) added.

```markdown
# Backlog

*Last updated: YYYY-MM-DD*

## Overdue
- [ ] Short title (due: YYYY-MM-DD) optional note
## Due soon (next 7 days)
- [ ] Short title (due: YYYY-MM-DD) optional note
## No date (whenever)
- [ ] Short title - optional note
## Done
- [x] Short title (done: YYYY-MM-DD)
```

- **Overdue:** Items with `due: YYYY-MM-DD` where date is before today.
- **Due soon:** Items with a due date in the next 7 days (today inclusive).
- **No date (whenever):** Items with no due date; do when convenient or when user asks "what should I work on?".
- **Done:** Completed items; move here when user marks done; optional to trim old entries periodically.

Use today's date in the repo's normal timezone (or ask once if ambiguous). For "due soon" classification, compute from the same timezone.

## Adding items

1. **Parse user input:** Extract one or more distinct ideas, tasks, or reminders. If the user gives a long paragraph, condense into 1–3 clear items with short titles and optional notes.
2. **Due date:** If the user gives a date or time ("next Friday", "March 15", "in two weeks"), resolve to YYYY-MM-DD and put the item in the right section (or create Overdue/Due soon/No date). If no date, put in "No date (whenever)".
3. **Write:** Append (or insert) each new item in the correct section. Update "Last updated" at the top. Do not remove or reorder existing items unless the user asks (e.g. "remove X", "mark Y done").
4. **Confirm:** Reply briefly with what was added and, if applicable, the due date.

## Showing the backlog (session start or on demand)

When the user asks to "start my session", "what should I work on?", "what's due?", "show my backlog", or when they begin a session and you have a habit of surfacing backlog:

1. Read the backlog file (create empty structure if missing).
2. Summarize in this order:
   - **Overdue:** List items; say they are past due.
   - **Due soon:** List items and due dates.
   - **No date:** Give the count and optionally 1–2 example titles; say they can ask to "show full backlog" or "work on something from backlog".
3. Suggest one next step (e.g. pick an overdue item, or "pick one from whenever").
4. Keep the summary short (bullet list plus one line of guidance).

If the file is empty or has no due/overdue items, say so and offer to add something ("Want to add an item or a reminder?").

## Marking done / removing

- **Mark done:** When user says "mark X done", "completed X", "did X": move that item from its current section to "Done" and add `(done: YYYY-MM-DD)`. Confirm.
- **Remove:** When user says "remove X", "delete X from backlog": delete that line from the file. Confirm.

## Condensing free-form input

When the user dumps a long idea or list:

- Split into discrete items (one actionable unit per bullet).
- Give each a short title (few words); put detail in a note after the title or in parentheses.
- If they mention a date for part of it, attach that date to the relevant item only.
- If nothing has a date, put all in "No date (whenever)".

Example: "I want to add a dark mode toggle and also fix the login bug by next week, and someday refactor the API layer" → three items: (1) "Add dark mode toggle" (whenever), (2) "Fix login bug" (due: next week), (3) "Refactor API layer" (whenever).

## References

- Backlog file: `_localsetup/backlog.md` or repo root `BACKLOG.md`.
- No external services required; everything is file-based and git-friendly.
