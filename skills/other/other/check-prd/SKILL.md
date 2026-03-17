---
name: check-prd
description: Verify PRD completion against its success criteria
---

# Check PRD Skill

Verify that a PRD's success criteria are met and all tasks are complete.

## Arguments

The user provides a PRD number or path. If not given, ask which PRD to check.

## Workflow

1. **Read PRD**: Load the full document
2. **Check Section 2 (Success Criteria)**: Verify each criterion
3. **Check Section 6 (Implementation Plan)**: Verify all tasks are done
4. **Run verifications**: Execute verification commands for each task
5. **Report results**: Pass/fail per criterion with evidence
6. **Recommend**: Suggest stage transition if all criteria pass

## Success Criteria Verification

For each success criterion in the table:

1. Read the Measurement column — understand how to verify
2. Read the Target column — understand what "pass" means
3. Run appropriate verification:
   - **Code existence**: Use Glob/Grep to find the code
   - **Test passing**: Run the test command
   - **Build success**: Run `bun turbo build`
   - **Type safety**: Run `bun turbo type-check`
   - **Lint clean**: Run `bun turbo lint`
   - **Manual check**: Inspect the relevant files

## Task Completion Check

For each task in Section 6:

1. Check if the expected files/changes exist
2. Run the task's verification command (from annotations)
3. Mark as PASS or FAIL

## Output Format

```markdown
## PRD Check: PRD-NNN — Title

### Success Criteria

| #   | Criterion   | Target       | Result    | Evidence       |
| --- | ----------- | ------------ | --------- | -------------- |
| 1   | Description | Target value | PASS/FAIL | What was found |
| 2   | ...         | ...          | ...       | ...            |

### Task Completion

| Task # | Description | Status    | Verification           |
| ------ | ----------- | --------- | ---------------------- |
| 1      | Task name   | PASS/FAIL | Command output summary |
| 2      | ...         | ...       | ...                    |

### Overall: PASS / FAIL

**Recommendation**: [Move to completed / Fix issues listed above]
```

## After Checking

- If all criteria pass: Suggest `/move-prd PRD-NNN completed`
- If some fail: List specific failures and what needs to be done
- If PRD is already in `completed/`: Confirm it's still valid
