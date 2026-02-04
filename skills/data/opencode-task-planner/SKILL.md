---
name: opencode-task-planner
description: "This skill should be used when the user asks to 'plan this', 'orchestrate', 'break down', 'split into phases', 'coordinate tasks', 'create a plan', 'multi-step feature', or has complex tasks needing structured decomposition. Decomposes work into wave-based parallel tasks, assigns specialized agents, creates GitHub Issue for tracking, and manages execution through automated hooks."
---

# Task Planner - Full Orchestration Skill

Orchestrates the COMPLETE feature lifecycle: brainstorm → specify → clarify → architecture → decompose → execute.

**This is the SINGLE ENTRY POINT** for multi-step features. Spawns specialized agents for each phase.

---

## Arguments

- `/task-planner "description"` - Start new plan (runs full flow)
- `/task-planner --skip-brainstorm` - Skip brainstorm phase (scope already clear)
- `/task-planner --skip-clarify` - Skip clarify phase (accept markers as-is)
- `/task-planner --skip-specify` - Skip brainstorm/specify/clarify (use existing spec)
- `/task-planner --status` - Show current task graph status
- `/task-planner --complete` - Finalize, clean up state
- `/task-planner --abort` - Cancel mid-execution, clean state

**Note:** All phases are MANDATORY by default. Skip flags allow explicit bypass with user acknowledgment.

---

## Full Orchestration Flow

```
/task-planner "feature description"
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│ Phase 0: BRAINSTORM [MANDATORY]                         │
│   Agent: brainstorm-agent                               │
│   Output: Refined understanding, selected approach      │
│   Skip: --skip-brainstorm                               │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│ Phase 1: SPECIFY [MANDATORY]                            │
│   Agent: specify-agent                                  │
│   Output: .opencode/specs/{slug}/spec.md                │
└─────────────────────────────────────────────────────────┘
        │
        ▼ (if >3 markers, else skip to ARCHITECTURE)
┌─────────────────────────────────────────────────────────┐
│ Phase 2: CLARIFY [MANDATORY if markers > 3]             │
│   Agent: clarify-agent                                  │
│   Output: Updated spec.md with resolved uncertainties   │
│   Skip: --skip-clarify                                  │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│ Phase 3: ARCHITECTURE                                   │
│   Agent: architecture-agent                             │
│   Output: .opencode/plans/{slug}.md                     │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│ Phase 4: DECOMPOSE                                      │
│   Extract tasks, assign agents, schedule waves          │
│   Output: Task graph + GitHub Issue                     │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│ Phase 5: EXECUTE (wave by wave)                         │
│   Spawn impl agents → wave-gate → advance               │
│   Output: Working implementation                        │
└─────────────────────────────────────────────────────────┘
```

---

## Phase 0: Brainstorm (MANDATORY)

**Always run** unless `--skip-brainstorm` flag provided.

**Plugin enforcement:** `validate-phase-order` hook blocks specify-agent if brainstorm not complete (unless skipped).

**Spawn brainstorm-agent** with context from `templates/phase-brainstorm.md`.

Substitute variables:
- `{feature_description}` - User's original request
- `{prior_context}` - Any notes from prior exploration

**Wait for agent completion.** Extract:
- Refined feature description
- Selected approach
- Key constraints

Pass to Phase 1.

---

## Phase 1: Specify

**Always run** (unless `--skip-specify` or spec already exists).

**Spawn specify-agent** with context from `templates/phase-specify.md`.

Substitute variables:
- `{feature_description}` - Refined description (from brainstorm or original)
- `{brainstorm_output}` - Summary from Phase 0 (or empty)
- `{date_slug}` - `YYYY-MM-DD-feature-name` format

**Wait for agent completion.** Extract:
- Spec file path
- Count of `[NEEDS CLARIFICATION]` markers

If markers > 3: Proceed to Phase 2.
If markers <= 3: Skip to Phase 3.

---

## Phase 2: Clarify (MANDATORY if markers > 3)

**Run if:** spec has >3 `[NEEDS CLARIFICATION]` markers. Skip via `--skip-clarify` if accepting markers as-is.

**Plugin enforcement:** `validate-phase-order` hook blocks architecture-agent if markers > 3 (unless clarify skipped).

**Spawn clarify-agent** with context from `templates/phase-clarify.md`.

Substitute variables:
- `{spec_file_path}` - Path to spec from Phase 1
- `{marker_count}` - Number of `[NEEDS CLARIFICATION]` markers

**Wait for agent completion.** Verify markers resolved.

If still >3 markers: Ask user to resolve remaining, or proceed with caveats.

---

## Phase 3: Architecture

**Always run.**

**Spawn architecture-agent** with context from `templates/phase-architecture.md`.

Substitute variables:
- `{feature_description}` - Feature name/description
- `{spec_file_path}` - Path to spec from Phase 1
- `{date_slug}` - `YYYY-MM-DD-feature-name` format

**Wait for agent completion.** Extract:
- Plan file path
- Implementation phases

---

## Phase 4: Decompose

**Run inline** (no agent spawn needed).

