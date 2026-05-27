---
name: design-audit
description: Comprehensive health audit for design documentation. Use when performing thorough quality checks, preparing for releases, or ensuring documentation compliance.
allowed-tools: Read, Glob, Grep, Bash
context: fork
agent: design-doc-agent
---

# Design Documentation Comprehensive Audit

Performs deep quality audits of design documentation, checking structure,
content, relationships, and compliance with standards.

## Overview

This skill provides comprehensive quality auditing for design documentation
by running all validation checks, analyzing content quality, verifying
cross-reference integrity, checking sync status, and generating detailed
audit reports with prioritized recommendations.

## Quick Start

**Audit all modules:**

```bash
/design-audit
```

**Audit specific module:**

```bash
/design-audit effect-type-registry
```

**Quick audit (non-strict):**

```bash
/design-audit --strict=false
```

## Parameters

### Optional

- `module`: Limit to specific module (default: all)
- `strict`: Enable strict mode (default: true)
- `include-archived`: Include archived docs (default: false)
- `output`: Output file path for report

## Workflow

High-level audit process:

1. **Parse parameters** to determine audit scope and strictness
2. **Load design.config.json** to get quality standards and validation rules
3. **Discover documents** across target modules using Glob
4. **Run validation checks** (frontmatter, structure, content, references, sync)
5. **Analyze content quality** (completeness, depth, examples, rationale)
6. **Check cross-references** for broken links and circular dependencies
7. **Verify sync status** with codebase alignment
8. **Calculate health scores** (document, module, overall)
9. **Identify issues** by severity (critical, high, medium, low)
10. **Generate audit report** with findings and recommendations
11. **Provide recommendations** prioritized by impact and effort

For detailed implementation steps, see supporting documentation below.

## Supporting Documentation

When you need detailed information, load the appropriate supporting file:

### For Detailed Workflow

See [instructions.md](instructions.md) for:

- Complete step-by-step audit workflow
- Document discovery and collection
- Validation check execution
- Content quality analysis algorithms
- Cross-reference integrity verification
- Sync status checking
- Health score calculation formulas
- Issue identification and severity assignment
- Report generation (Markdown, JSON, HTML)
- Recommendation prioritization
- Advanced features (trends, automated fixes, custom checks)

**Load when:** Performing audits or need implementation details

### For Validation Checks

See [checks.md](checks.md) for:

- Frontmatter validation rules (required fields, dates, cross-references)
- Structure validation (sections, headings, hierarchy)
- Content quality checks (completeness, depth, examples)
- Cross-reference integrity (broken links, circular dependencies)
- Sync status thresholds and scoring
- Technical debt detection (TODOs, incomplete sections)
- Overall health scoring formulas and weights
- Health rating ranges (A-F grades)
- Strict mode additional checks

**Load when:** Need check specifications, scoring details, or validation rules

### For Usage Examples

See [examples.md](examples.md) for:

- Full audit of all modules
- Module-specific audit in strict mode
- Quick audit without archived docs
- Audit with JSON output
- Example findings (critical, high, medium, low)
- Report format examples (Markdown, JSON, HTML)

**Load when:** User needs examples or clarification

## Error Handling

### No Documents Found

```text
INFO: No design documents found to audit

Scope: {module}

This is normal for new modules. Run /design-init to create your first
design doc.
```

### All Checks Passed

```text
SUCCESS: All audit checks passed!

Overall Health: {score}/100 ({rating})
No issues found.
```

## Integration

Works well with:

- `/design-validate` - Run validation before full audit
- `/design-review` - Review issues found in audit
- `/design-sync` - Fix sync issues identified
- `/design-update` - Address content quality issues
- `/design-report` - Compare audit with health report

## Success Criteria

A successful audit:

- ✅ All documents discovered and analyzed
- ✅ All validation checks executed
- ✅ Content quality assessed
- ✅ Cross-references verified
- ✅ Sync status checked
- ✅ Health scores calculated accurately
- ✅ Issues categorized by severity
- ✅ Clear, actionable recommendations provided
- ✅ Comprehensive report generated
