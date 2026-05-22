---
name: technical-specification
description: Creates detailed technical specifications for software projects covering requirements, architecture, APIs, and testing strategies. Use when planning features, documenting system design, or creating architecture decision records.
---

# Technical Specification

Create comprehensive technical specifications for software projects.

## Specification Template

```markdown
# Technical Specification: [Feature Name]

## Metadata
- **Status**: Draft | In Review | Approved
- **Author**: [Name]
- **Reviewers**: [Names]
- **Last Updated**: [Date]

## Executive Summary
[2-3 sentences: What problem does this solve? What's the proposed solution?]

## Background & Context
- Current pain points
- Why now?
- Related work

## Goals
### Primary Goals
1. [Measurable goal]

### Non-Goals
- [What this spec explicitly does NOT cover]

## Functional Requirements
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | [Description] | P0 |
| FR-2 | [Description] | P1 |

## Non-Functional Requirements
- **Performance**: Response time < 200ms
- **Scalability**: Support 10K concurrent users
- **Availability**: 99.9% uptime
- **Security**: [Requirements]

## Technical Design

### Architecture
[Diagram or description]

### API Design
```
POST /api/v1/resource
Request: { "field": "value" }
Response: { "id": "123", "field": "value" }
```

### Database Schema
```sql
CREATE TABLE resources (
  id UUID PRIMARY KEY,
  field VARCHAR(255)
);
```

## Implementation Plan
| Phase | Timeline | Deliverables |
|-------|----------|--------------|
| 1 | Week 1-2 | Core functionality |
| 2 | Week 3 | API endpoints |
| 3 | Week 4 | Testing & docs |

## Testing Strategy
- Unit tests: 80% coverage
- Integration tests: API endpoints
- E2E tests: Critical flows

## Risks & Mitigations
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk] | Medium | High | [Plan] |

## Success Criteria
- [ ] All P0 requirements implemented
- [ ] Tests passing
- [ ] Performance targets met
- [ ] Documentation complete
```

## Full Template

See [references/template.md](references/template.md) for a comprehensive copy-paste template including:
- Complete metadata section
- Success metrics tables
- Architecture diagrams
- Detailed API design sections
- Security threat analysis
- Monitoring & observability
- Risk assessment matrix
- Rollout and rollback plans
- Dependencies tracking
- Open questions section

## Best Practices

**Do:**
- Include measurable acceptance criteria
- Add architecture diagrams
- Define explicit API contracts
- Quantify performance targets
- Document risks and mitigations
- Get stakeholder review before implementation
- Include security considerations
- Define rollback procedures

**Don't:**
- Use vague requirements ("fast", "scalable")
- Skip non-functional requirements
- Ignore security considerations
- Leave alternatives unexplored
- Omit testing strategy
- Forget dependencies and risks
