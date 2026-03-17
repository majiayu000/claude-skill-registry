---
name: executing-plans
description: Execute implementation plans in batches with review checkpoints
version: 1.0.0
author: Ariff
when_to_use: When a plan is ready to be implemented
---

# Executing Plans

## Purpose
Execute plans in controlled batches with verification gates.

> "I'm using the Executing Plans skill to implement this plan."

## The Process

```
Load Plan → Review → Execute Batch → Report → Feedback → Next Batch
```

### Step 1: Load & Review

1. Read the plan file
2. Review critically - identify concerns
3. If concerns → Raise with user before starting
4. Create TodoWrite for all tasks

### Step 2: Execute Batch

**Default batch size: 3 tasks**

For each task:
1. Mark as `in_progress`
2. Follow each step exactly
3. Run verifications as specified
4. Mark as `completed`

### Step 3: Report

After each batch:

```markdown
## Batch Complete

**Implemented:**
- Task 1: [summary]
- Task 2: [summary]
- Task 3: [summary]

**Verification:**
\`\`\`
[test output]
\`\`\`

Ready for feedback.
```

### Step 4: Continue

Based on feedback:
- Apply changes if needed
- Execute next batch
- Repeat until complete

## When to STOP

🛑 **Stop immediately when:**
- Hit a blocker (missing dependency, unclear instruction)
- Test fails unexpectedly
- Plan has gaps preventing progress
- You don't understand something

**Ask for clarification. Don't guess.**

## Verification Rules

Before marking ANY task complete:
1. Run the verification command
2. Read the FULL output
3. Confirm it matches expectations
4. Only THEN mark complete

No "should work" or "looks good" - actual verification output.

## Batch Reporting Format

```markdown
### Batch N Complete

| Task | Status | Verification |
|------|--------|--------------|
| Task X | ✅ | 12/12 tests pass |
| Task Y | ✅ | Build successful |
| Task Z | ⚠️ | Needs review |

**Next batch:** Tasks A, B, C

Continue?
```

## Completion

After all tasks:

1. Run full test suite
2. Verify all requirements met
3. Report final status
4. Hand off to `finishing-branch` skill if applicable
