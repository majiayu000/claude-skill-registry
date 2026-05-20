---
name: execute-spec
description: >
  Use when a complete spec or PRD already exists and needs to be turned into working, tested, committed code.

  DO NOT USE FOR: Rough ideas without a spec (use god-agent), bug fixes, single-layer work, non-.NET/React projects.
user-invocable: true
argument-hint: "_docs/specs/my-feature-spec.md"
---

# Execute-Spec: Spec-to-Code Pipeline

**Version: 1.0.0**

> **ANNOUNCE AT STARTUP:** "Starting execute-spec v1.0.0"

Take an existing spec/PRD and deliver working, tested, reviewed, committed code. No brainstorming, no e2e, no design polish — straight to architecture, planning, execution.

**Input:** Path to spec/PRD file via `$ARGUMENTS`. Optional "Preferences: ..." suffix.

**Required stack:** .NET 9 + React 19 + Tailwind v4 + Zustand + SQLite. Existing spec file.

**Commitment:** Long-running (20+ min), resumable via STATE.md.

**Tech stack (always):** .NET 9, ASP.NET Core, EF Core 9, SQLite, SignalR, React 19, Vite, TypeScript, Tailwind CSS v4, Zustand.

**Subagent dispatch (always):** Run subagents in foreground. Never use `run_in_background`. When tasks are independent (e.g., Phase 2 planning for different work units), dispatch them in parallel by including multiple Task calls in a single message. Wait for all to complete before proceeding.

**Token tracking (always):** Every Task tool response includes a `<usage>` block with `total_tokens`, `tool_uses`, and `duration_ms`. After EVERY subagent dispatch (all phases), append a row to STATE.md `## Token Usage` table:

```
| {phase_number} | {task_or_phase_name} | {role} | {total_tokens} | {tool_uses} | {duration_ms}ms |
```

Phase column: use number only (e.g., `1`, not `Phase 1`).
Role values: `implementer`, `reviewer`, `planner`, `debugger`. For retries, append `-retry` (e.g., `implementer-retry`, `reviewer-retry`).

Update the cumulative line: `**Cumulative:** {sum} tokens across {count} subagent dispatches`

## Phase Overview

| Phase | Name | Gate | Output Artifact |
|-------|------|------|-----------------|
| 1 | Architecture | Blocking | `_docs/specs/{DATE}-{feature}-architecture.md` |
| 2 | Planning | Blocking | `_docs/plans/*.md` + `MANIFEST.json` |
| 2b | Verify Plan Coverage | Blocking | Coverage report (logged to STATE.md) |
| 3 | Execution | Blocking | Working code, passing tests |
| 4 | Integration | Blocking | `_docs/reports/{DATE}-{feature}-report.md` |

## Step 1: Pre-Flight

**Note:** Pre-flight runs as the controller with the user present. AskUserQuestion is allowed here. The autonomous preamble (`{AUTONOMOUS_PREAMBLE}`) only applies to dispatched subagents, not the controller.

Before anything else:

1. **Parse input.** Extract spec path from `$ARGUMENTS`. Look for optional "Preferences:" suffix.

2. **Validate spec.** Read the spec file. If it doesn't exist or is empty: STOP with `"Spec file not found or empty: {path}. Provide a valid spec path."`.

3. **Ask worktree question.** Use AskUserQuestion (one question only):
   - "Use a git worktree for this feature?"
   - Options: "Yes — create feature branch + worktree" / "No — work in current directory"
   - If yes:
     - Derive `{feature-name}` from spec title (kebab-case)
     - Create branch: `git branch feature/{feature-name}` (from current HEAD)
     - Create worktree: `git worktree add ../worktrees/{feature-name} feature/{feature-name}`
     - `cd` into the worktree directory
     - Open in VS Code: `code {worktree-path}`
   - If no: continue in current directory

4. **Detect mode.**
   - `CLAUDE.md` exists in project root → **Extension Mode** (build into existing codebase)
   - No `CLAUDE.md` → **Greenfield Mode** (scaffold first, then build)

5. **Greenfield scaffold (if applicable).**
   If greenfield mode: load `saurun:scaffold` via Skill tool with current path.
   Verify: `backend/`, `frontend/`, `CLAUDE.md`, `.gitignore` all exist after scaffold.

