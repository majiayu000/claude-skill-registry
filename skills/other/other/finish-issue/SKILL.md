---
name: finish-issue
description: |
  Complete issue workflow - commit, PR, merge, close, cleanup.
version: "3.1.0"

  TRIGGER when: User wants to complete/finish an issue ("finish issue #23", "complete issue", "merge and close", "done with issue").

  DO NOT TRIGGER when: User just wants to create issues (use /start-issue), review code (use /review), or manually commit changes.
user-invocable: true
argument-hint: "[issue-number] [--keep-branch] [--no-merge] [--dry-run] [--force]"
context: fork
---

# Finish Issue - Complete Issue Lifecycle

> Automates the final phase: commit, PR, merge, close, and cleanup

## Overview

This skill completes the issue lifecycle by automating 6 final steps:

**What it does:**
1. **Pre-Finish Validation** - Quality gates (tests, linting, review status)
2. **Commit & Push** - Commits all changes with semantic message
3. **Create PR** - Generates pull request with issue context
4. **Merge PR** - Merges after checks pass (optional)
5. **Close Issue** - Marks issue as done on GitHub
6. **Cleanup** - Deletes branches and temporary files

**Why it's needed:**
Manually finishing an issue requires 10+ commands (git, gh CLI) and takes 5-10 minutes. This skill automates everything in ~2 minutes with built-in safety checks.

**When to use:**
- After completing implementation and code review
- Ready to merge your feature branch
- Want automated PR creation and merging

**Three ways to use:**
1. **Manual**: Run git/gh commands yourself
2. **Script**: `python .claude/skills/finish-issue/scripts/finish.py 97`
3. **AI**: Say "finish issue #97" - Claude orchestrates the workflow

## Arguments

```bash
/finish-issue [issue-number] [options]
```

**Common usage:**
```bash
/finish-issue              # Auto-detect from branch
/finish-issue 97           # Specific issue
/finish-issue 97 --dry-run # Preview without executing
```

**Options:**
- `[issue-number]` - Optional, auto-detected from branch if omitted
- `--keep-branch` - Don't delete branch after merge
- `--no-merge` - Create PR but don't auto-merge
- `--dry-run` - Show what would happen without executing
- `--force` - Skip validation checks (use cautiously)

## AI Execution Instructions

**CRITICAL: Immediate Issue Detection**

When `/finish-issue` is invoked, AI MUST follow this pattern:

### Step 1: Detect Issue Number Immediately

**Before creating any tasks or introducing the skill**, determine which issue to finish:

```python
# Priority 1: Check if issue number provided as argument
if args:
    issue_num = args  # Use explicit argument
else:
    # Priority 2: Check conversation context/memory for active issue
    # Look for recently mentioned issue numbers in conversation
    # Example patterns to detect:
    # - "issue #158"
    # - "working on issue 158"
    # - "just completed #158"
    # - Recent /start-issue, /execute-plan, /review commands with issue number

    if issue_in_context:
        issue_num = detected_issue_from_context
    else:
        # Priority 3: Use issue detector (branch name, active plan, worktree)
        try:
            import sys
            sys.path.insert(0, '.claude/skills/_scripts')
            from framework.issue_detector import detect_issue_number
            issue_num = detect_issue_number(check_github=True, required=False)
        except:
            issue_num = None

        # Priority 4: Ask user if all detection fails
        if not issue_num:
            issue_num = AskUserQuestion(
                questions=[{
                    "question": "Which issue should I finish?",
                    "header": "Issue Number",
                    "options": [
                        {"label": "Enter manually", "description": "Type the issue number"}
                    ],
                    "multiSelect": false
                }]
            )
```

**What NOT to do:**
- ❌ Don't introduce the skill with overview text
- ❌ Don't show "Complete issue workflow - commit, PR, merge..." preamble
- ❌ Don't wait for user to specify issue if context already has it

