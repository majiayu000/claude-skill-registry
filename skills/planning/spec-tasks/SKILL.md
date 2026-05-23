---
name: spec-tasks
description: Generate actionable, dependency-ordered tasks.md organized by user story. Use when user says "/spec-tasks", "create tasks", "generate task list" after /spec-plan to prepare for implementation.
---

# Spec-Tasks

Generate task list organized by user story for implementation.

**Prerequisites**: plan.md must exist (run `/spec-plan` first).

## Workflow

1. **Setup** - Run `.specify/scripts/bash/check-prerequisites.sh --json`
2. **Load documents** - plan.md (required), spec.md, data-model.md, contracts/
3. **Generate tasks** - Organized by user story priority
4. **Write tasks.md** - Using `.specify/templates/tasks-template.md`
5. **Report** - Task count, parallel opportunities, MVP scope

## Task Format

```markdown
- [ ] [TaskID] [P?] [Story?] Description with file path
```

| Component | Description |
|-----------|-------------|
| `- [ ]` | Checkbox (required) |
| `[T001]` | Sequential ID |
| `[P]` | Parallelizable (optional) |
| `[US1]` | User story label (for story phases) |

### Examples

```markdown
- [ ] T001 Create project structure per implementation plan
- [ ] T005 [P] Implement auth middleware in src/middleware/auth.py
- [ ] T012 [P] [US1] Create User model in src/models/user.py
```

## Phase Structure

| Phase | Purpose |
|-------|---------|
| Phase 1: Setup | Project initialization |
| Phase 2: Foundational | Blocking prerequisites |
| Phase 3+: User Stories | One phase per story (P1, P2, P3...) |
| Final: Polish | Cross-cutting concerns |

## Task Sources

1. **User Stories (spec.md)** - Primary organization
2. **Contracts** - Map endpoints to stories
3. **Data Model** - Map entities to stories
4. **Infrastructure** - Setup/foundational tasks

## Parallel Rules

- `[P]` = Different files, no dependencies
- Models before services
- Services before endpoints
- Tests FAIL before implementation (if TDD)

## Implementation Strategy

### MVP First
1. Setup → Foundational → User Story 1
2. Test US1 independently
3. Deploy/demo

### Incremental
1. Add each story independently
2. Test and deploy each increment

## Next Steps

After `/spec-tasks`:
- `/spec-analyze` - Check consistency
- `/spec-implement` - Execute tasks
