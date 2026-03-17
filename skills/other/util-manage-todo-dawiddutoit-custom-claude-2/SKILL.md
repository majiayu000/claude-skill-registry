---
name: util-manage-todo
description: Manage project todos in todo.md files with task states (pending, in_progress, completed). PROACTIVELY invoke when Claude detects need to create or update a todo during a session. Use when breaking down work into tasks, tracking progress across sessions, organizing complex multi-step projects, or coordinating task states. Supports refactor/migration tracking with ADR integration.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Bash
---

# Manage Todo

## Purpose

Manage `./todo.md` in project root with task state tracking, TodoWrite synchronization, and ADR-governed refactor support. Primary use: Claude proactively creates/updates todos when detecting multi-step work.

## CRITICAL: Todo File Location

**Use `./todo.md` for 95% of work** (this skill)

| Use This Skill | Session Todo (rare) |
|---------------|---------------------|
| Bug fixes, features, refactors | Temporary spikes only |
| Multi-step work, team coordination | Throwaway research |
| Work committed to git | Quick experiments (<1hr) |
| **If unsure → use this skill** | |

Session todos: `.claude/artifacts/YYYY-MM-DD/todos/todo-{name}.md`

## When to Use

### Agent-Initiated (PRIMARY)

**PROACTIVELY invoke when Claude detects:**
- "I need to create a todo to track this work"
- "User has given me multiple tasks to coordinate"
- "This is complex enough to warrant tracking"

### User-Initiated

When user requests:
- "Create a todo for [feature]"
- "Update task [N] to [state]"
- "Track these tasks"

### NOT to Use

- Single, straightforward tasks
- Trivial operations (<3 steps)
- Purely informational requests

## Quick Start

### Creating a Todo

1. Read project context
2. Create `./todo.md` with structured tasks
3. Assign states (🔴 pending by default)
4. Add acceptance criteria
5. Sync with TodoWrite

### Updating State

1. Read `./todo.md`
2. Update task state: 🔴 → 🟡 → 🟢
3. Update TodoWrite to match
4. Update progress summary

### Checking Progress

1. Read `./todo.md`
2. Calculate completion %
3. Identify blockers
4. Suggest next actions

## Basic Todo Structure

```markdown
# Todo: [Feature Name]
Date: YYYY-MM-DD

## Objective
[Clear statement of goal]

## Tasks

### Task 1: [Title]
**Status:** 🔴 Not Started | 🟡 In Progress | 🟢 Complete
**Priority:** High | Medium | Low

**Description:**
What needs to be done.

**Acceptance Criteria:**
- [ ] Functionality implemented
- [ ] Tests pass
- [ ] Code follows conventions

## Progress Summary
- Total: X | Completed: Y (Z%)
```

## Task States

| State | Meaning |
|-------|---------|
| 🔴 Pending | Not started |
| 🟡 In Progress | Actively working |
| 🟢 Complete | Acceptance criteria met |
| ⚫ Blocked | Waiting on dependency |

## Integration Requirements (CRITICAL)

**Prevents "done but not integrated" failures.**

### The CCV Principle

| Phase | What It Proves |
|-------|----------------|
| **CREATION** | Artifact exists |
| **CONNECTION** | Wired into system |
| **VERIFICATION** | Works at runtime |

**Missing any phase = NOT complete**

### Four Questions Test

Before "done", answer ALL:
1. **How do I trigger this?**
2. **What connects it to the system?**
3. **What proves it runs?**
4. **What shows it works?**

### Three-Phase Todo Pattern

For integration work:

```markdown
### Phase 1: CREATION
- [ ] Create [module]
- [ ] Unit tests pass

### Phase 2: CONNECTION
- [ ] Import in [consumer]
- [ ] Register in [system]
- [ ] Verify: `grep "module" src/`

### Phase 3: VERIFICATION
- [ ] Integration test passes
- [ ] Execution logs attached
- [ ] Expected outcome observed
```

**See:** [references/integration-requirements.md](references/integration-requirements.md)

## Key Integrations

### TodoWrite Synchronization

**Rule:** `todo.md` is source of truth

```
Update todo.md → Update TodoWrite → Verify sync
```

### Refactor/Migration Tracking

**Rule:** Refactors REQUIRE an ADR

1. Detect refactor keywords
2. Invoke `validate-refactor-adr` skill
3. If no ADR: STOP, instruct user to create
4. If ADR exists: Use enhanced template

## Task Sizing

**Good size:**
- 1-4 hours of focused work
- Clear deliverable
- Single responsibility
- Testable outcome

**Too large:** "Implement entire auth system"
**Too small:** "Add import statement"

## Enforcement Rules

1. **No Create Without Connect** — Creation needs connection tasks
2. **No Connect Without Verify** — Connection needs verification
3. **No Verify Without Evidence** — Attach proof when checking
4. **Phase 3 Blocks Completion** — Cannot complete without runtime proof

## Supporting Files

### References
- [references/reference.md](references/reference.md) - Task states, sync protocol, refactor tracking
- [references/integration-requirements.md](references/integration-requirements.md) - CCV principle, patterns

### Templates
- [templates/todo-templates.md](templates/todo-templates.md) - Five use-case templates
- [templates/refactor-todo-template.md](templates/refactor-todo-template.md) - ADR-governed refactor
- [templates/integration-verification-checklist.md](templates/integration-verification-checklist.md) - Integration verification

### Examples
- [examples/examples.md](examples/examples.md) - Workflows and examples

## Red Flags

| Anti-Pattern | Why Bad |
|--------------|---------|
| Todos for trivial tasks | Overhead exceeds value |
| Vague descriptions | No clear acceptance criteria |
| Refactor without ADR | Violates policy |
| TodoWrite out of sync | Breaks single source of truth |
| Tasks too large/small | Poor granularity |
| Session todo for production work | Should use ./todo.md |

## Success Metrics

| Metric | Target |
|--------|--------|
| Context reduction | 80% vs agent prompts |
| Sync accuracy | 100% todo.md ↔ TodoWrite |
| ADR compliance | 100% for refactors |
| Integration verification | All Phase 3 tasks have evidence |

---

**Version:** 2.0.0 | **Updated:** 2025-12-07
