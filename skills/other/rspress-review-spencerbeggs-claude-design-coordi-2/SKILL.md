---
name: rspress-review
description: Review RSPress documentation for quality and Twoslash issues. Use when
  checking docs for completeness, accuracy, and code example quality.
allowed-tools: Read, Glob, Grep, Bash
context: fork
agent: rspress-doc-agent
---

# Review RSPress Documentation

Reviews RSPress documentation for quality, completeness, and Twoslash issues.

## Overview

This skill reviews documentation by:

1. Validating MDX syntax and structure
2. Checking Twoslash code blocks compile
3. Verifying cross-references
4. Analyzing content quality
5. Testing navigation flow
6. Identifying issues and recommendations

## Quick Start

**Review all documentation for a module:**

```bash
/rspress-review effect-type-registry
```

**Review specific page:**

```bash
/rspress-review rspress-plugin-api-extractor --page=guides/testing-hooks
```

**Strict mode (warnings as errors):**

```bash
/rspress-review website --strict
```

## How It Works

### 1. Parse Parameters

- `module`: Module name from design.config.json [REQUIRED]
- `--page`: Specific page to review (optional, defaults to all)
- `--strict`: Treat warnings as errors (optional)
- `--fix`: Auto-fix simple issues (optional)
- `--output`: Report output path (optional)

### 2. Load Module Configuration

Reads `design.config.json` to find:

- Site docs path
- API docs location
- Module configuration

### 3. Find Documentation Files

Locates all MDX files in the module:

- Concept pages
- Guide pages
- Example pages
- Landing page

Excludes auto-generated API docs.

### 4. Validate MDX Syntax

Checks each file for:

- Valid frontmatter (YAML)
- Proper heading hierarchy (h1 → h2 → h3)
- Unclosed JSX tags
- Malformed code blocks
- Invalid component imports

### 5. Validate Twoslash Code Blocks

For each `typescript twoslash vfs` block:

- Extract code
- Check all imports are present
- Verify it's a complete TypeScript program
- Attempt compilation
- Report any TypeScript errors
- Check Twoslash annotations are valid

### 6. Verify Cross-References

Check all markdown links:

- Internal links (../concepts/...) resolve to existing files
- API links (../api/classes/...) point to generated docs
- Anchors (#section) exist in target files
- No broken links

### 7. Analyze Content Quality

Review each page for:

- Clear purpose statement
- Proper structure (intro, content, conclusion)
- Active voice usage
- Concise, scannable content
- Code examples present
- Next steps provided

### 8. Test Navigation Flow

Verify navigation structure:

- `_meta.json` files are valid JSON
- All entries reference existing files
- Logical organization (basic → advanced)
- Breadcrumb paths work

### 9. Generate Report

Creates comprehensive report with:

- Overall quality score (0-100)
- Issues by severity (critical, high, medium, low)
- File-by-file breakdown
- Specific recommendations
- Auto-fix suggestions

## Issue Severity Levels

**Critical:**

- MDX syntax errors
- Twoslash compilation failures
- Broken navigation

**High:**

- Missing frontmatter
- Broken cross-references
- Incomplete code examples

**Medium:**

- Readability issues
- Missing sections
- Inconsistent formatting

**Low:**

- Style suggestions
- Minor improvements
- Optional enhancements

## Supporting Documentation

- `instructions.md` - Detailed review process
- `examples.md` - Sample review reports

## Success Criteria

- ✅ All documentation files reviewed
- ✅ Issues categorized by severity
- ✅ Twoslash blocks validated
- ✅ Cross-references checked
- ✅ Quality report generated

## Integration Points

- Uses `.claude/design/design.config.json`
- Reads `rspress.config.ts` for validation context
- Checks files in `{siteDocs}` directory
- Validates against API docs in `{siteDocs}/api/`

## Related Skills

- `/rspress-guide` - Generate guides
- `/rspress-examples` - Generate code examples
- `/rspress-sync` - Sync with API changes
- `/rspress-page` - Scaffold pages
