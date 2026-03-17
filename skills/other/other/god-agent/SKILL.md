---
name: god-agent
description: >
  Use when building a new greenfield app or major multi-layer feature requiring both .NET backend + React frontend.

  RECOMMENDED: Run /god-agent-plan first for high-quality specs via research + interview + external review.

  DO NOT USE FOR: Bug fixes, small changes, single-layer work (backend-only or frontend-only), non-.NET/React projects.

  REQUIRED: .NET 9 + React 19 + Tailwind v4 + Zustand + SQLite.

  INPUT: Idea string + optional "Preferences: ..." suffix.

  COMMITMENT: Long-running (30+ min), resumable via STATE.md.
user-invocable: true
argument-hint: "Build a recipe sharing app. Preferences: Danish market, mobile-first"
---

> ⚠️ **Spelling:** It's `saurun:` (with U), not "sauron"

# God-Agent: Autonomous Development Pipeline

**Version: 1.0.34** — Token usage tracking

> **ANNOUNCE AT STARTUP:** "Starting god-agent v1.0.34 (token usage tracking)"

Take any input (one-liner, rough spec, or product brief) and deliver working, tested, reviewed, committed code. No human interaction during execution.

**Tech stack (always):** .NET 9, ASP.NET Core, EF Core 9, SQLite, SignalR, React 19, Vite, TypeScript, Tailwind CSS v4, Zustand.

**Subagent dispatch (always):** Run subagents in foreground. Never use `run_in_background`. When tasks are independent (e.g., Phase 2 planning for different work units), dispatch them in parallel by including multiple Task calls in a single message. Wait for all to complete before proceeding.

**Token tracking (always):** Every Task tool response includes a `<usage>` block with `total_tokens`, `tool_uses`, and `duration_ms`. After EVERY subagent dispatch (all phases), append a row to STATE.md `## Token Usage` table:

```
| {phase_number} | {task_or_phase_name} | {role} | {total_tokens} | {tool_uses} | {duration_ms}ms |
```

Phase column: use number only (e.g., `3`, not `Phase 3`).
Role values: `implementer`, `reviewer`, `planner`, `debugger`. For retries, append `-retry` (e.g., `implementer-retry`, `reviewer-retry`).

Update the cumulative line: `**Cumulative:** {sum} tokens across {count} subagent dispatches`

## Phase Overview

| Phase | Name | Gate | Output Artifact |
|-------|------|------|-----------------|
| -1 | Scaffold | Blocking | Directory structure, git repo |
| 0 | Intake | Blocking | `_docs/specs/{DATE}-{feature}.md` |
| 1 | Architecture | Blocking | `_docs/specs/{DATE}-{feature}-architecture.md` |
| 2 | Planning | Blocking | `_docs/plans/*.md` + `MANIFEST.json` |
| 3 | Execution | Blocking | Working code, passing tests |
| 4 | Integration | Blocking | `_docs/reports/{DATE}-{feature}-report.md` |
| 5 | E2E Testing | **Non-Blocking** | `_docs/e2e-results/report.md` + videos |
| 6 | Design Polish | **Non-Blocking** | `frontend/public/assets/` + wired components |

## Step 1: Pre-Flight

Before anything else:

1. **Parse input.** Extract the idea and any inline preferences (look for "Preferences:" in the input string).

2. **Derive project path.**
   - Derive `{project-name}` from the idea (kebab-case, e.g., "recipe sharing app" → `recipe-app`)
   - Target path: `~/repos/playground/{project-name}/`
   - **Never ask the user where to create the project** — always use this location

3. **Detect mode.**
   - Target folder exists → **Extension Mode** (project already started, extend it)
   - Target folder does not exist → **Greenfield Mode** (create new project)

4. **Enter project directory.**
   - Greenfield: Create the directory, then `cd` into it
   - Extension: `cd` into the existing directory
   - Open the project in VS Code: `code {project-path}`

5. **Check for resume.** If `.god-agent/STATE.md` exists:
   - Read it
   - Find last completed phase
   - Read that phase's output artifact
   - Log `[RESUMED] from Phase {X}` in STATE.md
   - Skip to the next incomplete phase (or sub-position within a phase)

