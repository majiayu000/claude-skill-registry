---
name: speckit
description: Specification-Driven Development (SDD) toolkit. Transforms ideas into executable specifications, implementation plans, and task lists. Use for feature planning, PRD creation, or when user invokes /speckit.specify, /speckit.plan, /speckit.tasks commands.
license: MIT
---

# Spec Kit: Specification-Driven Development

## Overview

Spec Kit implements **Specification-Driven Development (SDD)** - a methodology where specifications drive code, not vice versa. Instead of specs serving as documentation for code, code becomes the expression of specifications.

### The Power Inversion

Traditional development: Code is truth, specs are scaffolding
**SDD**: Specifications are truth, code is generated output

This eliminates the gap between intent and implementation by making specifications executable through AI.

## Commands

### `/speckit.specify <feature-description>`

Creates a comprehensive feature specification from a natural language description.

**Usage**: `/speckit.specify Real-time chat with message history and presence`

**Output**:
- `specs/{feature-name}/spec.md` - Complete feature specification
- `specs/{feature-name}/checklists/requirements.md` - Quality validation checklist

**Process**:
1. Parse user description, extract key concepts (actors, actions, data, constraints)
2. Generate user scenarios with prioritized stories (P1, P2, P3)
3. Define functional requirements (FR-001, FR-002, etc.)
4. Create measurable success criteria
5. Identify key entities
6. Validate against quality checklist
7. Present clarification questions (max 3) if critical ambiguities exist

**Guidelines**:
- Focus on WHAT users need and WHY
- Avoid HOW (no tech stack, APIs, code structure)
- Make informed guesses using industry standards
- Limit `[NEEDS CLARIFICATION]` markers to 3 maximum
- Every requirement must be testable

For detailed template: read `references/spec-template.md`
For command details: read `references/commands/specify.md`

---

### `/speckit.plan [tech-context]`

Creates an implementation plan from an existing specification.

**Usage**: `/speckit.plan WebSocket, PostgreSQL, Redis` or `/speckit.plan` (will determine tech from context)

**Prerequisites**: `spec.md` must exist in the feature directory

**Output**:
- `specs/{feature}/plan.md` - Implementation plan with tech decisions
- `specs/{feature}/research.md` - Technology research and decisions
- `specs/{feature}/data-model.md` - Entity definitions
- `specs/{feature}/contracts/` - API specifications (OpenAPI/GraphQL)
- `specs/{feature}/quickstart.md` - Validation scenarios

**Process**:
1. Load feature specification and project constitution
2. Fill Technical Context section
3. Run Constitution Check (evaluate architectural gates)
4. Phase 0: Research unknowns, generate `research.md`
5. Phase 1: Design data models, generate contracts
6. Re-evaluate constitution compliance post-design

**Constitution Gates** (if using constitution):
- Simplicity Gate: Using ≤3 projects? No future-proofing?
- Anti-Abstraction Gate: Using framework directly?
- Integration-First Gate: Contracts defined?

For detailed template: read `references/plan-template.md`
For command details: read `references/commands/plan.md`

---

### `/speckit.tasks`

Generates an executable task list from the implementation plan.

**Usage**: `/speckit.tasks`

**Prerequisites**: `plan.md` and `spec.md` must exist

**Output**:
- `specs/{feature}/tasks.md` - Dependency-ordered task list

**Process**:
1. Load plan.md (tech stack, structure) and spec.md (user stories)
2. Optionally load: data-model.md, contracts/, research.md
3. Generate tasks organized by user story:
   - Phase 1: Setup (shared infrastructure)
   - Phase 2: Foundational (blocking prerequisites)
   - Phase 3+: User Stories in priority order (P1, P2, P3...)
   - Final Phase: Polish & cross-cutting
4. Mark parallelizable tasks with `[P]`
5. Number tasks (T001, T002...)
6. Generate dependency graph and parallel execution examples

**Task Format**: `[ID] [P?] [Story] Description`
- `[P]` = Can run in parallel (different files, no dependencies)
- `[Story]` = Which user story (US1, US2, US3)

For detailed template: read `references/tasks-template.md`
For command details: read `references/commands/tasks.md`

---

## Workflow Example

```bash
# 1. Create specification (5 min)
/speckit.specify Real-time chat with message history and user presence

# 2. Generate implementation plan (5 min)
/speckit.plan WebSocket for messaging, PostgreSQL for history, Redis for presence

# 3. Create task list (5 min)
/speckit.tasks
```

**Result** (in 15 minutes):
- Complete feature spec with user stories and acceptance criteria
- Detailed implementation plan with technology rationale
- API contracts and data models
- Executable task list organized by user story

## Project Constitution

A constitution defines immutable architectural principles for a project. When present at `memory/constitution.md`, the `/speckit.plan` command will:

1. Validate against constitutional gates before planning
2. Require justification for any violations
3. Track complexity deviations

**Sample principles**:
- Library-First: Features start as standalone libraries
- Test-First: TDD mandatory (Red-Green-Refactor)
- Simplicity: Maximum 3 projects, YAGNI
- Integration-First: Real databases over mocks

For constitution template: read `references/constitution-template.md`

## Key Concepts

### User Story Organization

Tasks are grouped by user story to enable:
- Independent implementation
- Independent testing
- Incremental delivery (ship P1, then P2, then P3)

### MVP-First Delivery

1. Complete Setup + Foundational phases
2. Implement User Story 1 (P1) → Test → Deploy
3. Add User Story 2 (P2) → Test → Deploy
4. Continue incrementally

### Template-Driven Quality

Templates constrain AI behavior for better outcomes:
- Prevent premature implementation details
- Force explicit uncertainty markers
- Enforce test-first thinking
- Prevent speculative features

## File Locations

When working in a project:
- Specifications: `specs/{feature-name}/`
- Constitution: `memory/constitution.md`

## Reference Files

- `references/spec-template.md` - Feature specification template
- `references/plan-template.md` - Implementation plan template
- `references/tasks-template.md` - Task list template
- `references/constitution-template.md` - Project constitution template
- `references/methodology.md` - Full SDD philosophy document
- `references/commands/` - Detailed command definitions
