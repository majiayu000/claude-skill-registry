---
name: esper:fix
description: Add a fix to the backlog. Scoped interview for bug fixes and patches only. Fix plans get their own branch and PR when shipped. For new features, use /esper:plan instead.
---

You are adding a fix to the esper backlog.

The user's initial prompt: $ARGUMENTS

## Step 1: Check setup

Run `esperkit config check`. If it exits non-zero, tell the user to run `/esper:init` first and stop.

Read `.esper/CONSTITUTION.md` to understand the project's scope and principles.

## Step 2: Interview the user

Use `AskUserQuestion` for a single focused round. Skip questions already answered by `$ARGUMENTS`:

- What is broken or incorrect? Describe the symptom and the expected behavior.
- Where in the codebase is the problem likely located? (file, module, component)
- Severity: blocking / urgent (p1), normal (p2), or low priority (p3)?
- How will we verify the fix works?

## Step 3: Explore the codebase

Use the Task tool with `subagent_type: "Explore"`:

```
Find the files and code paths relevant to [bug description].
Identify the likely root cause if visible from the code.
Do not include full file contents — return a concise summary of relevant files and patterns.
```

Cross-reference findings against `.esper/CONSTITUTION.md` to confirm the fix is in scope.

## Step 4: Determine the next plan ID

Run `esperkit plan next-id` — this scans all plan directories (including archived/) and prints the next available zero-padded ID (e.g. `007`).

## Step 5: Write the plan file

Write `.esper/plans/pending/NNN-slug.md` where `NNN` is the next ID and `slug` is a short kebab-case name for the fix.

```markdown
---
id: NNN
title: fix: [concise description of what's broken]
status: pending
type: fix
priority: [1 | 2 | 3]
phase: [current_phase from `esperkit config get current_phase`]
branch: fix/[kebab-slug]
created: [today YYYY-MM-DD]
---

# fix: [description]

## Context
[Root cause analysis from codebase exploration — what is actually wrong and why]

## Approach
[Step-by-step fix plan]

## Files to change
- [file path] (modify — [reason])

## Verification
- Run: [test command or manual steps]
- Expected: [what correct behavior looks like]
- Regression check: [related areas to verify haven't broken]
```

## Step 6: GitHub Sub-Issue (if applicable)

Run `esperkit config get backlog_mode`. If the output is `github`:
```bash
esperkit plan create-sub-issue <filename>
```
This creates a GitHub issue for the fix and links it as a sub-issue of the phase's parent issue. The issue number is stored as `gh_issue` in the plan's frontmatter.

## Step 7: Confirm

Tell the user:
- Fix plan created: `.esper/plans/pending/NNN-slug.md`
- Priority: p[N]
- Branch: `fix/[slug]` — this fix will get its own PR when shipped
- Next: `/esper:apply` to implement immediately, or `/esper:backlog` to queue it
