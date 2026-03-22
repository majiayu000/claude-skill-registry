---
name: execute-plan
description: |
  Execute implementation plan step-by-step - creates todos from plan, guides through tasks sequentially, runs until issue resolved.
  TRIGGER when: user wants to execute the plan after /start-issue (e.g., "execute the plan", "execute plan for #23", "implement issue #23", "work on the plan").
  DO NOT TRIGGER when: user just wants to plan (use /start-issue), review code (use /review), or finish work (use /finish-issue).
version: "3.1.0"
argument-hint: "[issue-number] [--resume] [--skip-task N]"
allowed-tools: Bash(git *), Bash(gh *), Bash(npm *), Read, Write, Glob, Grep, Edit
disable-model-invocation: false
user-invocable: true
---

# Execute Plan - Implementation Plan Executor

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
/execute-plan #23     → Executes plan tasks (this skill)
/review            → Validates quality
/finish-issue #23  → Commits + PR + merge
```

## Arguments

```bash
/execute-plan [issue-number] [options]
```

**Common usage:**
```bash
/execute-plan #23              # Start fresh implementation
/execute-plan #23 --resume     # Resume after interruption
/execute-plan --skip-task 3    # Skip specific task (rare)
```

**Options:**
- `[issue-number]` - Optional, inferred from branch if omitted
- `--resume` - Resume from last incomplete task
- `--skip-task N` - Skip task N (use cautiously)
- `--dry-run` - Preview workflow without executing

## AI Execution Instructions

**CRITICAL: Task creation and worktree path handling**

When executing `/execute-plan`, AI MUST follow this pattern:

### Step 1: Load Plan from Worktree (if exists)

```python
# Check plan metadata for worktree path
plan_file = f".claude/plans/active/issue-{issue_number}-plan.md"
plan_content = Read(plan_file)

# Extract worktree path from plan metadata
worktree_match = re.search(r'\*\*Worktree\*\*: (.+)', plan_content)
if worktree_match:
    worktree_path = worktree_match.group(1)
    # CRITICAL: Use worktree path for all operations
    plan_file = f"{worktree_path}/.claude/plans/active/issue-{issue_number}-plan.md"
```

### Step 2: Parse Tasks and Create Todos

```python
# Extract tasks from plan's ## Tasks section
tasks = parse_tasks_from_plan(plan_content)

# Create TaskCreate for each with dependencies
for i, task in enumerate(tasks):
    todo = TaskCreate(
        subject=task.title,
        description=task.details,
        activeForm=f"{task.verb}ing..."
    )

    # Add dependency: task i+1 blocked by task i
    if i > 0:
        TaskUpdate(todo.id, addBlockedBy=[previous_todo.id])
```

### Step 3: Execute Tasks Sequentially

```python
for task_id in task_ids:
    # Mark in progress
    TaskUpdate(task_id, status="in_progress")

    # Display context and guide implementation
    display_task_context(task)
    execute_or_guide_task(task)

    # Validate completion (tests, linting if applicable)
    validate_task_completion(task)

    # Mark completed
    TaskUpdate(task_id, status="completed")
```

### Step 4: Worktree Path Usage

**CRITICAL**: If worktree exists, ALL file operations use worktree path:

```python
# ✅ CORRECT
Read(f"{worktree_path}/src/component.tsx")
Edit(f"{worktree_path}/.claude/skills/skill/SKILL.md")
Bash(f'git -C "{worktree_path}" status')

# ❌ WRONG
Read("src/component.tsx")  # Uses main repo
Bash("git status")  # Missing -C flag
```

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

### Step 0: Issue Number Detection (Multi-Strategy)

If no issue number was provided as argument, use the shared detector module:

**Using the detector:**
```python
import sys
sys.path.insert(0, '.claude/skills/_scripts')

from framework.issue_detector import detect_issue_number

# Auto-detect with all 4 strategies + validation
issue_num = detect_issue_number(check_github=True, required=True)
# Returns: int (issue number) or raises IssueDetectionError
```

**Detection strategies (automatic, in order):**
1. **Extract from branch name** - `feature/137-python-shared-libs` → `137`
2. **Find single active plan** - If exactly 1 plan in `.claude/plans/active/`
3. **Extract from worktree path** - `ai-dev-137-python-shared-libs` → `137`
4. **Ask user** - Fallback prompt if all auto-detection fails

**For AI orchestration:**
When the user provides no issue number:
```markdown
1. Call detector: python -c "import sys; sys.path.insert(0, '.claude/skills/_scripts'); from framework.issue_detector import detect_issue_number; print(detect_issue_number())"
2. Capture issue number from output
3. If detection fails and user input needed:
   - Use AskUserQuestion tool to ask for issue number
   - Validate plan exists: .claude/plans/active/issue-{N}-plan.md
4. Continue with detected/provided issue number
```

**Plan file path:**
```bash
PLAN_FILE=".claude/plans/active/issue-${ISSUE_NUM}-plan.md"
```

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
- [ ] Read execute-plan/SKILL.md
- [ ] Create REFERENCE.md
- [ ] Update SKILL.md with links
```

