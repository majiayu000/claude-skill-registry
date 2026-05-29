---
name: rspress-sync
description: Sync site docs with API changes. Use when APIs have been updated and
  documentation needs to reflect the changes.
allowed-tools: Read, Glob, Grep, Edit, Write
context: fork
agent: rspress-doc-agent
---

# Sync RSPress Documentation with API Changes

Syncs RSPress site documentation with changes in auto-generated API docs.

## Overview

This skill detects API changes and updates user-facing documentation by:

1. Comparing API doc timestamps with user doc timestamps
2. Identifying stale documentation
3. Updating cross-references
4. Updating code examples
5. Adding migration notes for breaking changes
6. Preserving custom content

## Quick Start

**Sync all documentation for a module:**

```bash
/rspress-sync effect-type-registry
```

**Check what needs syncing (dry run):**

```bash
/rspress-sync rspress-plugin-api-extractor --check-only
```

**Force sync all docs:**

```bash
/rspress-sync website --force
```

## How It Works

### 1. Parse Parameters

- `module`: Module name from design.config.json [REQUIRED]
- `--check-only`: Report what needs syncing without writing (optional)
- `--force`: Sync all docs regardless of timestamps (optional)
- `--breaking`: Add breaking change notes (optional)

### 2. Load Configuration

Reads `design.config.json` to find:

- Site docs path
- API docs location
- Module package name

### 3. Detect API Changes

Compares timestamps:

- Get modification times of all API docs (`{siteDocs}/api/**/*.md`)
- Get modification times of all user docs (`{siteDocs}/**/*.mdx`)
- Identify user docs older than latest API changes

### 4. Analyze Impact

For each changed API doc:

- Parse API doc to understand what changed
- Identify which user docs reference this API
- Determine if changes are breaking or non-breaking
- Collect affected code examples

### 5. Update Cross-References

Fix broken or outdated links:

- Update paths if API docs moved
- Fix renamed classes/functions/interfaces
- Update anchors if heading structure changed
- Remove references to deleted APIs

### 6. Update Code Examples

Refresh Twoslash code blocks:

- Update imports if package exports changed
- Fix type signatures if APIs changed
- Add new parameters if required
- Remove deprecated usage patterns

### 7. Add Migration Notes

For breaking changes:

- Insert callout with migration instructions
- Show before/after code examples
- Link to changelog or release notes
- Highlight deprecated alternatives

### 8. Preserve Custom Content

Protect user additions:

- Keep custom sections
- Preserve added examples
- Maintain editorial content
- Only update generated portions

### 9. Generate Sync Report

Creates report with:

- Files updated
- Changes made
- Migration notes added
- Remaining manual updates needed

## Sync Strategies

### Non-Breaking Changes

For minor API updates:

- Update code examples silently
- Fix cross-references
- No migration notes needed

### Breaking Changes

For major API changes:

- Add prominent callout
- Include before/after examples
- Link to migration guide
- Mark deprecated patterns

### New APIs

For new functionality:

- Consider adding new guide pages
- Add examples to existing pages
- Update landing page features
- Refresh table of contents

### Removed APIs

For deleted functionality:

- Remove or mark as removed
- Add deprecation notice
- Suggest alternatives
- Link to migration path

## Supporting Documentation

- `instructions.md` - Detailed sync process
- `examples.md` - Sample sync operations

## Success Criteria

- ✅ Stale docs identified correctly
- ✅ Cross-references updated
- ✅ Code examples compile
- ✅ Migration notes added for breaking changes
- ✅ Custom content preserved
- ✅ Sync report generated

## Integration Points

- Uses `.claude/design/design.config.json`
- Reads API docs from `{siteDocs}/api/`
- Updates user docs in `{siteDocs}/`
- Reads `rspress.config.ts` for context

## Related Skills

- `/rspress-guide` - Generate new guides
- `/rspress-examples` - Update code examples
- `/rspress-review` - Review synced docs
- `/rspress-navigation` - Update navigation
