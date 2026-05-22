---
name: beads-plan
description: Transform project specifications into executable beads dependency graphs with proper decomposition, dependency mapping, and validation. Use when starting new projects, breaking down epics, planning multi-step work, or when asked to create a beads implementation plan.
---

# Beads Planning Skill

## What This Skill Does

This skill guides the transformation of project specifications into instantiated beads dependency graphs. A well-planned beads implementation creates an executable DAG (directed acyclic graph) where each bead (issue) has clear boundaries, explicit inputs/outputs, and testable success criteria.

### Integration with Org-mode Planning Layer

Beads operates as the **execution layer** in a layered planning architecture:

```
┌─────────────────────────────────────────────┐
│  PLANNING LAYER (Org-mode)                  │
│  - Human-visible project state              │
│  - Strategic decomposition                  │
└─────────────────────────────────────────────┘
                     │
       [spawn-to-beads: Task Spawns Epic]
                     ▼
┌─────────────────────────────────────────────┐
│  EXECUTION LAYER (Beads) ← YOU ARE HERE     │
│  - Agent-executable decomposition           │
│  - Swarm coordination and claiming          │
└─────────────────────────────────────────────┘
                     │
       [complete-to-org: Epic Completes]
                     ▼
┌─────────────────────────────────────────────┐
│  PLANNING LAYER (Org-mode) - State Updated  │
└─────────────────────────────────────────────┘
```

**Key Integration Points:**
- Epics may be spawned from org-mode tasks via `spawn-to-beads` skill
- Such epics have a `source_org_id` reference in their description
- When these epics complete, `complete-to-org` skill updates the source org task

### What Beads Planning Offers

1. **Explicit dependency graph** - Forces architectural clarity upfront
2. **Bounded units** - Each bead has clear inputs/outputs/success criteria
3. **Parallelization** - Independent beads can execute concurrently
4. **Integration contracts** - Boundaries are explicit and testable
5. **Fault isolation** - One bead's failure doesn't corrupt others
6. **Ready work detection** - `bd ready` shows unblocked work
7. **Progress visibility** - Dependency tree shows completion state

## Prerequisites

- `bd` CLI installed (`npm install -g @beads/bd` or `brew install steveyegge/beads/bd`)
- Repository initialized with `bd init` (run once per project)
- Working directory is within a git repository
- For iterative changes: Planning Context Snapshot recommended (see `iterative-planning-context` skill)

---

## Quick Start

For a simple project, the workflow is:

```bash
# 1. Create the epic (top-level container)
bd create "My Project Epic" -t epic -p 1 -d "Description of the overall goal"

# 2. Create tasks as children of the epic (auto-generates hierarchical IDs)
bd create "First task" -t task -p 2 --parent bd-XXXX
bd create "Second task" -t task -p 2 --parent bd-XXXX

# 3. Add blocking dependencies between tasks
bd dep add bd-XXXX.2 bd-XXXX.1  # Task 2 depends on Task 1

# 4. Validate the plan
bd ready          # Should show Task 1 as ready
bd dep tree bd-XXXX   # Visualize the dependency graph
bd dep cycles     # Should return empty (no cycles)
```

For complex projects, follow the five phases below. The phases are internal reasoning steps—work through them continuously and present the instantiated result. Only pause for user input when the specification has genuine ambiguity that blocks progress.

---

## Spawned Epics (from Org-mode)

When an epic is created via the `spawn-to-beads` skill from an org-mode task, special handling applies:

### Identifying Spawned Epics

Spawned epics include a source reference in their description:

```bash
# Epic created with source reference
bd create "Implement Authentication" -t epic -p 1 \
  -d "[source_org_id: task-implement-auth] Full description here..."
```

The `source_org_id` marker links this epic back to the originating org-mode task.

### Completion Callback Protocol

When closing an epic that has a `source_org_id`:

1. **Check for source reference** in epic description:
   ```bash
   bd show <epic-id> --json | jq -r '.description' | grep -o 'source_org_id: [^]]*'
   ```

2. **Verify 100% completion** (all child beads closed):
   ```bash
   bd epic status <epic-id>
   ```

3. **Trigger complete-to-org skill** to update the org-mode task:
   - The org task transitions from WAITING to DONE
   - The DELEGATED_TO property may be cleared or annotated

4. **Then close the epic**:
   ```bash
   bd close <epic-id> -r "All tasks complete. Org task updated."
   ```

**Important:** Always trigger the org callback BEFORE closing the epic, so the source reference is still accessible.

### Non-Spawned Epics

Epics created directly (without org source) follow normal workflow with no callback required.

**However**, direct epic creation violates org-mode coherence. See "Org-Mode Coherence" section below.

---

## Org-Mode Coherence

**Architectural Principle:** Org-mode is the canonical planning layer. All work SHOULD originate from org-mode.

### Why Coherence Matters

When epics are created without org source:
- Planning layer (org-mode) doesn't reflect actual work
- No bidirectional traceability
- Weekly reviews miss work in progress
- Completion callbacks cannot update planning state

