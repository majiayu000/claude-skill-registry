---
name: aim-jira-sync
description: 'Synchronize Jira issues and comments to AI Memory'
allowed-tools: Bash
---

# Jira Sync - Synchronize Jira Content

Synchronize Jira issues and comments from configured projects into the AI Memory jira-data collection.

## Usage

```bash
# Incremental sync (default) - only fetch updated issues
/aim-jira-sync

# Full sync - fetch all issues and comments
/aim-jira-sync --full

# Sync specific project
/aim-jira-sync --project BMAD

# Check sync status (last sync time, items synced, errors)
/aim-jira-sync --status

# Full sync for specific project
/aim-jira-sync --full --project BMAD
```

## Options

- `--incremental` - Sync only updated issues since last sync (default)
- `--full` - Full sync: fetch all issues and comments from scratch
- `--project <key>` - Sync specific project (default: all configured projects)
- `--status` - Display sync status (last sync time, items synced, errors)

## Sync Modes

### Incremental Sync (Default)

- Fetches issues updated since last sync timestamp
- Faster and more efficient for regular updates
- Uses JQL: `project = PROJ AND updated >= "2026-02-01 00:00"`
- Updates existing documents in-place (by jira_comment_id for comments)

### Full Sync

- Fetches all issues and comments from scratch
- Use for initial setup or after schema changes
- Warning: Can be slow for large projects (hundreds/thousands of issues)
- Overwrites existing documents

## Configuration

Sync requires Jira credentials in `.env`:

```env
JIRA_INSTANCE_URL=https://company.atlassian.net
JIRA_EMAIL=user@company.com
JIRA_API_TOKEN=your_api_token_here
JIRA_PROJECTS=BMAD,PROJ,DEV
JIRA_SYNC_ENABLED=true
JIRA_SYNC_DELAY_MS=100
```

## Examples

```bash
# Daily incremental sync (recommended)
/aim-jira-sync

# Initial full sync for new project
/aim-jira-sync --full --project NEWPROJ

# Check last sync status
/aim-jira-sync --status

# Full refresh of all projects (use sparingly)
/aim-jira-sync --full
```

## Implementation Reference

This skill invokes `scripts/jira_sync.py`:

```bash
cd /path/to/ai-memory
python3 scripts/jira_sync.py --incremental
python3 scripts/jira_sync.py --full --project BMAD
python3 scripts/jira_sync.py --status
```

## Technical Details

- **Rate Limiting**: Configurable delay between API requests (default 100ms)
- **Pagination**: Token-based for issues, offset-based for comments
- **Deduplication**: SHA256 content hashing prevents duplicate storage
- **Document Format**: ADF (Atlassian Document Format) → plain text
- **Collection**: jira-data (separate from code-patterns/conventions/discussions)
- **Tenant Isolation**: group_id = Jira instance hostname

## Notes

- Requires Jira Cloud API token (create at id.atlassian.com)
- Sync logs written to `~/.ai-memory/logs/activity.log`
- First sync can take several minutes for large projects
- Incremental sync timestamp stored in jira_sync_state.json
- Comments are linked to parent issues via jira_issue_key
