---
name: design
description: Create architecture documentation and ADRs from PRD requirements
argument-hint: [PRD path or architecture focus area]
user-invocable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebSearch
  - AskUserQuestion
context: fork
agent: architect
---

# /design - Architecture Design

Create architecture documentation and Architecture Decision Records from requirements.

## Purpose

Transform PRD requirements into:
- System architecture with components and interfaces
- Data flow and interaction patterns
- Constraints and risk analysis
- ADRs for significant decisions

## Inputs

- `$ARGUMENTS`: PRD path or specific focus area (optional)
- Default PRD location: `docs/architecture/PRD.md`
- Existing architecture: `docs/architecture/ARCHITECTURE.md`
- `${PROJECT_NAME}`: Current project context

## Outputs

- Architecture: `docs/architecture/ARCHITECTURE.md`
- ADRs: `docs/architecture/adr/NNN-decision-name.md`

## Workflow

### 1. Read Requirements
Load and understand the PRD:
- Functional requirements define WHAT to build
- Non-functional requirements define HOW it must perform
- User stories provide context for design decisions

### 2. Research Patterns
- Search for established patterns matching requirements
- Look up framework/library documentation
- Review prior art and alternatives

### 3. Identify Components
For each major functional area:
- Define component name and responsibility
- Specify interface/API contract
- List dependencies (internal and external)

### 4. Design Data Flow
- Map request/response flows
- Identify data transformations
- Document async/sync boundaries

### 5. Analyze Constraints
- Technical limitations
- Platform requirements
- Integration dependencies
- Performance bounds

### 6. Assess Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk description] | Low/Medium/High | Low/Medium/High | [Strategy] |

### 7. Document Trade-offs
For significant design choices:
- What alternatives were considered?
- Why was this option chosen?
- What are the consequences?

### 8. Create ADRs
For each significant decision, create an ADR:
```markdown
# ADR-NNN: [Decision Title]

**Status**: Proposed | Accepted | Deprecated
**Date**: [date]

## Context
[What is the issue/situation requiring a decision?]

## Decision
[What is the change/decision being made?]

## Rationale
[Why was this decision made?]

## Alternatives Considered
1. [Alternative 1]: [Why rejected]
2. [Alternative 2]: [Why rejected]

## Consequences
- [Positive consequence 1]
- [Positive consequence 2]
- [Negative consequence / trade-off]

## Related
- [Link to related ADRs]
- [Link to relevant requirements]
```

## Architecture Template

```markdown
# [Project Name] Architecture

**Version**: 0.1.0
**Date**: [date]
**Source**: [PRD.md](PRD.md)

---

## Overview
[High-level system diagram or description]

## Components

### [Component Name]
- **Responsibility**: [Single responsibility description]
- **Interface**: [API/contract definition]
- **Dependencies**: [What it requires]
- **Artifacts**: [What it produces]

## Data Flow
[Sequence or flow diagrams]

## Constraints
- [Technical constraint 1]
- [Platform constraint 2]

## Risks
[Risk table]

## Trade-offs
[Design decision rationale]

## Design Decisions
- [ADR-001](adr/001-decision.md): [Summary]
- [ADR-002](adr/002-decision.md): [Summary]
```

## Validation Checklist
- [ ] All FRs have corresponding components
- [ ] All components have clear responsibilities
- [ ] Interfaces are defined between components
- [ ] NFRs are addressed in design
- [ ] Risks are identified with mitigations
- [ ] Significant decisions have ADRs
