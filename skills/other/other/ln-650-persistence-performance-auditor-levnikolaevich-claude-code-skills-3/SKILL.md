---
name: ln-650-persistence-performance-auditor
description: "Use when auditing persistence and runtime performance through the evaluation platform with mandatory research, coordinated data-layer workers, and structured summaries."
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

**Type:** L2 Coordinator
**Category:** 6XX Audit

# Persistence Performance Auditor

## Mandatory Read

**MANDATORY READ:** Load `references/evaluation_coordinator_runtime_contract.md`, `references/evaluation_summary_contract.md`, `references/evaluation_research_contract.md`
**MANDATORY READ:** Load `references/audit_final_report_contract.md`
**MANDATORY READ:** Load `references/research_tool_fallback.md`
Conditional read: load `references/epistemic_protocol.md` only when source confidence or claim uncertainty affects issue validation.

## Purpose

- audit query efficiency, transaction correctness, runtime performance, and resource lifecycle
- coordinate `ln-651` through `ln-654`
- require database and framework best-practice research before scoring

## Runtime Contract

Runtime family:
- `evaluation-runtime`

Identifier:
- `persistence-audit`

Phase order:
1. `PHASE_0_CONFIG`
2. `PHASE_1_DISCOVERY`
3. `PHASE_2_RESEARCH`
4. `PHASE_3_DELEGATE`
5. `PHASE_4_AGGREGATE`
6. `PHASE_5_REPORT`
7. `PHASE_6_SELF_CHECK`

## Worker Set

- `ln-651-query-efficiency-auditor`
- `ln-652-transaction-correctness-auditor`
- `ln-653-runtime-performance-auditor`
- `ln-654-resource-lifecycle-auditor`

## Worker Invocation (MANDATORY)

**Host Skill Invocation:** `Skill(skill: "...", args: "...")` is mandatory delegation.
- Claude: call the Skill tool exactly as shown.
- Codex: if no Skill tool exists, locate the named skill in available skills, read its `SKILL.md`, treat `args` as `$ARGUMENTS`, execute that skill workflow, then return here with its result/artifact.
- Do not inline worker logic or mark the worker complete without executing the target skill.

Use the Skill tool for delegated workers. Do not inline worker logic inside the coordinator.

TodoWrite format (mandatory):
- `Resolve audit scope and build manifest`
- `Load data layer and runtime profile`
- `Run best-practice research`
- `Delegate to domain audit workers`
- `Aggregate worker findings`
- `Generate final audit report and remediation plan`
- `Verify cleanup and self-check`

Representative invocations:

```text
Skill(skill: "ln-651-query-efficiency-auditor", args: "{scope}")
Skill(skill: "ln-652-transaction-correctness-auditor", args: "{scope}")
Skill(skill: "ln-653-runtime-performance-auditor", args: "{scope}")
Skill(skill: "ln-654-resource-lifecycle-auditor", args: "{scope}")
```

## Workflow

1. Start `evaluation-runtime`.
2. Discover database, ORM, transaction, and runtime context.
3. Perform mandatory research.
4. Delegate specialized workers.
5. Aggregate findings into one persistence-performance audit by reading every worker `report_path`, normalizing and deduplicating issues, and validating actionable problems against `references/evaluation_research_contract.md`.
6. Write `.hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-650--final-report.md` with remediation plan per `references/audit_final_report_contract.md`.
7. Remove temporary worker markdown reports and record cleanup evidence.
8. Write the `evaluation-coordinator` summary with `report_path` set to the final report.

## Definition of Done

- [ ] Evaluation runtime started
- [ ] Persistence context discovered
- [ ] Mandatory research completed
- [ ] All planned worker summaries recorded
- [ ] Final report and remediation plan written
- [ ] Temporary worker markdown reports removed
- [ ] `evaluation-coordinator` summary written
- [ ] Runtime completed

## Meta-Analysis

Optional reference: load `references/meta_analysis_protocol.md` only when the user asks for post-run meta-analysis or protocol-formatted run reflection.

When requested after the coordinator run, analyze the session per protocol section 7 and include the protocol-formatted output with the final persistence-performance audit result.

## References

- Workers: `../ln-651-query-efficiency-auditor/SKILL.md`, `../ln-652-transaction-correctness-auditor/SKILL.md`, `../ln-653-runtime-performance-auditor/SKILL.md`, `../ln-654-resource-lifecycle-auditor/SKILL.md`

---
**Version:** 1.1.0
**Last Updated:** 2026-03-15
