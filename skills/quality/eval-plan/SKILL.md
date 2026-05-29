---
name: eval-plan
description: |
  Evaluate implementation plan before execution - validates architecture, coverage, dependencies, and best practices.
  TRIGGER when: user wants plan validated ("evaluate plan", "check plan", "validate plan", "review the plan before starting").
  DO NOT TRIGGER when: user wants to execute plan (use /execute-plan), create plan (use /start-issue or /plan), or review code (use /review).
version: "1.3.0"
argument-hint: "[issue-number] [--strict] [--json]"
allowed-tools: Bash(gh *), Read, Glob, Grep
disable-model-invocation: false
user-invocable: true
---

# Eval Plan - Implementation Plan Validator

Validate implementation plans before execution to catch issues early and prevent costly rework.

## Overview

This skill provides automated plan validation by checking:

**What it does:**
1. **Architecture alignment** - Validates against .claude/rules/architecture/
2. **Acceptance criteria coverage** - Ensures all issue requirements addressed
3. **Task dependencies** - Validates correct ordering and relationships
4. **Best practices** - Checks for error handling, docs, logging, tests
5. **Task clarity** - Ensures tasks are specific and actionable
6. **Generates scored evaluation** - 0-100 score with actionable feedback
7. **Writes status file** - For /work-issue integration

**Why it's needed:**
Manual plan review misses systematic issues like architecture violations, missing requirements, and dependency problems. These surface during implementation (Phase 2) causing 60+ minutes of rework. This skill catches issues before coding starts.

**When to use:**
- After /start-issue creates a plan
- Before /execute-plan begins implementation
- Automatically in /work-issue as Phase 1.5
- Anytime you want plan validation

**Value proposition:**
- Catches architecture violations before implementation
- Ensures requirement coverage (prevents incomplete PRs)
- Validates task ordering (prevents implementation stalls)
- Reminds of best practices (error handling, docs, logging)
- Fast (30-60 seconds) vs high impact (prevents hours of rework)

## Arguments

```bash
/eval-plan [issue-number] [options]
```

**Common usage:**
```bash
/eval-plan              # Evaluate plan for current branch
/eval-plan #23          # Evaluate specific issue's plan
/eval-plan --strict     # Fail on recommendations (not just blocking)
/eval-plan --json       # Output JSON only (for automation)
/eval-plan --mode=auto  # Auto-fix minor issues when score ≥90 (used by work-issue --auto)
```

**Options:**
- `[issue-number]` - Optional, inferred from branch if omitted
- `--strict` - Treat recommendations as blocking issues
- `--json` - Output JSON format only (no human-readable summary)
- `--mode=auto` - Enable auto-fix mode for minor issues (requires score ≥90)

## AI Execution Instructions

**CRITICAL: Evaluation scoring and status file**

When executing `/eval-plan`, AI MUST follow this pattern:

### Step 1: Create 8 Evaluation Tasks

```python
tasks = [
    TaskCreate(subject="Load plan file", ...),
    TaskCreate(subject="Evaluate architecture alignment", ...),
    TaskCreate(subject="Check acceptance criteria coverage", ...),
    TaskCreate(subject="Validate task dependencies", ...),
    TaskCreate(subject="Assess best practices", ...),
    TaskCreate(subject="Check task clarity", ...),
    TaskCreate(subject="Generate scored report", ...),
    TaskCreate(subject="Write status file", ...)
]
```

### Step 2: Load Plan from Worktree

```python
# Check plan metadata for worktree path
plan_file = f".claude/plans/active/issue-{issue_number}-plan.md"
worktree_path = extract_worktree_from_plan(plan_file)

if worktree_path:
    # CRITICAL: Read plan from worktree
    plan_file = f"{worktree_path}/.claude/plans/active/issue-{issue_number}-plan.md"

plan_content = Read(plan_file)
```

### Step 3: Evaluate 5 Dimensions

```python
scores = {
    "architecture": evaluate_architecture(plan, max=40),
    "coverage": evaluate_coverage(plan, issue, max=30),
    "dependencies": evaluate_dependencies(plan, max=15),
    "practices": evaluate_practices(plan, max=10),
    "clarity": evaluate_clarity(plan, max=5)
}

total_score = sum(scores.values())  # Max 100
```

### Step 4: Write Status File

**CRITICAL**: Always write `.claude/.eval-plan-status.json`:

