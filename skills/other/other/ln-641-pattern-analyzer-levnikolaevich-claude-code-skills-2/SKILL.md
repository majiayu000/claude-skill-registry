---
name: ln-641-pattern-analyzer
description: "Analyzes single pattern implementation, calculates compliance/completeness/quality scores, identifies gaps. Use when auditing a specific pattern."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__find_implementations, mcp__hex-graph__find_symbols
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Pattern Analyzer

**Type:** L3 Worker

L3 Worker that analyzes a single architectural pattern against best practices and calculates 4 scores.

## Purpose & Scope
- Analyze ONE pattern per invocation (receives pattern name, locations, best practices from coordinator)
- Find all implementations in codebase (Glob/Grep)
- Validate implementation exists and works
- Calculate 4 scores: compliance, completeness, quality, implementation
- Identify gaps and issues with severity and effort estimates
- Return structured analysis result to coordinator

**Out of Scope** (owned by ln-624-code-quality-auditor):
- Cyclomatic complexity thresholds (>10, >20)
- Method/class length thresholds (>50, >100, >500 lines)
- Quality Score focuses on pattern-specific quality (SOLID within pattern, pattern-level smells), not generic code metrics

## Inputs

```
- pattern: string          # Pattern name (e.g., "Job Processing")
- locations: string[]      # Known file paths/directories
- bestPractices: object    # Best practices from MCP Ref/Context7/WebSearch
- output_dir: string       # e.g., ".hex-skills/runtime-artifacts/runs/{run_id}/audit-report"
```

> **Note:** All patterns arrive pre-verified (passed ln-640 Phase 1d applicability gate with >= 2 structural components confirmed).

## Workflow

**MANDATORY READ:** Load `shared/references/two_layer_detection.md` for detection methodology.

### Phase 1: Find Implementations

**MANDATORY READ:** Load `../ln-640-pattern-evolution-auditor/references/pattern_library.md` -- use "Pattern Detection (Grep)" table for detection keywords per pattern.

```
IF pattern.source == "adaptive":
  # Pattern discovered by coordinator Phase 1b -- evidence already provided
  files = pattern.evidence.files
  SKIP detection keyword search (already done in Phase 1b)
ELSE:
  # Baseline pattern -- use library detection keywords
  files = Glob(locations)
  additional = Grep("{pattern_keywords}", "**/*.{ts,js,py,rb,cs,java}")
  files = deduplicate(files + additional)
```

### Phase 2: Read and Analyze Code

```
FOR EACH file IN files (limit: 10 key files):
  Read(file)
  Extract: components, patterns, error handling, logging, tests
```

### Phase 3: Calculate 4 Scores

**MANDATORY READ:** Load `../ln-640-pattern-evolution-auditor/references/scoring_rules.md` -- follow Detection column for each criterion.

| Score | Source in scoring_rules.md | Max |
|-------|---------------------------|-----|
| Compliance | "Compliance Score" section -- industry standard, naming, conventions, anti-patterns | 100 |
| Completeness | "Completeness Score" section -- required components table (per pattern), error handling, tests | 100 |
| Quality | "Quality Score" section -- method length, complexity, code smells, SOLID | 100 |
| Implementation | "Implementation Score" section -- compiles, production usage, integration, monitoring | 100 |

**Scoring process for each criterion:**
1. Run the Detection Grep/Glob from scoring_rules.md
2. If matches found -> add points per criterion
3. If anti-pattern/smell detected -> subtract per deduction table
4. Document evidence: file path + line for each score justification

### Phase 4: Identify Issues and Gaps

```
FOR EACH bestPractice NOT implemented:
  issues.append({
    severity: "HIGH" | "MEDIUM" | "LOW",
    category: "compliance" | "completeness" | "quality" | "implementation",
    issue: description,
    suggestion: how to fix,
    effort: "S" | "M" | "L"
  })

# Layer 2 context check (MANDATORY):
# Deviation documented in code comment or ADR? -> downgrade to LOW
# Pattern intentionally simplified for project scale? -> skip


gaps = {
  missingComponents: required components not found in code,
  inconsistencies: conflicting or incomplete implementations
}
```

### Phase 5: Calculate Score

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/audit_scoring.md`.

**Diagnostic sub-scores** (0-100 each) are calculated separately and reported in AUDIT-META for diagnostic purposes only:
- compliance, completeness, quality, implementation

### Phase 6: Write Report

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/templates/audit_worker_report_template.md`.

Write JSON summary per `shared/references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

```
# Build pattern name slug: "Job Processing" -> "job-processing"
slug = pattern.name.lower().replace(" ", "-")

# Build markdown report in memory with:
# - AUDIT-META (extended: score [penalty-based] + diagnostic score_compliance/completeness/quality/implementation)
# - Checks table (compliance_check, completeness_check, quality_check, implementation_check)
# - Findings table (issues sorted by severity)
# - DATA-EXTENDED: {pattern, codeReferences, gaps, recommendations}

Write to {output_dir}/ln-641--{slug}.md (atomic single Write call)
```

### Phase 7: Return Summary

```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-641--job-processing.md
Score: 7.9/10 (C:72 K:85 Q:68 I:90) | Issues: 3 (H:1 M:2 L:0)
```

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **One pattern only:** Analyze only the pattern passed by coordinator
- **Read before score:** Never score without reading actual code
- **Detection-based scoring:** Use Grep/Glob patterns from scoring_rules.md, not assumptions
- **Effort estimates:** Always provide S/M/L for each issue
- **Code references:** Always include file paths for findings

## Definition of Done

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- [ ] All implementations found via Glob/Grep (using pattern_library.md keywords or adaptive evidence)
- [ ] Key files read and analyzed
- [ ] 4 scores calculated using scoring_rules.md Detection patterns
- [ ] Issues identified with severity, category, suggestion, effort
- [ ] Gaps documented (missing components, inconsistencies)
- [ ] Recommendations provided
- [ ] Report written to `{output_dir}/ln-641--{slug}.md` (atomic single Write call)
- [ ] Summary written per contract

## Reference Files

- Scoring rules: `../ln-640-pattern-evolution-auditor/references/scoring_rules.md`
- Pattern library: `../ln-640-pattern-evolution-auditor/references/pattern_library.md`
- **MANDATORY READ:** `shared/references/research_tool_fallback.md`

---
**Version:** 2.0.0
**Last Updated:** 2026-02-08
