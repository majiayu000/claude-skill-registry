---
name: save-plan
description: Copy the most recent Claude Code plan into a properly-named Dendron note. Run after plan mode exits.
---

# Save Plan

Copy the most recent Claude Code plan from `.claude/plans/` into a Dendron note under `notes/`. This bridges Claude Code's random plan naming with the project's Dendron naming conventions.

## Workflow

```
(plan mode) -> approve/implement -> /save-plan <dendron-fname> -> /update-tasks-weekly -> /commit
```

## Arguments

**Required:** a Dendron fname for the target note.

- `/save-plan swanki.processing.image_processor.plan-0`
- `/save-plan workspace.ibiofoundry-ai.update.plan-1`

If no argument is provided, ask the user for the target Dendron fname. Do not proceed without one.

## Step 1: Find the most recent plan

List files in `.claude/plans/` sorted by modification time (newest first):

```bash
ls -t .claude/plans/*.md
```

If no plan files exist, inform the user and stop.

Display the filename and first few lines of the most recent plan so the user can confirm it is the right one. Use `AskUserQuestion` with single-select:

- **"Yes, save this plan"** -- proceed with the most recent plan
- **"Show me other plans"** -- list all plans so the user can pick

## Step 2: Read the plan content

Read the full content of the selected plan file. Strip any YAML frontmatter (`---` block at top) if present -- we will use Dendron's own frontmatter.

## Step 3: Create or update the Dendron note

Check if `notes/<dendron-fname>.md` already exists.

### If the note does NOT exist

Create it with proper frontmatter:

```bash
dendron-cli note write --fname "<dendron-fname>"
```

Then append the plan content under a dated H2:

```markdown
## YYYY.MM.DD - Plan

<plan content here>
```

### If the note already exists

Read the existing note. Append the plan content under a new dated H2 at the bottom:

```markdown
## YYYY.MM.DD - Plan

<plan content here>
```

Do not overwrite existing content.

## Step 4: Stage the note

```bash
git add notes/<dendron-fname>.md
```

## Step 5: Summary

Print:

```
Plan saved:
  Source: .claude/plans/<plan-filename>.md
  Target: notes/<dendron-fname>.md
  Section: ## YYYY.MM.DD - Plan

Note staged. Run /update-tasks-weekly to link from weekly note.
```

## Important Rules

- NEVER modify existing content in the target note -- only append.
- NEVER modify Dendron YAML frontmatter.
- Create missing notes with `dendron-cli note write` -- never with the Write tool.
- No Unicode emojis in any markdown content.
- Do NOT ask extra approval questions -- tool approval prompts are the gates (except the plan confirmation in Step 1).

## Example Invocations

- `/save-plan swanki.processing.image_processor.plan-0`
- `/save-plan workspace.ibiofoundry-ai.update.plan-1`
- "save the plan as swanki.processing.pdf_processor.plan-0"
