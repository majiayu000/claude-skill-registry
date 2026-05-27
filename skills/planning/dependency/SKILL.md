---
name: dependency
description: Map and visualize feature dependencies. Use when analyzing dependencies, identifying blockers, or creating dependency graphs. Triggers on keywords like "dependencies", "blockers", "what blocks", "dependency map".
infer: true
allowed-tools: Read, Write, Edit, Grep, Glob, TodoWrite
---

# Dependency Mapping

Map and visualize dependencies between features and work items.

## When to Use
- Planning feature sequencing
- Identifying blockers
- Understanding critical path

## Pre-Workflow

### Activate Skills

- Activate `project-manager` skill for dependency analysis best practices

## Quick Reference

### Workflow
1. Read target PBI/feature or all items from `team-artifacts/pbis/`
2. Extract dependency fields
3. Build dependency graph
4. Identify risks (circular dependencies, unresolved blockers, external dependencies)
5. Identify critical path
6. Generate visualization report
7. Output to console or save to file

### Dependency Types
| Type       | Symbol | Description                         |
| ---------- | ------ | ----------------------------------- |
| Blocked by | `->`   | Cannot start until X completes      |
| Blocks     | `<-`   | X cannot start until this completes |
| Mutual     | `<->`  | Bidirectional dependency            |
| Related to | `=>`   | Shares code/design elements         |
| Depends on | `~>`   | Needs external (API, service)       |

### Graph Notation
```
Feature A -> Feature B (blocked by)
Feature A <- Feature C (blocks)
Feature A <-> Feature D (mutual)
```

## Visualization Template

```markdown
## Dependency Map

### {Feature}

**Upstream (We depend on):**
- [ ] {Dep 1} - {status}
- [ ] {Dep 2} - {status}

**Downstream (Depends on us):**
- [ ] {Dep 1} - {their deadline}

### Critical Path
{A} -> {B} -> {C} -> {D}

### Risk Areas
- Red: {Feature X} blocking 3 items
- Yellow: {External API} - timeline uncertain
```

### Output Format
```
A -> B -> C (critical path)
     \-> D

Legend:
-> blocks
=> related
```

### Related
- **Role Skill:** `project-manager`
- **Command:** `/dependency`

## Example

```bash
/dependency team-artifacts/pbis/260119-pbi-dark-mode-toggle.md
/dependency all
```

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
