---
name: faion-feature-executor
user-invocable: false
description: "SDD feature executor: sequential task execution with quality gates. Runs tests/coverage validation after each task, performs code review, iterates until all issues resolved. Integrates with faion-task-executor-agent."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, TodoWrite, AskUserQuestion
---

# Feature Executor Skill

**Communication: User's language. Docs/code: English.**

## Purpose

Execute all tasks in an SDD feature with full quality gates:
1. Load project and feature context
2. Execute tasks sequentially via `faion-task-executor-agent`
3. After each task: verify tests pass, coverage adequate, project runs
4. After all tasks: code review cycle until no issues remain
5. Move feature to `done/`

## Agents Used

| Agent | Purpose |
|-------|---------|
| `faion-task-executor-agent` | Execute individual tasks |
| `faion-code-agent` | Code review (review mode) |
| `faion-test-agent` | Test execution and coverage analysis |
| `faion-hallucination-checker-agent` | Verify task completion claims |

---

## Input

```
/faion-feature-executor {project} {feature}
```

**Examples:**
```
/faion-feature-executor cashflow-planner 01-auth
/faion-feature-executor faion-net 02-landing-page
```

**Parameters:**
- `project`: Project name (folder in `aidocs/sdd/`)
- `feature`: Feature name (folder in `features/{status}/`)

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FEATURE EXECUTOR                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. CONTEXT LOADING                                          │
│     ├─ constitution.md (project standards)                   │
│     ├─ spec.md (requirements)                                │
│     ├─ design.md (architecture)                              │
│     └─ implementation-plan.md (task breakdown)               │
│                                                              │
│  2. TASK DISCOVERY                                           │
│     ├─ in-progress/ (resume first)                          │
│     └─ todo/ (sorted by number)                             │
│                                                              │
│  3. TASK EXECUTION LOOP                                      │
│     ┌──────────────────────────────────────┐                │
│     │  For each task:                       │                │
│     │  ├─ Execute via faion-task-executor-agent  │                │
│     │  ├─ Run tests                        │                │
│     │  ├─ Check coverage                   │                │
│     │  ├─ Verify project runs              │                │
│     │  └─ If fails → fix → retry (max 3)   │                │
│     └──────────────────────────────────────┘                │
│                                                              │
│  4. CODE REVIEW CYCLE                                        │
│     ┌──────────────────────────────────────┐                │
│     │  Loop until no issues:               │                │
│     │  ├─ Run code review                  │                │
│     │  ├─ Fix ALL issues                   │                │
│     │  ├─ Re-run review                    │                │
│     │  └─ Repeat until clean               │                │
│     └──────────────────────────────────────┘                │
│                                                              │
│  5. FINALIZE                                                 │
│     ├─ Move feature to done/                                │
│     └─ Generate summary report                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Context Loading

### 1.1 Locate Feature

```python
# Find feature in any status folder
feature_statuses = ["in-progress", "todo", "backlog"]
for status in feature_statuses:
    path = f"aidocs/sdd/{project}/features/{status}/{feature}"
    if exists(path):
        FEATURE_DIR = path
        FEATURE_STATUS = status
        break
```

### 1.2 Load Project Context

**Required files:**
```
aidocs/sdd/{project}/
├── constitution.md      # Project standards (MUST READ)
└── CLAUDE.md           # Project navigation (if exists)
```

**Extract from constitution:**
- Tech stack
- Code standards (linters, formatters)
- Testing requirements
- Build commands
- Git conventions

### 1.3 Load Feature Context

**Required files:**
```
{FEATURE_DIR}/
├── spec.md              # Functional requirements (FR-X)
├── design.md            # Architecture decisions (AD-X)
└── implementation-plan.md # Task breakdown
```

**Extract:**
- FR-X requirements with acceptance criteria
- AD-X architecture decisions
- Files to CREATE/MODIFY
- Dependencies between tasks

### 1.4 Build Context Package

Create context package for task executor:

