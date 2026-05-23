---
name: aget-assess-client
description: Assess client needs, constraints, and objectives
archetype: consultant
allowed-tools:
  - Read
  - Glob
  - Grep
---

# aget-assess-client

Assess client needs, constraints, and objectives to inform engagement scope. Produces structured needs assessment document.

## Instructions

When this skill is invoked:

1. **Gather Client Context**
   - Understand client's current state
   - Identify stated goals and objectives
   - Note organizational constraints

2. **Identify Needs**
   - **Explicit Needs**: What client has stated
   - **Implicit Needs**: What analysis reveals
   - Distinguish needs from wants

3. **Document Constraints**
   - Budget limitations
   - Timeline requirements
   - Technical constraints
   - Organizational constraints

4. **Prioritize**
   - Use impact/urgency matrix
   - Identify quick wins vs. strategic initiatives
   - Note dependencies between needs

5. **Gap Analysis**
   - Current state assessment
   - Desired state definition
   - Gap identification

## Output Format

```markdown
## Client Needs Assessment

### Client Overview

| Attribute | Value |
|-----------|-------|
| Client | [Name/Context] |
| Assessment Date | [Date] |
| Scope | [Area of focus] |

### Identified Needs

#### Explicit Needs (Stated)
1. [Need 1]: [Description]
2. [Need 2]: [Description]

#### Implicit Needs (Discovered)
1. [Need 1]: [How discovered, why important]

### Constraints

| Type | Constraint | Impact |
|------|------------|--------|
| Budget | [Description] | [How it limits options] |
| Timeline | [Description] | [How it limits options] |
| Technical | [Description] | [How it limits options] |

### Priority Matrix

| Need | Impact | Urgency | Priority |
|------|--------|---------|----------|
| [Need 1] | High | High | P1 |
| [Need 2] | High | Low | P2 |

### Gap Analysis

| Area | Current State | Desired State | Gap |
|------|---------------|---------------|-----|
| [Area 1] | [Description] | [Description] | [What's missing] |

### Recommended Focus Areas

1. [Area]: [Why prioritize this]
```

## Constraints

- **C1**: NEVER assume client needs without verification — assumptions lead to scope mismatch
- **C2**: NEVER ignore stated constraints — constraints bound the solution space
- **C3**: NEVER conflate wants with needs — distinguish to improve engagement focus

## Related

- SKILL-020: aget-assess-client specification
- ONTOLOGY_consultant.yaml: Client, Client_Need, Constraint concepts
- CAP-CON-001: Client Assessment capability