6. **Check for planning artifacts.** If `_docs/plans/MANIFEST.json` exists AND at least one `_docs/specs/*-architecture.md` exists:
   - Validate MANIFEST.json: `plans` array has >=1 entry, each entry's `path` points to an existing file on disk.
   - Validate architecture doc: has `## Entity Model` and `## API Contract` sections.
   - If valid:
     - Verify `design-system/MASTER.md` exists (god-agent-plan Step 7b produces this). If missing: STOP: "Planning artifacts found but design system missing. Re-run /god-agent-plan to resume from Step 7b."
     - Log: `[PLAN] Found god-agent-plan artifacts. Skipping Phases 0-2.`
     - Set `planning_source = "god-agent-plan"` in STATE.md
     - Jump directly to Phase 3: Execution
     - **Note:** Phase -1 (Scaffold) still runs if greenfield mode and directories don't exist yet
   - If invalid (files exist but malformed):
     - STOP: "Planning artifacts found but invalid: {specific issue}. Fix or delete and re-run /god-agent-plan."

   If no planning artifacts found:
   - Assess input completeness (same 7 dimensions as god-agent-plan -- see god-agent-plan/references/completeness-dimensions.md)
   - If 6+ dimensions covered (detailed spec/PRD attached): proceed with Phases 0-2 (self-dialogue)
   - If 1-5 dimensions (partial input): Log `[PLAN] Input has {N}/7 dimensions. Proceeding with self-dialogue Phases 0-2. For higher-quality specs, use /god-agent-plan.` Proceed with Phases 0-2.
   - If 0 dimensions (empty or trivial): STOP, recommend `/god-agent-plan`

7. **Verify required skills exist.** Load `superpowers:brainstorming` via the Skill tool. If it loads successfully, the plugin system is working and remaining skills can be verified lazily (each phase loads its own skills — if one is missing, the Skill tool will error and you STOP). If `superpowers:brainstorming` fails to load, STOP immediately — the plugin system is broken.

   Required skills (verified lazily when each phase first uses them):
   - `saurun:scaffold` (Phase -1)
   - `superpowers:brainstorming` (Phase 0)
   - `ui-ux-pro-max` (Phase 0 — style selection)
   - `saurun:dotnet-tactical-ddd` (Phase 1)
   - `saurun:react-frontend-patterns` (Phase 1)
   - `saurun:dotnet-writing-plans` (Phase 2 — backend)
   - `saurun:react-writing-plans` (Phase 2 — frontend)
   - `superpowers:subagent-driven-development` (Phase 3)
   - `saurun:dotnet-code-quality-reviewer-prompt` (Phase 3)
   - `saurun:react-code-quality-reviewer-prompt` (Phase 3)
   - `superpowers:systematic-debugging` (Phase 3)
   - `superpowers:finishing-a-development-branch` (Phase 4)
   - `superpowers:verification-before-completion` (Phase 4)
   - `saurun:e2e-test` (Phase 5)
   - `saurun:design-polish` (Phase 6 — asset generation)
   - `claude-md-management:revise-claude-md` (Post-Completion)

   Required agents (have skills pre-loaded):
   - `saurun:backend-implementer` (has `dotnet-tactical-ddd` + `dotnet-tdd`) — Phase 3
   - `saurun:frontend-implementer` (has `react-frontend-patterns` + `frontend-design` + `react-tdd`) — Phase 3
   - `saurun:design-polish-agent` (has `design-polish` + `nano-banana-pro`) — Phase 6

8. **Read context layers** (in priority order):

   | Layer | Source | When |
   |-------|--------|------|
   | Injected context | User preferences from input string | Always |
   | Project context | `CLAUDE.md`, `_docs/`, `agent-os/` | Extension mode only |
   | Stack defaults | .NET 9, React 19, Tailwind v4, Zustand, SQLite | Always (hardcoded) |

9. **Write initial STATE.md** to `.god-agent/STATE.md` (see STATE.md Protocol below).

---

## How Gates Work

After each phase completes, the **controller** (not the subagent) validates the output by reading the artifact and running through the gate checklist:

1. **Read artifact** — controller reads the phase output (spec file, architecture doc, plan files, etc.)
2. **Run checklist** — controller checks each item in the gate checklist
3. **Pass** — all items checked → proceed to next phase
4. **Fail** — one or more items unchecked → re-dispatch subagent with: `"Gate N failed: {unchecked items}. Fix these."`
5. **Retry limit** — up to 2 re-dispatches per gate. Still failing → log to STATE.md and STOP.

---

## Step 2: Execute Phases

Run phases -1 through 6 sequentially. ALL phases MUST be executed. After each phase: update STATE.md, run gate check. If gate fails: re-dispatch with feedback (up to 2 retries). If still failing: log to STATE.md and STOP.

**Phases marked "Non-Blocking" (5 and 6):** MUST execute, MUST run gate check. Execute with the same rigor as blocking phases. Only difference: gate failures are logged but don't trigger STOP. "Non-blocking" means "failures are tolerated." It does NOT mean "skip" or "reduce effort."

