---
context: fork
---

# /timeline

Generate a chronological timeline for a project or topic using sub-agents.

## Usage

```
/timeline <project or topic>
/timeline MyDataIntegration
/timeline NewProductLine
/timeline SAP migration
```

## Instructions

### Phase 1: Planning

1. Identify the project/topic
2. Load `.claude/context/projects.md` for context
3. Plan to gather events from:
   - Project file (key dates, milestones)
   - Meetings (by date)
   - ADRs (decision dates)
   - Tasks (created, completed dates)
   - Daily notes (mentions)

### Phase 2: Parallel Gathering (use sub-agents)

Launch sub-agents in parallel using `model: "haiku"` for efficiency:

**Agent 1: Project Milestones** (Haiku)
- Read project file
- Extract: start date, key milestones, status changes
- Return: date, event type, description

**Agent 2: Meeting Timeline** (Haiku)
- Search `+Meetings/` for all meetings linked to project
- Extract: date, meeting title, key outcomes
- Return: chronological list

**Agent 3: Decision Timeline** (Haiku)
- Find ADRs related to project
- Extract: created date, status change dates, decision
- Return: decision events

**Agent 4: Task Timeline** (Haiku)
- Find tasks linked to project
- Extract: created date, due date, completed date
- Return: task lifecycle events

### Phase 3: Compile Timeline

```markdown
# Timeline: {{Project/Topic}}

**Generated**: {{DATE}}
**Span**: {{earliest date}} to {{latest date}} ({{duration}})

## Visual Timeline

```
{{YEAR}}
├── Q1
│   ├── Jan
│   │   └── {{event}}
│   ├── Feb
│   │   └── {{event}}
│   └── Mar
├── Q2
...
```

## Detailed Timeline

### {{YYYY-MM}}

#### {{DATE}} - {{Event Title}}
- **Type**: Meeting / Decision / Milestone / Task
- **Details**: {{description}}
- **Outcome**: {{result if applicable}}
- **Link**: [[{{source note}}]]

### {{YYYY-MM}}
...

## Key Milestones

| Date | Milestone | Status |
|------|-----------|--------|
{{major milestones}}

## Decision Points

| Date | Decision | ADR |
|------|----------|-----|
{{decisions with links}}

## Activity Heatmap

{{show which months had most activity}}

## Gaps

{{identify periods with no documented activity}}

## Upcoming

{{future dated items if any}}
```
