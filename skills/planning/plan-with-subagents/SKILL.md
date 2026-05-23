---
name: plan-with-subagents
description: Plan multi-step implementation tasks to minimize context usage and maximize parallelism. Automatically applies whenever plan mode is active.
user-invocable: true
---

# Plan with Sub-Agents Skill

**These guidelines apply automatically whenever plan mode is active.** Plan mode implies complexity, so always design for parallelism and minimal context.

## Core Principle: Use Sub-Agents Generously

Sub-agents are cheap and effective. When in doubt, spawn an agent. Benefits:
- **Parallel execution** - Multiple agents work simultaneously
- **Reduced context** - Each agent only sees what it needs
- **Fault isolation** - One agent's failure doesn't block others
- **Cleaner commits** - Each agent commits its own work

**Default to spawning agents** for:
- Any exploration or research (use `Explore` agent)
- Designing approaches (use `Plan` agent)
- Independent file modifications (use `general-purpose` agents in parallel)
- Error-prone steps that involve noisy logs (e.g. running tests)
- Shell operations (use `Bash` agent)

## When Sub-Agents Apply

- Any task in plan mode (plan mode = complexity assumed)
- Tasks with 4+ distinct steps
- Work that touches multiple unrelated files
- Tasks where exploration and execution can be separated
- Long-running operations that benefit from parallel execution

## Phase Design Principles

### 1. Break by File Independence

Group work by which files are touched. Phases that modify **different files** can run in parallel.

```
Phase A: modifies src/api/server.py, src/api/models.py
Phase B: modifies tests/test_api.py, tests/conftest.py
Phase C: modifies README.md, docs/API.md
→ All three can run in parallel
```

### 2. Identify Sequential Dependencies

Some phases MUST run in order:
- Phase that creates a file → Phase that references it
- Phase that changes API → Phase that updates tests for that API
- Phase that installs deps → Phase that uses those deps

### 3. Minimize Context per Agent

Each sub-agent should receive ONLY the context it needs:
- Specific file paths to modify
- Exact changes to make
- Commit message to use

Avoid passing full project history or unrelated requirements.

## Agent Type Selection

| Task Type | Agent | Why |
|-----------|-------|-----|
| Run shell commands (git, gh, npm) | `Bash` | Direct command execution |
| Find files/patterns in codebase | `Explore` | Optimized for search |
| Design implementation approach | `Plan` | Architectural thinking |
| Write/modify code | `general-purpose` | Full tool access |
| Research questions | `general-purpose` | Web + file access |

## Execution Prompt Template

When spawning sub-agents, use this structure:

```
**Task:** [One sentence describing the goal]

**Files to modify:**
- path/to/file1.py - [what to change]
- path/to/file2.py - [what to change]

**Specific changes:**
1. [Concrete change 1]
2. [Concrete change 2]

**Commit when done:**
"[type]: [description]"
```

## Example Plan Structure

```markdown
## Phase 0: Setup (sequential)
- Create directory structure
→ COMMIT: "chore: Add project scaffolding"

## Phase 1: Research (sequential)
- Explore codebase to understand patterns
- No commit (exploration only)

## Phases 2, 3, 4 (PARALLEL)
Agent A - Phase 2: Backend changes
- Modify src/api/*.py
→ COMMIT: "feat: Add new endpoint"

Agent B - Phase 3: Frontend changes
- Modify src/ui/*.tsx
→ COMMIT: "feat: Add UI component"

Agent C - Phase 4: Documentation
- Modify docs/*.md
→ COMMIT: "docs: Document new feature"

## Phase 5: Integration (sequential, after 2-4)
- Update tests that depend on all changes
→ COMMIT: "test: Add integration tests"

## Phase 6: Validation
- Run tests, linting, type checks
→ COMMIT only if fixes needed
```

## Parallelization Checklist

Before marking phases as parallel, verify:

- [ ] No shared files between parallel phases
- [ ] No phase reads output from another parallel phase
- [ ] Each phase can commit independently
- [ ] Merge conflicts are impossible

## Anti-Patterns

**Don't:** Create one giant phase with all changes
**Do:** Split by logical units that can be tested independently

**Don't:** Pass entire CLAUDE.md to every sub-agent
**Do:** Extract only relevant sections for each task

**Don't:** Have parallel phases commit to the same file
**Do:** Sequence phases that touch shared files

## Commit Strategy

Each phase should commit its own work immediately when done. This provides:
- Clear git history
- Easy rollback if one phase fails
- Parallel agents don't block each other

Use conventional commit prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `chore:` - Maintenance
- `docs:` - Documentation
- `test:` - Tests
- `refactor:` - Code restructuring
