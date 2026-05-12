---
name: ln-310-multi-agent-validator
description: "Use when validating Stories, plans, or tasks through the evaluation platform with mandatory research, parallel evidence lanes, sequential merge, and bounded refinement. Modes: story | plan_review."
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

**Type:** L2 Coordinator
**Category:** 3XX Planning

# Multi-Agent Validator

Evaluation-platform coordinator for:
- `mode=story`
- `mode=plan_review`

This skill uses the evaluation platform for:
- mandatory official-doc, MCP Ref, Context7, and current-web research
- parallel read-only evidence lanes
- sequential documentation, repair, merge, refinement, and approval
- runtime-backed worker plans, worker summaries, agent sync, and cleanup verification

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `storyId` | `mode=story` | args, git branch, kanban, user | Story to validate |
| `plan {file}` | `mode=plan_review` | args or auto | Plan file to validate |

Mode detection:
- `plan` or `plan {file}` -> `mode=plan_review`
- otherwise -> `mode=story`

## Mandatory Read

**MANDATORY READ:** Load `references/environment_state_contract.md`, `references/storage_mode_detection.md`, `references/input_resolution_pattern.md`
**MANDATORY READ:** Load `references/evaluation_coordinator_runtime_contract.md`, `references/evaluation_summary_contract.md`, `references/evaluation_parallelism_policy.md`, `references/evaluation_research_contract.md`
**MANDATORY READ:** Load `references/agent_delegation_pattern.md`
**MANDATORY READ:** Load `references/penalty_points.md`
**MANDATORY READ:** Load `references/researchgraph_mcp_usage.md` when researchgraph files changed or the target claims hypothesis, goal, benchmark, or proposal readiness.
Conditional read: load `references/phase2_research_audit.md` only when the coordinator performs inline criteria mapping instead of consuming ln-312 findings summaries.

Agent review policy: run health check, record skipped reason when no advisor is available, verify every advisor claim before merge, and treat transport/auth/tool failures as operator evidence rather than domain findings. Load `references/agent_review_workflow.md` only when debugging lifecycle/liveness details outside the evaluation runtime.

## Worker Set

The coordinator uses these evaluation workers:
- `ln-311-review-research-worker`
- `ln-312-review-findings-worker`
- `ln-313-review-docs-worker`
- `ln-314-review-repair-worker`
- `ln-315-review-merge-worker`
- `ln-316-review-refinement-worker`

## Worker Invocation (MANDATORY)

**Host Skill Invocation:** `Skill(skill: "...", args: "...")` is mandatory delegation.
- Claude: call the Skill tool exactly as shown.
- Codex: if no Skill tool exists, locate the named skill in available skills, read its `SKILL.md`, treat `args` as `$ARGUMENTS`, execute that skill workflow, then return here with its result/artifact.
- Do not inline worker logic or mark the worker complete without executing the target skill.

Use the Skill tool for delegated workers. Do not inline worker logic inside the coordinator.

TodoWrite format (mandatory):
- `Resolve target and build runtime manifest`
- `Load target artifacts and metadata`
- `Launch external agents and verify health`
- `Run research and findings workers in parallel`
- `Generate documentation updates`
- `Apply accepted low-risk repairs`
- `Sync agents and merge all evidence`
- `Run refinement (MANDATORY in ALL modes when advisor available — do NOT skip)`
- `Compute verdict and write review output`
- `Verify runtime cleanup and self-check`

Representative invocations:

```text
Skill(skill: "ln-311-review-research-worker", args: "{identifier} research")
Skill(skill: "ln-312-review-findings-worker", args: "{identifier} findings")
Skill(skill: "ln-313-review-docs-worker", args: "{identifier} docs")
Skill(skill: "ln-314-review-repair-worker", args: "{identifier} repair")
Skill(skill: "ln-315-review-merge-worker", args: "{identifier} merge")
Skill(skill: "ln-316-review-refinement-worker", args: "{identifier} refinement")
```

## Runtime Contract

