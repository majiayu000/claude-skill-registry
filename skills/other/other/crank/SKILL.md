---
name: crank
description: 'Hands-free epic execution. Runs until ALL children are CLOSED. Uses /swarm with runtime-native spawning (Codex sub-agents or Claude teams). NO human prompts, NO stopping. Triggers: "crank", "run epic", "execute epic", "run all tasks", "hands-free execution", "crank it".'
skill_api_version: 1
user-invocable: true
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: full
metadata:
  tier: execution
  dependencies:
    - swarm       # required - executes each wave
    - vibe        # required - final validation
    - implement   # required - individual issue execution
    - beads       # optional - issue tracking via bd CLI (fallback: TaskList)
    - post-mortem # optional - suggested for learnings extraction
output_contract: "code changes across wave execution, .agents/swarm/results/*.json"
---

# Crank Skill

> **Quick Ref:** Autonomous epic execution. `/swarm` for each wave with runtime-native spawning. Output: closed issues + phase-2 handoff for `/validation`.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Autonomous execution: implement all issues until the epic is DONE.

**CLI dependencies:** bd (issue tracking), ao (knowledge flywheel). Both optional — see `skills/shared/SKILL.md` for fallback table. If bd is unavailable, use TaskList for issue tracking and skip beads sync. If ao is unavailable, skip knowledge injection/extraction.

For Claude runtime feature coverage (agents/hooks/worktree/settings), the shared source of truth is `skills/shared/references/claude-code-latest-features.md`, mirrored locally at `references/claude-code-latest-features.md`.

## Architecture: Crank + Swarm

Crank owns orchestration, epic/task lifecycle, and knowledge-flywheel steps. Swarm owns runtime-native worker spawning, fresh-context isolation, per-wave execution, and cleanup. In beads mode Crank gets each wave from `bd ready`, bridges issues into worker tasks, verifies results, and syncs status back to beads. In TaskList mode the same loop runs over pending unblocked tasks instead of beads issues.

Read `references/team-coordination.md` for the full per-wave execution model and `references/ralph-loop-contract.md` for the fresh-context worker contract.

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--test-first` | off | Enable spec-first TDD: SPEC WAVE generates contracts, TEST WAVE generates failing tests, IMPL WAVES make tests pass |
| `--per-task-commits` | off | Opt-in per-task commit strategy. Falls back to wave-batch when file boundaries overlap. See `references/commit-strategies.md`. |
| `--tier=<name>` | (auto) | Force a specific cost tier (quality/balanced/budget) for all council calls. Overrides effort-to-tier auto-mapping. |
| `--no-lifecycle` | off | Skip ALL lifecycle skill auto-invocations (test delegation in TEST WAVE, pre-vibe deps/test checks) |
| `--lifecycle=<tier>` | matches complexity | Controls which lifecycle skills fire: `minimal` (test only), `standard` (+deps vuln), `full` (all) |
| `--no-scope-check` | off | Skip scope-completion check before DONE marker (Step 8.7) |
| `--skip-audit` | off | Skip bd-audit pre-flight gate (Step 3a.2) |

## Global Limits

**MAX_EPIC_WAVES = 50** (hard limit across entire epic)

This prevents infinite loops on circular dependencies or cascading failures. Typical epics use 5–10 waves max.

## Completion Enforcement (The Sisyphus Rule)

Not done until you emit an explicit completion marker after each wave:
- `<promise>DONE</promise>` when the epic is truly complete
- `<promise>BLOCKED</promise>` when progress cannot continue
- `<promise>PARTIAL</promise>` when work remains

Never claim completion without one of these markers.

## Node Repair Operator

When a task fails during wave execution, classify as **RETRY** (transient — re-add with adjustment, max 2), **DECOMPOSE** (too complex — split into sub-issues, terminal), or **PRUNE** (blocked — escalate immediately). Budget: 2 per task. Read `references/failure-recovery.md` for classification signals and recovery commands.

**Mutation logging on failure classification:**
- **DECOMPOSE:** Log `task_removed` for the original task, then `task_added` for each new sub-task.
- **PRUNE:** Log `task_removed` with the block reason.
- **RETRY:** No mutation (task identity unchanged).

## Execution Steps

Given `/crank [epic-id | .agents/rpi/execution-packet.json | plan-file.md | "description"]`:

### Recovery Hooks

Register a `PostCompact` hook: `"command": "cat .agents/crank/wave-*-checkpoint.json | tail -1"` to auto-recover wave state after compaction. Consider `worktree.sparsePaths` to reduce worktree size.

**Effort levels per worker type:**

| Worker Role | Recommended Effort | Rationale |
|-------------|-------------------|-----------|
| SPEC wave (contracts) | `medium` | Balanced reasoning for spec generation |
| TEST wave (failing tests) | `medium` | Test scaffolding needs moderate depth |
| IMPL wave (make tests pass) | `high` | Deep reasoning for correct implementation |
| Docs/chore tasks | `low` | Fast execution for simple tasks |

**Effort-to-Tier Mapping:** high→opus, medium→sonnet, low→haiku. Used for council calls (wave acceptance, final vibe). Override with `--tier=<name>` flag or `models.skill_overrides.crank` in `.agentops/config.yaml`.

### Step 0: Load Knowledge Context (ao Integration)

If ao CLI available, pull relevant knowledge: `ao lookup --query "<epic-title>" --limit 5`, `ao metrics flywheel status`, `ao ratchet status`. Apply retrieved learnings as implementation constraints and cite with `ao metrics cite "<path>" --type applied` (influenced decision) or `--type retrieved` (loaded but not referenced). Prefer `matched_snippet` over full files when lookup results include section evidence. If ao unavailable, skip and proceed.

### Step 0.5: Detect Tracking Mode

```bash
if command -v bd &>/dev/null; then
  TRACKING_MODE="beads"
