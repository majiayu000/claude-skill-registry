---
name: gsd-migrate
description: Migrates existing projects to GSD structure without rewriting history. Activates when user mentions "migrate to GSD", "adopt GSD", "convert project", "brownfield GSD", or wants to add GSD to existing work.
---

# GSD Project Migration Assistant

Bridges the gap between existing projects and GSD adoption by inferring GSD artifacts from current project state, preserving git history and existing work.

## When to Use

Activate when the user:
- Has an existing project and wants to adopt GSD
- Mentions "migrate", "convert to GSD", "add GSD"
- Asks "can I use GSD on an existing project?"
- Has brownfield code and wants structure

## What This Skill Does

**Analyzes existing project** to extract:
- Project vision from README, package.json, docs
- Requirements from features, git commits, code analysis
- Current progress from file structure and git history
- Work remaining from TODOs, issues, backlog

**Generates GSD artifacts** that map current state:
- PROJECT.md (what this is, validated requirements, decisions)
- ROADMAP.md (completed phases + future work)
- STATE.md (current position)
- config.json (sensible defaults)

**Preserves history:**
- No git rewriting or rebasing
- Existing commits untouched
- GSD structure added on top

## Migration Process

### Phase 1: Discovery & Analysis

#### Step 1.1: Detect Project Type

```bash
# Analyze project indicators
if [ -f "package.json" ]; then
  PROJECT_TYPE="javascript"
  # Read: name, description, dependencies
elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
  PROJECT_TYPE="python"
elif [ -f "go.mod" ]; then
  PROJECT_TYPE="go"
elif [ -f "Cargo.toml" ]; then
  PROJECT_TYPE="rust"
fi

# Check for frameworks
if grep -q "react" package.json 2>/dev/null; then
  FRAMEWORK="react"
elif grep -q "express" package.json 2>/dev/null; then
  FRAMEWORK="express"
fi
```

#### Step 1.2: Extract Project Vision

**Sources to analyze:**

| Source | What to Extract |
|--------|-----------------|
| README.md | Project purpose, features, usage |
| package.json / Cargo.toml | Name, description, keywords |
| CONTRIBUTING.md | Project goals, roadmap |
| docs/ | Architecture, design decisions |
| Git commits | Feature patterns, evolution |

**Example extraction:**
```markdown
From README.md:
"TaskFlow - A lightweight task management API for teams"
→ Core Value: Team task coordination

From package.json:
"keywords": ["tasks", "api", "collaboration"]
→ Domain: Collaborative task management

From git log:
Early commits: Setup, models, basic CRUD
Recent commits: Real-time updates, permissions
→ Project maturity: Mid-stage, core features built
```

#### Step 1.3: Identify Completed Work

**Analyze git history:**
```bash
# Get all commits
git log --oneline --all > commits.txt

# Identify feature commits
grep -E "feat|add|implement" commits.txt

# Group by feature area
# "feat: add user auth" → Authentication feature
# "feat: implement tasks CRUD" → Task management feature
```

**Analyze codebase:**
```bash
# Find main features from file structure
ls src/
# → auth/, tasks/, notifications/, teams/

# For each directory, infer feature
# auth/ → Authentication feature
# tasks/ → Task management feature
```

#### Step 1.4: Identify Remaining Work

**Sources for remaining work:**

```bash
# TODOs in code
grep -r "TODO" src/ --include="*.js" --include="*.ts"

# GitHub/GitLab issues
gh issue list --state open

# Comments marked with future work
grep -r "FIXME\|HACK\|XXX" src/

# Incomplete features (from README)
# README says "Features: Auth, Tasks, Search"
# But src/ only has auth/ and tasks/
# → Search is remaining work
```

### Phase 2: Generate GSD Artifacts

#### Step 2.1: Create PROJECT.md

**Template:**
```markdown
# [Project Name]

## What This Is

[Extracted from README/package.json]

## Current State

**Built:** [Summary of completed features]
**Codebase:** [LOC] across [N] files
**Last activity:** [Most recent commit date]

**Migrated to GSD:** [Today's date]

## Core Value

[One-sentence value prop from README]

## Requirements

### Validated

[Features that already exist in codebase]

- ✓ REQ-01: User authentication
  - Source: src/auth/, committed [date]
- ✓ REQ-02: Task CRUD operations
  - Source: src/tasks/, committed [date]

### Active

[Work in progress or remaining from backlog]

- → REQ-03: Real-time notifications
  - Source: TODOs in src/, GitHub issue #42
- → REQ-04: Team collaboration
  - Source: README planned features

### Out of Scope

[Explicitly not doing, from CONTRIBUTING or discussions]

## Constraints

[Inferred from dependencies, architecture]

- **Tech stack:** [From package.json/requirements.txt]
- **Deployment:** [From Dockerfile, deployment files]
- **Compatibility:** [From .nvmrc, engines field]

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| [Tech choice from dependencies] | [Inferred] | ✓ Good - [status] |
```

