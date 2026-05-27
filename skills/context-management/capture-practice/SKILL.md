---
name: capture-practice
description: Captures an insight or practice discovered during work and registers it in the dotforge practices/inbox.
---

# Capture Practice

Register an insight, pattern, or lesson learned in the dotforge inbox.

## Input routing

**If $ARGUMENTS is empty → auto-detect mode (Step 0).**
**If $ARGUMENTS has content → skip to Step 1.**

---

## Step 0: Auto-detect (only when $ARGUMENTS is empty)

Analyze the recent conversation to identify the most generalizable insight from this session.

### Detection signals (in priority order)

1. **Workaround discovered** — the obvious approach failed and an alternative was used
2. **Multi-attempt bug** — a fix required more than one attempt or root cause was non-obvious
3. **Architectural decision with trade-offs** — two+ alternatives were considered, one chosen with reasoning
4. **Non-obvious tool/API/flag behavior** — a parameter, edge case, or behavior was surprising
5. **Missing rule** — the session revealed a gap in `.claude/rules/` or `CLAUDE.md` that would have prevented the problem

### Extraction rules

- Extract the single most generalizable insight — not session notes, not a summary of everything done
- Formulate it as a reusable principle: "When X, do Y because Z" or "Never do X — use Y instead"
- Keep it to 1-2 sentences max
- Ignore: trivial tasks, first-attempt successes, routine edits

### If no signal is present

Respond: "No generalizable insight detected in this session. If you have something specific in mind, run `/cap \"description\"`."
Stop — do not create a file.

### Propose and confirm

Show the proposed insight and ask for confirmation before proceeding:

```
Proposed practice:
"{{one-line insight}}"

Tags: {{inferred tags}}
Project: {{current project name}}

Save this? [Y/n/edit]
```

- If **Y** or user confirms → continue to Step 1 with the proposed text as $ARGUMENTS
- If **n** → stop, no file created
- If **edit** or user rewrites → use the rewritten text as $ARGUMENTS, continue to Step 1

---

## Step 1: Parse the insight

From $ARGUMENTS (provided or confirmed from Step 0), extract:
- **What**: the practice or pattern
- **Why**: evidence or context (current project, error that motivated it)
- **Impact**: which dotforge files could change
- **Tags**: categorization (hooks, rules, prompting, security, stack-specific, etc.)

## Step 2: Validate duplicates

Before creating, check for existing similar practices:
1. Search `$DOTFORGE_DIR/practices/active/` by title or similar tags
2. Search `$DOTFORGE_DIR/practices/inbox/` by similar title
3. If duplicate found → inform the user and ask: update existing or create new?

## Step 3: Generate file

Create file in `$DOTFORGE_DIR/practices/inbox/` with format:

```yaml
---
id: practice-{{YYYY-MM-DD}}-{{slug}}
title: {{short title}}
source: "own experience"
source_type: experience
discovered: {{YYYY-MM-DD}}
status: inbox
tags: [{{tags}}]
tested_in: {{current project or null}}
incorporated_in: []
replaced_by: null
---

## Description
{{what the practice states}}

## Evidence
{{why it works, discovery context}}

## Impact on dotforge
{{which files would need to change}}

## Decision
Pending
```

File name: `{{YYYY-MM-DD}}-{{slug}}.md`

## Step 4: Confirm

Show:
```
Practice captured: {{title}}
File: practices/inbox/{{file}}
Tags: {{tags}}

Next step: /forge update evaluates pending practices from inbox.
```
