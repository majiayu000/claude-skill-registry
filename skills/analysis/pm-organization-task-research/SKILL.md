---
name: pm-organization-task-research
description: Codebase research specialist for PM task assignment. Use proactively before assigning tasks to understand existing patterns, dependencies, and implementation approaches.
user-invocable: true
category: organization
---

# PM Task Research

> "Research before assignment - prevent misallocation and blockers."

Explore the codebase and return structured summaries for task assignment. This helps ensure tasks are assigned to the right agent with accurate complexity estimates.

## When to Use

Use proactively before assigning tasks to understand:
- Existing patterns in the codebase
- Files/components the task will touch
- Potential blockers or dependencies
- Which agent should handle the task
- Complexity estimate

## Research Process

1. Use `Grep` to find related implementations
2. Use `Read` to examine relevant files
3. Use `Glob` to find related components
4. Provide a **structured summary** (not raw exploration)

## What to Research

### For Each Task

1. **Existing Patterns:** What similar implementations exist?
2. **Dependencies:** What files/components will this task touch?
3. **Blockers:** Are there any blocking issues or missing dependencies?
4. **Agent Fit:** Should this go to Developer or Tech Artist?
5. **Complexity Estimate:** Micro/Simple/Medium/Complex based on codebase state

### Agent Selection Guide

| Category | Default Agent | When to Reassign |
|----------|---------------|-----------------|
| `architectural` | developer | If visual-heavy → techartist |
| `functional` | developer | If shader/VFX work → techartist |
| `integration` | developer | - |
| `visual` | techartist | If logic-heavy → developer |
| `shader` | techartist | - |
| `polish` | techartist | If functional changes → developer |

### Complexity Estimation

| Level | Criteria | Example |
|-------|----------|---------|
| **Micro** | Single line change, config update | Fix typo, change color value |
| **Simple** | Single file, well-defined pattern | Add utility function, simple component |
| **Medium** | 2-5 files, some coordination | Add feature to existing system |
| **Complex** | 5+ files, new patterns, architecture | New system, refactoring, multiplayer |

## Output Format

```markdown
## Task Research: {TASK_ID}

### Task Summary
- **Title:** {task title}
- **Category:** {architectural|functional|visual|shader|polish|integration}
- **Description:** {brief description}

### Existing Patterns
- Pattern 1: {location} - {brief description}
- Pattern 2: {location} - {brief description}

### Dependencies
- {file/path} - {reason for dependency}
- {file/path} - {reason for dependency}

### Files That Will Be Modified
- {file/path} - {what needs to change}
- {file/path} - {what needs to change}

### Blockers
- (if none, state "No blockers identified")
- (if blockers exist, list them with severity)

### Recommended Agent
- {developer|techartist} - {justification}

### Complexity Estimate
- {Micro|Simple|Medium|Complex} - {justification}

### Implementation Notes
- Any relevant notes for the implementing agent
- Potential gotchas or areas requiring extra care
```

## Important

- Keep analysis concise and actionable
- Don't return verbose file contents
- Focus on what the PM needs to know for assignment
- If you find critical issues, flag them prominently
- Always identify which agent should handle the task
- Be realistic about complexity estimates

## See Also

- [pm-organization-task-selection](../pm-organization-task-selection/SKILL.md) — Priority algorithm for selecting tasks
- [dev-research-codebase-exploration](../dev-research-codebase-exploration/SKILL.md) — Developer codebase exploration patterns
- [dev-research-pattern-finding](../dev-research-pattern-finding/SKILL.md) — Pattern finding for implementations
