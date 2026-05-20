---
name: cc-soul-daemon
description: Start, stop, or check the chittad daemon
execution: inline
---

# cc-soul-daemon

Manage the chittad background daemon.

## Usage

If the systemd user service is installed (the default since smart-install.sh sets it up),
use systemctl directly — it's the primary management interface:

```bash
# Check status
systemctl --user status chittad

# Start daemon
systemctl --user start chittad

# Stop daemon
systemctl --user stop chittad

# Restart daemon
systemctl --user restart chittad

# View logs
journalctl --user -u chittad -n 50
```

If systemd is not available (macOS, old Linux), fall back to subconscious.sh:

```bash
# Check status (default)
${CLAUDE_PLUGIN_ROOT}/hooks/subconscious.sh status

# Start / stop / restart
${CLAUDE_PLUGIN_ROOT}/hooks/subconscious.sh start
${CLAUDE_PLUGIN_ROOT}/hooks/subconscious.sh stop
${CLAUDE_PLUGIN_ROOT}/hooks/subconscious.sh restart
```

Parse user request for action (start/stop/restart/status/logs), default to status.
Run the appropriate command and report the result.