```python
import json
from datetime import datetime, timedelta

status = {
    "timestamp": datetime.now().isoformat(),
    "issue_number": issue_number,
    "status": "approved" if total_score > 90 else "needs_improvement" if total_score >= 70 else "rejected",
    "score": total_score,
    "breakdown": scores,
    "issues_count": {
        "blocking": len(blocking_issues),
        "recommendations": len(recommendations),
        "suggestions": len(suggestions)
    },
    "valid_until": (datetime.now() + timedelta(minutes=90)).isoformat(),
    "plan_file": plan_file
}

with open(".claude/.eval-plan-status.json", "w") as f:
    json.dump(status, f, indent=2)
```

### Step 4.5: Auto-Fix (if --mode=auto and score ≥90)

**CRITICAL**: Apply auto-fixes when in auto mode with passing score:

```python
def auto_fix_if_applicable(mode, score, issues, plan_content, plan_file):
    """
    自动修复微小问题（仅在 auto 模式且分数 ≥90 时）
    """
    # 检查是否启用自动修复
    if mode != "auto" or score < 90:
        return plan_content, []  # 不修复

    # 分类问题：微小 vs 重大
    minor_issues = [i for i in issues if i.category in AUTO_FIXABLE]
    major_issues = [i for i in issues if i.category not in AUTO_FIXABLE]

    if not minor_issues:
        return plan_content, []  # 无需修复

    # 应用修复
    fixes_applied = []
    content = plan_content

    try:
        for issue in minor_issues:
            fixer = FIXERS[issue.category]
            content, fix_log = fixer(content, issue)
            fixes_applied.append(fix_log)

        # 写入修复后的计划
        Write(plan_file, content)

        # 重新评估（可选，验证修复效果）
        new_score = evaluate_plan(content)

        return content, fixes_applied, new_score

    except Exception as e:
        # 优雅降级：修复失败，返回原内容
        log.error(f"Auto-fix failed: {e}")
        return plan_content, [], score

# 修复器定义
AUTO_FIXABLE = {
    "missing_todo",
    "incomplete_test",
    "format_issue",
    "missing_file_ref",
    "logic_gap"
}

FIXERS = {
    "missing_todo": lambda content, issue: add_todo_comment(content, issue),
    "incomplete_test": lambda content, issue: expand_test_description(content, issue),
    "format_issue": lambda content, issue: fix_task_numbering(content),
    "missing_file_ref": lambda content, issue: add_file_path(content, issue),
    "logic_gap": lambda content, issue: insert_missing_step(content, issue)
}
```

**Usage in eval-plan:**
```python
# After Step 3: Evaluation complete
score, issues = evaluate_plan(plan_content)

# Step 4: Write initial status file
write_status_file(score, issues)

# Step 4.5: Auto-fix if applicable
if mode == "auto" and score >= 90:
    fixed_content, fixes, new_score = auto_fix_if_applicable(
        mode, score, issues, plan_content, plan_file
    )

    # Update status file with auto-fix results
    update_status_file({
        "score": new_score,
        "score_before_autofix": score,
        "auto_fixes_applied": fixes
    })

    # Report auto-fixes to user
    report_auto_fixes(fixes, score, new_score)
```

### Step 5: Generate Output (Mode-Aware)

**Output mode detection**:
- **Auto mode** (--mode=auto or called by /work-issue): Minimal 2-line output
- **Interactive mode** (direct invocation): Concise summary ≤20 lines

**Auto mode output**:
```python
is_auto_mode = args.get('mode') == 'auto' or os.path.exists('.claude/.work-issue-state.json')

if is_auto_mode:
    print(f"✅ Plan evaluation: {total_score}/100 ({status})")
    print(f"Status: .claude/.eval-plan-status.json")
else:
    # Interactive mode - show concise summary (see "Evaluation Output" section)
    print_concise_summary(scores, issues)
```

**Concise summary format** (interactive mode, max 20 lines):
```markdown
# Plan Evaluation: Issue #{issue_number}

Score: {score}/100 ({status})
Issues: {blocking} blocking, {recommendations} recommendations

{Top 3 issues only}

Status file: .claude/.eval-plan-status.json
```

### Step 6: Task Updates

```python
for task_id in task_ids:
    TaskUpdate(task_id, status="in_progress")
    # ... execute evaluation dimension ...
    TaskUpdate(task_id, status="completed")
```

## Workflow Steps

Copy this checklist when executing:

