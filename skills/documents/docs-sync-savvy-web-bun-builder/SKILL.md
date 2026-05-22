---
name: docs-sync
description: Sync user documentation with design doc changes. Use when design docs
  have been updated and user docs need to reflect the changes.
allowed-tools: Read, Glob, Edit, Write
context: fork
agent: docs-gen-agent
---

# Sync User Documentation

Syncs user documentation with changes in design docs to keep them current.

## Overview

This skill detects changes in design docs and updates corresponding
user documentation by:

1. Comparing design doc timestamps with user doc timestamps
2. Identifying which user docs are affected
3. Regenerating or updating affected sections
4. Preserving custom user-added content
5. Updating sync timestamps

## Quick Start

**Sync all levels for a module:**

```bash
/docs-sync effect-type-registry
```

**Sync specific level only:**

```bash
/docs-sync rspress-plugin-api-extractor --level=1
```

**Preview changes without writing:**

```bash
/docs-sync website --dry-run
```

## How It Works

### 1. Parse Parameters

- `module`: Module to sync [REQUIRED]
- `--level`: Sync specific level (1=README, 2=repo, 3=site)
- `--dry-run`: Preview changes without writing

### 2. Detect Changes

Compare timestamps:

- Design doc `updated` field
- User doc last modification time
- Identify stale user docs (design newer than user docs)

### 3. Analyze Impact

For each changed design doc:

- Determine which user docs it affects
- Identify sections that need updates
- Check for breaking changes

### 4. Update User Documentation

Update strategies:

- **README** - Regenerate features, quick start, API overview
- **Repository Docs** - Update affected topic guides
- **Site Docs** - Refresh concept docs and guides

### 5. Preserve Custom Content

Protect user additions:

- Custom examples
- Additional sections
- Badges and shields
- Screenshots and GIFs

### 6. Update Timestamps

Mark synced docs with current timestamp.

## Supporting Documentation

- `instructions.md` - Detailed sync process
- `examples.md` - Sync scenarios and outputs

## Success Criteria

- ✅ Stale docs identified correctly
- ✅ Affected sections updated
- ✅ Custom content preserved
- ✅ Timestamps updated
- ✅ No broken links introduced

## Integration Points

- Uses `.claude/design/design.config.json`
- Reads design docs from `designDocsPath`
- Updates files in `userDocs` paths
- Respects quality standards

## Related Skills

- `/docs-generate-readme` - Regenerate README
- `/docs-generate-repo` - Regenerate repo docs
- `/docs-generate-site` - Regenerate site docs
- `/docs-review` - Review sync quality
