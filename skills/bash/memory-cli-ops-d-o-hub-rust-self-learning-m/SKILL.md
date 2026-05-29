---
name: memory-cli-ops
description: Execute and troubleshoot memory-cli commands for episode management, pattern analysis, and storage operations. Use this skill when running CLI commands, debugging CLI issues, explaining command usage, or guiding users through CLI workflows.
---

# Memory CLI Operations

Execute and troubleshoot the memory-cli for the self-learning memory system.

## Quick Reference

- **[Commands](commands.md)** - Full command reference
- **[Troubleshooting](troubleshooting.md)** - Debugging guide
- **[Examples](examples.md)** - Common workflows

## When to Use

- Running CLI commands for episode/pattern management
- Debugging CLI command failures
- Understanding command syntax and options
- Guiding users through CLI workflows

## CLI Overview

**Location**: `./target/release/memory-cli`
**Output Formats**: human (default), json, yaml

## Global Options

```bash
memory-cli [OPTIONS] <COMMAND>

Options:
  -c, --config <FILE>    Configuration file path
  -f, --format <FORMAT>  Output format (human|json|yaml)
  -v, --verbose          Enable verbose output
  --dry-run              Show what would be done
```

## Commands Overview

| Command | Alias | Purpose |
|---------|-------|---------|
| episode | ep | Episode management |
| pattern | pat | Pattern analysis |
| storage | st | Storage operations |
| config | cfg | Configuration |
| health | hp | Health monitoring |
| backup | bak | Backup/restore |
| monitor | mon | Metrics |

See **[commands.md](commands.md)** for detailed command documentation and **[examples.md](examples.md)** for common workflows.