### Creating Epics

**RECOMMENDED: Spawn from org-mode**

Use `spawn-to-beads` skill to create epic from org task:
```bash
# 1. Have org task ready
# 2. Use spawn-to-beads skill (establishes bidirectional refs)
# 3. Result: epic has source_org_id, org task has DELEGATED_TO
```

**TACTICAL EXCEPTION: Direct creation**

Creating epics directly is permitted but produces a warning:
```bash
# Before: bd create "Epic Title" -t epic -p 1 -d "Description"
# 
# Ask yourself:
# - Is this genuinely ad-hoc work?
# - Should an org task exist for this work?
# - Will I remember to update org-mode when complete?
#
# If creating without org source, acknowledge the deviation:
echo "WARNING: Creating epic without org source. Org-mode coherence violated."
```

### Coherence Check (Phase 4)

During instantiation, before creating the epic:

1. **Check for org source**: Does this work have an org task?
2. **If yes**: Use `spawn-to-beads` skill instead of direct creation
3. **If no**: 
   - Consider creating org task first (recommended)
   - Or proceed with warning (tactical exception)

### Retroactive Sync

If an epic was created without org source and should be tracked:

1. Create corresponding org task in appropriate project
2. Set org task to WAITING state
3. Add `DELEGATED_TO` property pointing to existing epic ID
4. Edit epic description to include `[source_org_id: <org-id>]` marker

This restores bidirectional traceability but is more work than doing it right initially.

---

## Context-Aware Planning (Iterative Changes)

When planning changes to an **existing codebase** (vs greenfield), leverage Planning Context Snapshots for better decomposition.

### Check for Existing Context

Before starting Phase 1, check if a Planning Context Snapshot exists:

```bash
ls docs/planning/context-*.md 2>/dev/null
```

If found, read it first - it contains:
- **Structure Map**: Where new code should live
- **Conventions**: Patterns to follow (naming, error handling, tests)
- **Integration Points**: What existing code to touch
- **Core Abstractions**: Types/traits to extend or use

### Using Context During Decomposition

**Phase 1 Enhancement** - Use context to:
- Verify scope against documented structure
- Identify integration points from context rather than exploring
- Check for existing planning state (related work, blockers)

**Phase 2 Enhancement** - Use context for better beads:
- Match file locations to "Adding New Code" table
- Follow documented naming conventions in bead titles
- Reference existing patterns in acceptance criteria
- Add integration beads for documented touch points

**Phase 3 Enhancement** - Use context for dependencies:
- Dependencies on documented integration points become explicit beads
- Test patterns inform test bead structure
- Build/deploy patterns inform chore beads

### Context-Informed Bead Anatomy

When context exists, beads should reference it:

| Field | Context Enhancement |
|-------|---------------------|
| **Title** | Use naming conventions from context |
| **Description** | Reference location from structure map |
| **Acceptance** | Include pattern compliance from conventions |

Example with context:

```bash
# Context says: new commands go in commands/<name>.rs, follow init.rs pattern
bd create "Add export command" -t task -p 2 --parent bd-XXXX \
  -d "Create commands/export.rs following init.rs pattern. See context-beadsmith.md §Structure Map." \
  --acceptance "Command works, tests in #[cfg(test)] module, error handling uses anyhow::Result with .context()"
```

### Acquiring Context When Missing

If no Planning Context Snapshot exists and the change is non-trivial:

1. **For minor changes**: Proceed with Phase 1 exploration
2. **For major changes**: Use `iterative-planning-context` skill first to generate context
3. **Save context**: Output to `docs/planning/context-<project>.md` for future use

### Context Staleness

Planning Context Snapshots include staleness warnings. If context is stale:
- For structural info (directory layout): Verify before relying on it
- For patterns: Sample a recent file to confirm conventions haven't changed
- For integration points: May need refresh if major changes occurred

---

## Phase 1: Understanding

**Goal**: Fully understand the project scope before decomposing.

### Key Determinations

Before creating any beads, establish clarity on:

1. **Scope**: What is the deliverable? What is explicitly out of scope?
2. **Success criteria**: How will we know when the project is complete?
3. **Constraints**: Timeline, technology stack, external dependencies?
4. **Risks**: What could go wrong? What's uncertain?
5. **Stakeholders**: Who needs to review or approve?

### Identifying Natural Boundaries

Look for natural decomposition points:

- **Functional boundaries**: Different capabilities (auth, data, UI)
- **Data boundaries**: Different data domains or storage systems
- **Interface boundaries**: API contracts between components
- **Deployment boundaries**: Services that deploy independently
- **Team boundaries**: Work that different people/agents would own

### Surfacing Hidden Dependencies

Identify non-obvious blockers:

- External services or APIs to integrate
- Data migrations or schema changes
- Infrastructure provisioning
- Documentation or compliance requirements
- Testing environments or fixtures

### Output of Phase 1

A clear mental model of:
- The project's overall structure
- 3-7 major components or phases
- Known dependencies between them
- Risks that need mitigation beads

