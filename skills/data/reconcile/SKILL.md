---
name: reconcile
description: Reconcile increment ID collisions after multi-developer merge. Renumbers conflicting increments based on modification dates.
---

# Reconcile Increment IDs

**Post-merge command for multi-developer workflows.** When multiple developers create increments with the same ID on different branches, run this after merging to resolve collisions by renumbering.

## Philosophy

**Renumber, don't delete.** Unlike `/sw:fix-duplicates` which removes duplicates, this command:
- Keeps ALL increments intact
- Renumbers the "later" ones (by modification date) to next available IDs
- Updates all references (metadata, living docs, external sync)
- Creates audit trail of what was renamed

## When to Use

Run after merging branches that may have created increments with same IDs:

```bash
git checkout main
git merge feature-branch-a
git merge feature-branch-b
/sw:reconcile           # Fix any ID collisions
git add . && git commit -m "reconcile: fix increment ID collisions"
```

## Usage

```bash
# Detect and fix all ID collisions (interactive)
/sw:reconcile

# Preview what would change (dry-run)
/sw:reconcile --dry-run

# Auto-fix without confirmation
/sw:reconcile --force

# Check specific increment number
/sw:reconcile 0001
```

## Options

- `<increment-number>`: Optional. Check only collisions for specific number (e.g., "0001")
- `--dry-run`: Show what would change without making modifications
- `--force`: Skip confirmation prompts (for CI/scripts)
- `--by-commit`: Use git commit date instead of file modification date for ordering

## How It Works

### Step 1: Detection

Scans ALL increment directories for ID collisions:
- `.specweave/increments/NNNN-*` (active)
- `.specweave/increments/_archive/NNNN-*`
- `.specweave/increments/_abandoned/NNNN-*`
- `.specweave/increments/_paused/NNNN-*`

**Collision detection**:
- Same base number (e.g., two `0001E-*` folders)
- OR same number with different E-suffix (e.g., `0001-*` and `0001E-*`)

### Step 2: Chronological Ordering

Uses file modification dates to determine which increment came first:

```
0001E-auth-feature/      modified: 2026-01-15 10:00
0001E-payment-feature/   modified: 2026-01-20 14:30  ← LATER (renumber)
```

**Date sources (priority order)**:
1. `metadata.json` → `created` field
2. `spec.md` file modification time
3. Directory modification time
4. Git first commit date (if `--by-commit`)

### Step 3: Renumbering

The "later" increment gets renumbered to next available ID:

```
BEFORE:
  0001E-auth-feature/        (Jan 15)
  0001E-payment-feature/     (Jan 20)

AFTER:
  0001E-auth-feature/        (kept as 0001E)
  0002E-payment-feature/     (renumbered to 0002E)
```

### Step 4: Reference Updates

Updates ALL references to the renumbered increment:

**Local Files:**
1. **metadata.json** - Updates `id` field, adds `reconcileHistory` entry
2. **spec.md frontmatter** - Updates `increment:` field
3. **Living docs** - Renames `FS-XXX` folders in `.specweave/docs/internal/specs/`
   - Updates `FEATURE.md` frontmatter and content
   - Updates all `us-*.md` user story files

**External Tools (automatically updated via API):**
4. **GitHub**:
   - Milestone titles containing old feature ID
   - Issue titles with `[FS-XXX]` prefix
   - Uses `gh` CLI for updates
5. **JIRA**:
   - Epic/story summary (title) containing old feature ID
   - Uses JIRA REST API v3
6. **ADO**:
   - Feature/user story `System.Title` field
   - Uses ADO REST API

### Step 5: Audit Report

Creates `reports/RECONCILE-{timestamp}.md` documenting:
- Original ID → New ID mapping
- Which references were updated
- Modification dates used for ordering

## Examples

### Example 1: Two External Imports Collision

Two developers imported issues from JIRA, both got 0001E:

```bash
/sw:reconcile
```

