---
name: ln-620-codebase-auditor
description: "Use when auditing the codebase through the evaluation platform with mandatory research, coordinated domain audit workers, and structured summaries."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root.

**Type:** L2 Coordinator
**Category:** 6XX Audit

# Codebase Auditor

## Mandatory Read

**MANDATORY READ:** Load `shared/references/evaluation_coordinator_runtime_contract.md`, `shared/references/evaluation_summary_contract.md`, `shared/references/evaluation_research_contract.md`
**MANDATORY READ:** Load `shared/references/research_tool_fallback.md`

## Purpose

- audit security, build health, code quality, dependencies, observability, concurrency, lifecycle, and structure
- coordinate `ln-621` through `ln-629`
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

- `ln-621-security-auditor`
- `ln-622-build-auditor`
- `ln-623-code-principles-auditor`
- `ln-624-code-quality-auditor`
- `ln-625-dependencies-auditor`
- `ln-626-dead-code-auditor`
- `ln-627-observability-auditor`
- `ln-628-concurrency-auditor`
- `ln-629-lifecycle-auditor`

## Worker Invocation (MANDATORY)

Use the Skill tool for delegated workers. Do not inline worker logic inside the coordinator.

TodoWrite format (mandatory):
- `Resolve audit scope and build manifest`
- `Load codebase structure and stack`
- `Run best-practice research`
- `Delegate to domain audit workers`
- `Aggregate worker findings`
- `Generate audit report`
- `Verify cleanup and self-check`

Representative invocations:

```text
Skill(skill: "ln-621-security-auditor", args: "{scope}")
Skill(skill: "ln-622-build-auditor", args: "{scope}")
Skill(skill: "ln-623-code-principles-auditor", args: "{scope}")
Skill(skill: "ln-624-code-quality-auditor", args: "{scope}")
Skill(skill: "ln-625-dependencies-auditor", args: "{scope}")
Skill(skill: "ln-626-dead-code-auditor", args: "{scope}")
Skill(skill: "ln-627-observability-auditor", args: "{scope}")
Skill(skill: "ln-628-concurrency-auditor", args: "{scope}")
Skill(skill: "ln-629-lifecycle-auditor", args: "{scope}")
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

Merge security, correctness, architecture, and maintainability findings.

### Phase 5: Report

Write final codebase audit output and coordinator summary.

### Phase 6: Self-Check

Required checks:
- [ ] research completed
- [ ] all applicable worker summaries recorded
- [ ] aggregation completed
- [ ] cleanup verified
- [ ] coordinator summary recorded

## Summary Contract

Write `summary_kind=evaluation-coordinator`.

## Definition of Done

- [ ] Evaluation runtime started
- [ ] Applicable workers selected
- [ ] Research completed
- [ ] All applicable worker summaries recorded
- [ ] Final report written
- [ ] `evaluation-coordinator` summary written
- [ ] Runtime completed

## Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

After the coordinator run, analyze the session per protocol section 7 and include the protocol-formatted output with the final codebase audit result.

## References

- Workers: `../ln-621-security-auditor/SKILL.md`, `../ln-622-build-auditor/SKILL.md`, `../ln-623-code-principles-auditor/SKILL.md`, `../ln-624-code-quality-auditor/SKILL.md`, `../ln-625-dependencies-auditor/SKILL.md`, `../ln-626-dead-code-auditor/SKILL.md`, `../ln-627-observability-auditor/SKILL.md`, `../ln-628-concurrency-auditor/SKILL.md`, `../ln-629-lifecycle-auditor/SKILL.md`

---
**Version:** 5.0.0
**Last Updated:** 2025-12-23
