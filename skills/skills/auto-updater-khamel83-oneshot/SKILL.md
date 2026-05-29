---
name: auto-updater
description: "Automatically update ONE_SHOT skills from GitHub on session start. Checks once per day and updates silently. Use /update to force update."
allowed-tools: Bash, Read
---

# Auto-Updater

Keep ONE_SHOT skills up-to-date by automatically pulling from GitHub.

## Behavior

**Fully Automatic:**
- On every session start, checks if >24 hours since last check
- If update available, pulls it AUTOMATICALLY (no prompting)
- Notifies you after update: "ONE_SHOT has been auto-updated"
- Then doesn't check again for 24 hours

**Manual Override:**
- `/update` or `oneshot-update.sh force` - Force update now
- `/update status` - Show current version info

## How It Works

1. **Session Start Hook** (via session-context.sh):
   - Runs `oneshot-update.sh auto`
   - If rate limit not hit AND update available → auto-update
   - Stashes local changes, pulls, restores
   - All happens silently in background

2. **Manual Update** (when user says "update oneshot"):
   - Pulls latest from GitHub to ~/github/oneshot
   - Syncs skills/agents to the **current working project**
   - Detects current project from $PWD or ONESHOT_PROJECT_DIR env var

3. **Rate Limiting**:
   - Checks cached to once per 24 hours
   - Cache file: `~/github/oneshot/.cache/last-update-check`
   - Won't slow down every session, just first of the day

## Commands

```bash
# Auto-check and update (used by session start hook)
~/.claude/skills/oneshot/auto-updater/oneshot-update.sh auto

# Check for updates (rate-limited)
~/.claude/skills/oneshot/auto-updater/oneshot-update.sh check

# Force update from GitHub AND sync to current project
~/.claude/skills/oneshot/auto-updater/oneshot-update.sh force

# Show status
~/.claude/skills/oneshot/auto-updater/oneshot-update.sh status

# Sync skills/agents to a specific project (after manual git pull)
~/.claude/skills/oneshot/auto-updater/oneshot-update.sh sync [project-dir]
```

## Session Start Integration

Add to hooks-manager or session-context.sh:

```bash
# Check for ONE_SHOT updates
UPDATE_SCRIPT="$HOME/.claude/skills/oneshot/auto-updater/oneshot-update.sh"
if [ -x "$UPDATE_SCRIPT" ]; then
    UPDATE_STATUS=$("$UPDATE_SCRIPT" check 2>/dev/null)
    if echo "$UPDATE_STATUS" | grep -q "UPDATE_AVAILABLE"; then
        CONTEXT="$CONTEXT\n\n## ONE_SHOT Update Available\nNew version available. Run /update or say 'update oneshot' to get latest skills."
    fi
fi
```

## Workflow

### Automatic Check (Session Start)

```
Session starts
  → oneshot-update.sh check
  → If UPDATE_AVAILABLE:
       "ONE_SHOT update available. Run /update to get latest skills."
  → If UP_TO_DATE or RATE_LIMITED:
       (silent, no message)
```

### Manual Update

```
User: "update oneshot"

1. Force check for updates
2. Pull latest from GitHub to ~/github/oneshot
3. Sync skills/agents to current project (detected from $PWD)
4. Report results

Alternative: Just sync after manual git pull
User: "sync oneshot"
→ Runs oneshot-update.sh sync
→ Syncs skills/agents from ~/github/oneshot to current project
```

## Rate Limiting

- Checks cached to once per 24 hours
- Cache file: `~/github/oneshot/.cache/last-update-check`
- Force check bypasses cache
- Prevents API rate limits and unnecessary network calls

## Error Handling

| Scenario | Behavior |
|----------|----------|
| No internet | Skip silently |
| GitHub API rate limited | Skip silently, retry next session |
| Local changes conflict | Stash, update, pop stash |
| Merge conflict | Abort update, report to user |

## Configuration

Environment variables:

```bash
ONESHOT_DIR="$HOME/github/oneshot"      # Source repo location
SKILLS_SYMLINK="$HOME/.claude/skills/oneshot"  # Skills symlink
```

## What Gets Updated

When you run `update oneshot`:

1. **~/github/oneshot** - Pulls latest from GitHub
2. **Current project** - Syncs `.claude/skills/` and `.claude/agents/` from oneshot
   - Detects project by walking up from $PWD looking for `.claude/` folder
   - Or set `ONESHOT_PROJECT_DIR` env var to override

Synced content:
- All skills in `.claude/skills/`
- Agent definitions in `.claude/agents/`
- AGENTS.md (orchestration spec)
- Hooks and scripts

## What Stays Local

- Your project files
- CLAUDE.md (project-specific)
- Secrets in `secrets/` (encrypted)
- Local `.cache/` files

## Keywords

update, upgrade, oneshot, latest, version, sync, pull, github, auto-update