---

## Phase 2: Decomposition

**Goal**: Break work into bounded units (beads) with clear definitions.

### Bead Anatomy

Every bead must have:

| Field | Description | Example |
|-------|-------------|---------|
| **Title** | Clear, action-oriented | "Implement user authentication API" |
| **Type** | epic, feature, task, bug, chore | `-t task` |
| **Priority** | P0 (critical) to P4 (backlog) | `-p 1` |
| **Description** | What and why | `-d "Create JWT-based auth..."` |
| **Acceptance criteria** | Testable success conditions | `--acceptance "Tests pass, docs updated"` |

### Type Selection Guide

| Type | Use When | Typical Children |
|------|----------|------------------|
| **epic** | Container for related work, multi-week effort | features, tasks |
| **feature** | User-visible capability, days to a week | tasks |
| **task** | Single unit of work, hours to a day | none or sub-tasks |
| **bug** | Defect fix | none |
| **chore** | Maintenance, refactoring, tooling | none |

### Priority Mapping

| Priority | Meaning | Use When |
|----------|---------|----------|
| P0 | Critical/Blocker | Must be done immediately, blocks everything |
| P1 | High | Core functionality, needed for MVP |
| P2 | Medium | Important but not blocking (default) |
| P3 | Low | Nice to have, polish |
| P4 | Backlog | Future consideration |

### Granularity Rules

**Too Large** (split it):
- Takes more than 2-3 days
- Has multiple distinct deliverables
- Would benefit from partial completion visibility
- Different skills or contexts needed for different parts

**Too Small** (merge it):
- Takes less than 30 minutes
- Has no independent value
- Always done together with another task
- Creates noise in the dependency graph

**Just Right**:
- Clear single deliverable
- Independently testable
- Can be claimed and completed in one session
- Dependencies are obvious and minimal

### Bead Quality Criteria (CRITICAL)

**The planning context window is precious.** When you plan, you have full visibility into requirements, research, and design decisions. That knowledge must be encoded into the bead, not left implicit.

A poorly-specified bead forces the executing agent to re-discover domain knowledge, make assumptions about intent, and produce work that technically passes but misses the point.

See `docs/bead-quality-criteria.md` for the complete specification. Key requirements:

**1. Description Encodes Domain Knowledge**

Bad: "Create the vision-workshop skill for guided vision creation."

Good: "Create skills/vision-workshop/input.yaml implementing the Product Vision Board methodology (Roman Pichler) for co-creative vision document creation. Workflow phases: 1) North Star, 2) Target Users, 3) Core Problem, 4) Value Proposition, 5) Standout Capabilities, 6) Success Criteria, 7) Anti-Goals, 8) Synthesis. Reference: skills/org-planning/input.yaml for structure pattern."

**Test:** Could an agent with NO prior context execute this bead and produce the intended result?

**2. Acceptance Criteria Are Behavioral, Not Mechanical**

Acceptance criteria should verify that the bead achieves its **purpose**, not just that artifacts exist or code was written.

**Common anti-pattern: Mechanism-vs-Purpose confusion**

For a bead about "per-bead context isolation":

Bad (verifies mechanism):
```
1. Function get_next_ready_bead() exists
2. Session persistence code removed
3. CONTEXT.md file created before each bead
```

Good (verifies purpose):
```
1. Run harness on 2-bead epic: opencode session list shows 2 distinct sessions
2. Bead 2 cannot reference variables/decisions from Bead 1's context
3. CONTEXT.md timestamps differ between beads (stat shows different mtime)
```

The bad criteria verify that changes were made. The good criteria verify that **isolation actually works**.

**More examples by bead type:**

| Bead Type | Mechanical (bad) | Behavioral (good) |
|-----------|------------------|-------------------|
| File migration | "Files moved to new location" | "grep shows all references use new paths" |
| New function | "Function exists in module" | "Calling function with X input produces Y output" |
| Refactor | "Code restructured per plan" | "All existing tests still pass + new behavior verified" |
| Config change | "Config file updated" | "System behavior changes as expected when config applied" |

**Test:** Do the acceptance criteria verify PURPOSE, not just EXISTENCE?

**3. References Are Concrete**

Bad: "Follow existing patterns in the codebase."

Good: "Follow the pattern in skills/org-planning/input.yaml: workflow section with phases/steps/outputs, patterns section, antipatterns section, checklist section, examples section."

**4. Scope Is Bounded**

Every bead should have implicit or explicit in-scope/out-of-scope. If scope is ambiguous, make it explicit in the description.

**Quality Checklist (verify before finalizing each bead):**

- [ ] Domain knowledge encoded (methodologies, constraints, key decisions)
- [ ] Behavioral acceptance criteria (verify purpose, not just existence)
- [ ] Concrete references (file paths, line numbers, pattern examples)
- [ ] Bounded scope (in-scope and out-of-scope explicit if ambiguous)
- [ ] Observable success (verification steps are concrete)

### Decomposition Patterns