**MANDATORY READ:** Load `references/loop_health_contract.md`

Runtime family:
- `evaluation-runtime`

Identifier:
- `story-{storyId}` for story mode
- `plan-{slug}` for plan review

Phase order:
1. `PHASE_0_CONFIG`
2. `PHASE_1_DISCOVERY`
3. `PHASE_2_AGENT_LAUNCH`
4. `PHASE_3_EVIDENCE_LANES`
5. `PHASE_4_DOCS`
6. `PHASE_5_REPAIR`
7. `PHASE_6_MERGE`
8. `PHASE_7_REFINEMENT`
9. `PHASE_8_APPROVAL`
10. `PHASE_9_SELF_CHECK`

Phase policy:
- `delegate_phases = [PHASE_3_EVIDENCE_LANES, PHASE_4_DOCS, PHASE_5_REPAIR, PHASE_6_MERGE, PHASE_7_REFINEMENT]`
- `aggregate_phase = PHASE_6_MERGE`
- `report_phase = PHASE_8_APPROVAL`
- `cleanup_phase = PHASE_9_SELF_CHECK`
- `self_check_phase = PHASE_9_SELF_CHECK`
- `agent_resolve_before = [PHASE_6_MERGE]`
- `required_phases_when_advisor_available = [PHASE_7_REFINEMENT]`

## Parallelism Rules

Allowed overlap:
- external agents
- `ln-311`
- `ln-312`
- local repo inspection and evidence gathering

Sequential only:
- `ln-313`
- `ln-314`
- `ln-315`
- `ln-316`
- approval and status mutation

## Workflow

### Phase 0: Config

1. Resolve `mode`, identifier, and storage mode.
2. Resolve story or plan target.
3. Build evaluation runtime manifest with:
   - `expected_agents`
   - `required_research=true`
   - exact `phase_order`
   - `phase_policy`
   - report path
4. Start runtime:

```bash
node references/scripts/evaluation-runtime/cli.mjs start \
  --skill ln-310 \
  --identifier {identifier} \
  --manifest-file .hex-skills/evaluation/{identifier}_manifest.json
```

5. Checkpoint Phase 0.

### Phase 1: Discovery

1. Materialize the exact target artifact.
2. Load only the metadata needed for the current mode.
3. In `mode=story`, resolve Story and child tasks.
4. In `mode=plan_review`, resolve the plan file.
5. If researchgraph files changed or the target cites `H##`, `G##`, run IDs, benchmark manifests, or readiness claims, run read-only researchgraph verification/audits and attach the result as validation evidence.
6. Checkpoint Phase 1 with resolved refs.

### Phase 2: Agent Launch

1. Run agent health check.
2. Exclude disabled agents from `.hex-skills/environment_state.json`.
3. If no agents are available:
   - record `agents_skipped_reason`
   - checkpoint Phase 2
   - continue
4. Otherwise:
   - build per-agent prompts
   - launch each available agent
   - register each launched agent:

```bash
node references/scripts/evaluation-runtime/cli.mjs register-agent \
  --skill ln-310 \
  --identifier {identifier} \
  --agent {name} \
  --prompt-file {promptPath} \
  --result-file {resultPath} \
  --metadata-file {metadataPath}
```

5. Checkpoint Phase 2 with `health_check_done`, `agents_available`, `agents_required`, and optional `agents_skipped_reason`.
6. Classify each external agent result before domain verdict:
   - `rate_limited`, `tool_missing`, `auth_missing`, `permission_denial`, and `asked_question` are transport/operator states.
   - Do not convert them into `NO-GO` without domain evidence from artifacts or findings.
   - Record loop health for repeated advisor/session failures and pause when retry usefulness is exhausted.

### Phase 3: Evidence Lanes

This phase is the mandatory parallel evidence barrier.

1. Build `worker_plan` with:
   - `ln-311` lane `research` (mandatory)
   - `ln-312` lane `findings` (mandatory)
