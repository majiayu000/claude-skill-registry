---
context: fork
---

# /project-status

Generate a comprehensive status report for a project using sub-agents for efficiency.

## Usage

```
/project-status <project name>
/project-status MyDataIntegration
/project-status NewProductLine
```

## Instructions

### Phase 1: Planning

1. Identify the project by searching for matching `Project - *.md` file
2. Load `.claude/context/projects.md` for project context
3. Create a plan to gather:
   - Project metadata and status
   - Recent meetings (last 30 days)
   - Open tasks
   - Recent ADRs
   - Key people involved

### Phase 2: Parallel Data Gathering (use sub-agents)

Launch these sub-agents in parallel using `model: "haiku"` for efficiency:

**Agent 1: Project Details** (Haiku)
- Read the project file
- Extract status, priority, timeframe, description

**Agent 2: Recent Meetings** (Haiku)
- Search in `+Meetings/` for `Meeting - *.md` files where project field matches
- Get last 10 meetings, extract summaries and decisions

**Agent 3: Tasks** (Haiku)
- Find tasks linked to this project
- Separate into: completed (last 30 days), open, blocked

**Agent 4: ADRs & Decisions** (Haiku)
- Find ADRs mentioning this project
- Extract key architectural decisions

### Phase 3: Compile Report

Generate status report:

```markdown
# Project Status: {{Project Name}}

**Generated**: {{DATE}}
**Status**: {{status}}
**Priority**: {{priority}}

## Executive Summary

{{2-3 sentence overview based on recent activity}}

## Current State

- **Timeline**: {{timeframe}}
- **Health**: {{Green/Amber/Red based on activity}}
- **Last Activity**: {{date of most recent meeting/update}}

## Recent Progress (Last 30 Days)

### Meetings Held
| Date | Meeting | Key Outcomes |
|------|---------|--------------|
{{meeting table}}

### Decisions Made
{{list of decisions from meetings and ADRs}}

### Tasks Completed
- {{completed tasks}}

## Outstanding Items

### Open Tasks
| Task | Priority | Due | Assignee |
|------|----------|-----|----------|
{{open tasks table}}

### Pending Decisions
{{any proposed ADRs or open questions}}

## Key Stakeholders

{{people involved based on meetings}}

## Risks & Blockers

{{identify from meeting notes or task blockers}}

## Next Steps

{{based on action items and upcoming meetings}}
```

4. Output the report (don't save unless asked)
