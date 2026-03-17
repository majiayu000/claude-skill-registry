---
name: project-report
context: fork
description: Generate project status reports (single or all projects)
model: opus
---

# /project-report

Generate project status reports — either a detailed single-project report or an overview of all active projects.

## Usage

```
/project-report <project name>   # Detailed single-project report
/project-report                  # Overview of all active projects
/project-report all              # All projects including paused/completed
```

## Examples

```
/project-report Alpha
/project-report Delta
/project-report all
```

---

## Mode 1: Single Project Report

When a project name is provided.

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
- Search in `Meetings/` for `Meeting - *.md` files where project field matches
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
- **Health**: Green/Amber/Red based on activity
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

## Compliance & Security

- **DPIA Status**: {{status and OneTrust ID if applicable}}
- **Cyber Approval**: {{status}}
- **Other Compliance**: {{any other requirements}}

## Risks & Blockers

{{identify from meeting notes or task blockers}}

## Next Steps

{{based on action items and upcoming meetings}}
```

Output the report (don't save unless asked).

---

## Mode 2: All Projects Overview

When no project name is provided, or `all` is specified.

### Instructions

1. **Find all project files** using Glob: `Project*.md`

2. **Read each project file** to extract:
   - Project title and status
   - Related ADRs and tasks
   - Recent meetings
   - Key stakeholders
   - Current blockers/risks
   - DPIA status (if applicable)
   - Last modified date

3. **Filter by status** (unless `all` specified):
   - Active projects (status: active, in progress, or null)
   - Exclude paused and completed unless `all` flag used

4. **For each project, assess:**
   - Health status: Green (on track), Amber (at risk), Red (blocked)
   - Recent activity (meetings/tasks in last 7 days)
   - Pending actions and priorities
   - Compliance status (DPIA, Cyber, etc.)

5. **Generate formatted overview:**

```markdown
# Engineering Projects Snapshot

**Generated**: {{DATE}}
**Scope**: Active projects / All projects

## Executive Summary

- **Total Active Projects**: {{count}}
- **On Track**: {{count}}
- **At Risk**: {{count}}
- **Blocked**: {{count}}
- **Paused**: {{count}}
- **Completed This Month**: {{count}}

## Projects by Status

### On Track ({{count}} projects)

#### [[Project - Example A]]
- **Status**: Active
- **Health**: Green
- **Recent Progress**:
  - Completed items and recent meetings
- **Next Actions**: Upcoming milestones
- **Owner**: [[Person]]
- **Compliance**: DPIA/Cyber status
- **Timeline**: {{timeframe}}

#### [[Project - Example B]]
- (same structure)

### At Risk ({{count}} projects)

#### [[Project - Example C]]
- **Health**: Amber - reason for risk
- **Blockers**: What is causing risk
- **Next Actions**: Steps to resolve

### Blocked ({{count}} projects)

#### [[Project - Example D]]
- **Health**: Red
- **Blocker**: Description
- **Escalation**: Required by {{date}}

### Paused ({{count}} projects)
(Only shown if `all` flag used)

### Recently Completed ({{count}} projects)
(Only shown if `all` flag used or completed in last 30 days)

## Key Milestones This Week

| Project | Milestone | Due Date | Status |
|---------|-----------|----------|--------|
{{milestone rows}}

## Immediate Attention Required

### High Priority Actions (Next 24-48 Hours)
{{numbered list of urgent items with owner and due date}}

### Medium Priority Actions (This Week)
{{numbered list}}

## Compliance Overview

| Project | DPIA Status | Cyber Status | Other Compliance |
|---------|-------------|--------------|------------------|
{{compliance rows}}

## Projects Summary Table

| Project | Status | Health | Owner | Recent Activity | Next Milestone |
|---------|--------|--------|-------|-----------------|----------------|
{{summary rows}}

## Risks & Concerns

### Critical Risks
{{numbered list}}

### Medium Risks
{{numbered list}}

## Recommended Actions

**For Leadership:**
{{numbered list}}

**For Project Teams:**
{{numbered list}}

**For Architecture:**
{{numbered list}}
```

6. **Output the snapshot** as formatted markdown

7. **Provide actionable insights:**
   - Flag urgent items requiring immediate attention
   - Identify patterns across projects (e.g., multiple DPIA delays)
   - Highlight resource constraints or bottlenecks
   - Recommend prioritisation

8. **Optionally save snapshot** by asking user:
   - "Would you like me to save this project snapshot as a note?"

---

## Notes

- Use UK English spelling throughout
- Use health indicators (Green/Amber/Red) for quick visual status
- Flag projects with no recent activity (>14 days)
- Cross-reference with DPIA status and ADR reports
- Calculate "days since last activity" for each project
- Prioritise actionable information over historical data
- Output the report directly (don't save unless asked)