6. **Check for resume.** If `.execute-spec/STATE.md` exists:
   - Read it
   - Find last completed phase
   - Read that phase's output artifact
   - Log `[RESUMED] from Phase {X}` in STATE.md
   - Skip to the next incomplete phase (or sub-position within a phase)

7. **Required skills and agents (verified lazily per phase):**

   Skills (loaded by subagents, never by the controller):
   - `saurun:scaffold` (Pre-flight — greenfield only)
   - `saurun:dotnet-tactical-ddd` (Phase 1)
   - `saurun:react-frontend-patterns` (Phase 1)
   - `saurun:dotnet-writing-plans` (Phase 2 — backend)
   - `saurun:react-writing-plans` (Phase 2 — frontend)
   - `saurun:verify-plan-coverage` (Phase 2b)
   - `saurun:dotnet-code-quality-reviewer-prompt` (Phase 3)
   - `saurun:react-code-quality-reviewer-prompt` (Phase 3)
   - `superpowers:systematic-debugging` (Phase 3)
   - `superpowers:finishing-a-development-branch` (Phase 4)
   - `superpowers:verification-before-completion` (Phase 4)
   - `claude-md-management:revise-claude-md` (Post-Completion)

   Required agents (have skills pre-loaded):
   - `saurun:backend-implementer` (has `dotnet-tactical-ddd` + `dotnet-tdd`) — Phase 3
   - `saurun:frontend-implementer` (has `react-frontend-patterns` + `frontend-design` + `react-tdd`) — Phase 3

8. **Read context layers** (in priority order):

   | Layer | Source | When |
   |-------|--------|------|
   | Spec content | The spec file from `$ARGUMENTS` | Always |
   | Injected context | User preferences from input string | If provided |
   | Project context | `CLAUDE.md`, `_docs/`, existing code | Extension mode |
   | Stack defaults | .NET 9, React 19, Tailwind v4, Zustand, SQLite | Always (hardcoded) |

9. **Write initial STATE.md** to `.execute-spec/STATE.md` (see STATE.md Protocol below).

---

## How Gates Work

After each phase completes, the **controller** (not the subagent) validates the output by reading the artifact and running through the gate checklist:

1. **Read artifact** — controller reads the phase output (architecture doc, plan files, etc.)
2. **Run checklist** — controller checks each item in the gate checklist
3. **Pass** — all items checked → proceed to next phase
4. **Fail** — one or more items unchecked → re-dispatch subagent with: `"Gate N failed: {unchecked items}. Fix these."`
5. **Retry limit** — up to 2 re-dispatches per gate. Still failing → log to STATE.md and STOP.

---

## Step 2: Execute Phases

Run phases 1 through 4 sequentially. ALL phases MUST be executed. After each phase: update STATE.md, run gate check. If gate fails: re-dispatch with feedback (up to 2 retries). If still failing: log to STATE.md and STOP.

---

### Phase 1: Architecture (Spec -> Technical Design)

**Dispatch subagent:**