**Top-Down**: Start with epic, break into features, break into tasks
```
Epic: Build Authentication System
  Feature: User Registration
    Task: Create registration form
    Task: Implement email validation
    Task: Add password strength checker
  Feature: Login Flow
    Task: Create login form
    Task: Implement JWT generation
    Task: Add session management
```

**Horizontal Layers**: Decompose by system layer
```
Epic: Add Search Feature
  Task: Design search API contract
  Task: Implement search backend
  Task: Create search UI component
  Task: Add search result caching
  Task: Write integration tests
```

**Vertical Slices**: End-to-end thin slices
```
Epic: User Dashboard
  Task: Basic dashboard with user info (full stack)
  Task: Add activity feed (full stack)
  Task: Add settings panel (full stack)
```

### Integration & Synthesis Beads (REQUIRED for multi-component epics)

When an epic has multiple features or components that must work together, you MUST add integration beads as leaf nodes in the DAG. These execute last (after all feature beads) and ensure the system works as a coherent whole.

**Why Integration Beads Are Necessary:**
- Each agent optimizes locally for its bead
- Agents produce documentation that only describes their piece
- Cross-component contracts can drift silently
- No agent has the full picture without explicit integration tasks

**Standard Integration Beads:**

For any epic with 2+ features, add:

```
Feature: Integration & Documentation (P3 - depends on all other features)
  Task: Documentation synthesis
    - Generate unified README from spec + all component implementations
    - Ensure docs tell the complete story, not just one piece
    - Acceptance: README covers full system architecture, setup, and usage
  
  Task: Cross-component verification
    - Verify API contracts match between client and server
    - Run end-to-end tests across component boundaries
    - Acceptance: E2E test passes: data flows through entire system
  
  Task: Deployment documentation
    - Verify deployment docs cover full stack (not just one component)
    - Acceptance: New developer can deploy entire system from docs
```

**Dependency Pattern:**

Integration beads use fan-in - they depend on ALL feature beads:

```bash
# Integration depends on all features
bd dep add bd-integration bd-feature1
bd dep add bd-integration bd-feature2
bd dep add bd-integration bd-feature3
```

This ensures integration beads naturally execute last, after all components are built.

**Example: Multi-Component App**

```
Epic: Oracy MVP
  Feature: Server Core (P1)
    └── [server tasks...]
  Feature: Mobile Core (P1)
    └── [mobile tasks...]
  Feature: Integration & Documentation (P3)
    ├── Task: Write unified README from spec + implementations
    ├── Task: Verify mobile API client matches server OpenAPI spec
    ├── Task: E2E test: record audio → upload → transcript appears
    └── Task: Verify deployment docs cover full stack
```

**When to Skip Integration Beads:**
- Single-component epics (no cross-component boundaries)
- Pure refactoring epics (no new functionality to document)
- Bug-fix epics (no integration surface changed)

**Do NOT skip integration beads just because they're "P3"** - they're P3 because they must run last, not because they're optional.

---

## Phase 3: Dependency Mapping

**Goal**: Establish relationships between beads.

### Dependency Types

| Type | Semantics | Use When | Command |
|------|-----------|----------|---------|
| **blocks** | A must complete before B starts | Sequential work, technical dependency | `bd dep add B A` |
| **parent-child** | Hierarchical containment | Epic contains features/tasks | `--parent <epic-id>` |
| **related** | Soft connection, informational | Related but independent work | `bd dep add A B -t related` |
| **discovered-from** | Work found during other work | Bug found while implementing feature | `bd dep add B A -t discovered-from` |

### Dependency Decision Tree

```
Is B inside A (containment)?
  YES -> parent-child (use --parent on create)
  NO  -> Continue...

Must A complete before B can start?
  YES -> blocks (bd dep add B A)
  NO  -> Continue...

Was B discovered while working on A?
  YES -> discovered-from (bd dep add B A -t discovered-from)
  NO  -> Continue...

Are A and B related but independent?
  YES -> related (bd dep add A B -t related)
  NO  -> No dependency needed
```

### Blocking Dependency Patterns

**Sequential Chain**:
```bash
# A -> B -> C (A blocks B, B blocks C)
bd dep add bd-B bd-A
bd dep add bd-C bd-B
```

**Fan-Out** (one blocks many):
```bash
# Setup blocks all implementation tasks
bd dep add bd-impl1 bd-setup
bd dep add bd-impl2 bd-setup
bd dep add bd-impl3 bd-setup
```

**Fan-In** (many block one):
```bash
# All features must complete before release
bd dep add bd-release bd-feature1
bd dep add bd-release bd-feature2
bd dep add bd-release bd-feature3
```

**Diamond** (convergent paths):
```bash
# A -> B, A -> C, B -> D, C -> D
bd dep add bd-B bd-A
bd dep add bd-C bd-A
bd dep add bd-D bd-B
bd dep add bd-D bd-C
```

### Detecting Cycles Before Instantiation

Before adding dependencies, mentally trace the graph:
- Can I reach A from A by following dependencies? If yes, cycle exists.
- Draw it out if complex.

