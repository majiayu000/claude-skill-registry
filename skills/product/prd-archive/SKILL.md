---
name: prd-archive
description: Archive completed or cancelled PRDs
argument-hint: <prd-file> [--reason <reason>]
---

# prd-archive

**Category**: Product & Strategy

## Usage

```bash
prd-archive <prd-file> [--reason <reason>] [--force]
```

## Arguments

- `<prd-file>`: Required - Path to the PRD file to archive
- `--reason`: Optional - Reason for archiving (default: "Implementation complete" or "Project cancelled")
- `--force`: Optional - Archive even if status is not COMPLETE or ARCHIVED

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

1. Read the PRD file and validate it exists
2. Check current status:
   - If COMPLETE: proceed with archiving
   - If ARCHIVED: warn that it's already archived
   - If other status and no --force: ask for confirmation
3. If PRD has a linked task file, calculate final completion percentage
4. Add archive metadata to the PRD:
   - archive_date
   - archive_reason
   - final_task_completion (if applicable)
   - implementation_duration (if dates available)
5. Determine archive location:
   - Extract year from last_updated or use current year
   - Create path: `product-docs/prds/archive/YYYY/`
   - For cancelled PRDs: `product-docs/prds/archive/YYYY/cancelled/`
6. Move the PRD file to archive location (use git mv if in git repo)
7. Update status to ARCHIVED
8. Optionally archive the linked task file to the same location
9. Create an archive summary file if this is the first archive of the month

## Archive Metadata

Add to PRD header before moving:
```yaml
status: ARCHIVED
archive_date: 2025-01-06
archive_reason: Implementation complete - v1.0 released
final_task_completion: 100%
implementation_duration: 15 days
original_location: product-docs/prds/active/feature-prds/
```

## Archive Directory Structure

```
product-docs/prds/archive/
├── 2025/
│   ├── Q1/
│   │   ├── completed/
│   │   │   ├── user-auth-frd.md
│   │   │   └── user-auth-frd-tasks.md
│   │   ├── cancelled/
│   │   │   └── experimental-feature-frd.md
│   │   └── 2025-Q1-archive-summary.md
│   └── Q2/
└── 2024/
```

## Output Format

```
📦 Archiving PRD: user-authentication-frd.md

Current Status: COMPLETE
Task Completion: 100% (20/20 tasks)

✅ Adding archive metadata:
   - archive_date: 2025-01-06
   - archive_reason: Implementation complete - v1.0 released
   - final_task_completion: 100%
   - implementation_duration: 15 days

📁 Moving to archive:
   From: product-docs/prds/active/feature-prds/user-authentication-frd.md
   To: product-docs/prds/archive/2025/Q1/completed/user-authentication-frd.md

📄 Also archiving linked task file:
   To: product-docs/prds/archive/2025/Q1/completed/user-authentication-frd-tasks.md

✅ Archive complete!

📊 Archive Summary:
   - Implementation started: 2024-12-22
   - Implementation completed: 2025-01-06
   - Total duration: 15 days
   - Final status: Successfully delivered
```

## Archive Summary File

Create quarterly summary when archiving (e.g., `2025-Q1-archive-summary.md`):
```markdown
# Q1 2025 Archive Summary

## Completed PRDs (3)

1. **user-authentication-frd.md**
   - Archived: 2025-01-06
   - Duration: 15 days
   - Completion: 100%

2. **search-enhancement-frd.md**
   - Archived: 2025-02-15
   - Duration: 22 days
   - Completion: 100%

## Cancelled PRDs (1)

1. **experimental-ai-frd.md**
   - Archived: 2025-01-20
   - Reason: Project scope changed
   - Completion at cancellation: 35%

## Statistics
- Total PRDs archived: 4
- Success rate: 75% (3/4)
- Average implementation time: 18.5 days
```

## Error Handling

- If file doesn't exist: Exit with error
- If already archived: Show current location and exit
- If no write permission: Suggest using appropriate permissions
- If task file missing: Continue with PRD only, note in output
- If archive directory missing: Create it automatically

## Example

```bash
# Archive a completed PRD
prd-archive user-authentication-frd.md

# Archive with custom reason
prd-archive old-feature-frd.md --reason "Superseded by new design"

# Force archive of active PRD
prd-archive experimental-frd.md --force --reason "Project cancelled"

# Archive from different location
prd-archive ./drafts/completed-feature-frd.md
```

## Implementation Tips for Claude Code

1. **Git Integration**: Always use git mv when in a git repository
2. **Task File Handling**: Look for task file in same directory and ./tasks/
3. **Quarter Calculation**: Use Q1-Q4 based on month for organization
4. **Backup Safety**: Consider creating backup before archiving
5. **Summary Updates**: Append to existing quarterly summary if it exists
6. **Path Preservation**: Store original location in metadata for reference
