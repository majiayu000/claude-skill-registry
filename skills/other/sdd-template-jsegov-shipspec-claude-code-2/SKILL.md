---
name: sdd-template
description: This skill should be used when the user asks to "create a design document", "write technical specs", "document architecture", "generate SDD", "design the system", "API design", or when creating technical design documents from approved PRDs.
version: 0.1.0
---

# Software Design Document Template

Create comprehensive technical design documents following the Atlassian 8-section structure.

## Document Structure Overview

| Section | Purpose |
|---------|---------|
| 1. Introduction | Purpose, scope, definitions |
| 2. System Overview | High-level architecture |
| 3. Design Considerations | Assumptions, constraints, risks |
| 4. Architectural Strategies | Key decisions and alternatives |
| 5. System Architecture | Components, data flow, APIs, models |
| 6. Policies and Tactics | Security, error handling, logging |
| 7. Detailed Design | Component-level specifications |
| 8. Appendix | Diagrams, glossary |

## Section Templates

### Section 1: Introduction

```markdown
## 1. Introduction

### 1.1 Purpose
[What this document covers and its intended audience]

### 1.2 Scope
[System boundaries - what's included and excluded]

### 1.3 Definitions and Acronyms
| Term | Definition |
|------|------------|
| [Term] | [Definition] |

### 1.4 References
- PRD: [link to PRD document]
- [Other relevant documents]
```

### Section 2: System Overview

```markdown
## 2. System Overview

### 2.1 System Context
[How this system fits into the broader architecture]

### 2.2 High-Level Architecture
[Architecture diagram description or ASCII diagram]

### 2.3 Key Components
- **Component A**: [Purpose and responsibility]
- **Component B**: [Purpose and responsibility]
```

### Section 3: Design Considerations

```markdown
## 3. Design Considerations

### 3.1 Assumptions
- [Assumption 1]
- [Assumption 2]

### 3.2 Constraints
- [Technical constraint]
- [Business constraint]

### 3.3 Dependencies
- [External system X]
- [Library Y version Z]

### 3.4 Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | High/Med/Low | [Strategy] |
```

### Section 4: Architectural Strategies

```markdown
## 4. Architectural Strategies

### 4.1 Strategy Selection
[Why this architecture was chosen over alternatives]

### 4.2 Alternatives Considered
| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| [Option A] | [Pros] | [Cons] | Selected |
| [Option B] | [Pros] | [Cons] | Rejected |

### 4.3 Key Architectural Decisions
- **Decision 1**: [Decision and rationale]
- **Decision 2**: [Decision and rationale]
```

### Section 5: System Architecture

```markdown
## 5. System Architecture

### 5.1 Component Diagram
[Description or ASCII representation]

### 5.2 Data Flow
[How data moves through the system]

### 5.3 API Design

#### 5.3.1 Endpoints
| Method | Path | Description |
|--------|------|-------------|
| POST | /api/resource | Create resource |
| GET | /api/resource/:id | Get resource |

#### 5.3.2 Request/Response Schemas
[TypeScript interfaces or JSON schemas]

### 5.4 Data Models
[Database schema with types and constraints]
```

### Section 6: Policies and Tactics

```markdown
## 6. Policies and Tactics

### 6.1 Security
- Authentication: [Strategy]
- Authorization: [Strategy]
- Data encryption: [At rest / in transit]

### 6.2 Error Handling
- [Error handling strategy]
- [Retry policies]

### 6.3 Logging and Monitoring
- [What to log]
- [Alerting thresholds]

### 6.4 Performance
- [Caching strategy]
- [Connection pooling]
```

### Section 7: Detailed Design

```markdown
## 7. Detailed Design

### 7.1 [Component A] Design

#### 7.1.1 Responsibilities
- [Responsibility 1]
- [Responsibility 2]

#### 7.1.2 Interface
[TypeScript interface or function signatures]

#### 7.1.3 Implementation Notes
[Specific implementation details, algorithms, or patterns]
```

### Section 8: Appendix

```markdown
## 8. Appendix

### 8.1 Sequence Diagrams
[For complex flows]

### 8.2 State Diagrams
[For stateful components]

### 8.3 Glossary
[Extended definitions]
```

## Requirement Traceability

Each design decision should trace to requirements:

```markdown
### REQ-001 Implementation
**Requirement:** [Quote requirement]
**Design:** [How this design satisfies it]
**Verification:** [How to test it]
```

## Quality Checklist

Before finalizing an SDD:

- [ ] Every PRD requirement (REQ-XXX) is addressed
- [ ] Data models are complete with types and constraints
- [ ] API contracts are fully specified
- [ ] Error scenarios are documented
- [ ] Security considerations are addressed
- [ ] Performance requirements have corresponding strategies
- [ ] Dependencies are versioned
- [ ] Diagrams are included where helpful

## Additional Resources

For detailed section guidance and examples, see `references/sections.md`.