---

### Phase -1: Scaffold (Greenfield Only)

**Skip if:** Extension mode (CLAUDE.md exists).

**Runs as:** Controller loads and executes `saurun:scaffold` skill.

Load `saurun:scaffold` via Skill tool with argument: `{project-path}`

**Gate -1 Checklist** (verified by controller after skill completes):
- [ ] Directory `backend/` exists
- [ ] Directory `frontend/` exists
- [ ] Directory `_docs/` exists
- [ ] File `CLAUDE.md` exists
- [ ] File `.gitignore` exists
- [ ] File `backend/Api/Program.cs` exists with `/health` endpoint
- [ ] Git repo initialized (`.git/` exists)
- [ ] At least one commit exists (`git log` succeeds)

**On failure:** Re-dispatch with: `"Gate -1 failed: {unchecked items}. Fix these."`

**Update STATE.md:** Phase -1 complete.

---

### Phase 0: Intake (Idea -> Product Spec)

**Dispatch subagent:**

```
Task(subagent_type="general-purpose", prompt="""
{AUTONOMOUS_PREAMBLE}

You are executing Phase 0 (Intake) of the god-agent pipeline.

INPUT: {user_input}

STATE: {STATE.md contents}

SKILL TO FOLLOW: superpowers:brainstorming
Load this skill via the Skill tool and follow its process, but in
self-dialogue mode -- generate questions, answer them from context,
log assumptions.

MODE: {Greenfield | Extension}

OUTPUT REQUIREMENTS:
1. Write product spec to _docs/specs/{DATE}-{feature}.md using the template below
2. Update .god-agent/STATE.md with decisions and assumptions
3. Write brainstorming Q&A log to .god-agent/brainstorm-qa.md using the Q&A template below

Q&A LOG TEMPLATE: See references/qa-template.md

SPEC TEMPLATE: See references/spec-template.md
""")
```

**After Phase 0 subagent completes, controller runs style selection:**

```
# Extension mode check
If design-system/MASTER.md exists:
  Log "[STYLE] Reusing existing design system"
  Skip style generation
Else:
  # Extract style keywords from Q&A log
  Read .god-agent/brainstorm-qa.md
  Extract Q9 answer → style_keywords

  # If Q9 was derived (not from user input), use product context
  If style_keywords is generic:
    Combine: {product_type from Q3} + {industry from Q1} + {users from Q2}
    → style_keywords

  # Run ui-ux-pro-max
  Invoke Skill tool: ui-ux-pro-max
  Run: python3 {skill_path}/scripts/search.py \
    "{style_keywords}" \
    --design-system --persist -p "{project_name}"

  # Fallback if derivation fails
  If ui-ux-pro-max fails or produces empty result:
    Use default: "modern minimal clean"
    Log assumption to STATE.md

# Update CLAUDE.md
Add to CLAUDE.md:
  ## Visual Style
  Style: {style_name from MASTER.md}
  Design System: design-system/MASTER.md
```

**Gate 0 Checklist:**
- [ ] Spec file exists at `_docs/specs/{DATE}-{feature}.md`
- [ ] Section "## Problem" exists and is not empty
- [ ] Section "## Solution" exists and is not empty
- [ ] Section "## Scope" has "### In Scope" with at least 1 item
- [ ] Section "## Scope" has "### Out of Scope" with at least 1 item
- [ ] Section "## Entities" lists at least 1 entity
- [ ] Section "## User Flows" describes at least 1 flow
- [ ] Section "## API Surface" exists and is not empty
- [ ] Section "## Tech Decisions" exists and is not empty
- [ ] Section "## Decisions & Rationale" has at least 3 numbered entries
- [ ] Section "## Rejected Alternatives" has at least 2 entries with reasoning
- [ ] Section "## Risks & Mitigations" table has at least 2 rows
- [ ] No obvious contradictions between In Scope and Out of Scope
- [ ] Q&A log exists at `.god-agent/brainstorm-qa.md`
- [ ] Q&A log has answers for all **9** standard questions
- [ ] Each Q&A entry has a Source field (Injected context | Project context | Stack defaults | Assumption)
- [ ] `design-system/MASTER.md` exists (greenfield) OR was already present (extension)
- [ ] CLAUDE.md has `## Visual Style` section

**On failure:** Re-dispatch phase subagent with prompt including:
"Previous attempt failed Gate 0. Issues: {list unchecked items}. Fix these specific issues."

**Update STATE.md:** Phase 0 complete, record spec path.

---

### Phase 1: Architecture (Spec -> Technical Design)