```
Task Progress:
- [ ] Step 1: Load plan file
- [ ] Step 2: Evaluate architecture alignment
- [ ] Step 3: Check acceptance criteria coverage
- [ ] Step 4: Validate task dependencies
- [ ] Step 5: Assess best practices
- [ ] Step 6: Check task clarity
- [ ] Step 7: Generate scored report
- [ ] Step 8: Write status file
- [ ] Step 9: Auto-fix minor issues (if --mode=auto and score ≥90)
- [ ] Step 10: Report results
```

Execute these steps in sequence using TaskCreate/TaskUpdate for progress tracking.

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

## Evaluation Dimensions

### 1. Architecture Alignment (40 points)

**What it checks:**
- Module boundaries respected (clean architecture)
- Dependency direction correct (inward, not outward)
- Layer separation maintained (UI → Domain → Data)
- No architectural anti-patterns
- Consistent with .claude/rules/architecture/

**How to check:** Read .claude/rules/architecture/, review tasks for violations (UI → Domain → Data layers, dependency direction inward)

**Common violations:** DB query in React component, UI import in service layer, direct API calls from components

**Scoring:** 40=perfect, 30=minor issues, 20=some violations, 0-10=major problems

### 2. Acceptance Criteria Coverage (30 points)

**What it checks:**
- All issue acceptance criteria have corresponding tasks
- No criteria left unaddressed
- Tasks map clearly to requirements
- No scope creep (extra features not in criteria)

**How to check:** Extract criteria from issue, map each to tasks, flag missing coverage or scope creep

**Scoring:** 30=100% coverage, 25=90%+, 20=80%+, 10=<80%, 0=<50%

### 3. Task Dependencies (15 points)

**What it checks:**
- Tasks in topological order
- Dependencies come before dependents
- No circular dependencies
- Clear prerequisite relationships

**How to check:** Parse dependencies, build graph, check for cycles, verify topological order

**Common issues:** Test tasks before creation tasks, circular dependencies

**Scoring:** 15=perfect order, 10=minor issues, 5=several problems, 0=circular/chaos

### 4. Best Practices (10 points)

**What it checks:**
- Error handling strategy defined
- Documentation updates included
- Logging/monitoring considered
- Test coverage planned
- Security considerations addressed
- Performance implications reviewed

**Checks for:** Error handling, tests, docs, logging, security, performance tasks

**Scoring:** 10=all covered, 7=minor gaps, 4=several missing, 0=critical missing

### 5. Task Clarity (5 points)

**What it checks:**
- Tasks are specific and actionable
- No vague descriptions ("Add tests", "Fix bugs")
- Clear acceptance criteria per task
- Reasonable granularity (not too large/small)

**Checks:** Tasks specific and actionable, not vague ("Add tests" ❌, "Add unit tests for UserService with 80% coverage" ✅)

**Scoring:** 5=all clear, 3=mostly clear, 1=several vague, 0=mostly unclear

## Evaluation Output

**Output adapts based on mode:**

### Auto Mode Output (2 lines)

When called by `/work-issue --auto` or with `--mode=auto`:

```
✅ Plan evaluation: 92/100 (approved)
Status: .claude/.eval-plan-status.json
```

### Interactive Mode Output (≤20 lines)

When called directly by user:

```markdown
# Plan Evaluation: Issue #23

Score: 82/100 (needs_improvement)
Issues: 0 blocking, 3 recommendations

Top Issues:
1. Task 5 - Architecture violation: API in UI component
2. Missing error handling task
3. Task 3 - Dependency order incorrect

Full details: .claude/.eval-plan-status.json
Next: Edit plan or /execute-plan #23
```

### Full Report Format (status file only)

Complete evaluation stored in `.claude/.eval-plan-status.json`:

```json
{
  "timestamp": "2026-03-11T10:30:00Z",
  "issue_number": 23,
  "status": "needs_improvement",
  "score": 82,
  "breakdown": {
    "architecture": 35,
    "coverage": 25,
    "dependencies": 12,
    "practices": 7,
    "clarity": 3
  },
  "issues": {
    "blocking": [],
    "recommendations": [
      {
        "task": "Task 5",
        "category": "architecture",
        "description": "API endpoint in UI component violates clean architecture",
        "fix": "Move API call to service layer",
        "impact": "high"
      }
    ]
  }
}
```

### JSON Format (for automation)