#### Step 2.2: Create ROADMAP.md

**Map completed work to phases:**
```markdown
# Roadmap

## Milestones

### v1.0 - MVP (Complete)

Completed: [Date of feature completion]

#### Phase 1: Project Setup

**Status:** ✓ Complete
**Completed:** [First commit date]

**Goal:** Initialize project structure

**Deliverables:**
- ✓ Node.js project with Express
- ✓ Database configuration (PostgreSQL)
- ✓ Basic server skeleton

**Success Criteria:**
- Server starts successfully
- Database connection works

---

#### Phase 2: Authentication

**Status:** ✓ Complete
**Completed:** [Auth commit date]

**Goal:** User registration and login

**Deliverables:**
- ✓ User model with password hashing
- ✓ Registration endpoint
- ✓ Login with JWT
- ✓ Auth middleware

**Success Criteria:**
- Users can register and login
- Protected routes require valid JWT

---

### v2.0 - Collaboration Features (In Progress)

#### Phase 3: Task Management

**Status:** ✓ Complete
**Completed:** [Task commit date]

**Goal:** CRUD operations for tasks

**Deliverables:**
- ✓ Task model
- ✓ Create, read, update, delete endpoints
- ✓ Task assignment to users

---

#### Phase 4: Real-Time Notifications

**Status:** → In Progress
**Started:** [Date or "Not started"]

**Goal:** Live updates for task changes

**Deliverables:**
- WebSocket server setup
- Task change events
- Client subscription model

**Success Criteria:**
- Users see task updates in real-time
- No polling required

---

#### Phase 5: Team Collaboration

**Status:** Planned

**Goal:** Multi-user teams with permissions

**Deliverables:**
- Team model
- Invite system
- Role-based permissions
- Team task visibility

**Success Criteria:**
- Users can create teams
- Tasks scoped to teams
- Only team members can view team tasks
```

#### Step 2.3: Create STATE.md

**Map current position:**
```markdown
# Project State

## Project Reference

See: .planning/PROJECT.md (created [date] during migration)

**Core value:** [From PROJECT.md]
**Current focus:** [Inferred from recent commits or in-progress work]

## Current Position

Phase: 4 of 5 (based on ROADMAP.md analysis)
Plan: In progress (Phase 4 started, not complete)
Status: Migrated to GSD [date]
Last activity: [Most recent commit date]

Progress: [████████░░] 80% (4 of 5 phases)

## Completed Work (Pre-GSD)

| Phase | Name | Completion Date |
|-------|------|-----------------|
| 1 | Project Setup | [First commit date] |
| 2 | Authentication | [Auth complete date] |
| 3 | Task Management | [Tasks complete date] |

## Current Work

Phase 4: Real-Time Notifications
Status: In progress (WebSocket setup done, events TODO)
Files: src/websocket/, src/events/ (partial)

## Accumulated Context

### Decisions

Pre-GSD decisions inferred from codebase:

| Decision | Source | Date |
|----------|--------|------|
| PostgreSQL over MongoDB | package.json dependencies | [Date] |
| JWT over sessions | src/auth/jwt.js | [Date] |
| Express framework | package.json | [Initial commit] |

### Pending Todos

- [ ] Complete WebSocket event system (Phase 4)
- [ ] Add team permissions (Phase 5)
- [ ] Write integration tests (TODO comments in code)

### Blockers/Concerns

None (fresh migration)

## Session Continuity

Last session: [Migration date]
Stopped at: Migration complete, GSD structure created
Resume file: None
```

#### Step 2.4: Create config.json

**Sensible defaults:**
```json
{
  "mode": "interactive",
  "model_profile": "balanced",
  "depth": "standard",
  "research": false,
  "commit_docs": true
}
```

**Rationale:**
- `interactive`: Safer for existing projects (require confirmation)
- `balanced`: Good quality without excessive cost
- `depth: standard`: Not too quick, not too thorough
- `research: false`: Existing project likely has established patterns
- `commit_docs: true`: Track docs with code

### Phase 3: Review & Confirm

Present the migration plan to the user:

