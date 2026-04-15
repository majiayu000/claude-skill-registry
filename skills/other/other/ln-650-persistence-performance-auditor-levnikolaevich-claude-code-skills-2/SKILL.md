---
name: ln-650-persistence-performance-auditor
description: "Use when auditing persistence and runtime performance through the evaluation platform with mandatory research, coordinated data-layer workers, and structured summaries."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root.

**Type:** L2 Coordinator
**Category:** 6XX Audit

# Persistence Performance Auditor

## Mandatory Read

**MANDATORY READ:** Load `shared/references/evaluation_coordinator_runtime_contract.md`, `shared/references/evaluation_summary_contract.md`, `shared/references/evaluation_research_contract.md`
**MANDATORY READ:** Load `shared/references/research_tool_fallback.md`

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

Use the Skill tool for delegated workers. Do not inline worker logic inside the coordinator.

TodoWrite format (mandatory):
- `Resolve audit scope and build manifest`
- `Load data layer and runtime profile`
- `Run best-practice research`
- `Delegate to domain audit workers`
- `Aggregate worker findings`
- `Generate audit report`
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
5. Aggregate findings into one persistence-performance audit.
6. Write final report and `evaluation-coordinator` summary.

## Definition of Done

- [ ] Evaluation runtime started
- [ ] Persistence context discovered
- [ ] Mandatory research completed
- [ ] All planned worker summaries recorded
- [ ] Aggregate report written
- [ ] `evaluation-coordinator` summary written
- [ ] Runtime completed

## Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

After the coordinator run, analyze the session per protocol section 7 and include the protocol-formatted output with the final persistence-performance audit result.

## References

- Workers: `../ln-651-query-efficiency-auditor/SKILL.md`, `../ln-652-transaction-correctness-auditor/SKILL.md`, `../ln-653-runtime-performance-auditor/SKILL.md`, `../ln-654-resource-lifecycle-auditor/SKILL.md`

---
**Version:** 1.1.0
**Last Updated:** 2026-03-15
