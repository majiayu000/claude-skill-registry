---
name: backend-ralph-plan
description: >
  Create a structured plan directory with Ralph Wiggum Loop integration for
  backend Django projects. Generates PLAN.md (task index), task files, and
  RALPH-PROMPT.md (the actual prompt for ralph-loop). Use for rigorous,
  iterative implementation requiring quality gates and verification.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
---

# Backend RALPH Plan Skill

## Purpose

This skill creates **two deliverables**:

1. **PLAN.md** - Structured task index with quality tracking
2. **RALPH-PROMPT.md** - The prompt fed to `/ralph-wiggum:ralph-loop`

The key insight: Ralph works by feeding the **same prompt** repeatedly. Claude
sees its previous work in files/git and iterates. RALPH-PROMPT.md becomes that
prompt, instructing Claude to work through tasks with strict quality gates.

## When to Use

- Backend Django features requiring rigorous quality control
- Multi-task implementations needing iterative, autonomous execution
- When you want continuous regression testing between tasks
- Projects where you'll walk away and let Ralph complete the work

## When NOT to Use

- Quick prototypes or exploratory code
- Frontend projects (create `frontend-ralph-plan` if needed)
- Simple tasks that don't need iteration
- Plans where human judgment is needed at each step

## The Two-Step Process

**Step 1: This skill creates the plan**
```
docs/plans/<slug>/
├── PLAN.md              # Task index with tracking
├── RALPH-PROMPT.md      # Prompt for ralph-loop
├── 001-<task>.md        # Task files
└── ...
```

**Step 2: Run the plan**
```
/plan-directory:run <slug>
```

That's it. This command:
1. Reads RALPH-PROMPT.md
2. Extracts the completion promise
3. Invokes `/ralph-wiggum:ralph-loop` automatically

Optional: `/plan-directory:run <slug> --max-iterations 50`

## Required Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Plan title | Yes | Human-readable name |
| Plan slug | Yes | Directory name, kebab-case |
| Task list | Yes | Tasks with names and scopes |
| Django app path | Yes | e.g., `optimo_surveys/` |
| Module path | Yes | e.g., `digest/` |
| Test filter | Yes | Pytest `-k` filter |

### Tooling Configuration

| Input | Default | Description |
|-------|---------|-------------|
| Lint command | `ruff check` | Prefix with `.bin/` if needed |
| Format command | `ruff format` | |
| Type check | `ty` | Or `mypy`, `pyright` |
| Test command | `pytest` | |
| Test config | `` | e.g., `--dc=TestLocalApp` |
| Django command | `django` | |
| Coverage target | `90` | Minimum percentage |
| Max iterations | `100` | Ralph loop limit |

## Task Granularity Guidelines

**Right-sized tasks for Ralph:**

| Task Size | Checklist Items | Good For |
|-----------|-----------------|----------|
| Too small | 1-2 | Overhead exceeds value |
| **Ideal** | **4-8** | **Clear scope, achievable in one iteration** |
| Too large | 10+ | Gets stuck, split it |

**Signs a task is too large:**
- Requires multiple commits to feel "done"
- Has more than 8 checklist items
- Spans multiple unrelated concerns
- Would take a human more than 2-4 hours

**Split large tasks by:**
- Separating model/service/API layers
- Breaking by feature subset
- Isolating integration points

## Completion Promise Format

The promise must be **plan-specific**, not generic:

```
ALL {{TASK_COUNT}} {{PLAN_SLUG_UPPER}} TASKS COMPLETE
```

Examples:
- `ALL 4 USER-PREFERENCES TASKS COMPLETE`
- `ALL 11 MANAGER-DIGEST TASKS COMPLETE`
- `ALL 6 NOTIFICATION-SERVICE TASKS COMPLETE`

This prevents Claude from lying with a generic "done" when tasks remain.

## RALPH-PROMPT.md: The Key File

The prompt is **iteration-aware**. It tells Claude to:

