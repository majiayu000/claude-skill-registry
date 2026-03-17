---
name: task-decomposition
description: Use when the Architect is breaking down change requests into implementable tasks, defining acceptance criteria, estimating task size, mapping dependencies, or creating technical sub-tasks for Developer and Integrator.
version: 1.0.0
---

# Task Decomposition Expertise

## When This Applies

Apply this guidance when:
- Breaking a CR into implementation tasks
- Creating technical sub-tasks from architecture
- Writing acceptance criteria for tasks
- Mapping task dependencies
- Estimating effort and sizing

## Decomposition Process

### Step 1: Identify Work Streams

From the CR and architecture, identify:
1. **Data layer tasks** — Models, migrations, storage
2. **Logic layer tasks** — Business logic, services, validation
3. **Interface layer tasks** — APIs, UI, integrations
4. **Test tasks** — Unit tests, e2e tests, test data
5. **Infrastructure tasks** — Config, deployment, CI/CD

### Step 2: Size Each Task

A good task is:
- **Completable in one session** — If it takes more, break it down further
- **Independently testable** — Can be verified without other tasks
- **Clearly scoped** — Developer knows exactly what files to touch
- **Has clear done criteria** — Unambiguous definition of complete

### Size Guidelines

| Size | Lines of Code | Files | Complexity |
|------|--------------|-------|------------|
| Small | < 50 | 1-2 | Straightforward |
| Medium | 50-200 | 2-5 | Some decisions required |
| Large | 200+ | 5+ | Break down further |

### Step 3: Define Dependencies

Map which tasks must complete before others can start:

```
TASK-001 (data model) ─┬─▶ TASK-003 (API endpoint)
TASK-002 (auth logic)  ─┘         │
                                  ▼
                          TASK-004 (integration tests)
```

Mark dependent tasks in their descriptions. Assign upstream tasks first.

### Step 4: Write Acceptance Criteria

Each task needs:
1. **Given** — Starting conditions and context
2. **When** — The action or change being made
3. **Then** — Expected outcome, verifiable result

Example:
```
Given: User model exists with email field
When: Login endpoint receives valid credentials
Then: Returns JWT token with 24h expiry and user profile
```

## Task Assignment Guidelines

| Task Type | Assign To |
|-----------|-----------|
| Feature implementation | Developer |
| Unit/e2e tests | Integrator |
| API design review | Self (Architect) |
| Database migrations | Developer (implement) → Integrator (commit) |
| CI/CD changes | DevOp |
| Deployment | DevOp → Production Engineer |

## Common Decomposition Patterns

### New Feature
1. Define data model → Developer
2. Implement business logic → Developer
3. Create API endpoint → Developer
4. Write unit tests → Integrator
5. Write e2e tests → Integrator
6. Update documentation → Architect

### Bug Fix
1. Reproduce and document → Developer
2. Implement fix → Developer
3. Add regression test → Integrator
4. Verify fix → Architect (review)

### Refactoring
1. Document current behavior with tests → Integrator
2. Refactor implementation → Developer
3. Verify tests still pass → Integrator
4. Review architecture impact → Architect