```json
{
  "timestamp": "2026-03-11T10:30:00Z",
  "issue_number": 23,
  "issue_title": "Fix user authentication flow",
  "plan_file": ".claude/plans/active/issue-23-plan.md",
  "status": "needs_improvement",
  "score": 82,
  "breakdown": {
    "architecture": {
      "score": 35,
      "max": 40,
      "status": "pass"
    },
    "coverage": {
      "score": 25,
      "max": 30,
      "status": "pass"
    },
    "dependencies": {
      "score": 12,
      "max": 15,
      "status": "warning"
    },
    "practices": {
      "score": 7,
      "max": 10,
      "status": "warning"
    },
    "clarity": {
      "score": 3,
      "max": 5,
      "status": "warning"
    }
  },
  "issues": {
    "blocking": [],
    "recommendations": [
      {
        "task": "Task 5",
        "category": "architecture",
        "description": "API endpoint in UI component violates clean architecture",
        "fix": "Move API call to service layer",
        "impact": "high"
      },
      {
        "task": "Missing",
        "category": "best_practices",
        "description": "No error handling strategy",
        "fix": "Add error handling task",
        "impact": "high"
      },
      {
        "task": "Task 3",
        "category": "dependencies",
        "description": "Test task before service creation",
        "fix": "Swap order - create service first",
        "impact": "medium"
      }
    ],
    "suggestions": [
      "Add documentation update task",
      "Add logging for auth events",
      "Split Task 5 into smaller tasks"
    ]
  },
  "strengths": [
    "Clear task breakdown",
    "Good acceptance criteria mapping (90%)",
    "Test coverage included"
  ],
  "metrics": {
    "total_tasks": 8,
    "acceptance_criteria": 5,
    "coverage_percentage": 90,
    "estimated_complexity": "medium"
  },
  "valid_until": "2026-03-11T12:00:00Z"
}
```

## Status File for Integration

After evaluation, write `.claude/.eval-plan-status.json`:

```json
{
  "timestamp": "2026-03-11T10:30:00Z",
  "issue_number": 23,
  "status": "needs_improvement",
  "score": 82,
  "breakdown": {
    "architecture": 35,
    "coverage": 25,
    "dependencies": 12,
    "practices": 7,
    "clarity": 3
  },
  "issues_count": {
    "blocking": 0,
    "recommendations": 3,
    "suggestions": 3
  },
  "valid_until": "2026-03-11T12:00:00Z",
  "plan_file": ".claude/plans/active/issue-23-plan.md"
}
```

**Status values:**
- `"approved"` - Score > 90, no blocking issues
- `"needs_improvement"` - Score 70-90, recommendations present
- `"rejected"` - Score < 70, must fix before proceeding

**Validity:** 90 minutes from evaluation

## Auto-Fix Mode (NEW in v1.1.0)

**Purpose**: Automatically fix minor issues when score ≥90 in `--mode=auto`, enabling seamless continuation to execute-plan.

### When Auto-Fix Triggers

```
Conditions (ALL must be true):
1. Mode is --mode=auto (set by work-issue --auto)
2. Score ≥ 90 (passing threshold)
3. Issues are classified as "minor" (fixable)
```

### Auto-Fixable Issue Types

| Issue Type | Description | Example Fix |
|------------|-------------|-------------|
| **missing_todo** | Task mentions TODO but no TODO comment | Add `<!-- TODO: ... -->` comment |
| **incomplete_test** | "Add tests" without specifics | Add "Add unit tests (80% coverage): normal case, error case, edge cases" |
| **format_issue** | Task numbering gaps, inconsistent formatting | Renumber tasks 1→2→4→5 to 1→2→3→4 |
| **missing_file_ref** | "Update SKILL.md" without path | Add full path `.claude/skills/eval-plan/SKILL.md` |
| **logic_gap** | Missing obvious steps between tasks | Insert missing intermediate task |

### Non-Auto-Fixable Issues (Manual Review Required)

| Issue Type | Why Not Auto-Fixed | Action |
|------------|-------------------|--------|
| **architecture_violation** | Requires redesign | Stop at checkpoint |
| **missing_acceptance_criteria** | Requires PO/user input | Stop at checkpoint |
| **circular_dependency** | Requires re-planning | Stop at checkpoint |
| **security_issue** | Requires expert review | Stop at checkpoint |
| **performance_concern** | Requires benchmarking | Stop at checkpoint |

### Auto-Fix Workflow

```
1. eval-plan runs → Score = 92/100
2. Detect mode = auto (from --mode=auto argument)
3. Score ≥ 90 → Trigger auto-fix
4. Classify issues:
   - 2 × missing_todo → AUTO-FIX
   - 1 × format_issue → AUTO-FIX
   - 1 × suggestion (non-blocking) → SKIP
5. Apply fixes to plan file
6. Re-evaluate → New score = 95/100
7. Write status file with fix log
8. Report auto-fixes to user
9. Continue to execute-plan (seamless)
```

