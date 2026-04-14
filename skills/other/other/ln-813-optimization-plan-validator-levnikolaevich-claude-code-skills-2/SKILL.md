---
name: ln-813-optimization-plan-validator
description: "Use when validating optimization plans through the evaluation platform with mandatory research, parallel agent evidence, sequential merge, and bounded refinement."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root.

**Type:** L2 Coordinator
**Category:** 8XX Optimization

# Optimization Plan Validator

Coordinator for validating optimization plans before execution.

## Mandatory Read

**MANDATORY READ:** Load `shared/references/evaluation_coordinator_runtime_contract.md`, `shared/references/evaluation_summary_contract.md`, `shared/references/evaluation_research_contract.md`
**MANDATORY READ:** Load `shared/references/agent_review_workflow.md`, `shared/references/agent_delegation_pattern.md`
**MANDATORY READ:** Load `references/optimization_review_focus.md`

## Purpose

- verify feasibility of optimization hypotheses
- require source-backed research before plan approval
- use parallel external agents plus local feasibility analysis
- keep merge and refinement sequential

## Inputs

Primary input:
- `.hex-skills/optimization/{slug}/context.md`

Required context sections:
- performance map
- hypotheses
- suspicion stack
- test command

## Runtime Contract

Runtime family:
- `evaluation-runtime`

Identifier:
- `optimization-{slug}`

Phase order:
1. `PHASE_0_CONFIG`
2. `PHASE_1_LOAD_CONTEXT`
3. `PHASE_2_AGENT_LAUNCH`
4. `PHASE_3_RESEARCH_AND_FEASIBILITY`
5. `PHASE_4_MERGE`
6. `PHASE_5_REFINEMENT`
7. `PHASE_6_VERDICT`
8. `PHASE_7_SELF_CHECK`

## Worker Invocation (MANDATORY)

Use the Skill tool for delegated workers. Do not inline worker logic inside the coordinator.

TodoWrite format (mandatory):
- `Config`
- `Load context`
- `Agent launch`
- `Research and feasibility`
- `Merge`
- `Refinement`
- `Verdict`
- `Self-check`

Representative invocations:

```text
Skill(skill: "ln-311-review-research-worker", args: "{slug} optimization research")
Skill(skill: "ln-316-review-refinement-worker", args: "{slug} optimization refinement")
```

## Workflow

### Phase 0: Config

1. Resolve optimization slug.
2. Build evaluation runtime manifest with `required_research=true`.
3. Start `evaluation-runtime`.

### Phase 1: Load Context

1. Load `.hex-skills/optimization/{slug}/context.md`.
2. Fail if required sections are missing.
3. Materialize agent-readable context when needed.

### Phase 2: Agent Launch

1. Run health check.
2. Launch available agents.
3. Register every launched agent in `evaluation-runtime`.
4. If no agents are available, record `agents_skipped_reason` and continue.

### Phase 3: Research And Feasibility

Required work:
- run `ln-311-review-research-worker`
- perform local feasibility validation in parallel while agents work

Minimum research lanes:
1. official documentation or standards
2. MCP Ref
3. Context7 for involved libraries
4. current web best-practice research

Feasibility checks:
- files exist
- no invalid overlap across hypotheses
- every hypothesis traces to profiler or research evidence
- unsupported removal hypotheses are flagged
- high-level fixes are preferred over low-level churn when evidence supports them

### Phase 4: Merge

1. Sync agents at the merge barrier.
2. Merge:
   - local feasibility findings
   - research findings
   - agent findings
3. Reject unsupported suggestions.
4. Apply accepted corrections directly to `context.md`.

### Phase 5: Refinement

Refinement uses a 2-stage state machine (see `ln-316-review-refinement-worker`):
- Stage 1 (parallel): `dry_run_executor`, `new_dev_tester`, `adversarial_reviewer`
- Stage 2 (after merge): `final_sweep`

Rules:
- Stage 1 runs in parallel, Stage 2 after merge
- no skip when Codex is available except runtime-backed failure or disablement
- cleanup evidence is mandatory

### Phase 6: Verdict

Possible verdicts:
- `GO`
- `GO_WITH_CONCERNS`
- `NO_GO`

`NO_GO` when:
- critical feasibility gaps remain
- research does not support the plan
- both local validation and agent review reject the plan

### Phase 7: Self-Check

Required checks:
- [ ] context loaded and validated
- [ ] mandatory research completed
- [ ] local feasibility check completed
- [ ] all required agents resolved before merge
- [ ] merge summary exists
- [ ] refinement trace exists when Codex was available
- [ ] cleanup verified
- [ ] coordinator summary recorded

## Summary Contract

Write `summary_kind=evaluation-coordinator`.

Recommended payload:
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
- [ ] Optimization context validated
- [ ] Mandatory research completed
- [ ] Agents launched or explicitly skipped
- [ ] Feasibility analysis completed
- [ ] Merge completed after agent barrier
- [ ] Refinement executed or explicitly justified
- [ ] Verdict issued
- [ ] `evaluation-coordinator` summary written
- [ ] Runtime completed

## Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

After the coordinator run, analyze the session per protocol section 7 and include the protocol-formatted output with the final optimization-plan verdict.

## References

- Runtime: `shared/references/evaluation_coordinator_runtime_contract.md`, `shared/references/evaluation_summary_contract.md`
- Research: `shared/references/evaluation_research_contract.md`
- Review workflow: `shared/references/agent_review_workflow.md`, `shared/references/agent_delegation_pattern.md`
- Focus: `references/optimization_review_focus.md`

---
**Version:** 1.0.0
**Last Updated:** 2026-03-15
