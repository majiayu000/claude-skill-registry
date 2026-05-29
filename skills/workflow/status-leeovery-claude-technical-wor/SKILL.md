---
name: status
description: "Show workflow status - what exists, where you are, and what to do next."
disable-model-invocation: true
---

Show the current state of the workflow for this project.

## Step 0: Run Migrations

**This step is mandatory. You must complete it before proceeding.**

Invoke the `/migrate` skill and assess its output.

**If files were updated**: STOP and wait for the user to review the changes (e.g., via `git diff`) and confirm before proceeding to Step 1. Do not continue automatically.

**If no updates needed**: Proceed to Step 1.

---

## Step 1: Scan Directories

Check for files in each workflow directory:

```
docs/workflow/research/
docs/workflow/discussion/
docs/workflow/specification/
docs/workflow/planning/
```

## Step 2: Present Status

Research is project-wide exploration. From discussion onwards, work is organised by **topic** - different topics may be at different stages.

Show a summary like this:

```
## Workflow Status

**Research:** 2 files (exploration.md, market-analysis.md)

**Topics:**

| Topic        | Discussion | Spec | Plan | Implemented |
|--------------|------------|------|------|-------------|
| auth-system  | ✓          | ✓    | ✓    | in progress |
| payment-flow | ✓          | ✓    | -    | -           |
| notifications| ✓          | -    | -    | -           |
```

Adapt based on what exists:
- If a directory is empty or missing, show "Not started"
- For planning, note the output format if specified in frontmatter
- Match topics across phases by filename

## Step 3: Suggest Next Steps

Based on what exists, offer relevant options. Don't assume linear progression - topics may have dependencies on each other.

**If nothing exists:**
- "Start with `/start-research` to explore ideas, or `/start-discussion` if you already know what you're building."

**If topics exist at various stages**, summarise options without being prescriptive:
- Topics in discussion can move to specification
- Topics with specs can move to planning
- Topics with plans can move to implementation
- Completed implementations can be reviewed

Example: "auth-system has a plan ready. payment-flow needs a spec before planning. You might want to complete planning for related topics before implementing if there are dependencies."

Keep suggestions brief - the user knows their project's dependencies better than we do.

## Step 4: Mention Plan Viewing

If planning files exist, let the user know they can view plan details:

```
To view a plan's tasks and progress, use /view-plan
```

## Notes

- Keep output concise - this is a quick status check
- Use tables for scannable information
