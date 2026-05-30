---
name: ln-610-docs-auditor
description: "Use when auditing project documentation through the evaluation platform with mandatory research, coordinated audit workers, and structured summaries."
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

**Type:** L2 Coordinator
**Category:** 6XX Audit

# Docs Auditor

## Mandatory Read

**MANDATORY READ:** Load `references/evaluation_coordinator_runtime_contract.md`, `references/evaluation_summary_contract.md`, `references/evaluation_research_contract.md`
**MANDATORY READ:** Load `references/audit_final_report_contract.md`
**MANDATORY READ:** Load `references/research_tool_fallback.md`
Conditional read: load `references/epistemic_protocol.md` only when source confidence or claim uncertainty affects issue validation.

## Purpose

- audit documentation structure, relevance, comments, and factual accuracy
- coordinate `ln-611`, `ln-612`, `ln-613`, `ln-614`
- require research-backed standards before final scoring

## Runtime Contract

Runtime family:
- `evaluation-runtime`

Identifier:
- `docs-audit`

Phase order:
1. `PHASE_0_CONFIG`
2. `PHASE_1_DISCOVERY`
3. `PHASE_2_RESEARCH`
4. `PHASE_3_DELEGATE`
5. `PHASE_4_AGGREGATE`
6. `PHASE_5_REPORT`
7. `PHASE_6_SELF_CHECK`

## Worker Set

- `ln-611-docs-structure-auditor`
- `ln-612-semantic-content-auditor`
- `ln-613-code-comments-auditor`
- `ln-614-docs-fact-checker`

## Worker Invocation (MANDATORY)

**Host Skill Invocation:** `Skill(skill: "...", args: "...")` is mandatory delegation.
- Claude: call the Skill tool exactly as shown.
- Codex: if no Skill tool exists, locate the named skill in available skills, read its `SKILL.md`, treat `args` as `$ARGUMENTS`, execute that skill workflow, then return here with its result/artifact.
- Do not inline worker logic or mark the worker complete without executing the target skill.

Use the Skill tool for delegated workers. Do not inline worker logic inside the coordinator.

TodoWrite format (mandatory):
- `Resolve audit scope and build manifest`
- `Load project documentation tree`
- `Run best-practice research`
- `Delegate to domain audit workers`
- `Aggregate worker findings`
- `Generate final audit report and remediation plan`
- `Verify cleanup and self-check`

Representative invocations:

```text
Skill(skill: "ln-611-docs-structure-auditor", args: "{scope}")
Skill(skill: "ln-612-semantic-content-auditor", args: "{scope}")
Skill(skill: "ln-613-code-comments-auditor", args: "{scope}")
Skill(skill: "ln-614-docs-fact-checker", args: "{scope}")
```

## Workflow

### Phase 0: Config

Start `evaluation-runtime` with `required_research=true`.

### Phase 1: Discovery

Discover documentation surfaces and scope.

### Phase 2: Research

Mandatory research sources:
1. official docs or standards
2. MCP Ref
3. Context7 when framework docs matter
4. current web best-practice research

### Phase 3: Delegate

Delegate specialized audit workers.

Child workers must use `evaluation-worker-runtime` and emit evaluation-compatible summaries recorded through `evaluation-runtime`.

### Phase 4: Aggregate

Merge worker summaries into one documentation audit result. Read every worker `report_path`, normalize findings, deduplicate repeated issues, and validate each actionable problem against the research source order in `references/evaluation_research_contract.md`.

### Phase 5: Report

Write `.hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-610--final-report.md` per `references/audit_final_report_contract.md`. Include the remediation plan, source-backed validation for each confirmed issue, and cleanup note. Remove temporary worker markdown reports after consolidation. The `evaluation-coordinator` summary `report_path` must point to the final report only.

### Phase 6: Self-Check

Required checks:
- [ ] mandatory research completed
- [ ] all worker summaries recorded
- [ ] aggregate summary exists
- [ ] final remediation report written
- [ ] temporary worker markdown reports removed
- [ ] cleanup verified
- [ ] coordinator summary recorded

## Summary Contract

Write `summary_kind=evaluation-coordinator`.

## Definition of Done

- [ ] Evaluation runtime started
- [ ] Research completed
- [ ] All documentation audit workers completed
- [ ] Aggregation completed
- [ ] Final report and remediation plan written
- [ ] Temporary worker markdown reports removed
- [ ] `evaluation-coordinator` summary written
- [ ] Runtime completed

## Meta-Analysis

Optional reference: load `references/meta_analysis_protocol.md` only when the user asks for post-run meta-analysis or protocol-formatted run reflection.

When requested after the coordinator run, analyze the session per protocol section 7 and include the protocol-formatted output with the final documentation audit result.

## References

- Workers: `../ln-611-docs-structure-auditor/SKILL.md`, `../ln-612-semantic-content-auditor/SKILL.md`, `../ln-613-code-comments-auditor/SKILL.md`, `../ln-614-docs-fact-checker/SKILL.md`

---
**Version:** 5.0.0
**Last Updated:** 2026-03-01
