---
name: aget-report-progress
description: Report progress on current work
archetype: worker
allowed-tools:
  - Read
  - Glob
---

# aget-report-progress

Report progress on current work including completion percentage, blockers, and remaining items. Supports handoff documentation.

## Instructions

When this skill is invoked:

1. **Assess Current State**
   - What's complete
   - What's in progress
   - What's remaining

2. **Calculate Progress**
   - Completion percentage
   - Velocity (if applicable)
   - Estimated remaining

3. **Identify Issues**
   - Current blockers
   - Risks to completion
   - Dependencies

4. **Prepare Handoff** (if needed)
   - Context for continuation
   - State of work
   - Next steps

## Output Format

```markdown
## Progress Report

### Overview

| Field | Value |
|-------|-------|
| Work | [Task/Project Name] |
| Reporter | [Agent] |
| As Of | [Timestamp] |
| Status | [On Track/At Risk/Blocked] |

---

### Progress

**Completion**: [X]%

```
[███████████░░░░░░░░░] 55%
```

---

### Completed

1. [x] [Completed item 1]
2. [x] [Completed item 2]
3. [x] [Completed item 3]

---

### In Progress

1. [ ] [Current item]: [Status details]

---

### Remaining

1. [ ] [Remaining item 1]
2. [ ] [Remaining item 2]

---

### Blockers

| Blocker | Impact | Resolution Path |
|---------|--------|-----------------|
| [Blocker 1] | [Impact] | [How to resolve] |

---

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Action] |

---

### Handoff (if session ending)

**Context**: [What needs to be known to continue]

**Current State**: [Where things stand]

**Next Steps**:
1. [What should happen next]
2. [Follow-up action]

**Files Modified**:
- [file1]: [What changed]
- [file2]: [What changed]
```

## Constraints

- **C1**: NEVER overstate completion percentage — accurate progress essential for planning
- **C2**: NEVER hide blockers — blockers need attention
- **C3**: NEVER omit risks to protect optimistic view — honest risk reporting enables intervention

## Related

- SKILL-039: aget-report-progress specification
- ONTOLOGY_worker.yaml: Progress, Task_Status, Handoff concepts
- CAP-WRK-002: Progress Reporting capability