1. **Orient first** - Check git log, read PLAN.md for current status
2. **Don't repeat work** - Skip what's already committed
3. **Verify rigorously** - Run all gates after each task
4. **Commit progress** - Git commit after each task completion
5. **Handle blockers** - Document, try alternatives, don't lie to exit

See `references/ralph-prompt-template.md` for the full template.
See `examples/user-preferences/` for a complete working example.

## Git Integration

Each task completion includes a commit:

```bash
git commit -m "Complete 001 - Preferences Model

- Added JSONField to User model
- Created Pydantic schemas for validation
- 5 tests added, 94% coverage

Plan: user-preferences"
```

This is critical for Ralph because:
- Progress persists across iterations
- Claude can see what it did via `git log`
- Partial progress is never lost

## Handling Complex Codebases

For large/unfamiliar codebases, add a **warm-up task**:

```markdown
# 000 - Codebase Orientation

## Goal
Understand existing patterns before implementing.

## Checklist
- [ ] Read existing models in `{{APP_PATH}}`
- [ ] Identify service layer patterns
- [ ] Note testing conventions
- [ ] Document relevant existing code in Notes section

## Completion Criteria
- [ ] Notes section filled with findings
- [ ] No implementation (orientation only)
```

This prevents Claude from fighting existing patterns.

## Escape Hatches

If Claude is genuinely stuck:

1. **Blockers section** in task file:
   ```markdown
   ## Blockers
   - **Blocked by:** External API not available
   - **Attempted:** Mock implementation, local stub
   - **Needs:** API credentials or decision to defer
   ```

2. **Skip to independent task** if dependencies allow

3. **Max iterations** as ultimate safety net

The loop continues until genuine completion or max iterations.
Claude should never lie to exit.

## Workflow

### 1. Gather Inputs

Ask for all required inputs. Clarify:
- Exact paths (trailing slashes matter)
- Test filter that isolates this feature
- Non-standard tooling (`.bin/` wrappers)

### 2. Analyze Dependencies

Before creating files:
1. Identify foundation tasks (no dependencies)
2. Map task dependencies
3. Determine critical path
4. Order to minimize blocking

### 3. Create Files

1. Create `docs/plans/<slug>/` directory
2. Write `PLAN.md` with task index and tracking tables
3. Write each task file with standard sections
4. Write `RALPH-PROMPT.md` with all placeholders replaced

### 4. Replace Placeholders

In RALPH-PROMPT.md, replace:
- `{{PLAN_TITLE}}` → e.g., "User Preferences API"
- `{{TASK_COUNT}}` → e.g., "4"
- `{{PLAN_SLUG}}` → e.g., "user-preferences"
- `{{PLAN_SLUG_UPPER}}` → e.g., "USER-PREFERENCES"
- `{{LINT_CMD}}` → e.g., ".bin/ruff check"
- `{{APP_PATH}}` → e.g., "accounts/"
- `{{MODULE_PATH}}` → e.g., "preferences/"
- All other command/path placeholders

### 5. Verify Deliverables

Before delivering:
- [ ] PLAN.md has task index and tracking tables
- [ ] All task files have Goal, Scope, Checklist, Tests, Completion Criteria
- [ ] Task checklist items are 4-8 each (not too small, not too large)
- [ ] RALPH-PROMPT.md has NO remaining `{{placeholders}}`
- [ ] Execution order matches actual dependencies
- [ ] Completion promise includes task count and slug

## Example

See `examples/user-preferences/` for a complete working example:
- `PLAN.md` - 4-task plan with tracking
- `RALPH-PROMPT.md` - Iteration-aware prompt
- `001-preferences-model.md` - Foundation task (model layer)
- `002-preferences-service.md` - Service layer
- `003-api-endpoints.md` - API layer
- `004-caching-layer.md` - Performance optimization

## Reference Files

- `references/ralph-prompt-template.md` - Full prompt template
- `references/plan-template.md` - PLAN.md structure
- `references/quality-gates.md` - Verification commands
- `examples/user-preferences/` - Working example
