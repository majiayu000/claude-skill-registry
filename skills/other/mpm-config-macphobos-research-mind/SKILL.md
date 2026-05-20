---
name: mpm-config
description: Manage Claude MPM configuration
user-invocable: true
version: "1.0.0"
category: mpm-command
tags: [mpm-command, config, pm-recommended]
---

# /mpm-config

Unified configuration management with auto-detection.

## Usage
```
/mpm-config [auto|view|validate|status] [options]
```

**Modes:**
- `auto` (default): Auto-detect toolchain and configure agents/skills
- `view`: Display current configuration
- `validate`: Check configuration validity
- `status`: Show configuration health

**Key Options:**
- `--yes`: Auto-deploy without confirmation
- `--preview`: Show recommendations only

See docs/commands/config.md for full options.