After instantiation, verify:
```bash
bd dep cycles  # Should return empty
```

---

## Phase 4: Instantiation

**Goal**: Create the beads in the correct order with proper relationships.

### Order of Creation

1. **Epics first** (top of hierarchy)
2. **Features** (with `--parent` pointing to epic)
3. **Tasks** (with `--parent` pointing to epic or feature)
4. **Dependencies** (after all beads exist)

### Coherence Check (Before Creating Epic)

Before creating the epic, verify org-mode coherence:

1. **Does this work have an org task?**
   - If YES → Use `spawn-to-beads` skill instead (see "Spawned Epics" section)
   - If NO → Continue, but acknowledge the deviation

2. **If proceeding without org source:**
   ```bash
   # Acknowledge coherence violation (tactical exception)
   echo "NOTE: Creating epic without org source - ensure org-mode is updated when complete"
   ```

### Creating Epics

**With org source (RECOMMENDED):**
```bash
# Use spawn-to-beads skill - it creates epic with source_org_id
# and updates org task with DELEGATED_TO property
```

**Without org source (TACTICAL EXCEPTION):**
```bash
bd create "Project Epic Title" \
  -t epic \
  -p 1 \
  -d "High-level description of the project goal" \
  --acceptance "All child features complete, tests passing, docs updated"
```

Capture the returned ID (e.g., `bd-a3f8`).

### Creating Child Tasks with Hierarchical IDs

```bash
# Using --parent auto-generates hierarchical IDs: bd-a3f8.1, bd-a3f8.2, etc.
bd create "First task" -t task -p 2 --parent bd-a3f8 \
  -d "Description of what this task accomplishes" \
  --acceptance "Specific testable criteria"

bd create "Second task" -t task -p 2 --parent bd-a3f8 \
  -d "Description" \
  --acceptance "Criteria"
```

### Adding Dependencies

After all beads are created:

```bash
# Task 2 depends on Task 1 (Task 1 blocks Task 2)
bd dep add bd-a3f8.2 bd-a3f8.1

# Task 3 depends on Task 2
bd dep add bd-a3f8.3 bd-a3f8.2

# Final task depends on multiple tasks (fan-in)
bd dep add bd-a3f8.5 bd-a3f8.3
bd dep add bd-a3f8.5 bd-a3f8.4
```

### Batch Creation from Markdown

For larger plans, create a markdown file:

```markdown
# Project Plan

## Epic: Authentication System
- Type: epic
- Priority: 1
- Description: Implement complete auth system

### Task: Design API contract
- Type: task
- Priority: 1
- Blocks: Implement auth endpoints

### Task: Implement auth endpoints
- Type: task
- Priority: 2
```

Then: `bd create -f plan.md`

---

## Phase 5: Validation

**Goal**: Verify the dependency graph is complete, correct, and executable.

### Validation Checklist

#### 0. Bead Quality Gate (REQUIRED)

Before structural validation, verify each bead meets quality criteria:

```bash
# Check description length (guards against thin beads)
bd list --parent $EPIC_ID --json | jq -e '
  [.[] | select((.description | length) < 100)] 
  | if length > 0 then 
      "QUALITY FAIL: Thin descriptions on: \([.[].id] | join(", "))" | halt_error 
    else empty end
'

# Check acceptance criteria count (minimum 2 criteria per bead)
# Note: This guards against missing/thin criteria but cannot detect mechanical-vs-behavioral.
# The planner must self-audit for behavioral criteria using the test: "Does this verify PURPOSE?"
bd list --parent $EPIC_ID --json | jq -e '
  [.[] | select(
    .acceptance_criteria == null or 
    (.acceptance_criteria | split("\n") | map(select(length > 0)) | length) < 2
  )] 
  | if length > 0 then 
      "QUALITY FAIL: Insufficient acceptance criteria on: \([.[].id] | join(", "))" | halt_error 
    else empty end
'
```

**Quality Failures Are Hard Stops.** Do not proceed to execution with thin beads.

**Remediation:** For each failing bead:
1. Ask: "What domain knowledge does the executor need that I have right now?"
2. Encode that knowledge into the description
3. Ask: "How will we verify this achieves its PURPOSE, not just exists?"
4. Add behavioral acceptance criteria

#### 1. Ready Work Exists

```bash
bd ready
```

**Expected**: At least one bead with status `open` and no blockers.

**If empty**: Check for cycles or missing root tasks.

#### 2. No Cycles

```bash
bd dep cycles
```

**Expected**: Empty output (no cycles detected).

**If cycles found**: Remove one edge to break the cycle.

#### 3. Dependency Tree is Coherent

```bash
bd dep tree bd-EPIC-ID
```

**Expected**: All tasks appear in the tree, logical ordering.

**Check for**:
- Orphaned beads (not connected to epic)
- Missing dependencies (parallel tasks that should be sequential)
- Over-connected graph (unnecessary dependencies)

#### 4. Visualize Execution Order

