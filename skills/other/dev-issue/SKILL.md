---
name: dev-issue
description: |
  [DEPRECATED] Use /execute-plan instead. This skill has been renamed for clarity.
  Execute implementation plan step-by-step - creates todos from plan, guides through tasks sequentially, runs until issue resolved.
  TRIGGER when: user wants to implement after /start-issue (e.g., "start development", "implement issue #23", "work on the plan", "execute the tasks").
  DO NOT TRIGGER when: user just wants to plan (use /start-issue), review code (use /review), or finish work (use /finish-issue).
version: "3.0.0"
argument-hint: "[issue-number] [--resume] [--skip-task N]"
allowed-tools: Bash(git *), Bash(gh *), Bash(npm *), Read, Write, Glob, Grep, Edit
disable-model-invocation: false
user-invocable: true
---

# ⚠️ DEPRECATED: Dev Issue - Use /execute-plan Instead

**This skill has been renamed to `/execute-plan` for better clarity.**

**Why renamed:**
- "dev-issue" was vague and didn't clearly describe its purpose
- "execute-plan" accurately reflects what it does: executes implementation plans step-by-step
- Better discoverability for new users

**Migration:**
- `/dev-issue` still works as an alias for backwards compatibility
- Update your workflows to use `/execute-plan` instead
- All documentation has been updated to reference the new name

**→ See**: [/execute-plan](../execute-plan/SKILL.md) for current documentation

---

## Legacy Documentation (for reference only)

Execute implementation plan step-by-step until issue is resolved.

## Overview

This skill bridges `/start-issue` (planning) and `/review` (quality check) by orchestrating active development:

**What it does:**
1. **Loads plan** from `/start-issue` (`.claude/plans/active/issue-{N}-plan.md`)
2. **Creates todos** from plan tasks for progress tracking
3. **Guides implementation** task-by-task with context
4. **Validates progress** after each task (tests, linting, build)
5. **Continues until complete** - all tasks done, tests passing
6. **Prepares deliverables** for `/review` to validate quality

**Why it's needed:**
The gap between planning and completion lacks structure. Developers lose focus, skip tasks, or forget validation. This skill provides systematic task execution with built-in checkpoints.

**When to use:**
- After `/start-issue` creates branch and plan
- User says "start development", "implement", "work on issue"
- Need structured guidance through multi-task implementation

**Workflow sequence:**
```
/start-issue #23   → Creates branch + plan
/dev-issue #23     → Executes plan tasks (this skill)
/review            → Validates quality
/finish-issue #23  → Commits + PR + merge
```

## Arguments

```bash
/dev-issue [issue-number] [options]
```

**Common usage:**
```bash
/dev-issue #23              # Start fresh implementation
/dev-issue #23 --resume     # Resume after interruption
/dev-issue --skip-task 3    # Skip specific task (rare)
```

**Options:**
- `[issue-number]` - Optional, inferred from branch if omitted
- `--resume` - Resume from last incomplete task
- `--skip-task N` - Skip task N (use cautiously)
- `--dry-run` - Preview workflow without executing

## Workflow Steps

Copy this checklist to track progress:

```
Task Progress (High-Level):
- [ ] Step 1: Load plan and prerequisites
- [ ] Step 2: Create todos from plan
- [ ] Step 3: Execute tasks sequentially
- [ ] Step 4: Final validation
- [ ] Step 5: Report completion

Specific Tasks (from plan):
- [ ] Task 1: {from your plan}
- [ ] Task 2: {from your plan}
- [ ] Task 3: {from your plan}
... (tasks extracted from .claude/plans/active/issue-N-plan.md)
```

**Note**: Specific tasks are extracted from your implementation plan. The checklist above shows the high-level workflow phases.

Execute in sequence with progress tracking:

### Step 1: Load Plan and Prerequisites

**Verify environment:**
- On feature branch (not main)
- Plan file exists: `.claude/plans/active/issue-{N}-plan.md`
- Git working directory clean (or can be stashed)

**Load plan:**
```bash
# Read plan file
PLAN_FILE=".claude/plans/active/issue-${ISSUE_NUM}-plan.md"
cat "$PLAN_FILE"
```

**Extract tasks** from plan's `## Tasks` section (look for `- [ ]` checkboxes or numbered lists).

**Abort if**:
- Not on feature branch → suggest `/start-issue #N`
- Plan file missing → suggest `/start-issue #N` or `/plan`
- No tasks found in plan → ask user to clarify plan