### 4a. Extract Tasks

Parse plan into tasks. **Design = the plan itself, NOT a tracked task**:

```
T1: Create User domain model (+ tests)
T2: Implement JWT service (+ tests)
T3: Add login endpoint (+ tests)
```

**CRITICAL: Implementation tasks INCLUDE tests.** Do NOT create separate test tasks for new code. The `code-implementer-agent` writes both implementation AND tests (per impl-agent-context.md). Separate test tasks cause circular dependencies:
- Test task depends on impl task (can't test what doesn't exist)
- Impl task already writes tests
- Test task blocked waiting for impl "completed", but wave-gate needs test task evidence → deadlock

**When to use test-only agents (`java-test-agent`, `ts-test-agent`):**
- Adding tests to EXISTING code that lacks coverage
- Task description: "Add missing tests for X" (not "Write tests for new X")

**Sizing heuristics** - decompose further if:
- Task touches >5 files
- Multiple unrelated concerns in one task
- Description needs "and" to explain

**Test requirements** - set `new_tests_required: false` for:
- migration, config, schema, rename, bump, version, refactor, cleanup, typo, docs
- Patterns: `→`, `->`, `interface update`

### 4b. Map Spec Anchors

Link each task to spec requirements (FR-xxx, SC-xxx, US-x.acceptance[N]):

```json
[{"anchor":"FR-003","score":0.85,"text":"System MUST validate email format"},...]
```

Review suggestions, adjust as needed, store as `spec_anchors: ["FR-003", "SC-002", "US1.acceptance"]`

### 4c. Assign Agents

| Agent (subagent_type) | Triggers |
|-------|----------|
| code-implementer-agent | implement, create, build, add, write code, model — **writes tests too** |
| architecture-agent | design, architecture, pattern, refactor |
| java-test-agent | add missing tests to EXISTING Java code only |
| ts-test-agent | add missing tests to EXISTING TypeScript code only |
| security-agent | security, auth, jwt, oauth, vulnerability |
| dotfiles-agent | nix, nixos, home-manager, sops |
| k8s-agent | kubernetes, k8s, kubectl, helm, argocd |
| keycloak-agent | keycloak, realm, oidc, abac |
| frontend-agent | frontend, ui, react, next.js, component — **writes tests too** |

Fallback: `general-purpose`

**Note:** `java-test-agent` and `ts-test-agent` are for backfilling tests on existing code, NOT for testing new implementations. New code gets tests from impl agents.

### 4d. Schedule Waves

```
Wave 1: Tasks with no dependencies (run parallel)
Wave 2: Tasks depending on Wave 1
Wave N: Tasks depending on Wave N-1
```

### 4e. User Approval

Present plan summary:
- Spec path
- Plan path
- Task breakdown with agents
- Wave schedule
- GitHub Issue will be created

Ask: "Proceed with this plan?"

### 4f. Create Artifacts

On approval:

**A. GitHub Issue:**
```bash
gh issue create --title "Plan: {title}" --body "$(cat .opencode/plans/{slug}.md)"
```

**B. State File:** `.opencode/state/active_task_graph.json`
- Include `spec_file` and `plan_file` paths
- Include `spec_anchors` per task

---

## Phase 5: Execute

For each wave:

1. Get pending tasks in current wave
2. Spawn ALL wave tasks in parallel (single message, multiple Task calls)
3. Wait for all to reach "implemented"
4. Invoke `/opencode-wave-gate` (test + spec-check + review)
5. If passed: advance to next wave
6. If blocked: fix issues, re-run `/opencode-wave-gate`

**Agent context:** Use `templates/impl-agent-context.md` for each task.

Substitute variables:
- `{task_id}`, `{wave}`, `{agent_type}`, `{dependencies}`
- `{task_description}` - From task breakdown
- `{spec_anchors_formatted}` - Formatted anchor list with requirement text
- `{plan_context}` - Relevant section from plan
- `{file_list}` - Files to create/modify
- `{plan_file_path}` - Path to full plan

---

## Quick Start Examples

### Full flow (recommended):
```
/task-planner "Add user authentication with email/password"
```
Runs: brainstorm → specify → clarify → arch → decompose → execute

### Skip to architecture (spec exists):
```
/task-planner --skip-specify "Add user authentication"
```
Runs: arch → decompose → execute (uses existing spec)

### Simple feature (clear scope):
```
/task-planner "Add logout button to navbar"
```
Detects simple → may skip brainstorm, minimal spec

---

## State Management

### On `/task-planner "description"`:
1. Run phases 0-4
2. Create `.opencode/state/active_task_graph.json`
3. Plugin hooks become active (block direct edits)

### On `/task-planner --status`:
```
Plan: Issue #42 - User Authentication
Phase: Execute (Wave 2/3)
Spec: .opencode/specs/2025-01-29-user-auth/spec.md
Plan: .opencode/plans/2025-01-29-user-auth.md

[✓] T1: User model (code-implementer) — tests: PASS
[✓] T2: JWT service (code-implementer) — tests: PASS
[→] T3: Login endpoint (code-implementer) — tests: pending
```

