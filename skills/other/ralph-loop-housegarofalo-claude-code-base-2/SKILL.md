---
name: ralph-loop
version: 1.0.0
description: Iterative development loop methodology for autonomous AI work. Configure self-correcting coding loops that iterate until completion criteria are met, integrate with Archon for task tracking, and support multiple execution modes. Use when running autonomous coding sessions, implementing self-correcting workflows, or building iterative development pipelines.
---

# Ralph Loop: Iterative Development Methodology

Configure and run self-correcting iterative development loops for autonomous AI coding. Ralph loops iterate until completion criteria are met, with proper state management and handoff support.

## Triggers

Use this skill when:
- Running autonomous coding sessions
- Implementing self-correcting workflows
- Building iterative development pipelines
- Creating loops that validate and fix their own work
- Setting up background coding tasks
- Keywords: ralph, iterative, loop, autonomous, self-correcting, iteration, background, continuous

## Concept Overview

```
RALPH LOOP CYCLE

  ┌─────────────────────────────────────────────┐
  │                                             │
  │    ┌──────────┐                             │
  │    │  Start   │                             │
  │    │ Iteration│                             │
  │    └────┬─────┘                             │
  │         │                                   │
  │         v                                   │
  │    ┌──────────┐     ┌──────────┐           │
  │    │   Work   │────>│ Validate │           │
  │    │          │     │          │           │
  │    └──────────┘     └────┬─────┘           │
  │                          │                  │
  │              ┌───────────┴───────────┐     │
  │              │                       │     │
  │              v                       v     │
  │         [FAIL]                  [PASS]     │
  │              │                       │     │
  │              │                       v     │
  │              │              ┌──────────┐   │
  │              │              │ Complete?│   │
  │              │              └────┬─────┘   │
  │              │                   │         │
  │              │         ┌────────┴────────┐│
  │              │         │                 ││
  │              v         v                 v│
  │         [Fix Issue]  [NO]            [YES]│
  │              │         │                 ││
  │              └─────────┘             EXIT │
  │                    │                      │
  └────────────────────┘                      │
                                              │
                                    <promise>COMPLETE</promise>
```

---

## Setup Wizard

### Phase 1: Project Selection

```python
# Query Archon for projects
projects = find_projects(masters_only=True, include_hierarchy=True)
```

Present options:
```markdown
## Select Project

| # | Project | Description | Tasks |
|---|---------|-------------|-------|
| 1 | [Project Name] | [Description] | [X] todo |
| 2 | [Project Name] | [Description] | [X] todo |

Enter project number (or 'new' to create):
```

### Phase 2: Task Selection

```python
# Get tasks for selected project
tasks = find_tasks(
    filter_by="project",
    filter_value=PROJECT_ID,
    include_closed=False
)
```

Present options:
```markdown
## Select Task

### TODO Tasks (Recommended)
| # | Task | Feature | Priority |
|---|------|---------|----------|
| 1 | [Task Title] | [Feature] | [Order] |
| 2 | [Task Title] | [Feature] | [Order] |

### In Progress (Continue existing)
| # | Task | Feature | Assignee |
|---|------|---------|----------|
| 3 | [Task Title] | [Feature] | [Assignee] |

Enter task number (or 'new' to create, 'custom' for custom prompt):
```

### Phase 3: Prompt Configuration

**Auto-Generated Prompt Template:**

```markdown
# Ralph Loop: [TASK_TITLE]

## Objective
[From task description]

## Requirements
[Extracted from task]

## Acceptance Criteria
[From task if available]

## Self-Correction Loop

For each iteration:
1. Review previous work in files and git history
2. Run validation: `[TEST_COMMAND]`
3. If validation fails:
   - Analyze failure output
   - Fix the issue
   - Re-run validation
4. If validation passes:
   - Check against acceptance criteria
   - Continue to next requirement
5. When all requirements met:
   - Run full validation suite
   - Update Archon task to "done"
   - Output: <promise>COMPLETE</promise>

## Validation Commands
```bash
[BUILD_COMMAND]
[TEST_COMMAND]
```

## Archon Context
- Project: [PROJECT_ID]
- Task: [TASK_ID]

## Escape Hatch

After 15 iterations without progress:
1. Update Archon task with blocker details
2. Document what was attempted
3. Output: <promise>BLOCKED</promise>
```

### Phase 4: Options Configuration

```markdown
## Loop Options

### Iteration Limits
| Setting | Default | Your Choice |
|---------|---------|-------------|
| Max iterations | 50 | ___ |
| Timeout per iteration (min) | 0 (unlimited) | ___ |
| Pause between iterations (sec) | 0 | ___ |

### Completion Settings
| Setting | Default | Your Choice |
|---------|---------|-------------|
| Completion promise | "COMPLETE" | ___ |
| Complete on Archon task done | Yes | Yes / No |
| Complete on tests pass | No | Yes / No |

### Execution Mode
- [ ] **Background** - Fully autonomous (recommended for tested prompts)
- [ ] **Manual** - You trigger each iteration
- [ ] **Hybrid** - Start manual, then background (recommended)

### Validation Commands
| Type | Command | Auto-Detected |
|------|---------|---------------|
| Build | [detected] | Yes/No |
| Test | [detected] | Yes/No |
| Lint | [detected] | Yes/No |
```

### Auto-Detection Logic

```bash
# Detect project type and commands
if [ -f "package.json" ]; then
    BUILD_CMD="npm run build"
    TEST_CMD="npm test"
    LINT_CMD="npm run lint"
elif [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
    BUILD_CMD="python -m build"
    TEST_CMD="pytest"
    LINT_CMD="ruff check ."
elif [ -f "*.csproj" ] || [ -f "*.sln" ]; then
    BUILD_CMD="dotnet build"
    TEST_CMD="dotnet test"
    LINT_CMD="dotnet format --verify-no-changes"
elif [ -f "go.mod" ]; then
    BUILD_CMD="go build ./..."
    TEST_CMD="go test ./..."
    LINT_CMD="golangci-lint run"
fi
```

