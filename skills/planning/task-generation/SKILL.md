---
description: This skill should be used when generating implementation tasks from PRDs, decomposing features into atomic tasks, inferring dependencies, or mapping PRD content to task metadata.
triggers:
  - generate tasks from PRD
  - create tasks from requirements
  - decompose features into tasks
  - PRD to tasks
  - task generation
  - implementation tasks
---

# Task Generation Skill

This skill provides structured knowledge for transforming Product Requirements Documents into Claude Code native Tasks with proper dependencies, metadata, and acceptance criteria.

## Core Principles

### 1. Atomic Task Decomposition

Tasks should be:
- **Single Responsibility**: Each task accomplishes one specific outcome
- **Independent**: Minimal coupling with other tasks where possible
- **Verifiable**: Clear completion criteria that can be objectively assessed
- **Estimable**: Complexity can be reasonably assessed (XS/S/M/L/XL)

### 2. Layered Architecture Pattern

Decompose features following natural implementation layers:

```
Data Model → API/Service → Business Logic → UI/Frontend → Tests
```

This pattern ensures:
- Dependencies flow in one direction
- Each layer can be implemented and tested independently
- Integration points are well-defined

### 3. PRD-to-Task Traceability

Every task should trace back to the source PRD:
- Reference specific section numbers
- Quote relevant user stories
- Link acceptance criteria to PRD requirements

## Task Schema

Each task created via TaskCreate follows this enhanced structure with categorized acceptance criteria and testing requirements:

```
TaskCreate:
  subject: "Create User data model"                    # Imperative mood
  description: |
    Define the User data model based on PRD section 7.3.

    Fields:
    - id: UUID (primary key)
    - email: string (unique, required)
    - passwordHash: string (required)
    - createdAt: timestamp

    **Acceptance Criteria:**

    _Functional:_
    - [ ] Schema defined with all required fields
    - [ ] Indexes created for email lookup
    - [ ] Migration script created

    _Edge Cases:_
    - [ ] Handle duplicate email constraint violation
    - [ ] Support maximum email length (254 chars)

    _Error Handling:_
    - [ ] Clear error messages for constraint violations

    **Testing Requirements:**
    • Unit: Schema validation for all field types
    • Unit: Email format validation
    • Integration: Database persistence and retrieval
    • Integration: Unique constraint enforcement

    Source: specs/PRD-Auth.md Section 7.3
  activeForm: "Creating User data model"              # Present continuous
  metadata:
    priority: critical                                # From PRD P0-P3
    complexity: S                                     # XS/S/M/L/XL
    source_section: "7.3 Data Models"                 # PRD section reference
    prd_path: "specs/PRD-Auth.md"                     # Source PRD
    feature_name: "User Authentication"               # Parent feature
    task_uid: "specs/PRD-Auth.md:user-auth:model:001" # Unique ID for merge
```

### Acceptance Criteria Categories

Structure acceptance criteria into these categories:

| Category | Purpose | Examples |
|----------|---------|----------|
| **Functional** | Core behavior that must work | Feature works as specified, correct outputs |
| **Edge Cases** | Boundary conditions, unusual scenarios | Empty input, max values, concurrent ops |
| **Error Handling** | Failure scenarios and recovery | Invalid input, network failures, timeouts |
| **Performance** | Speed and resource requirements | Response times, throughput targets |

### Testing Requirements Section

Add a Testing Requirements section below acceptance criteria. Infer test types from:
1. **Task layer** - Data model → Unit + Integration; API → Integration + E2E
2. **PRD testing section** - Extract explicit test requirements from Section 8
3. **Task priority** - Higher priority → more thorough testing

See `references/testing-requirements.md` for detailed test type mappings.

## PRD Section Mapping

Extract task information from specific PRD sections:

| PRD Section | What to Extract | Task Type |
|-------------|-----------------|-----------|
| 5.x Functional Requirements | Feature names, priorities, user stories | Feature tasks |
| 6.x Non-Functional Requirements | Performance, security constraints | Constraint tasks |
| 7.x Technical Considerations | Architecture, tech stack | Infrastructure tasks |
| 7.3 Data Models (Full-Tech) | Entity definitions | Data model tasks |
| 7.4 API Specifications (Full-Tech) | Endpoints | API tasks |
| 9.x Implementation Plan | Phase ordering, deliverables | Phase grouping |
| 10.x Dependencies | Blocking relationships | Dependency inference |

## Priority Mapping

Convert PRD priority notation to task priority:

| PRD Priority | Task Priority | Meaning |
|--------------|---------------|---------|
| P0 (Critical) | `critical` | Blocking release, must be done first |
| P1 (High) | `high` | Core functionality, high value |
| P2 (Medium) | `medium` | Important but not blocking |
| P3 (Low) | `low` | Nice to have, can be deferred |

## Complexity Estimation

Estimate task complexity using T-shirt sizing:

| Size | Scope | Typical Lines | Example |
|------|-------|---------------|---------|
| XS | Single simple function | <20 | Add config constant |
| S | Single file, straightforward | 20-100 | Create data model |
| M | Multiple files, moderate logic | 100-300 | Implement API endpoint |
| L | Multiple components, significant logic | 300-800 | Build feature module |
| XL | System-wide, complex integration | >800 | Major refactoring |

## Depth-Aware Task Generation

Adjust task granularity based on PRD depth level:

### High-Level PRD
- Create 1-2 tasks per feature
- Focus on feature-level deliverables
- Minimal technical breakdown
- Example: "Implement user authentication feature"

### Detailed PRD
- Create 3-5 tasks per feature
- Decompose by functional area
- Include acceptance criteria from user stories
- Example: "Implement login endpoint", "Create password validation"

### Full-Tech PRD
- Create 5-10 tasks per feature
- Granular technical decomposition
- Include data model, API, and test tasks
- Example: "Create User model", "Implement POST /auth/login", "Add User model tests"

## Merge Strategy for Re-runs

When generating tasks for a PRD that already has tasks:

1. **Match by task_uid**: Find existing tasks with same `metadata.task_uid`
2. **Preserve status**: Never change status of `in_progress` or `completed` tasks
3. **Update descriptions**: Refresh descriptions if PRD changed
4. **Add new tasks**: Create tasks for new requirements
5. **Flag obsolete**: Ask user about tasks that no longer map to PRD

## Reference Files

- `references/decomposition-patterns.md` - Feature decomposition patterns by type
- `references/dependency-inference.md` - Automatic dependency inference rules
- `references/testing-requirements.md` - Test type mappings and acceptance criteria patterns
