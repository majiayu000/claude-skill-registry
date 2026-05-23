---
name: aget-execute-task
description: Execute tasks with progress tracking
archetype: worker
allowed-tools:
  - Bash
  - Read
  - Glob
  - Write
  - Edit
---

# aget-execute-task

Execute defined tasks with progress tracking and deliverable production. Follows task definition through to completion.

## Instructions

When this skill is invoked:

1. **Validate Task**
   - Task definition exists
   - Required inputs available
   - Prerequisites met

2. **Plan Execution**
   - Break into steps
   - Identify deliverables
   - Note checkpoints

3. **Execute Steps**
   - Sequential execution
   - Track progress
   - Handle blockers

4. **Produce Deliverables**
   - Create specified outputs
   - Verify quality
   - Document location

5. **Report Completion**
   - Summary of work
   - Deliverables list
   - Any issues

## Output Format

```markdown
## Task Execution: [Task Name]

### Task Info

| Field | Value |
|-------|-------|
| Task | [Name/ID] |
| Started | [Timestamp] |
| Status | [In Progress/Blocked/Complete] |

---

### Progress

| Step | Description | Status |
|------|-------------|--------|
| 1 | [Step 1] | [Done/In Progress/Pending] |
| 2 | [Step 2] | [Done/In Progress/Pending] |
| 3 | [Step 3] | [Done/In Progress/Pending] |

**Progress**: [N]/[Total] steps ([X]%)

---

### Current Activity

[What is being worked on right now]

---

### Deliverables

| Deliverable | Status | Location |
|-------------|--------|----------|
| [D1] | [Pending/Complete] | [Path] |
| [D2] | [Pending/Complete] | [Path] |

---

### Blockers (if any)

1. **[Blocker]**: [Description]
   - Impact: [What's blocked]
   - Needed: [What would unblock]

---

### Completion Summary (when done)

**Completed**: [Timestamp]
**Duration**: [Time]

**Deliverables Produced**:
1. [Deliverable 1]: [Location]

**Notes**: [Any relevant observations]
```

## Constraints

- **C1**: NEVER skip steps without explicit approval — task integrity requires step completion
- **C2**: NEVER claim completion without deliverables — deliverables are proof of completion
- **C3**: NEVER continue past blockers silently — blockers require human decision

## Related

- SKILL-038: aget-execute-task specification
- ONTOLOGY_worker.yaml: Task, Deliverable, Task_Status concepts
- CAP-WRK-001: Task Execution capability
