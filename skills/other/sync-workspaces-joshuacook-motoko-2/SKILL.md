---
name: sync-workspaces
description: Sync local and remote workspaces with latest motoko framework changes. Use when asked to update workspaces, sync skills, or push motoko changes to workspaces.
allowed-tools: Bash, Read, Write, Glob
---

# Sync Workspaces with Motoko

Sync Context Lake workspaces with the latest motoko framework (tachikoma skills, schema patterns, etc.).

## Workspace Locations

**Local workspaces** (manual git sync):
- `~/working/coyote`
- `~/working/escuela`
- `~/working/project-management`

**Remote workspaces** (VM with auto-commit cron):
- `/opt/workspaces/josh/coyote`
- `/opt/workspaces/josh/escuela`
- `/opt/workspaces/josh/project-management`

**Motoko source** (this repo):
- `~/working/claude-code-apps/motoko`

## What to Sync

### Tachikoma Skills
Copy from `motoko/.claude/skills/tachikoma-*/` to workspace `.claude/skills/`:
- `tachikoma-schema/SKILL.md`
- `tachikoma-frontmatter/SKILL.md`
- `tachikoma-structure/SKILL.md`

### MCP Config (if needed)
Ensure `.mcp.json` points to batou:
```json
{
  "mcpServers": {
    "batou": {
      "command": "uv",
      "args": ["--directory", "/path/to/motoko/batou", "run", "batou"],
      "env": {
        "WORKSPACE_PATH": "/path/to/workspace"
      }
    }
  }
}
```

## Process

1. **Identify target workspaces** - Ask which workspaces to sync (local, remote, or both)

2. **Sync local workspaces**:
   ```bash
   # For each local workspace
   cp -r ~/working/claude-code-apps/motoko/.claude/skills/tachikoma-* ~/working/{workspace}/.claude/skills/
   cd ~/working/{workspace} && git add -A && git commit -m "Sync tachikoma skills from motoko" && git push
   ```

3. **Sync remote workspaces** (via gcloud ssh):
   ```bash
   # First push motoko changes
   cd ~/working/claude-code-apps/motoko && git add -A && git commit -m "..." && git push

   # Then on VM, pull and copy
   gcloud compute ssh chelle --project=rs-chelle --account=root@joshuacook.net --zone=us-central1-a --command="
     cd /opt/claude-code-apps && git pull
     for ws in /opt/workspaces/josh/*; do
       cp -r /opt/claude-code-apps/motoko/.claude/skills/tachikoma-* \$ws/.claude/skills/ 2>/dev/null
       cd \$ws && git add -A && git commit -m 'Sync tachikoma skills from motoko' 2>/dev/null
     done
   "
   ```

4. **Pull remote changes to local** (if remote was updated first):
   ```bash
   cd ~/working/{workspace} && git pull --rebase
   ```

## Output

Report what was synced:
- Which workspaces were updated
- What files were copied
- Any conflicts or errors
