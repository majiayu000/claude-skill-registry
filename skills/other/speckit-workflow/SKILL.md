---
name: speckit-workflow
description: Comprehensive understanding of the spec-kit methodology. Constitution-driven feature development with specify, plan, tasks, and implement phases.
version: 0.1.0
---

# SpecKit Workflow

The SpecKit methodology is a constitution-driven approach to feature development. It ensures consistency across features by grounding all decisions in project principles.

## Core Philosophy

**Constitution First**: Every feature is designed against the project's constitution - a living document of principles, constraints, and standards.

**Governance Over Convention**: Rather than implicit patterns, SpecKit makes governance explicit through:
- Constitution principles (MUST, SHOULD, MAY)
- Feature specifications tied to principles
- Quality checklists as "unit tests for requirements"
- Consistency analysis across artifacts

## Directory Structure

```text
.specify/
├── memory/
│   └── constitution.md       # Project principles and standards
├── .current-feature          # Active feature pointer
├── templates/                # Artifact templates
│   ├── spec-template.md
│   ├── plan-template.md
│   ├── tasks-template.md
│   └── checklist-template.md
└── specs/
    └── <id>-<name>/          # Feature directories
        ├── .speckit-state.json
        ├── .progress.md
        ├── .coordinator-prompt.md
        ├── spec.md           # Feature specification
        ├── plan.md           # Technical design
        ├── tasks.md          # Implementation tasks
        ├── research.md       # Research findings (optional)
        ├── data-model.md     # Entity definitions (optional)
        ├── contracts/        # API contracts (optional)
        └── checklists/       # Quality checklists
```

## Feature ID System

Features use auto-incremented 3-digit IDs:
- `001-user-auth`
- `002-payment-gateway`
- `003-notification-system`

Benefits:
- Natural ordering in filesystem
- Easy reference in commits/PRs
- Prevents naming conflicts

## Workflow Phases

### Phase 1: Constitution (`/speckit:constitution`)

Establish or update project-wide principles.

**Inputs**: Project context, team preferences
**Outputs**: `.specify/memory/constitution.md`

Constitution sections:
- **Identity**: Project name, purpose, core domain
- **Principles**: MUST/SHOULD/MAY rules
- **Technology Stack**: Languages, frameworks, tools
- **Patterns**: Architecture, naming, error handling
- **Quality Standards**: Testing, performance, security

### Phase 2: Specify (`/speckit:specify`)

Define the feature specification against constitution.

**Inputs**: Feature goal, constitution reference
**Outputs**: `spec.md`

Specification contains:
- Feature overview and goals
- User stories with acceptance criteria
- Constitution alignment markers
- Out of scope items
- Dependencies and risks

### Phase 3: Clarify (`/speckit:clarify`) - Optional

Resolve ambiguities through structured Q&A.

**Inputs**: `spec.md` with ambiguities
**Outputs**: Updated `spec.md` with clarifications

Rules:
- Maximum 5 clarifying questions per session
- Each question has 2-4 options + "Other"
- Recommendations marked when applicable
- Clarifications appended to spec

### Phase 4: Plan (`/speckit:plan`)

Generate technical design from specification.

**Inputs**: `spec.md`, constitution, codebase context
**Outputs**: `plan.md`, optionally `data-model.md`, `contracts/`

Plan contains:
- Architecture overview
- Component breakdown
- Data flow diagrams
- API contracts
- Integration points
- Risk mitigation

### Phase 5: Tasks (`/speckit:tasks`)

Break plan into dependency-ordered implementation tasks.

**Inputs**: `plan.md`, `spec.md`
**Outputs**: `tasks.md`

Task format:
```markdown
- [ ] T001 [P] [US1] Task description `path/to/file.ts`
```

Components:
- `T001`: Sequential task ID
- `[P]`: Parallel marker (optional)
- `[US1]`: User story reference (optional)
- Description with file path