2. Launch all planned workers in parallel.
3. While those workers run, continue local repo inspection and collect additional evidence.
4. Sync agents opportunistically, but do not block on them until merge.
5. Record each worker summary with:

```bash
node references/scripts/evaluation-runtime/cli.mjs record-worker-result \
  --skill ln-310 \
  --identifier {identifier} \
  --payload-file {childSummaryArtifactPath}
```

Research is mandatory in every mode:
- official documentation or standards
- MCP Ref
- Context7 when a library or framework is involved
- current web best-practice research

For `mode=story`, findings must still produce penalty-point evidence and coverage analysis.

### Phase 4: Docs

1. In `mode=story`, run `ln-313-review-docs-worker` when documentation changes are required.
2. In `mode=plan_review`, skip only when there is no documentation delta to create.
3. Record the worker summary or explicit skip rationale.

### Phase 5: Repair

1. Apply accepted low-risk repairs through `ln-314-review-repair-worker`.
2. Do not merge repair logic into research or findings lanes.
3. Record summary and any cleanup evidence.

### Phase 6: Merge

Preconditions:
- all planned evidence workers resolved
- all required agents resolved or explicitly skipped

Steps:
1. Sync agents once at the merge barrier:

```bash
node references/scripts/evaluation-runtime/cli.mjs sync-agent --skill ln-310 --identifier {identifier}
```

2. Run `ln-315-review-merge-worker`.
3. Deduplicate:
   - local findings
   - worker findings
   - agent findings
   - prior review history
4. Reject unsupported claims.
5. Apply only verified accepted changes.
6. Checkpoint Phase 6 with `aggregation_summary`.

### Phase 7: Refinement

> **NEVER SKIP THIS PHASE.** Phase 7 applies to ALL modes: `story`, `plan_review`.
> The ONLY valid skip reason is no advisor available in health check.
> Mode is NOT a skip reason. Complexity is NOT a skip reason. Time is NOT a skip reason.
> If you are about to checkpoint Phase 7 without running ln-316 while an advisor is available — STOP. You are making an error.

| Mode | Phase 7 required? | Skip allowed? |
|------|-------------------|---------------|
| `story` | YES | NO (only if no advisor available) |
| `plan_review` | YES | NO (only if no advisor available) |

Phase 7 is MANDATORY when an advisor is available. The coordinator MUST NOT checkpoint Phase 7 without a recorded `review-refinement` worker summary from ln-316. The runtime `advance` command will reject the transition if an advisor was available in health check but no refinement summary exists.

Run `ln-316-review-refinement-worker`. Refinement uses a 2-stage state machine:
- Stage 1: 3 parallel advisor sessions (dry_run_executor, new_dev_tester, adversarial_reviewer)
- Stage 2: 1 sequential advisor session (final_sweep) after merging Stage 1 results

Rules:
- all 4 perspectives are mandatory
- Stage 1 runs in parallel, Stage 2 runs after Stage 1 merge
- each perspective = independent advisor process via `agent_runner.mjs` (NOT host-native sub-agents)
- every launched process requires cleanup evidence
- advisor session failures use `failure_class`, `progress_signals`, and `session_usable` from `agent_runner.mjs`; classified transport failures pause/defer instead of becoming domain findings
- refinement trace is mandatory
- wait for advisor results via runtime `sync-agent`; Claude hosts may use `Monitor` for observability

### Phase 8: Approval

Story mode:
1. Compute final gate from post-merge and post-refinement state.
2. Final Assessment Model:

| Metric | Before | After | Meaning |
|--------|--------|-------|---------|
| Penalty Points | from ln-312 | from ln-314 | 0 = all fixed |
| Readiness Score | `clamp(1,10,10-floor(before/5))` | `clamp(1,10,10-floor(after/5))` | Quality (1-10) |
| Anti-Hallucination | — | from ln-311 | VERIFIED/FLAGGED |
| AC Coverage | — | N/N | 100% = pass |
| Gate | — | GO/NO_GO | Final verdict |

