---
name: design-sync
description: Sync design docs with codebase state. Use when verifying documentation accuracy, after code changes, or when last-synced is stale.
allowed-tools: Read, Glob, Grep, Edit, Bash
context: fork
agent: design-doc-agent
---

# Design Documentation Synchronization

Synchronizes design documentation with current codebase state by analyzing
source code and updating docs to reflect actual implementation.

## Overview

This skill keeps design documentation aligned with code by extracting file
references and claims from docs, verifying them against actual source code,
identifying discrepancies, and applying safe updates automatically while
flagging unsafe changes for manual review.

## Quick Start

**Basic sync (check-only):**

```bash
/design-sync effect-type-registry
```

**Sync with auto-update:**

```bash
/design-sync effect-type-registry --auto-update
```

**Sync specific document:**

```bash
/design-sync effect-type-registry observability.md
```

## Parameters

### Required

- `module`: Module name to sync (or "all" for all modules)

### Optional

- `doc`: Specific document to sync (default: all docs in module)
- `auto-update`: Automatically apply safe updates (default: false)
- `check-only`: Only report discrepancies, no updates (default: true if
  auto-update not set)

## Workflow

High-level synchronization process:

1. **Parse parameters** to determine module and document scope
2. **Load design.config.json** to get module and package paths
3. **Read design document** and extract file references, exports,
   implementation claims, architecture descriptions, metrics, and dependencies
4. **Analyze source code** to verify each claim against actual code
5. **Generate sync report** with summary, critical issues, warnings, safe
   updates, and items requiring manual review
6. **Apply updates** (safe updates automatically if --auto-update, unsafe
   flagged for review)
7. **Update frontmatter** with last-synced timestamp and sync status
8. **Report results** with actions taken and next steps

For detailed implementation steps, see supporting documentation below.

## Supporting Documentation

When you need detailed information, load the appropriate supporting file:

### For Detailed Workflow

See [instructions.md](instructions.md) for:

- Complete step-by-step synchronization workflow
- Configuration loading and path resolution
- Document content extraction methods
- Source code verification techniques
- Sync report generation structure
- Update application logic (safe vs. unsafe)
- Frontmatter update procedures
- Edge case handling (non-existent code, undocumented code, version
  mismatches, package moves)

**Load when:** Performing synchronization or need implementation details

### For Analysis Strategies

See [analysis-strategies.md](analysis-strategies.md) for:

- File existence verification
- Export verification methods
- Function signature extraction
- Line count comparison
- Dependency checking
- Architecture structure validation
- Performance metric verification
- Static analysis techniques

**Load when:** Need code analysis methods or verification strategies

### For Update Operations

See [update-operations.md](update-operations.md) for:

- Safe update categories (timestamps, typos, line counts, versions)
- Unsafe update categories (signatures, architecture, removed features)
- Update application algorithms
- Rollback procedures
- Conflict resolution strategies
- Batch update operations

**Load when:** Applying updates or need update strategy details

### For Usage Examples

See [examples.md](examples.md) for:

- Basic sync check-only
- Sync with auto-update
- Sync specific document
- Sync all modules
- Example sync reports (clean, warnings, critical issues)
- Error scenarios (missing files, outdated info, broken references)

**Load when:** User needs examples or clarification

## Error Handling

### No Documents Found

```text
INFO: No design documents found to sync

Module: {module}

This is normal for new modules. Run /design-init to create design docs.
```

### Module Not Found

```text
ERROR: Module not configured

Module: {module}

Fix: Add module to design.config.json
```

### Document Not Found

```text
ERROR: Design document not found

Document: {doc}
Path: .claude/design/{module}/{doc}

Fix: Check document name or create with /design-init
```

## Integration

Works well with:

- `/design-validate` - Validate before syncing
- `/design-update` - Update docs after sync identifies issues
- `/design-review` - Review sync status across modules
- `/design-report` - Include sync status in health reports

## Success Criteria

A successful sync:

- ✅ All file references verified
- ✅ All exports checked against code
- ✅ Implementation claims validated
- ✅ Architecture structure confirmed
- ✅ Safe updates applied (if auto-update enabled)
- ✅ Unsafe updates flagged for manual review
- ✅ Last-synced timestamp updated
- ✅ Clear sync report generated
