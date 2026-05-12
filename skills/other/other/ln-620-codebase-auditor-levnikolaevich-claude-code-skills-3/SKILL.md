---
name: ln-620-codebase-auditor
description: "Use when auditing the codebase through the evaluation platform with mandatory research, coordinated domain audit workers, and structured summaries."
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

**Type:** L2 Coordinator
**Category:** 6XX Audit

# Codebase Auditor

## Mandatory Read

**MANDATORY READ:** Load `references/evaluation_coordinator_runtime_contract.md`, `references/evaluation_summary_contract.md`, `references/evaluation_research_contract.md`
**MANDATORY READ:** Load `references/audit_final_report_contract.md`
**MANDATORY READ:** Load `references/codebase_audit_worker_boundaries.md`
**MANDATORY READ:** Load `references/research_tool_fallback.md`
Conditional read: load `references/epistemic_protocol.md` only when source confidence or claim uncertainty affects issue validation.

## Purpose

- audit runtime/codebase risks: security, delivery gates, dependency/reuse health, maintainability, dead code, diagnosability, concurrency, lifecycle, and config validation
- coordinate exactly `ln-621` through `ln-629`
- require stack-aware research before scoring

## Runtime Contract

Runtime family:
- `evaluation-runtime`

Identifier:
- `codebase-audit`

Phase order:
1. `PHASE_0_CONFIG`
2. `PHASE_1_DISCOVERY`
3. `PHASE_2_RESEARCH`
4. `PHASE_3_DELEGATE`
5. `PHASE_4_AGGREGATE`
6. `PHASE_5_REPORT`
7. `PHASE_6_SELF_CHECK`

## Worker Set

- `ln-621-security-boundary-auditor`
- `ln-622-build-delivery-gate-auditor`
- `ln-623-duplication-overabstraction-auditor`
- `ln-624-code-maintainability-hotspot-auditor`
- `ln-625-dependency-reuse-auditor`
- `ln-626-dead-code-pruning-auditor`
- `ln-627-diagnosability-auditor`
- `ln-628-concurrency-correctness-auditor`
- `ln-629-runtime-lifecycle-config-auditor`

## Worker Invocation (MANDATORY)

**Host Skill Invocation:** `Skill(skill: "...", args: "...")` is mandatory delegation.
- Claude: call the Skill tool exactly as shown.
- Codex: if no Skill tool exists, locate the named skill in available skills, read its `SKILL.md`, treat `args` as `$ARGUMENTS`, execute that skill workflow, then return here with its result/artifact.
- Do not inline worker logic or mark the worker complete without executing the target skill.

Use the Skill tool for delegated workers. Do not inline worker logic inside the coordinator.

TodoWrite format (mandatory):
- `Resolve audit scope and build manifest`
- `Load codebase structure and stack`
- `Run best-practice research`
- `Delegate to domain audit workers`
- `Aggregate worker findings`
- `Generate final audit report and remediation plan`
- `Verify cleanup and self-check`

Representative invocations:

```text
Skill(skill: "ln-621-security-boundary-auditor", args: "{scope}")
Skill(skill: "ln-622-build-delivery-gate-auditor", args: "{scope}")
Skill(skill: "ln-623-duplication-overabstraction-auditor", args: "{scope}")
Skill(skill: "ln-624-code-maintainability-hotspot-auditor", args: "{scope}")
Skill(skill: "ln-625-dependency-reuse-auditor", args: "{scope}")
Skill(skill: "ln-626-dead-code-pruning-auditor", args: "{scope}")
Skill(skill: "ln-627-diagnosability-auditor", args: "{scope}")
Skill(skill: "ln-628-concurrency-correctness-auditor", args: "{scope}")
Skill(skill: "ln-629-runtime-lifecycle-config-auditor", args: "{scope}")
```

## Workflow

### Phase 0: Config

Start `evaluation-runtime` with `required_research=true`.

### Phase 1: Discovery

Detect project type, stack, and applicability of audit workers.

### Phase 2: Research

Mandatory research sources:
1. official docs or standards
2. MCP Ref
3. Context7 when framework docs matter
4. current web best-practice research

### Phase 3: Delegate

Delegate applicable audit workers. Child workers must use `evaluation-worker-runtime` and emit evaluation-compatible summaries.

### Phase 4: Aggregate

Merge runtime/codebase risk findings using `references/codebase_audit_worker_boundaries.md`. Read every worker `report_path`, normalize actions, deduplicate repeated issues, resolve worker conflicts, and validate each actionable problem against the research source order in `references/evaluation_research_contract.md`.

### Phase 5: Report

Write `.hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-620--final-report.md` per `references/audit_final_report_contract.md`. Include the remediation plan, source-backed validation for each confirmed issue, and cleanup note. Remove temporary worker markdown reports after consolidation. The `evaluation-coordinator` summary `report_path` must point to the final report only.

### Phase 6: Self-Check

Required checks:
- [ ] research completed
- [ ] all applicable worker summaries recorded
- [ ] worker conflicts resolved with `codebase_audit_worker_boundaries.md`
- [ ] aggregation completed
- [ ] final remediation report written
- [ ] cleanup verified
- [ ] temporary worker markdown reports removed
- [ ] coordinator summary recorded

## Summary Contract

Write `summary_kind=evaluation-coordinator`.

## Definition of Done

- [ ] Evaluation runtime started
- [ ] Applicable workers selected
- [ ] Research completed
- [ ] All applicable worker summaries recorded
- [ ] Worker set remained exactly `ln-621` through `ln-629`
- [ ] Worker conflicts resolved with `codebase_audit_worker_boundaries.md`
- [ ] Final report and remediation plan written
- [ ] Temporary worker markdown reports removed
- [ ] `evaluation-coordinator` summary written
- [ ] Runtime completed

## Meta-Analysis

Optional reference: load `references/meta_analysis_protocol.md` only when the user asks for post-run meta-analysis or protocol-formatted run reflection.

When requested after the coordinator run, analyze the session per protocol section 7 and include the protocol-formatted output with the final codebase audit result.

## References

- Workers: `../ln-621-security-boundary-auditor/SKILL.md`, `../ln-622-build-delivery-gate-auditor/SKILL.md`, `../ln-623-duplication-overabstraction-auditor/SKILL.md`, `../ln-624-code-maintainability-hotspot-auditor/SKILL.md`, `../ln-625-dependency-reuse-auditor/SKILL.md`, `../ln-626-dead-code-pruning-auditor/SKILL.md`, `../ln-627-diagnosability-auditor/SKILL.md`, `../ln-628-concurrency-correctness-auditor/SKILL.md`, `../ln-629-runtime-lifecycle-config-auditor/SKILL.md`

---
**Version:** 5.0.0
**Last Updated:** 2025-12-23
