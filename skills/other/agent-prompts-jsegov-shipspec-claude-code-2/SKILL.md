---
name: agent-prompts
description: This skill should be used when the user asks to "generate tasks", "create implementation plan", "break down feature", "write agent prompts", "decompose into tasks", "create work items", or when creating agent-ready task descriptions from PRD and SDD documents.
version: 0.2.0
---

# Agent Prompt Generation

Create structured task prompts that coding agents can execute effectively.

## Output Files

Task generation produces two files:

| File | Purpose | Used By |
|------|---------|---------|
| `TASKS.json` | Machine-parseable metadata | Plugin agents, hooks, commands |
| `TASKS.md` | Human-readable task prompts | Developers, code review |

**Source of Truth**: TASKS.json is authoritative. TASKS.md is a derived human-readable view.

## TASKS.json Structure

```json
{
  "version": "1.0",
  "feature": "feature-name",
  "summary": {
    "total_tasks": 5,
    "total_points": 18,
    "critical_path": ["TASK-001", "TASK-003", "TASK-005"]
  },
  "phases": [
    { "id": 1, "name": "Foundation" },
    { "id": 2, "name": "Core Implementation" },
    { "id": 3, "name": "Polish" }
  ],
  "tasks": {
    "TASK-001": {
      "title": "Setup Database Schema",
      "status": "not_started",
      "phase": 1,
      "points": 3,
      "depends_on": [],
      "blocks": ["TASK-002", "TASK-003"],
      "prd_refs": ["REQ-001", "REQ-002"],
      "sdd_refs": ["Section 5.1"],
      "acceptance_criteria": [
        "Schema file exists at db/schema.sql",
        "All tables have primary keys",
        "Foreign key relationships match SDD",
        "Migration runs without errors"
      ],
      "testing": [
        "Run migration: npm run db:migrate",
        "Verify tables: npm run db:verify"
      ],
      "prompt": "## Context\nThis task establishes the data layer...\n\n## Requirements\n- Create users table with id, email, created_at\n..."
    }
  }
}
```

### Task Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Clear, action-oriented task title |
| `status` | enum | `"not_started"` \| `"in_progress"` \| `"completed"` |
| `phase` | integer | Phase number (1-indexed) |
| `points` | integer | Fibonacci story points: 1, 2, 3, 5, 8 |
| `depends_on` | array | Task IDs that must complete first |
| `blocks` | array | Task IDs that depend on this task |
| `prd_refs` | array | Requirement IDs (REQ-XXX) this task addresses |
| `sdd_refs` | array | SDD section references |
| `acceptance_criteria` | array | Verifiable criteria for completion |
| `testing` | array | Test commands or verification steps |
| `prompt` | string | Full markdown prompt for implementation |

## TASKS.md Structure

The markdown file contains human-readable content only. No status markers, dependencies, or acceptance criteria (those live in JSON).

```markdown
# Implementation Tasks: [Feature Name]

## Summary

- Total Tasks: 5
- Total Story Points: 18
- Critical Path: TASK-001 → TASK-003 → TASK-005

## Requirement Coverage

| Requirement | Task(s) |
|-------------|---------|
| REQ-001 | TASK-001, TASK-003 |
| REQ-002 | TASK-002, TASK-004 |

---

## Phase 1: Foundation

### TASK-001: Setup Database Schema

#### Context
This task establishes the data layer for the feature. The schema must support
all entities defined in the SDD and enable the API operations in Phase 2.

#### Requirements
- Create users table with id, email, created_at
- Create sessions table with foreign key to users
- Add indexes for common query patterns

#### Technical Approach
Follow the existing migration pattern in `db/migrations/`. Use the same
column naming conventions as existing tables.

#### Files to Create/Modify
- `db/migrations/002_add_users.sql` - New migration file
- `db/schema.sql` - Update schema documentation

#### Key Interfaces
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### Constraints
- Follow existing naming conventions (snake_case)
- Use SERIAL for auto-increment IDs
- All timestamps must include timezone

---

## Phase 2: Core Implementation

### TASK-002: Create API Endpoints
...
```

