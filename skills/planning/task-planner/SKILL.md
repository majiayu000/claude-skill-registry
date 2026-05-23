---
name: task-planner
version: "3.1.0"
description: "This skill should be used when the user asks to 'plan this', 'orchestrate', 'break down', 'split into phases', 'coordinate tasks', 'create a plan', 'multi-step feature', or has complex tasks needing structured decomposition. Decomposes work into wave-based parallel tasks, assigns specialized agents, creates GitHub Issue for tracking, and manages execution through automated hooks."
---

# Task Planner - Full Orchestration Skill

Orchestrates the COMPLETE feature lifecycle: brainstorm → specify → clarify → architecture → decompose → execute.

**This is the SINGLE ENTRY POINT** for multi-step features. Spawns specialized agents for each phase.

---

## Arguments

- `/task-planner "description"` - Start new plan (runs full flow)
- `/task-planner --skip-specify` - Skip brainstorm/specify/clarify (use existing spec)
- `/task-planner --status` - Show current task graph status
- `/task-planner --complete` - Finalize, clean up state
- `/task-planner --abort` - Cancel mid-execution, clean state

---

## Full Orchestration Flow

```
/task-planner "feature description"
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│ Phase 0: BRAINSTORM (if unclear)                        │
│   Agent: brainstorm-agent                               │
│   Output: Refined understanding, selected approach      │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│ Phase 1: SPECIFY                                        │
│   Agent: specify-agent                                  │
│   Output: .claude/specs/{slug}/spec.md                  │
└─────────────────────────────────────────────────────────┘
        │
        ▼ (if >3 NEEDS CLARIFICATION markers)
┌─────────────────────────────────────────────────────────┐
│ Phase 2: CLARIFY                                        │
│   Agent: clarify-agent                                  │
│   Output: Updated spec.md with resolved uncertainties   │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│ Phase 3: ARCHITECTURE                                   │
│   Agent: architecture-agent                             │
│   Output: .claude/plans/{slug}.md                       │
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

## Phase 0: Brainstorm (Optional)

**When to run:** Feature description is vague, multiple approaches possible, or user says "explore" / "brainstorm".

**When to skip:** Clear scope, specific requirements, or user says "just build it".

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

## Phase 2: Clarify (Conditional)

**Run if:** spec has >3 `[NEEDS CLARIFICATION]` markers.

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

**Sizing heuristics** - decompose further if:
- Task touches >5 files
- Multiple unrelated concerns in one task
- Description needs "and" to explain

**Test requirements** - set `new_tests_required: false` for:
- migration, config, schema, rename, bump, version, refactor, cleanup, typo, docs
- Patterns: `→`, `->`, `interface update`

Helper: `~/.claude/hooks/helpers/detect-test-requirement.sh "desc"` → "true"/"false"

### 4b. Map Spec Anchors

Use helper to suggest anchors for each task:

```bash
~/.claude/hooks/helpers/suggest-spec-anchors.sh "task description" .claude/specs/*/spec.md
```

Returns JSON with suggested anchors and confidence scores:
```json
[{"anchor":"FR-003","score":0.85,"text":"System MUST validate email format"},...]
```

Review suggestions, adjust as needed, store as `spec_anchors: ["FR-003", "SC-002", "US1.acceptance"]`

### 4c. Assign Agents

| Agent (subagent_type) | Triggers |
|-------|----------|
| code-implementer-agent | implement, create, build, add, write code, model |
| architecture-agent | design, architecture, pattern, refactor |
| java-test-agent | test, junit, jqwik, property-based (Java) |
| ts-test-agent | vitest, playwright, react test (TypeScript) |
| security-agent | security, auth, jwt, oauth, vulnerability |
| dotfiles-agent | nix, nixos, home-manager, sops |
| k8s-agent | kubernetes, k8s, kubectl, helm, argocd |
| keycloak-agent | keycloak, realm, oidc, abac |
| frontend-agent | frontend, ui, react, next.js, component |

Fallback: `general-purpose`

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
gh issue create --title "Plan: {title}" --body "$(cat .claude/plans/{slug}.md)"
```

**B. State File:** `.claude/state/active_task_graph.json`
- Include `spec_file` and `plan_file` paths
- Include `spec_anchors` per task

---

## Phase 5: Execute

For each wave:

1. Get pending tasks in current wave
2. Spawn ALL wave tasks in parallel (single message, multiple Task calls)
3. Wait for all to reach "implemented"
4. Invoke `/wave-gate` (test + spec-check + review)
5. If passed: advance to next wave
6. If blocked: fix issues, re-run `/wave-gate`

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
2. Create `.claude/state/active_task_graph.json`
3. Hooks become active (block direct edits)

### On `/task-planner --status`:
```
Plan: Issue #42 - User Authentication
Phase: Execute (Wave 2/3)
Spec: .claude/specs/2025-01-29-user-auth/spec.md
Plan: .claude/plans/2025-01-29-user-auth.md

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
3. Hooks deactivate

---

## Hook Integration

Hooks auto-activate when `active_task_graph.json` exists:

| Hook | Event | Purpose |
|------|-------|---------|
| `block-direct-edits.sh` | PreToolUse: Edit/Write | Forces Task tool |
| `guard-state-file.sh` | PreToolUse: Bash | Blocks state writes |
| `validate-task-execution.sh` | PreToolUse: Task | Validates wave order |
| `update-task-status.sh` | SubagentStop | Marks "implemented" |
| `store-reviewer-findings.sh` | SubagentStop | Parses review findings |
| `store-spec-check-findings.sh` | SubagentStop | Parses spec-check findings |

**NEVER call helpers yourself.** All helpers (`mark-tests-passed.sh`, `complete-wave-gate.sh`, `verify-new-tests.sh`, etc.) run automatically via hooks or `/wave-gate`. Only exception: `detect-test-requirement.sh` during planning.

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
jq '.' .claude/state/active_task_graph.json

# Per-task status
jq '.tasks[] | {id, status, tests_passed, review_status}' .claude/state/active_task_graph.json

# Wave gate status
jq '.wave_gates' .claude/state/active_task_graph.json
```

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Task stuck `in_progress` | Agent crashed | Re-spawn same task |
| `tests_passed` missing | No recognizable output | Re-spawn, ensure test markers in output |
| Wave not advancing | Gate blocked | Check `wave_gates[N].blocked`, run `/wave-gate` |
| State write blocked | Guard hook active | State writes via hooks only; reads OK |

### Fixing Blocked Waves

When blocked (critical findings), Edit/Write blocked too. To fix:
1. **Re-spawn via Task** — create fix agent with findings context (subagent CAN Edit/Write)
2. **Run `/wave-gate`** — re-reviews only blocked tasks
3. **Emergency**: remove state file, fix manually, rebuild from GH issue

---

## Constraints

- **ALL phases via agents** - brainstorm, specify, clarify, architecture agents
- **ALL implementation via Task tool** - Edit/Write blocked
- **ALL state writes via hooks** - Bash writes blocked
- **NEVER skip specify** unless `--skip-specify` flag or spec exists
- **NEVER proceed with >3 unresolved markers** without user acknowledgment
- Only ONE active plan at a time

---

## Error Recovery

| Failure | Recovery |
|---------|----------|
| Brainstorm agent unclear | Re-spawn with more specific prompt |
| Specify agent too technical | Re-spawn with "focus on WHAT not HOW" |
| Clarify agent stuck | Ask user to resolve remaining markers |
| Architecture agent off-spec | Re-spawn referencing spec requirements |
| Implementation agent fails tests | Re-spawn with error context |
| Wave gate blocked | Fix issues, re-run `/wave-gate` |

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
