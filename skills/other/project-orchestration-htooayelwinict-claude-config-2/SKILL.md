---
name: project-orchestration
description: Coordinate multiple agents by routing tasks to appropriate specialists. EXCLUSIVE to project-manager agent.
allowed-tools: Read, Grep, Glob, Edit, Write
---
# Project Orchestration

**Exclusive to:** `project-manager` agent

## Instructions

1. Analyze the user request to identify domain(s) involved
2. Route to appropriate specialist agent(s) using decision tree
3. Use handoff protocol when transitioning between agents
4. Update documentation when changes are complete

## Agent Roster

| Agent | Domain | Triggers |
|-------|--------|----------|
| `planner` | Architecture | "plan", "design" |
| `fullstack-developer` | Implementation | "implement", "build" |
| `database-admin` | Data layer | "migration", "schema" |
| `ui-ux-designer` | Interface | "UI", "component" |
| `researcher` | Research | "research", "compare" |
| `debugger` | Troubleshooting | "bug", "error", "fix" |
| `reviewer` | Quality | "review", "check" |

## Routing Decision Tree

```
Request → Is it a bug/error? → debugger
        → Is it a review? → reviewer
        → Is it UI/UX? → ui-ux-designer
        → Is it database? → database-admin
        → Is it research? → researcher
        → Is it planning? → planner
        → Is it implementation? → fullstack-developer
        → Multi-domain? → project-manager
```

## Handoff Protocol

```markdown
## Handoff: [From] → [To]
- **Completed**: [what was done]
- **Deliverables**: [files]
- **Next**: [what to do]
```

## Task Breakdown Template

```markdown
| # | Task | Agent | Dependencies |
|---|------|-------|--------------|
| 1 | Design | planner | none |
| 2 | Migration | database-admin | #1 |
| 3 | Implement | fullstack-developer | #2 |
```

## Documentation Sync

| Change Type | Update |
|-------------|--------|
| New feature | `docs/codebase-summary.md` |
| New model | `docs/codebase-summary.md` |
| Pattern change | `docs/code-standards.md` |

## Examples
- "Coordinate UI + API + migration work"
- "Break down this feature across agents"