else
  TRACKING_MODE="tasklist"
  echo "Note: bd CLI not found. Using TaskList for issue tracking."
fi
```

**Tracking mode determines the source of truth for the rest of the workflow:**

| | Beads Mode | TaskList Mode |
|---|---|---|
| **Source of truth** | `bd` (beads issues) | TaskList (Claude-native) |
| **Find work** | `bd ready` | `TaskList()` → pending, unblocked |
| **Get details** | `bd show <id>` | `TaskGet(taskId)` |
| **Mark complete** | `bd update <id> --status closed` | `TaskUpdate(taskId, status="completed")` |
| **Track retries** | `bd comments add` | Task description update |
| **Epic tracking** | `bd update <epic-id> --append-notes` | In-memory wave counter |

### Step 0.6: Detect gc Pool Backend

Check `gc status --json` for a running controller. Set `GC_POOL_AVAILABLE=true` if gc is available. When true, gc pool handles worker lifecycle and auto-scales based on `bd ready --count`. Crank simplifies to: create issues, gc scales workers, workers close issues, crank validates. See [references/gc-pool-dispatch.md](references/gc-pool-dispatch.md) for dispatch details.

### Step 1: Identify the Epic / Work Source

**Beads mode:**

**If epic ID provided:** Use it directly. Do NOT ask for confirmation.

**If no epic ID:** Discover it:
```bash
bd list --type epic --status open 2>/dev/null | head -5
```

**Single-Epic Scope Check (WARN):**
If `bd list --type epic --status open` returns more than one epic, log a warning:
```
WARN: Multiple open epics detected. /crank operates on a single epic.
Use --allow-multi-epic to suppress this warning.
```
If multiple epics found, ask user which one (WARN, not FAIL).

**TaskList mode:**

If input is an epic ID → Error: "bd CLI required for beads epic tracking. Install bd or provide a plan file / task list."

If input is a plan file path (`.md`):
1. Read the plan file
2. Decompose into TaskList tasks (one `TaskCreate` per distinct work item)
3. Set up dependencies via `TaskUpdate(addBlockedBy)`
4. Proceed to Step 3

If no input:
1. Check `TaskList()` for existing pending tasks
2. If tasks exist, use them as the work items
3. If no tasks, ask user what to work on

If input is a description string:
1. Decompose into tasks (`TaskCreate` for each)
2. Set up dependencies
3. Proceed to Step 3

### Step 1a: Initialize Wave Counter

**Beads mode:**
```bash
# Initialize crank tracking in epic notes
bd update <epic-id> --append-notes "CRANK_START: wave=0 at $(date -Iseconds)" 2>/dev/null
```

**TaskList mode:** Track wave counter in memory only. No external state needed.

Track in memory: `wave=0`

### Step 1a.1: Initialize Plan Mutation Audit Trail

```bash
mkdir -p .agents/rpi
: > .agents/rpi/plan-mutations.jsonl
```

Initialize the `log_plan_mutation` helper and budget counters. See [references/plan-mutations.md](references/plan-mutations.md) for the full JSONL schema, helper function, budget limits, and mutation types.

### Step 1a.2: Initialize Shared Task Notes

```bash
mkdir -p .agents/crank
cat > .agents/crank/SHARED_TASK_NOTES.md <<EOF
# Shared Task Notes — Epic ${EPIC_ID:-unknown}
> Cross-wave context for workers. Read before starting.
EOF
```

See [references/shared-task-notes.md](references/shared-task-notes.md) for the full pattern, size management, and worker integration.

### Step 1b: Detect Test-First Mode (--test-first only)

```bash
# Check for --test-first flag
if [[ "$TEST_FIRST" == "true" ]]; then
    # Classify issues by type
    # spec-eligible: feature, bug, task → SPEC + TEST waves apply
    # skip: docs, chore, ci, epic → standard implementation waves only
    SPEC_ELIGIBLE=()
    SPEC_SKIP=()

    if [[ "$TRACKING_MODE" == "beads" ]]; then
        for issue in $READY_ISSUES; do
            ISSUE_TYPE=$(bd show "$issue" 2>/dev/null | grep "Type:" | head -1 | awk '{print tolower($NF)}')
            case "$ISSUE_TYPE" in
                feature|bug|task) SPEC_ELIGIBLE+=("$issue") ;;
                docs|chore|ci|epic) SPEC_SKIP+=("$issue") ;;
                *)
                    echo "WARNING: Issue $issue has unknown type '$ISSUE_TYPE'. Defaulting to spec-eligible."
                    SPEC_ELIGIBLE+=("$issue")
                    ;;
            esac
        done
    else
        # TaskList mode: no bd available, default all to spec-eligible
        SPEC_ELIGIBLE=($READY_ISSUES)
        echo "TaskList mode: all ${#SPEC_ELIGIBLE[@]} issues defaulted to spec-eligible (no bd type info)"
    fi
    echo "Test-first mode: ${#SPEC_ELIGIBLE[@]} spec-eligible, ${#SPEC_SKIP[@]} skipped (docs/chore/ci/epic)"
