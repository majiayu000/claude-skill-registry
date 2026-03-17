---
name: design-archive
description: Archive outdated design documentation. Use when design docs are no longer relevant, have been superseded, or document deprecated features.
allowed-tools: Read, Edit, Bash
context: fork
agent: design-doc-agent
---

# Design Document Archival

Archives design documentation that is no longer relevant or has been superseded
by newer documentation.

## Overview

This skill safely archives design documents by updating their status, adding
archival metadata and notices, updating cross-references, and optionally
moving files to an archive directory. It ensures proper documentation
lifecycle management and maintains documentation integrity.

## Quick Start

**Basic archival:**

```bash
/design-archive effect-type-registry old-cache-design.md
```

**With replacement:**

```bash
/design-archive effect-type-registry cache-v1.md --replacement=cache-optimization.md
```

**Move to archive directory:**

```bash
/design-archive design-doc-system obsolete-patterns.md --move
```

## Parameters

### Required

- `module`: Module name
- `doc`: Document filename to archive

### Optional

- `reason`: Archival reason (superseded, deprecated, obsolete, completed)
- `replacement`: Path to replacement doc (required if superseded)
- `move`: Move to _archive directory (default: false)

## Workflow

High-level archival process:

1. **Parse parameters** to identify document and archival reason
2. **Load design.config.json** to verify module and get paths
3. **Validate archival** (doc exists, not already archived, replacement
   exists if superseded)
4. **Update frontmatter** to set status="archived" and add archival metadata
5. **Add archival notice** prominently at top of document
6. **Update cross-references** in other docs (frontmatter, content links,
   CLAUDE.md)
7. **Optionally move** to _archive directory if --move specified
8. **Report summary** of all actions taken

For detailed implementation steps, see supporting documentation below.

## Supporting Documentation

When you need detailed information, load the appropriate supporting file:

### For Detailed Workflow

See [instructions.md](instructions.md) for:

- Complete step-by-step archival workflow
- Frontmatter update algorithms for each archival reason
- Archive notice templates and insertion logic
- Cross-reference finding and updating procedures
- Archive directory structure and file moving
- Validation requirements and error handling
- Advanced features (batch archival, audit, restoration)

**Load when:** Performing archival or need implementation details

### For Archival Reasons

See [archival-reasons.md](archival-reasons.md) for:

- Superseded: When to use, requirements, best practices
- Deprecated: Deprecation timelines, transition period handling
- Obsolete: Historical preservation guidelines
- Completed: Outcome types and final documentation links
- Choosing the right reason for different scenarios

**Load when:** Need to determine appropriate archival reason or understand
requirements

### For Reference Updates

See [reference-updates.md](reference-updates.md) for:

- Finding references (design docs, CLAUDE.md, indirect)
- Update strategies (replace, note, remove, move)
- Batch update procedures
- Validation checklist

**Load when:** Working with cross-references or batch archival

### For Usage Examples

See [examples.md](examples.md) for:

- Superseded by new doc
- Deprecated feature with timeline
- Move to archive directory
- Completed project
- Multiple references to update
- Error scenarios (already archived, replacement not found)

**Load when:** User needs examples or clarification

## Error Handling

### Document Not Found

```text
ERROR: Design document not found
Module: {module}, Document: {doc}
Expected: .claude/design/{module}/{doc}
```

### Already Archived

```text
INFO: Document is already archived ({date})
Reason: {reason}
No action needed.
```

### Replacement Not Found

```text
ERROR: Replacement document not found
Specified: {replacement}
Fix: Create replacement doc first or correct the path
```

## Integration

Works well with:

- `/design-review` - Identify candidates for archival
- `/design-validate` - Validate before and after archival
- `/design-update` - Update replacement docs
- `/design-init` - Create replacement before archiving

## Success Criteria

A successful archival:

- ✅ Document status changed to "archived"
- ✅ Archival notice added to document
- ✅ Archival metadata complete and accurate
- ✅ All cross-references updated
- ✅ CLAUDE.md references handled
- ✅ Clear summary provided
- ✅ Replacement exists and is adequate (if superseded)
