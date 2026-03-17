---
name: esper:revise
description: Revise a plan, phase, or fix document based on your feedback. You comment, the agent edits. Supports multiple rounds of revision.
---

You are revising an esper document based on the user's feedback.

The user's initial prompt (if any): $ARGUMENTS

## Step 1: Check setup

Run `esperkit config check`. If it exits non-zero, tell the user to run `/esper:init` first and stop.

Read `.esper/CONSTITUTION.md` for project principles.

## Step 2: Identify target

If `$ARGUMENTS` specifies a target, resolve it:

- **Plan ID** (e.g. `21`, `#021`): run `esperkit plan list --format json` to find the matching plan. Look across pending, active, and done directories. Resolve to the file path.
- **Phase name** (e.g. `004-exploration-and-review-skills`): resolve to `.esper/phases/004-exploration-and-review-skills.md`
- **File path** (e.g. `.esper/plans/pending/021-explore-skill.md`): use directly

If no argument or the argument is ambiguous, use `AskUserQuestion`:
"Which document do you want to revise?"
- A pending plan (list plan titles from `esperkit plan list --dir pending --format json`)
- An active plan (list from `esperkit plan list --dir active --format json`)
- The current phase file
- Other (let the user provide a path)

## Step 3: Read and present

Read the target document in full.

Print it for the user to review. Use the document's headings to provide structure:
```
Loaded: .esper/plans/pending/021-explore-skill.md

[full document content]
```

## Step 4: Collect feedback

The user's initial `$ARGUMENTS` may already contain feedback (e.g. `/esper:revise 021 change the approach to use a queue`). If so, use it directly — do not re-ask.

Otherwise, the user will provide feedback in their next message. Wait for it.

The user's feedback can be:
- Free-form comments ("the approach section is too vague")
- Specific edits ("change the priority to 1")
- Structural feedback ("add an edge cases section")
- Multiple items at once

## Step 5: Apply revisions

Edit the document according to the user's feedback using the Edit tool.

After applying changes, print a summary of what was changed:
```
Changes applied:
- [section]: [what changed]
```

Then ask: "Any more changes, or is this good?"

If the user has more feedback, repeat Steps 4-5.

## Step 6: Confirm

When the user is satisfied, confirm:
```
Document updated: [file path]
```

Suggest next steps based on the document type:
- **Pending plan**: "Run `/esper:apply` to start building, or `/esper:backlog` to review the full queue."
- **Active plan**: "The active plan has been updated. Continue with `/esper:continue`."
- **Phase file**: "Phase definition updated."
- **Done plan**: "Note: this plan is already shipped. The revision is recorded but won't affect implementation."
