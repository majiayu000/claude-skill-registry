---
name: projects-quick
description: Quick overview of all projects (lightweight, Haiku-powered). Use to check project statuses, see what's active, or get a summary of all work. Triggers on "project status", "show projects", "what projects", "project overview".
model: claude-haiku-4-5-20251001
allowed-tools: Read, Glob
---

Show status of all projects from the ideas/ repo.

## Data Sources

1. Read `ideas/CLAUDE.md` for project index
2. For each active project, read `ideas/ideas/[project]/README.md`

## Output Format

### Active Projects

| Project | Phase | Last Activity | Next Step |
|---------|-------|---------------|-----------|
| CareerBrain | MVP | [date] | [from README] |
| ... | ... | ... | ... |

### On Hold

| Project | Reason | Resume When |
|---------|--------|-------------|
| YourBench | Job search priority | After job secured |
| ... | ... | ... |

### Quick Stats
- Total active: X
- Total on hold: Y
- Open issues: Z (scan issues/ directories)

## Optional Deep Dive

If Taylor asks about a specific project:
1. Read its `project-brief.md`
2. List open issues from `issues/`
3. Show recent WORKLOG entries
4. Suggest next steps

Keep the overview scannable - details on request.
