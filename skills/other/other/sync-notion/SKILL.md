---
context: fork
---

# /sync-notion

Sync meetings from Notion database to Obsidian.

## Usage

```
/sync-notion
/sync-notion --since 2025-01-01
/sync-notion --dry-run
```

## Instructions

### Prerequisites

- Notion token must be available (check environment or ask user)
- Script exists at `scripts/notion_sync.py`

### Phase 1: Planning

1. Check if sync script exists
2. Determine sync scope:
   - Default: all new/modified since last sync
   - `--since`: from specific date
   - `--dry-run`: preview only, no changes

### Phase 2: Execute Sync

1. Run the sync script:
   ```bash
   python3 scripts/notion_sync.py
   ```

2. If script doesn't exist or fails, offer to:
   - Check Notion token
   - Recreate the script
   - Manual sync instructions

### Phase 3: Post-Sync Processing (use sub-agents)

Launch sub-agents using `model: "haiku"` for efficiency:

**Agent 1: Identify New Files** (Haiku)
- Compare before/after file list
- Identify newly created meeting files
- Return: list of new files

**Agent 2: Standardize Names** (Haiku)
- Run standardization on new files in `+Meetings/`
- Ensure `Meeting - YYYY-MM-DD Title.md` format
- Move files to `+Meetings/` folder if not already there
- Return: renamed files

**Agent 3: Fix Project Links** (Haiku)
- Check new files for project references
- Ensure links use actual project names
- Return: fixed links

**Agent 4: Update MOC** (Haiku)
- Add new meetings to MOC - Meetings MOC if needed
- Return: MOC updates

### Phase 4: Report

```markdown
# Notion Sync Report

**Synced**: {{DATE}}
**Database**: Work - Meeting Minutes & Notes

## Summary

- New meetings imported: {{count}}
- Updated meetings: {{count}}
- Skipped (no changes): {{count}}
- Errors: {{count}}

## New Meetings

| Date | Title | Project |
|------|-------|---------|
{{new meeting list}}

## Updated Meetings

{{list of updated meetings}}

## Project Links Fixed

| Meeting | Project |
|---------|---------|
{{project link fixes}}

## Errors

{{any errors encountered}}

## Next Steps

- Review new meetings for accuracy
- Add attendees where missing
- Link to relevant projects
```

### Dry Run Mode

If `--dry-run`:
- Query Notion for changes
- Show what WOULD be synced
- Don't write any files
