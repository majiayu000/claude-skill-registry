---
name: executing-issues
description: Execute a discrete GitHub issue from a detailed plan file (gi_*.md). Use when implementing a specific, well-defined task with an existing implementation plan in doc/plans/issues/. Handles status tracking, verification, and issue lifecycle.
---

# Executing Issues

## Overview

Execute a discrete GitHub issue from a detailed implementation plan (`gi_*.md` file).

**When to use:**
- Implementing a specific issue with an existing plan in `doc/plans/issues/`
- The plan follows the issue-planning template (has Tasks, Acceptance Criteria, etc.)

**When NOT to use:**
- High-level architecture plans (use `executing-plans` instead)
- Plans that span multiple issues
- Exploratory or research tasks

**Announce at start:** "I'm using the executing-issues skill to implement [issue name]."

---

## The Process

### Step 1: Load Issue Plan

1. Read the issue file from `doc/plans/issues/gi_*.md`
2. Verify it has the required sections:
   - Summary
   - Implementation Steps (with checkboxes)
   - Acceptance Criteria
   - Testing section
3. If sections missing: Stop and ask user to complete the plan first

### Step 2: Update Status

1. Update the issue file: `**Status**: Draft` → `**Status**: In Progress`
2. Update `doc/plans/module_issues.md`: Change status to `In Progress`

### Step 3: Review Plan Critically

Before implementing:
1. Read the Technical Analysis and Implementation Plan sections
2. Verify the referenced files exist at the specified paths
3. Check if any dependencies are unmet
4. Identify any questions or concerns

**If concerns:** Raise them with user before starting implementation
**If no concerns:** Create TodoWrite from Implementation Steps and proceed

### Step 4: Execute Implementation

**Batch size: 3 tasks at a time**

For each task in Implementation Steps:
1. Mark as `in_progress` in TodoWrite
2. Follow the step exactly as written
3. If step references specific code: implement as shown
4. Mark checkbox in issue file: `- [ ]` → `- [x]`
5. Mark as `completed` in TodoWrite

**After each batch:**
- Show what was implemented
- Run any specified tests
- Say: "Batch complete. Ready for feedback."
- Wait for user input before continuing

### Step 5: Run Tests

After all implementation steps complete:
1. Run the test commands specified in the Testing section
2. Run any manual verification steps
3. Report results

**If tests fail:**
- Stop and report the failure
- Ask user how to proceed

### Step 6: Verify Acceptance Criteria

Go through each acceptance criterion:
1. Check if it's met
2. Mark checkbox in issue file: `- [ ]` → `- [x]`
3. If any criterion not met: Stop and report

### Step 7: Complete Issue

When all acceptance criteria pass:

1. Update issue file status: `**Status**: In Progress` → `**Status**: Complete`

2. Update `doc/plans/module_issues.md`:
   - Change status to `Complete`
   - Add resolution date if not present

3. Report completion:
   ```
   Issue [name] complete.

   Summary of changes:
   - [list of files modified/created]

   Tests: [pass/fail status]

   Acceptance criteria: All met

   Next steps:
   - [ ] Create PR (if not already done)
   - [ ] Publish to GitHub Issues (if still draft)
   ```

4. **If issue is still a draft** (`gi_draft_*.md`):
   - Remind user: "This issue is ready to publish to GitHub. After creating the GitHub issue, rename the file to `gi_<id>_<desc>.md`"

---

## File Locations

| File | Purpose |
|------|---------|
| `doc/plans/issues/gi_*.md` | Detailed implementation plans |
| `doc/plans/module_issues.md` | Issue index (update status here) |

---

## When to Stop and Ask

**STOP immediately when:**
- A referenced file doesn't exist
- Code example in plan doesn't match actual code structure
- Test fails and you don't know how to fix it
- Acceptance criterion is ambiguous
- You need to make a design decision not covered in the plan

**Ask for clarification rather than guessing.**

---

## Checklist

Before starting:
- [ ] Issue file exists in `doc/plans/issues/`
- [ ] Plan has Implementation Steps with checkboxes
- [ ] Plan has Acceptance Criteria
- [ ] Plan has Testing section

During execution:
- [ ] Status updated to In Progress
- [ ] Each step followed exactly
- [ ] Checkboxes marked as completed
- [ ] Tests run after implementation

After completion:
- [ ] All acceptance criteria met
- [ ] Status updated to Complete
- [ ] module_issues.md updated
- [ ] User reminded about GitHub publication (if draft)

---

## Example Flow

```
User: "Implement the preprunoff operational modes issue"

Claude: "I'm using the executing-issues skill to implement PREPQ-001.

Loading doc/plans/issues/gi_draft_preprunoff_operational_modes.md...

The plan has 5 implementation steps and 7 acceptance criteria.

Updating status to In Progress...

Starting batch 1 (steps 1-3):
1. Create config.yaml
2. Create config.py
3. Add mode parameter handling

[implements steps]

Batch complete. Files created:
- apps/preprocessing_runoff/config.yaml
- apps/preprocessing_runoff/src/config.py

Ready for feedback."
```

---

## Related Skills

- **issue-planning**: Use to create the detailed plan before executing
- **pre-deploy-validation**: Use after completion to validate before deployment
- **software-architecture**: Reference for code conventions
