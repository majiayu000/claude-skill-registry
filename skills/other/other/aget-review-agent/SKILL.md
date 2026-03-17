---
name: aget-review-agent
description: Review agent health and conformance
archetype: supervisor
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# aget-review-agent

Review a specific agent's health, conformance, and recent activity. Produces assessment with recommendations.

## Instructions

When this skill is invoked:

1. **Verify Agent Exists**
   - Check fleet registry
   - Confirm in supervisor's scope
   - Note portfolio

2. **Assess Health**
   - Version currency
   - Configuration validity
   - Dependency status

3. **Check Conformance**
   - Conformance level (L0-L5)
   - Gap identification
   - Compliance issues

4. **Review Activity**
   - Recent sessions
   - Commits/changes
   - Issues/blockers

5. **Generate Recommendations**
   - Priority improvements
   - Upgrade guidance
   - Risk flags

## Output Format

```markdown
## Agent Review: [Agent Name]

### Overview

| Field | Value |
|-------|-------|
| Agent | [Name] |
| Portfolio | [Portfolio] |
| Archetype | [Type] |
| Version | [vX.Y.Z] |
| Review Date | [YYYY-MM-DD] |

---

### Health Assessment

| Check | Status | Notes |
|-------|--------|-------|
| Version Current | [Yes/No] | [Current: X, Latest: Y] |
| Config Valid | [Yes/No] | [Issue if any] |
| Dependencies | [OK/Issues] | [Details] |

**Health Score**: [Good/Fair/Poor]

---

### Conformance

| Level | Status | Gaps |
|-------|--------|------|
| L0 (Exists) | [Pass] | — |
| L1 (Structure) | [Pass/Fail] | [Gap] |
| L2 (Identity) | [Pass/Fail] | [Gap] |
| L3 (Session) | [Pass/Fail] | [Gap] |
| L4 (Evolution) | [Pass/Fail] | [Gap] |
| L5 (Governance) | [Pass/Fail] | [Gap] |

**Conformance Level**: L[N]

---

### Recent Activity

| Period | Sessions | Commits | Issues |
|--------|----------|---------|--------|
| Last 7 days | [N] | [N] | [N] |
| Last 30 days | [N] | [N] | [N] |

---

### Blockers

1. [Blocker description]

---

### Recommendations

| Priority | Recommendation | Effort |
|----------|----------------|--------|
| P1 | [High priority action] | [Low/Med/High] |
| P2 | [Medium priority action] | [Low/Med/High] |
```

## Constraints

- **C1**: NEVER review agents outside supervisor's fleet — scope boundary enforcement
- **C2**: NEVER modify agent during review — review is read-only
- **C3**: NEVER expose sensitive agent configurations — security boundary respected

## Related

- SKILL-036: aget-review-agent specification
- ONTOLOGY_supervisor.yaml: Agent_Registry, Agent_Status, Fleet_Audit concepts
- CAP-SUP-002: Agent Review capability