**Dispatch subagent:**

```
Task(subagent_type="general-purpose", prompt="""
{AUTONOMOUS_PREAMBLE}

You are executing Phase 1 (Architecture) of the god-agent pipeline.

PRODUCT SPEC: {contents of the spec from Phase 0}

STATE: {STATE.md contents}

SKILLS TO LOAD (use Skill tool):
1. saurun:dotnet-tactical-ddd -- for backend architecture decisions
2. saurun:react-frontend-patterns -- for frontend architecture decisions

ENTITY DESIGN DECISION FRAMEWORK:
For each entity in the spec, ask:
  Does it have business rules or behavior methods?
  YES -> Rich domain object (private setters, factory methods, invariants)
         Test at domain level (unit tests on behavior methods)
  NO  -> Anemic property bag (public getters/setters, no domain methods)
         Do NOT test at domain level
         Test at integration level (API endpoints exercise it through EF Core)

OUTPUT REQUIREMENTS:
1. Write architecture doc to _docs/specs/{DATE}-{feature}-architecture.md
   using the template below
2. Update .god-agent/STATE.md with architecture decisions

CONCISENESS RULES (this doc is for autonomous agents, not humans):
- NO redundancy: information appears ONCE in the most logical place
- NO full code: method signatures only, not implementations
- NO obvious patterns: don't describe standard TanStack Query or EF Core flows
- NO separate validation section: put validation inline in DTOs as comments
- Rich entities: list method signatures only (e.g., `Create(), AddItem(), RemoveItem()`)
- Anemic entities: just name and properties, no behavior section
- Data Flow: ONLY describe non-standard flows or critical decisions
- Infrastructure: ONLY non-default choices (skip "EF Core code-first migrations")

ARCHITECTURE TEMPLATE: See references/architecture-template.md
""")
```

**Gate 1 Checklist:**
- [ ] Architecture doc exists at `_docs/specs/{DATE}-{feature}-architecture.md`
- [ ] Section "## Entity Model" classifies each entity as rich or anemic with aggregate boundaries
- [ ] Rich entities list behavior method names (not full implementations)
- [ ] Section "## API Contract" has:
  - [ ] "### DTOs" with properties AND inline validation comments (no separate validation section)
  - [ ] "### Endpoints" with request/response types
- [ ] Section "## Component Tree" covers pages, components, stores, hooks (compact format)
- [ ] Section "## Infrastructure Decisions" lists ONLY non-default choices
- [ ] Section "## Test Layer Map" has entry for every entity with correct test layer
- [ ] NO redundancy: validation not repeated, entity design not duplicated
- [ ] NO full code implementations (method signatures only for rich entities)

**On failure:** Re-dispatch phase subagent with prompt including:
"Previous attempt failed Gate 1. Issues: {list unchecked items}. Fix these specific issues."

**Update STATE.md:** Phase 1 complete, record architecture doc path.

---

### Phase 2: Planning (Architecture -> Implementation Plans)

**For each work unit**, dispatch a separate subagent. Select applicable units from:

- Project scaffold (greenfield only)
- Backend domain + infra
- Backend API
- Backend real-time (if SignalR needed)
- Frontend state + API
- Frontend pages + components
- Integration

**Skill routing:**

| Work Unit | Skill |
|-----------|-------|
| Scaffold | `saurun:dotnet-writing-plans` then `saurun:react-writing-plans` |
| Backend | `saurun:dotnet-writing-plans` |
| Frontend | `saurun:react-writing-plans` |
| Integration | `saurun:dotnet-writing-plans` then `saurun:react-writing-plans` |

**Subagent prompt (per work unit):**

```
Task(subagent_type="general-purpose", prompt="""
{AUTONOMOUS_PREAMBLE}

You are executing Phase 2 (Planning) of the god-agent pipeline.
Generate an implementation plan for work unit: {unit_name}

ARCHITECTURE DOC: {contents of architecture doc}
PRODUCT SPEC: {contents of product spec}
STATE: {STATE.md contents}

SKILL TO LOAD: {saurun:dotnet-writing-plans | saurun:react-writing-plans}
Load via Skill tool. Use dotnet-writing-plans for backend work units, react-writing-plans for frontend.

CONTEXT FOR PLAN WRITER:
{relevant sections of architecture doc for this work unit}

OUTPUT: Write plan to _docs/plans/{DATE}-{unit_name}.md
""")
```

**After all Phase 2 subagents complete**, the controller writes `_docs/plans/MANIFEST.json`:

