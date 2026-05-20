---
name: managing-tickets-and-tasks-in-plane
description: |
  Multi-workspace Plane sprint board management with intelligent automation, ticket creation, and BMAD workflow integration.

  Use this skill when:
  - Creating tickets from BMAD stories, task descriptions, or audit findings
  - Auditing board organization (ticket clustering, label optimization, status bottlenecks)
  - Selecting the next optimal ticket to work on (priority scoring algorithm)
  - Promoting completed tickets to production and generating changelogs
  - Managing sprint workflows with status tracking and WIP limits
  - Working with multiple Plane workspaces (auto-detects from git remote or directory)

  Triggers: "create ticket", "board audit", "what should I work on", "next ticket", "promote to production", "changelog", "sprint status", "WIP limit", plane ticket operations
---

# Managing Tickets and Tasks in Plane

## Plane Configuration

**Connection:** Plane MCP server or direct Plane REST API via `curl`

**Premium Features Limitation:** Cycles (sprints) are a premium-only feature. Use sprint labels as a workaround:
- Create labels: `sprint-1`, `sprint-2`, `sprint-3`, etc.
- Filter views by sprint label to simulate cycle boards
- Use label colors to visually distinguish sprints (e.g., teal for current sprint)

**Multi-Workspace Support:** Automatically detects workspace from:
1. Local `.plane.json` in project root (highest priority)
2. Git remote URL patterns
3. Current directory path
4. `PLANE_WORKSPACE` environment variable
5. Default workspace from `~/.claude/plane-workspaces.json`

**Plane REST API Endpoints:**
- `GET /api/v1/workspaces/{workspace}/projects/{project}/issues/` - List issues
- `POST /api/v1/workspaces/{workspace}/projects/{project}/issues/` - Create issue
- `PATCH /api/v1/workspaces/{workspace}/projects/{project}/issues/{id}/` - Update issue
- `GET /api/v1/workspaces/{workspace}/projects/{project}/states/` - List states/statuses
- `GET /api/v1/workspaces/{workspace}/projects/{project}/labels/` - List labels

**Authentication:** `X-Api-Key` header with value from workspace-specific env var (e.g., `PLANE_API_KEY`)

## Core Workflows

### 0. Initialize New Project (First-Time Setup)

When initializing a new project in Plane, execute the full onboarding workflow:

**Trigger:** "initialize project in plane", "setup plane for project", or first ticket creation in unknown project

**Workflow Steps:**

1. **Create/Verify Project**
   - Check if project exists (by identifier)
   - Create if missing with description from README/CLAUDE.md
   - Set project emoji based on theme

2. **Generate Absurd Project Art** (via `fal-text-to-image` skill)
   - Generate themed mascot/header image using project context
   - Prompt formula: `"A weird [PROJECT_THEME] creature in absurdist corporate art style, [PROJECT_SPECIFIC_ELEMENTS], vibrant colors, slightly unsettling but friendly, like a mascot designed by a 5-year-old CEO"`
   - Save to `docs/[project]-mascot.png`
   - Set as Plane project cover image

3. **Create Label Taxonomy**
   - Priority: `must-have`, `should-have`, `could-have` (MoSCoW)
   - Sprint: `sprint-1`, `sprint-2`, `sprint-3`, etc. (workaround for premium cycles)
   - Type: `infrastructure`, `feature`, `ai-pipeline`, `auth`, `monetization`
   - Effort: `effort:S`, `effort:M`, `effort:L`, `effort:XL` (optional)
   - Special: `blocked`, `needs-review` (status helpers)

4. **Seed Backlog from PRD** (if PRD exists)
   - Parse feature list from PRD
   - Create one ticket per feature with:
     - Description from PRD user story
     - Appropriate phase/priority/effort labels
     - Acceptance criteria from PRD

5. **Establish Art Theme** (document in project)
   - Create `docs/PLANE_ART_THEME.md` with:
     - Theme name and visual language
     - Tone description
     - Usage guidelines for ticket categories
     - Original mascot prompt for variations

**Output:**
```
✓ Project initialized: [PROJ] Project Name
  Cover: docs/project-mascot.png (uploaded)
  Labels: 14 created (3 priority, 4 phase, 4 effort, 3 type)
  Backlog: 10 tickets seeded from PRD
  Art Theme: "Theme Name" documented in docs/PLANE_ART_THEME.md
```

See [references/project-initialization.md](references/project-initialization.md) for detailed workflow.

### 1. Create Ticket from Story/Task

Parse input for discrete tasks, extract metadata, check duplicates, create via API.

**Ticket Metadata:**
- Title: Clear, action-oriented
- Description: User story format + acceptance criteria
- Priority: urgent/high/medium/low
- Story points: 1/2/3/5/8/13
- Labels: Auto-detect (security, performance, frontend, backend, sprint-N)

**Output format:**
```
✓ Ticket Created: [CWS-015] Fix API authentication bug
Priority: urgent | Points: 3 | Sprint: 1 | Labels: security, backend
URL: https://plane.internal.intelliforia.com/.../CWS-015
```

See [references/create-ticket-from-story.md](references/create-ticket-from-story.md) for full workflow.