```markdown
# Migration Plan for [Project Name]

## Analysis Summary

**Detected:**
- Language/Framework: Node.js + Express
- Database: PostgreSQL
- Features: Authentication, Task CRUD, partial Notifications
- Commits: 142 commits over 6 months
- Last activity: 3 days ago

## Proposed GSD Structure

### PROJECT.md
- Core Value: Team task coordination
- Validated Requirements: REQ-01 (Auth), REQ-02 (Tasks), REQ-03 (Notifications - partial)
- Active Requirements: REQ-04 (Teams), REQ-05 (Permissions)

### ROADMAP.md
- ✓ Phase 1: Setup (complete)
- ✓ Phase 2: Authentication (complete)
- ✓ Phase 3: Task Management (complete)
- → Phase 4: Notifications (in progress)
- Planned: Phase 5: Team Collaboration

### STATE.md
- Current Position: Phase 4 of 5 (80% progress)
- 142 commits preserved in history
- Ready to continue with GSD workflows

## What Gets Created

Files to write:
- .planning/PROJECT.md
- .planning/REQUIREMENTS.md
- .planning/ROADMAP.md
- .planning/STATE.md
- .planning/config.json

Git:
- 1 commit: "chore: migrate project to GSD structure"
- Existing history untouched

## Next Steps After Migration

1. Review generated artifacts and edit as needed
2. Continue current work:
   - /gsd:plan-phase 4 (if not already planned)
   - /gsd:execute-phase 4 (finish notifications)
3. Plan remaining work:
   - /gsd:plan-phase 5 (team collaboration)

---

Ready to migrate? (yes/review-files/cancel)
```

### Phase 4: Execute Migration

If user confirms:

```bash
# Create .planning/ directory
mkdir -p .planning/phases

# Write generated artifacts
write_file ".planning/PROJECT.md" "$PROJECT_MD_CONTENT"
write_file ".planning/REQUIREMENTS.md" "$REQUIREMENTS_MD_CONTENT"
write_file ".planning/ROADMAP.md" "$ROADMAP_MD_CONTENT"
write_file ".planning/STATE.md" "$STATE_MD_CONTENT"
write_file ".planning/config.json" "$CONFIG_JSON_CONTENT"

# Create phase directories for completed phases
for phase in 01-setup 02-auth 03-tasks; do
  mkdir -p ".planning/phases/$phase"
done

# Create .gitkeep for empty directories
touch .planning/phases/04-notifications/.gitkeep

# Commit the migration
git add .planning/
git commit -m "chore: migrate project to GSD structure

Migrated existing project to GSD workflow system.

Completed work mapped to Phases 1-3.
Current work (Phase 4: Notifications) in progress.
Remaining work (Phase 5: Teams) planned in ROADMAP.

All existing commits preserved.
GSD structure added for future development.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

## Migration Strategies

### Strategy 1: Full Project Migration

**When:** Complete brownfield project, want full GSD adoption

**Approach:**
- Analyze entire history
- Map all completed work to phases
- Create complete ROADMAP with all remaining work

**Outcome:** Full GSD structure, ready for complete workflow adoption

---

### Strategy 2: Incremental Migration

**When:** Large project, want to ease into GSD

**Approach:**
- Only map recent work (last N months)
- Mark everything before as "Legacy"
- Use GSD for new work only

**Outcome:**
```markdown
ROADMAP.md:

## Legacy Work (Pre-GSD)
Phases 1-10: Completed before GSD adoption
See: git log --before="2024-01-01"

## v2.0 (GSD-Managed)
Phase 11: New feature (planned with GSD)
Phase 12: Refactor (planned with GSD)
```

---

### Strategy 3: Feature Branch Migration

**When:** Want to try GSD on one feature before full adoption

**Approach:**
- Create feature branch
- Initialize minimal GSD structure for that feature only
- Merge back if successful

**Outcome:** Risk-free trial of GSD workflows

## Common Migration Scenarios

### Scenario 1: Project with Clear Features

**Example:** E-commerce site with auth, products, cart, checkout

**Migration:**
```
Phase 1: Setup
Phase 2: Authentication
Phase 3: Product Catalog
Phase 4: Shopping Cart
Phase 5: Checkout Process

All phases marked complete in ROADMAP.
STATE.md shows: Phase 5 of 5 complete.
Ready for: /gsd:new-milestone to start v2.0
```

---

### Scenario 2: Project with Incomplete Work

**Example:** Started notifications but not finished

**Migration:**
```
Phase 4: Notifications
  Status: In Progress
  Completed:
    - WebSocket server setup
    - Connection handling
  Remaining:
    - Event emission on task changes
    - Client subscription system

ROADMAP: Mark as "In Progress"
STATE.md: Current Position = Phase 4
Next: /gsd:plan-phase 4 to plan remaining work
```

---

### Scenario 3: Project with No Clear Structure

**Example:** Monolith with mixed concerns, unclear boundaries

**Migration:**
```
Ask user to help define phases:

"I see your project has authentication, data processing,
and reporting features mixed together. How would you
like to structure these into phases?"

User helps define:
Phase 1: Core setup
Phase 2: Data ingestion
Phase 3: Processing pipeline
Phase 4: Report generation
Phase 5: API endpoints

