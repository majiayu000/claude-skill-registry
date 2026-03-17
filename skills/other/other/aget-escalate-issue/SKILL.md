---
name: aget-escalate-issue
description: Escalate issues to higher authority
archetype: supervisor
allowed-tools:
  - Read
  - Glob
  - Write
---

# aget-escalate-issue

Escalate issues to higher authority when they exceed current scope. Creates structured escalation documentation.

## Instructions

When this skill is invoked:

1. **Verify Escalation Needed**
   - Confirm issue exceeds current authority
   - Document why local resolution not possible
   - Check if similar escalation exists

2. **Document Context**
   - Issue description
   - Impact assessment
   - Prior attempts

3. **Identify Target**
   - Appropriate escalation path
   - Decision authority needed
   - Contact method

4. **Create Escalation**
   - Structured escalation document
   - Urgency classification
   - Tracking mechanism

## Escalation Criteria

| Should Escalate | Should NOT Escalate |
|-----------------|---------------------|
| Exceeds authority | Within authority |
| Cross-portfolio | Single portfolio |
| Policy change | Operational |
| Resource conflict | Local resource |
| Security/compliance | Routine issue |

## Output Format

```markdown
## Escalation Request

### Issue Summary

| Field | Value |
|-------|-------|
| ID | ESC-[YYYY]-[NNN] |
| From | [Escalating Agent] |
| To | [Target Authority] |
| Date | [YYYY-MM-DD] |
| Urgency | [Low/Medium/High/Critical] |

---

### Issue Description

**Title**: [Brief title]

**Description**: [Full description of the issue]

**Impact**: [Who/what is affected, severity]

---

### Why Escalation Required

**Authority Check**:
- [ ] Issue exceeds my decision authority
- [ ] Requires cross-portfolio coordination
- [ ] Policy/governance decision needed
- [ ] Resource beyond my allocation

**Prior Attempts**:
1. [Attempt 1]: [Result]
2. [Attempt 2]: [Result]

---

### Request

**Decision Needed**: [Specific decision or action requested]

**Options** (if applicable):
1. [Option A]: [Pros/Cons]
2. [Option B]: [Pros/Cons]

**Recommendation**: [If you have one]

---

### Urgency Justification

**Urgency**: [Level]

**Why**: [Justification for urgency level]

**Deadline** (if any): [Date/Time]

---

### Tracking

**Escalation ID**: ESC-[YYYY]-[NNN]
**Status**: Open
**Created**: [Timestamp]
```

## Constraints

- **C1**: NEVER escalate issues within current authority — unnecessary escalation wastes resources
- **C2**: NEVER escalate without documenting prior attempts — escalation requires proof of local effort
- **C3**: NEVER set urgency inappropriately high — urgency inflation reduces effectiveness

## Related

- SKILL-037: aget-escalate-issue specification
- ONTOLOGY_supervisor.yaml: Escalation, Intervention, Authority concepts
- CAP-SUP-003: Issue Escalation capability