3. Gate rules:
   - `GO` = `penalty_after=0` AND no `FLAGGED` items AND `ac_coverage=100%`
   - `NO_GO` = otherwise
   - Coverage: 80-99% = +3 penalty and forced `NO_GO`
   - Coverage: <80% = +5 penalty and forced `NO_GO`
4. On `GO`: mutate Story status to `Todo`; update `kanban_board.md` to `APPROVED`.
5. Retry status transition once; if failure → `NO_GO`.
6. Write user-facing review output with per-criterion penalty before/after breakdown.

Plan mode:
- write final review output without workflow mutation

Write coordinator summary:

```bash
node references/scripts/evaluation-runtime/cli.mjs record-summary \
  --skill ln-310 \
  --identifier {identifier} \
  --payload '{...evaluation-coordinator summary...}'
```

### Phase 9: Self-Check

Required checks:
- [ ] runtime started
- [ ] discovery checkpoint exists
- [ ] agent health recorded
- [ ] mandatory research completed
- [ ] all required worker summaries recorded
- [ ] all required agents resolved before merge
- [ ] merge summary exists
- [ ] refinement trace exists when an advisor was available
- [ ] background cleanup evidence recorded
- [ ] cleanup verified
- [ ] coordinator summary recorded
- [ ] final result recorded

Then:

```bash
node references/scripts/evaluation-runtime/cli.mjs complete --skill ln-310 --identifier {identifier}
```

## Summary Contract

Coordinator summary kind:
- `evaluation-coordinator`

Recommended payload fields:
- `status`
- `final_result`
- `report_path`
- `worker_count`
- `agent_count`
- `issues_total`
- `severity_counts`
- `warnings`
- `cleanup_verified`
- `research_completed`
- `penalty_before`
- `penalty_after`
- `readiness_score`
- `ac_coverage`
- `gate` (GO/NO_GO)
- `flagged_items`

## Definition of Done

- [ ] Evaluation runtime started
- [ ] Mandatory research completed and recorded
- [ ] Read-only evidence lanes executed in parallel
- [ ] Docs, repair, merge, refinement, and approval executed sequentially
- [ ] All required worker summaries recorded
- [ ] All required agents resolved before merge
- [ ] Refinement executed when advisor available; SKIPPED only when no advisor available in health check
- [ ] Cleanup evidence recorded and verified
- [ ] `evaluation-coordinator` summary written
- [ ] Runtime completed successfully

## Meta-Analysis

Optional reference: load `references/meta_analysis_protocol.md` only when the user asks for post-run meta-analysis or protocol-formatted run reflection.

When requested after the coordinator run, analyze the session per protocol section 7 and include the protocol-formatted output with the final review result.

## References

- Runtime: `references/evaluation_coordinator_runtime_contract.md`, `references/evaluation_summary_contract.md`
- Research: `references/evaluation_research_contract.md`, `references/research_tool_fallback.md`, `references/plan_review_pipeline.md`
- Parallelism: `references/evaluation_parallelism_policy.md`
- Workers: `../ln-311-review-research-worker/SKILL.md`, `../ln-312-review-findings-worker/SKILL.md`, `../ln-313-review-docs-worker/SKILL.md`, `../ln-314-review-repair-worker/SKILL.md`, `../ln-315-review-merge-worker/SKILL.md`, `../ln-316-review-refinement-worker/SKILL.md`
- Validation criteria: `references/phase2_research_audit.md`, `references/penalty_points.md`
- Supporting validator refs: `references/cross_reference_validation.md`, `references/dependency_validation.md`, `references/domain_patterns.md`, `references/templates/mcp_ref_findings_template.md`, `references/premortem_validation.md`, `references/quality_validation.md`, `references/risk_validation.md`, `references/solution_validation.md`, `references/standards_validation.md`, `references/structural_validation.md`, `references/traceability_validation.md`, `references/workflow_validation.md`

---
**Version:** 8.0.0
**Last Updated:** 2026-03-22
