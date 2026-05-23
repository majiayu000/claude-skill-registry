---
name: skill-planner
description: Create phased implementation plans from research findings. Invoke when a task needs an implementation plan.
allowed-tools: Read, Write, Edit, Glob, Grep
context:
  - core/formats/plan-format.md
  - core/standards/task-management.md
  - core/workflows/status-transitions.md
---

# Planner Skill

Create structured, phased implementation plans.

## Trigger Conditions

This skill activates when:
- Task status allows planning (not_started, researched)
- /plan command is invoked
- Implementation approach needs to be formalized

## Planning Strategy

### 1. Context Gathering

Collect all relevant information:
- Task description and requirements
- Research reports (if available)
- Related codebase context
- Dependencies and constraints

### 2. Scope Analysis

Determine implementation scope:
- Files to create/modify
- Dependencies to add
- Integration points
- Testing requirements

### 3. Phase Decomposition

Break work into logical phases:
- Each phase: 1-3 hours of work
- Each phase: Independently verifiable
- Each phase: Clear deliverables
- Typically: 2-5 phases total

### 4. Risk Assessment

Identify potential issues:
- Technical risks
- Dependency risks
- Integration risks
- Mitigation strategies

## Execution Flow

```
1. Receive task context
2. Load research reports if available
3. Analyze codebase for integration points
4. Decompose into phases
5. Define steps for each phase
6. Identify risks and mitigations
7. Create plan document
8. Return results
```

## Plan Format

Create plan at `.claude/specs/{N}_{SLUG}/plans/implementation-{NNN}.md`:

```markdown
# Implementation Plan: Task #{N}

**Task**: {title}
**Version**: {NNN}
**Created**: {date}
**Language**: {language}

## Overview

{Summary of approach}

## Phases

### Phase 1: {Name}

**Estimated effort**: {hours}
**Status**: [NOT STARTED]

**Objectives**:
1. {Objective}

**Files to modify**:
- `path/to/file` - {changes}

**Steps**:
1. {Step with detail}
2. {Step with detail}

**Verification**:
- {How to verify completion}

---

### Phase 2: {Name}
{Same structure}

## Dependencies

- {Dependency}

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| {Risk} | {Level} | {Strategy} |

## Success Criteria

- [ ] {Criterion}
```

## Return Format

```json
{
  "status": "completed",
  "summary": "Plan created with N phases",
  "artifacts": [
    {
      "path": ".claude/specs/{N}_{SLUG}/plans/implementation-001.md",
      "type": "plan",
      "description": "Implementation plan"
    }
  ],
  "phases": [
    {"name": "Phase 1", "effort": "2 hours"},
    {"name": "Phase 2", "effort": "1 hour"}
  ],
  "total_effort": "3 hours"
}
```
