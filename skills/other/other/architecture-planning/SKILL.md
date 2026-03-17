---
name: architecture-planning
description: Create detailed architecture plans with decision records and risk
  assessments. Use when planning significant features or system changes.
---

# Architecture Planning Skill

## Purpose
Produce consistent, thorough architecture documentation for system design.

## When to Use
- Planning significant feature implementations
- Making technology or pattern decisions
- Designing new modules or services
- Before major refactoring efforts
- System integration planning

## Templates

### Main Templates
- [templates/architecture-doc.md](templates/architecture-doc.md) - Full architecture document
- [templates/decision-record.md](templates/decision-record.md) - ADR (Architecture Decision Record) format
- [templates/risk-assessment.md](templates/risk-assessment.md) - Risk matrix template

### Pattern Library
Reference established architectural patterns:
- [patterns/microservices.md](patterns/microservices.md) - Microservices architecture
- [patterns/monolith.md](patterns/monolith.md) - Monolithic architecture
- [patterns/serverless.md](patterns/serverless.md) - Serverless architecture

## Decision Framework

### When to Create an ADR
Create a formal Architecture Decision Record when:
- Choosing between technologies (database, framework, library)
- Selecting architectural patterns (monolith vs microservice)
- Defining integration approaches (sync vs async)
- Making security model changes
- Decisions that are hard to reverse

### ADR Format (Lightweight)
```markdown
# ADR-[N]: [Title]
**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** [YYYY-MM-DD]

## Context
[Why is this decision needed? What's the situation?]

## Decision
[What was decided?]

## Consequences
[What follows from this decision?]
```

## Risk Assessment Matrix

Use this matrix to categorize risks:

| Probability ↓ / Impact → | Low | Medium | High |
|---------------------------|-----|--------|------|
| **High** | Medium | High | Critical |
| **Medium** | Low | Medium | High |
| **Low** | Low | Low | Medium |

### Risk Categories
- **Technical**: Technology limitations, complexity, performance
- **Timeline**: Schedule impacts, dependencies
- **Integration**: External system dependencies, API changes
- **Security**: Vulnerabilities, compliance requirements
- **Operational**: Deployment, monitoring, maintenance

## Architecture Document Sections

### Required Sections
1. **Overview** - High-level description
2. **Design Decisions** - Key choices with rationale
3. **Component Design** - Responsibilities and interfaces
4. **Risk Assessment** - Identified risks and mitigations

### Optional Sections (as needed)
- Data Flow diagrams
- Integration Points
- Security Considerations
- Performance Requirements
- Migration Strategy

## Quality Checklist

Before finalizing an architecture document:
- [ ] All major decisions documented with options considered
- [ ] Rationale provided for each decision
- [ ] Trade-offs explicitly stated
- [ ] Risks identified with mitigation strategies
- [ ] Aligns with existing codebase patterns (from research)
- [ ] Integration points clearly defined
- [ ] Component responsibilities are clear and non-overlapping
- [ ] Security implications considered
- [ ] Performance requirements addressed

## Output Location
Save architecture documents to: `docs/plans/architecture-{session}.md`
Save ADRs to: `docs/plans/adr-{number}-{title}.md`

## Integration with Workflow

1. **Research phase** provides codebase context and patterns
2. **Questioning phase** provides validated requirements
3. **Architecture planning** creates design documents (this skill)
4. **Task breakdown** converts architecture to executable tasks
5. **Implementation** follows the approved plan