fi
```

If `--test-first` is NOT set, skip Steps 3b and 3c entirely — behavior is unchanged.

### Step 2: Get Epic Details

**Beads mode:**
```bash
bd show <epic-id> 2>/dev/null
```

**TaskList mode:** `TaskList()` to see all tasks and their status/dependencies.

### Step 3: List Ready Issues (Current Wave)

**Beads mode:**

Find issues that can be worked on (no blockers):
```bash
bd ready 2>/dev/null
```

**`bd ready` returns the current wave** - all unblocked issues. These can be executed in parallel because they have no dependencies on each other.

**TaskList mode:**

`TaskList()` → filter for status=pending, no blockedBy (or all blockers completed). These are the current wave.

### Step 3a: Pre-flight Check - Issues Exist

**Verify there are issues to work on:**

**If 0 ready issues found (beads mode) or 0 pending unblocked tasks (TaskList mode):**
```
STOP and return error:
  "No ready issues found for this epic. Either:
   - All issues are blocked (check dependencies)
   - Epic has no child issues (run /plan first)
   - All issues already completed"
```

Also verify: epic has at least 1 child issue total. An epic with 0 children means /plan was not run.

Do NOT proceed with empty issue list - this produces false "epic complete" status.

### Step 3a.1: Pre-flight Check - Pre-Mortem Required (3+ issues)

If the epic has 3+ child issues, look for a pre-mortem report in `.agents/council/*pre-mortem*`. If none found, emit `<promise>BLOCKED</promise>` and stop — run `/pre-mortem` first. Pre-mortems have positive ROI for 3+ issue epics; cost (~2 min) is negligible.

### Step 3a.2: Pre-flight Check - Bead Audit (Stale/Fixed/Consolidatable)

Run `scripts/bd-audit.sh --json` (beads mode only) before wave execution to avoid burning compute on dead work. **WARNING gate** — warns on any flagged beads, **blocks at >50%** flagged. Use `--skip-audit` to bypass. If blocked, clean up with `scripts/bd-audit.sh --auto-close` and `scripts/bd-cluster.sh --auto-merge`, then re-run crank.

### Step 3a.3: Pre-flight Check - Changed-String Grep

**Before spawning workers, grep for every string being changed by the plan.**

This catches stale cross-references that the plan missed. Grep for each key term being modified across the codebase. Matches outside the planned file set indicate scope gaps — add those files to the epic or document as tech debt.

### Step 3b: SPEC WAVE (--test-first only)

**Skip if `--test-first` is NOT set or if no spec-eligible issues exist.**

For each spec-eligible issue (feature/bug/task):
1. **TaskCreate** with subject `SPEC: <issue-title>`
2. Worker receives: issue description, plan boundaries, contract template (`skills/crank/references/contract-template.md`), codebase access (read-only)
3. Worker generates: `.agents/specs/contract-<issue-id>.md`
4. **Validation:** files_exist + content_check for `## Invariants` AND `## Test Cases`
5. **Wave 1 spec consistency checklist (MANDATORY):** run `skills/crank/references/wave1-spec-consistency-checklist.md` across all contracts in this wave. If any item fails, re-run SPEC workers for affected issues and do NOT proceed to TEST WAVE.
6. Lead commits all specs after validation

For BLOCKED recovery and full worker prompt, read `skills/crank/references/test-first-mode.md`.

### Step 3c: TEST WAVE (--test-first only)

**Skip if `--test-first` is NOT set or if no spec-eligible issues exist.**

**Lifecycle integration:** If `--no-lifecycle` is NOT set, delegate test generation to `/test`:

For each spec-eligible issue:
1. **TaskCreate** with subject `TEST: <issue-title>`
2. Worker receives: contract-<issue-id>.md + codebase types (NOT implementation code)
3. Worker generates failing tests via:
   ```
   Skill(skill="test", args="tdd <issue-description> --levels <test_levels>")
   ```
   If `/test` is unavailable or `--no-lifecycle` is set, workers generate tests inline (original behavior).
   - Workers classify generated tests by pyramid level: L0 (contract), L1 (unit), L2 (integration), L3 (component)
   - If `test_levels` metadata exists on the issue, workers MUST generate tests at each required level
4. **RED Gate:** Lead runs test suite — ALL new tests must FAIL
5. Lead commits test harness after RED Gate passes

For RED Gate enforcement and retry logic, read `skills/crank/references/test-first-mode.md`.

**Summary:** SPEC WAVE generates contracts from issues → TEST WAVE generates failing tests from contracts → RED Gate verifies all new tests fail before proceeding. Docs/chore/ci issues bypass both waves.

### Step 3b.1: Build Context Briefing (Before Worker Dispatch)

```bash
if command -v ao &>/dev/null; then
    ao context assemble --task='<epic title>: wave $wave'
fi
```

This produces a 5-section briefing (GOALS, HISTORY, INTEL, TASK, PROTOCOL) at `.agents/rpi/briefing-current.md` with secrets redacted. Include the briefing path in each worker's TaskCreate description so workers start with full project context.

Worker prompt signpost:
- Claude workers should include: `Knowledge artifacts are in .agents/. See .agents/AGENTS.md for navigation. Use \`ao lookup --query "topic"\` for learnings.`
- Codex workers cannot rely on `.agents/` file access in sandbox. The lead should search `.agents/learnings/` for relevant material and inline the top 3 results directly in the worker prompt body.

### Step 3b.2: Load Shared Task Notes (Before Worker Dispatch)

Read `.agents/crank/SHARED_TASK_NOTES.md` and inject its contents into every worker's TaskCreate description (after the issue body). Include a `DISCOVERY REPORTING` instruction so workers report new findings for the orchestrator to harvest. See [references/shared-task-notes.md](references/shared-task-notes.md) for the injection template, size management rules, and discovery reporting format.

### Step 4: Execute Wave via Swarm

**GREEN mode (--test-first only):** If `--test-first` is set and SPEC/TEST waves have completed, modify worker prompts for spec-eligible issues:
- Include in each worker's TaskCreate: `"Failing tests exist at <test-file-paths>. Make them pass. Do NOT modify test files. See GREEN Mode rules in /implement SKILL.md."`
- Workers receive: failing tests (immutable), contract, issue description
- Workers follow GREEN Mode rules from `/implement` SKILL.md
- Docs/chore/ci issues (skipped by SPEC/TEST waves) use standard worker prompts unchanged

**Issue typing + file manifests (REQUIRED):** Include `metadata.issue_type` plus a `metadata.files` array in every TaskCreate. `issue_type` feeds active constraint applicability and validation policy; `files` feed swarm's pre-spawn conflict detection. Two workers claiming the same file in the same wave get serialized or worktree-isolated automatically. Derive both from the issue description, plan, or codebase exploration during planning.
This is the shift-left edge of the prevention ratchet: compiled findings target issue type plus changed files, so missing `metadata.issue_type` weakens enforcement back into guesswork.

**Grep-for-existing-functions (REQUIRED for new function issues):** When an issue description says "create", "add", or "implement" a new function/utility, include `metadata.grep_check` with the function name pattern. Workers MUST grep the codebase for existing implementations before writing new code. This prevents utility duplication (e.g., `estimateTokens` was duplicated in context-orchestration-leverage because no grep check was specified).

**Validation metadata policy (REQUIRED):** For implementation tasks typed `feature|bug|task`, include `metadata.validation.tests` plus at least one structural check (`files_exist` or `content_check`). `docs|chore|ci` use an explicit test-exempt path and should still include applicable structural and/or command/lint checks. Do not omit `metadata.issue_type` and hope task-validation can infer it later. When `/plan` includes `test_levels` metadata in the issue, carry it forward into `metadata.validation.test_levels` so workers know which pyramid levels (L0–L3) to target. See the test pyramid standard (`test-pyramid.md` in the standards skill) for level definitions.

**Language Standards Injection (REQUIRED for code tasks):** Detect project language from repo root markers (`go.mod`, `pyproject.toml`, `Cargo.toml`, `package.json`) and load the matching standard from the standards skill. For `feature|bug|task` issues, include the Testing section verbatim in each worker's task description. For test-modifying issues, also inject file naming and assertion quality rules.

**Validation block extraction (beads mode):** Extract validation metadata from each issue's fenced `validation` block (written by `/plan`). If no block found, fall back to `files_exist` from mentioned file paths. Inject into `metadata.validation` of each TaskCreate.

**Display file-ownership table (from swarm Step 1.5):**

Before spawning, verify the ownership map has zero unresolved conflicts:

```
File Ownership Map (Wave $wave):
┌─────────────────────────────┬──────────┬──────────┐
│ File                        │ Owner    │ Conflict │
├─────────────────────────────┼──────────┼──────────┤
│ (populated by swarm)        │          │          │
└─────────────────────────────┴──────────┴──────────┘
Conflicts: 0
```

**If conflicts > 0:** Do NOT invoke `/swarm`. Resolve by serializing conflicting tasks into sub-waves or merging task scope before proceeding.

**BEFORE each wave:**
```bash
wave=$((wave + 1))
WAVE_START_SHA=$(git rev-parse HEAD)

if [[ "$TRACKING_MODE" == "beads" ]]; then
    bd update <epic-id> --append-notes "CRANK_WAVE: $wave at $(date -Iseconds)" 2>/dev/null
fi

# CHECK GLOBAL LIMIT
if [[ $wave -ge 50 ]]; then
    echo "<promise>BLOCKED</promise>"
    echo "Global wave limit (50) reached."
    # STOP - do not continue
fi
```

**Pre-Spawn: Spec Consistency Gate**

Prevents workers from implementing inconsistent or incomplete specs. Hard failures (missing frontmatter, bad structure, scope conflicts) block spawn; WARN-level issues (terminology, implementability) do not.

```bash
if [ -d .agents/specs ] && ls .agents/specs/contract-*.md &>/dev/null 2>&1; then
    bash scripts/spec-consistency-gate.sh .agents/specs/ || {
        echo "⚠️ Spec consistency check failed — fix contract files before spawning workers"
        exit 1
    }
fi
```

**Cross-cutting constraint injection (SDD):**

Before spawning workers, extract cross-cutting constraints from the plan's `## Boundaries` / `## Cross-Cutting Constraints` section and inject into every TaskCreate's `metadata.validation.cross_cutting` array. Each entry has `name`, `type` (e.g., `content_check`), `file`, and `pattern`. "Ask First" boundaries are annotation-only in auto mode.

**gc pool dispatch (when `GC_POOL_AVAILABLE=true`):**

When gc pool is available, replace `/swarm` with gc pool dispatch — workers are pre-started, assigned via `gc session nudge`, and gc handles crash recovery automatically. When unavailable, the existing `/swarm` path is used unchanged. See [references/gc-pool-dispatch.md](references/gc-pool-dispatch.md) for the full dispatch script.

**For wave execution details (beads sync, TaskList bridging, swarm invocation), read `skills/crank/references/team-coordination.md`.**

**Cross-cutting validation (SDD):**

After per-task validation passes, run cross-cutting checks across all files modified in the wave:

```bash
# Only if cross_cutting constraints were injected
if [[ -n "$CROSS_CUTTING_CHECKS" ]]; then
    WAVE_FILES=$(git diff --name-only "${WAVE_START_SHA}..HEAD")
    for check in $CROSS_CUTTING_CHECKS; do
        run_validation_check "$check" "$WAVE_FILES"
    done
fi
```

### Step 5: Verify and Sync to Beads (MANDATORY)

**External Gate Enforcement:** After each worker completes, the orchestrator (not the worker) runs the gate command. Workers must not declare their own completion. See `references/external-gate-protocol.md`. Swarm executes per-task validation (see `skills/shared/validation-contract.md`); crank trusts swarm validation and focuses on beads sync.

**For verification details, retry logic, and failure escalation, read `skills/crank/references/team-coordination.md` and `skills/crank/references/failure-recovery.md`.**

### Step 5.5: Wave Acceptance Check (MANDATORY)

> **Principle:** Verify each wave meets acceptance criteria using lightweight inline judges. No skill invocations — prevents context explosion in the orchestrator loop.

**For acceptance check details (diff computation, inline judges, verdict gating), read `skills/crank/references/wave-patterns.md`.**

### Step 5.7: Wave Checkpoint

After each wave completes (post-vibe-gate, pre-next-wave), write `.agents/crank/wave-${wave}-checkpoint.json` with fields: `schema_version`, `wave`, `timestamp`, `tasks_completed`, `tasks_failed`, `files_changed`, `git_sha`, `acceptance_verdict` (from Step 5.5), `commit_strategy`, `mutations_this_wave`, `total_mutations`, `mutation_budget` (task_added limit 5, task_reordered limit 3). On retry of the same wave, the file is overwritten.

Immediately validate the checkpoint before using it downstream:

```bash
bash skills/crank/scripts/validate-wave-checkpoint.sh ".agents/crank/wave-${wave}-checkpoint.json"
```

The validator fails closed when `git_sha` does not resolve in the current repo, `timestamp` is invalid or more than 5 minutes in the future, or required checkpoint fields are missing/malformed. Do not proceed to Step 5.7b until this passes.

### Step 5.7b: Vibe Context Checkpoint

Copy the wave checkpoint to `.agents/vibe-context/latest-crank-wave.json` for downstream `/vibe` consumption. Use file copy (not symlink) per repo conventions.

### Step 5.7c: Update Shared Task Notes (After Wave)

Harvest `## Discoveries` sections from completed worker results and append to `.agents/crank/SHARED_TASK_NOTES.md`. Also capture failed approaches from wave failures. See [references/shared-task-notes.md](references/shared-task-notes.md) for the harvest script and size management rules.

### Step 5.7d: Log Plan Mutations (After Wave)

Call `log_plan_mutation` for each plan change during this wave: DECOMPOSE → `task_removed` + `task_added` per sub-task, PRUNE → `task_removed`, scope/dependency/reorder changes → matching mutation type. See [references/plan-mutations.md](references/plan-mutations.md) for the full logging examples and budget enforcement.

### Step 5.8: Wave Status Report

Display a consolidated status table (task, subject, status, validation, duration) plus epic progress (issues closed, blocked, next wave). Informational — does not gate progression.

### Step 5.9: Refresh Worktree Base SHA (MANDATORY)

After committing a wave, verify HEAD advanced past `WAVE_START_SHA`. Next wave's worktrees must branch from this new SHA to prevent cross-wave file collisions. Before spawning the next wave, cross-reference next wave's file manifests (`metadata.files`) against `git diff --name-only "${WAVE_START_SHA}..HEAD"` — log any overlap so workers are aware of prior-wave changes in their worktree base.

### Step 6: Check for More Work

After completing a wave, check for newly unblocked issues (beads: `bd ready`, TaskList: `TaskList()`). Loop back to Step 4 if work remains, or proceed to Step 7 when done.

**For detailed check/retry logic, read `skills/crank/references/team-coordination.md`.**

### Step 6.5: De-Sloppify Pass (Optional)

If implementation waves produced significant output (>200 lines changed), run an optional cleanup pass before final validation. This uses a separate focused worker — see `references/de-sloppify.md` for the full pattern.

**De-sloppify targets:** coverage-padding tests, debug logging, commented-out code, over-defensive error handling, dead imports. Does NOT touch business logic or behavioral tests.

**Skip if:** Total changes < 50 lines, or epic is docs/chore only.

```bash
# Quick slop scan before deciding whether to de-sloppify
SLOP_COUNT=$(git diff --name-only "${FIRST_WAVE_SHA}..HEAD" | xargs grep -l 'fmt\.Println\|console\.log\|# TODO\|// TODO\|commented out' 2>/dev/null | wc -l | tr -d ' ')
if [[ "$SLOP_COUNT" -gt 0 ]]; then
    echo "De-sloppify: $SLOP_COUNT files with potential slop detected"
    # Spawn single cleanup worker (no parallelism needed)
fi
```

### Step 6.9: Pre-Vibe Lifecycle Checks

Skip if `--no-lifecycle` is set.

```
a) if dependency files changed (go.mod, go.sum, package.json, package-lock.json,
     requirements.txt, poetry.lock, Cargo.toml, Cargo.lock, Gemfile, Gemfile.lock):
     Skill(skill="deps", args="vuln --quick")
     CRITICAL vulns (CVSS >= 9.0): BLOCK (treat as test failure — fix before vibe).
     All others: WARN, append to phase summary.

b) Skill(skill="test", args="coverage --quick")
     Append coverage report to vibe context.
```

### Step 7: Final Batched Validation

When all issues complete, run ONE comprehensive vibe on recent changes. Fix CRITICAL issues before completion.

If hooks or `lib/hook-helpers.sh` were modified, verify embedded copies are in sync: `cd cli && make sync-hooks`.

**For detailed validation steps, read `skills/crank/references/failure-recovery.md`.**

### Step 8: Write Phase-2 Summary

Before extracting learnings, write a phase-2 summary for downstream `/validation` consumption:

```bash
mkdir -p .agents/rpi
cat > ".agents/rpi/phase-2-summary-$(date +%Y-%m-%d)-crank.md" <<PHASE2
# Phase 2 Summary: Implementation

- **Epic:** <epic-id>
- **Waves completed:** ${wave}
- **Issues completed:** <completed-count>/<total-count>
- **Files modified:** $(git diff --name-only "${WAVE_START_SHA}..HEAD" | wc -l | tr -d ' ')
- **Status:** <DONE|PARTIAL|BLOCKED>
- **Completion marker:** <promise marker from Step 9>
- **Timestamp:** $(date -Iseconds)
PHASE2
```

This summary is consumed by `/validation` closeout (and its internal `/post-mortem`) for scope reconciliation.

### Step 8.5: Extract Learnings (ao Integration)

If ao CLI available: run `ao forge transcript`, `ao flywheel close-loop --quiet`, `ao metrics flywheel status`, and `ao pool list --status=pending` to extract and review learnings. If ao unavailable, skip and recommend `/validation` manually.

### Step 8.6: Archive Shared Task Notes

Archive `.agents/crank/SHARED_TASK_NOTES.md` to `.agents/crank/archives/` for post-mortem review. See [references/shared-task-notes.md](references/shared-task-notes.md) for the archive script.

### Step 8.7: Scope-Completion Check (Pre-Close Gate)

Before marking the epic DONE, verify planned acceptance criteria are met:

1. Read the plan from `.agents/plans/` (most recent matching the epic)
2. Extract acceptance criteria from each issue's `## Acceptance` section
3. For each criterion, check current state:
   - `files_exist`: verify file paths exist
   - `content_check`: grep for expected patterns
   - `command`: run verification commands
4. Report results:
   - All criteria met → proceed to Step 9
   - Any criteria NOT met → **WARN** with list of unmet criteria (do not block — validation phase catches remaining gaps)

Example: `PLAN_FILE=$(ls -t .agents/plans/*.md 2>/dev/null | head -1)` then extract and verify each acceptance criterion from the plan.

**Opt-out:** `--no-scope-check` flag.

### Step 9: Report Completion

Tell the user:
1. Epic ID and title
2. Number of issues completed
3. Total iterations used (of 50 max)
4. Final vibe results
5. Flywheel status (if ao available)
6. Suggest running `/validation` to complete closeout and promote learnings

**Output completion marker:**
```
<promise>DONE</promise>
Epic: <epic-id>
Issues completed: N
Iterations: M/50
Flywheel: <status from ao metrics flywheel status>
```

If stopped early:
```
<promise>BLOCKED</promise>
Reason: <global limit reached | unresolvable blockers>
Issues remaining: N
Iterations: M/50
```

## The FIRE Loop

Crank repeats FIRE (Find → Ignite → Reap → Vibe → Escalate) for each wave until all issues are CLOSED (beads) or all tasks are completed (TaskList). Read `references/wave-patterns.md` for the loop model, parallel wave rules, and acceptance check details.

## Key Rules

- Auto-detect tracking (`bd` first, TaskList fallback) and use the provided epic or plan input directly.
- Use `/swarm` for every wave, preserve fresh per-issue context, and refuse to continue past unresolved conflicts or the 50-wave cap.
- Validate once per wave, fix CRITICAL findings before completion, and keep looping until every issue/task is done.
- Load learnings at the start, extract learnings at the end, and always emit `DONE`, `BLOCKED`, or `PARTIAL`.

### Verb Disambiguation for Worker Prompts

Read `references/worker-verb-disambiguation.md` for the verb clarification table. Ambiguous verbs (extract, remove, update, consolidate) cause workers to implement wrong operations — always use explicit instructions with `wc -l` assertions.

## Examples

**User says:** `/crank ag-m0r` — Beads epic: loads learnings, swarm per wave, loops until all closed, final vibe.
**User says:** `/crank .agents/plans/auth-refactor.md` — Plan file: decomposes into tasks, swarm per wave, final vibe.
**User says:** `/crank --test-first ag-xj9` — SPEC → TEST → RED Gate → GREEN IMPL. See `references/test-first-mode.md`.

---

## Troubleshooting

Common failure modes: no ready issues, repeated wave gate failures, missing files from workers, bad RED-gate output, or TaskList/beads mismatches. See `references/troubleshooting.md` for fixes and command-level recovery steps.

---

## Reference Documents

- [references/de-sloppify.md](references/de-sloppify.md)
- [references/plan-mutations.md](references/plan-mutations.md)
- [references/shared-task-notes.md](references/shared-task-notes.md)
- [references/claude-code-latest-features.md](references/claude-code-latest-features.md)
- [references/commit-strategies.md](references/commit-strategies.md)
- [references/worktree-per-worker.md](references/worktree-per-worker.md)
- [references/contract-template.md](references/contract-template.md)
- [references/failure-recovery.md](references/failure-recovery.md)
- [references/failure-taxonomy.md](references/failure-taxonomy.md)
- [references/fire.md](references/fire.md)
- [references/gc-pool-dispatch.md](references/gc-pool-dispatch.md)
- [references/ralph-loop-contract.md](references/ralph-loop-contract.md)
- [references/taskcreate-examples.md](references/taskcreate-examples.md)
- [references/team-coordination.md](references/team-coordination.md)
- [references/test-first-mode.md](references/test-first-mode.md)
- [references/troubleshooting.md](references/troubleshooting.md)
- [references/uat-integration-wave.md](references/uat-integration-wave.md)
- [references/wave1-spec-consistency-checklist.md](references/wave1-spec-consistency-checklist.md)
- [references/wave-patterns.md](references/wave-patterns.md)
- [references/worker-verb-disambiguation.md](references/worker-verb-disambiguation.md)
- [references/external-gate-protocol.md](references/external-gate-protocol.md)
