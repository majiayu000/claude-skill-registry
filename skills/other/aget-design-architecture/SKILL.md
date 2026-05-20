---
name: aget-design-architecture
description: Design system architecture with components and patterns
archetype: architect
allowed-tools:
  - Read
  - Glob
  - Grep
---

# aget-design-architecture

Design system architecture including components, relationships, and patterns. Addresses quality attributes and produces architectural artifacts.

## Instructions

When this skill is invoked:

1. **Understand Requirements**
   - Gather functional requirements
   - Identify quality attributes (scalability, reliability, security, etc.)
   - Note constraints (technology, budget, timeline)

2. **Decompose the System**
   - Identify logical components
   - Define responsibilities (single responsibility)
   - Establish boundaries

3. **Select Patterns**
   - Choose appropriate architectural patterns:
     - Layered, Microservices, Event-Driven, etc.
   - Match patterns to requirements and constraints

4. **Define Relationships**
   - Document interfaces between components
   - Specify communication protocols
   - Map dependencies

5. **Address Quality Attributes**
   - Scalability: How system grows
   - Reliability: How system handles failure
   - Security: How system protects assets

## Output Format

```markdown
## Architecture Design: [System Name]

### Overview

[2-3 sentence description of the architecture]

### Components

| Component | Responsibility | Interface |
|-----------|---------------|-----------|
| [Name] | [What it does] | [API/Events/etc.] |

### Architecture Diagram

```
┌─────────────┐     ┌─────────────┐
│ Component A │────▶│ Component B │
└─────────────┘     └─────────────┘
        │
        ▼
┌─────────────┐
│ Component C │
└─────────────┘
```

### Patterns Applied

| Pattern | Rationale |
|---------|-----------|
| [Pattern] | [Why chosen] |

### Quality Attributes

| Attribute | Approach |
|-----------|----------|
| Scalability | [How addressed] |
| Reliability | [How addressed] |
| Security | [How addressed] |

### Dependencies

```
A → B (sync API)
B → C (async events)
```

### Risks & Trade-offs

- [Trade-off 1]: [What was traded for what]
```

## Constraints

- **C1**: NEVER propose architecture without understanding requirements — architecture serves requirements
- **C2**: NEVER introduce unnecessary complexity — simplest solution meeting requirements preferred
- **C3**: NEVER ignore non-functional requirements — quality attributes are architectural drivers

## Related

- SKILL-018: aget-design-architecture specification
- ONTOLOGY_architect.yaml: Architecture, Component, Pattern concepts
- CAP-ARC-001: Architecture Design capability
