---
name: walkthrough
description: Present items one at a time for focused review. Use when user asks to "walk through", "step through", "present one by one", or needs to review a list interactively.
---

# Walkthrough

Interactive step-by-step presentation of any list of items.

## Protocol

Follow @context/workflows/ralph/review/chunked-presentation.md

## Execution

Based on ARGUMENTS and context:

### With a file path

If user provides a file path (e.g., `/walkthrough subtasks.json`):

1. Read the file
2. Identify reviewable items (array of objects, list items, sections)
3. Announce: "Found [N] items. I'll present one at a time. Ready?"
4. Present each item with context
5. Wait for response: `next / discuss / skip / edit`
6. Summarize when complete

### With context from conversation

If items are already in conversation context:

1. Identify what to walk through (findings, suggestions, tasks, etc.)
2. Announce: "I'll walk you through [N] items. Ready for the first?"
3. Present one at a time
4. Wait for response after each

### With explicit list

If user provides inline items:

1. Parse the items
2. Present one at a time
3. Track position (e.g., "**Item 2/5:**")

### No argument or `help`

Show:
```
/walkthrough <file>        Walk through items in a file
/walkthrough              Walk through items from conversation context

Controls:
  next / n / ok   → Continue to next item
  discuss / d     → Dig deeper on this item
  skip / s        → Skip remaining items
  edit / e        → Make a change based on this item
  back / b        → Go back to previous item
  list / l        → Show all items (summary view)
```

## Presentation Format

For each item:

```
---

**[Type] [N]/[Total]:** [Title or summary]

[Details with enough context to understand]

[Action suggestion if applicable]

[next / discuss / skip / edit]
```

## State Tracking

Keep track of:
- Current position
- Items skipped
- Items discussed
- Edits made

At the end, summarize: "Walked through [N] items. [X] discussed, [Y] skipped, [Z] edited."