---

## Configuration Files

### Directory Structure

```
.ralph/
├── config.json        # Loop configuration
├── prompts/
│   └── current.md     # Active iteration prompt
└── checkpoints/
    └── iteration-N.json  # State snapshots
```

### config.json

```json
{
  "loop_id": "ralph-2025-01-23-001",
  "archon_project_id": "<PROJECT_ID>",
  "archon_task_id": "<TASK_ID>",
  "prompt_file": ".ralph/prompts/current.md",
  "max_iterations": 50,
  "completion_promise": "COMPLETE",
  "mode": "hybrid",
  "validation": {
    "build": "npm run build",
    "test": "npm test",
    "lint": "npm run lint"
  },
  "integration": {
    "harness": false,
    "speckit": false,
    "prp": false
  }
}
```

---

## Execution Commands

| Command | Description |
|---------|-------------|
| `/ralph-setup` | Launch setup wizard |
| `/ralph-start` | Create and start new loop |
| `/ralph-iterate` | Run single iteration (manual mode) |
| `/ralph-continue` | Resume background execution |
| `/ralph-status` | Check loop status |
| `/ralph-cancel` | Stop active loop |

### Quick Start Examples

```bash
# Full wizard
/ralph-setup

# Quick with defaults
/ralph-start --quick --project <id> --task <id>

# Auto mode (highest priority TODO task)
/ralph-start --auto

# Custom prompt without task
/ralph-start --custom "Implement feature X with tests"
```

---

## Archon Integration

### Create State Document

```python
manage_document("create",
    project_id=PROJECT_ID,
    title=f"Ralph Loop State: {loop_id}",
    document_type="note",
    content={
        "loop_id": loop_id,
        "status": "running",
        "current_iteration": 0,
        "max_iterations": 50,
        "task_id": TASK_ID,
        "iterations": []
    }
)
```

### Update Task on Start

```python
manage_task("update",
    task_id=TASK_ID,
    status="doing",
    assignee="Ralph Agent",
    description=f"""[ORIGINAL_DESCRIPTION]

---
## Ralph Loop Attached
- Loop ID: {loop_id}
- Max Iterations: {max_iterations}
- Mode: {mode}
- Started: {timestamp}

Progress updates will appear here.
"""
)
```

### Update on Completion

```python
manage_task("update",
    task_id=TASK_ID,
    status="done",
    description=f"""[ORIGINAL_DESCRIPTION]

---
## Ralph Loop Complete
- Loop ID: {loop_id}
- Total Iterations: {iterations}
- Completed: {timestamp}

All acceptance criteria met.
"""
)
```

---

## Iteration Protocol

### Each Iteration Must:

1. **Check Previous State**
   - Read progress file
   - Check git history
   - Review Archon task

2. **Execute Work**
   - Make changes
   - Write code
   - Update files

3. **Validate**
   - Run build command
   - Run test command
   - Check lint (optional)

4. **Handle Result**
   - If PASS: Check completion criteria
   - If FAIL: Analyze error, fix, re-validate

5. **Update State**
   - Update progress file
   - Update Archon task
   - Git commit (if changes)

### Completion Criteria

Loop ends when ANY of these are true:
- `<promise>COMPLETE</promise>` output
- All tests pass (if configured)
- Archon task status is "done"
- Max iterations reached
- `<promise>BLOCKED</promise>` output

---

## Framework Integration

Ralph can integrate with other frameworks:

| Framework | Integration Mode |
|-----------|-----------------|
| **Autonomous Harness** | Ralph replaces coding loop |
| **SpecKit** | Ralph implements tasks from plan |
| **PRP Framework** | Ralph executes fix iterations |

### Detection

```bash
has_harness = exists(".harness/config.json")
has_speckit = exists(".specify/") or exists("specs/")
has_prp = exists("PRPs/")
```

---

## Error Handling

### No Archon Connection

```markdown
Warning: Archon MCP Not Connected

Ralph requires Archon for state management. Please:
1. Verify Archon MCP server is configured
2. Check Archon server is running
3. Retry: /ralph-start

For standalone mode (not recommended):
/ralph-start --no-archon
```

### Stuck Loop (No Progress)

After 15 iterations without meaningful progress:

```python
manage_task("update",
    task_id=TASK_ID,
    status="review",
    description=f"""[ORIGINAL_DESCRIPTION]

---
## Ralph Loop BLOCKED
- Loop ID: {loop_id}
- Iterations Attempted: {iterations}
- Blocked At: {timestamp}

### What Was Attempted
{attempt_summary}

### Blocker Details
{blocker_description}

### Recommended Actions
{recommendations}

Requires human intervention.
"""
)
```

Output: `<promise>BLOCKED</promise>`

---

## Best Practices

1. **Clear Acceptance Criteria**: Define what "done" looks like
2. **Testable Validation**: Use automated tests, not manual checks
3. **Small Tasks**: Break large work into Ralph-sized chunks
4. **State Preservation**: Always update Archon between iterations
5. **Escape Hatches**: Have clear blocker conditions
6. **Git Commits**: Commit after each successful iteration
7. **Monitor Mode First**: Use manual/hybrid before full background

---

## Notes

- Ralph works best with well-defined, testable tasks
- Background mode requires high confidence in prompt quality
- Archon integration provides persistence across sessions
- Use escape hatches to prevent infinite loops
- Monitor resource usage in long-running loops
