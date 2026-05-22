---
name: design-report
description: Generate status reports for design documentation. Use when creating documentation summaries, tracking progress, or preparing documentation reviews.
allowed-tools: Read, Glob, Bash
context: fork
agent: design-doc-agent
---

# Design Documentation Status Reports

Generates comprehensive status reports for design documentation, including
progress metrics, health scores, and actionable recommendations.

## Overview

This skill analyzes design documentation to provide insights into
documentation quality, completeness, and health. It calculates progress
metrics, assigns health scores, identifies issues (stale docs, orphans,
sync lag), and provides prioritized recommendations for improvement.

## Quick Start

**Full report:**

```bash
/design-report
```

**Module-specific:**

```bash
/design-report effect-type-registry
```

**JSON output:**

```bash
/design-report --format=json
```

**Focus on health:**

```bash
/design-report --focus=health
```

## Parameters

### Optional

- `module`: Limit to specific module (default: all)
- `format`: Output format (markdown, json, html) (default: markdown)
- `focus`: Report focus (progress, health, gaps, all) (default: all)
- `include-archived`: Include archived docs (default: false)

## Workflow

High-level report generation process:

1. **Parse parameters** to determine scope, format, and focus
2. **Load design.config.json** to identify modules and quality standards
3. **Collect design documents** using Glob, filtering by module and archive
   status
4. **Parse metadata** from frontmatter (status, completeness, dates,
   references)
5. **Calculate progress metrics** (overall, per-module, per-category)
6. **Assess health scores** using weighted formula (completeness, status,
   freshness, relationships)
7. **Identify issues** (stale docs, orphans, incomplete, sync lag, missing
   categories)
8. **Generate report** in requested format with visualizations
9. **Provide recommendations** prioritized by impact and effort

For detailed implementation steps, see supporting documentation below.

## Supporting Documentation

When you need detailed information, load the appropriate supporting file:

### For Detailed Workflow

See [instructions.md](instructions.md) for:

- Complete step-by-step report generation workflow
- Frontmatter parsing and derived metrics calculation
- Progress metrics formulas and aggregation
- Health score calculation with component weights
- Issue detection algorithms and severity assignment
- Report generation for each format
- Recommendation prioritization strategies
- Advanced features (trends, benchmarking, custom focus)

**Load when:** Generating reports or need implementation details

### For Metrics Calculations

See [metrics-calculation.md](metrics-calculation.md) for:

- Progress metrics formulas (coverage, completeness, completion rate)
- Health score calculation with component weights
- Derived metrics (age, staleness, sync lag, velocity)
- Issue detection algorithms
- Trend analysis and benchmarking

**Load when:** Need formula details or implementing custom metrics

### For Report Formats

See [report-formats.md](report-formats.md) for:

- Markdown report structure and sections
- JSON schema and object format
- HTML template with CSS styling
- Format selection guidelines

**Load when:** Generating output or need format specifications

### For Usage Examples

See [examples.md](examples.md) for:

- Full report for all modules
- Module-specific progress report
- Health focus in JSON
- Documentation gaps report
- Module comparison
- Including archived documents
- Error scenarios (no docs, invalid frontmatter)

**Load when:** User needs examples or clarification

## Error Handling

### No Documents Found

```text
INFO: No design documents found in {module}

This is normal for new modules. Run /design-init to create your first
design doc.
```

### Invalid Frontmatter

```text
WARNING: Invalid frontmatter in {file}
Issue: {error-description}

Impact: Document excluded from report
Fix: Run /design-validate {module} to identify and fix issues
```

## Integration

Works well with:

- `/design-review` - Review docs flagged in report
- `/design-validate` - Fix frontmatter issues
- `/design-update` - Improve metrics by updating docs
- `/design-sync` - Sync never-synced or stale docs
- `/design-link` - Resolve orphaned documents

## Success Criteria

A successful report:

- ✅ All design docs discovered and parsed
- ✅ Accurate metrics calculated
- ✅ Health scores computed with weighted formula
- ✅ Issues identified with severity levels
- ✅ Clear, actionable recommendations with priorities
- ✅ Proper format output (markdown/json/html)
- ✅ Insights and trends beyond raw numbers