```markdown
## Project Context

### Constitution Summary
- Tech: {stack}
- Standards: {linters, formatters}
- Testing: {framework, coverage threshold}
- Build: {commands}

### Feature: {feature}

#### Requirements (from spec.md)
- FR-1: {quoted requirement}
- FR-2: {quoted requirement}
...

#### Architecture (from design.md)
- AD-1: {quoted decision}
- AD-2: {quoted decision}
...

#### Files
- CREATE: {list}
- MODIFY: {list}
```

---

## Phase 2: Task Discovery

### 2.1 Find Tasks

```bash
# Priority order
1. {TASKS_DIR}/in-progress/TASK_*.md  # Resume first
2. {TASKS_DIR}/todo/TASK_*.md         # Then new tasks

# Sort by task number
TASK_001, TASK_002, TASK_003...
```

### 2.2 Build Execution Queue

```python
tasks = []

# In-progress first (resume)
for task in glob("{TASKS_DIR}/in-progress/TASK_*.md"):
    tasks.append(task)

# Then todo (sorted)
for task in sorted(glob("{TASKS_DIR}/todo/TASK_*.md")):
    tasks.append(task)

if not tasks:
    return "NO_TASKS: All tasks completed"
```

### 2.3 Pre-Execution Validation

Before starting, verify:
- [ ] All task files are valid markdown
- [ ] No circular dependencies
- [ ] Constitution is readable
- [ ] Spec and design exist

---

## Phase 3: Task Execution Loop

### 3.1 Execute Single Task

```python
for task in tasks:
    # Move to in-progress if in todo
    if task in todo:
        mv(task, "{TASKS_DIR}/in-progress/")

    # Execute via agent
    result = Task(
        subagent_type="faion-task-executor-agent",
        description=f"Execute {task.name}",
        prompt=f"""
PROJECT: {project}
FEATURE: {feature}
FEATURE_DIR: {FEATURE_DIR}
TASKS_DIR: {TASKS_DIR}

## Context Package
{context_package}

## Task to Execute
{task.name}

Execute this task following SDD workflow.
""",
        model="opus"
    )

    # Check result
    if result.status == "SUCCESS":
        post_task_validation(task)
    elif result.status == "BLOCKED":
        handle_blocked(task, result)
    elif result.status == "FAILED":
        handle_failed(task, result)
```

### 3.2 Post-Task Validation

After EACH task completion:

```python
def post_task_validation(task):
    """Run quality gates after task execution."""

    # 1. Run tests
    test_result = run_tests()
    if not test_result.passed:
        fix_tests(test_result.failures)
        # Retry up to 3 times

    # 2. Check coverage
    coverage = check_coverage()
    if coverage < threshold:
        log_warning(f"Coverage {coverage}% below threshold {threshold}%")

    # 3. Verify project runs
    build_result = run_build()
    if not build_result.success:
        fix_build(build_result.errors)
        # Retry up to 3 times

    # 4. Verify with hallucination checker
    Task(
        subagent_type="faion-hallucination-checker-agent",
        prompt=f"Verify task {task.name} completion with evidence"
    )
```

### 3.3 Test Execution

```bash
# Detect test framework from constitution/config
# Python
pytest -v --tb=short --cov={module} --cov-report=term-missing

# JavaScript
npm test -- --coverage --verbose

# Go
go test -v -cover ./...
```

**Validation criteria:**
- All tests pass
- No new test failures
- Coverage not decreased

### 3.4 Build Verification

```bash
# From constitution build commands
make build          # or
npm run build       # or
go build ./...      # etc.

# Then verify it runs
make run-dev        # or
npm run dev         # etc.
```

### 3.5 Handle Failures

```python
def handle_task_failure(task, error, attempt):
    if attempt >= 3:
        return TaskResult(
            status="FAILED",
            task=task,
            error=error,
            message="Max retries exceeded"
        )

    # Analyze error
    if is_test_failure(error):
        fix_tests()
    elif is_build_failure(error):
        fix_build()
    elif is_lint_failure(error):
        run_formatters()

    # Retry
    return execute_task(task, attempt + 1)
```

---

## Phase 4: Code Review Cycle

After ALL tasks completed, enter review cycle.

### 4.1 Run Code Review

