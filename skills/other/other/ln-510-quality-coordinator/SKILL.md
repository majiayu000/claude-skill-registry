---
name: ln-510-quality-coordinator
description: "Use when coordinating story quality evaluation with mandatory research, worker summaries, agent review, regression evidence, and bounded refinement."
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

**Type:** L2 Coordinator
**Category:** 5XX Quality

# Quality Coordinator

Evaluation-platform coordinator for story quality review.

## Mandatory Read

**MANDATORY READ:** Load `references/evaluation_coordinator_runtime_contract.md`, `references/evaluation_summary_contract.md`, `references/evaluation_research_contract.md`, `references/loop_health_contract.md`
**MANDATORY READ:** Load `references/agent_delegation_pattern.md`
**MANDATORY READ:** Load `references/criteria_validation.md`, `references/gate_levels.md`

Agent review policy: run health check, record skipped reason when no advisor is available, verify every advisor claim before verdict, and treat transport/auth/tool failures as operator evidence rather than quality findings. Load `references/agent_review_workflow.md` only when debugging lifecycle/liveness details outside the evaluation runtime.

## Purpose

- invoke `ln-511-code-quality-checker`
- invoke `ln-512-tech-debt-cleaner`
- invoke `ln-513-regression-checker`
- invoke `ln-514-test-log-analyzer`
- run inline agent review in parallel with read-only evidence gathering
- keep merge, refinement, and verdict sequential
- return normalized quality results

## Inputs

Primary input:
- `storyId`
- `--previous-cycle-focus` (optional, from ln-500): comma-separated blocking categories from prior FAIL cycle

Status filter:
- `To Review`

## Critical Rule

Fast-track paths that skip research are not allowed.

Every quality run must include:
1. official documentation or standards
2. MCP Ref
3. Context7 when a framework or library is involved
4. current web best-practice research

## Runtime Contract

Runtime family:
- `evaluation-runtime`

Identifier:
- `quality-{storyId}`

Phase order:
1. `PHASE_0_CONFIG`
2. `PHASE_1_DISCOVERY`
3. `PHASE_2_READ_ONLY_EVIDENCE`
4. `PHASE_3_CLEANUP`
5. `PHASE_4_AGENT_BARRIER`
6. `PHASE_5_MERGE`
7. `PHASE_7_REFINEMENT`
8. `PHASE_8_VERDICT`
9. `PHASE_9_SELF_CHECK`

## Worker Invocation (MANDATORY)

**Host Skill Invocation:** `Skill(skill: "...", args: "...")` is mandatory delegation.
- Claude: call the Skill tool exactly as shown.
- Codex: if no Skill tool exists, locate the named skill in available skills, read its `SKILL.md`, treat `args` as `$ARGUMENTS`, execute that skill workflow, then return here with its result/artifact.
- Do not inline worker logic or mark the worker complete without executing the target skill.

Use the Skill tool for delegated workers. Do not inline worker logic inside the coordinator.

TodoWrite format (mandatory):
- `Resolve Story and build runtime manifest`
- `Load Story metadata and detect changed files`
- `Run quality checkers and research in parallel`
- `Apply safe tech-debt cleanup`
- `Sync agents and wait for all evidence`
- `Merge and deduplicate all findings`
- `Run bounded refinement loop`
- `Compute quality verdict and score`
- `Verify runtime cleanup and self-check`

Representative invocations:

```text
Skill(skill: "ln-511-code-quality-checker", args: "{storyId}")
Skill(skill: "ln-512-tech-debt-cleaner", args: "{storyId}")
Skill(skill: "ln-513-regression-checker", args: "{storyId}")
Skill(skill: "ln-514-test-log-analyzer", args: "{storyId}")
```

## Workflow

### Phase 0: Config

1. Resolve `storyId`.
2. Build evaluation runtime manifest with `required_research=true`.
3. Start `evaluation-runtime`.

### Phase 1: Discovery