Then map files to phases based on user input.
```

---

### Scenario 4: Project with TODOs but No Backlog

**Migration:**
```bash
# Extract TODOs from code
grep -r "TODO" src/ > todos.txt

# Group by feature area
# TODO in src/auth/ → Authentication todos
# TODO in src/tasks/ → Task management todos

# Create phase for "Tech Debt & Improvements"
Phase 6: Tech Debt & Improvements
  Goal: Address TODOs and improve code quality
  Deliverables:
    - Fix auth edge cases (3 TODOs)
    - Optimize task queries (2 TODOs)
    - Add error handling (5 TODOs)
```

## Post-Migration Checklist

After migration completes:

```markdown
## Immediate Steps

- [ ] Review generated PROJECT.md - adjust vision/requirements
- [ ] Review ROADMAP.md - verify phase mapping is accurate
- [ ] Review STATE.md - confirm current position
- [ ] Test GSD workflows:
  - [ ] Run /gsd:progress (should show current state)
  - [ ] Try /gsd:plan-phase for next incomplete phase
  - [ ] Try /gsd:quick for a small task

## First Week

- [ ] Complete current phase using GSD execution
- [ ] Run /gsd:verify-work to validate
- [ ] Use /gsd:add-todo for capturing ideas
- [ ] Commit docs and summaries as work progresses

## Long Term

- [ ] Team members run /gsd:progress to sync
- [ ] Use PROJECT.md Key Decisions table for ADRs
- [ ] Plan milestones with /gsd:new-milestone
- [ ] Archive completed milestones with /gsd:complete-milestone
```

## Troubleshooting Migration

### Issue: Can't determine what's complete

**Solution:**
```
Ask user to guide:

"I see features in src/auth/, src/tasks/, and src/notifications/.
Which of these are complete and production-ready?

User: "Auth and tasks are done, notifications is half-done"

→ Mark Phase 2 (Auth) and 3 (Tasks) complete
→ Mark Phase 4 (Notifications) in progress
```

---

### Issue: Git history is messy

**Solution:**
```
Don't try to parse messy history perfectly.

Instead:
- Look at current file structure (what exists now)
- Ask user what's complete
- Mark everything as "Legacy" if needed
- Focus GSD on future work
```

---

### Issue: Project uses non-standard structure

**Solution:**
```
GSD is flexible - adapt phase mapping:

Phase 1: Infrastructure (Terraform files)
Phase 2: Backend API (src/api/)
Phase 3: Background Jobs (src/workers/)
Phase 4: Frontend (client/)

Map phases to YOUR project's structure, not a template.
```

## Migration Examples

### Example 1: Todo App Migration

**Before:**
```
todo-app/
├── src/
│   ├── auth.js
│   ├── todos.js
│   ├── db.js
│   └── server.js
├── tests/
├── README.md
└── package.json

Git: 47 commits over 2 months
Last: "fix: todo deletion bug"
```

**After Migration:**
```
todo-app/
├── .planning/
│   ├── PROJECT.md
│   ├── REQUIREMENTS.md
│   ├── ROADMAP.md
│   ├── STATE.md
│   ├── config.json
│   └── phases/
│       ├── 01-setup/
│       ├── 02-auth/
│       └── 03-todos/
├── src/ [unchanged]
├── tests/ [unchanged]
└── [other files unchanged]

ROADMAP shows:
  ✓ Phase 1: Setup
  ✓ Phase 2: Authentication
  ✓ Phase 3: Todo CRUD

STATE shows:
  Current: All phases complete
  Next: /gsd:new-milestone for v2.0
```

### Example 2: API with Incomplete Features

**Before:**
```
api-server/
├── src/
│   ├── users/ (complete)
│   ├── posts/ (complete)
│   ├── comments/ (partial - create/read only)
│   └── search/ (empty - planned)

Git: 89 commits over 4 months
```

**After Migration:**
```
ROADMAP:
  ✓ Phase 1: Setup
  ✓ Phase 2: User Management
  ✓ Phase 3: Posts
  → Phase 4: Comments (in progress)
  Planned: Phase 5: Search

STATE:
  Current Position: Phase 4 of 5
  Next: /gsd:plan-phase 4 (complete comments CRUD)
```

## Integration with GSD

This skill **complements** GSD by:
- Enabling brownfield adoption without rewriting history
- Bridging the gap between unstructured and structured development
- Preserving all existing work and commits
- Creating a smooth onboarding path for existing projects

It **does not replace** GSD:
- No workflow logic duplicated
- After migration, standard GSD workflows take over
- Migration is one-time; GSD workflows are ongoing
- Purely a bridge to get projects into GSD structure