```bash
bd graph bd-EPIC-ID
```

**Expected**: ASCII visualization showing layers:
- Layer 0: No dependencies (start here)
- Higher layers: Depend on lower layers
- Same layer: Can run in parallel

#### 5. Epic Status

```bash
bd epic status bd-EPIC-ID
```

**Expected**: Shows completion percentage and blocked/ready counts.

### Orphan Detection

List all beads and verify each is either:
- A root epic, OR
- Has a `--parent` relationship, OR  
- Has at least one `blocks` or `related` dependency

```bash
bd list --all --json | jq '.[] | select(.parent == null and .dependencies == [])'
```

### Planning Complete: Handoff to Execution

**Phase 5 is the END of the beads-plan skill's responsibility.**

After validation passes, the planning agent outputs a handoff message and STOPS:

```
Planning complete.

Epic: <epic-id>
Branch: <branch-name>  
Work Type: <type>
Beads: <count> tasks ready for execution

To execute:
  beads-harness <epic-id>
```

**The planning agent MUST NOT execute beads.** Execution is a separate phase with a separate agent (the `beads-harness`). This separation ensures:

1. **Beads are self-contained** - If the planning agent could execute, beads might rely on conversational context that isn't encoded in the bead description.

2. **Execution is scalable** - The harness can parallelize across multiple agents. Manual execution cannot.

3. **Recovery is possible** - If execution fails, the plan remains intact for retry.

See `docs/bead-quality-criteria.md` § "Planning/Execution Boundary" for details.

**Exception:** The planning agent may execute only if the user explicitly requests it (e.g., "execute the first bead now").

---

## Swarm Execution Guidance

> **Note:** This section documents how the `beads-harness` and execution agents work.
> It is reference material, not actions for the planning agent to perform.

When multiple agents work on the same beads project, coordination is essential.

### Agent Workflow

1. **Find ready work**:
   ```bash
   bd ready --json
   ```

2. **Claim a bead** (atomic operation):
   ```bash
   bd update bd-XXXX --claim
   ```
   This atomically sets `status=in_progress` and `assignee=<agent>`. Fails if already claimed.

3. **Work on the bead**: Implement the task.

4. **Complete the bead**:
   ```bash
   bd close bd-XXXX -r "Completed: brief summary"
   ```

5. **Sync changes**:
   ```bash
   bd sync
   ```

6. **Check for newly unblocked work**:
   ```bash
   bd ready --json
   ```

### Status Transitions

```
open -> in_progress (via --claim or --status in_progress)
in_progress -> closed (via bd close)
closed -> open (via bd reopen, if needed)
```

### Avoiding Conflicts

- **Always claim before working**: Never work on unclaimed beads
- **Sync frequently**: Run `bd sync` before and after work sessions
- **Use JSON output**: `--json` flag for programmatic parsing
- **Check assignee**: `bd show bd-XXXX --json | jq '.assignee'`

### Multi-Agent Patterns

**Round-Robin**:
Each agent queries `bd ready`, claims the first unclaimed bead.

**Specialized Agents**:
Filter by label: `bd ready --label backend` vs `bd ready --label frontend`

**Priority-Based**:
Sort by priority: `bd ready --sort priority`

---

## Worked Example: CLI Tool with 3 Subcommands

### Specification

> Build a CLI tool called `mytool` with three subcommands: `init`, `run`, and `status`. 
> It should be written in Go, have a config file, and include tests.

### Phase 1: Understanding

**Scope**: CLI tool with 3 commands, Go, config support, tests.
**Success**: `mytool init`, `mytool run`, `mytool status` all work, tests pass.
**Constraints**: Go 1.21+, Cobra for CLI framework.
**Boundaries**: 
- Core library (shared code)
- CLI layer (Cobra commands)
- Config system
- Each subcommand

### Phase 2: Decomposition

```
Epic: mytool CLI
  Task: Project scaffolding (go mod, directory structure)
  Task: Implement config loading
  Task: Implement `init` subcommand
  Task: Implement `run` subcommand  
  Task: Implement `status` subcommand
  Task: Add unit tests
  Task: Add integration tests
  Task: Write README documentation
```

### Phase 3: Dependency Mapping

```
scaffolding <- config <- init
scaffolding <- config <- run
scaffolding <- config <- status
init, run, status <- unit tests
unit tests <- integration tests
integration tests <- documentation (docs describe tested behavior)
```

### Phase 4: Instantiation