```
Task(subagent_type="general-purpose", prompt="""
{AUTONOMOUS_PREAMBLE}

You are executing Phase 1 (Architecture) of the execute-spec pipeline.

PRODUCT SPEC: {contents of the spec file}

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
2. Update .execute-spec/STATE.md with architecture decisions

CONCISENESS RULES (this doc is for autonomous agents, not humans):
- NO redundancy: information appears ONCE in the most logical place
- NO full code: method signatures only, not implementations
- NO obvious patterns: don't describe standard TanStack Query or EF Core flows
- NO separate validation section: put validation inline in DTOs as comments
- Rich entities: list method signatures only (e.g., Create(), AddItem(), RemoveItem())
- Anemic entities: just name and properties, no behavior section
- Data Flow: ONLY describe non-standard flows or critical decisions
- Infrastructure: ONLY non-default choices (skip "EF Core code-first migrations")

ARCHITECTURE TEMPLATE:
{controller reads references/architecture-template.md and injects contents here}
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

You are executing Phase 2 (Planning) of the execute-spec pipeline.
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
  "feature": "{feature-name}",
  "created": "{ISO timestamp}",
  "spec_path": "{path to input spec}",
  "plans": [
    {"id": "backend-domain", "path": "_docs/plans/{DATE}-backend-domain.md"},
    {"id": "backend-api", "path": "_docs/plans/{DATE}-backend-api.md"},
    {"id": "frontend-state", "path": "_docs/plans/{DATE}-frontend-state.md"},
    {"id": "frontend-pages", "path": "_docs/plans/{DATE}-frontend-pages.md"}
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

### Phase 2b: Verify Plan Coverage

**Why:** Plans silently drop ~14% of requirements. This step catches gaps before execution begins.

**Dispatch subagent:**

```
Task(subagent_type="general-purpose", prompt="""
{AUTONOMOUS_PREAMBLE}

You are executing Phase 2b (Verify Plan Coverage) of the execute-spec pipeline.

SKILL TO LOAD: saurun:verify-plan-coverage (use Skill tool)

INPUTS:
- Spec: {spec_path}
- Architecture: {architecture_doc_path}
- Plans: MANIFEST.json at _docs/plans/MANIFEST.json

Load the skill and execute its full algorithm. The skill will cross-reference
spec + architecture against all plans and produce a coverage report.

OUTPUT: Print the full PLAN COVERAGE REPORT to stdout.
""")
```

**Gate 2b Checklist:**
- [ ] Coverage report was produced
- [ ] Spec coverage ≥ 90% (COVERED status)
- [ ] Architecture coverage ≥ 95% (COVERED status)
- [ ] Zero MUTATED items (value mismatches between spec and plan)
- [ ] Zero ORPHAN tasks (tasks referencing non-existent contracts)

**On failure (coverage gaps found):**
1. Read the FIXES NEEDED section from the coverage report
2. Map gaps to planners: check which plan file each gap belongs to (the report lists plan file per item). Backend gaps → re-dispatch with `saurun:dotnet-writing-plans`. Frontend gaps → re-dispatch with `saurun:react-writing-plans`. Include the specific fix instructions from the report in the re-dispatch prompt.
3. For each MUTATED item: edit the plan file directly to correct the value (controller does this, no subagent needed)
4. Re-run verify-plan-coverage (up to 2 retries)
5. If coverage still below thresholds after retries: log gaps to STATE.md and proceed with a warning (do NOT STOP — partial coverage is better than no execution)

**Update STATE.md:** Phase 2b complete, record coverage percentages.

---

### Phase 3: Execution (Plans -> Working Code)

**You (the controller) run this directly.** Do NOT delegate Phase 3 to a single subagent. You orchestrate the task loop yourself, dispatching individual implementer/reviewer subagents per task. This preserves cross-phase context from Phases 1-2.

**Do NOT load any skills in the controller.** The orchestration logic is fully defined below. All skill usage happens inside dispatched subagents.

**Orchestration guardrails:**
- Never dispatch multiple implementation subagents in parallel (file conflicts)
- Never skip reviews — every task gets reviewed, no exceptions
- If reviewer finds issues → implementer fixes → re-review. Do NOT skip the re-review.
- If implementer asks questions → answer from spec/architecture context before letting them proceed
- Do not fix implementer failures manually (context pollution) — re-dispatch or escalate to `systematic-debugging`

**Orchestration loop:**

```
Read MANIFEST.json -> plans array defines execution order
Read architecture doc ONCE (for contract extraction)

# Extract style summary for frontend tasks (read once)
If design-system/MASTER.md exists:
  Extract from MASTER.md:
    - Style name, primary/accent/background colors, fonts, mood keywords
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
       - If implementer asks questions -> answer from spec/architecture context
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
Do NOT spend time sourcing real images.

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

### Phase 4: Integration (Working Code -> Verified & Committed)

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

You are executing Phase 4 (Integration) of the execute-spec pipeline.

SKILLS TO LOAD:
1. superpowers:finishing-a-development-branch
2. superpowers:verification-before-completion

STATE: {STATE.md contents}
PRODUCT SPEC: {spec summary}
ARCHITECTURE: {architecture summary}

WORKTREE: {yes/no from pre-flight step 3}
MODE: {Greenfield | Extension}

