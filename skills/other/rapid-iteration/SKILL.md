---
name: rapid-iteration
description: |
  Optimizes for fast version cycling. Minimal questions, maximum output.
  Auto-diffs between versions and accepts terse feedback. Use when you need
  to iterate quickly on designs, code, or content. Ship-feedback-next loop.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
---

# Rapid Iteration

Ship fast. Get feedback. Iterate. Repeat.

---

## Quick Start

1. **Describe what you want.** Run `/rapid-iteration "a signup form with email and password"`. Version 1 appears immediately with no clarifying questions.
2. **Give terse feedback.** Say "bigger title", "add a forgot password link", or just "more padding". Each response produces the next version with a diff from the previous one.
3. **Say "done" when satisfied.** The skill shows the final version history and offers to clean up intermediates or commit.

---

## Overview

When speed matters more than perfection, this skill optimizes for fast version cycling. It:

- Skips brainstorming and goes straight to output
- Accepts terse feedback ("bigger", "more blue", "add X")
- Auto-diffs between versions
- Tracks version history
- Minimizes questions, maximizes output

---

## Commands

### `/rapid-iteration [description]`

Start a new rapid iteration cycle.

1. Immediately produce Version 1 (v1) based on the description
2. Enter iteration loop

### `/rapid-iteration next [feedback]`

Apply feedback and produce next version.

### `/rapid-iteration diff [v1] [v2]`

Show diff between two specific versions.

### `/rapid-iteration history`

Show all versions with brief change summaries.

### `/rapid-iteration revert [version]`

Go back to a specific version.

---

## The Loop

```
1. User gives description or feedback
2. Produce output IMMEDIATELY (no clarifying questions)
3. Show version number and brief change summary
4. Show diff from previous version (if not v1)
5. Wait for feedback
6. GOTO 1
```

---

## Key Behaviors

### 1. No Brainstorming

Do NOT ask "What style do you prefer?" or "Should I use X or Y?".
Pick the most reasonable default and ship it. The user will correct.

### 2. Terse Feedback Accepted

Interpret short commands as iteration instructions:

| User Says | Interpretation |
|---|---|
| "bigger" | Increase size/scale of the primary element |
| "smaller" | Decrease size/scale |
| "more X" | Increase the quality/quantity of X |
| "less X" | Decrease the quality/quantity of X |
| "add X" | Include X in the output |
| "remove X" | Remove X from the output |
| "move X to Y" | Reposition X to location Y |
| "like before but with X" | Revert to previous, add X |
| "good but X" | Keep current, modify only X |
| "undo" | Revert to previous version |
| "perfect" / "done" / "ship it" | End iteration, finalize |

### 3. Version Tracking

Track each version with:

```markdown
## Version History

| Version | Change | File |
|---------|--------|------|
| v1 | Initial version | output/feature-v1.ext |
| v2 | Made header bigger | output/feature-v2.ext |
| v3 | Added blue accent | output/feature-v3.ext |
```

### 4. Auto-Diff

After each version (except v1), show a concise diff:

```
Changes from v2 → v3:
- Header: font-size 24px → 32px
- Added: blue accent border on cards
- Removed: gray background on sidebar
```

For code changes, use actual diff format. For design/content changes, use human-readable descriptions.

### 5. File Management

Save each version with version suffix:
- `output/component-v1.tsx`
- `output/component-v2.tsx`
- `output/component-v3.tsx`

Or, if iterating on a single file, use git-friendly approach:
- Edit in place
- Note the version in a comment or the version history

Ask user preference on first iteration: "Save each version separately or iterate in place?"

---

## Speed Optimizations

- **No preamble**: Don't explain what you're about to do. Just do it.
- **No recap**: Don't summarize the previous version. Show the diff.
- **No alternatives**: Don't offer options. Ship one version.
- **No confirmation**: Don't ask "Is this what you wanted?". They'll tell you.
- **Parallel output**: If generating multiple files, write them all at once.

---

## Ending the Loop

The iteration loop ends when the user says any of:
- "done", "perfect", "ship it", "that's it", "finalize", "good"

On end:
1. Confirm the final version number
2. Show complete version history
3. Clean up intermediate versions if user wants
4. Offer to commit the final version

---

## File Type Awareness

