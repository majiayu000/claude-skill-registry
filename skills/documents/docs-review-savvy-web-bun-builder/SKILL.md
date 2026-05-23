---
name: docs-review
description: Review user doc quality. Use when checking documentation completeness,
  accuracy, readability, and ensuring examples work correctly.
allowed-tools: Read, Glob, Bash
context: fork
agent: docs-gen-agent
---

# Review User Documentation

Reviews user documentation for quality, completeness, and accuracy.

## Overview

This skill reviews user documentation by:

1. Checking readability metrics
2. Validating code examples
3. Ensuring design concepts are covered
4. Checking for broken links
5. Validating framework-specific syntax
6. Identifying missing sections

## Quick Start

**Review all levels for a module:**

```bash
/docs-review effect-type-registry
```

**Review specific level only:**

```bash
/docs-review rspress-plugin-api-extractor --level=2
```

**Strict mode (warnings as errors):**

```bash
/docs-review website --strict
```

## How It Works

### 1. Parse Parameters

- `module`: Module to review
- `--level`: Review specific level (1, 2, or 3)
- `--strict`: Treat warnings as errors

### 2. Check Readability

Analyze text for:

- Flesch reading ease score
- Average sentence length
- Technical jargon usage
- Active vs passive voice

### 3. Validate Code Examples

For each code example:

- Syntax validation
- Completeness (imports included)
- Copy-paste ready
- Comments for clarity

### 4. Check Coverage

Ensure all design doc topics covered:

- Major features documented
- Architecture concepts explained
- Integration points shown
- Troubleshooting included

### 5. Validate Links

Check all links:

- Internal links resolve
- External links accessible
- Anchors exist
- Cross-references valid

### 6. Framework Syntax

For Level 3 docs:

- MDX syntax valid
- Framework components correct
- Frontmatter complete
- Navigation configured

### 7. Generate Report

Quality report with:

- Overall score (0-100)
- Issues by severity
- Specific recommendations
- Missing sections

## Quality Metrics

### Level 1 (README)

- Length: 200-500 words
- Readability: >60 (plain English)
- Examples: 1-3
- Required sections present

### Level 2 (Repository)

- Coverage: 1 doc per major topic
- Length: 500-2000 words per doc
- Readability: >50
- Examples: 2+ per guide

### Level 3 (Site)

- All topics covered
- Progressive navigation
- Interactive elements used
- Mobile responsive

## Supporting Documentation

- `instructions.md` - Review process details
- `examples.md` - Review reports

## Success Criteria

- ✅ Complete quality report generated
- ✅ Issues categorized by severity
- ✅ Actionable recommendations provided
- ✅ Code examples validated
- ✅ Readability scored accurately

## Integration Points

- Uses `.claude/design/design.config.json`
- Reads user docs from `userDocs` paths
- Validates against quality standards
- Can trigger regeneration if needed

## Related Skills

- `/docs-sync` - Sync after fixing issues
- `/docs-generate-readme` - Regenerate README
- `/docs-generate-repo` - Regenerate repo docs
- `/docs-generate-site` - Regenerate site docs
