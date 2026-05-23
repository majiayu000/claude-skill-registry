---
name: ln-641-pattern-fitness-auditor
description: "Audits whether one implemented architectural pattern fits project needs and best practices. Use when checking pattern fitness."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__find_implementations, mcp__hex-graph__find_symbols, mcp__hex-line__read_file, mcp__hex-line__grep_search, mcp__hex-line__outline
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

# Pattern Fitness Auditor

**Type:** L3 Worker

L3 Worker that analyzes a single architectural pattern against best practices and project needs.

## Purpose & Scope
- Analyze ONE pattern per invocation (receives pattern name, locations, best practices)
- Find all implementations in codebase (Glob/Grep)
- Validate implementation exists and works
- Calculate 4 scores: compliance, completeness, quality, implementation
- Identify gaps and issues with severity and effort estimates
- Return structured analysis result
- Emit `KEEP_PATTERN`, `SIMPLIFY_PATTERN`, `COMPLETE_PATTERN`, or `REPLACE_PATTERN`

**Out of Scope:**
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

> **Note:** If pattern evidence is provided by a managed run, use that evidence instead of rediscovering the same pattern from scratch.

## Workflow

Detection policy: use two-layer detection (candidate scan, then context verification); load `references/two_layer_detection.md` only when the verification method is ambiguous.
Tool policy: follow host AGENTS.md MCP preferences; load `references/mcp_tool_preferences.md` and `references/mcp_integration_patterns.md` only when host policy is absent or MCP behavior is unclear.

Use `hex-graph` first when implementation discovery materially improves confidence. Use `hex-line` first for local code reads when available. If MCP is unavailable, unsupported, or not indexed, continue with built-in `Read/Grep/Glob/Bash` and state the fallback in the report.

### Phase 1: Find Implementations

**MANDATORY READ:** Load `references/pattern_library.md` -- use "Pattern Detection (Grep)" table for detection keywords per pattern.

```
IF pattern.source == "adaptive":
  # Pattern evidence was already provided by the caller
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

**MANDATORY READ:** Load `references/scoring_rules.md` -- follow Detection column for each criterion.

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

**MANDATORY READ:** Load `references/audit_worker_core_contract.md` and `references/audit_scoring.md`.

**Diagnostic sub-scores** (0-100 each) are calculated separately and reported in AUDIT-META for diagnostic purposes only:
- compliance, completeness, quality, implementation

### Phase 6: Write Report

**MANDATORY READ:** Load `references/templates/audit_worker_report_template.md`.

Write JSON summary per `references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

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

Apply the already-loaded `references/audit_worker_core_contract.md`.

- **One pattern only:** Analyze only the pattern provided in input
- **Read before score:** Never score without reading actual code
- **Detection-based scoring:** Use Grep/Glob patterns from scoring_rules.md, not assumptions
- **Effort estimates:** Always provide S/M/L for each issue
- **Code references:** Always include file paths for findings
- **Unique angle:** Audit one pattern's architectural fitness only. Do not audit generic code quality, dependency topology, package health, or runtime operations.
- **Action required:** Every finding uses `KEEP_PATTERN`, `SIMPLIFY_PATTERN`, `COMPLETE_PATTERN`, or `REPLACE_PATTERN`.

## Definition of Done

Apply the already-loaded `references/audit_worker_core_contract.md`.

- [ ] All implementations found via Glob/Grep (using pattern_library.md keywords or adaptive evidence)
- [ ] Key files read and analyzed
- [ ] 4 scores calculated using scoring_rules.md Detection patterns
- [ ] Issues identified with severity, category, suggestion, effort
- [ ] Gaps documented (missing components, inconsistencies)
- [ ] Recommendations provided
- [ ] Report written to `{output_dir}/ln-641--{slug}.md` (atomic single Write call)
- [ ] Summary written per contract

## Reference Files

- Scoring rules: `references/scoring_rules.md`
- Pattern library: `references/pattern_library.md`

---
**Version:** 2.0.0
**Last Updated:** 2026-02-08