Different file types need different diffing and change-description strategies. A code diff is useless for describing a CSS layout change, and a prose description wastes space when a real diff is clearer.

### Diffing Strategy by File Type

| File Type | Diff Strategy | Example Output |
|---|---|---|
| Code (`.ts`, `.tsx`, `.js`, `.py`, `.go`) | Actual diff (unified format, 3 lines context). Show added/removed/changed lines. | `- const size = 24;` / `+ const size = 32;` |
| Styles (`.css`, `.scss`, `.tailwind` classes) | Describe visual changes, not selectors. Users think in visuals, not class names. | "Header: larger text (text-xl to text-3xl), added bottom border" |
| Markup (`.html`, `.jsx` structure) | Describe structural changes: added/removed/moved elements. | "Added: password confirmation field below password field. Moved: submit button to full-width layout" |
| Markdown (`.md`) | Structural diff: sections added/removed/reordered, heading level changes. | "Added: ## Installation section after Overview. Removed: FAQ section" |
| Config (`.json`, `.yaml`, `.toml`, `.env`) | Key-value changes only. Show the key, old value, new value. | `port: 3000 -> 8080`, `debug: added (true)` |
| Images / binary | Cannot diff. Describe the change in words. | "Replaced logo with higher-res version (200x200 -> 400x400)" |

### When in Doubt

If the file type is ambiguous, use the code diff format. It is always technically correct, even if not the most readable option for that file type.

---

## Rollback Chain

The `undo` command currently reverts to the previous version. But users often need to go back further: "actually, go back to the version before the sidebar change." Maintain a full rollback chain.

### Version Stack

Internally, keep an ordered stack of all versions:

```
v5 <- current
v4
v3
v2
v1
```

### Rollback Commands

| Command | Behavior |
|---|---|
| `undo` | Revert to v(current-1). New current becomes v(current-1). The undone version is not deleted; it moves to a "redo" stack. |
| `undo 3` | Revert to v(current-3). Same redo-stack behavior. |
| `redo` | Re-apply the last undone version. Only available immediately after `undo`. |
| `revert v2` | Jump directly to v2. All versions after v2 remain in history but current pointer moves to v2. The next `next` command creates v(latest+1) branching from v2. |
| `history` | Show all versions with change summaries. Mark the current version. |

### Branching After Revert

If the user reverts to v2 and then gives new feedback, the new version is v6 (not v3). The history becomes:

```
v6 <- current (branched from v2)
v5 (original path)
v4 (original path)
v3 (original path)
v2 <- branch point
v1
```

This avoids confusion about which "v3" you mean.

---

## Batch Feedback

Users often have multiple changes in mind at once. Instead of forcing one change per iteration cycle, accept compound feedback and apply all changes in a single version.

### How to Detect Batch Feedback

Batch feedback contains multiple instructions in one message. Look for:

- Comma-separated instructions: "bigger title, remove sidebar, add blue accent"
- Numbered lists: "1. fix the header 2. add a footer 3. change background to gray"
- "and" connectors: "make it wider and add padding and change the font"

### How to Handle

1. Parse each instruction separately.
2. Apply all of them to produce one new version.
3. In the diff output, list each change on its own line so the user can see that all instructions were addressed:

```
Changes from v3 -> v4:
- Title: font-size 24px -> 36px (you said "bigger title")
- Sidebar: removed entirely (you said "remove sidebar")
- Cards: added 2px blue left border (you said "add blue accent")
```

4. If instructions conflict with each other ("make it bigger" + "make it smaller"), apply the last one and note the conflict:

```
Note: "bigger" and "smaller" conflict. Applied "smaller" (last instruction).
```

### Partial Rejection

If the user responds with "good but undo the sidebar part", apply a selective rollback:

1. Take current version (v4)
2. Re-apply only the sidebar from v3
3. Keep the other changes from v4
4. Produce v5 with a diff showing only the sidebar restoration

---

## Important Constraints

- **Speed over perfection**: v1 should appear in < 10 seconds of thinking
- **Never block on questions**: If unsure, pick a reasonable default
- **Respect "undo"**: Always be able to revert to any previous version
- **Keep diffs concise**: 3-5 key changes, not a line-by-line dump
- **Don't over-interpret**: "bigger" means bigger, not "bigger and also refactored and improved"