### Step 2: Create Todos from Plan

**Parse tasks** from plan and create with TaskCreate:

```markdown
For each task in plan:
1. Extract task description
2. Create todo: TaskCreate(subject, description, activeForm)
3. Add dependencies: task N blocks task N+1
4. Track task ID mapping
```

**Example:**
Plan has:
```markdown
## Tasks
- [ ] Read dev-issue/SKILL.md
- [ ] Create REFERENCE.md
- [ ] Update SKILL.md with links
```

Creates 3 linked todos:
- Task #1: "Read dev-issue/SKILL.md"
- Task #2: "Create REFERENCE.md" (blocked by #1)
- Task #3: "Update SKILL.md" (blocked by #2)

**Why todos:** Visual progress in Claude Code UI + checkpoint tracking.

### Step 3: Execute Tasks Sequentially

**For each task:**

**3.1. Display task context:**
```markdown
📋 Current Task (X/Y)

**Task**: {task description}
**From plan**: {link to plan section}
**Dependencies**: {completed tasks}
**Remaining**: {Y-X tasks}

**Acceptance criteria** (if defined in plan):
- {criteria 1}
- {criteria 2}
```

**3.2. Guide implementation:**
- Explain what needs to be done
- Show relevant code patterns or examples
- Suggest file locations and structure
- Provide implementation approach

**3.3. Execute or guide user:**
- For straightforward tasks (file edits, renames): Execute directly
- For complex tasks (new features, algorithms): Provide guidance + code snippets
- For research tasks (investigation, analysis): Conduct research and summarize

**3.4. Validate task completion:**
```bash
# After each task, run quick checks:
- If code changed: npm run lint (if exists)
- If tests exist: npm test (quick smoke test)
- If build required: npm run build
- Git status: ensure changes are intentional
```

**3.5. Mark task complete:**
```
TaskUpdate(task_id, status="completed")
```

**3.6. Move to next task:**
- Unblock next task in dependency chain
- Display next task context
- Repeat 3.1-3.5

**Interruption handling:**
- If user stops mid-task: Save progress state
- Resume with `--resume`: Continue from last incomplete task
- Show clear "You are here" indicator

### Step 4: Final Validation

**After all tasks complete:**

**4.1. Run comprehensive checks:**
```bash
# If tests exist
npm test || echo "⚠️ Tests need attention"

# If linting configured
npm run lint || echo "⚠️ Linting issues found"

# If build exists
npm run build || echo "⚠️ Build failed"

# Git status
git status --short
```

**4.2. Verify all tasks done:**
```markdown
✅ All tasks complete (Y/Y)

Completed:
- ✅ Task 1: {description}
- ✅ Task 2: {description}
- ✅ Task 3: {description}
...
```

**4.3. Prepare deliverables summary:**
```markdown
📦 Deliverables Ready for Review

**Files changed**: {count} files
**Lines added/removed**: +X/-Y
**Tests**: {passing}/{total} passing
**Linting**: {status}
**Build**: {status}

**Review checklist**:
- [ ] Code quality (run /review)
- [ ] Tests comprehensive
- [ ] Documentation updated
- [ ] No unintended changes
```

### Step 5: Report Completion

**Success message:**
```markdown
🎉 Development Complete!

**Issue #23**: {title}
**Tasks completed**: {Y}/{Y}
**Status**: ✅ Ready for review

**Next steps**:
1. Review code quality: /review
2. Make adjustments if needed
3. Finish issue: /finish-issue #23

**Current state**:
Branch: {branch-name}
Files changed: {count}
Tests: {status}
```

**What NOT to do:**
- Don't commit yet (that's `/finish-issue`'s job)
- Don't push yet
- Don't create PR yet

**Hand off to:**
- `/review` - Quality validation
- `/finish-issue #23` - Final commit + PR + merge

## Error Handling

**Not on feature branch:**
```
❌ Not on feature branch

You're on: {current-branch}
Need: feature/{N}-{title}

Fix: /start-issue #23
```

**Plan file missing:**
```
❌ Plan not found

Expected: .claude/plans/active/issue-{N}-plan.md

Options:
1. Create plan: /start-issue #23
2. Custom plan: /plan "feature description"
```