**Output**:
```
🔄 Scanning for ID collisions...

Found 1 collision:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Collision: Base ID 0001E (2 increments)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Increments (ordered by modification date):
  1. 0001E-auth-feature           (2026-01-15) → KEEP
  2. 0001E-payment-feature        (2026-01-20) → RENUMBER to 0002E

Proceeding with reconciliation...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Collisions found: 1
Increments renumbered: 1
References updated: 7

📦 Operations performed:

  ✓ 0001E-payment-feature → 0002E-payment-feature
    Feature: FS-001E → FS-002E
    Updated:
      ✓ metadata: Renamed folder
      ✓ metadata: Updated id field in metadata.json
      ✓ spec: Updated increment field in spec.md
      ✓ living-docs: Renamed FS-001E → FS-002E
      ✓ github: Updated issue #45 title: FS-001E → FS-002E
      ✓ jira: Updated PROJ-123 summary: FS-001E → FS-002E
      ✓ ado: Updated work item #789 title: FS-001E → FS-002E

📝 Report saved to: .specweave/increments/reports/RECONCILE-20260201-120000.md

💡 Next steps:
  1. Review the changes
  2. git add . && git commit -m "reconcile: fix ID collisions"
  3. Run /sw-github:sync or /sw-jira:sync to update external tools
```

### Example 2: Dry-Run Preview

```bash
/sw:reconcile --dry-run
```

**Output**:
```
[DRY RUN] Scanning for ID collisions...

Found 2 collisions:

Collision 1: Base ID 0001E
  [DRY RUN] Would keep: 0001E-auth-feature (2026-01-15)
  [DRY RUN] Would renumber: 0001E-payment-feature → 0002E-payment-feature

Collision 2: Base ID 0005
  [DRY RUN] Would keep: 0005-user-profile (2026-01-10)
  [DRY RUN] Would renumber: 0005-dashboard → 0006-dashboard

Summary:
  Would renumber: 2 increments
  Would update: 8 references

Run without --dry-run to apply changes.
```

### Example 3: Three-Way Collision

Three developers created 0001E increments:

```bash
/sw:reconcile
```

**Output**:
```
Collision: Base ID 0001E (3 increments)

Increments (ordered by modification date):
  1. 0001E-auth-feature      (2026-01-10) → KEEP as 0001E
  2. 0001E-payment-feature   (2026-01-15) → RENUMBER to 0002E
  3. 0001E-user-profile      (2026-01-20) → RENUMBER to 0003E

Proceed? [y/N]: y

✓ Kept 0001E-auth-feature as 0001E
✓ Renamed 0001E-payment-feature → 0002E-payment-feature
✓ Renamed 0001E-user-profile → 0003E-user-profile
```

### Example 4: Archive Collision

Collision between active and archived increment:

```bash
/sw:reconcile
```

**Output**:
```
Collision: Base ID 0042 (2 increments)

Increments:
  1. _archive/0042-old-feature    (2026-01-05, archived) → KEEP as 0042
  2. 0042-new-feature             (2026-01-25, active)   → RENUMBER to 0043

Note: Archived increment keeps original ID (earlier date)
```

## Reference Update Details

### metadata.json

```json
// BEFORE
{ "id": "0001E-payment-feature", ... }

// AFTER
{ "id": "0002E-payment-feature", ... }
```

### spec.md Frontmatter

```yaml
# BEFORE
---
increment: 0001E-payment-feature
title: "Payment Feature"
---

# AFTER
---
increment: 0002E-payment-feature
title: "Payment Feature"
---
```

### Living Docs

```
# BEFORE
.specweave/docs/internal/specs/backend/FS-001E/

# AFTER
.specweave/docs/internal/specs/backend/FS-002E/
```

### External Sync (GitHub)

If GitHub milestone exists:
- Old: Milestone "FS-001E: Payment Feature"
- New: Milestone "FS-002E: Payment Feature"

Note: GitHub issue numbers don't change (milestone renamed, not recreated)

## Error Handling

### No Collisions Found