TASKS:
1. Load finishing-a-development-branch skill and follow its process
2. Update CLAUDE.md Implementation Status section with newly built features
3. Commit and/or PR based on context:
   - Worktree enabled (feature branch) -> commit all work, push branch, create PR with summary
   - Extension mode, no worktree (on main) -> commit with summary
   - Greenfield mode, no worktree (on main, no remote) -> commit with summary
4. Write completion report to _docs/reports/{DATE}-{feature}-report.md

COMPLETION REPORT TEMPLATE:
{controller reads references/completion-report-template.md and injects contents here}
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

### Post-Completion: Knowledge Capture

After Phase 4 gate passes, the **controller** dispatches one final subagent:

```
Task(subagent_type="general-purpose", prompt="""
{AUTONOMOUS_PREAMBLE}

You are executing Post-Completion (Knowledge Capture) of the execute-spec pipeline.

SKILL TO LOAD: claude-md-management:revise-claude-md (use Skill tool)

FEATURE SUMMARY: {spec title and one-line description}
ARCHITECTURE SUMMARY: {key entities, endpoints, components built}
STATE: {STATE.md contents}

Analyze what was built in this session and update the project's CLAUDE.md
with patterns, conventions, and implementation details that future sessions should know.
""")
```

Non-blocking — if it fails, log and continue. Pipeline is complete regardless.

**Done.**

---

## STATE.md Protocol

Written to `.execute-spec/STATE.md`. Updated after every phase completion AND after every task within Phase 3. Template: See references/state-template.md

---

## Error Handling

**STOP Protocol — every STOP means ALL of these steps:**
1. Update STATE.md: set current phase status to `Failed`, record failure details in Failures table
2. Commit any uncommitted work to git (so nothing is lost)
3. Output to user: `Execute-spec STOPPED at Phase {X}, {task if applicable}: {one-line reason}. Fix the issue and re-invoke /execute-spec to resume.`
4. Do NOT continue to the next phase or task. The session ends here.

**Subagent dispatch failure (API error):**
Retry same dispatch up to 2 times with backoff. Still failing -> STOP.

**Gate check failure:**
Re-dispatch same phase subagent with feedback listing specific issues. Up to 2 retries. Still failing -> STOP.

**Test suite failure (end of plan):**
Dispatch `superpowers:systematic-debugging` with failing test output + recent git diff + plan spec. Up to 2 debugging retries. Still failing -> STOP.

**Context exhaustion:**
STATE.md has exact position. All completed code is committed. All plan docs are on disk. Re-invoking `/execute-spec` reads STATE.md and resumes from exact checkpoint. The `## Token Usage` table in STATE.md provides a cumulative token count — use this to gauge how much context you've consumed and whether a clean stop is approaching.

---

## Red Flags — STOP and Reassess

If you catch yourself thinking any of these, you are rationalizing. Stop and follow the rules.

| Rationalization | Reality |
|----------------|---------|
| "I'll dispatch multiple implementers in parallel to go faster" | File conflicts. One implementer at a time, always. |
| "Tests pass, reviewer is unnecessary" | Every task gets reviewed. No exceptions. |
| "This task is trivial / similar to the last one, skip it" | Every task in the plan gets implemented. Plans are the contract. |
| "This gate item is pedantic, it's fine" | Gates are the quality mechanism. Check every item. |
| "I'm running low on context, skip remaining phases" | Update STATE.md and STOP. Do not silently skip phases. Resume will pick up. |
| "The user won't notice if I skip this" | You are autonomous. Quality is your only constraint. |
| "The spec is vague here, I'll just guess" | Log the assumption in STATE.md Assumptions Log. Make reasonable decision, don't skip. |
| "I'll skip the architecture phase, the spec is detailed enough" | Architecture phase derives entity model, API contracts, test layers. Spec doesn't have these. |
| "Worktree setup failed, I'll just work in-place" | If user requested worktree: fix or STOP. Don't silently change scope. |

---

## Autonomous Preamble (Reference)

Inject `{AUTONOMOUS_PREAMBLE}` into EVERY subagent dispatch. Content: See references/autonomous-preamble.md