**Task fails validation:**
```
⚠️ Task validation failed

Task: {description}
Error: {error message}

Options:
1. Fix and retry
2. Skip (--skip-task N) - not recommended
3. Pause and investigate
```

**Tests fail mid-implementation:**
```
❌ Tests failing

Failed: {test names}

This is expected during TDD. Continue implementing, then fix tests.

Options:
1. Continue (tests can fail during development)
2. Fix now (recommended for regressions)
3. Pause and debug
```

## Examples

### Example 1: Basic Implementation

**User says:**
> "start development on issue 95"

**Workflow:**
1. Load plan from `.claude/plans/active/issue-95-plan.md`
2. Create 15 todos from plan tasks
3. Execute task 1: "Read dev-issue/SKILL.md" → provides summary
4. Execute task 2: "Create REFERENCE.md" → creates file
5. Execute task 3: "Update SKILL.md" → updates with links
6. ... continues through all 15 tasks ...
7. Final validation: all tasks ✅, tests passing
8. Report: "Ready for review"

**Time:** Varies by complexity (30 min - 2 hours)

### Example 2: Resume After Interruption

**User says:**
> "resume development on issue 95"

**Workflow:**
1. Load plan and todo state
2. Find last incomplete task (task #8)
3. Display context: "Resuming from task 8/15"
4. Continue execution from task 8
5. Complete remaining tasks
6. Final validation and report

**Time:** Depends on remaining tasks

### Example 3: Skip Task

**User says:**
> "continue development but skip task 3, I already did it manually"

**Workflow:**
1. Load plan and current task (#2 just completed)
2. Skip task 3 (mark as completed without executing)
3. Move to task 4
4. Continue normally

**Time:** Same as basic flow minus one task

## Integration

**Workflow integration:**
```
Issue Lifecycle:
1. /start-issue #23     - Create branch + plan (30 sec)
2. /dev-issue #23       - Execute plan (30 min - 2 hrs) ← THIS SKILL
3. /review              - Quality check (5-10 min)
4. /finish-issue #23    - Commit + PR + merge (2-3 min)
```

**Plan structure expected:**
```markdown
## Tasks
- [ ] Task 1 description
- [ ] Task 2 description
- [ ] Task 3 description

## Acceptance Criteria
- Criteria 1
- Criteria 2
```

**Files involved:**
- Input: `.claude/plans/active/issue-{N}-plan.md`
- State: Tracked via TaskCreate/TaskUpdate
- Output: Modified code files (not committed yet)

## Best Practices

1. **Always use after /start-issue** - Ensure plan exists
2. **Don't skip tasks** unless absolutely necessary
3. **Let validation run** - Catches issues early
4. **Review before finishing** - Use `/review` before `/finish-issue`
5. **Commit at logical points** - If multi-day work, commit WIP

## Performance

- **Startup time:** <5 seconds (load plan + create todos)
- **Per task:** 2-15 minutes (depends on complexity)
- **Total time:** 30 minutes - 2 hours (typical)
- **Validation:** 10-30 seconds per task

Fast because:
- Structured task execution (no wandering)
- Built-in checkpoints (validate after each task)
- Clear context (always know next step)

## Workflow Skills Requirements

This is a **workflow skill** and must follow the standard pattern:

1. **TaskCreate** at start - Create todo list from plan tasks
2. **TaskUpdate** during execution - Mark tasks as completed
3. **Verification checklist** - Final validation before completion

**See**: [WORKFLOW_PATTERNS.md](../WORKFLOW_PATTERNS.md) for complete implementation guide

## Related Skills

- **/start-issue** - Creates branch and plan (run before this)
- **/review** - Quality validation (run after this)
- **/finish-issue** - Commit and close issue (final step)
- **/next** - Get single next task (lighter alternative)

## Advanced Topics

For detailed guidance on:
- **TDD Workflow** - Test-first development approach
- **Architecture Documentation** - When and how to document design
- **Complex Task Patterns** - Multi-file refactoring, API changes
- **State Recovery** - Handling interruptions and resuming

**See**: [REFERENCE.md](REFERENCE.md) for complete details

---

**Version:** 3.0.0
**Last Updated:** 2026-03-10
**Changelog:**
- v3.0.0 (2026-03-10): Development workflow for issue implementation (variant of work-issue)

**Pattern:** Workflow Orchestrator (executes plan step-by-step)
**Compliance:** ADR-001 ✅ | WORKFLOW_PATTERNS.md ✅