**Expected behavior:**
1. Skill invoked → Immediately detect issue number
2. If recent context mentions issue (like issue #158 just worked on) → Use it
3. If no context → Try auto-detection from branch/plan
4. If detection fails → Ask user "Which issue should I finish?"
5. Once issue number determined → Create tasks and execute

### Step 2: Create Task List and Execute

**After** issue number is determined, proceed with normal workflow:

## Output Strategy (Mode-Aware)

**Output adapts based on mode:**

### Auto Mode Output (2 lines)

When called by `/work-issue --auto`:

```
✅ Issue #{issue_number} finished | PR #{pr_number} merged
Cleanup: Branch deleted, worktree removed, status files cleared
```

### Interactive Mode Output (≤20 lines)

When called directly by user:

```markdown
🎉 Issue #{issue_number} Complete!

✅ Committed and pushed
✅ PR #{pr_number} created and merged
✅ Issue closed on GitHub
✅ Branch deleted
✅ Worktree removed
✅ Status files cleaned

Back on: main branch (up to date)
```

## Workflow Steps (AI Orchestration)

Copy this checklist when executing:

```
Task Progress:
- [ ] Step 1: Pre-Finish Validation
- [ ] Step 2: Commit & Push
- [ ] Step 3: Create Pull Request
- [ ] Step 4: Merge Pull Request
- [ ] Step 5: Close Issue
- [ ] Step 6: Cleanup
```

Execute these steps in sequence using the Python script or manual commands.

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

**Python script integration:**
The `finish.py` script now uses the shared detector instead of its own `extract_issue_number()` function:
```bash
# Auto-detect (recommended)
python .claude/skills/finish-issue/scripts/finish.py

# Explicit issue number (still supported)
python .claude/skills/finish-issue/scripts/finish.py 137
```

**For AI orchestration:**
When the user provides no issue number:
```markdown
1. Call detector: python -c "import sys; sys.path.insert(0, '.claude/skills/_scripts'); from framework.issue_detector import detect_issue_number; print(detect_issue_number())"
2. Capture issue number from output
3. If detection fails and user input needed:
   - Use AskUserQuestion tool to ask for issue number
   - Validate issue exists on GitHub: gh issue view {N}
4. Continue with detected/provided issue number
```

### Step 1: Pre-Finish Validation

**Quality gates to check:**

```bash
# Check review status
cat .claude/.review-status.json

# Check for uncommitted changes
git status --porcelain

# Check branch is not main
git rev-parse --abbrev-ref HEAD

# Verify tests pass (if applicable)
npm test 2>/dev/null || echo "No tests configured"

# Check synced with main
python .claude/skills/finish-issue/scripts/check_sync.py
```

**Using the script:**
```bash
# Validation happens automatically
python .claude/skills/finish-issue/scripts/finish.py 97
```

**Validation checklist:**
- ✅ Not on main branch
- ✅ No uncommitted changes
- ✅ Review status exists (score ≥ 90 recommended)
- ✅ Tests passing (if applicable)
- ✅ Branch synced with main

**If validation fails:**
- Commit changes: `git add . && git commit -m "..."`
- Run review: `/review`
- Sync branch: `/sync`
- Override: Use `--force` (not recommended)

### Step 2: Commit & Push

**Auto-commit all changes:**

```bash
# Manual approach
git add -A
git commit -m "feat: implement feature (Issue #97)

Closes #97

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
git push

# Script approach (automatic)
python finish.py 97
```

**Commit message format:**
- Type determined from issue title (feat/fix/docs/test/refactor)
- Title from GitHub issue
- Includes "Closes #N"
- Co-authored by Claude

### Step 3: Create Pull Request

**Create PR with context:**

```bash
# Manual approach
gh pr create \
  --title "feat: implement feature (Issue #97)" \
  --body "## Summary

Completes issue #97

## Changes
...

🤖 Generated with Claude Code"

# Script approach (automatic)
# PR created automatically in finish.py
```

**PR includes:**
- Issue number in title
- Summary section
- Changes description
- Claude Code attribution

### Step 4: Merge Pull Request

**Merge with squash:**

```bash
# Manual approach
gh pr merge --squash --delete-branch

# Script approach (automatic, unless --no-merge)
python finish.py 97

# Skip merging
python finish.py 97 --no-merge
```

**Merge strategy:** Squash commit (clean history)

**Branch deletion:** Automatic (unless `--keep-branch`)

### Step 5: Close Issue

**Close with completion comment:**

```bash
# Manual approach
gh issue close 97 --comment "✅ Completed in PR #109"

# Script approach (automatic)
# Issue closed automatically in finish.py
```

### Step 6: Cleanup

**Clean up environment:**

```bash
# Manual approach
git checkout main
git pull

# Delete all workflow state files
rm -f .claude/.work-issue-state.json
rm -f .claude/.eval-plan-status.json
rm -f .claude/.review-status.json

# Script approach (automatic)
# Cleanup happens automatically in finish.py
```

**Cleanup actions:**
- Switch to main branch
- Pull latest changes
- **Archive plan file** (IMPORTANT):
  - Move `.claude/plans/active/issue-{N}-plan.md` → `.claude/plans/archive/`
  - Preserves history for future reference
  - Do NOT delete plan files
- Delete workflow state files:
  - `.claude/.work-issue-state.json` (workflow progress)
  - `.claude/.eval-plan-status.json` (plan validation results)
  - `.claude/.review-status.json` (code review results)
- Delete all issue-related tasks/todos created during workflow
- Delete local feature branch (if merged)
- Remove worktree directory (if used)

**AI Orchestration - Archive Plan File:**

When finishing an issue via AI orchestration, **MUST** archive the plan file (do NOT delete):

```python
import shutil
from pathlib import Path

# Archive plan file
issue_number = 154  # Detected issue number
plan_file = Path(f".claude/plans/active/issue-{issue_number}-plan.md")
archive_dir = Path(".claude/plans/archive")

if plan_file.exists():
    # Ensure archive directory exists
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Move plan to archive
    archive_path = archive_dir / plan_file.name
    shutil.move(str(plan_file), str(archive_path))

    print(f"✅ Plan archived: {archive_path}")
else:
    print(f"ℹ️ Plan file not found: {plan_file}")
```

**CRITICAL**: Do NOT delete plan files. Always move to archive for historical reference.

**AI Orchestration - Cleanup Tasks/Todos:**

When finishing an issue via AI orchestration, **MUST** clean up all tasks created during the workflow:

```python
# After all other cleanup steps, delete all issue-related todos
# Use TaskList to get all tasks, then delete them

from typing import List

# Step 1: Get all current tasks
task_list = TaskList()

# Step 2: Delete each task (set status to deleted)
for task in task_list:
    try:
        TaskUpdate(task_id=task.id, status="deleted")
    except Exception as e:
        # Task may already be deleted, continue
        pass

print("✅ All tasks/todos cleaned up")
```

**Important:** This cleanup ensures no stale tasks remain after issue completion. All tasks created during phases (start-issue, eval-plan, execute-plan, review, finish-issue) are removed.

## Task Management (AI Orchestration)

When executing via AI orchestration, use TaskCreate/TaskUpdate:

**Create tasks at start:**
```python
tasks = [
    "Pre-Finish Validation",
    "Commit & Push",
    "Create Pull Request",
    "Merge Pull Request",
    "Close Issue",
    "Cleanup"
]

for task in tasks:
    TaskCreate(
        subject=f"Step N: {task}",
        description="...",
        activeForm=f"{task}ing..."
    )
```

**Update during execution:**
```python
# Mark task in progress
TaskUpdate(task_id=1, status="in_progress")

# Execute step
execute_step_1()

# Mark complete
TaskUpdate(task_id=1, status="completed")

# Move to next
TaskUpdate(task_id=2, status="in_progress")
```

**Final verification:**
```markdown
- [ ] All 6 tasks completed
- [ ] PR merged to main
- [ ] Issue closed on GitHub
- [ ] Branches cleaned up
- [ ] Status files deleted
- [ ] All issue-related tasks/todos deleted
- [ ] On main branch
```

## Three Usage Modes

### Mode 1: Manual Execution

**Run git/gh commands yourself:**

```bash
# 1. Validate
git status
cat .claude/.review-status.json

# 2. Commit
git add -A
git commit -m "feat: ..."
git push

# 3. PR
gh pr create --title "..." --body "..."

# 4. Merge
gh pr merge --squash --delete-branch

# 5. Close
gh issue close 97 --comment "✅ Completed"

# 6. Cleanup
git checkout main && git pull

# Archive plan file (create directory if needed)
mkdir -p .claude/plans/archive
mv .claude/plans/active/issue-97-plan.md .claude/plans/archive/

# Delete state files
rm -f .claude/.review-status.json
rm -f .claude/.work-issue-state.json
rm -f .claude/.eval-plan-status.json
```

**When to use:**
- Need full control
- Complex merge conflicts
- Non-standard workflow

### Mode 2: Script Execution

**Run Python script:**

```bash
# Basic
python .claude/skills/finish-issue/scripts/finish.py 97

# With options
python finish.py 97 --dry-run      # Preview
python finish.py 97 --no-merge     # Skip auto-merge
python finish.py 97 --keep-branch  # Keep branch

# Auto-detect issue from branch
python finish.py
```

**When to use:**
- Want automation
- Standard workflow
- Trust validation

### Mode 3: AI Orchestration

**Tell Claude to finish:**

```
User: "finish issue #97"

Claude:
1. Creates task list (6 tasks)
2. Calls: python finish.py 97
3. Updates tasks as script executes
4. Reports completion
```

**When to use:**
- Prefer conversational interface
- Want progress tracking
- Claude handles errors

## Error Handling

**Common errors and solutions:**

**Not on feature branch:**
```
❌ Cannot finish from main branch

Fix: git checkout feature/97-...
```

**Uncommitted changes:**
```
❌ Uncommitted changes detected

Fix: git add . && git commit -m "..."
```

**No review status:**
```
⚠️ No review status found

Fix: /review
Or: python finish.py 97 --force
```

**PR already exists:**
```
⚠️ PR may already exist

Check: gh pr list
Merge: gh pr merge <number> --squash
```

**Merge conflicts:**
```
❌ Merge conflict detected

Fix:
1. Sync with main: /sync
2. Resolve conflicts
3. Re-run: python finish.py 97
```

## Examples

### Example 1: Basic Finish

**User:** "finish issue #97"

**Claude orchestrates:**
```python
# 1. Create task list
create_tasks([...])

# 2. Execute script
run_command("python finish.py 97")

# 3. Update progress
# Script output shows each step completion

# 4. Report
"✅ Issue #97 finished successfully!"
```

**Time:** ~2 minutes

### Example 2: Preview with Dry Run

**User:** "show me what would happen if I finish issue #97"

**Execute:**
```bash
python finish.py 97 --dry-run
```

**Output:**
```
🔍 DRY RUN - Would execute:
  1. Commit & Push changes
  2. Create pull request
  3. Merge pull request
  4. Close issue
  5. Delete branches
  6. Cleanup
```

**Time:** <10 seconds

### Example 3: Create PR Without Merging

**User:** "create PR for issue #97 but don't merge yet"

**Execute:**
```bash
python finish.py 97 --no-merge
```

**Result:**
- ✅ PR created
- ⏭️  Merge skipped
- ✅ Issue closed
- Branch kept for manual review

## Integration

**Workflow sequence:**
```
/start-issue #97    → Branch + plan
/execute-plan #97   → Implementation
/review             → Quality check
/finish-issue #97   → Merge + close (THIS SKILL)
```

**Or complete lifecycle:**
```
/work-issue #97
  → Calls /start-issue
  → Calls /eval-plan
  → Calls /execute-plan
  → Calls /review
  → Calls /finish-issue (automatic)
```

## Best Practices

1. **Always review first** - Run `/review` before finishing
2. **Check dry-run** - Preview with `--dry-run` if unsure
3. **Sync before finish** - Run `/sync` to avoid conflicts
4. **Trust validation** - Fix issues instead of using `--force`
5. **Use auto-detect** - Let script infer issue from branch

## Performance

- **Validation**: <5 seconds
- **Commit + Push**: ~10 seconds
- **PR creation**: ~5 seconds
- **Merge**: ~30 seconds
- **Cleanup**: ~5 seconds
- **Total**: ~1-2 minutes

Fast because:
- Automated validation (no manual checks)
- Parallel GitHub operations
- Efficient git commands

## Worktree Support

If the issue was started with `/start-issue` and a worktree was created, all git operations MUST use the worktree path.

### Auto-Detection

**Read plan metadata** to get worktree path:
```bash
PLAN_FILE=".claude/plans/active/issue-${ISSUE_NUM}-plan.md"
WORKTREE_PATH=$(grep "^**Worktree**:" "$PLAN_FILE" | cut -d' ' -f2)
```

### Git Operations with Worktree

**All git commands must use `-C` flag** to operate in worktree directory:

```bash
# Check status
git -C ${WORKTREE_PATH} status

# Stage changes
git -C ${WORKTREE_PATH} add .

# Commit
git -C ${WORKTREE_PATH} commit -m "feat: implement feature"

# Push
git -C ${WORKTREE_PATH} push origin feature/117-...

# Create PR (gh works from worktree)
cd ${WORKTREE_PATH} && gh pr create --title "..." --body "..."
# OR
gh pr create --repo owner/repo --head feature/117-... --title "..." --body "..."
```

### Cleanup with Worktree

After merging PR and closing issue:

```bash
# 1. Switch back to main repo
cd ${MAIN_REPO_PATH}  # e.g., /Users/woo/dev/ai-dev

# 2. Remove worktree
git worktree remove ${WORKTREE_PATH}
# OR (if worktree has uncommitted changes)
git worktree remove --force ${WORKTREE_PATH}

# 3. Delete local branch (already deleted remotely)
git branch -D feature/117-...

# 4. Pull latest main
git checkout main
git pull origin main
```

### Fallback Behavior

If no worktree path found:
- ✅ Use standard git commands (current directory)
- ✅ No `-C` flag needed
- ✅ Backward compatible with traditional workflow

**Note**: The skill should automatically detect worktree presence and adjust git commands accordingly.

---

## Final Verification

**Critical checks before completion:**

```
- [ ] Plan file archived (not deleted) to .claude/plans/archive/
- [ ] All 3 state files deleted (.work-issue-state, .eval-plan-status, .review-status)
- [ ] All todos cleaned up (TaskUpdate status="deleted")
- [ ] Worktree removed (if used)
- [ ] On main branch and up to date
```

Missing items indicate incomplete cleanup.

## Workflow Skills Requirements

This is a **workflow skill** and must follow the standard pattern:

1. **TaskCreate** at start - Create todo list for progress tracking
2. **TaskUpdate** during execution - Mark tasks in_progress → completed
3. **Verification checklist** - Final validation before completion

**See**: [WORKFLOW_PATTERNS.md](../WORKFLOW_PATTERNS.md) for complete implementation guide

---

## Related Skills

- **/start-issue** - Phase 1: Begin issue workflow
- **/eval-plan** - Phase 1.5: Validate plan
- **/execute-plan** - Phase 2: Implementation
- **/review** - Phase 2.5: Quality check
- **/work-issue** - Complete lifecycle (calls this skill)
- **/sync** - Sync branch with main

---

**Version:** 3.1.0
**Pattern:** Workflow Orchestrator (AI-guided + Script)
**Compliance:** ADR-001 ✅ | ADR-003 ✅ | WORKFLOW_PATTERNS ✅
**Last Updated:** 2026-03-18
**Changelog:**
- v3.1.0: Added mode-aware output (2 lines auto, ≤20 lines interactive) (Issue #263)
- v3.0.0: Complete rewrite with Python script + AI orchestration
- v2.0.0: Added workflow pattern compliance
- v1.0.0: Initial release