```python
def code_review_cycle():
    """Iterate until no issues remain."""

    iteration = 0
    max_iterations = 5

    while iteration < max_iterations:
        iteration += 1

        # Run code review
        review = Task(
            subagent_type="faion-code-agent",
            description="Review feature code",
            prompt=f"""
task_type: review
project_path: {PROJECT_PATH}
context: Review all code changes for feature {feature}

Focus on:
1. Code correctness
2. Security issues
3. Performance problems
4. Style violations
5. Missing tests
6. Documentation gaps

Feature files:
{list_changed_files()}
"""
        )

        # Parse review results
        issues = parse_review_issues(review.output)

        if not issues:
            return ReviewResult(status="CLEAN", iterations=iteration)

        # Fix ALL issues
        for issue in issues:
            fix_issue(issue)

        # Run tests again
        if not run_tests().passed:
            fix_tests()

        # Continue to next iteration

    return ReviewResult(status="MAX_ITERATIONS", issues=issues)
```

### 4.2 Issue Categories

| Category | Auto-Fix | Action |
|----------|----------|--------|
| Style/Format | Yes | Run formatter |
| Missing docstring | Yes | Add docstring |
| Unused import | Yes | Remove import |
| Type hint missing | Yes | Add type hint |
| Security issue | No | Manual fix required |
| Logic error | No | Manual fix required |
| Missing test | Partial | Generate test |

### 4.3 Fix Implementation

```python
def fix_issue(issue):
    """Fix a single review issue."""

    if issue.category == "style":
        run_formatters()

    elif issue.category == "unused_import":
        remove_line(issue.file, issue.line)

    elif issue.category == "missing_test":
        Task(
            subagent_type="faion-test-agent",
            prompt=f"Generate tests for {issue.target}"
        )

    elif issue.category in ["security", "logic"]:
        # These require careful manual fixes
        Edit(
            file_path=issue.file,
            old_string=issue.current_code,
            new_string=issue.suggested_fix
        )
```

### 4.4 Review Acceptance Criteria

Review cycle ends when:
- [ ] No critical issues
- [ ] No security issues
- [ ] All tests pass
- [ ] Coverage meets threshold
- [ ] Build succeeds
- [ ] No style violations

---

## Phase 5: Finalize

### 5.1 Move Feature to Done

```bash
# Move entire feature directory
mv aidocs/sdd/{project}/features/in-progress/{feature} \
   aidocs/sdd/{project}/features/done/{feature}
```

### 5.2 Update Task Files

Ensure all tasks in `done/`:

```bash
# Move any remaining in-progress tasks
mv {TASKS_DIR}/in-progress/TASK_*.md {TASKS_DIR}/done/
```

### 5.3 Git Commit

```bash
git add -A
git commit -m "feat({feature}): complete feature implementation

Implements:
- FR-1: {summary}
- FR-2: {summary}
...

Following architecture decisions:
- AD-1: {summary}
...

Tasks completed: {N}
Test coverage: {X}%
Code review: PASSED"
```

---

## Output Format

### Success

```markdown
# Feature Execution: {project}/{feature}

## Status: SUCCESS

### Summary
| Metric | Value |
|--------|-------|
| Tasks Completed | N/N |
| Tests | X passed |
| Coverage | Y% |
| Review Iterations | Z |
| Total Duration | HH:MM |

### Task Results

| Task | Status | Tests | Coverage | Commit |
|------|--------|-------|----------|--------|
| TASK_001 | ✅ | 12/12 | 85% | abc123 |
| TASK_002 | ✅ | 8/8 | 82% | def456 |
| TASK_003 | ✅ | 15/15 | 88% | ghi789 |

### Code Review
- Iterations: 2
- Issues Fixed: 7
- Final Status: CLEAN

### Files Changed
- `app/models/refund.py` (CREATE, 120 lines)
- `app/services/refund.py` (CREATE, 200 lines)
- `app/views/refund.py` (CREATE, 80 lines)
- `tests/test_refund.py` (CREATE, 150 lines)

### Next Steps
- Feature moved to `done/`
- Ready for deployment
```

### Partial Success

