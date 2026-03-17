---
name: sabx
version: 1.0.0
description: Control SABnzbd download manager via CLI. Use when users need to check download queue/history, add NZBs, manage priorities, control speed limits, pause/resume downloads, configure RSS feeds, run scheduled tasks, or automate Usenet workflows. Triggers include "sabnzbd", "sabx", "downloads", "nzb", "usenet", "download queue", "download status".
metadata:
  short-description: SABnzbd CLI for download automation
  compatibility: claude-code, codex-cli
---

# SABnzbd CLI (sabx)

Control SABnzbd from the terminal. Covers common SABnzbd API operations.

## Prerequisites

```bash
# Install (Go 1.24+)
go install github.com/avivsinai/sabx/cmd/sabx@latest

# Authenticate (stores API key in OS keyring)
sabx login --base-url http://localhost:8080 --api-key <key>
```

## Quick Command Reference

| Task | Command |
|------|---------|
| Queue status | `sabx queue list` |
| Active downloads | `sabx queue list --active` |
| Add NZB from URL | `sabx queue add url <url>` |
| Add NZB file | `sabx queue add file <path>` |
| Pause queue | `sabx queue pause` |
| Resume queue | `sabx queue resume` |
| Set priority | `sabx queue item priority <nzo_id> 2` |
| Delete item | `sabx queue item delete <nzo_id>` |
| History | `sabx history list` |
| Retry failed | `sabx history retry <nzo_id>` |
| Delete all history | `sabx history delete --all` |
| System status | `sabx status` |
| Full diagnostics | `sabx status --full --performance` |
| Speed status | `sabx speed status` |
| Set speed limit | `sabx speed limit --rate 5M` |
| Remove speed limit | `sabx speed limit --none` |
| Live dashboard | `sabx top` |

## Priority Values

Priority is -1 to 2: `-1`=low, `0`=normal, `1`=high, `2`=force

## Common Patterns

### Check and manage downloads
```bash
sabx queue list --active          # What's downloading now
sabx status --full                # Overall system health
sabx speed status                 # Current speed and limits
sabx warnings list                # Any runtime issues
```

### Add downloads
```bash
sabx queue add url https://example.com/file.nzb
sabx queue add file ./local.nzb --cat movies
sabx queue add local /path/on/server/file.nzb
```

### Priority and queue management
```bash
sabx queue item priority <nzo_id> 2    # Force (2=force priority)
sabx queue item move <nzo_id> top      # Move to top
sabx queue item move <nzo_id> to 0     # Move to position 0
sabx queue sort name                   # Sort by name
sabx history delete --all              # Clear entire history
sabx history delete --failed           # Clear failed items only
```

### Pause/resume workflows
```bash
sabx queue pause                  # Pause all downloads
sabx queue resume                 # Resume downloads
sabx postprocess pause            # Pause post-processing
sabx postprocess resume           # Resume post-processing
```

### RSS feed automation
```bash
sabx rss list                           # List configured feeds
sabx rss add TVFeed --url <rss-url> --cat tv
sabx rss run TVFeed                     # Manually trigger specific feed
sabx rss run                            # Run all feeds
sabx rss delete TVFeed
```

### Scheduler tasks
```bash
sabx schedule list
sabx schedule add NightPause --set command=pause --set day=mon-sun --set hour=01 --set min=00
sabx schedule set NightPause --set hour=02
sabx schedule delete NightPause
```

### Server management
```bash
sabx server list                  # News servers
sabx server stats                 # Per-server statistics
sabx server test primary          # Test connectivity
sabx server disconnect            # Disconnect from all servers
```

### Troubleshooting
```bash
sabx doctor                       # Health checks
sabx warnings list                # Runtime warnings
sabx logs list --lines 50         # Recent logs
sabx logs tail --follow           # Stream logs
sabx debug gc-stats               # GC diagnostics
```

## Output Modes

All commands support `--json` for scripting:
```bash
sabx queue list --json | jq '.slots[0].filename'
sabx speed status --json
```

## Configuration

```bash
# Multiple profiles
sabx login --profile home --base-url http://home:8080 --api-key <key>
sabx login --profile server --base-url http://server:8080 --api-key <key>

# Switch profiles
sabx --profile server queue list

# Environment overrides
SABX_BASE_URL=http://alt:8080 SABX_API_KEY=xxx sabx status
```

## References

- **Full command reference**: See [references/commands.md](references/commands.md)
