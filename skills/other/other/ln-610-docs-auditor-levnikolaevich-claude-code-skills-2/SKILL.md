---
name: ln-610-docs-auditor
description: "Use when auditing project documentation through the evaluation platform with mandatory research, coordinated audit workers, and structured summaries."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root.

**Type:** L2 Coordinator
**Category:** 6XX Audit

# Docs Auditor

## Mandatory Read

**MANDATORY READ:** Load `shared/references/evaluation_coordinator_runtime_contract.md`, `shared/references/evaluation_summary_contract.md`, `shared/references/evaluation_research_contract.md`
**MANDATORY READ:** Load `shared/references/research_tool_fallback.md`

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

Use the Skill tool for delegated workers. Do not inline worker logic inside the coordinator.

TodoWrite format (mandatory):
- `Config`
- `Discovery`
- `Research`
- `Delegate`
- `Aggregate`
- `Report`
- `Self-check`

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

Child workers may remain on `audit-worker-runtime`, but the coordinator records every worker summary through `evaluation-runtime`.

### Phase 4: Aggregate

Merge worker findings into one documentation audit result.

### Phase 5: Report

Write final documentation audit output and coordinator summary.

### Phase 6: Self-Check

Required checks:
- [ ] mandatory research completed
- [ ] all worker summaries recorded
- [ ] aggregate summary exists
- [ ] cleanup verified
- [ ] coordinator summary recorded

## Summary Contract

Write `summary_kind=evaluation-coordinator`.

## Definition of Done

- [ ] Evaluation runtime started
- [ ] Research completed
- [ ] All documentation audit workers completed
- [ ] Aggregation completed
- [ ] Final report written
- [ ] `evaluation-coordinator` summary written
- [ ] Runtime completed

## Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

After the coordinator run, analyze the session per protocol section 7 and include the protocol-formatted output with the final documentation audit result.

## References

- Workers: `../ln-611-docs-structure-auditor/SKILL.md`, `../ln-612-semantic-content-auditor/SKILL.md`, `../ln-613-code-comments-auditor/SKILL.md`, `../ln-614-docs-fact-checker/SKILL.md`

---
**Version:** 5.0.0
**Last Updated:** 2026-03-01