```json
{
  "feature": "recipe-sharing",
  "created": "2026-02-04T10:30:00Z",
  "plans": [
    {"id": "backend-domain", "path": "_docs/plans/2026-02-04-backend-domain.md"},
    {"id": "backend-api", "path": "_docs/plans/2026-02-04-backend-api.md"},
    {"id": "frontend-state", "path": "_docs/plans/2026-02-04-frontend-state.md"},
    {"id": "frontend-pages", "path": "_docs/plans/2026-02-04-frontend-pages.md"}
  ]
}
```

Array order is execution order (backend before frontend).

**Gate 2 Checklist (per plan):**
- [ ] Plan file exists at `_docs/plans/{DATE}-{unit}.md`
- [ ] Plan header includes Goal, Architecture reference, Tech Stack
- [ ] Every task has `**Implements:**` referencing a contract from architecture doc
- [ ] Every task has `**Files:**` with exact Create/Modify/Test paths
- [ ] Every task has `**Behaviors:**` with at least 2 items (happy path + error case)
- [ ] Tasks with dependencies have `**Dependencies:**` listing prerequisite tasks
- [ ] No task references a contract that doesn't exist in architecture doc (cross-reference validation)

**Gate 2 Checklist (MANIFEST.json):**
- [ ] File exists at `_docs/plans/MANIFEST.json`
- [ ] Contains `plans` array with at least 1 entry
- [ ] Each entry has `id` and `path` fields
- [ ] Plans are in correct execution order (backend before frontend)
- [ ] All referenced plan files exist

**On failure:** Re-dispatch the failing plan's subagent with prompt including:
"Previous attempt failed Gate 2 for {plan_name}. Issues: {list unchecked items}. Fix these specific issues."

**Update STATE.md:** Phase 2 complete, list all plan paths.

---

### Phase 3: Execution (Plans -> Working Code)

**You (the controller) run this directly.** Do NOT delegate Phase 3 to a single subagent. You orchestrate the task loop yourself, dispatching individual implementer/reviewer subagents per task. This preserves cross-phase context from Phases 0-2.

**Load skill:** `superpowers:subagent-driven-development` — follow its process for the implement/review loop.

**Orchestration loop:**

```
Read MANIFEST.json -> plans array defines execution order
Read architecture doc ONCE (for contract extraction)

# Extract style summary for frontend tasks (read once)
If design-system/MASTER.md exists:
  Extract from MASTER.md:
    - Style name (e.g., "Scandinavian Minimal")
    - Primary color hex
    - Secondary/accent color hex
    - Background color hex
    - Heading font
    - Body font
    - Mood keywords (e.g., "warm, friendly, approachable")
  Store as style_summary for frontend dispatches

For each plan (in array order):
  Read the plan file, extract all tasks
  For each task:
    1. Update STATE.md: current position
    2. Extract relevant contract from architecture doc:
       - Find the contract referenced in task's "Implements:" field
       - Extract just the relevant DTO definitions, endpoint spec, validation rules
       - Keep extracted contract to ~15 lines max
    3. Dispatch IMPLEMENTER subagent (see agent routing below)
       - Use specialized agent: saurun:backend-implementer or saurun:frontend-implementer
       - Provide: task name, extracted contract, file paths, behaviors
       - For frontend tasks: include style_summary + placeholder convention
       - Skills are pre-loaded by the agent (no skill-loading instructions needed)
       - If implementer asks questions -> answer from Phase 0/1 context
    4. Dispatch REVIEWER subagent (single-pass, combined spec + quality review)
       - Uses superpowers:code-reviewer with stack-specific quality criteria
       - Pass -> continue
       - Fail (Critical/Important) -> resume implementer with fix instructions -> re-review (up to 2 retries)
       - Fail (Minor) -> note and continue
    5. Log token usage: read <usage> from implementer + reviewer responses,
       append rows to STATE.md ## Token Usage, update cumulative line
    6. Update STATE.md: task complete
  After all tasks in plan:
    Run full test suite: dotnet test backend/ && npm test (if frontend exists)
    Pass -> next plan
    Fail -> dispatch superpowers:systematic-debugging subagent (up to 2 attempts)
    Still fails -> STOP and report
```

**Example implementer dispatch (backend):**

