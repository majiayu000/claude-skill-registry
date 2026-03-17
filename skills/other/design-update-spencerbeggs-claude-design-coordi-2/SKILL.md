---
name: design-update
description: Update specific design document with new content or metadata. Use when modifying design docs, updating status/completeness, or syncing after code changes.
allowed-tools: Read, Edit, Bash
context: fork
agent: design-doc-agent
---

# Design Document Update

Updates design documentation files with new content, metadata changes, or
structural improvements.

## Overview

This skill updates design documents by:

1. Reading the current design doc
2. Understanding the requested changes
3. Validating changes against schema
4. Updating frontmatter metadata
5. Modifying content sections
6. Running validation checks
7. Confirming changes applied correctly

## Quick Start

**Update status:**

```bash
/design-update effect-type-registry cache-optimization.md --status=draft
```

**Update completeness:**

```bash
/design-update effect-type-registry observability.md --completeness=80
```

**Mark as synced:**

```bash
/design-update effect-type-registry cache-optimization.md --sync
```

**Update section:**

```bash
/design-update rspress-plugin-api-extractor type-loading.md --section=Overview
```

**Bulk update:**

```bash
/design-update effect-type-registry observability.md \
  --status=current --completeness=90 --sync
```

## Parameters

### Required

- `module` - Module name
- `doc` - Document filename (without path)

### Optional

- `status` - New status (stub, draft, current, needs-review, archived)
- `completeness` - New completeness (0-100)
- `section` - Specific section to update
- `content` - New content to add/replace
- `sync` - Mark as synced (sets last-synced to current date)
- `add-related` - Add cross-reference to related doc
- `add-dependency` - Add dependency reference

## Workflow Overview

1. **Parse Parameters** - Extract module, doc, and change parameters
2. **Load Configuration** - Read config, verify module exists
3. **Read Document** - Parse current frontmatter and content
4. **Apply Updates** - Frontmatter or content changes
5. **Validate Changes** - Check alignment and correctness
6. **Smart Recommendations** - Suggest related updates
7. **Report Changes** - Summary with validation results

## Supporting Documentation

### For Update Operations

See [update-operations.md](update-operations.md) for:

- All supported update operations (frontmatter fields, content sections)
- Validation rules for each operation
- Bulk update operations
- Output format templates

**Load when:** Performing specific updates or need validation rules

### For Smart Completeness

See [completeness-estimation.md](completeness-estimation.md) for:

- Completeness estimation algorithm
- Section analysis scoring
- Placeholder detection
- Content depth assessment
- Smart suggestion logic

**Load when:** Estimating completeness or validating declared values

### For Usage Examples

See [examples.md](examples.md) for:

- Complete update scenarios (status, completeness, sections)
- Bulk updates
- Cross-reference management
- Smart estimation examples
- Common update patterns

**Load when:** User needs concrete examples or clarification

## Status-Completeness Matrix

Quick reference for alignment:

| Completeness | Expected Status |
| :----------- | :-------------- |
| 0-20 | stub |
| 21-60 | draft |
| 61-90 | current, needs-review |
| 91-100 | current |

## Integration

Use this skill with:

- `/design-validate` - Validate after updates
- `/design-sync` - Sync with codebase before updating
- `/design-review` - Review to identify needed updates
- `/design-init` - Create before updating

## Success Criteria

A successful update:

- ✅ Changes applied correctly
- ✅ Frontmatter valid and consistent
- ✅ Status-completeness aligned
- ✅ All validations pass
- ✅ User receives clear summary
- ✅ Recommendations provided
