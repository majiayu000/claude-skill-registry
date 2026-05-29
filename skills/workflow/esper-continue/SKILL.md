---
name: esper:continue
description: Resume an interrupted session. Reads the active increment, assesses progress, and picks up where the last session left off.
---

You are resuming an interrupted implementation session.

## Step 1: Check setup

Run `esperkit context get`. If it fails, tell the user to run `esper:init` first and stop.

Parse the context JSON.

## Step 2: Find the active increment

If `active_increment` is null:
- Run `esperkit increment list --format json` to check for pending increments
- If pending increments exist: "No active increment. You have pending increments. Run `esper:atom` to activate one, or `esper:batch` to review the queue."
- If no increments at all: "No increments found. Run `esper:atom` to create one, or `esper:spec` to work on specs."
- Stop.

## Step 3: Read the active increment

Read the increment file from `.esper/increments/active/<filename>`.
Parse its frontmatter and full body.
If the increment references a spec file, read it: `esperkit spec get <file>`

## Step 4: Assess current state

Run `git log --oneline -10` to see recent commits.
Run `git status --porcelain` to see uncommitted changes.

Cross-reference against the increment:
- Check `## Scope` items against recent commits and file changes
- Check `## Progress` section for recorded progress
- Check `## Files Affected` against actual file state
- Check `## Verification` — run the verification commands if possible

## Step 5: Summarize and resume

Present a concise status:

```
Resuming: [increment title]

Done:
  - [completed scope items]

Remaining:
  - [incomplete scope items]

Uncommitted changes:
  - [files with changes]
```

## Step 6: Continue implementation

Pick up implementation from the first incomplete scope item:
1. Follow the `## Scope` section
2. Create/modify files as planned
3. Run verification after each change
4. Update `## Progress` as work is completed
5. Commit according to workflow_defaults

When all scope items are complete:
- Run final verification
- Ask the user if they want to finish: "All scope items complete. Run `esper:go` to finish, or `esper:review` to verify first."

## Available CLI commands

- `esperkit context get` — read context
- `esperkit increment list` — list increments
- `esperkit spec get <file>` — read a spec
