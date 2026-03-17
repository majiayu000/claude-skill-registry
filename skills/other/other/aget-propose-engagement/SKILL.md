---
name: aget-propose-engagement
description: Create engagement proposals with scope and deliverables
archetype: consultant
allowed-tools:
  - Read
  - Glob
  - Write
---

# aget-propose-engagement

Create engagement proposals outlining scope, approach, and deliverables. Produces structured proposal document with clear boundaries.

## Instructions

When this skill is invoked:

1. **Verify Prerequisites**
   - Client needs assessment completed
   - Constraints understood
   - Objectives clear

2. **Define Scope**
   - In-scope items (explicit)
   - Out-of-scope items (explicit)
   - Scope boundaries

3. **Design Approach**
   - Methodology selection
   - Phase breakdown
   - Key activities per phase

4. **Specify Deliverables**
   - Concrete deliverable list
   - Acceptance criteria per deliverable
   - Delivery timeline

5. **Document Assumptions**
   - Client-side requirements
   - Dependencies
   - Risk factors

## Output Format

```markdown
# Engagement Proposal: [Title]

**Date**: [YYYY-MM-DD]
**Client**: [Client Name]
**Prepared By**: [Agent Name]

---

## Executive Summary

[2-3 sentences describing the engagement value proposition]

---

## Scope

### In Scope
- [Item 1]: [Description]
- [Item 2]: [Description]

### Out of Scope
- [Item 1]: [Why excluded]
- [Item 2]: [Why excluded]

---

## Approach

### Methodology
[Description of approach/methodology]

### Phases

| Phase | Activities | Duration |
|-------|------------|----------|
| 1. [Name] | [Key activities] | [Timeframe] |
| 2. [Name] | [Key activities] | [Timeframe] |

---

## Deliverables

| Deliverable | Description | Acceptance Criteria |
|-------------|-------------|---------------------|
| [D1] | [What it is] | [How to verify complete] |
| [D2] | [What it is] | [How to verify complete] |

---

## Assumptions & Dependencies

### Assumptions
1. [Assumption 1]
2. [Assumption 2]

### Dependencies
- [Dependency 1]: [What we need from client]

---

## Success Criteria

1. [Measurable criterion 1]
2. [Measurable criterion 2]

---

## Next Steps

1. [Action 1]
2. [Action 2]
```

## Constraints

- **C1**: NEVER propose without prior needs assessment — proposals must be grounded in client needs
- **C2**: NEVER leave scope ambiguous — clear scope prevents scope creep
- **C3**: NEVER define deliverables without acceptance criteria — criteria enable completion verification

## Related

- SKILL-021: aget-propose-engagement specification
- ONTOLOGY_consultant.yaml: Engagement, Proposal, Deliverable concepts
- CAP-CON-002: Engagement Proposal capability
