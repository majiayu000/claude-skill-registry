---
name: feature-creator
description: Guide for creating DevContainer features. Use when creating a new feature for devcontainer, implementing install.sh scripts (npm package, binary download, source build, dotnet tool, or directory setup patterns), or configuring devcontainer-feature.json metadata. Triggers on phrases like "create a feature", "add devcontainer feature", "install.sh template", or "devcontainer-feature.json".
---

# DevContainer Feature Creator

Create DevContainer features efficiently using proven patterns from this repository.

## Feature Structure

Every feature consists of exactly two files:

```
features/<feature-name>/
├── devcontainer-feature.json  # Metadata definition
└── install.sh                 # Installation script
```

## devcontainer-feature.json Schema

### Required Fields

```json
{
  "id": "<feature-name>", // kebab-case, matches folder name
  "version": "1.0.0", // semver format
  "name": "Human Readable Name",
  "description": "Brief description of what this feature installs"
}
```

### Optional Fields

```json
{
  "options": {
    "version": {
      "type": "string",
      "default": "latest",
      "description": "Version to install"
    }
  },
  "installsAfter": [
    "ghcr.io/devcontainers/features/node" // Dependencies
  ],
  "postStartCommand": "command to run after container starts"
}
```

## install.sh Patterns

Five proven patterns exist. See `references/install-patterns.md` for complete templates.

| Pattern | Use Case                       | Example                            |
| ------- | ------------------------------ | ---------------------------------- |
| npm     | Node.js packages               | claude-code, editorconfig-prettier |
| binary  | Pre-built binaries from GitHub | lazygit, copilot-cli, yazi         |
| source  | Build from source              | luarocks                           |
| dotnet  | .NET global tools              | easydotnet                         |
| setup   | Directory/config setup         | vimcontainer-setup                 |

## Creation Workflow

### Step 1: Initialize Feature

Run the initialization script:

```bash
python3 scripts/init_feature.py <feature-name> <pattern>
```

Patterns: `npm`, `binary`, `source`, `dotnet`, `setup`

### Step 2: Edit devcontainer-feature.json

1. Update `name` and `description`
2. Add `options` if configurable (e.g., version)
3. Add `installsAfter` if dependencies exist

### Step 3: Edit install.sh

1. Replace placeholder values
2. Add error handling
3. Test installation

### Step 4: Test Feature

```bash
# Build and test locally
devcontainer features test -f <feature-name> .
```

## Best Practices

### install.sh Guidelines

1. **Always start with**: `#!/bin/bash` and `set -e`
2. **Version handling**: `VERSION="${VERSION:-default}"`
3. **Architecture detection** (for binaries):
   ```bash
   ARCH=$(dpkg --print-architecture)
   case "$ARCH" in
       amd64) TARGET_ARCH="x86_64" ;;
       arm64) TARGET_ARCH="arm64" ;;
       *) echo "Unsupported: $ARCH"; exit 1 ;;
   esac
   ```
4. **Dependency checks**: Verify required tools before use
5. **Cleanup**: Remove temp files and apt cache
6. **Verification**: Confirm installation succeeded

### Error Handling

- Check command availability before use
- Provide clear error messages
- Exit with non-zero code on failure
- Validate downloaded files (check gzip magic bytes)

### User Context

For user-specific installations:

```bash
INSTALL_USER="${_REMOTE_USER:-${USERNAME:-vscode}}"
USER_HOME=$(getent passwd "${INSTALL_USER}" | cut -d: -f6)
```

## Resources

- **Initialization script**: `scripts/init_feature.py` - Generate feature scaffolding
- **Pattern templates**: `references/install-patterns.md` - Detailed templates for each pattern
