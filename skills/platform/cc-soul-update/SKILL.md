---
name: cc-soul-update
description: Update cc-soul binaries (downloads pre-built or builds from source)
execution: inline
---

# cc-soul-update

Update chitta binaries to the latest version.

## Usage

```bash
# Run smart-install script
${CLAUDE_PLUGIN_ROOT}/scripts/smart-install.sh
```

This will:
1. Check current vs installed version
2. Stop running daemon if version changed
3. Try to download pre-built binaries for your platform
4. Fall back to building from source if download fails
5. Download embedding model if needed
6. Configure bash permissions

Pre-built binaries available for:
- linux-x64
- linux-arm64
- macos-x64
- macos-arm64