```
Task(subagent_type="saurun:backend-implementer", prompt="""
{AUTONOMOUS_PREAMBLE}

TASK: {task name from plan}

CONTRACT (from Architecture doc):
- Endpoint: POST /lists/{id}/items ← AddItemRequest → ShoppingItemDto
- AddItemRequest { name, category }
- ShoppingItemDto { id, name, category, isChecked, addedAt }
- Validation: name required 1-100 chars, category required enum

FILES:
- Create: Api/Endpoints/ShoppingListEndpoints.cs
- Test: Tests/Api/ShoppingListEndpointsTests.cs

BEHAVIORS:
- Valid input → returns created ShoppingItemDto with 201
- Empty name → returns 400 with validation error
- Invalid category → returns 400 with validation error
- List not found → returns 404

PREVIOUS TASK OUTCOMES: {summary of completed tasks in this plan}
""")
```

**Example implementer dispatch (frontend):**

```
Task(subagent_type="saurun:frontend-implementer", prompt="""
{AUTONOMOUS_PREAMBLE}

TASK: {task name from plan}

DESIGN SYSTEM:
- Style: {style_name}
- Colors: Primary {primary_hex}, Accent {accent_hex}, Background {bg_hex}
- Typography: {heading_font} / {body_font}
- Mood: {mood_keywords}

CONTRACT (from Architecture doc):
- Component: AddItemForm { listId: string, onItemAdded: (item: ShoppingItemDto) => void }
- ShoppingItemDto { id, name, category, isChecked, addedAt }
- API: POST /lists/{id}/items ← { name, category } → ShoppingItemDto

FILES:
- Create: src/components/AddItemForm.tsx
- Test: src/components/__tests__/AddItemForm.test.tsx

BEHAVIORS:
- Submitting valid input calls onItemAdded with new item
- Empty name shows validation error
- Displays loading state while submitting

PLACEHOLDER CONVENTION:
When the design needs images/illustrations, use placeholder elements:
- Hero images: <div data-asset="hero-{name}" className="bg-gray-200 aspect-video" />
- Illustrations: <div data-asset="illustration-{name}" className="bg-gray-100 w-64 h-64" />
- Icons (custom): <span data-asset="icon-{name}" />
Do NOT spend time sourcing real images. Phase 6 generates all visual assets.

PREVIOUS TASK OUTCOMES: {summary of completed tasks in this plan}
""")
```

**Example reviewer dispatch (single-pass):**

```
Task(subagent_type="superpowers:code-reviewer", prompt="""
Review this implementation for both spec compliance and code quality.

TASK SPEC:
{task spec from plan}

WHAT WAS IMPLEMENTED:
{implementer's report}

DIFF: Compare {BASE_SHA}..{HEAD_SHA}

**Load the appropriate criteria skill for stack-specific review guidance:**
- Backend tasks: Load `saurun:dotnet-code-quality-reviewer-prompt` via Skill tool
- Frontend tasks: Load `saurun:react-code-quality-reviewer-prompt` via Skill tool

Follow the ADDITIONAL_REVIEW_CRITERIA from the loaded skill.
""")
```

**Agent routing:**

| Plan Type | Implementer Agent | Pre-loaded Skills | Review Criteria Source |
|-----------|-------------------|-------------------|------------------------|
| Backend domain | `saurun:backend-implementer` | `dotnet-tactical-ddd`, `dotnet-tdd` | Reviewer loads `saurun:dotnet-code-quality-reviewer-prompt` |
| Backend API | `saurun:backend-implementer` | `dotnet-tactical-ddd`, `dotnet-tdd` | Reviewer loads `saurun:dotnet-code-quality-reviewer-prompt` |
| Backend SignalR | `saurun:backend-implementer` | `dotnet-tactical-ddd`, `dotnet-tdd` | Reviewer loads `saurun:dotnet-code-quality-reviewer-prompt` |
| Frontend state | `saurun:frontend-implementer` | `react-frontend-patterns`, `react-tailwind-v4-components`, `frontend-design`, `react-tdd` | Reviewer loads `saurun:react-code-quality-reviewer-prompt` |
| Frontend pages | `saurun:frontend-implementer` | `react-frontend-patterns`, `react-tailwind-v4-components`, `frontend-design`, `react-tdd` | Reviewer loads `saurun:react-code-quality-reviewer-prompt` |
| Integration | Both agents | All skills (via agents) | Reviewer loads both criteria skills |

**Failure escalation:**

```
Task fails after 2 implementer retries
  -> Dispatch superpowers:systematic-debugging subagent
     Input: failing test output, relevant code, task spec
     Output: diagnosis + fix
  -> Apply fix, re-run review loop
  -> Still failing after 2 debugging retries -> STOP
     Write failure report to STATE.md
```

**Gate 3 Checklist:**
- [ ] Every plan in MANIFEST.json has status "Complete" in STATE.md
- [ ] `dotnet test backend/` passes with 0 failures
- [ ] `npm test` passes with 0 failures (if frontend exists)
- [ ] No unresolved entries in STATE.md Failures table
- [ ] Git working tree is clean (no uncommitted changes)

