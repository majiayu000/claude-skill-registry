---
name: doc-maintain
description: Maintain documentation (sync, cleanup, update)
user-invocable: true
allowed-tools: Skill, Read, Write, Edit, Glob, Grep, Bash
---

# Documentation Maintain Skill

Maintenance operations for existing documentation: sync with code, cleanup stale content, refresh metadata.

## Parameters

- **action** (required): sync|cleanup|update
- **target** (optional): File or directory (default: current directory)

## Workflow

### Step 1: Parse Parameters

```
If action not provided OR action not in [sync, cleanup, update]:
  Show usage and exit
```

**Usage:**
```
/doc-maintain action=<action> [target=<path>]

Parameters:
  action - Required: sync|cleanup|update
  target - Optional: File or directory (default: .)

Actions:
  sync    - Sync documentation with code changes
  cleanup - Remove stale/duplicate documentation
  update  - Refresh metadata and cross-references

Examples:
  /doc-maintain action=update
  /doc-maintain action=sync target=standards/
  /doc-maintain action=cleanup target=docs/
  /doc-maintain action=update target=README.adoc
```

### Step 2: Validate Target

```
If target is file:
  Verify file exists and has .adoc extension
  scope = "single"

If target is directory:
  Verify directory exists
  scope = "batch"

If target not found:
  Error: "Target not found: {target}"
```

### Step 3: Load Documentation Skill

```
Skill: pm-documents:ref-documentation
```

### Step 4: Execute Action

**For action = sync:**
```
Execute workflow: sync-with-code
Parameters:
  target: {target}
  code_path: src/ (or auto-detect)

Reports:
- Code changes without documentation
- Documentation for removed code
- Outdated documentation sections
```

**For action = cleanup:**
```
Execute workflow: cleanup-stale
Parameters:
  target: {target}

Reports:
- Duplicate content across files
- Orphaned documentation
- Stale content with TODOs

Prompts user before any removal.
```

**For action = update:**
```
Execute workflow: refresh-metadata
Parameters:
  target: {target}

Actions:
- Fix broken cross-references
- Update header metadata
- Ensure consistent formatting
```

### Step 5: Generate Report

**For sync:**
```
═══════════════════════════════════════════════
Documentation Sync Report
═══════════════════════════════════════════════

Target: {target}
Code analyzed: {file_count} files

Drift Detected:
X {count} items need attention

Details:
- {description of each drift item}

Recommendations:
1. {action to take}
```

**For cleanup:**
```
═══════════════════════════════════════════════
Documentation Cleanup Report
═══════════════════════════════════════════════

Target: {target}
Files analyzed: {count}

Candidates:
- Duplicates: {count}
- Orphaned: {count}
- Stale: {count}

{Detailed list of candidates}

Actions Taken:
- {list of cleanup actions performed}
```

**For update:**
```
═══════════════════════════════════════════════
Documentation Update Report
═══════════════════════════════════════════════

Target: {target}
Files processed: {count}

Updates Applied:
Y Metadata fixed: {count}
Y Cross-references fixed: {count}
Y Headers updated: {count}

Manual Review Needed:
- {file}: {reason}
```

## Architecture

**Pattern**: Thin Orchestrator (~110 lines)
- Parses action and target
- Routes to appropriate skill workflow
- No business logic in skill

**Skill Dependency**: pm-documents:ref-documentation
- Provides: sync-with-code, cleanup-stale, refresh-metadata workflows

## Related

- `/doc-doctor` - Diagnose documentation issues
- `/doc-create` - Create new documentation
- `ref-documentation` skill - Provides maintenance workflows
