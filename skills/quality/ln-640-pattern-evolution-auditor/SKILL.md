---
name: ln-640-pattern-evolution-auditor
description: Audits architectural patterns against best practices (MCP Ref, Context7, WebSearch). Maintains patterns catalog, calculates 4 scores, creates refactor Stories via ln-220. Use when user asks to: (1) Check architecture health, (2) Audit patterns before refactoring, (3) Find undocumented patterns in codebase.
---

# Pattern Evolution Auditor

L2 Coordinator that analyzes implemented architectural patterns against current best practices, tracks evolution over time, and creates Stories for improvements.

## Purpose & Scope

- Maintain `docs/project/patterns_catalog.md` with implemented patterns
- Research best practices via MCP Ref, Context7, WebSearch
- Audit layer boundaries via ln-642 (detect violations, check coverage)
- Calculate 4 scores per pattern via ln-641
- Create Stories for patterns with score < 70% via ln-220
- Track quality trends over time (improving/stable/declining)

## 4-Score Model

| Score | What it measures | Threshold |
|-------|------------------|-----------|
| **Compliance** | Industry standards, ADR/Guide, naming, layer boundaries | 70% |
| **Completeness** | All components, error handling, tests, docs | 70% |
| **Quality** | Readability, maintainability, no smells, SOLID, no duplication | 70% |
| **Implementation** | Code exists, production use, integrated, monitored | 70% |

## Workflow

### Phase 1: Discovery

```
1. Load docs/project/patterns_catalog.md
   IF missing → create from shared/templates/patterns_template.md

2. Load docs/reference/adrs/*.md → link patterns to ADRs
   Load docs/reference/guides/*.md → link patterns to Guides

3. Auto-detect undocumented patterns
   Use patterns from common_patterns.md "Pattern Detection" table
   IF found but not in catalog → add as "Undocumented"
```

### Phase 2: Best Practices Research

```
FOR EACH pattern WHERE last_audit > 30 days OR never:

  # MCP Ref + Context7 + WebSearch
  ref_search_documentation("{pattern} best practices {tech_stack}")
  IF pattern.library: query-docs(library_id, "{pattern}")
  WebSearch("{pattern} implementation best practices 2026")

  → Store: contextStore.bestPractices[pattern]
```

### Phase 3: Layer Boundary Audit

```
Task(ln-642-layer-boundary-auditor)
  Input: architecture_path, codebase_root, skip_violations
  Output: violations[], coverage{}

# Apply deductions to affected patterns (per scoring_rules.md)
FOR EACH violation IN violations:
  affected_pattern = match_violation_to_pattern(violation)
  affected_pattern.issues.append(violation)
  affected_pattern.compliance_deduction += get_deduction(violation)
```

### Phase 4: Pattern Analysis Loop

```
FOR EACH pattern IN catalog:
  Task(ln-641-pattern-analyzer)
    Input: pattern, locations, adr_reference, bestPractices
    Output: scores{}, issues[], gaps{}

  # Merge layer violations from Phase 3
  pattern.issues += layer_violations.filter(v => v.pattern == pattern)
  pattern.scores.compliance -= compliance_deduction
  pattern.scores.quality -= quality_deduction
```

### Phase 5: Gap Analysis

```
gaps = {
  undocumentedPatterns: found in code but not in catalog,
  implementationGaps: ADR decisions not implemented,
  layerViolations: code in wrong architectural layers,
  consistencyIssues: conflicting patterns
}
```

### Phase 6: Story Creation (via ln-220)

**REFACTORING PRINCIPLE (MANDATORY):**
> Stories MUST include: **"Zero Legacy / Zero Backward Compatibility"** — no compatibility hacks, clean architecture is priority.

```
refactorItems = patterns WHERE any_score < 70%

IF refactorItems.length > 0:
  # Auto-detect Epic (Architecture/Refactoring/Technical Debt)
  targetEpic = find_epic(["Architecture", "Refactoring", "Technical Debt"])
  IF not found → AskUserQuestion

  FOR EACH pattern IN refactorItems:
    Task(ln-220-story-coordinator)
      Create Story with AC from issues list
      MANDATORY AC: Zero Legacy principle
```

### Phase 7: Report + Trend Analysis

```
1. Update patterns_catalog.md:
   - Pattern scores, dates, Story links
   - Layer Boundary Status section
   - Quick Wins section
   - Patterns Requiring Attention section

2. Calculate trend: compare current vs previous scores

3. Output summary:
   - Patterns analyzed: N
   - Layer violations: M
   - Architecture Health Score: X%
   - Trend: improving/stable/declining
```

## Critical Rules

- **MCP Ref first:** Always research best practices before analysis
- **Layer audit first:** Run ln-642 before ln-641 pattern analysis
- **4 scores mandatory:** Never skip any score calculation
- **Layer deductions:** Apply scoring_rules.md deductions for violations
- **ln-220 for Stories:** Create Stories, not standalone tasks
- **Zero Legacy:** Refactor Stories must include "no backward compatibility" AC
- **Auto-detect Epic:** Only ask user if cannot determine automatically

## Definition of Done

- Pattern catalog loaded or created
- Best practices researched for all patterns needing audit
- Layer boundaries audited via ln-642 (violations detected, coverage calculated)
- All patterns analyzed via ln-641 (4 scores with layer deductions applied)
- Gaps identified (undocumented, unimplemented, layer violations, inconsistent)
- Stories created via ln-220 for patterns with score < 70%
- Catalog updated with scores, dates, Layer Boundary Status, Story links
- Trend analysis completed
- Summary report output

## Reference Files

- Pattern catalog template: `shared/templates/patterns_template.md`
- Common patterns detection: `references/common_patterns.md`
- Scoring rules: `references/scoring_rules.md`
- Pattern analysis: `../ln-641-pattern-analyzer/SKILL.md`
- Layer boundary audit: `../ln-642-layer-boundary-auditor/SKILL.md`
- Story creation: `../ln-220-story-coordinator/SKILL.md`

---
**Version:** 1.1.0
**Last Updated:** 2026-01-29
