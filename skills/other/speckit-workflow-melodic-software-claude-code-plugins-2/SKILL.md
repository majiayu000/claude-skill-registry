---
name: speckit-workflow
description: GitHub Spec Kit 5-phase workflow. Use when following the Constitution → Specify → Plan → Tasks → Implement cycle. Provides phase guidance, file templates, and workflow orchestration.
allowed-tools: Read, Glob, Grep, Write, Edit, Task
---

# Spec Kit Workflow

GitHub Spec Kit 5-phase specification-driven development workflow.

## When to Use This Skill

**Keywords:** Spec Kit, 5-phase workflow, constitution, specify, plan, tasks, implement, feature.md, design.md, tasks.md, specification workflow, GitHub Spec Kit, constitution.md, phased development

**Use this skill when:**

- Implementing specification-driven development workflows
- Creating or updating project constitution files
- Generating feature specifications from requirements
- Creating implementation plans from specifications
- Breaking down plans into task lists
- Following the full Specify → Plan → Tasks → Implement cycle

## Workflow Overview

```text
Phase 0: Constitution (One-time setup)
    ↓
Phase 1: Specify (Generate feature.md)
    ↓
Phase 2: Plan (Generate design.md)
    ↓
Phase 3: Tasks (Generate tasks.md)
    ↓
Phase 4: Implement (Code with guidance)
```

## Phase 0: Constitution

### Purpose

Establish project-wide principles, constraints, and non-functional requirements that guide ALL specifications.

### File: `.constitution.md`

```markdown
# Project Constitution

## Core Principles
- <principle 1>
- <principle 2>

## Technical Constraints
- <constraint 1>
- <constraint 2>

## Quality Standards
- <standard 1>
- <standard 2>

## Non-Functional Requirements
- Performance: <requirement>
- Security: <requirement>
- Accessibility: <requirement>
```

### Constitution Checklist

- [ ] Core development principles defined
- [ ] Technical constraints documented
- [ ] Quality standards specified
- [ ] Non-functional requirements listed
- [ ] Team conventions captured
- [ ] Dependencies and integration requirements noted

### When to Update

Update the constitution when:

- New non-functional requirements emerge
- Team conventions change
- Architectural decisions impact all features
- Project-wide constraints are added

## Phase 1: Specify

### Purpose

Transform a feature request or user story into a structured specification with EARS requirements and acceptance criteria.

### Input

- Feature request (natural language)
- User story (As a... I want... So that...)
- Problem statement

### Output: `feature.md`

```markdown
# Feature: <Feature Name>

## Context
### Problem Statement
<What problem does this solve?>

### Motivation
<Why is this important?>

### Scope
<What's in/out of scope?>

## Requirements

### REQ-001: <Requirement Title>
**EARS Pattern:** <ubiquitous|state-driven|event-driven|unwanted|optional>
**Priority:** <must|should|could>
**Text:** <EARS-formatted requirement>

#### Acceptance Criteria
- **AC-001:**
  - Given: <precondition>
  - When: <action>
  - Then: <outcome>

### REQ-002: ...

## Dependencies
- <dependency 1>
- <dependency 2>

## Risks
- <risk 1>
- <risk 2>
```

### Specify Phase Checklist

- [ ] Problem statement is clear and specific
- [ ] All requirements use EARS patterns
- [ ] Each requirement has acceptance criteria
- [ ] Requirements are prioritized (MoSCoW)
- [ ] Dependencies identified
- [ ] Risks documented
- [ ] Scope boundaries defined

## Phase 2: Plan

### Purpose

Design the technical implementation approach for the specified feature.

### Input

- `feature.md` from Phase 1
- Constitution constraints
- Existing codebase context

### Output: `design.md`

```markdown
# Design: <Feature Name>

## Overview
<High-level approach>

## Architecture

### Component Design
- <component 1>: <purpose>
- <component 2>: <purpose>

### Data Model
<Entities, relationships, schema changes>

### API Design
<Endpoints, contracts, interfaces>

## Technical Approach

### Approach Selected
<Chosen approach with rationale>

### Alternatives Considered
| Alternative | Pros | Cons | Why Not |
| --- | --- | --- | --- |
| <alt 1> | ... | ... | ... |

## Integration Points
- <integration 1>
- <integration 2>

## Testing Strategy
- Unit tests: <approach>
- Integration tests: <approach>
- E2E tests: <approach>

## Rollout Plan
<How will this be deployed?>
```

### Plan Phase Checklist

- [ ] Architecture aligns with constitution
- [ ] All requirements can be addressed
- [ ] Alternatives were considered
- [ ] Data model is complete
- [ ] API contracts defined
- [ ] Testing strategy covers acceptance criteria
- [ ] Integration points identified
- [ ] Rollout plan exists

## Phase 3: Tasks

### Purpose

Break down the design into implementable tasks with clear deliverables.

### Input

- `design.md` from Phase 2
- `feature.md` requirements for traceability

### Output: `tasks.md`

````markdown
# Tasks: <Feature Name>

## Task List

### TSK-001: <Task Title>
**Status:** pending
**Requirement:** REQ-001
**Estimated Effort:** <S|M|L|XL>