### Status File with Auto-Fix

Extended `.claude/.eval-plan-status.json`:

```json
{
  "timestamp": "2026-03-13T08:30:00Z",
  "issue_number": 177,
  "status": "approved",
  "score": 95,
  "score_before_autofix": 92,
  "auto_fixes_applied": [
    {
      "type": "missing_todo",
      "task": "Task 5",
      "description": "Added TODO comment for error handling",
      "before": "添加错误处理",
      "after": "添加错误处理\n<!-- TODO: Handle network errors, validation errors -->"
    },
    {
      "type": "format_issue",
      "description": "Renumbered tasks 1,2,4,5 → 1,2,3,4"
    }
  ],
  "issues_count": {
    "blocking": 0,
    "recommendations": 0,
    "suggestions": 1
  }
}
```

### Auto-Fix Example

**Before (Score 88/100):**
```markdown
## Tasks

1. 分析 eval-plan 结构
2. 添加自动修复逻辑
4. 添加错误处理  ← Gap in numbering
5. 更新文档  ← No file path specified
```

**Auto-Fixes Applied:**
1. Format issue: Renumber task 4→3, task 5→4
2. Missing file ref: "更新文档" → "更新 `.claude/skills/eval-plan/SKILL.md`"

**After (Score 95/100):**
```markdown
## Tasks

1. 分析 eval-plan 结构
2. 添加自动修复逻辑
3. 添加错误处理
4. 更新 `.claude/skills/eval-plan/SKILL.md`
```

### Graceful Degradation

**If auto-fix fails:**
```python
try:
    fixed_content, fixes = auto_fix_plan(content, issues)
    write_plan(fixed_content)
except AutoFixError as e:
    log.error(f"Auto-fix failed: {e}")
    # Fall back to interactive mode
    return prompt_user_checkpoint()
```

**Fallback behavior:**
- Show original evaluation results
- Prompt user for action (continue/edit/stop)
- Preserve original plan file
- Log failure reason

### Performance

- **Auto-fix time**: < 10 seconds
- **Total eval-plan time**: 40-70 seconds (was 30-60 seconds)
- **Impact**: +10 seconds for auto-fix, saves 5-60 minutes of manual editing

## Approval Thresholds

### ✅ Approved (Score > 90)
- All dimensions strong
- No blocking issues
- Minor suggestions only
- **Auto mode**: Proceed automatically
- **Interactive mode**: Show results, offer continue/edit/stop

### ⚠️ Needs Improvement (Score 70-90)
- Good foundation, some gaps
- Recommendations present (not blocking)
- Can proceed with awareness
- **Auto mode**: Stop at checkpoint if score ≤ 90
- **Interactive mode**: Always stop, show recommendations

### ❌ Rejected (Score < 70)
- Critical issues present
- Must fix before proceeding
- High rework risk
- **Both modes**: Stop, require fixes

## Integration with /work-issue

**Workflow:**
```
Phase 1: /start-issue #23 → Creates plan
Phase 1.5: /eval-plan → Automatic validation (THIS SKILL)
Checkpoint 1: Review eval results
  - Interactive mode: Always stop
  - Auto mode: Stop if score ≤ 90
Phase 2: /execute-plan #23 → Implementation
Phase 2.5: /review → Code validation
Checkpoint 2: Review quality
Phase 3: /finish-issue #23 → Ship
```

**Checkpoint 1 behavior:**
```markdown
📊 Plan Evaluation Results

Issue #23: Fix authentication flow
Score: 82/100 ⚠️ Needs improvements

Issues:
- Task 5: Architecture violation
- Missing: Error handling strategy
- Task 3: Dependency ordering

Options:
[C]ontinue anyway - proceed to implementation
[E]dit plan - fix issues and re-evaluate
[S]top here - pause workflow
[Q]uit - cancel workflow

Your choice: _
```

## Usage Examples

### Example 1: Excellent Plan (Score 95)
- All tasks specific and actionable
- Perfect layer separation (service → repository → tests)
- 100% acceptance criteria coverage
- **Result:** ✅ Approved immediately

### Example 2: Good Plan (Score 82)
- Good structure, minor gaps
- Task 2 unclear about service layer
- Missing error handling task
- **Result:** ⚠️ Approved with recommendations