**On failure:** Identify which plan/task failed, dispatch `superpowers:systematic-debugging` with failure details, then re-run gate.

**Update STATE.md:** Phase 3 complete.

---

### Phase 4: Integration (Working Code -> Verified)

**Run verification first (as controller):**
```bash
dotnet test backend/
dotnet build backend/
npm test          # if frontend exists
npm run build     # if frontend exists
```
All pass -> dispatch integration subagent. Any fail -> `superpowers:systematic-debugging` (last chance).

**Dispatch subagent:**

```
Task(subagent_type="general-purpose", prompt="""
{AUTONOMOUS_PREAMBLE}

You are executing Phase 4 (Integration) of the god-agent pipeline.

SKILLS TO LOAD:
1. superpowers:finishing-a-development-branch
2. superpowers:verification-before-completion

STATE: {STATE.md contents}
PRODUCT SPEC: {spec summary}
ARCHITECTURE: {architecture summary}

TASKS:
1. Load finishing-a-development-branch skill and follow its process
2. Update CLAUDE.md Implementation Status section with newly built features
3. If greenfield with no remote -> commit to main
   If existing project -> create PR with summary
4. Write completion report to _docs/reports/{DATE}-{feature}-report.md

COMPLETION REPORT TEMPLATE: See references/completion-report-template.md
""")
```

**Gate 4 Checklist:**
- [ ] `dotnet test backend/` passes
- [ ] `dotnet build backend/` succeeds
- [ ] `npm test` passes (if frontend exists)
- [ ] `npm run build` succeeds (if frontend exists)
- [ ] Completion report exists at `_docs/reports/{DATE}-{feature}-report.md`
- [ ] Completion report has all sections populated
- [ ] No unresolved failures in STATE.md
- [ ] Git working tree is clean
- [ ] CLAUDE.md `## Implementation Status` section lists newly implemented features
- [ ] No security violations in STATE.md Security Log

**On failure:** Re-dispatch phase subagent with prompt including:
"Previous attempt failed Gate 4. Issues: {list unchecked items}. Fix these specific issues."

**Update STATE.md:** Phase 4 complete.

---

### Phase 5: E2E Testing (Non-Blocking)

**Skip if:** Extension mode AND no new UI components AND no User Flows in spec.

**Runs as:** Controller dispatches E2E subagent.

**Pre-dispatch (controller):**
1. Commit checkpoint:
   ```bash
   git add -A && git commit -m "chore: pre-e2e checkpoint - all unit/integration tests passing"
   ```

**Dispatch subagent:**

```
Task(subagent_type="general-purpose", prompt="""
{AUTONOMOUS_PREAMBLE}

You are executing Phase 5 (E2E Testing) of the god-agent pipeline.

SKILL TO LOAD: saurun:e2e-test (use Skill tool)

SPEC FILE: {spec_path}
ARCHITECTURE: {architecture_path}

STEPS:
1. Load saurun:e2e-test skill and execute with spec path: {spec_path}
2. Follow the skill's full execution flow (detect project, generate tests, run, fix loop, report)

REPORT BACK (print these exact lines at end):
E2E_TOTAL: {n}
E2E_PASSED: {n}
E2E_FIXED: {n}
E2E_FAILED: {n}
E2E_REPORT: {results_dir}/report.md
E2E_UNRESOLVED: {list or "none"}
""")
```

