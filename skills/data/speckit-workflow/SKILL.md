---
name: speckit-workflow
version: 1.0.0
description: Spec-driven development workflow for creating feature specifications, clarifying requirements, building technical plans, and generating implementation tasks. Follows the SpecKit methodology for structured software development from natural language descriptions. Use when starting new features, writing specifications, creating implementation plans, or breaking down work into tasks.
---

# SpecKit: Spec-Driven Development Workflow

Guide users through structured specification-driven development from feature description to implementation tasks. This skill implements the complete SpecKit methodology for turning natural language feature descriptions into actionable development work.

## Triggers

Use this skill when:
- Starting a new feature development
- Writing feature specifications
- Clarifying ambiguous requirements
- Creating technical implementation plans
- Breaking down work into actionable tasks
- Generating user stories and acceptance criteria
- Keywords: speckit, specification, spec, feature, requirements, user story, acceptance criteria, implementation plan, task breakdown

## Workflow Overview

```
SPECKIT PIPELINE

  /speckit-specify     Create specification from description
        |
        v
  /speckit-clarify     Identify and resolve ambiguities (optional)
        |
        v
  /speckit-plan        Generate technical implementation plan
        |
        v
  /speckit-tasks       Break plan into actionable tasks
        |
        v
  /speckit-implement   Execute implementation (iterative)
```

---

## Phase 1: Specify - Create Feature Specification

### Purpose

Transform natural language feature descriptions into structured specifications. Focus on **WHAT** users need and **WHY** - avoid implementation details.

### Process

1. **Analyze Description**: Extract key concepts (actors, actions, data, constraints)
2. **Generate Branch Name**: Create 2-4 word short name (action-noun format)
3. **Create Spec Directory**: `specs/<NNN-feature-name>/`
4. **Fill Required Sections**:
   - User Scenarios with priorities (P1, P2, P3)
   - Functional Requirements (FR-001, FR-002, etc.)
   - Success Criteria (measurable, technology-agnostic)
5. **Mark Ambiguities**: Maximum 3 `[NEEDS CLARIFICATION]` markers

### Specification Template

```markdown
# Feature: [Feature Name]

## Overview
[1-2 paragraph summary of the feature]

## User Scenarios

### P1: [Primary User Journey] (MVP)
**As a** [user type]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- Given [context], when [action], then [outcome]
- Given [context], when [action], then [outcome]

### P2: [Secondary Journey]
[Same format as P1]

## Functional Requirements

- **FR-001**: System MUST [specific capability]
- **FR-002**: System MUST [specific capability]
- **FR-003**: System SHOULD [optional capability]

## Success Criteria

- Users can complete [journey] in under [time]
- System supports [scale metric]
- [Measurable outcome]

## Out of Scope
- [Explicitly excluded items]

## Clarifications
[This section populated during clarify phase]
```

### Key Rules

- Focus on user value and business needs
- Write for non-technical stakeholders
- No implementation details (languages, frameworks, APIs)
- Requirements must be testable and unambiguous

---

## Phase 2: Clarify - Resolve Ambiguities

### Purpose

Detect and reduce ambiguity in the specification by asking targeted clarification questions and encoding answers back into the spec.

### Process

1. **Load Specification**: Read current spec file
2. **Scan for Ambiguities**: Check coverage across categories
3. **Generate Questions**: Maximum 5 questions, prioritized by impact
4. **Sequential Questioning**: Present ONE question at a time
5. **Integrate Answers**: Update spec immediately after each answer

### Ambiguity Categories

| Category | What to Check |
|----------|---------------|
| Functional Scope | User goals, out-of-scope declarations |
| Domain & Data Model | Entities, relationships, state transitions |
| Interaction & UX | User journeys, error states, accessibility |
| Non-Functional | Performance, scalability, security |
| Integration | External services, APIs, failure modes |
| Edge Cases | Negative scenarios, conflict resolution |
| Constraints | Technical constraints, tradeoffs |
| Terminology | Glossary consistency |
| Completion Signals | Testable acceptance criteria |

### Question Format

For Multiple-Choice:
```markdown
**Recommended:** Option [X] - [1-2 sentence reasoning]

| Option | Description |
|--------|-------------|
| A | Option A description |
| B | Option B description |
| C | Option C description |

Reply with option letter, accept recommendation with "yes", or provide your own answer.
```

For Short-Answer:
```markdown
**Suggested:** [proposed answer] - [brief reasoning]

Format: Short answer (5 words max). Accept with "yes" or provide your own.
```

### Integration Rules

After each answer:
1. Add to `## Clarifications` section with session date
2. Apply to appropriate spec section
3. Replace conflicting earlier statements
4. Save immediately

