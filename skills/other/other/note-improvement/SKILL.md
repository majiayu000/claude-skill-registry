---
name: note-improvement
description: "Capture an out-of-scope improvement opportunity so it doesn't get lost. Use when the user asks to \"note improvement\", \"save improvement\", \"track this for later\", \"remember this improvement\", \"note this idea\", \"log improvement\", \"backlog this\", or \"park this idea\". Also invoke proactively when noticing something improvable during work that falls outside the current task's scope — briefly mention it to the user and offer to note it."
argument-hint: "[improvement description]"
---

# Note Improvement

Capture improvement opportunities discovered during work so they don't get silently dropped. Appends to a project-level `.turbo/improvements.md` file that serves as a backlog of actionable ideas.

## Step 1: Determine Project Root

Find the nearest `.git` directory or project root. The improvements file lives at `.turbo/improvements.md` relative to the project root.

## Step 2: Identify the Improvement

Gather from context or `$ARGUMENTS`:

- **What**: One-line summary of the improvement
- **Where**: File path(s) and/or area of the codebase affected
- **Why**: Brief rationale — what's the benefit?
- **Category**: One of `refactor`, `performance`, `reliability`, `readability`, `testing`, `docs`, `dx` (developer experience), or `feature`

## Step 3: Append to File

Read `.turbo/improvements.md` if it exists. Create it with the header below if it doesn't.

**File header** (only when creating new):

```markdown
# Improvements

Out-of-scope improvement opportunities captured during work sessions. Review periodically and pull items into active work when appropriate.
```

**Entry format:**

```markdown
### [one-line summary]

- **Category**: [category]
- **Where**: `[file path or area]`
- **Why**: [brief rationale]
- **Noted**: [YYYY-MM-DD]
```

Append the new entry at the end of the file.

## Step 4: Confirm

Tell the user the improvement was noted and where the file is.

## Rules

- Do not duplicate — before appending, check if a similar improvement already exists. If it does, update the existing entry instead.
- Keep entries concise — 3-5 lines max per entry. These are backlog items, not specs.
- Do not act on the improvement — only record it. The user decides when to address it.
- Do not create the `.turbo/` directory if the project doesn't have one — ask the user where to put the file instead.
