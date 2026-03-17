---
name: task-valid-review
description: "[Task Mgmt] Verification tool for validating task completion in Review section. Use when checking if tasks are actually done before moving from Review to Done. Verifies subtask completion, code/file changes, and task-work alignment. Optional but recommended for quality assurance. (user)"
---

# Task Valid Review

Verification skill for validating task completion. Use this when reviewing tasks in the Review section to check if work is actually complete before moving to Done.

## When to Use

| Situation | Usage |
|-----------|-------|
| Task is in Review section | Verify before moving to Done |
| User wants to check completion | Run validation checklist |
| Uncertain if work matches task | Generate validation report |

**Note:** This is a verification tool for the Review stage, not a mandatory gate. AI moves tasks to Review first, then this tool helps verify completion.

## Verification Checklist

### 1. Subtask Completion Check

**Check if all subtasks are completed.**

```
Validation Steps:
1. Count total subtasks under parent task
2. Count completed subtasks (- [x])
3. If incomplete subtasks exist → List them
4. Determine if task is ready for Done
```

### 2. Code/File Change Verification

**Check if actual changes exist for code-related tasks.**

| Task Type | Expected Evidence |
|-----------|-------------------|
| New Feature | New files created OR existing files modified |
| Bug Fix | Code changes in relevant files |
| Refactoring | File modifications detected |
| UI/UX | View/Component files changed |
| Documentation | .md files created/modified |

**Verification Method:**
```bash
git status                    # Check current changes
git diff --stat HEAD~N        # Check recent commits
```

### 3. Task-Work Alignment Check

**Check if completed work matches the task description.**

| Check | Description |
|-------|-------------|
| Title Match | Work addresses what the task title describes |
| Scope Match | All aspects mentioned in subtasks are addressed |
| No Partial Work | No "TODO" or "FIXME" left in new code |
| Build Success | Code compiles without errors |

## Output Format

**On Validation PASS:**
```markdown
## Task Validation: PASS ✅

**Task:** [Task Title]
**Subtasks:** 5/5 completed
**Files Changed:** 3 files (+120, -45 lines)
**Evidence:**
- Created: `Sources/Features/Login/LoginView.swift`
- Modified: `Sources/App/AppCoordinator.swift`

→ Ready to move from Review to Done
```

**On Validation FAIL:**
```markdown
## Task Validation: FAIL ❌

**Task:** [Task Title]
**Reason:** [Specific failure reason]

**Issues Found:**
1. ❌ Subtasks incomplete: 2/5 completed
   - [ ] Add form validation logic
   - [ ] Handle error states
2. ❌ No file changes detected

**Recommended Actions:**
- Complete remaining subtasks
- Move back to Worker for more work
```

## Exception Cases (No Code Changes Expected)

| Task Type | Valid Reason for No Code |
|-----------|-------------------------|
| Research/Analysis | Output is documentation or notes |
| Planning | Output is plan document |
| Review | Output is review comments |
| Documentation-only | Only .md files expected |

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `task-mover` | Move task from Review to Done after verification |
| `task-segmentation` | If subtasks need more breakdown |
| `task-add` | When discovering additional work needed |
| `history-logger` | After task moves to Done, log completion |