---
name: cc-soul-setup
description: Build cc-soul from source (requires cmake, make, C++ compiler)
execution: inline
---

# cc-soul-setup

Build chitta binaries from source code.

## Requirements
- cmake
- make
- C++ compiler (g++ or clang++)

## Usage

```bash
# Run smart-install from plugin directory (builds from source as fallback)
${CLAUDE_PLUGIN_ROOT}/scripts/smart-install.sh
```

This will:
1. Stop any running daemon
2. Download pre-built binaries (or build from source if unavailable)
3. Install to ~/.claude/bin/
4. Download embedding model if needed
5. Install hooks and configure permissions
6. Set up systemd user service (Linux only) and start the daemon
7. Run database migrations if needed

If cmake is not available and pre-built binaries aren't found, suggest using `/cc-soul-update` to download pre-built binaries instead.

After setup, the daemon is managed by systemd (`systemctl --user status chittad`). It starts automatically and restarts on crash.
