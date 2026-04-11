---
name: ln-510-quality-coordinator
description: "Use when coordinating story quality evaluation with mandatory research, worker summaries, agent review, regression evidence, and bounded refinement."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root.

**Type:** L2 Coordinator
**Category:** 5XX Quality

# Quality Coordinator

Evaluation-platform coordinator for story quality review.

## Mandatory Read

**MANDATORY READ:** Load `shared/references/evaluation_coordinator_runtime_contract.md`, `shared/references/evaluation_summary_contract.md`, `shared/references/evaluation_research_contract.md`
**MANDATORY READ:** Load `shared/references/agent_review_workflow.md`, `shared/references/agent_delegation_pattern.md`
**MANDATORY READ:** Load `references/criteria_validation.md`, `references/gate_levels.md`

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

Use the Skill tool for delegated workers. Do not inline worker logic inside the coordinator.

TodoWrite format (mandatory):
- `Config`
- `Discovery`
- `Read-only evidence`
- `Cleanup`
- `Agent barrier`
- `Merge`
- `Refinement`
- `Verdict`
- `Self-check`

Representative invocations:

```text
Skill(skill: "ln-311-review-research-worker", args: "{storyId} quality research")
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
- `ln-311-review-research-worker`
- `ln-511-code-quality-checker`
- `ln-513-regression-checker`
- `ln-514-test-log-analyzer`
- external agent launch

Rules:
- research is mandatory
- worker summaries are the only completion signal
- no merge or mutation occurs in this phase

### Phase 3: Cleanup

1. Run `ln-512-tech-debt-cleaner` only after read-only evidence is collected.
2. Cleanup remains sequential because it mutates files.
3. Record the worker summary and any cleanup evidence.

### Phase 4: Agent Barrier

1. Sync agents through `evaluation-runtime`.
2. Do not cross this barrier until all required agents are resolved or explicitly skipped.

### Phase 5: Merge

Merge inputs:
- research summary
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

Refinement order:
1. `dry_run_executor`
2. `adversarial_reviewer`
3. `new_dev_tester`
4. `generic_quality`
5. `final_sweep`

Rules:
- sequential only
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

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

After the coordinator run, analyze the session per protocol section 7 and include the protocol-formatted output with the final quality verdict.

## References

- Runtime: `shared/references/evaluation_coordinator_runtime_contract.md`, `shared/references/evaluation_summary_contract.md`
- Research: `shared/references/evaluation_research_contract.md`
- Workers: `../ln-511-code-quality-checker/SKILL.md`, `../ln-512-tech-debt-cleaner/SKILL.md`, `../ln-513-regression-checker/SKILL.md`, `../ln-514-test-log-analyzer/SKILL.md`
- Quality criteria: `references/criteria_validation.md`, `references/gate_levels.md`

---
**Version:** 7.0.0
**Last Updated:** 2026-02-09