## Task Prompt Template

Each task's `prompt` field should follow this structure:

```markdown
## Context
[2-3 sentences explaining where this task fits in the larger system and why it matters]

## Requirements
- [Specific, verifiable requirement 1]
- [Specific, verifiable requirement 2]
- [Specific, verifiable requirement 3]

## Technical Approach

### Suggested Implementation
[Step-by-step guidance based on codebase patterns]

### Files to Create/Modify
- `path/to/new-file.ts` - [Purpose]
- `path/to/existing-file.ts` - [What changes]

### Key Interfaces
```typescript
// Define expected interfaces
interface ExpectedInput {
  field: string;
}

interface ExpectedOutput {
  result: boolean;
}
```

## Constraints
- Follow existing patterns in `[reference file]`
- Use `[specific library]` for `[purpose]`
- Do not modify `[protected area]`
- Maintain backward compatibility with `[existing API]`
```

## Task Sizing Guidelines

| Points | Description | Example |
|--------|-------------|---------|
| 1 | Trivial change | Config update, copy change |
| 2 | Small task | Single function, simple component |
| 3 | Medium task | Multiple functions, moderate complexity |
| 5 | Large task | Significant feature piece |
| 8 | Complex task | Cross-cutting, multiple systems |

**Rule:** Tasks >5 points trigger auto-refinement. Tasks >8 points must be broken down.

## Task Categories

| Category | Description | Examples |
|----------|-------------|----------|
| `feature` | New user-facing functionality | New UI component, API endpoint |
| `infrastructure` | Backend systems, tooling | Database migration, CI setup |
| `testing` | Test coverage | Unit tests, E2E tests |
| `documentation` | Docs and comments | API docs, README updates |
| `security` | Auth, permissions | Input validation, auth flow |
| `performance` | Optimization | Caching, query optimization |

## Dependency Mapping

When generating tasks, identify:

1. **Hard Dependencies (depends_on/blocks)**
   - Task X must complete before Task Y can start
   - Usually: schema → API → UI

2. **Parallel Tasks**
   - Can be worked on simultaneously
   - Usually: independent components, tests

3. **Critical Path**
   - The longest chain of dependent tasks
   - Store in `summary.critical_path`

## Execution Phases

Group tasks into logical phases:

| Phase | Purpose | Typical Tasks |
|-------|---------|---------------|
| 1: Foundation | Setup and infrastructure | Schema, types, config |
| 2: Core | Main implementation | APIs, services, core logic |
| 3: UI | User interface | Components, pages, forms |
| 4: Polish | Quality and docs | Tests, documentation, cleanup |

## Quality Checklist

Before finalizing tasks:

- [ ] Every task has clear acceptance criteria in JSON
- [ ] Dependencies form a valid DAG (no cycles)
- [ ] No task exceeds 8 story points
- [ ] Every requirement (REQ-XXX) maps to at least one task
- [ ] Tests are included as explicit tasks
- [ ] File paths reference actual codebase structure
- [ ] `prompt` field contains full implementation guidance

## Typical Decomposition Pattern

```
Feature X
├── TASK-001: Database schema/migrations (infrastructure, 3pts)
├── TASK-002: Type definitions and interfaces (infrastructure, 2pts)
├── TASK-003: API endpoint - create (feature, 3pts)
├── TASK-004: API endpoint - read (feature, 2pts)
├── TASK-005: API endpoint - update (feature, 3pts)
├── TASK-006: API endpoint - delete (feature, 2pts)
├── TASK-007: UI component - form (feature, 3pts)
├── TASK-008: UI component - list (feature, 3pts)
├── TASK-009: Unit tests (testing, 3pts)
├── TASK-010: Integration tests (testing, 3pts)
└── TASK-011: Documentation (documentation, 2pts)
```

## Schema Reference

See `references/tasks-schema.json` for the full JSON Schema specification.
See `references/state-schemas.json` for loop state file schemas.
