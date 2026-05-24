---
name: aim-github-sync
description: 'Synchronize GitHub issues, PRs, commits, and CI results to AI Memory'
allowed-tools: Bash
---

# GitHub Sync - Synchronize GitHub Content

Synchronize GitHub issues, pull requests, commits, and CI results from the configured repository into the AI Memory discussions collection.

## Usage

```bash
# Incremental sync (default) - only fetch updated items
/aim-github-sync

# Full sync - fetch all items from scratch
/aim-github-sync --full

# Check sync status (last sync time, items synced, errors)
/aim-github-sync --status
```

## Options

- `--incremental` - Sync only updated items since last sync (default)
- `--full` - Full sync: fetch all items from scratch
- `--status` - Display sync status (last sync time, items synced per type)

## Sync Modes

### Incremental Sync (Default)

- Fetches items updated since last sync timestamp per document type
- Faster and more efficient for regular updates
- Priority order: PRs -> Issues -> Commits -> CI Results
- Updates existing documents via dedup/versioning protocol (SPEC-005)

### Full Sync

- Fetches all items from scratch
- Use for initial setup or after schema changes
- Warning: Can be slow for large repositories

## Configuration

Sync requires GitHub credentials in `.env`:

```env
GITHUB_TOKEN=ghp_your_token_here
GITHUB_REPO=owner/repo-name
GITHUB_BRANCH=main
GITHUB_SYNC_ENABLED=true
```

## Implementation Reference

This skill invokes `GitHubSyncEngine.sync()` from `src/memory/connectors/github/sync.py`:

```bash
# The skill invokes the sync engine via a thin script
cd "$AI_MEMORY_INSTALL_DIR" || { echo "Error: AI_MEMORY_INSTALL_DIR is not set or directory does not exist"; exit 1; }
MODE="${MODE:-incremental}"
for arg in "$@"; do
  case "$arg" in
    --full) MODE="full" ;;
    --incremental) MODE="incremental" ;;
  esac
done
"$AI_MEMORY_INSTALL_DIR/.venv/bin/python" -c "
import asyncio
from memory.connectors.github.sync import GitHubSyncEngine
engine = GitHubSyncEngine()
result = asyncio.run(engine.sync(mode='${MODE}'))
print(f'Synced {result.total_synced} items ({result.items_skipped} skipped, {result.errors} errors) in {result.duration_seconds:.1f}s')
d = result.to_dict()
for k, v in d.items():
    if v and k != 'total_synced':
        print(f'  {k}: {v}')
"
```

### Status Mode

Reads `.audit/state/github_sync_state.json` and displays last sync timestamps per type:

```bash
cd "$AI_MEMORY_INSTALL_DIR" || { echo "Error: AI_MEMORY_INSTALL_DIR is not set or directory does not exist"; exit 1; }
python3 -c "
import json
from pathlib import Path
state_file = Path('.audit/state/github_sync_state.json')
if not state_file.exists():
    print('No sync state found. Run /aim-github-sync first.')
else:
    state = json.loads(state_file.read_text())
    print('## GitHub Sync Status')
    print('')
    for type_key, info in state.items():
        last = info.get('last_synced', 'never')
        count = info.get('last_count', 0)
        print(f'  {type_key}: last synced {last} ({count} items)')
"
```

## Guard

If `GITHUB_SYNC_ENABLED` is not `true`, the skill will display:

```
Error: GitHub sync is not enabled. Set GITHUB_SYNC_ENABLED=true and configure GITHUB_TOKEN and GITHUB_REPO.
```

## Technical Details

- **Rate Limiting**: Uses GitHubClient with configurable request delays
- **Pagination**: Automatic pagination for all GitHub API endpoints
- **Deduplication**: SHA256 content hashing prevents duplicate storage (SPEC-005)
- **Versioning**: Changed content creates new version, marks old as superseded
- **Collection**: discussions (shared with conversation data, filtered by source="github")
- **Tenant Isolation**: group_id = owner/repo
- **Sync Priority**: PRs (+ reviews + diffs) -> Issues (+ comments) -> Commits -> CI Results

## Notes

- Requires GitHub personal access token (classic or fine-grained)
- Sync logs written to `~/.ai-memory/logs/activity.log`
- First full sync can take several minutes for large repositories
- Incremental sync timestamps stored per type in `github_sync_state.json`
- Reviews and diffs are synced as part of PR sync
- Issue comments are synced as part of issue sync
