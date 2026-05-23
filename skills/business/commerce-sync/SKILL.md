---
name: commerce-sync
description: Manage sequencer sync, outbox, and conflict resolution. Use when running `stateset-sync` or checking sync status, push, or pull.
---

# Commerce Sync

Synchronize local events with the sequencer using VES.

## How It Works

1. Initialize sync config and keys.
2. Push local outbox events to the sequencer.
3. Pull remote events and apply changes.
4. Resolve conflicts and acknowledge synced events.

## Usage

- CLI: `stateset-sync status`, `stateset-sync push`, `stateset-sync pull`, `stateset-sync resolve`.
- Skill scripts: `bash /mnt/skills/user/commerce-sync/scripts/sync-status.sh`, `bash /mnt/skills/user/commerce-sync/scripts/sync-push.sh`, `bash /mnt/skills/user/commerce-sync/scripts/sync-pull.sh`.
- MCP tools: `sync_status`, `sync_push`, `sync_pull`, `sync_outbox`, `sync_conflicts`, `sync_resolve`.

## Output

```json
{"status":"synced","pending":0,"conflicts":0}
```

## Present Results to User

- Sync status, pending counts, and conflicts.
- Events pushed/pulled and any failures.
- Next steps for unresolved conflicts.

## Troubleshooting

- Sync config missing: run `stateset-sync init`.
- Signature errors: re-register keys with the sequencer.
- Conflicts: choose a resolution strategy before retrying.

## References
- references/sync-commands.md
- /home/dom/stateset-icommerce/cli/.claude/agents/sync.md
- /home/dom/stateset-icommerce/examples/getting-started-sync.md
- /home/dom/stateset-icommerce/cli/SYNC_CLI_SPEC.md
