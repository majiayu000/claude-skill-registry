---
name: aget-run-playbook
description: Execute runbooks for operational scenarios
archetype: operator
allowed-tools:
  - Bash
  - Read
  - Glob
---

# aget-run-playbook

Execute runbooks for deployment, rollback, and operational scenarios. Provides step-by-step execution with verification checkpoints.

## Instructions

When this skill is invoked:

1. **Validate Playbook**
   - Verify playbook exists
   - Parse steps and parameters
   - Check prerequisites

2. **Confirm Execution**
   - Display playbook summary
   - Get user confirmation
   - Note parameters

3. **Execute Steps**
   - Run sequentially
   - Verify each step
   - Log all actions

4. **Handle Failures**
   - Stop on failure
   - Offer rollback options
   - Document state

5. **Complete**
   - Verify final state
   - Generate execution log
   - Report outcome

## Output Format

```markdown
## Playbook Execution: [Name]

### Configuration

| Parameter | Value |
|-----------|-------|
| Playbook | [Path/Name] |
| Started | [Timestamp] |
| Parameters | [List] |

---

### Execution Log

| Step | Action | Status | Duration |
|------|--------|--------|----------|
| 1 | [Description] | [Pass/Fail] | [Xs] |
| 2 | [Description] | [Pass/Fail] | [Xs] |

---

### Current Status

**Status**: [Running/Complete/Failed]

**Progress**: [N]/[Total] steps

---

### Output

```
[Command output for current/last step]
```

---

### Rollback Options (if failed)

1. [Rollback step 1]
2. [Rollback step 2]
```

## Playbook Format

```yaml
# playbooks/deploy.yaml
name: Deploy Application
steps:
  - name: Backup current version
    command: ./scripts/backup.sh
    verify: test -f backups/latest.tar.gz
  - name: Deploy new version
    command: ./scripts/deploy.sh
    verify: curl -s localhost:8080/health
rollback:
  - ./scripts/restore.sh
```

## Constraints

- **C1**: NEVER execute playbooks without user confirmation — operational actions require authorization
- **C2**: NEVER skip verification steps — verification ensures state correctness
- **C3**: NEVER proceed after failure without explicit override — failures may indicate unsafe state

## Related

- SKILL-028: aget-run-playbook specification
- ONTOLOGY_operator.yaml: Runbook, Deployment, Rollback concepts
- CAP-OPS-002: Playbook Execution capability