```markdown
# Feature Execution: {project}/{feature}

## Status: PARTIAL

### Summary
| Metric | Value |
|--------|-------|
| Tasks Completed | M/N |
| Tasks Failed | K |
| Blockers | L |

### Failed Tasks

| Task | Status | Reason | Attempts |
|------|--------|--------|----------|
| TASK_003 | FAILED | Tests failing | 3 |
| TASK_004 | BLOCKED | Depends on TASK_003 | - |

### Required Actions
1. Fix TASK_003 test failures manually
2. Re-run feature executor
```

### Failed

```markdown
# Feature Execution: {project}/{feature}

## Status: FAILED

### Reason
{Critical error description}

### Context
- Last successful task: TASK_002
- Failed at: TASK_003
- Error: {error details}

### Recovery Steps
1. {Step 1}
2. {Step 2}
```

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Feature not found | Search all status folders, ask user |
| No tasks | Report "All tasks completed" |
| Test framework unknown | Ask user for test command |
| Build fails repeatedly | Stop, report, require manual fix |
| Review cycle stuck | Stop after 5 iterations, report remaining issues |
| Circular dependency | Report, ask user to resolve |

---

## Configuration

### From Constitution

The skill reads these settings from `constitution.md`:

```yaml
testing:
  framework: pytest          # or jest, vitest, go test
  command: make test-dev     # test execution command
  coverage_threshold: 80     # minimum coverage %

build:
  command: make build        # build command
  run_command: make run-dev  # run/verify command

formatting:
  command: make fix          # auto-format command
```

### Defaults

If not specified in constitution:

| Setting | Default |
|---------|---------|
| Test command | `pytest` / `npm test` |
| Coverage threshold | 80% |
| Build command | `npm run build` / `make build` |
| Max review iterations | 5 |
| Max task retries | 3 |

---

## Constraints

**Must:**
- Load full context before execution
- Run tests after EVERY task
- Fix ALL review issues before completing
- Document all changes
- Verify project runs

**Must NOT:**
- Skip failing tests
- Ignore code review issues
- Push to remote without review
- Modify spec or design (only implementation)
- Delete or skip tasks

---

## Integration

### With SDD Workflow

```
SPEC → DESIGN → IMPL-PLAN → TASKS → [FEATURE-EXECUTOR] → DONE
                                           ↑
                                    This skill
```

### With Other Skills

| Skill | Integration |
|-------|-------------|
| faion-sdd-domain-skill | Provides SDD context |
| faion-dev-django-skill | Django-specific patterns |
| faion-testing-skill | Test generation patterns |

---

## Examples

### Example 1: Execute Auth Feature

```
User: /faion-feature-executor cashflow-planner 01-auth
Skill: Loading context...
- Constitution: cashflow-planner (Django 5.x, pytest, 80% coverage)
- Feature: 01-auth (4 tasks in todo/)
- Spec: 5 FR, Design: 3 AD

Executing tasks:

TASK_001_user_model ━━━━━━━━━━ EXECUTING
├─ Creating User model...
├─ Running tests... 12/12 ✅
├─ Coverage: 85%
└─ Status: SUCCESS

TASK_002_auth_service ━━━━━━━━━━ EXECUTING
├─ Creating AuthService...
├─ Running tests... 8/8 ✅
├─ Coverage: 82%
└─ Status: SUCCESS

...

Code Review Cycle:
├─ Iteration 1: 5 issues found
│   ├─ Fixed: 3 style issues
│   ├─ Fixed: 2 missing docstrings
├─ Iteration 2: 0 issues ✅
└─ Status: CLEAN

Feature completed:
- Tasks: 4/4
- Coverage: 88%
- Review: PASSED
- Moved to: features/done/01-auth
```

### Example 2: Resume Partial Execution

```
User: /faion-feature-executor faion-net 02-landing-page

Skill: Found 1 task in in-progress/, 3 in todo/
Resuming from TASK_002...

TASK_002_hero_section ━━━━━━━━━━ RESUMING
├─ Previous progress: 60%
├─ Completing implementation...
├─ Running tests... 15/15 ✅
└─ Status: SUCCESS

Continuing with remaining tasks...
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-18 | Initial release |

---

*faion-feature-executor v1.0.0*
*Execute features with quality gates*
