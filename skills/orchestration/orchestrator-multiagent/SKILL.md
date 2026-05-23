---
name: orchestrator-multiagent
description: Multi-agent orchestration for building software incrementally. Use when coordinating workers via native Agent Teams (Teammate + TaskCreate + SendMessage), managing task state with Beads, delegating features to specialized workers (frontend-dev-expert, backend-solutions-engineer, etc.), tracking progress across sessions, or implementing the four-phase pattern (ideation → planning → execution → validation). Triggers on orchestration, coordination, multi-agent, beads, worker delegation, session handoff, progress tracking, agent teams, teammates.
title: "Orchestrator Multiagent"
status: active
---

# Multi-Agent Orchestrator Skill

## 🚀 SESSION START (Do This First)

| Step | Action | Reference |
|------|--------|-----------|
| 1 | **Pre-Flight Checklist** | Complete [PREFLIGHT.md](PREFLIGHT.md) |
| 2 | **Find Work** | `bd ready` |
| 3 | **Multi-feature?** | See [WORKFLOWS.md](WORKFLOWS.md#autonomous-mode-protocol) |

**Everything below is reference material.**

---

## Core Rule: Delegate, Don't Implement

**Orchestrator = Coordinator. Worker = Implementer.**

```python
# ✅ CORRECT - Worker via native team teammate
# Step 1: Create team (once per session, in PREFLIGHT)
Teammate(
    operation="spawnTeam",
    team_name="{initiative}-workers",
    description="Workers for {initiative}"
)

# Step 2: Create work item
TaskCreate(
    subject="Implement feature F001",
    description="""
    ## Task: [Task title from Beads]

    **Context**: [investigation summary]
    **Requirements**: [list requirements]
    **Acceptance Criteria**: [list criteria]
    **Scope** (ONLY these files): [file list]

    **Report back with**: Files modified, tests written/passed, any blockers
    """,
    activeForm="Implementing F001"
)

# Step 3: Spawn specialist worker into team
Task(
    subagent_type="frontend-dev-expert",
    team_name="{initiative}-workers",
    name="worker-frontend",
    prompt="You are worker-frontend in team {initiative}-workers. Check TaskList for available work. Claim tasks, implement, report completion via SendMessage to team-lead."
)

# Step 4: Worker results arrive via SendMessage (auto-delivered to you)
# Worker sends: SendMessage(type="message", recipient="team-lead", content="Task #X complete: ...")
```

**Why native teams?** Workers are persistent teammates that can claim tasks, communicate with each other, and handle multiple assignments within a single session. The orchestrator creates tasks and workers pick them up -- no blocking, no single-assignment limitation.

**Parallel workers**: Spawn multiple teammates into the same team. Each claims different tasks from the shared TaskList. Workers coordinate peer-to-peer via SendMessage.

---

## Implementation Complete Handoff

**When orchestrator's workers finish implementation:**

Orchestrators mark tasks `impl_complete` to signal System 3 for independent validation.
Orchestrators do NOT close tasks — System 3's oversight team handles validation and closure.

**Handoff Protocol:**
1. Workers confirm: code committed, unit tests pass, implementation complete
2. Orchestrator marks bead: `bd update <id> --status=impl_complete`
3. Orchestrator continues to next task (does NOT wait for S3 validation)

**Custom Beads Status Lifecycle:**
```
open → in_progress → impl_complete → [S3 validates] → closed
                         ↑                    │
                         └────────────────────┘
                       (s3_rejected → back to in_progress)
```

| Status | Set By | Meaning |
|--------|--------|---------|
| `open` | Planning | Task exists, not started |
| `in_progress` | Orchestrator | Worker actively implementing |
| `impl_complete` | Orchestrator | Done — requesting S3 review |
| `s3_validating` | System 3 | Oversight team actively checking |
| `s3_rejected` | System 3 | Failed validation — back to orchestrator |
| `closed` | System 3 (s3-validator) | Validated with evidence |

**What orchestrators SHOULD NOT do:**
- Do NOT run `bd close` — System 3 handles this after independent validation
- Do NOT spawn a validator teammate — validation is System 3's responsibility
- Do NOT wait for validation before starting next task

---

## Quick Reference

### State Management (Beads - Recommended)

**Primary**: `.beads/` directory managed by `bd` commands

```bash
# Essential Beads commands
bd ready                          # Get unblocked tasks (MOST IMPORTANT)
bd list                           # All tasks
bd show <bd-id>                   # Task details
bd reopen <bd-id>                 # Reopen if regression found
bd dep list <bd-id>               # Show dependencies
```

**Quick Reference**: [REFERENCE.md](REFERENCE.md#beads-commands)

### Worker Types (Spawned as Teammates)

These types are used as `subagent_type` when spawning teammates via `Task(..., team_name=..., name=...)`:

| Type | subagent_type | Teammate Name | Use For |
|------|---------------|---------------|---------|
| Frontend | `frontend-dev-expert` | `worker-frontend` | React, Next.js, UI, TypeScript |
| Backend | `backend-solutions-engineer` | `worker-backend` | Python, FastAPI, PydanticAI, MCP |
| **Browser Testing** | `tdd-test-engineer` | `worker-tester` | **E2E UI validation, automated browser testing** |
| Architecture | `solution-design-architect` | `worker-architect` | Design docs, PRDs |
| General | `Explore` | `worker-explore` | Investigation, code search |

**Pattern**: Use `Task(subagent_type="...", team_name="...", name="...")` to spawn teammates. Workers claim tasks from the shared TaskList and report via SendMessage.

### Key Directories
- `.beads/` - Task state (managed by `bd` commands)
- `.claude/progress/` - Session summaries and logs
- `.claude/learnings/` - Accumulated patterns

### Service Ports
- Frontend: 5001 | Backend: 8000 | eddy_validate: 5184 | user_chat: 5185

### Essential Commands

```bash
# Services (see VALIDATION.md for details)
./my-project-backend/start_services.sh
cd my-project-frontend && npm run dev

# Task status (Beads - RECOMMENDED)
bd ready                                    # Get unblocked tasks
bd list                                     # All tasks
bd show <bd-id>                             # Task details

# Update task status (Beads)
bd update <bd-id> --status in-progress      # Mark as started
bd update <bd-id> --status=impl_complete     # Signal S3 for validation

# Commit (Beads)
git add .beads/ && git commit -m "feat(<bd-id>): [description]"
```

---

## Workflow Triage (MANDATORY FIRST STEP)

**Before any orchestration, determine which workflow applies:**

```
1. Check Beads status: bd list
   ↓
2. If NO TASKS exist → IDEATION + PLANNING MODE (Phase 0 + Phase 1)

   🚨 STOP HERE - Before planning:
   □ Read WORKFLOWS.md Feature Decomposition section (MANDATORY)
   □ Complete Phase 0: Ideation (brainstorming + research)
   □ Create TodoWrite checklist for Phase 1 steps
   ↓
3. If TASKS exist → Check task status: bd stats
   ↓
4. Determine execution workflow type:

   ALL tasks open → EXECUTION MODE (Phase 2)
   SOME tasks closed, some open → CONTINUATION MODE (Phase 2)
   All impl done, AT pending → VALIDATION MODE (Phase 3)
   ALL tasks closed → MAINTENANCE MODE (delegate single hotfix)
```

### Session Start Memory Check (CRITICAL CIRCUIT BREAKER)

**🚨 MANDATORY: Run [PREFLIGHT.md](PREFLIGHT.md) checklist before ANY investigation.**

The preflight includes:
- ✅ Serena activation (code navigation only)
- ✅ Hindsight memory recall (patterns, lessons learned)
- ✅ Service health verification
- ✅ Regression validation (1-2 closed tasks)
- ✅ Session goal determination

**Why This Matters**: Memory check prevents repeating mistakes. Missing memories costs hours of repeated investigation (Session F087-F092 evidence).

### Workflow Decision Matrix

| Scenario | Signs | Workflow |
|----------|-------|----------|
| **Ideation** | No tasks exist, new initiative | Phase 0: Ideation (brainstorming + research) |
| **Planning** | Ideation done, no Beads tasks | Phase 1: Planning (uber-epic + task decomposition + acceptance test generation) |
| **Execution** | Tasks exist, all open | Phase 2: Execution (incremental implementation) |
| **Continuation** | Some tasks closed, some open | Phase 2: Execution (continue from where left off) |
| **Validation** | All impl done, AT pending | Phase 3: Validation (AT epic closure) |
| **Maintenance** | All tasks closed, minor fix needed | Direct Fix (delegate single task) |

---

## The Four-Phase Pattern

### Phase 0: Ideation (Brainstorming + Research)

**Every new project MUST begin with structured ideation.**

**Essential Steps**:
1. Research via Perplexity/Brave/context7
2. `Skill("superpowers:brainstorming")` - Explore 2-3 alternative approaches
3. For complex architectures: `/parallel-solutioning` - Deploys 7 solution-architects
4. Convert design to implementation steps via `Skill("superpowers:writing-plan")`

**Outputs**: **PRD** (business goals, user stories, architectural decisions, epics list)
- PRD template: `.taskmaster/templates/prd-template.md`
- PRD location: `.taskmaster/docs/PRD-{CATEGORY}-{DESCRIPTOR}.md`
- PRD is the operator-facing artifact — it does NOT go into Task Master directly
- Store research notes and decisions in Hindsight

---

### Epic Hierarchy Patterns (MANDATORY)

**Every initiative requires this hierarchy. No exceptions.**

```
UBER-EPIC: "Q1 Authentication System"
│
├── EPIC: User Login Flow ─────────────────┐
│   ├── TASK: Implement login API          │ [parent-child]
│   ├── TASK: Create login form            │ Concurrent work OK
│   └── TASK: Add validation               │
│                                          │
├── EPIC: AT-User Login Flow ──────────────┤ [blocks]
│   ├── TASK: Unit tests for login API     │ AT blocks functional epic
│   ├── TASK: E2E test login flow          │
│   └── TASK: API integration tests        │
│                                          │
├── EPIC: Session Management ──────────────┤
│   ├── TASK: Implement session store      │ [parent-child]
│   └── TASK: Add session timeout          │
│                                          │
└── EPIC: AT-Session Management ───────────┘ [blocks]
    └── TASK: Session validation tests
```

**Quick Setup**:
```bash
# 1. Create uber-epic (ALWAYS FIRST)
bd create --title="Q1 Authentication System" --type=epic --priority=1
# Returns: my-project-001

# 2. Create functional epic + paired AT epic
bd create --title="User Login Flow" --type=epic --priority=2           # my-project-002
bd create --title="AT-User Login Flow" --type=epic --priority=2        # my-project-003
bd dep add my-project-002 my-project-003 --type=blocks                   # AT blocks functional

# 3. Create tasks under each epic
bd create --title="Implement login API" --type=task --priority=2
bd dep add my-project-004 my-project-002 --type=parent-child             # Task under epic
```

**Dependency Types**:
| Type | Purpose | Blocks `bd ready`? | Use For |
|------|---------|-------------------|---------|
| `parent-child` | Organizational grouping | ❌ No | Uber-epic→Epic, Epic→Task |
| `blocks` | Sequential requirement | ✅ Yes | AT-epic→Functional-epic, Task→Task |

**Key Rules**:
- **Uber-Epic First**: Create before any planning work
- **AT Pairing**: Every functional epic MUST have a paired AT epic
- **Closure Order**: AT tasks → AT epic → Functional epic → Uber-epic
- **Concurrent Development**: `parent-child` allows ALL epics to progress simultaneously

**Validation**: Each AT task must pass 3-level validation (Unit + API + E2E). See [WORKFLOWS.md](WORKFLOWS.md#validation-protocol-3-level).

**Quick Reference**: [REFERENCE.md](REFERENCE.md#epic-hierarchy)

---

### Phase 1: Planning (Uber-Epic + Task Decomposition)

**Prerequisites**:
1. ✅ Phase 0 complete (ideation, brainstorming done)
2. ✅ PRD exists in `.taskmaster/docs/PRD-{CATEGORY}-{DESCRIPTOR}.md` (from Phase 0)
3. ✅ Read [WORKFLOWS.md](WORKFLOWS.md#feature-decomposition-maker) for MAKER decomposition principles

**Two-Document Model**:
- **PRD** (Phase 0 output) — business artifact: goals, user stories, architectural decisions, epics list. NOT fed into Task Master.
- **SD** (Phase 1 creates, one per epic) — automation input: business context + technical design. This is what Task Master parses.

**Planning Workflow**:
```bash
# 1. Create uber-epic in my-org/ (from validated PRD)
cd $CLAUDE_PROJECT_DIR
bd create --title="[Initiative from PRD]" --type=epic --priority=1
# Note the returned ID (e.g., my-project-001)

# 2. Create Solution Design (SD) per epic from PRD
#    Delegate to solution-design-architect worker — do NOT write SD yourself
#    SD template: .taskmaster/templates/solution-design-template.md
#    SD location: .taskmaster/docs/SD-{CATEGORY}-{NUMBER}-{epic-slug}.md
#    The SD includes:
#      - Business Context section (summarizes relevant PRD goals for Task Master)
#      - Technical Architecture (data models, API contracts, component design)
#      - Functional Decomposition (capabilities → features with explicit dependencies)
#      - Acceptance Criteria per feature (Gherkin-ready)
#      - File Scope (new/modified/excluded files)

# 2.5a. Codebase Analysis with ZeroRepo (Recommended — run before writing SD)
# For detailed workflow, see ZEROREPO.md
#
# Run ZeroRepo to map PRD against existing codebase:
python .claude/skills/orchestrator-multiagent/scripts/zerorepo-run-pipeline.py \
  --operation init --project-path .  # Once per project
python .claude/skills/orchestrator-multiagent/scripts/zerorepo-run-pipeline.py \
  --operation generate --prd .taskmaster/docs/PRD-{ID}.md \
  --baseline .zerorepo/baseline.json --model claude-sonnet-4-6 \
  --output .zerorepo/output
# Read delta report: .zerorepo/output/05-delta-report.md
# Use EXISTING/MODIFIED/NEW classification to populate SD File Scope section:
#   EXISTING → Reference only (no task needed)
#   MODIFIED → Scoped task with file path + specific changes
#   NEW      → Full implementation task with module structure
# Include delta context in SD Functional Decomposition and File Scope sections

# 2.5b. Enrich Beads with RPG Graph Context (After sync in step 5)
# For each bead created by sync, update --design with context from 04-rpg.json:
# bd update <bead-id> --design "Delta: NEW | Files: ... | Interface: ... | Dependencies: ..."
# See ZEROREPO.md "Enriching Beads with RPG Graph Context" for full pattern

# 3. Note current highest task ID before parsing
task-master list | tail -5  # e.g., last task is ID 170

# 4. Parse SD with Task Master (--append if tasks exist)
#    NOTE: Parse the SD, NOT the PRD — SD has the structured decomposition TM needs
task-master parse-prd .taskmaster/docs/SD-{CATEGORY}-{NUMBER}-{epic-slug}.md --research --append
task-master analyze-complexity --research
task-master expand --all --research
# Note the new ID range (e.g., 171-210)

# 5. Sync ONLY new tasks to Beads (run from my-org/ root!)
cd $CLAUDE_PROJECT_DIR
node my-project/.claude/skills/orchestrator-multiagent/scripts/sync-taskmaster-to-beads.js \
    --uber-epic=my-project-001 \
    --from-id=171 --to-id=210 \
    --tasks-path=my-project/.taskmaster/tasks/tasks.json
# This also closes Task Master tasks 171-210 (status=done)

# 6. Generate acceptance tests from SD (IMMEDIATELY after sync)
#    Use SD as source — it contains Business Context + per-feature Acceptance Criteria
Skill("acceptance-test-writer", args="--prd=PRD-AUTH-001 --source=.taskmaster/docs/SD-AUTH-001-login.md")
# This generates:
# acceptance-tests/PRD-AUTH-001/
# ├── manifest.yaml          # PRD metadata + feature list
# ├── AC-user-login.yaml     # Acceptance criteria (from SD Section 6)
# ├── AC-invalid-credentials.yaml
# └── ...

# 7. Commit acceptance tests
git add acceptance-tests/ && git commit -m "test(PRD-AUTH-001): add acceptance test suite"

# 7.5. Generate DOT pipeline from beads (beads must exist from step 5)
# Set solution_design attribute on each codergen node to point to its SD file
cobuilder pipeline create \
    --prd PRD-AUTH-001 \
    --output .pipelines/pipelines/auth-001.dot
# Set SD reference on nodes (so Runner can brief orchestrators with full context):
cobuilder pipeline node-modify auth-001.dot impl_login \
    --set solution_design=.taskmaster/docs/SD-AUTH-001-login.md
# Validate
cobuilder pipeline validate \
    .pipelines/pipelines/auth-001.dot

# 8. Review hierarchy (filter by uber-epic)
bd list --parent=my-project-001   # See only tasks under this initiative
bd ready --parent=my-project-001  # Ready tasks for this initiative only

# 9. Commit planning artifacts (completes Phase 1)
git add .beads/ .taskmaster/docs/ .pipelines/pipelines/ && \
    git commit -m "plan: initialize [initiative] hierarchy with SD documents"
# Write progress summary to .claude/progress/
```


---

**Manual Planning** (Hotfixes only - already have clear scope):
```bash
bd create --title="[Hotfix Description]" --type=epic --priority=1
# Create tasks directly: bd create --title="[Task]" --type=task
# Skip Phase 0 only for emergency fixes with <3 file changes
```

**Warning: Ignore plan skill's "execute with superpowers:executing-plans"** -- we use native Agent Teams teammates.

---

### Sync Script Reference (Task Master → Beads)

**🚨 Run from project root** (e.g., `my-org/`) to use the correct `.beads` database.

```bash
node my-project/.claude/skills/orchestrator-multiagent/scripts/sync-taskmaster-to-beads.js \
    --uber-epic=<id> --from-id=<start> --to-id=<end> --tasks-path=<path>
```

**Key flags**: `--uber-epic` (links to parent), `--from-id`/`--to-id` (filter range), `--dry-run` (preview)

**After Sync**:
- ✅ Creates beads with rich field mapping (description, design, acceptance)
- ✅ Links all beads to uber-epic via parent-child
- ✅ Closes synced Task Master tasks (status=done)
- ✅ Filter by initiative: `bd ready --parent=my-project-001`

### Phase 2: Execution (Incremental Implementation)

**🚨 For multi-feature autonomous operation, see [WORKFLOWS.md](WORKFLOWS.md#autonomous-mode-protocol)**

The autonomous mode protocol provides:
- ✅ Continuation criteria (when to proceed automatically)
- ✅ Stop conditions (when to pause and report)
- ✅ Comprehensive validation (Unit + API + E2E for backend and frontend)
- ✅ Session handoff procedures

**Quick Reference (Single Feature)**:
```
1. Run PREFLIGHT.md checklist (includes team creation)
   ↓
2. `bd ready` -> Select next task
   ↓
3. `bd update <bd-id> --status in-progress`
   ↓
4. DELEGATE TO WORKER TEAMMATE
   TaskCreate(subject="Implement ...", description="...", activeForm="...")
   SendMessage(type="message", recipient="worker-backend", content="Task available", summary="New task")
   ↓
5. Worker sends results via SendMessage (auto-delivered to you)
   ↓
6. Mark impl_complete
   bd update <bd-id> --status=impl_complete
   ↓
7. `git add . && git commit -m "feat(<bd-id>): [description]"`
```

**Critical Rules**:
- One feature at a time. Leave clean state. Commit progress.
- **Use TaskCreate + SendMessage for all worker delegation** - Workers claim tasks from shared TaskList
- **NEVER use `bd close` directly** - Mark `impl_complete` and let S3 validate/close
- Orchestrator coordinates; Workers implement

**Legacy feature_list.json**: See [LEGACY_FEATURE_LIST.md](archive/LEGACY_FEATURE_LIST.md) for legacy workflow.

### Phase 3: Validation (System 3 Independent Oversight)

**System 3 handles validation independently** using its oversight team:
- s3-investigator verifies code changes
- s3-prd-auditor checks PRD coverage
- s3-validator runs real E2E tests
- s3-evidence-clerk produces closure reports

**Orchestrator's role in Phase 3:**
1. Ensure all tasks are marked `impl_complete`
2. Monitor for `s3_rejected` tasks (fix and re-submit)
3. When all tasks are `closed` by S3 → initiative complete

**Closure Order** (managed by System 3):
```
impl_complete → s3_validating → closed
                (or s3_rejected → in_progress → impl_complete)
```

**Full Validation Protocol**: See [WORKFLOWS.md](WORKFLOWS.md#validation-protocol-3-level)

---

## State Integrity Principles

**State = What can be independently verified** (tests, browser, git status).

**Immutability Rules**:
| ✅ Allowed | ❌ Never |
|-----------|---------|
| Change status (open → closed) | Remove tasks |
| Add timestamps/evidence | Edit task definitions after creation |
| Add discovered subtasks | Reorder task hierarchy |

**MAKER-Inspired Decomposition**: Tasks must be small enough for a Haiku model to complete reliably. See [WORKFLOWS.md](WORKFLOWS.md#feature-decomposition-maker) for the four questions and decision tree.

---

## Memory-Driven Decision Making

**Core principle**: Before deciding, recall. After learning, retain. When stuck, reflect + validate.

Key integration points: task start (recall), user feedback (retain → reflect → retain), double-rejection (recall → reflect → Perplexity → retain), session closure (reflect → retain).

**Full workflow**: See [references/hindsight-integration.md](references/hindsight-integration.md)

---

## Worker Delegation (Native Teams)

**Orchestrators use native Agent Teams for all worker delegation.**

**Essential pattern**: Create team → Spawn workers → Create tasks → Workers claim and report

```python
# Spawn worker teammate (once per session in PREFLIGHT)
Task(
    subagent_type="backend-solutions-engineer",
    team_name="{initiative}-workers",
    name="worker-backend",
    prompt="Check TaskList, claim tasks, implement, report via SendMessage"
)

# Assign work
TaskCreate(subject="Implement X", description="...", activeForm="Implementing X")
SendMessage(type="message", recipient="worker-backend", content="Task available", summary="New task")
```

### Quick Worker Selection

| Feature Type | subagent_type | Teammate Name |
|--------------|---------------|---------------|
| React, UI | `frontend-dev-expert` | `worker-frontend` |
| API, Python | `backend-solutions-engineer` | `worker-backend` |
| **E2E Browser Tests** | **`tdd-test-engineer`** | **`worker-tester`** |
| Architecture | `solution-design-architect` | `worker-architect` |
| Investigation | `Explore` | `worker-explore` |

**Full examples**: See [WORKERS.md](WORKERS.md) for detailed patterns

### Browser Testing Worker Pattern

**When to use**: Features requiring actual browser automation (not just unit tests)

**Pattern**: Orchestrator creates task, persistent tdd-test-engineer teammate picks it up. Because the tester is a persistent teammate, it can maintain browser sessions across multiple test tasks.

```python
# Create browser testing task
TaskCreate(
    subject="E2E browser testing for F084",
    description="""
    MISSION: Validate feature F084 via browser automation

    TARGET: http://localhost:5001/[path]

    TESTING CHECKLIST:
    - [ ] Navigate to page
    - [ ] Verify UI renders correctly
    - [ ] Test user interactions
    - [ ] Capture screenshots as evidence

    Report: Pass/Fail per item, screenshots, overall assessment
    """,
    activeForm="Browser testing F084"
)
SendMessage(type="message", recipient="worker-tester", content="Browser test task available for F084", summary="Browser test request")
# Worker-tester picks up task, maintains browser session, reports results via SendMessage
```

### Fallback: Task Subagent Mode

**When AGENT_TEAMS is not enabled**, fall back to the original Task subagent pattern:

```python
result = Task(
    subagent_type="frontend-dev-expert",
    description="Implement [feature]",
    prompt="""
    ## Task: [Task title from Beads]

    **Context**: [investigation summary]
    **Requirements**: [list requirements]
    **Acceptance Criteria**: [list criteria]
    **Scope** (ONLY these files): [file list]

    **Report back with**: Files modified, tests written/passed, any blockers
    """
)
# Result returned directly - no monitoring, no cleanup needed
```

In fallback mode, after implementation the orchestrator marks tasks `impl_complete`:
```bash
bd update <bd-id> --status=impl_complete
```

**How to detect**: Check for `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in environment. If absent, use fallback.

**Full Guide**: [WORKERS.md](WORKERS.md)
- Worker Assignment Template
- Parallel Worker Pattern
- Browser Testing Workers (E2E validation)

---

## Service Management

**BEFORE starting Phase 2:**

```bash
# Start services (see VALIDATION.md for details)
cd my-project-backend && ./start_services.sh
cd my-project-frontend && npm run dev

# Verify services running
lsof -i :5001 -i :8000 -i :5184 -i :5185 | grep LISTEN
```

**Full Guide**: [VALIDATION.md](VALIDATION.md#service-management)
- Service Setup and Health Checks
- Starting from Clean State
- Worker Dependency Verification
- Troubleshooting Service Issues

---

## Testing & Validation

### Testing (Level 1 — Orchestrator Responsibility)

Orchestrators ensure basic quality before marking `impl_complete`:
- Unit tests pass (pytest/jest)
- Code compiles/builds without errors
- Basic smoke tests pass

**Level 2+3 validation (E2E, PRD compliance) is performed independently by System 3's oversight team.**
The orchestrator does NOT need to set up E2E infrastructure or run acceptance tests.

### Validation Types

| Type | When | How |
|------|------|-----|
| `browser` | UI features | chrome-devtools automation |
| `api` | Backend endpoints | curl/HTTP requests |
| `unit` | Pure logic | pytest/jest |

**Full Guide**: [VALIDATION.md](VALIDATION.md)
- 3-Level Validation Protocol
- Testing Infrastructure
- Hollow Test Problem explanation

---

## Mandatory Regression Check (CIRCUIT BREAKER)

**🚨 This is covered in [PREFLIGHT.md](PREFLIGHT.md) Phase 3.**

**Quick Summary**: Before ANY new feature work:
1. Pick 1-2 closed tasks (`bd list --status=closed`)
2. Run 3-level validation (Unit + API + E2E)
3. If ANY fail: `bd reopen <id>` and fix BEFORE new work

**Why It Matters**: Hidden regressions multiply across features. Session F089-F090 evidence shows regression checks prevented 3+ hour blockages.

**Full Validation Protocol**: See [WORKFLOWS.md](WORKFLOWS.md#validation-protocol-3-level)

**Failure Recovery**: [VALIDATION.md](VALIDATION.md#recovery-patterns)

---

## Progress Tracking

### Session Handoff Checklist

**Before Ending:**
1. ✅ Current feature complete or cleanly stopped
2. ✅ Beads state synced (`bd sync`)
3. ✅ Progress summary updated (`.claude/progress/`)
4. ✅ Git status clean, changes committed and pushed
5. ✅ Learnings stored in Hindsight (`mcp__hindsight__retain()`)

**Starting New:**
1. Run PREFLIGHT.md checklist (includes memory check)
2. `bd ready` to find next available work
3. Review task details with `bd show <id>`
4. Continue with Phase 2 workflow

**Full Guide**: [WORKFLOWS.md](WORKFLOWS.md#progress-tracking)
- Session Summary template
- Progress Log template
- Learnings Accumulation
- Handoff procedures

---

## Quick Troubleshooting

### Worker Red Flags

| Signal | Action |
|--------|--------|
| Modified files outside scope | Reject - Fresh retry |
| TODO/FIXME in output | Reject - Fresh retry |
| Validation fails | Reject - Fresh retry |
| Exceeds 2 hours | Stop - Re-decompose |

### Orchestrator Self-Check

**Before Starting Phase 1 (Planning):**
- ✅ Completed Phase 0 (Ideation)?
- ✅ Read WORKFLOWS.md Feature Decomposition section?
- ✅ Created TodoWrite checklist for Phase 1?
- ✅ Used MAKER checklist to evaluate approach?
- ✅ Chose correct workflow (Task Master vs Manual)?

**After each feature:**
- Did I use **TaskCreate + SendMessage** for worker delegation (or Task subagent fallback)?
- Ran regression check first?
- Worker stayed within scope?
- Validated feature works (not just tests pass)?
- **Marked impl_complete (`bd update <bd-id> --status=impl_complete`)?**
- Committed with message?
- Git status clean?

**Pattern**: All worker delegation uses native Agent Teams (TaskCreate + SendMessage to teammates). When AGENT_TEAMS is not enabled, fall back to `Task(subagent_type="...")`.

**Full Guide**: [VALIDATION.md](VALIDATION.md#troubleshooting)
- Worker Red Flags & Recovery
- Orchestrator Anti-Patterns
- Hollow Test Problem
- Voting Protocol (when consensus needed)
- Recovery Patterns

---

## Graph Editing Workflow

Orchestrators use the attractor CLI CRUD commands to build and maintain pipeline graphs.

### Command Reference

| Command | Description |
|---------|-------------|
| `cli.py node <file> list [--output json]` | List all nodes in the pipeline |
| `cli.py node <file> add <id> --handler <type> --label "..." [--set key=value ...]` | Add a new task node |
| `cli.py node <file> modify <id> --set key=value ... [--dry-run]` | Update node attributes |
| `cli.py node <file> remove <id> [--dry-run]` | Remove a node (cascades edge removal) |
| `cli.py edge <file> list [--output json]` | List all edges in the pipeline |
| `cli.py edge <file> add <src> <dst> [--label "..."] [--condition pass\|fail\|partial]` | Add a dependency edge |
| `cli.py edge <file> remove <src> <dst> [--condition ...] [--label ...]` | Remove matching edge(s) |
| `cli.py generate --scaffold --prd <PRD-REF> [--output file.dot]` | Scaffold initial graph from PRD |
| `cli.py validate <file>` | Validate graph structure and constraints |

### Typical Workflow

1. **Scaffold**: `cli.py generate --scaffold --prd PRD-XXX-001 --output pipeline.dot`
2. **Populate**: Add task nodes with `node add`, connect with `edge add`
3. **Validate**: `cli.py validate pipeline.dot` after each batch of changes
4. **Iterate**: Modify status with `node modify --set status=active`, remove obsolete nodes/edges as scope evolves

### Notes

- `--dry-run` is available on all mutating commands (add, remove, modify)
- `--output json` is available on list/add/remove for machine-readable output
- `node remove` automatically removes all edges referencing the deleted node
- All mutations append to `<file>.ops.jsonl` for audit trail

### Pipeline Status & Transition Tracking

After building and validating a pipeline graph, orchestrators track execution progress using the status, transition, and checkpoint commands.

#### Status Commands

```bash
# Full status overview with node distribution
cobuilder pipeline status pipeline.dot --json --summary

# Human-readable status table
cobuilder pipeline status pipeline.dot

# JSON output for programmatic consumption
cobuilder pipeline status pipeline.dot --json
```

#### Transition Commands

Advance nodes through the lifecycle: `pending` → `active` → `impl_complete` → `validated` (or `failed` → `active` retry).

```bash
# Mark a node as active (implementation started)
cobuilder pipeline transition pipeline.dot impl_auth active

# Mark implementation complete (triggers paired validation gate)
cobuilder pipeline transition pipeline.dot impl_auth impl_complete

# Mark validated after passing acceptance criteria
cobuilder pipeline transition pipeline.dot val_auth validated

# Retry on failure — transition back to active
cobuilder pipeline transition pipeline.dot impl_auth active
```

#### Checkpoint Commands

Save and restore graph state as a safety net during complex transitions.

```bash
# Save current state before a batch of transitions
cobuilder pipeline checkpoint-save pipeline.dot

# Checkpoint after every transition (recommended)
cobuilder pipeline transition pipeline.dot node_x active && \
cobuilder pipeline checkpoint-save pipeline.dot
```

#### Transition Best Practices

- **Always checkpoint** after transitions — enables rollback if downstream work fails
- **Validate after transitions**: `cobuilder pipeline validate pipeline.dot`
- **Check status before dispatch**: Ensure upstream dependencies are `validated` before transitioning a node to `active`
- **Report transitions to System 3** after `impl_complete` (via `bd update <bd-id> --status=impl_complete`)

### Pipeline Dashboard & Progress

Use the dashboard for a unified view of initiative progress across all lifecycle stages.

```bash
# Human-readable progress table
cobuilder pipeline status pipeline.dot --summary

# JSON output for programmatic consumption
cobuilder pipeline status pipeline.dot --json --summary
```

#### Dashboard Output Includes

- **Pipeline stage**: Definition / Implementation / Validation / Finalized
- **Node status distribution**: pending / active / impl_complete / validated / failed
- **Dependency readiness**: Which nodes have all upstream dependencies met
- **Progress percentage**: Validated nodes vs total implementation nodes

#### Integration with Orchestrator Workflow

1. **Before Phase 3 (Execution)**: Check dashboard to identify dispatchable nodes
2. **During Execution**: Monitor after each worker completion to track progress
3. **After Validation**: Verify all hexagon gates show `validated` before signaling finalization

```bash
# Check if all validation gates are validated (finalize-ready)
cobuilder pipeline status pipeline.dot --json | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print('READY' if all(n['status']=='validated' for n in d.get('nodes',[]) if n.get('shape')=='hexagon') else 'NOT_READY')"
```

#### Progress Tracking Across Sessions

Status is persisted in the DOT file itself. After context compaction or session restart:
1. Re-read pipeline status: `cobuilder pipeline status pipeline.dot --summary`
2. Resume from last checkpoint if needed
3. Continue dispatching from where the previous session left off

---

## Reference Guides

### When to Consult Each Guide

**Quick Lookup:**
- **[REFERENCE.md](REFERENCE.md)** - Commands, ports, directories, session templates

**Session Start (MANDATORY):**
- **[PREFLIGHT.md](PREFLIGHT.md)** - 🚨 MANDATORY - Unified pre-flight checklist consolidating all circuit breakers (Serena, services, memory, regression)

**During Ideation + Planning (Phase 0-1):**
- **[WORKFLOWS.md](WORKFLOWS.md#feature-decomposition-maker)** - 🚨 MANDATORY READ before Phase 1 - Contains MAKER checklist, decision tree, red flags
- **[ZEROREPO.md](ZEROREPO.md)** - Codebase analysis with ZeroRepo. Delta classification (EXISTING/MODIFIED/NEW), CLI commands, troubleshooting, worker context enrichment

**During Execution (Phase 2):**
- **[WORKFLOWS.md](WORKFLOWS.md)** - 4-Phase Pattern, Autonomous Mode Protocol, Validation (Unit + API + E2E), Progress Tracking, Session Handoffs
- **[WORKERS.md](WORKERS.md)** - Launching workers, monitoring, feedback, browser testing
- **[VALIDATION.md](VALIDATION.md)** - Service startup, health checks, testing infrastructure, troubleshooting, recovery patterns

**Session Boundaries:**
- **[WORKFLOWS.md](WORKFLOWS.md#session-handoffs)** - Handoff checklists, summaries, learning documentation

**Memory:**
- **[references/hindsight-integration.md](references/hindsight-integration.md)** - Memory-driven decision making, learning loops, feedback patterns

**Legacy Support:**
- **[LEGACY_FEATURE_LIST.md](archive/LEGACY_FEATURE_LIST.md)** - Archived feature_list.json documentation for migration

---

**Skill Version**: 5.3 (Progressive Disclosure Streamlining)
**Progressive Disclosure**: 8 reference files for detailed information
**Last Updated**: 2026-02-08
**Latest Enhancements**:
- v5.3: **Progressive Disclosure Streamlining** - Reduced SKILL.md from 6,473 to ~3,800 words (~41% reduction). Moved Memory-Driven Decision Making (~600 words) to reference file (references/hindsight-integration.md). Compressed Phase 0 Ideation, Sync Script, Worker Delegation, and Testing & Validation sections. Removed duplicate Acceptance Test Generation subsection (already in Phase 1 workflow). All writing converted to imperative/infinitive form (no second-person).
- v5.2: **Bead Enrichment from RPG Graph** - Added Phase 1.5 workflow to inject 04-rpg.json context into beads after Task Master sync. New "Enriching Beads with RPG Graph Context" section in ZEROREPO.md documents the enrichment pattern with real examples. Updated model from claude-sonnet-4-20250514 to claude-sonnet-4-5-20250929. Step 2.5 now split into 2.5a (generate delta) and 2.5b (enrich beads). Workers receive implementation-ready specs with file paths, interfaces, and technology stacks extracted from RPG graph.
- v5.1: **ZeroRepo Integration** - Added codebase-aware orchestration via ZeroRepo delta analysis. New Step 2.5 in Phase 1 planning runs `zerorepo init` + `zerorepo generate` to classify PRD components as EXISTING/MODIFIED/NEW. Delta context enriches worker task assignments with precise file paths and change summaries. New ZEROREPO.md reference guide. Three wrapper scripts (`zerorepo-init.sh`, `zerorepo-generate.sh`, `zerorepo-update.sh`). Codebase-Aware Task Creation workflow added to WORKFLOWS.md.
- v5.0: **Native Agent Teams** - Replaced Task subagent worker delegation with native Agent Teams (Teammate + TaskCreate + SendMessage). Workers are now persistent teammates that claim tasks from a shared TaskList, communicate peer-to-peer, and maintain session state across multiple assignments. Validator is a team role (not a separate Task subagent). Worker communication uses native team inboxes. Fallback to Task subagent mode when AGENT_TEAMS is not enabled.
- v4.0: **Task-Based Worker Delegation** - Replaced tmux worker delegation with Task subagents. Workers now receive assignments via `Task(subagent_type="...")` and return results directly. No session management, monitoring loops, or cleanup required. Parallel workers use `run_in_background=True` with `TaskOutput()` collection. System 3 -> Orchestrator still uses tmux for session isolation; Orchestrator -> Worker now uses Task subagents.
- v3.13: 🆕 **Sync Script Finalization** - Sync script now auto-closes Task Master tasks after sync (status=done). Removed mapping file (redundant with beads hierarchy). **IMPORTANT**: Must run from `my-org/` root to use correct `.beads` database. Updated all docs with correct paths and `--tasks-path` usage.
- v3.12: **ID Range Filtering** - `--from-id=<id>` and `--to-id=<id>` to filter which Task Master tasks to sync. Essential for multi-PRD projects.
- v3.11: **Enhanced Sync Script** - `--uber-epic=<id>` for parent-child linking. Auto-maps description, details→design, testStrategy→acceptance.
- v3.10: **Reference Consolidation** - Created REFERENCE.md as quick reference card. Merged BEADS_INTEGRATION.md, README.md, and ORCHESTRATOR_INITIALIZATION_TEMPLATE.md into REFERENCE.md. Reduced reference files from 6 to 5. Essential commands, patterns, and session templates now in single quick-lookup location.
- v3.9: **Validation Consolidation** - Merged TESTING_INFRASTRUCTURE.md, TROUBLESHOOTING.md, and SERVICE_MANAGEMENT.md into unified VALIDATION.md. Reduced reference files from 8 to 6. All testing, troubleshooting, and service management now in single location.
- v3.8: **Workflow Consolidation** - Merged AUTONOMOUS_MODE.md, ORCHESTRATOR_PROCESS_FLOW.md, FEATURE_DECOMPOSITION.md, and PROGRESS_TRACKING.md into unified WORKFLOWS.md. Reduced reference files from 11 to 8. All workflow documentation now in single location.
- v3.7: Removed legacy inter-instance messaging (replaced by beads status updates).
- v3.6: **Memory-Driven Decision Making** - Integrated Hindsight for continuous learning. Task start recall, user feedback loop (retain → reflect → retain), double-rejection analysis with Perplexity validation, hollow test prevention, session closure reflection. Creates learning loop where each task benefits from all previous experience.
- v3.5: Clear four-phase pattern (Phase 0: Ideation → Phase 1: Planning → Phase 2: Execution → Phase 3: Validation). Consolidated Uber-Epic and AT-Epic patterns into unified "Epic Hierarchy Patterns" section with cleaner visual. Updated all phase references for consistency.
- v3.4: Beads-only workflow - Removed ALL feature_list.json references (now in LEGACY_FEATURE_LIST.md). Added MANDATORY Ideation Phase with brainstorming + parallel-solutioning.
- v3.3: Major streamlining - Created PREFLIGHT.md (unified session checklist), AUTONOMOUS_MODE.md (multi-feature protocol with 3-level validation), LEGACY_FEATURE_LIST.md (archived legacy docs).
- v3.2: Added Mandatory Acceptance Test Epic Pattern - every functional epic requires a paired AT epic with blocking dependency.
- v3.1: Added Uber-Epic First Pattern - mandatory hierarchy (uber-epic → epic → task) for all initiatives.
- v3.0: Added Beads task management integration as recommended state tracking method.
