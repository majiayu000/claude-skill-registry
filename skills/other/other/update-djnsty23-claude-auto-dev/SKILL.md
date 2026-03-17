---
name: update
description: Updates claude-auto-dev to latest version. Syncs repo with ~/.claude.
triggers:
  - update dev
  - update auto-dev
  - update skills
  - sync skills
allowed-tools: Bash, Read, Write, Glob
model: opus
user-invocable: true
---

# Update Claude Auto-Dev

Sync the local repo with ~/.claude installation.

## Process

Execute the following with the Bash tool immediately. Do NOT print it — run it. Use a SINGLE Bash call:

```bash
REPO=$(cat ~/.claude/repo-path.txt 2>/dev/null | tr -d '\r\n')
if [ -z "$REPO" ] || [ ! -d "$REPO" ]; then
  REPO=/tmp/claude-auto-dev
  rm -rf "$REPO"
  gh repo clone djnsty23/claude-auto-dev "$REPO"
fi
cd "$REPO" && git pull && bash "$REPO/scripts/update.sh" "$REPO"
```

After the Bash call completes, report the version and status from the output, then remind the user: "Start a new session (`/exit` then `claude`) for CLAUDE.md changes to take effect." Do NOT do anything else.

## What Gets Synced

| Source | Destination | Mode |
|--------|-------------|------|
| `repo/skills/` | `~/.claude/skills/` | Copy + clean stale (manifest-based) |
| `repo/hooks/` | `~/.claude/hooks/` | Copy (overwrite) |
| `repo/config/rules/` | `~/.claude/rules/` | Copy (add/update only, no delete) |
| `repo/agents/` | `~/.claude/agents/` | Copy (add/update only, preserves user agents) |
| `repo/config/settings.json` | `~/.claude/settings.json` | Overwrite (security-critical) |

Note: `commands.md` lives inside `skills/` — it syncs automatically with skills.

## What Does NOT Get Synced

- `~/.claude/CLAUDE.md` - User instructions, never touched (uses @include for commands.md)
