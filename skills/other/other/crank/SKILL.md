---
name: crank
description: Execute epics through waves.
practices:
- continuous-delivery
- xp
- agile-manifesto
hexagonal_role: domain
consumes:
- beads
- implement
- post-mortem
- swarm
- vibe
produces:
- .agents/swarm/results/*.json
- git-changes
context_rel:
- kind: shared-kernel
  with: standards
skill_api_version: 1
user-invocable: true
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: full
metadata:
  tier: execution
  dependencies:
  - swarm
  - vibe
  - implement
  - beads
  - post-mortem
output_contract: code changes across wave execution, .agents/swarm/results/*.json
---
# Crank Skill

> **Quick Ref:** Autonomous epic execution. `/swarm` for each wave with runtime-native spawning. Output: closed issues + phase-2 handoff for `/validation`.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

## Loop position

Move **5 (wave execution)** of the [operating loop](../../docs/architecture/operating-loop.md). Consumes the [slice validation plan](../../docs/templates/slice-validation.md); produces wave-by-wave slice completion via `/swarm` + `/implement`. Hard gate at wave start: every row of the wave-validity check must pass (distinct write scopes, no shared migration/contract/CLI surface, declared integration order, owner per slice, discard path per slice). Any failed row → run those slices sequential, not parallel. Parallelism is explicit ownership, not swarm chaos.

Autonomous execution: implement all issues until the epic is DONE.

**CLI dependencies:** bd (issue tracking), ao (knowledge flywheel). Both optional — see `skills/shared/SKILL.md` for fallback table. If bd is unavailable, use TaskList for issue tracking and skip beads sync. If ao is unavailable, skip knowledge injection/extraction.

For Claude runtime feature coverage (agents/hooks/worktree/settings), the shared source of truth is `skills/shared/references/claude-code-latest-features.md`, mirrored locally at `references/claude-code-latest-features.md`.

## Architecture: Crank + Swarm

Crank owns orchestration, epic/task lifecycle, and knowledge-flywheel steps. Swarm owns runtime-native worker spawning, fresh-context isolation, per-wave execution, and cleanup. In beads mode Crank gets each wave from `bd ready`, bridges issues into worker tasks, verifies results, and syncs status back to beads. In TaskList mode the same loop runs over pending unblocked tasks instead of beads issues.

Read `references/team-coordination.md` for the full per-wave execution model, `references/ralph-loop-contract.md` for the fresh-context worker contract, and `references/worker-specs.md` for per-worker model/tool/prompt specs.

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

### Preflight (Recovery hooks → Step 3a.3)

Read [references/execution-preflight.md](references/execution-preflight.md) when you need recovery-hook setup, effort/tier mapping, knowledge-context loading (Step 0), tracking-mode detection (0.5), gc-pool detection (0.6), epic identification (Step 1), branch isolation (1.5), wave-counter / mutation-trail / shared-task-notes initialization (1a–1a.2), test-first classification (1b), epic details (Step 2), ready-issue listing (Step 3), and the four pre-flight checks (3a, 3a.1 pre-mortem, 3a.2 bd-audit, 3a.3 changed-string grep).

The Branch Isolation Gate (Step 1.5) has its own dedicated contract — see [references/branch-isolation.md](references/branch-isolation.md) for when crank must create or refuse an isolation branch.

### Wave dispatch (Step 3b → Step 4)

Read [references/wave-dispatch.md](references/wave-dispatch.md) when you need SPEC WAVE / TEST WAVE / RED Gate flow (Steps 3b–3c), context-briefing assembly (3b.1), shared-notes injection (3b.2), parallel-wave isolation (3b.3), or Step 4 wave execution detail — GREEN mode, issue-typing + file manifests, grep-for-existing-functions, validation metadata policy, acceptance-criteria injection, language-standards injection, file-ownership table, wave-counter / 50-cap gate, spec-consistency gate, cross-cutting constraint injection, gc-pool dispatch, and cross-cutting validation.

### Wave completion (Step 5 → Step 8.7)

Read [references/wave-completion.md](references/wave-completion.md) when you need verify-and-sync (Step 5, external-gate protocol), wave acceptance check + CI-policy parity gate (5.5), wave checkpoint + per-criterion verdicts + back-compat fallback (5.7), vibe-context checkpoint (5.7b), shared-task-notes harvest (5.7c), plan-mutation logging (5.7d), wave status report (5.8), worktree base-SHA refresh (5.9), check-for-more-work loop (Step 6), de-sloppify pass (6.5), pre-vibe lifecycle checks (6.9), final batched validation (Step 7), phase-2 summary (Step 8), learnings extraction (8.5), shared-notes archive (8.6), and the scope-completion pre-close gate (8.7).

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

## Inline Work Policy

Most `/crank` steps delegate worker execution via `/swarm` or `Skill()`. A small number of steps are **orchestrator-owned** by design — these are inline gates, scans, and bookkeeping that must stay in the orchestrator's context to make a downstream decision. Orchestrator-owned steps are marked with a `*(orchestrator-owned: …)*` admonition in the body (see STEP 3a.3, STEP 6.5 slop-scan, STEP 8.7).

**Do NOT convert orchestrator-owned steps into `Skill()` or `/swarm` delegations** — they are intentionally inline. Every other step (SPEC wave, TEST wave, IMPL wave, vibe, lifecycle checks) should delegate via the documented `Skill(...)` call or `/swarm` invocation.

If unsure whether a step is orchestrator-owned or delegatable, the default is **delegate**. Only steps marked with the admonition above are exempt.

Crank runs as an isolated phase-2 execution context — discovery and validation are sealed off from this skill. See [references/isolation-contract.md](references/isolation-contract.md) for the four-lever enforcement model and the compression patterns `scripts/check-skill-isolation.sh` flags. See [references/best-practices.md](references/best-practices.md) for the lifecycle principle + anti-pattern citation table (cite by number; do not duplicate body content).

## Reference Documents

- [references/crank.feature](references/crank.feature) — Executable spec: wave-validity hard gate, FIRE loop, mandatory completion marker, 50-wave cap (soc-qk4b.2)
- [references/de-sloppify.md](references/de-sloppify.md)
- [references/execution-preflight.md](references/execution-preflight.md)
- [references/parallel-wave-isolation.md](references/parallel-wave-isolation.md)
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
- [references/phase-data-contracts.md](references/phase-data-contracts.md) — phase artifact data contracts (cited from references/isolation-contract.md)
- [references/uat-integration-wave.md](references/uat-integration-wave.md)
- [references/wave-completion.md](references/wave-completion.md)
- [references/wave-dispatch.md](references/wave-dispatch.md)
- [references/wave1-spec-consistency-checklist.md](references/wave1-spec-consistency-checklist.md)
- [references/wave-patterns.md](references/wave-patterns.md)
- [references/worker-verb-disambiguation.md](references/worker-verb-disambiguation.md)
- [references/external-gate-protocol.md](references/external-gate-protocol.md)