```bash
# Create epic
bd create "mytool CLI" -t epic -p 1 \
  -d "CLI tool with init, run, and status subcommands" \
  --acceptance "All commands work, tests pass, README complete"
# Returns: bd-m7k2

# Create tasks with hierarchical IDs
bd create "Project scaffolding" -t task -p 1 --parent bd-m7k2 \
  -d "Set up go.mod, directory structure, Cobra root command" \
  --acceptance "go build succeeds, mytool --help works"
# Returns: bd-m7k2.1

bd create "Implement config loading" -t task -p 1 --parent bd-m7k2 \
  -d "Config file parsing with Viper, support YAML and env vars" \
  --acceptance "Config loads from file and environment"
# Returns: bd-m7k2.2

bd create "Implement init subcommand" -t task -p 2 --parent bd-m7k2 \
  -d "mytool init creates default config file" \
  --acceptance "Running mytool init creates .mytool.yaml"
# Returns: bd-m7k2.3

bd create "Implement run subcommand" -t task -p 2 --parent bd-m7k2 \
  -d "mytool run executes the main workflow" \
  --acceptance "Running mytool run produces expected output"
# Returns: bd-m7k2.4

bd create "Implement status subcommand" -t task -p 2 --parent bd-m7k2 \
  -d "mytool status shows current state" \
  --acceptance "Running mytool status displays state information"
# Returns: bd-m7k2.5

bd create "Add unit tests" -t task -p 2 --parent bd-m7k2 \
  -d "Unit tests for config, init, run, status packages" \
  --acceptance "go test ./... passes with >70% coverage"
# Returns: bd-m7k2.6

bd create "Add integration tests" -t task -p 3 --parent bd-m7k2 \
  -d "End-to-end tests running actual CLI commands" \
  --acceptance "Integration test suite passes"
# Returns: bd-m7k2.7

bd create "Write README documentation" -t task -p 3 --parent bd-m7k2 \
  -d "README with installation, usage, and examples" \
  --acceptance "README covers all commands with examples"
# Returns: bd-m7k2.8

# Add dependencies
bd dep add bd-m7k2.2 bd-m7k2.1  # config depends on scaffolding
bd dep add bd-m7k2.3 bd-m7k2.2  # init depends on config
bd dep add bd-m7k2.4 bd-m7k2.2  # run depends on config
bd dep add bd-m7k2.5 bd-m7k2.2  # status depends on config
bd dep add bd-m7k2.6 bd-m7k2.3  # unit tests depend on init
bd dep add bd-m7k2.6 bd-m7k2.4  # unit tests depend on run
bd dep add bd-m7k2.6 bd-m7k2.5  # unit tests depend on status
bd dep add bd-m7k2.7 bd-m7k2.6  # integration tests depend on unit tests
bd dep add bd-m7k2.8 bd-m7k2.7  # docs depend on integration tests
```

### Phase 5: Validation

```bash
$ bd ready
bd-m7k2.1  P1  task  Project scaffolding

$ bd dep cycles
# (empty - no cycles)

$ bd graph bd-m7k2
┌─────────────────────────────────────────────────────────────┐
│ Layer 0                                                     │
│ ○ bd-m7k2.1 Project scaffolding                             │
├─────────────────────────────────────────────────────────────┤
│ Layer 1                                                     │
│ ○ bd-m7k2.2 Implement config loading                        │
├─────────────────────────────────────────────────────────────┤
│ Layer 2                                                     │
│ ○ bd-m7k2.3 Implement init subcommand                       │
│ ○ bd-m7k2.4 Implement run subcommand                        │
│ ○ bd-m7k2.5 Implement status subcommand                     │
├─────────────────────────────────────────────────────────────┤
│ Layer 3                                                     │
│ ○ bd-m7k2.6 Add unit tests                                  │
├─────────────────────────────────────────────────────────────┤
│ Layer 4                                                     │
│ ○ bd-m7k2.7 Add integration tests                           │
├─────────────────────────────────────────────────────────────┤
│ Layer 5                                                     │
│ ○ bd-m7k2.8 Write README documentation                      │
└─────────────────────────────────────────────────────────────┘

$ bd epic status bd-m7k2
Epic: mytool CLI (bd-m7k2)
Progress: 0/8 complete (0%)
Ready: 1, Blocked: 7, In Progress: 0
```

**Result**: Valid dependency graph with one ready starting point, no cycles, clear execution layers.

---

## BD Command Reference

### Initialization

```bash
bd init                    # Interactive initialization
bd init --quiet            # Non-interactive (for agents)
bd init --prefix myproj    # Custom ID prefix
```

### Creating Issues

```bash
bd create "Title" [flags]

Flags:
  -t, --type string        # epic|feature|task|bug|chore (default: task)
  -p, --priority string    # 0-4 or P0-P4 (default: 2)
  -d, --description string # Issue description
  --parent string          # Parent issue ID for hierarchical child
  --acceptance string      # Acceptance criteria
  -l, --labels strings     # Labels (comma-separated)
  -a, --assignee string    # Assignee
  --deps strings           # Dependencies on create (type:id format)
  --json                   # JSON output
```

### Dependency Management

```bash
bd dep add <issue> <depends-on> [-t type]  # Add dependency
bd dep remove <issue> <depends-on>          # Remove dependency
bd dep tree <issue>                         # Show dependency tree
bd dep tree <issue> --direction=up          # Show what this blocks
bd dep cycles                               # Detect cycles
bd dep list <issue>                         # List dependencies
```

Dependency types: `blocks` (default), `related`, `parent-child`, `discovered-from`, `tracks`

