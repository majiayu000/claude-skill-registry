---
name: mpm-doctor
description: Run diagnostic checks on Claude MPM installation
user-invocable: true
version: "1.0.0"
category: mpm-command
tags: [mpm-command, system, pm-required, diagnostics, troubleshooting]
---

# /mpm-doctor

Run comprehensive diagnostics on Claude MPM installation.

## Usage

```
/mpm-doctor [--verbose] [--fix]
```

## Options

- `--verbose`: Show detailed diagnostic output
- `--fix`: Attempt to automatically fix detected issues

## What It Checks

- **Installation**: MPM package installation and version
- **Configuration**: Config file validity and required settings
- **WebSocket**: WebSocket server connectivity and health
- **Agents**: Agent availability and configuration
- **Memory**: Memory system health and accessibility
- **Hooks**: Hook system setup and functionality

## When to Use

- After initial MPM installation (verify setup)
- When experiencing issues with commands or delegation
- Before reporting bugs (gather diagnostic information)
- After configuration changes (verify correctness)
- When WebSocket monitoring isn't working

## Example Output

```
✅ MPM Installation: OK (v5.4.105)
✅ Configuration: Valid
⚠️  WebSocket Server: Not running (start with /mpm-monitor start)
✅ Agents: 15 available
✅ Memory System: Healthy
✅ Hooks: Configured
```

See docs/commands/doctor.md for details.
