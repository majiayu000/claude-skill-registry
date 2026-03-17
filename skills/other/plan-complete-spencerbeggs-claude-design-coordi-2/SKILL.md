---
name: plan-complete
description: Complete a plan by updating design docs and removing the transitory plan file. Use when implementation is finished and knowledge should be persisted to design documentation.
allowed-tools: Read, Edit, Write, Bash
context: fork
agent: design-doc-agent
---

# Plan Completion

Completes implementation plans by updating linked design documentation,
recording completion metadata, and removing the transitory plan file.

## Overview

Plans are ephemeral work tracking (like GitHub issues). When work is done,
this skill:

1. Validates completion requirements
2. Updates linked design docs with implementation status
3. Records completion metadata
4. Deletes the plan file (knowledge now lives in design docs)

**Philosophy:** Plans are temporary. Design docs are permanent.

## Quick Start

**Complete a plan:**

```bash
/plan-complete plan-design-linking-phase-1
```

**With custom outcome:**

```bash
/plan-complete cache-optimization --outcome=partial
```

**Dry run (preview changes):**

```bash
/plan-complete subagent-integration --dry-run
```

## Parameters

### Required

- `plan-name`: Plan identifier (without .md extension)

### Optional

- `--outcome`: Completion outcome (success, partial, failed) [default: success]
- `--dry-run`: Preview changes without executing
- `--keep`: Keep plan file after completion (for reference)

## Workflow

High-level completion process:

1. **Load plan** from `.claude/plans/{plan-name}.md`
2. **Validate completion requirements** (status, progress, linked docs exist)
3. **Update design docs** (status, last-synced, completion metadata)
4. **Record completion** in design doc frontmatter
5. **Delete plan file** (unless --keep specified)
6. **Generate report** of all actions taken

For detailed implementation steps, see supporting documentation below.

## Supporting Documentation

When you need detailed information, load the appropriate supporting file:

### For Completion Workflow

See [instructions.md](instructions.md) for:

- Step-by-step completion process
- Design doc update procedures
- Completion metadata format
- Validation requirements
- Error handling and rollback

**Load when:** Performing completion or need implementation details

### For Design Doc Updates

See [design-doc-updates.md](design-doc-updates.md) for:

- Updating status (draft → current, stub → current)
- Recording completion metadata format
- Handling multiple linked design docs
- Last-synced timestamp updates
- Bidirectional link cleanup

**Load when:** Working with design doc updates or metadata

### For Usage Examples

See [examples.md](examples.md) for:

- Complete successful implementation
- Partial completion with notes
- Failed implementation (knowledge still valuable)
- Multiple design docs linked
- Dry run preview
- Keep plan file for reference

**Load when:** User needs examples or clarification

## Validation Requirements

Before completion, the skill verifies:

### Plan Requirements

- ✅ Plan file exists
- ✅ Status is "completed" or can be set to completed
- ✅ Progress is 100%
- ✅ All required frontmatter fields present
- ✅ Has `implements` field with design docs

### Design Doc Requirements

- ✅ All linked design docs exist
- ✅ Design docs are in appropriate state (draft/stub)
- ✅ Bidirectional links are correct

### Implementation Evidence

- ✅ Design docs have been updated with implementation details
- ✅ Last-synced is reasonably recent (< 30 days)
- ✅ Completeness score increased during implementation

## What Gets Updated

### Design Doc Frontmatter

```yaml
status: current  # Was: draft or stub
last-synced: 2026-01-18  # Today's date
completeness: 95  # Should be high after implementation

# New completion metadata
completed-plans:
  - name: "plan-design-linking-phase-1"
    completed: "2026-01-18"
    outcome: "success"
```

### Plan File

**Deleted** (unless `--keep` specified) because:

- Knowledge now lives in design docs
- Plan was temporary work tracking
- Reduces clutter in `.claude/plans/`

## Error Handling

### Plan Not Completed

```text
ERROR: Cannot complete plan with status 'in-progress'

Current state:
  Status: in-progress
  Progress: 75%

Required state:
  Status: completed
  Progress: 100%

Fix: Update plan frontmatter first, then complete
```

### Linked Design Docs Missing

```text
ERROR: Linked design doc not found
Plan implements: design-doc-system/missing-doc.md
Path checked: .claude/design/design-doc-system/missing-doc.md

Fix: Create design doc or fix path in plan frontmatter
```

### Design Doc Already Current

```text
WARNING: Design doc already marked as current
Doc: effect-type-registry/observability.md
Status: current
Last-synced: 2026-01-15

This may indicate the plan was already completed.
Continue anyway? (y/n)
```

## Integration

Works well with:

- `/plan-validate` - Validate before completing
- `/design-sync` - Sync design docs before completion
- `/design-review` - Review updated docs
- `/plan-list` - Find completed plans

## Success Criteria

A successful completion:

- ✅ All linked design docs updated to current status
- ✅ Completion metadata recorded
- ✅ Last-synced timestamps updated
- ✅ Plan file deleted (or kept if requested)
- ✅ Clear completion report generated
- ✅ No broken links remain

## Rollback

If something goes wrong during completion:

1. Design doc changes are in git (can revert)
2. Plan file deletion is final (but can recreate if needed)
3. Recommendation: Use `--dry-run` first for preview