### On `/task-planner --complete`:
1. Verify all tasks completed
2. Optionally close GitHub Issue
3. Remove state file
4. Invoke `/finalize` for PR

### On `/task-planner --abort`:
1. Ask: close issue or leave open?
2. Remove state file
3. Plugin hooks deactivate

---

## Plugin Hook Integration

Hooks auto-activate when `active_task_graph.json` exists:

| Hook | Event | Purpose |
|------|-------|---------|
| `block-direct-edits` | tool.execute.before: Edit/Write | Forces Task tool |
| `guard-state-file` | tool.execute.before: Bash | Blocks state writes |
| `validate-task-execution` | tool.execute.before: Task | Validates wave order |
| `update-task-status` | session.idle | Marks "implemented" |
| `store-review-findings` | session.idle | Parses review findings |
| `parse-spec-check` | session.idle | Parses spec-check findings |

**NEVER write to state file directly.** All state updates happen via plugin hooks. Only exception during planning: initial state file creation.

---

## Operations Reference

### Status Transitions

```
pending → in_progress    (task spawned to agent)
in_progress → implemented (agent completes, hook extracts test evidence)
implemented → completed   (wave gate passed: tests + review + no critical findings)
```

### Observability

```bash
# Current state
jq '.' .opencode/state/active_task_graph.json

# Per-task status
jq '.tasks[] | {id, status, tests_passed, review_status}' .opencode/state/active_task_graph.json

# Wave gate status
jq '.wave_gates' .opencode/state/active_task_graph.json
```

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Task stuck `in_progress` | Agent crashed | Re-spawn same task |
| `tests_passed` missing | No recognizable output | Re-spawn, ensure test markers in output |
| Wave not advancing | Gate blocked | Check `wave_gates[N].blocked`, run `/opencode-wave-gate` |
| State write blocked | Guard hook active | State writes via hooks only; reads OK |
| Test task blocked, impl wrote tests | Separate test task for new code | Don't create separate test tasks; mark superseded or merge |

### Fixing Blocked Waves

When blocked (critical findings), Edit/Write blocked too. To fix:
1. **Re-spawn via Task** — create fix agent with findings context (subagent CAN Edit/Write)
2. **Run `/opencode-wave-gate`** — re-reviews only blocked tasks
3. **Emergency**: remove state file, fix manually, rebuild from GH issue

---

## Constraints

- **ALL phases via agents** - brainstorm, specify, clarify, architecture agents
- **ALL implementation via Task tool** - Edit/Write blocked
- **ALL state writes via hooks** - Bash writes blocked
- **NEVER skip phases** unless explicit `--skip-X` flag provided
- **NEVER proceed with >3 unresolved markers** without user acknowledgment or `--skip-clarify`
- Only ONE active plan at a time

---

## Phase Enforcement (Plugin)

The task-planner plugin enforces phase ordering:

### tool.execute.before: `validate-phase-order`
Blocks agent spawns if prerequisite phases not complete.

| Target Agent | Requires |
|--------------|----------|
| specify-agent | brainstorm complete OR `--skip-brainstorm` |
| clarify-agent | spec.md exists |
| architecture-agent | spec.md exists + markers ≤ 3 OR `--skip-clarify` |
| impl agents | plan.md exists |

### session.idle: `advance-phase`
Advances `current_phase` when phase agents complete.

| Agent Completes | Next Phase |
|-----------------|------------|
| brainstorm-agent | specify |
| specify-agent | clarify (if markers > 3) OR architecture |
| clarify-agent | architecture |
| architecture-agent | decompose |

### State Tracking

```json
{
  "current_phase": "specify",
  "phase_artifacts": {
    "brainstorm": "completed",
    "specify": null,
    "clarify": null,
    "architecture": null
  },
  "skipped_phases": ["clarify"]
}
```

### Skip Flags

- `--skip-brainstorm` - Adds "brainstorm" to `skipped_phases`, starts at specify
- `--skip-clarify` - Adds "clarify" to `skipped_phases`, proceeds to architecture regardless of markers
- `--skip-specify` - Adds brainstorm, specify, clarify to skipped; requires existing spec.md

---

## Error Recovery

| Failure | Recovery |
|---------|----------|
| Brainstorm agent unclear | Re-spawn with more specific prompt |
| Specify agent too technical | Re-spawn with "focus on WHAT not HOW" |
| Clarify agent stuck | Ask user to resolve remaining markers |
| Architecture agent off-spec | Re-spawn referencing spec requirements |
| Implementation agent fails tests | Re-spawn with error context |
| Wave gate blocked | Fix issues, re-run `/opencode-wave-gate` |

---

## Plan Limits

- **Max tasks:** 8-12 (split if larger)
- **Max waves:** 4-5
- **Max parallel tasks per wave:** 4-6

---

## CRITICAL: Agent Spawning

Each phase spawns ONE agent (except Execute which spawns wave tasks in parallel).

**Sequential phases:** brainstorm → specify → clarify → architecture
**Parallel within wave:** T1, T2, T3 in same message

Pass context forward between phases via agent outputs.
