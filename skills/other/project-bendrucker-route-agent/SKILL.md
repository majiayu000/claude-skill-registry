---
name: project
description: |
  Manage route-agent project: check status, find next tasks, spawn parallel work. Use when starting work, checking progress, or asking "what's next?"
allowed-tools:
  - Bash(gh:*)
  - Bash(git:*)
  - mcp__github
  - Task
---

# Project Management

Assess project status, find ready tasks, and orchestrate parallel work.

## Commands

| Command | Action |
|---------|--------|
| `/project` | Show milestone progress and ready tasks |
| `/project next` | Recommend single next task |
| `/project work` | Spawn sub-agents for ready tasks (parallel) |
| `/project work #N` | Work on specific issue |
| `/project cleanup` | Remove worktrees for merged PRs |

## Quick Start

```bash
# Milestone progress
gh api repos/bendrucker/route-agent/milestones --jq '.[] | "\(.title): \(.closed_issues)/\(.open_issues + .closed_issues)"'

# Open issues
gh issue list --repo bendrucker/route-agent --state open --json number,title,milestone,body --limit 100
```

## Finding Ready Tasks

**Ready** = No "Depends On" section, OR all dependencies closed.

Parse from issue body:
```markdown
## Depends On
- Issue title here
```

## Parallel Work (`/project work`)

1. **Find ready tasks** - Parse dependencies, filter unblocked
2. **Create worktrees** - One per issue in `./worktrees/<N>/` (inside project, sandbox-allowed)
3. **Spawn sub-agents** - Each works in background, creates PR
4. **Report** - List spawned agents for monitoring

See [references/worktrees.md](references/worktrees.md) for details.

### Sub-Agent Prompt

```
Work on issue #N in worktree at <path>.

Issue: <title>
<body>

1. cd to worktree
2. Read CLAUDE.md and relevant docs
3. Implement requirements
4. Commit with descriptive message
5. Push and create PR with "Closes #N"
6. Return PR URL
```

## Milestone Priority

1. Foundation
2. Eval Setup (parallel)
3. Strava Integration
4. GraphHopper Integration
5. Route Synthesis
6. Place Search, Water Stops, Climb Integration, Weather Integration
7. Ride Preparation, Narrative Research
8. Research Quality, Route Refinement
9. Evaluation Framework

## Output

**Status:**
```
## Project Status

### Foundation (1/2)
- [x] #2 SDK project structure
- [ ] #3 Checkpoint system - READY

### Ready (2)
- #3 Checkpoint system (Foundation)
- #4 Promptfoo setup (Eval Setup)
```

**Work:**
```
## Parallel Work

Spawning:
- #3 Checkpoint system → worktree created, agent launched
- #4 Promptfoo setup → worktree created, agent launched

Monitor with /tasks. PRs appear for review.
```