**Gate 5 Checklist (non-blocking — failures don't stop pipeline, but phase MUST execute):**
- [ ] Pre-E2E commit exists with message containing "pre-e2e checkpoint"
- [ ] E2E test files exist in `frontend/e2e/*.spec.ts`
- [ ] All User Flows from spec have corresponding test files
- [ ] Playwright ran successfully (process completed, regardless of test results)
- [ ] Report exists at `_docs/e2e-results/report.md`
- [ ] Videos exist for all tests that ran
- [ ] Fix attempts logged for any failures that were auto-fixed
- [ ] Unresolved failures have screenshots + traces in `_docs/e2e-results/failures/`

**Update STATE.md:**
- Add Phase 5 row to Phase Tracker with status (Complete/Partial)
- Add `## E2E Summary` section with pass/fix/fail counts
- Parse subagent's reported E2E_TOTAL/PASSED/FIXED/FAILED lines

**Update Completion Report:**
Add E2E results section (see updated template below).

**Note:** This phase is **mandatory but non-blocking** — it MUST execute and produces valuable artifacts (demo videos, test coverage), but failures don't stop the pipeline. If all tests fail after fix attempts, log the results and continue to Phase 6.

---

### Phase 6: Design Polish (Asset Generation)

**Skip if:** Extension mode AND no new UI components were added in Phase 3.

**Runs as:** Controller dispatches `saurun:design-polish-agent` (has `design-polish` + `nano-banana-pro` pre-loaded).

**Dispatch subagent:**

```
Task(subagent_type="saurun:design-polish-agent", prompt="""
{AUTONOMOUS_PREAMBLE}

You are executing Phase 6 (Design Polish) of the god-agent pipeline.

Spec path: {spec_path}

STATE CONTEXT (for reference — what was built in prior phases):
{summary of Phase 3 completed tasks and frontend components}

Follow the design-polish skill process. Both skills (design-polish + nano-banana-pro) are pre-loaded.

When complete, report: assets generated count, manual-needed count, placeholder status.
""")
```

**Gate 6 Checklist (non-blocking — failures don't stop pipeline, but phase MUST execute):**
- [ ] Asset inventory at `_docs/design-polish/asset-inventory.md`
- [ ] Generation log at `_docs/design-polish/generation-log.md`
- [ ] All hero images generated (or marked manual)
- [ ] All illustration assets generated (or marked manual)
- [ ] OG image + favicon generated
- [ ] No `data-asset=` placeholders remaining in code
- [ ] E2E tests still pass

**Update STATE.md:** Phase 6 complete, add asset summary.

---

### Post-Completion: Knowledge Capture

After Phase 4 gate passes and STATE.md is finalized, the **controller** runs one final step:

**Invoke skill:** `claude-md-management:revise-claude-md`

This captures learnings from the god-agent session into the project's CLAUDE.md:
- Patterns that worked well
- Gotchas encountered during implementation
- Architecture decisions worth preserving
- Stack-specific conventions established

This step is **non-blocking** — if it fails, log to STATE.md and continue. The pipeline is considered complete regardless.

**Done.**

---

## STATE.md Protocol

Written to `.god-agent/STATE.md`. Updated after every phase completion AND after every task within Phase 3. Template: See references/state-template.md

---

## Error Handling

**STOP Protocol — every STOP means ALL of these steps:**
1. Update STATE.md: set current phase status to `Failed`, record failure details in Failures table
2. Commit any uncommitted work to git (so nothing is lost)
3. Output to user: `God-agent STOPPED at Phase {X}, {task if applicable}: {one-line reason}. Fix the issue and re-invoke /god-agent to resume.`
4. Do NOT continue to the next phase or task. The session ends here.

**Subagent dispatch failure (API error):**
Retry same dispatch up to 2 times with backoff. Still failing -> STOP.

**Gate check failure:**
Re-dispatch same phase subagent with feedback listing specific issues. Up to 2 retries. Still failing -> STOP.

**Test suite failure (end of plan):**
Dispatch `superpowers:systematic-debugging` with failing test output + recent git diff + plan spec. Up to 2 debugging retries. Still failing -> STOP.

**Context exhaustion:**
STATE.md has exact position. All completed code is committed. All plan docs are on disk. Re-invoking `/god-agent` reads STATE.md and resumes from exact checkpoint. The `## Token Usage` table in STATE.md provides a cumulative token count — use this to gauge how much context you've consumed and whether a clean stop is approaching.

---

## Red Flags — STOP and Reassess

If you catch yourself thinking any of these, you are rationalizing. Stop and follow the rules.

| Rationalization | Reality |
|----------------|---------|
| "Phase 5/6 are non-blocking, I can skip them" | Non-blocking = failures tolerated. Execution is mandatory. |
| "Tests pass, reviewer is unnecessary" | Every task gets reviewed. No exceptions. |
| "This task is trivial / similar to the last one, skip it" | Every task in the plan gets implemented. Plans are the contract. |
| "Phase 4 passed, the pipeline is done" | Pipeline is done after Phase 6 + Post-Completion. Phase 4 = verified, not finished. |
| "Non-blocking means low effort is fine" | Execute with same rigor as blocking phases. Only failure *consequences* differ. |
| "This gate item is pedantic, it's fine" | Gates are the quality mechanism. Check every item. |
| "I'm running low on context, skip remaining phases" | Update STATE.md and STOP. Do not silently skip phases. Resume will pick up. |
| "The user won't notice if I skip this" | You are autonomous. Quality is your only constraint. |

---

## Autonomous Preamble (Reference)

Inject `{AUTONOMOUS_PREAMBLE}` into EVERY subagent dispatch. Content: See references/autonomous-preamble.md
