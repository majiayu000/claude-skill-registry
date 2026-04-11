---
name: ln-310-multi-agent-validator
description: "Use when validating Stories, plans, or context through the evaluation platform with mandatory research, parallel evidence lanes, sequential merge, and bounded refinement."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root.

**Type:** L2 Coordinator
**Category:** 3XX Planning

# Multi-Agent Validator

Evaluation-platform coordinator for:
- `mode=story`
- `mode=plan_review`
- `mode=context`

This skill replaces the old review-runtime-centric flow with:
- mandatory official-doc, MCP Ref, Context7, and current-web research
- parallel read-only evidence lanes
- sequential documentation, repair, merge, refinement, and approval
- runtime-backed worker plans, worker summaries, agent sync, and cleanup verification

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `storyId` | `mode=story` | args, git branch, kanban, user | Story to validate |
| `plan {file}` | `mode=plan_review` | args or auto | Plan file to validate |
| `context` | `mode=context` | conversation, git diff, user | Arbitrary review context |

Mode detection:
- `plan` or `plan {file}` -> `mode=plan_review`
- `context` -> `mode=context`
- otherwise -> `mode=story`

## Mandatory Read

**MANDATORY READ:** Load `shared/references/environment_state_contract.md`, `shared/references/storage_mode_detection.md`, `shared/references/input_resolution_pattern.md`
**MANDATORY READ:** Load `shared/references/evaluation_coordinator_runtime_contract.md`, `shared/references/evaluation_summary_contract.md`, `shared/references/evaluation_parallelism_policy.md`, `shared/references/evaluation_research_contract.md`
**MANDATORY READ:** Load `shared/references/agent_review_workflow.md`, `shared/references/agent_delegation_pattern.md`
**MANDATORY READ:** Load `references/phase2_research_audit.md`, `references/penalty_points.md`

## Worker Set

The coordinator uses these evaluation workers:
- `ln-311-review-research-worker`
- `ln-312-review-findings-worker`
- `ln-313-review-docs-worker`
- `ln-314-review-repair-worker`
- `ln-315-review-merge-worker`
- `ln-316-review-refinement-worker`

## Worker Invocation (MANDATORY)

Use the Skill tool for delegated workers. Do not inline worker logic inside the coordinator.

TodoWrite format (mandatory):
- `Config`
- `Discovery`
- `Agent launch`
- `Evidence lanes`
- `Docs`
- `Repair`
- `Merge`
- `Refinement`
- `Approval`
- `Self-check`

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

Runtime family:
- `evaluation-runtime`

Identifier:
- `story-{storyId}` for story mode
- `plan-{slug}` for plan review
- `context-{slug}` for context mode

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
2. Resolve story, plan, or context target.
3. Build evaluation runtime manifest with:
   - `expected_agents`
   - `required_research=true`
   - exact `phase_order`
   - `phase_policy`
   - report path
4. Start runtime:

```bash
node shared/scripts/evaluation-runtime/cli.mjs start \
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
5. In `mode=context`, materialize discussion context when needed.
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
node shared/scripts/evaluation-runtime/cli.mjs register-agent \
  --skill ln-310 \
  --identifier {identifier} \
  --agent {name} \
  --prompt-file {promptPath} \
  --result-file {resultPath} \
  --metadata-file {metadataPath}
```

5. Checkpoint Phase 2 with `health_check_done`, `agents_available`, `agents_required`, and optional `agents_skipped_reason`.

### Phase 3: Evidence Lanes

This phase is the mandatory parallel evidence barrier.

1. Build `worker_plan` with:
   - `ln-311` lane `research`
   - `ln-312` lane `findings`
2. Launch both workers in parallel.
3. While those workers run, continue local repo inspection and collect additional evidence.
4. Sync agents opportunistically, but do not block on them until merge.
5. Record each worker summary with:

```bash
node shared/scripts/evaluation-runtime/cli.mjs record-worker-result \
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
2. In `mode=plan_review` and `mode=context`, skip only when there is no documentation delta to create.
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
node shared/scripts/evaluation-runtime/cli.mjs sync-agent --skill ln-310 --identifier {identifier}
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

Run `ln-316-review-refinement-worker` with fixed step order:
1. `dry_run_executor`
2. `adversarial_reviewer`
3. `new_dev_tester`
4. `generic_quality`
5. `final_sweep`

Rules:
- sequential only
- bounded loop
- no quality-based skip when Codex is available
- every launched process requires cleanup evidence
- refinement trace is mandatory

### Phase 8: Approval

Story mode:
1. Compute final gate from post-merge and post-refinement state.
2. `GO` only when no remaining blocking issues exist.
3. Mutate Story status only on `GO`.
4. Write user-facing review output.

Plan/context mode:
- write final review output without workflow mutation

Write coordinator summary:

```bash
node shared/scripts/evaluation-runtime/cli.mjs record-summary \
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
- [ ] refinement trace exists when Codex was available
- [ ] background cleanup evidence recorded
- [ ] cleanup verified
- [ ] coordinator summary recorded
- [ ] final result recorded

Then:

```bash
node shared/scripts/evaluation-runtime/cli.mjs complete --skill ln-310 --identifier {identifier}
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

## Definition of Done

- [ ] Evaluation runtime started
- [ ] Mandatory research completed and recorded
- [ ] Read-only evidence lanes executed in parallel
- [ ] Docs, repair, merge, refinement, and approval executed sequentially
- [ ] All required worker summaries recorded
- [ ] All required agents resolved before merge
- [ ] Refinement executed in fixed order or explicitly justified as skipped
- [ ] Cleanup evidence recorded and verified
- [ ] `evaluation-coordinator` summary written
- [ ] Runtime completed successfully

## Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

After the coordinator run, analyze the session per protocol section 7 and include the protocol-formatted output with the final review result.

## References

- Runtime: `shared/references/evaluation_coordinator_runtime_contract.md`, `shared/references/evaluation_summary_contract.md`
- Research: `shared/references/evaluation_research_contract.md`, `shared/references/research_tool_fallback.md`
- Parallelism: `shared/references/evaluation_parallelism_policy.md`
- Workers: `../ln-311-review-research-worker/SKILL.md`, `../ln-312-review-findings-worker/SKILL.md`, `../ln-313-review-docs-worker/SKILL.md`, `../ln-314-review-repair-worker/SKILL.md`, `../ln-315-review-merge-worker/SKILL.md`, `../ln-316-review-refinement-worker/SKILL.md`
- Validation criteria: `references/phase2_research_audit.md`, `references/penalty_points.md`
- Supporting validator refs: `references/context_review_pipeline.md`, `references/cross_reference_validation.md`, `references/dependency_validation.md`, `references/domain_patterns.md`, `references/mcp_ref_findings_template.md`, `references/premortem_validation.md`, `references/quality_validation.md`, `references/risk_validation.md`, `references/solution_validation.md`, `references/standards_validation.md`, `references/structural_validation.md`, `references/traceability_validation.md`, `references/workflow_validation.md`

---
**Version:** 8.0.0
**Last Updated:** 2026-03-22
