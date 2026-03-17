---
name: agent-coordination
description: Agent assignment matrix, blocker escalation, and TDM coordination patterns. Use when assigning work to specialists, managing blockers, or coordinating multi-agent workflows.
---

# Agent Coordination Skill

## Purpose

Guide correct agent assignment, blocker escalation, and delivery coordination following the TDM role boundaries.

## When This Skill Applies

Invoke this skill when:

- Assigning work to specialist agents
- Managing blockers across agents
- Coordinating multi-agent workflows
- Escalating issues to ARCHitect/POPM
- Verifying pre-implementation gate
- Updating Linear with evidence

## Stop-the-Line Conditions

### FORBIDDEN Patterns

```text
# FORBIDDEN: Wrong agent assignment
Database work → BE Developer    # WRONG: Use Data Engineer!
Security validation → QAS       # WRONG: Use Security Engineer!
Documentation → BE Developer    # WRONG: Use Tech Writer!

# FORBIDDEN: Skipping pre-implementation gate
Start coding before BSA spec    # Must have acceptance criteria first

# FORBIDDEN: Unresolved blockers >4 hours
Blocker exists but not escalated  # Escalate within 1 hour
```

### CORRECT Patterns

```text
# CORRECT: Right agent for the job
Database work → Data Engineer
Security validation → Security Engineer
Documentation → Tech Writer
Planning/Specs → BSA
Architecture review → System Architect
API implementation → BE Developer
UI implementation → FE Developer
Testing → QAS
PR/Release → RTE

# CORRECT: Pre-implementation gate
1. BSA creates spec with acceptance criteria
2. System Architect reviews patterns
3. THEN specialist executes
```

## Agent Assignment Matrix (MANDATORY)

| Work Type           | Correct Agent     | Never Use           |
| ------------------- | ----------------- | ------------------- |
| Database/Migrations | Data Engineer     | BE Developer        |
| Security/RLS        | Security Engineer | QAS                 |
| Documentation       | Tech Writer       | BE/FE Developer     |
| Specs/Planning      | BSA               | Any implementation  |
| Architecture        | System Architect  | Direct to developer |
| API Routes          | BE Developer      | FE Developer        |
| UI Components       | FE Developer      | BE Developer        |
| Testing/QA          | QAS               | Implementation team |
| PR/Releases         | RTE               | Developers          |

**Reference**: `docs/workflow/TDM_AGENT_ASSIGNMENT_MATRIX.md`

## Blocker Escalation Protocol

### When to Escalate

| Condition              | Escalate To | Deadline    |
| ---------------------- | ----------- | ----------- |
| Blocker > 1 hour       | TDM         | Immediately |
| Blocker > 4 hours      | ARCHitect   | Urgent      |
| Architecture ambiguity | ARCHitect   | Before work |
| Cross-team dependency  | TDM + POPM  | Same day    |
| Security concern       | SecEng      | Immediately |

### Escalation Template

```markdown
**Blocker Escalation**

**Ticket**: {TICKET_PREFIX}-XXX
**Blocked Since**: [timestamp]
**Agent**: [which specialist is blocked]

**Issue**:
[Clear description of what's blocking progress]

**Attempts Made**:

1. [What was tried]
2. [What was tried]

**Request**:
[Specific ask - decision needed, resource needed, etc.]
```

## Pre-Implementation Gate

**MANDATORY** before any implementation work:

```text
1. BSA creates spec with:
   - [ ] Clear acceptance criteria
   - [ ] Pattern references for execution
   - [ ] Success validation command

2. System Architect reviews:
   - [ ] Pattern compliance
   - [ ] RLS requirements (if database)
   - [ ] Security implications

3. THEN implementation can begin
```

## Evidence Attachment

All work must include evidence in Linear:

````markdown
**Implementation Evidence**

**Session ID**: [Claude session ID]
**Agent**: [which specialist]
**Ticket**: {TICKET_PREFIX}-XXX

**Work Completed**:

- [x] Task 1
- [x] Task 2

**Validation**:

```bash
yarn ci:validate
# All checks passed
```
````

**Next Steps**: [if any]

```

## TDM Boundaries

### TDM Does

- ✅ Track delivery progress
- ✅ Update Linear tickets
- ✅ Escalate blockers
- ✅ Attach evidence
- ✅ React to issues

### TDM Does NOT

- ❌ Orchestrate feature work (ARCHitect's job)
- ❌ Run CI/CD validation (specialists' job)
- ❌ Execute technical work (specialists' job)
- ❌ Proactively assign features (ARCHitect's job)

## Authoritative References

- **Agent Assignment Matrix**: `docs/workflow/TDM_AGENT_ASSIGNMENT_MATRIX.md`
- **Agent Workflow SOP v1.3**: `docs/sop/AGENT_WORKFLOW_SOP.md`
- **CONTRIBUTING.md**: Workflow requirements
- **Linear SOP skill**: Evidence attachment templates
```