### Example 3: Needs Work (Score 58)
- Vague tasks ("Fix authentication", "Add tests")
- No architecture guidance
- Can't verify criteria coverage
- **Result:** ❌ Rejected - needs revision

**See**: [REFERENCE.md](REFERENCE.md) for detailed examples

## Task Management (AI Orchestration)

When executing via AI orchestration, use TaskCreate/TaskUpdate:

**Create tasks at start:**
```python
tasks = [
    "Load plan file",
    "Evaluate architecture alignment",
    "Check acceptance criteria coverage",
    "Validate task dependencies",
    "Assess best practices",
    "Check task clarity",
    "Generate scored report",
    "Write status file"
]

for i, task in enumerate(tasks, 1):
    TaskCreate(
        subject=f"Step {i}: {task}",
        description=f"Evaluate {task.lower()} for the implementation plan",
        activeForm=f"{task}..."
    )
```

**Update during execution:**
```python
# Mark task in progress
TaskUpdate(task_id=1, status="in_progress")

# Execute evaluation step
execute_step_1()

# Mark complete
TaskUpdate(task_id=1, status="completed")

# Move to next
TaskUpdate(task_id=2, status="in_progress")
```

**Final verification:**
```markdown
- [ ] All 8 evaluation tasks completed
- [ ] Score calculated (0-100)
- [ ] Status file written (.claude/.eval-plan-status.json)
- [ ] Approval level determined (✅/⚠️/❌)
- [ ] Valid until timestamp set (90 min)
```

## Best Practices

1. **Run after /start-issue** - Validate auto-generated plans
2. **Fix recommendations** - Prevents rework during implementation
3. **Re-evaluate after edits** - Verify fixes improved score
4. **Trust the evaluation** - AI catches systematic issues humans miss
5. **Use in /work-issue** - Automatic integration recommended

## Worktree Support

If the issue was started with `/start-issue` and a worktree was created, all operations MUST use the worktree path.

### Auto-Detection

**Read plan file** to get worktree path:
```bash
PLAN_FILE=".claude/plans/active/issue-${ISSUE_NUM}-plan.md"
WORKTREE_PATH=$(grep "^**Worktree**:" "$PLAN_FILE" | cut -d' ' -f2)
```

If worktree path exists, use it for ALL file operations.

### File Operations with Worktree

**Always use absolute paths** when worktree is detected:

```bash
# ✅ CORRECT - Read plan from worktree
Read ${WORKTREE_PATH}/.claude/plans/active/issue-N-plan.md

# ✅ CORRECT - Check files in worktree
ls ${WORKTREE_PATH}/.claude/rules/

# ❌ WRONG - Reads main repo instead
Read .claude/plans/active/issue-N-plan.md
```

### Fallback Behavior

If no worktree path found in plan metadata:
- ✅ Use current working directory
- ✅ Relative paths work (backward compatibility)
- ✅ Standard workflow continues normally

**This ensures eval-plan works correctly whether or not worktrees are used.**

## Final Verification

**Critical checks before completion:**

```
- [ ] All 8 evaluation tasks completed
- [ ] Score calculated (0-100)
- [ ] Status file written (.claude/.eval-plan-status.json)
- [ ] Status file has valid_until timestamp (90 min)
- [ ] Approval level determined (approved/needs_improvement/rejected)
```

Missing items indicate incomplete evaluation.

## Workflow Skills Requirements

This is a **workflow skill** and must follow the standard pattern:

1. **TaskCreate** at start - Create todo list for progress tracking
2. **TaskUpdate** during execution - Mark tasks in_progress → completed
3. **Verification checklist** - Final validation before completion

**See**: [WORKFLOW_PATTERNS.md](../WORKFLOW_PATTERNS.md) for complete implementation guide

## Related Skills

- **/start-issue** - Creates plan (run before this)
- **/work-issue** - Calls this skill automatically in Phase 1.5
- **/execute-plan** - Executes plan (run after this)
- **/review** - Validates code (Phase 2.5 - symmetric validation)

---

**Version:** 1.3.0
**Pattern:** Analysis skill (validates before execution)
**Compliance:** ADR-001 ✅ | WORKFLOW_PATTERNS.md ✅
**Last Updated:** 2026-03-18
**Changelog:**
- v1.3.0: Added mode-aware output (2 lines auto, ≤20 lines interactive) (Issue #263)
- v1.2.0: Added auto-fix mode for minor issues when score ≥90 (Issue #177)
- v1.0.0: Initial release with 5-dimension evaluation
