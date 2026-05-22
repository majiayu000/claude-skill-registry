---
name: design-review
description: Review and analyze design docs for health, quality, and improvement opportunities. Use when auditing design documentation, checking doc health, or identifying areas for improvement.
allowed-tools: Read, Glob, Bash
context: fork
agent: design-doc-agent
---

# Design Documentation Review

Analyzes design documentation for health, quality, and actionable improvement
opportunities.

## Overview

This skill performs comprehensive health checks on design documentation by:

1. Reading all design docs for a module (or all modules)
2. Analyzing frontmatter completeness and accuracy
3. Checking documentation quality and thoroughness
4. Identifying missing or outdated content
5. Finding broken cross-references
6. Assessing status progression and maintenance
7. Providing prioritized recommendations

## Quick Start

**Review single module:**

```bash
/design-review effect-type-registry
```

**Review all modules:**

```bash
/design-review all
```

**Detailed analysis:**

```bash
/design-review all --verbose
```

**Focus on specific aspect:**

```bash
/design-review rspress-plugin-api-extractor --focus=completeness
```

## Parameters

### Required

- `target` - Module name to review, or "all" for all modules

### Optional

- `verbose` - Show detailed analysis (default: false)
- `focus` - Specific aspect: completeness | quality | references | maintenance

## Workflow Overview

1. **Parse Parameters** - Extract target and options
2. **Load Configuration** - Read config for module paths and standards
3. **Find Documents** - Glob all markdown files (skip `_` prefixed)
4. **Analyze Each Document** - Run health checks (see
   [analysis-checks.md](analysis-checks.md))
5. **Calculate Scores** - Compute health scores (see
   [scoring-reports.md](scoring-reports.md))
6. **Generate Report** - Create comprehensive findings report
7. **Focus Reports** - Generate targeted analysis if focus specified

## Supporting Documentation

### For Analysis Criteria

See [analysis-checks.md](analysis-checks.md) for:

- Frontmatter health check criteria (status, completeness, staleness)
- Content quality assessment rules (overview, rationale, implementation)
- Structure validation requirements (sections, TOC, formatting)
- Cross-reference validation logic (related, dependencies, links)
- Maintenance health indicators (abandonment, duplication, scope)

**Load when:** Performing detailed document analysis or diagnosing specific
issues

### For Scoring and Reports

See [scoring-reports.md](scoring-reports.md) for:

- Health score calculation formulas (4 components: completeness, recency,
  quality, references)
- Scoring rubrics for each component (0-100 scale)
- Report format templates (executive summary, findings, recommendations)
- Priority classification system (critical, warning, info)
- Recommendation frameworks (impact/effort matrix)

**Load when:** Computing health scores or generating reports

### For Usage Examples

See [examples.md](examples.md) for:

- Complete usage scenarios (basic, verbose, focused reviews)
- Example outputs for different review types
- Focus-specific reports (completeness, quality, references, maintenance)
- Success report format

**Load when:** User wants to see concrete examples or needs clarification on
output format

## Health Score Components

Overall Health = (Completeness + Recency + Quality + References) / 4

- 🟢 **Healthy** (80-100): Well-maintained, comprehensive documentation
- 🟡 **Needs Attention** (60-79): Some issues, improvement recommended
- 🔴 **Critical** (<60): Significant issues, immediate action required

## Integration

Use this skill with:

- `/design-validate` - Fix structural/frontmatter issues first
- `/design-update` - Apply recommended improvements
- `/design-sync` - Address staleness and sync issues
- `/design-prune` - Remove historical cruft identified in review

## Success Criteria

A successful review:

- ✅ Analyzes all docs in target module(s)
- ✅ Identifies critical issues requiring immediate action
- ✅ Provides specific, actionable recommendations
- ✅ Calculates accurate health scores
- ✅ Prioritizes improvements by impact and effort
- ✅ Gives clear next steps