### 2. Audit Board State

Analyze ticket distribution and recommend optimizations.

**Audit Checklist:**
1. **Ticket Clustering** - Group related tickets (3+ related → parent issue, 5+ → epic)
2. **Label Optimization** - Missing labels, redundant labels, new label recommendations
3. **Status Distribution** - WIP bottlenecks, stale tickets (>14 days in todo)
4. **View Recommendations** - "My Sprint", "Blocked Items", "Quick Wins", "Tech Debt"
5. **Dependency Analysis** - Map dependencies, detect circular refs, identify blockers

**Audit Depths:**
- `quick`: Basic metrics (<5 seconds)
- `standard`: With clustering analysis (<15 seconds)
- `comprehensive`: Full NLP analysis (<60 seconds)

See [references/audit-board-state.md](references/audit-board-state.md) for full workflow.

### 3. Select Next Logical Ticket

Score and recommend optimal ticket based on priority algorithm.

**Selection Algorithm:**
```
score = priority_score + effort_score + age_score + dependency_bonus + critical_path_bonus - blocker_penalty
```

**Scoring Weights:**
- Priority: urgent=10, high=7, medium=3, low=0
- Effort (favor quick wins): 1-2pts=+5, 3-5pts=+3, 8+pts=-2
- Age (address stale): >14 days=+3, >7 days=+2
- Dependency bonus: +2 per ticket unblocked (cap 10)
- Critical path: +8

**Output:**
```
🎯 Recommended: [CWS-004] Fix production build (Score: 21)
Why: URGENT priority, unblocks 2 tickets, on critical path

Alternatives:
1. [CWS-001] API key rotation (18 pts, security critical)
2. [CWS-012] Add CSP (8 pts, quick win - 1 point)

Marking CWS-004 as in-progress...
✓ Status updated, assigned to you, start time logged
```

See [references/select-next-ticket.md](references/select-next-ticket.md) for full algorithm.

### 4. Promote Completed Tickets

After staging merged to main:
1. Query completed tickets in current sprint
2. Verify acceptance criteria met
3. Move to "live" status, add "deployed-production" label
4. Generate changelog from ticket data
5. Send notification email to team

See [assets/changelog-email.md](assets/changelog-email.md) for email template.

## Hook Integration

### Pre-Prompt Hook (Automatic)

Runs before every prompt to check board state.

**Checks:**
- WIP limit exceeded? (warn if >5 in-progress)
- Current ticket context from git branch
- Dependency conflicts
- Urgent tickets needing attention

**Silent mode:** Passes without output if no issues.

### Stop Hook (Automatic)

Runs at session end to update ticket.

**Actions:**
1. Detect ticket from git branch (`CWS-\d+` pattern)
2. Generate session summary (files changed, commits, duration)
3. Prompt for status update (in-progress/completed/blocked)
4. Append development log to ticket description

## BMAD Integration Points

| Workflow | Phase | Action |
|----------|-------|--------|
| `/create-story` | post-creation | Auto-create Plane ticket from story |
| `/sprint-planning` | post-planning | Batch create all sprint tickets |
| `/dev-story` | pre-implementation | Select optimal ticket, mark in-progress |
| `/captain:sync` | continuous | Bidirectional doc/ticket sync |
| `/captain:health` | on-demand | Board health and decomposition check |
| `/captain:prune` | weekly | Backlog cleanup recommendations |

## Multi-Workspace Configuration

**Config file:** `~/.claude/plane-workspaces.json`

```json
{
  "workspaces": {
    "intelliforia": {
      "api_key_env": "PLANE_API_KEY",
      "base_url": "plane.internal.intelliforia.com",
      "projects": { "default": "dfb05f73-cab7-4447-a4a1-360bb7ca7177" },
      "wip_limits": { "individual": 3, "team": 7 }
    }
  },
  "detection": {
    "git_remote_patterns": { "intelliforia": "intelliforia" },
    "directory_patterns": { "/home/delorenj/code/intelliforia": "intelliforia" }
  },
  "default_workspace": "intelliforia"
}
```

**Per-project override:** Create `.plane.json` in project root:
```json
{ "workspace": "intelliforia", "project_id": "uuid-here" }
```

## Ticket Template

See [assets/ticket-template.md](assets/ticket-template.md) for standard ticket format with:
- User story (As a... I want... So that...)
- Acceptance criteria checklist
- Technical notes and dependencies
- Development log (auto-populated by stop hook)

## Error Handling

**API failures:** Retry with exponential backoff (3 attempts), cache locally for later sync

**Ticket not found:** Search similar IDs, prompt user, offer to create new ticket

**Dependency conflicts:** Warn user, offer options (work on blocker first, continue anyway, remove dependency)

**WIP limit exceeded:** Warn but don't block, suggest completing existing work

## Quick Reference

```bash
# Create ticket
"Create a ticket for fixing the login bug, high priority, 3 points"

# Board audit
"Run a board audit" or "Audit board state --depth comprehensive"

# Next ticket
"What should I work on next?" or "Select next ticket"

# Promote to production
"Promote completed tickets from Sprint 1 and send changelog"

# Check status
"Show sprint progress" or "List my in-progress tickets"
```
