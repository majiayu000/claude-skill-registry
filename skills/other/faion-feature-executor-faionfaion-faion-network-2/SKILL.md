---
name: faion-feature-executor
description: "SDD feature executor: sequential task execution with quality gates, test validation."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, TodoWrite, AskUserQuestion
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Feature Executor Skill

**Communication: User's language. Docs/code: English.**

## Navigation

| File | Description |
|------|-------------|
| [SKILL.md](SKILL.md) | This file - overview and usage |
| [CLAUDE.md](CLAUDE.md) | Navigation hub |
| [execution-workflow.md](execution-workflow.md) | Complete workflow with all phases |
| [quality-gates.md](quality-gates.md) | Validation and acceptance criteria |

---

## Purpose

Execute all tasks in an SDD feature with full quality gates:
1. Load project and feature context
2. **Ask user permission** before starting YOLO execution
3. Execute tasks sequentially via `faion-task-YOLO-executor-opus-agent`
4. After each task: verify tests pass, coverage adequate, project runs
5. After all tasks: code review cycle until no issues remain
6. Move feature to `done/`

---

## Context Discovery

### Auto-Investigation

| Signal | Check For | Why |
|--------|-----------|-----|
| `.aidocs/todo/` or `in-progress/` | Feature folders with tasks | Features ready for execution |
| `constitution.md` | Tech stack, testing requirements | Project standards |
| Test suite config | Testing framework, coverage tools | Quality gate setup |
| CI/CD pipelines | Automated test runs | Integration readiness |
| Feature tasks count | Number of TASK-*.md files | Execution scope estimation |

### Discovery Questions

```yaml
questions:
  - question: "What execution mode do you prefer?"
    options:
      - label: "YOLO (autonomous)"
        description: "Full automation, no confirmations (requires permission)"
      - label: "Interactive"
        description: "Task-by-task confirmation"
      - label: "Review-only"
        description: "Review existing implementation"

  - question: "How many tasks are in this feature?"
    options:
      - label: "1-3 tasks"
        description: "Fast sequential execution"
      - label: "4-10 tasks"
        description: "Standard execution with checkpoints"
      - label: "10+ tasks"
        description: "Consider splitting feature or batching"

  - question: "What quality gates do you need?"
    options:
      - label: "All gates (L1-L6)"
        description: "Production-ready code"
      - label: "Essential (L1-L5)"
        description: "Development quality"
      - label: "Minimal (L1-L3)"
        description: "Prototype/POC quality"
```

## Decision Tree

| If you need... | Use | Why |
|----------------|-----|-----|
| Create tasks before execution | [faion-sdd](../faion-sdd/) | No tasks in todo/ yet |
| Execute single task | [faion-software-developer](../faion-software-developer/) | Direct execution faster |
| Execute multiple dependent tasks | This skill | Sequential execution with quality gates |
| Execute independent tasks | [faion-sdd](../faion-sdd/) | Parallelize via SDD |
| CI/CD integration | [faion-devops-engineer](../faion-devops-engineer/) | Infrastructure tasks |
| Return to orchestrator | [faion-net](../faion-net/) | Multi-domain coordination |

### Quality Modes

| Quality Level | Gates Applied | Use Case |
|---------------|---------------|----------|
| **High** | L1-L6 (all) | Production code |
| **Medium** | L1-L5 | Feature development |
| **Low** | L1-L3 | Prototypes/POC |

**Quality Gates:** L1=Lint, L2=Types, L3=Unit tests, L4=Integration, L5=Code review, L6=Acceptance

### Error Responses

| Error Type | Action |
|------------|--------|
| Test failure | Fix tests, retry task, continue others |
| Build failure | Stop execution, fix build first |
| Git conflict | Stop execution, resolve manually |
| Security issue | Stop execution, escalate to user |

## CRITICAL: User Permission Required

**Before launching `faion-task-YOLO-executor-opus-agent`, ALWAYS ask user:**

```
⚠️ YOLO Mode Activation

About to execute {N} tasks autonomously:
- Task 1: {name}
- Task 2: {name}
...

YOLO mode means:
- No confirmations during execution
- All file edits auto-approved
- Full autonomy until completion

Proceed with YOLO execution? [Yes/No]
```

**Use AskUserQuestion tool to get explicit permission.**

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
- `project`: Project name (containing `.aidocs/` folder)
- `feature`: Feature name (folder in `.aidocs/{status}/`)

---

## Workflow Phases

See [execution-workflow.md](execution-workflow.md) for complete details.

1. **Context Loading** - Load constitution, spec, design, implementation plan
2. **Task Discovery** - Find tasks in `in-progress/` and `todo/`
3. **Task Execution Loop** - Execute each task with validation (tests, coverage, build)
4. **Code Review Cycle** - Iterate until no issues remain
5. **Finalize** - Move to `done/`, generate summary

## Quality Gates

See [quality-gates.md](quality-gates.md) for validation criteria.

After each task:
- All tests pass
- Coverage meets threshold
- Project builds and runs

After all tasks:
- Code review passes
- No critical/security issues
- No style violations

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
| faion-sdd | Provides SDD context |
| faion-dev-django-skill | Django-specific patterns |
| faion-testing-skill | Test generation patterns |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-18 | Initial release |
| 1.1.0 | 2026-01-23 | Modularized documentation |

---

*faion-feature-executor v1.1.0*
*Execute features with quality gates*