```
Scanning for ID collisions...

✓ No collisions found!

All increment IDs are unique across all folders.
```

### Renumbering Fails

```
Error renumbering 0001E-payment-feature:
  Failed to rename directory
  Reason: Permission denied

Recommendation:
  1. Check folder permissions
  2. Close any programs using these files
  3. Retry
```

### External Sync Reference Update Fails

```
Warning: Could not update GitHub milestone
  Milestone "FS-001E" not found on remote

The increment was renumbered locally.
Run /sw-github:sync to recreate the milestone.
```

## Reconcile Report Format

**File**: `reports/RECONCILE-{timestamp}.md`

```markdown
# Increment ID Reconciliation Report

**Date**: 2026-02-01 12:00:00 UTC
**Command**: /sw:reconcile
**Trigger**: Post-merge ID collision resolution

## Collisions Detected

### Collision 1: Base ID 0001E

| Original Path | Modified Date | Action |
|---------------|---------------|--------|
| 0001E-auth-feature | 2026-01-15 | KEPT |
| 0001E-payment-feature | 2026-01-20 | RENUMBERED → 0002E |

## Renaming Operations

| Original ID | New ID | Folder Path |
|-------------|--------|-------------|
| 0001E-payment-feature | 0002E-payment-feature | .specweave/increments/ |

## Reference Updates

### 0002E-payment-feature (formerly 0001E)

- [x] metadata.json: id field updated
- [x] spec.md: frontmatter updated
- [x] Living docs: FS-001E → FS-002E renamed
- [ ] GitHub milestone: Not found (needs manual sync)
- [x] JIRA epic: Updated PROJ-123 custom field

## Summary

- Collisions resolved: 1
- Increments renumbered: 1
- Living docs renamed: 1
- External refs updated: 1
- Manual action needed: 1 (GitHub milestone)
```

## Implementation

The reconcile command should:

1. **Scan all increment folders** using `IncrementNumberManager.getAllIncrementNumbers()`

2. **Group by base number** (strip E suffix for comparison):
   ```typescript
   const groups = groupBy(increments, inc => inc.baseNumber);
   const collisions = groups.filter(g => g.length > 1);
   ```

3. **Order by modification date**:
   ```typescript
   collision.sort((a, b) =>
     new Date(a.modifiedDate).getTime() - new Date(b.modifiedDate).getTime()
   );
   ```

4. **Renumber later increments**:
   ```typescript
   for (let i = 1; i < collision.length; i++) {
     const newNumber = IncrementNumberManager.getNextIncrementNumber(root);
     await renameIncrement(collision[i], newNumber);
   }
   ```

5. **Update references**:
   ```typescript
   await updateMetadataId(increment, newId);
   await updateSpecFrontmatter(increment, newId);
   await renameLivingDocsFolder(oldFeatureId, newFeatureId);
   await updateExternalSyncRefs(increment, newId);
   ```

## Related Commands

- `/sw:fix-duplicates` - Remove actual duplicates (same increment in multiple locations)
- `/sw:status` - View all increments
- `/sw:sync-specs` - Sync living docs after reconciliation
- `/sw-github:sync` - Update GitHub references after reconciliation

## Best Practices

1. **Always run after multi-branch merge** - Make it a habit
2. **Use dry-run first** - Preview changes before applying
3. **Commit the reconciliation** - The renumbering should be a separate commit
4. **Sync external tools** - Run `/sw-github:sync` or `/sw-jira:sync` after reconcile

```bash
# Recommended post-merge workflow
git merge feature-branch
/sw:reconcile --dry-run    # Preview
/sw:reconcile              # Apply
git add . && git commit -m "reconcile: fix ID collisions after merge"
/sw-github:sync            # Update external tools
```

## Safety Notes

- **Non-destructive**: All increments are preserved, only renumbered
- **Reversible**: Git history preserves original state
- **Audit trail**: Reports document all changes
- **External sync safe**: Updates references, doesn't delete external issues
