---
name: plan-archive
version: 1.0.0
description: '[Planning] Write journal entries and archive specific plans or all plans'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Write journal entries and archive completed or obsolete plans from the plans/ directory.

**Workflow:**
1. **Identify** -- Find plans to archive (specific or all completed)
2. **Journal** -- Write summary journal entry for archived plans
3. **Archive** -- Move plans to archive location or mark as completed

**Key Rules:**
- Preserve plan content during archival, never delete
- Write journal entry documenting what was archived and why
- Clean up plans/ directory for better organization

## Your mission

Read and analyze the plans, then write journal entries and archive specific plans or all plans in the `plans` directory.

## Plan Resolution

1. If `$ARGUMENTS` provided → Use that path
2. Else read all plans in the `plans` directory

## Workflow

### Step 1: Read Plan Files

Read the plan directory:

- `plan.md` - Overview and phases list
- `phase-*.md` - 20 first lines of each phase file to understand the progress and status

### Step 2: Summarize the plans and document them with `/journal` slash command

Use `AskUserQuestion` tool to ask if user wants to document journal entries or not.
Skip this step if user selects "No".
If user selects "Yes":

- Analyze the information in previous steps.
- Use Task tool with `subagent_type="journal-writer"` in parallel to document all plans.
- Journal entries should be concise and focused on the most important events, key changes, impacts, and decisions.
- Keep journal entries in the `./docs/journals/` directory.

### Step 3: Ask user to confirm the action before archiving these plans

Use `AskUserQuestion` tool to ask if user wants to proceed with archiving these plans, select specific plans to archive or all completed plans only.
Use `AskUserQuestion` tool to ask if user wants to delete permanently or move to the `./plans/archive` directory.

### Step 4: Archive the plans

Start archiving the plans based on the user's choice:

- Move the plans to the `./plans/archive` directory.
- Delete the plans permanently: `rm -rf ./plans/<plan-1> ./plans/<plan-2> ...`

### Step 5: Ask if user wants to commit the changes

Use `AskUserQuestion` tool to ask if user wants to commit the changes with these options:

- Stage and commit the changes (Use `/commit` slash command)
- Commit and push the changes (Use `/git-cp` slash command)
- Nah, I'll do it later

## Output

After archiving the plans, provide summary:

- Number of plans archived
- Number of plans deleted permanently
- Table of plans that are archived or deleted (title, status, created date, LOC)
- Table of journal entries that are created (title, status, created date, LOC)

## Important Notes

**IMPORTANT:** Only ask questions about genuine decision points - don't manufacture artificial choices.
**IMPORTANT:** Sacrifice grammar for the sake of concision when writing outputs.
**IMPORTANT:** In the last summary report, list any unresolved questions at the end, if any.
**IMPORTANT:** Ensure token efficiency while maintaining high quality.
