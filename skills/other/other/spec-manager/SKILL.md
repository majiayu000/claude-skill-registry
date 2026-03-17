---
name: spec-manager
description: Orchestrates specification management workflow by coordinating init-specs, specify-with-requirements, plan-with-specs, and update-requirements skills. Manages the full lifecycle of task specifications from requirements through implementation planning.
allowed-tools: Skill, Read, Write, Edit, Glob, Grep
user-invocable: false
---

# Spec Manager Agent

## Agent Type

This is an **orchestrator agent** that coordinates the full specification lifecycle for task planning. Unlike worker skills that perform specific tasks, this agent manages the workflow across requirements, specs, and plans.

## Coordinated Skills

- **init-specs**: Scaffold spec documents for a new task
- **specify-with-requirements**: Analyze requirements and generate technical specs
- **plan-with-specs**: Generate implementation plans from finalized specs
- **update-requirements**: Update requirements and cascade changes to specs and plans

## Purpose

This agent manages the complete specification lifecycle:

```
init-specs → (user writes requirements) → specify-with-requirements → (user reviews/clarifies) → plan-with-specs → (implementation) → update-requirements (as needed)
```

## Architecture

### Orchestrator Pattern

```
spec-manager (Orchestrator)
├── Phase 1: Initialize
│   └── Invokes init-specs → Scaffold markdown files
├── Phase 2: Specify
│   └── Invokes specify-with-requirements → Generate technical specs
├── Phase 3: Plan
│   └── Invokes plan-with-specs → Generate implementation plan
└── Phase 4: Update (iterative)
    └── Invokes update-requirements → Cascade changes through all docs
```

### File Structure

All spec documents live in `specs/` directory:

```
specs/
└── {task-slug}/
    ├── requirements.md   # User-authored requirements
    ├── specs.md           # Generated technical specifications
    └── plans.md           # Generated implementation plan
```

## Workflow

### Full Lifecycle

1. **User** runs `/init-specs <task title>` to scaffold documents
2. **User** writes requirements in `specs/{slug}/requirements.md`
3. **User** runs `/specify-with-requirements <slug>` to generate specs
4. **Agent** analyzes requirements, asks clarifying questions if needed
5. **User** reviews generated specs, iterates on clarifications
6. **User** runs `/plan-with-specs <slug>` to generate implementation plan
7. **User** reviews plan and begins implementation
8. During implementation, specs and plans are updated as needed
9. If requirements change, **user** runs `/update-requirements <change description>` to cascade updates

### Skill Invocation

Each skill is invoked independently by the user via slash commands. The spec-manager agent provides the shared context and conventions that all skills follow.

## Conventions

### File Naming

- Task titles are slugified: lowercase, hyphens for spaces, no special characters
- Example: "User Authentication Flow" → `user-authentication-flow`

### Document Cross-References

- Requirements link to nothing (they are the source of truth)
- Specs link back to requirements via `> Requirements: [...]`
- Plans link back to both requirements and specs

### Traceability

- Functional Requirements: `FR-1`, `FR-2`, ...
- Technical Specifications: `TS-1` (from `FR-1`), `TS-2` (from `FR-2`), ...
- Implementation Steps: `Step 1` references `TS-X`

### Status Flow

**Requirements**: `Draft` → `Final`
**Specs**: `Pending` → `Draft` → `Final`
**Plans**: `Pending` → `Ready` → `In Progress` → `Completed`

## Guidelines

### Do:
- Always read existing documents before making changes
- Maintain traceability between requirements → specs → plans
- Preserve completed work when cascading changes
- Log all clarifications and changes for audit trail
- Examine the codebase for context when generating specs and plans

### Don't:
- Generate specs from empty/template requirements
- Skip the clarification step when ambiguities exist
- Silently drop requirements, specs, or plan steps
- Modify completed implementation steps without explicit warning
- Proceed to the next phase without user review
