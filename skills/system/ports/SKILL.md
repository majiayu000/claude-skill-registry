---
name: ports
description: Check what's using shella ports (47100-47199). Use when debugging port conflicts or seeing what's running.
allowed-tools: Bash(lsof:*)
---

# Shella Port Check

Show what processes are using ports in the shella range.

## Port Ranges

- **47100**: Daemon API
- **47101-47199**: Plugin instances
- **47200**: Standalone plugin dev (`npm run dt dev plugin <name>`)

## Command

```bash
lsof -i :47100-47200 -P -n 2>/dev/null | grep LISTEN
```

## Output

Show a table of:
- Port number
- Process name
- PID
- What it likely is (daemon, plugin instance, standalone dev)

If nothing is listening, say so.

If there are unexpected processes (not node), flag them as potential conflicts.
