---
name: project-session
description: Project session management workflow for starting work sessions. Use at the beginning of a Claude Code session to select a project, load context from README.md and TASK_LIST.md, and get recommendations for next tasks. Handles project onboarding, task prioritization, and session handover.
---

# Project Session Workflow

## Session Startup Protocol

When starting a new session, follow this workflow:

### Step 1: Project Selection

List available projects from `source-code/` and ask the user:

```
👋 Welcome back! Which project would you like to work on today?

Available projects:
1. {project-1} - {brief description from README}
2. {project-2} - {brief description from README}
3. {project-3} - {brief description from README}

Or enter a project name directly.
```

### Step 2: Load Project Context

After selection, `cd` into `source-code/{project-name}/` and read:

1. **README.md** - Project overview, tech stack, setup instructions
2. **TASK_LIST.md** - Current tasks, priorities, blockers
3. **PROJECT_STATUS.md** (if exists) - Latest status update

### Step 3: Session Briefing

Present a formatted session briefing:

```
📋 Session Briefing: {Project Name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📂 Project: {name}
🔗 Tech Stack: {technologies}
📍 Working Directory: source-code/{project}/

📌 Current Sprint Focus
{summary from TASK_LIST}

📊 Task Status
✅ Completed: {count}
🔄 In Progress: {count}
📋 Pending: {count}
🚫 Blocked: {count}

🎯 Recommended Next Task
{suggested task with reasoning}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What would you like to do?
1. Start recommended task
2. View all tasks
3. Work on a specific task
4. Something else
```

## Directory Structure

```
My-Code/
├── bin/                    # Automation scripts
├── docs/                   # General documentation
├── logs/                   # Session changelogs
│   └── {PROJECT}_{SESSIONID}-{DATE}.md
├── projects/               # Project plans
│   └── {PROJECT}_{DATE}/
│       ├── PROJECT_CHARTER.md
│       ├── PROJECT_PROPOSAL.md
│       ├── PROJECT_PLAN.md
│       └── SPRINT_PLAN.md
└── source-code/            # Source code repositories
    └── {project}/
        ├── README.md
        ├── TASK_LIST.md
        └── PROJECT_STATUS.md
```

## TASK_LIST.md Format

```markdown
# Task List: {Project Name}

_Last Updated: {DATE}_
_Current Sprint: {Sprint Name}_

## Sprint Goals
- Goal 1
- Goal 2

## In Progress
| Task | Assignee | Status | Notes |
|------|----------|--------|-------|
| TASK-001 | @user | 🔄 Working | {brief note} |

## Pending (Prioritized)
| Priority | Task | Effort | Dependencies |
|----------|------|--------|--------------|
| P0 | TASK-002 | M | None |
| P1 | TASK-003 | S | TASK-002 |

## Blocked
| Task | Blocker | Owner | ETA |
|------|---------|-------|-----|
| TASK-004 | Waiting for API | @other | 2024-01-20 |

## Completed This Sprint
| Task | Completed | Notes |
|------|-----------|-------|
| TASK-005 | 2024-01-15 | Done |

## Handover Notes
{Context for next session}
```

## Session End Protocol

Before ending a session, create a session log in `logs/`:

**File:** `logs/{PROJECT}_{SESSIONID}-{DATE}.md`

```markdown
# Session Log: {Project Name}

**Date:** {DATE}
**Session:** {SESSIONID}
**Duration:** {approximate}

## Summary
{What was accomplished}

## Tasks Worked On
- {TASK-ID}: {description} - {status}

## Changes Made
- {file/component}: {change description}

## Decisions
- {decision}: {reasoning}

## Blockers Encountered
- {blocker}: {resolution or status}

## Next Steps
1. {Next task recommendation}
2. {Another next step}

## Handover Notes
{Context for next session}
```

## Response Style

Use appropriate formatting for different message types:

### Task Recommendations
```
🎯 Recommended: {Task Title}

Priority: P0 | Effort: M | Type: {feature/bug/refactor}

Why this task:
{reasoning based on dependencies, sprint goals, or urgency}

Getting started:
1. {first step}
2. {second step}

Ready to start? Let me know!
```

### Progress Updates
```
✅ Progress Update

Completed:
- {item 1}
- {item 2}

In Progress:
- {current work}

Next:
- {upcoming}
```

### Session Summary
```
📋 Session Complete!

Accomplished:
✅ {achievement 1}
✅ {achievement 2}

Time to wrap up?
1. Create session log
2. Update TASK_LIST.md
3. Commit changes
```

## Quick Commands

During a session, respond to these requests:

| User Says | Action |
|-----------|--------|
| "What's next?" | Show recommended task |
| "Show all tasks" | Display full TASK_LIST |
| "Update status" | Update task status in TASK_LIST.md |
| "End session" | Create session log and summary |
| "Switch project" | Return to project selection |
| "Create task" | Add new task to TASK_LIST.md |

## Integration with Other Skills

- **java-backend** / **nextjs-frontend** / **ui-designer** - Load appropriate skill based on project type
- **project-planner** - Use for creating new project plans in `projects/`
- **skill-creator** - Use for creating project-specific skills

## References

- **Task Prioritization**: See [references/prioritization.md](references/prioritization.md) for task ranking methodology
- **Session Templates**: See [references/templates.md](references/templates.md) for log templates
