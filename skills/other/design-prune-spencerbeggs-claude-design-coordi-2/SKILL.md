---
name: design-prune
description: Remove historical cruft from design docs. Use when docs accumulate outdated content, after major refactorings, or when preparing for releases.
allowed-tools: Read, Edit, Glob, Bash
context: fork
agent: design-doc-agent
---

# Design Documentation Pruning

Removes historical cruft from design documentation by detecting and removing
outdated content, update histories, and deprecated sections while preserving
essential historical context.

## Overview

This skill cleans up design documentation by identifying historical content
patterns, calculating staleness scores, generating pruning plans, and
applying safe removal strategies to keep docs focused on current state
while preserving important context.

## Quick Start

**Basic pruning:**

```bash
/design-prune effect-type-registry
```

**Aggressive pruning:**

```bash
/design-prune effect-type-registry --aggressive
```

**Dry-run (preview only):**

```bash
/design-prune effect-type-registry --dry-run
```

## Parameters

### Required

- `module`: Module name to prune (or "all" for all modules)

### Optional

- `doc`: Specific document to prune (default: all docs in module)
- `aggressive`: Remove all historical content (default: false, conservative mode)
- `dry-run`: Preview changes without applying (default: false)

## Workflow

High-level pruning process:

1. **Parse parameters** to determine module, document, and pruning mode
2. **Load design.config.json** to get module paths and pruning configuration
3. **Read design document** and parse structure, sections, and content types
4. **Detect historical content** using pattern matching for historical markers
5. **Calculate staleness score** based on age, markers, redundancy, and
   cross-references
6. **Generate pruning plan** with specific actions (remove, condense, archive,
   preserve)
7. **Apply pruning** according to mode (conservative/aggressive/dry-run)
8. **Update frontmatter** with last-pruned date and reduction percentage
9. **Validate result** to ensure document still valid after pruning
10. **Generate pruning report** with summary and actions taken

For detailed implementation steps, see supporting documentation below.

## Supporting Documentation

When you need detailed information, load the appropriate supporting file:

### For Detailed Workflow

See [instructions.md](instructions.md) for:

- Complete step-by-step pruning workflow
- Historical content detection algorithms
- Staleness scoring formulas and categories
- Pruning plan generation
- Pruning execution (conservative, aggressive, dry-run)
- Frontmatter updates
- Validation procedures
- Report generation
- Edge case handling (cross-references, partial historical, conflicting dates)

**Load when:** Performing pruning or need implementation details

### For Pruning Strategies

See [pruning-strategies.md](pruning-strategies.md) for:

- Remove entirely strategy (when and how)
- Condense to summary strategy
- Archive strategy
- Preserve with marker strategy
- Strategy selection criteria
- Safety checks and rollback

**Load when:** Need strategy details or deciding which approach to use

### For Content Patterns

See [content-patterns.md](content-patterns.md) for:

- Historical content markers (keywords, dates, strikethrough)
- Update history patterns
- Deprecated section patterns
- Redundant content patterns
- Pattern matching algorithms
- False positive handling

**Load when:** Detecting historical content or understanding pattern matching

### For Usage Examples

See [examples.md](examples.md) for:

- Basic conservative pruning
- Aggressive pruning
- Dry-run preview
- Pruning specific document
- Example pruning reports (before/after)
- Error scenarios (over-pruning, broken references)

**Load when:** User needs examples or clarification

## Error Handling

### No Historical Content Found

```text
INFO: No historical content detected

Document: {doc}
All content appears current.

No pruning needed.
```

### Over-Pruning Warning

```text
WARNING: Pruning would remove >50% of content

Document: {doc}
Removal: {percentage}%

Suggestion: Review document - consider if it should be archived entirely
or switch to conservative mode.
```

### Broken References After Pruning

```text
ERROR: Pruning would break cross-references

Section: {section}
Referenced by: {other-docs}

Action: Preserved section to maintain references.
Update referencing docs before pruning.
```

## Integration

Works well with:

- `/design-sync` - Sync docs before pruning to ensure currency
- `/design-review` - Identify documents needing pruning
- `/design-validate` - Validate after pruning
- `/design-archive` - Archive documents that are mostly historical

## Success Criteria

A successful pruning:

- ✅ Historical content identified accurately
- ✅ Staleness scores calculated
- ✅ Appropriate pruning strategy applied
- ✅ Cross-references preserved
- ✅ Document still validates
- ✅ Frontmatter updated with pruning metadata
- ✅ Clear pruning report generated
- ✅ Content reduction documented
