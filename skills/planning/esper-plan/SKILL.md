---
name: esper:plan
description: Add a new feature plan to the current phase backlog. Interviews the user, explores the codebase for context, then writes a detailed plan file. For bug fixes, use /esper:fix instead.
---

You are adding a new feature plan to the esper backlog.

The user's initial prompt: $ARGUMENTS

## Step 1: Check setup

Run `esperkit config check`. If it exits non-zero, tell the user to run `/esper:init` first and stop.

Run `esperkit config get current_phase` to get the current phase slug. Read `.esper/CONSTITUTION.md` and `.esper/phases/<current_phase>.md` to understand the project's scope and current phase goals.

If the feature sounds out of scope for the current phase, flag it and use `AskUserQuestion` to ask whether to proceed anyway or defer it.

## Step 2: Interview the user

Use `AskUserQuestion` for 1–2 rounds. Skip questions already answered by `$ARGUMENTS`:

- What exactly needs to be built or changed?
- Why now — what does this unblock or enable for the phase goal?
- Any constraints: performance, compatibility, design patterns to follow?
- What does "done" look like — how will we verify it works?
- Edge cases or integration risks to be aware of?

For bug fixes, direct the user to `/esper:fix` instead — it has a more appropriate interview.

## Step 3: Explore the codebase

Use the Task tool with `subagent_type: "Explore"`:

```
Find existing files and patterns relevant to [feature being added].
Look for similar features already implemented (for consistency).
Identify potential conflicts or dependencies.
Return a concise summary — do not include full file contents.
```

Cross-reference findings against `.esper/CONSTITUTION.md` to confirm the feature is in scope and doesn't violate any principles.

## Step 4: Determine the next plan ID

Run `esperkit plan next-id` — this scans all plan directories (including archived/) and prints the next available zero-padded ID (e.g. `007`).

## Step 5: Write the plan file

Write `.esper/plans/pending/NNN-slug.md` where `NNN` is the next ID and `slug` is a short kebab-case name.

Feature plans share the phase branch — all features for a phase are batched into one phase PR.

```markdown
---
id: NNN
title: [concise feature title]
status: pending
type: feature
priority: [1 = urgent/blocking, 2 = normal, 3 = low — ask or infer from urgency]
phase: [current_phase obtained above]
branch: feature/[current_phase]
created: [today YYYY-MM-DD]
---

# [Feature title]

## Context
[What you found in the codebase — relevant files, existing patterns, dependencies]

## Approach
[Step-by-step implementation plan, specific to this codebase]

## Files to change
- [file path] ([create/modify] — [brief reason])

## Verification
- Run: [test command from esper.json, or "manual" if no test command]
- Expected: [what passing looks like]
- Edge cases: [anything non-obvious to verify]
```

## Step 6: GitHub Sub-Issue (if applicable)

Run `esperkit config get backlog_mode`. If the output is `github`:
```bash
esperkit plan create-sub-issue <filename>
```
This creates a GitHub issue for the plan and links it as a sub-issue of the phase's parent issue. The issue number is stored as `gh_issue` in the plan's frontmatter.

## Step 7: Confirm

Tell the user:
- Plan file created: `.esper/plans/pending/NNN-slug.md`
- Priority: p[N]
- Part of: [current_phase] — will be batched into the phase PR when all phase plans are done
- Next: `/esper:apply` to start it immediately, or `/esper:backlog` to review the full queue
