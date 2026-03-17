---
name: task-decomposition
description: "Expertise in breaking down specifications into executable, dependency-ordered tasks. Activates when user discusses task planning, work breakdown, or implementation ordering. Trigger keywords: task decomposition, work breakdown, task list, dependency order, implementation tasks, tasks.md, T001, parallelizable"
allowed-tools: Read, Write, Edit, Glob, Grep
user-invocable: false
---

# Task Decomposition Skill

## Purpose

This skill provides expertise in decomposing specifications into executable, dependency-ordered implementation tasks. It transforms structured requirements and user stories into a concrete work plan that developers can follow sequentially or in parallel. The output is a `tasks.md` file with numbered tasks, dependency annotations, and full traceability back to the specification.

## When It Activates

The skill is triggered when the conversation involves:

- Breaking down a specification into implementation tasks
- Creating or updating a `tasks.md` file
- Discussing work breakdown, task ordering, or dependency analysis
- Planning implementation phases or sprint work
- Identifying parallelizable work streams

## Capabilities

### 1. Phase-Based Task Ordering

Tasks are organized into five sequential phases:

| Phase | Purpose | Examples |
|-------|---------|---------|
| **Setup** | Project scaffolding, tooling, configuration | Init repo, install deps, configure linter |
| **Foundation** | Core infrastructure and data layer | Database schema, base models, auth setup |
| **Stories** | Feature implementation per user story | Implement US1, US2, US3 endpoints and UI |
| **Integration** | Cross-feature wiring, E2E flows | API integration, state management, routing |
| **Finalization** | Quality assurance, polish, deployment prep | Testing, docs, CI/CD, performance tuning |

Tasks within each phase are ordered by dependency. A later phase never starts before its prerequisites in earlier phases are complete.

### 2. Task Format

Every task follows this standardized format:

```
- [ ] T001 [P] [US1] path/to/file.ts -- Description (S) [Spec FR-001]
```

Where:

- `T001` -- Unique task identifier, zero-padded and sequential
- `[P]` -- Parallelizable marker (present only if the task can run concurrently with others)
- `[US1]` -- User story reference linking to the specification
- `path/to/file.ts` -- Primary file or directory affected
- `Description` -- Concise action description starting with a verb
- `(S)` -- Size estimate: `(S)` small, `(M)` medium, `(L)` large
- `[Spec FR-001]` -- Traceability reference back to a specific requirement section

### 3. Dependency Detection

The skill analyzes tasks to detect and annotate dependencies:

- **Explicit dependencies**: Task B requires output of Task A (e.g., schema before migration)
- **Implicit dependencies**: Shared file or module modifications that must be sequenced
- **Blocking dependencies**: Tasks that gate an entire phase transition

Dependencies are expressed as `depends: T001, T003` annotations when non-obvious ordering exists.

### 4. Parallel Task Identification

Tasks that share no dependencies are marked with the `[P]` flag, indicating they can be executed concurrently. The skill groups parallelizable tasks together within each phase to maximize throughput.

### 5. Coverage Validation

After generating the task list, the skill validates coverage:

- Every `FR-XXX` in the specification maps to at least one task
- Every `NFR-XXX` has a corresponding task or is addressed by a cross-cutting task
- Every user story (`US1`, `US2`, ...) appears in at least one task's `[USx]` tag

### 6. Gap Flagging

When coverage validation detects missing mappings, the skill inserts explicit gap markers:

```
- [ ] T015 [Gap] -- No task covers FR-012 (payment retry logic) [Spec FR-012]
```

Gap markers are clearly labeled with `[Gap]` so they can be identified and resolved before implementation begins.

## Methodology

The decomposition process follows these steps:

1. **Parse Specification**: Read `spec.md` to extract all FR, NFR, user stories, data model entities, and API contracts.
2. **Identify Work Units**: Map each requirement to one or more concrete implementation actions (file creation, function implementation, configuration change).
3. **Assign Phases**: Place each work unit into the appropriate phase (Setup, Foundation, Stories, Integration, Finalization).
4. **Detect Dependencies**: Analyze inter-task relationships and establish ordering constraints.
5. **Mark Parallelism**: Flag tasks with no dependencies as parallelizable `[P]`.
6. **Estimate Sizes**: Assign size estimates based on scope and complexity.
7. **Validate Coverage**: Ensure every requirement is covered by at least one task.
8. **Flag Gaps**: Insert `[Gap]` markers for any uncovered requirements.

## References

For detailed format specifications, dependency patterns, and phase ordering rules, consult:

- `references/task-format.md` -- Full task format specification with examples
- `references/dependency-patterns.md` -- Common dependency patterns and resolution strategies
- `references/phase-ordering.md` -- Phase definitions, transition criteria, and ordering rules
