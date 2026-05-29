---
name: project-status
description: "Enhanced project status dashboard with intelligent context analysis. Use for session start context, weekly reviews, or seeing what needs attention."
model: claude-haiku-4-5-20251001
allowed-tools: Read, Glob, Grep, Task
---

# /project-status

Dashboard showing status of all ideas, specs, and issues across the repository.

## Usage

```bash
/project-status                       # Overview of all projects
/project-status --project coordinatr  # Focus on one project
/project-status --detailed            # Comprehensive analysis
```

## Output Structure

```
# Ideas Repository Status

## Active Projects

### Coordinatr
Status: Active planning
Specs: 2 (1 complete, 1 in progress)
Issues: 3 (1 in_progress, 2 pending)
Active: 001-auth-research (TASK, in_progress)

### YourBench
Status: MVP in progress (60%)
Specs: 1 (complete)
Issues: 0

## Needs Attention
- Coordinatr TASK-002 blocked (waiting on TASK-001)
- IRL Social research 75% complete

## Quick Stats
- 13 ideas total
- 4 specs across all projects
- 5 active issues

## Suggested Next Actions
1. Complete Coordinatr TASK-001
2. Create plan for YourBench auth
```

## Execution Steps

### 1. Scan Repository Structure

```bash
ls ideas/
# For each: README.md, specs/, issues/, docs/
```

### 2. Parse Project Status

For each idea folder:
1. Read README.md for status
2. Count specs: `ideas/{project}/specs/SPEC-*.md`
3. Analyze issues: status, PLAN.md progress, WORKLOG activity

### 3. Parse Dependencies

Read `depends_on` from issue frontmatter:
```yaml
depends_on: [001, 002]
```

Auto-block detection: If depends on incomplete issues, flag as blocked.

### 4. Check Branch Status

For in_progress issues:
```bash
cd spaces/[project]
git branch -a | grep "feature/###"
git log origin/branch..branch  # Unpushed commits
```

### 5. Identify Attention Items

- Issues with status: blocked
- Issues blocked by dependencies
- Stale issues (no activity 14+ days)
- Incomplete spikes past time box
- Branches with unpushed commits

### 6. Generate Recommendations

- Next logical step for active work
- Items to unblock
- Stale items to review

## Status Taxonomy

### Project Status
- Initial brainstorming
- Active brainstorming
- Active planning
- Concept phase
- Pre-MVP
- MVP in progress (X%)
- Portfolio-first
- Shelved
- Graduated

### Issue Status
- `open` - Not started
- `in_progress` - Currently working
- `blocked` - Waiting
- `complete` - Done

## When to Use

- Session start (get context)
- Before planning (see what's active)
- Weekly review (find stale items)
- After completing work (see what's next)