1. Load Story metadata and completed implementation task scope.
2. Detect changed files and project stack.
3. Index semantic graph when available.

### Phase 2: Read-Only Evidence

Parallel work allowed in this phase:
- inline research by the coordinator (per `references/evaluation_research_contract.md`)
- `ln-511-code-quality-checker`
- `ln-513-regression-checker`
- `ln-514-test-log-analyzer`
- external agent launch

Rules:
- research is mandatory
- worker summaries are the only completion signal
- no merge or mutation occurs in this phase

When `previous_cycle_focus` is provided:
- Prioritize evidence collection for the listed blocking categories.
- ln-511 code quality checker should focus on the specified areas first.
- This does not exclude other evidence — it reorders priority.

### Phase 3: Cleanup

1. Run `ln-512-tech-debt-cleaner` only after read-only evidence is collected.
2. Cleanup remains sequential because it mutates files.
3. Record the worker summary and any cleanup evidence.

### Phase 4: Agent Barrier

1. Sync agents through `evaluation-runtime`.
2. Do not cross this barrier until all required agents are resolved or explicitly skipped.
3. Treat `failure_class` from agent results as transport evidence:
   - `rate_limited`, `tool_missing`, `auth_missing`, `permission_denial`, and `asked_question` are not quality FAIL findings by themselves.
   - `timeout_productive` can continue to merge/review only when output/log/session evidence exists.
   - repeated identical worker/agent failure without new artifacts pauses through loop health before another cycle.

### Phase 5: Merge

Merge inputs:
- inline research evidence
- `ln-511` summary
- `ln-512` summary
- `ln-513` summary
- `ln-514` summary
- agent findings

Rules:
- deduplicate before scoring
- unsupported claims are rejected
- security and correctness issues remain high priority

### Phase 6: Refinement

Refinement uses a 2-stage state machine per `references/agents/prompt_templates/iterative_refinement.md` and `references/agents/prompt_templates/refinement_perspectives.md`:
- Stage 1 (parallel): `dry_run_executor`, `new_dev_tester`, `adversarial_reviewer`
- Stage 2 (after merge): `final_sweep`

Rules:
- Stage 1 runs in parallel, Stage 2 after merge
- cleanup evidence required for spawned processes
- no research skipping

### Phase 7: Verdict

Compute normalized quality verdict using:
- code quality
- cleanup result
- agent review
- criteria validation
- linter result
- regression result
- log analysis result

Final verdict values:
- `PASS`
- `CONCERNS`
- `FAIL`

### Phase 8: Self-Check

Required checks:
- [ ] runtime started
- [ ] mandatory research completed
- [ ] all worker summaries recorded
- [ ] all required agents resolved before merge
- [ ] cleanup verified
- [ ] refinement trace recorded when applicable
- [ ] coordinator summary written

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
- [ ] Mandatory research completed
- [ ] Read-only evidence workers completed
- [ ] Cleanup worker completed or justified
- [ ] Agent barrier resolved
- [ ] Merge completed
- [ ] Refinement executed or explicitly justified
- [ ] Final verdict calculated
- [ ] `evaluation-coordinator` summary written
- [ ] Runtime completed

## Meta-Analysis

Optional reference: load `references/meta_analysis_protocol.md` only when the user asks for post-run meta-analysis or protocol-formatted run reflection.

When requested after the coordinator run, analyze the session per protocol section 7 and include the protocol-formatted output with the final quality verdict.

## References

- Runtime: `references/evaluation_coordinator_runtime_contract.md`, `references/evaluation_summary_contract.md`
- Research: `references/evaluation_research_contract.md`
- Workers: `../ln-511-code-quality-checker/SKILL.md`, `../ln-512-tech-debt-cleaner/SKILL.md`, `../ln-513-regression-checker/SKILL.md`, `../ln-514-test-log-analyzer/SKILL.md`
- Quality criteria: `references/criteria_validation.md`, `references/gate_levels.md`

---
**Version:** 7.0.0
**Last Updated:** 2026-02-09