---

## Phase 3: Plan - Create Implementation Plan

### Purpose

Create a technical implementation plan from the feature specification. Generate design artifacts including research, data models, and API contracts.

### Process

1. **Load Context**: Read spec and any existing research
2. **Fill Technical Context**: Tech stack, dependencies, constraints
3. **Research Phase**: Resolve any NEEDS CLARIFICATION items
4. **Design Phase**: Generate data models and contracts
5. **Structure Phase**: Define project layout

### Generated Artifacts

```
specs/<feature>/
├── spec.md           # Feature specification
├── plan.md           # Implementation plan
├── research.md       # Research and decisions
├── data-model.md     # Entity definitions
├── quickstart.md     # Getting started guide
└── contracts/
    └── api-spec.json # OpenAPI specification
```

### Implementation Plan Template

```markdown
# Implementation Plan: [Feature Name]

## Technical Context

**Language/Version**: [e.g., Python 3.11, TypeScript 5.x]
**Primary Dependencies**: [e.g., FastAPI, React]
**Storage**: [e.g., PostgreSQL, MongoDB]
**Testing**: [e.g., pytest, Jest]
**Target Platform**: [e.g., Linux container, AWS Lambda]

## Project Structure

src/
├── models/
├── services/
├── api/
└── lib/

tests/
├── unit/
├── integration/
└── e2e/

## Data Model Summary

[Key entities and relationships]

## API Endpoints Summary

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/v1/resource | Create resource |
| GET | /api/v1/resource/:id | Get resource |

## Implementation Phases

1. Setup & Infrastructure
2. Core Data Model
3. Business Logic
4. API Layer
5. Testing & Polish
```

---

## Phase 4: Tasks - Generate Actionable Tasks

### Purpose

Generate dependency-ordered task list organized by user story from the implementation plan.

### Task Format (Required)

```
- [ ] T001 [P] [US1] Description with file path
```

Components:
- **Checkbox**: Always `- [ ]`
- **Task ID**: Sequential (T001, T002...)
- **[P]**: Parallelizable (different files, no dependencies)
- **[Story]**: User story label (US1, US2...)
- **Description**: Clear action with exact file path

### Phase Structure

```markdown
## Phase 1: Setup (Shared Infrastructure)
- Project initialization
- Dependencies

## Phase 2: Foundational (Blocking Prerequisites)
- Database schema
- Authentication
- Base models
**Checkpoint**: Foundation ready

## Phase 3: User Story 1 - [Title] (P1) MVP
**Goal**: [What this delivers]
**Independent Test**: [How to verify]

### Tests for User Story 1
- [ ] T010 [P] [US1] Contract test for endpoint

### Implementation for User Story 1
- [ ] T012 [P] [US1] Create Model in src/models/
- [ ] T013 [US1] Implement Service in src/services/
- [ ] T014 [US1] Implement endpoint in src/api/

**Checkpoint**: US1 complete

## Phase 4+: Additional User Stories
[Same pattern]

## Phase N: Polish & Cross-Cutting
- Documentation
- Performance optimization
```

### MVP Strategy

1. Complete Setup + Foundational
2. Complete User Story 1 (P1)
3. STOP and VALIDATE
4. Deploy/demo if ready
5. Then continue with US2, US3...

---

## Integration with Archon

### Create Tasks in Archon

```python
# For each generated task:
manage_task("create",
    project_id="<PROJECT_ID>",
    title="T001: Create User model",
    description="Create User model in src/models/user.py with fields...",
    status="todo",
    feature="User Story 1",
    task_order=10
)
```

### Task Status Flow

```
todo -> doing -> review -> done
```

---

## Best Practices

1. **Start with Why**: Understand user value before technical details
2. **One Concern Per Section**: Keep spec sections focused
3. **Testable Everything**: All requirements must be verifiable
4. **Iterative Refinement**: Multiple clarify passes are OK
5. **Technology Agnostic Specs**: Keep impl details in plan, not spec
6. **MVP First**: Prioritize P1 stories for initial delivery
7. **Checkpoints Matter**: Validate at each phase boundary

---

## Command Reference

| Command | Description |
|---------|-------------|
| `/speckit-specify <description>` | Create spec from description |
| `/speckit-clarify` | Run clarification on current spec |
| `/speckit-plan <tech-stack>` | Generate implementation plan |
| `/speckit-tasks` | Generate task breakdown |
| `/speckit-status` | Show current spec status |

---

## Notes

- Specifications should be written for stakeholders, not developers
- The plan document is where technical decisions live
- Tasks should be small enough for one session (30min-4hrs)
- Use Archon for persistent task tracking across sessions