Creates 3 linked todos:
- Task #1: "Read execute-plan/SKILL.md"
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

**Output mode detection**:
- **Auto mode** (called by /work-issue): Minimal 2-line output
- **Interactive mode** (direct invocation): Concise summary ≤20 lines

**Auto mode output**:
```python
is_auto_mode = os.path.exists('.claude/.work-issue-state.json')

if is_auto_mode:
    print(f"✅ Plan executed: {completed_tasks}/{total_tasks} tasks | {files_changed} files changed")
    print(f"Next: /review")
else:
    # Interactive mode - show concise summary
    print(f"""
🎉 Development Complete!

Issue #{issue_number}: {title}
Tasks: {completed_tasks}/{total_tasks} ✅
Files changed: {files_changed}
Tests: {test_status}

Next: /review → /finish-issue #{issue_number}
""")
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
3. Execute task 1: "Read execute-plan/SKILL.md" → provides summary
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
2. /execute-plan #23       - Execute plan (30 min - 2 hrs) ← THIS SKILL
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

## Worktree Support

If the issue was started with `/start-issue` and a worktree was created, all operations MUST use the worktree path.

### Auto-Detection

1. **Read plan file** to get worktree path:
   ```bash
   PLAN_FILE=".claude/plans/active/issue-${ISSUE_NUM}-plan.md"
   WORKTREE_PATH=$(grep "^**Worktree**:" "$PLAN_FILE" | cut -d' ' -f2)
   ```

2. **If worktree path exists**, use it for ALL operations
3. **If no worktree path**, use current directory (backward compatibility)

### File Operations with Worktree

**Always use absolute paths** when worktree is detected:

```bash
# Read files
Read ${WORKTREE_PATH}/.claude/plans/active/issue-117-plan.md
Read ${WORKTREE_PATH}/.claude/skills/execute-plan/SKILL.md
Read ${WORKTREE_PATH}/src/components/Button.tsx

# Edit files
Edit ${WORKTREE_PATH}/.claude/skills/start-issue/SKILL.md
Edit ${WORKTREE_PATH}/src/utils/helpers.ts

# Write new files
Write ${WORKTREE_PATH}/src/services/new-service.ts

# Git operations (use -C flag)
git -C ${WORKTREE_PATH} status
git -C ${WORKTREE_PATH} add .
git -C ${WORKTREE_PATH} diff

# Run commands in worktree context
cd ${WORKTREE_PATH} && npm test
# OR
npm --prefix ${WORKTREE_PATH} test
```

### Example: Full Task Execution

```markdown
## Task 1: Update start-issue SKILL.md

# ✅ CORRECT - Uses worktree path
Read /Users/woo/dev/ai-dev-117-auto-detect-worktree/.claude/skills/start-issue/SKILL.md
Edit /Users/woo/dev/ai-dev-117-auto-detect-worktree/.claude/skills/start-issue/SKILL.md

# ❌ WRONG - Uses relative path or main repo
Read .claude/skills/start-issue/SKILL.md
Edit /Users/woo/dev/ai-dev/.claude/skills/start-issue/SKILL.md
```

### Fallback Behavior

If no worktree path found in plan metadata:
- ✅ Use current working directory (traditional workflow)
- ✅ Relative paths work as before
- ✅ Backward compatible with non-worktree setups

**This ensures the skill works correctly whether or not worktrees are used.**

---

## Final Verification

**Critical checks before completion:**

```
- [ ] All plan tasks completed
- [ ] Todo list all marked completed
- [ ] Git status shows only expected changes
- [ ] No unintended file modifications
- [ ] Ready for /review phase
```

If any item fails, address before completing execution.

## Workflow Skills Requirements

This is a **workflow skill** and must follow the standard pattern:

1. **TaskCreate** at start - Create todo list from plan tasks
2. **TaskUpdate** during execution - Mark tasks as completed
3. **Verification checklist** - Final validation before completion

**See**: [WORKFLOW_PATTERNS.md](../WORKFLOW_PATTERNS.md) for complete implementation guide

## Related Skills

- **/start-issue** - Creates branch and plan (Phase 1 - run before this)
- **/eval-plan** - Validates plan quality (Phase 1.5 - recommended before execution)
- **/review** - Quality validation (Phase 2.5 - run after this)
- **/finish-issue** - Commit and close issue (Phase 3 - final step)
- **/next** - Get single next task (lighter alternative)

## Advanced Topics

For detailed guidance on:
- **TDD Workflow** - Test-first development approach
- **Architecture Documentation** - When and how to document design
- **Complex Task Patterns** - Multi-file refactoring, API changes
- **State Recovery** - Handling interruptions and resuming

**See**: [REFERENCE.md](REFERENCE.md) for complete details

---

**Version:** 3.1.0
**Pattern:** Workflow Orchestrator (executes plan step-by-step)
**Compliance:** ADR-001 ✅ | WORKFLOW_PATTERNS.md ✅
**Last Updated:** 2026-03-18
**Changelog:**
- v3.1.0: Added mode-aware output (2 lines auto, ≤20 lines interactive) (Issue #263)
- v3.0.0: Worktree support and task execution
- v2.0.0: Added progress tracking