### Querying Issues

```bash
bd ready                   # Show ready work (no blockers)
bd ready --json            # JSON output for parsing
bd ready --limit 5         # Limit results
bd ready --assignee name   # Filter by assignee
bd ready --label backend   # Filter by label

bd list                    # List all open issues
bd list --all              # Include closed
bd list --parent bd-XXX    # Children of specific parent
bd list --status open      # Filter by status

bd show <id>               # Show issue details
bd show <id> --json        # JSON output

bd blocked                 # Show blocked issues
bd graph <id>              # ASCII dependency visualization
bd graph --all             # All open issues
```

### Updating Issues

```bash
bd update <id> [flags]

Flags:
  --status string          # open|in_progress|closed
  --claim                  # Atomically claim (set in_progress + assignee)
  --title string           # New title
  -d, --description string # New description
  -p, --priority string    # New priority
  --acceptance string      # Acceptance criteria
  --add-label strings      # Add labels
  --remove-label strings   # Remove labels
```

### Closing Issues

```bash
bd close <id>              # Close an issue
bd close <id> -r "reason"  # Close with reason
bd close <id> --suggest-next  # Show newly unblocked after close
```

### Epic Management

```bash
bd epic status <id>        # Show epic completion status
bd epic close-eligible     # Close epics where all children complete
```

### Swarm Operations

```bash
bd swarm validate <epic>   # Validate epic structure for swarming
bd swarm create <epic>     # Create swarm molecule from epic
bd swarm status            # Show swarm status
```

### Sync and Data

```bash
bd sync                    # Sync with git (export + commit + pull + push)
bd export -o file.jsonl    # Export to JSONL
bd import -i file.jsonl    # Import from JSONL
```

---

## Anti-Patterns

### Over-Decomposition

**Symptom**: 50+ tiny tasks for a simple feature.
**Problem**: Graph noise, overhead exceeds value.
**Fix**: Merge related micro-tasks, aim for 30min-3hr tasks.

### Under-Decomposition

**Symptom**: One "Implement everything" task.
**Problem**: No progress visibility, can't parallelize.
**Fix**: Break into functional units with clear boundaries.

### Missing Dependencies

**Symptom**: `bd ready` shows tasks that actually can't start.
**Problem**: Implicit dependencies not captured.
**Fix**: Trace each task's true prerequisites, add blocking deps.

### Cycle Creation

**Symptom**: `bd dep cycles` returns results.
**Problem**: Deadlock - nothing can complete.
**Fix**: Identify the spurious edge, remove it.

### Orphaned Beads

**Symptom**: Tasks not connected to any epic or dependency.
**Problem**: Lost work, unclear ownership.
**Fix**: Add parent or dependency relationships.

### Vague Acceptance Criteria

**Symptom**: "It works" as acceptance criteria.
**Problem**: No way to verify completion.
**Fix**: Specify testable conditions: "Tests pass", "API returns 200", "Config loads".

### Priority Inflation

**Symptom**: Everything is P0.
**Problem**: No way to triage, paralysis.
**Fix**: Reserve P0 for true blockers, use P1-P2 for normal work.

### Ignoring Org Callback

**Symptom**: Closing spawned epic without updating source org task.
**Problem**: Org task remains in WAITING forever; planning layer out of sync with reality.
**Fix**: Before closing any epic with `source_org_id`, run `complete-to-org` skill to update the org task.

### Closing Epic Before Callback

**Symptom**: Running `bd close` on spawned epic, THEN trying to find source_org_id.
**Problem**: Source reference may become harder to access after close.
**Fix**: Extract source_org_id and trigger callback BEFORE closing the epic.

---

## Troubleshooting

### "bd ready" Returns Empty

**Causes**:
1. All tasks have blockers - check `bd blocked`
2. Cycle exists - run `bd dep cycles`
3. All tasks closed - run `bd list --status open`

**Fix**: Add a task with no dependencies, or break the cycle.

### "bd dep add" Fails

**Causes**:
1. Issue ID doesn't exist - verify with `bd show <id>`
2. Would create cycle - check existing deps first

**Fix**: Verify IDs, reconsider dependency direction.

### Hierarchical ID Not Generated

**Cause**: Missing `--parent` flag on create.

**Fix**: Use `--parent bd-EPIC-ID` when creating child tasks.

### Sync Conflicts

**Cause**: Multiple agents modified same JSONL.

**Fix**: 
```bash
git pull --rebase
bd import -i .beads/issues.jsonl
bd sync
```

### Agent Can't Claim

**Cause**: Another agent already claimed.

**Fix**: Query `bd ready --unassigned` to find unclaimed work.

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `iterative-planning-context` | Produces Planning Context Snapshots consumed during decomposition |
| `beads-execute` | Executes the beads created by this skill |
| `spawn-to-beads` | Spawns epics from org-mode tasks |
| `complete-to-org` | Callbacks when spawned epics complete |
| `agents-md` | Creates AGENTS.md files that inform codebase context |