Task phases:
1. **Setup**: Environment, dependencies, scaffolding
2. **Core**: Main implementation tasks
3. **Integration**: Connect components
4. **Polish**: Error handling, edge cases
5. **Verification**: Quality checkpoints

### Phase 6: Implement (`/speckit:implement`)

Execute tasks via Ralph Wiggum loop.

**Inputs**: `tasks.md`, state file
**Outputs**: Code changes, commits, updated progress

Execution model:
- Coordinator reads state, delegates to executor
- 4-layer verification before advancing
- Parallel execution for [P] marked tasks
- Fresh context per task

## State Management

### State File (`.speckit-state.json`)

```json
{
  "featureId": "001",
  "name": "user-auth",
  "basePath": ".specify/specs/001-user-auth",
  "phase": "execution",
  "taskIndex": 0,
  "totalTasks": 15,
  "taskIteration": 1,
  "maxTaskIterations": 5,
  "globalIteration": 1,
  "maxGlobalIterations": 100,
  "awaitingApproval": false
}
```

### Progress File (`.progress.md`)

Tracks:
- Completed tasks with commit hashes
- Learnings and context for future tasks
- Blockers and resolutions
- Cross-task dependencies

## Quality Assurance

### Checklists (`/speckit:checklist`)

Domain-specific quality checklists:
- UX checklist
- API checklist
- Security checklist
- Performance checklist
- Accessibility checklist

Checklists are "unit tests for requirements" - verifiable criteria before implementation.

### Analyze (`/speckit:analyze`)

Cross-artifact consistency analysis:
- Spec ↔ Constitution alignment
- Plan ↔ Spec coverage
- Tasks ↔ Plan traceability
- Identifies gaps, conflicts, ambiguities

## Command Reference

| Command | Purpose | Phase |
|---------|---------|-------|
| `/speckit:start <name>` | Create or resume feature | Entry |
| `/speckit:constitution` | Create/update project principles | 1 |
| `/speckit:specify` | Define feature specification | 2 |
| `/speckit:clarify` | Resolve spec ambiguities | 3 |
| `/speckit:plan` | Generate technical design | 4 |
| `/speckit:tasks` | Break plan into tasks | 5 |
| `/speckit:implement` | Execute tasks | 6 |
| `/speckit:analyze` | Check consistency | Any |
| `/speckit:checklist` | Generate quality checklist | Any |
| `/speckit:status` | Show current state | Any |
| `/speckit:switch <id>` | Change active feature | Any |
| `/speckit:cancel` | Stop execution, cleanup | Any |

## Agent Ecosystem

| Agent | Purpose | Used By |
|-------|---------|---------|
| `constitution-architect` | Create/update constitution | constitution |
| `spec-analyst` | Generate specifications | specify |
| `plan-architect` | Technical design | plan |
| `task-planner` | Task breakdown | tasks |
| `spec-executor` | Execute single task | implement |
| `qa-engineer` | Verification tasks | implement |

## Constitution Integration

All phases reference the constitution:

1. **Specify**: Maps features to constitution principles
2. **Plan**: Architecture follows constitution patterns
3. **Tasks**: Quality checkpoints enforce constitution
4. **Implement**: Executor validates against standards

Constitution markers in artifacts:
- `[C§3.1]`: References constitution section 3.1
- `[MUST]`: Required by constitution
- `[SHOULD]`: Recommended by constitution
- `[MAY]`: Optional per constitution

## Best Practices

### Starting New Features

1. Ensure constitution exists and is current
2. Use descriptive feature names (kebab-case)
3. Include clear success criteria in spec
4. Reference related features if applicable

### During Implementation

1. Follow task order (dependencies matter)
2. Commit after each task
3. Update progress with learnings
4. Run verification checkpoints

### Maintaining Constitution

1. Version constitution changes semantically
2. Run sync impact analysis after updates
3. Update affected features if needed
4. Document rationale for changes