**Description:**
<What needs to be done>

**Deliverables:**
- [ ] <deliverable 1>
- [ ] <deliverable 2>

**Acceptance Criteria:**
- [ ] <criterion 1>
- [ ] <criterion 2>

### TSK-002: ...

## Dependency Graph

```text
TSK-001 → TSK-003
TSK-002 → TSK-003
TSK-003 → TSK-004
```

## Effort Summary

| Size | Count | Typical Duration |
| --- | --- | --- |
| S | <n> | < 2 hours |
| M | <n> | 2-4 hours |
| L | <n> | 4-8 hours |
| XL | <n> | > 8 hours |
````

### Tasks Phase Checklist

- [ ] Every requirement has at least one task
- [ ] Tasks are independently deliverable
- [ ] Dependencies are mapped
- [ ] Effort estimates provided
- [ ] Acceptance criteria are testable
- [ ] No task is larger than XL
- [ ] Critical path identified

## Phase 4: Implement

### Purpose

Execute tasks with continuous validation against specifications.

### Input

- `tasks.md` from Phase 3
- `design.md` for technical guidance
- `feature.md` for acceptance criteria

### Workflow

```text
1. Select next task (respecting dependencies)
2. Review task deliverables and acceptance criteria
3. Implement the task
4. Validate against acceptance criteria
5. Mark task complete
6. Repeat until all tasks done
```

### Implementation Checklist (Per Task)

- [ ] Task dependencies are complete
- [ ] Implementation follows design
- [ ] Code passes acceptance criteria
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Task marked complete in tasks.md

### Feature Completion Checklist

- [ ] All tasks marked complete
- [ ] All acceptance criteria verified
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Feature reviewed against original request

## Phase Transitions

### Phase 0 → Phase 1

**Gate:** Constitution exists and is current

**Validation:**

- [ ] `.constitution.md` file exists
- [ ] Constitution reviewed within last quarter
- [ ] No blocking updates needed

### Phase 1 → Phase 2

**Gate:** Specification is complete and valid

**Validation:**

- [ ] All requirements use EARS patterns
- [ ] All requirements have acceptance criteria
- [ ] Priorities assigned
- [ ] Dependencies identified
- [ ] Stakeholder approval (if required)

### Phase 2 → Phase 3

**Gate:** Design is implementable

**Validation:**

- [ ] Design addresses all requirements
- [ ] Architecture aligns with constitution
- [ ] Technical approach selected
- [ ] Integration points defined
- [ ] Testing strategy documented

### Phase 3 → Phase 4

**Gate:** Tasks are ready for implementation

**Validation:**

- [ ] All tasks mapped to requirements
- [ ] Dependencies graphed
- [ ] Effort estimated
- [ ] No blocking dependencies external to feature
- [ ] Development environment ready

## Prompts Reference

### Specify Prompt

Located at: `prompts/specify.prompt.md`

Key sections:

- Context extraction from user input
- EARS pattern application
- Acceptance criteria generation
- Prioritization guidance

### Plan Prompt

Located at: `prompts/plan.prompt.md`

Key sections:

- Architecture design
- Alternatives analysis
- Testing strategy
- Integration planning

### Tasks Prompt

Located at: `prompts/tasks.prompt.md`

Key sections:

- Task decomposition
- Dependency mapping
- Effort estimation
- Acceptance criteria mapping

## File Organization

```text
.specs/
├── <feature-name>/
│   ├── feature.md      # Phase 1 output
│   ├── design.md       # Phase 2 output
│   └── tasks.md        # Phase 3 output
└── ...

.constitution.md        # Phase 0 (project root)
```

## Quick Commands

| Phase | Command | Description |
| --- | --- | --- |
| 0 | `/spec:constitution` | Create/update constitution |
| 1 | `/spec:specify` | Generate specification |
| 2 | `/spec:plan` | Generate design |
| 3 | `/spec:tasks` | Generate task breakdown |
| 4 | `/spec:implement` | Guided implementation |
| All | `/spec:speckit:run` | Full workflow |

## Integration with Canonical Spec

Spec Kit outputs map to the canonical specification model:

| Spec Kit | Canonical Field |
| --- | --- |
| feature.md context | `context.problem`, `context.motivation` |
| REQ-xxx | `requirements[].id` |
| EARS text | `requirements[].text` |
| Priority | `requirements[].priority` |
| AC-xxx | `requirements[].acceptance_criteria[]` |
| design.md | `implementation_notes` |

## References

**Detailed Documentation:**

- [Constitution Guide](references/constitution.md) - Constitution file patterns
- [Phase Reference](references/phase-reference.md) - Detailed phase instructions
- [Prompts Guide](references/prompts-guide.md) - Prompt templates per phase

**Related Skills:**

- `spec-management` - Specification workflow navigation
- `canonical-spec-format` - Canonical specification structure
- `ears-authoring` - EARS requirement patterns
- `gherkin-authoring` - Acceptance criteria syntax

---

**Last Updated:** 2025-12-24

## Version History

- **v1.0.0** (2025-12-26): Initial release

---
