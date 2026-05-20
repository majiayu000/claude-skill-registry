---
name: aget-handle-incident
description: Handle incidents with diagnosis and mitigation
archetype: operator
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# aget-handle-incident

Handle incidents including triage, diagnosis, mitigation, and resolution tracking. Maintains incident timeline and post-mortem documentation.

## Instructions

When this skill is invoked:

1. **Triage**
   - Assess severity (P1-P4)
   - Identify impact scope
   - Determine urgency

2. **Diagnose**
   - Gather diagnostic information
   - Identify probable causes
   - Document findings

3. **Mitigate**
   - Propose mitigation steps
   - Prioritize by impact
   - Execute with approval

4. **Track**
   - Maintain timeline
   - Document all actions
   - Update status

5. **Resolve & Learn**
   - Confirm resolution
   - Document root cause
   - Create prevention recommendations

## Severity Classification

| Level | Criteria | Response |
|-------|----------|----------|
| P1 | Complete outage, data loss | Immediate |
| P2 | Major feature broken | Within hour |
| P3 | Minor feature degraded | Within day |
| P4 | Cosmetic/minor | Scheduled |

## Output Format

```markdown
## Incident Report: [ID]

### Summary

| Field | Value |
|-------|-------|
| Severity | P[1-4] |
| Status | [Active/Mitigated/Resolved] |
| Impact | [Description] |
| Started | [Timestamp] |
| Resolved | [Timestamp or Ongoing] |

---

### Timeline

| Time | Event | Actor |
|------|-------|-------|
| [HH:MM] | [What happened] | [Who/What] |

---

### Diagnosis

**Probable Cause**: [Description]

**Evidence**:
- [Finding 1]
- [Finding 2]

---

### Mitigation

| Step | Action | Status |
|------|--------|--------|
| 1 | [Action] | [Done/Pending] |
| 2 | [Action] | [Done/Pending] |

---

### Root Cause Analysis (Post-Resolution)

**Root Cause**: [Description]

**Prevention**:
1. [Action to prevent recurrence]
```

## Constraints

- **C1**: NEVER skip severity assessment — severity drives response priority
- **C2**: NEVER apply fixes without user approval — production changes require authorization
- **C3**: NEVER close incident without confirmation — premature closure hides ongoing issues

## Related

- SKILL-027: aget-handle-incident specification
- ONTOLOGY_operator.yaml: Incident, Response, Root_Cause concepts
- CAP-OPS-001: Incident Handling capability
