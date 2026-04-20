---
name: lifecycle-hooks
description: Session-start lifecycle hooks for cross-plugin dependency resolution. Creates symlinks so cross-package references work in cached plugin environments.
dependencies: []
---

# Lifecycle Hooks

This skill documents the session-start lifecycle hooks used by the dev-tools package. These hooks run automatically at session initialization to ensure cross-plugin references resolve correctly in cached environments.

## Cross-Plugin Dependency Resolution

### Problem

When plugins are installed from a marketplace/registry, each plugin is cached in an isolated directory with organization-prefixed names and version subdirectories. Cross-plugin references (e.g., loading a skill from a sibling plugin via relative paths) break because the directory structure differs from the local development monorepo layout.

**Local monorepo layout:**
```
claude/
├── core-tools/       <- ../core-tools/ resolves naturally
├── dev-tools/
└── claude-tools/
```

**Cached plugin layout:**
```
plugins/cache/org-name/
├── org-name-core-tools/
│   └── 0.2.3/       <- long path, org-prefixed name
├── org-name-dev-tools/
│   └── 0.3.4/
└── org-name-claude-tools/
    └── 0.2.5/
```

### Solution

The `resolve-cross-plugins.sh` script (in `references/`) runs at session start and creates short-name symlinks at the plugin-name directory level so that `../{short-name}/` resolves correctly in both environments.

**After script runs:**
```
plugins/cache/org-name/org-name-dev-tools/
├── 0.3.4/                    <- actual plugin content
├── core-tools -> ../org-name-core-tools/0.2.3   <- symlink
└── claude-tools -> ../org-name-claude-tools/0.2.5  <- symlink
```

### Hook Configuration

The hook runs as a `session_start` event of type `command`:

```yaml
event: session_start
type: command
command: bash <plugin_root>/hooks/resolve-cross-plugins.sh <plugin_root>
timeout: 10
```

### Script Behavior

The `resolve-cross-plugins.sh` script:

1. **Guard**: Only runs in cached plugin environments (path contains `/plugins/cache/`). In local monorepo development, the script exits immediately since relative paths already work.

2. **Discovery**: Iterates over sibling directories in the organization directory, stripping the org prefix to derive the short name (e.g., `org-name-core-tools` -> `core-tools`).

3. **Version Resolution**: Determines the correct version directory using:
   - Primary: reads `installed_plugins.json` from the agent configuration directory (requires `jq`)
   - Fallback: sorts version directories by version number and takes the latest

4. **Symlink Creation**: Creates relative symlinks (`ln -sfn`) from the short name to the resolved version directory. Skips if a real (non-symlink) directory already exists with that name.

5. **Safety**: Never blocks session start -- the script traps all errors and exits cleanly with code 0. Debug logging is available via the `AGENT_ALCHEMY_HOOK_DEBUG=1` environment variable.

### Adaptation for Other Platforms

If your platform uses a different plugin caching mechanism:

1. **Identify the cached layout** -- how are sibling plugins organized on disk?
2. **Determine the naming convention** -- are names prefixed with organization/scope?
3. **Create equivalent symlinks** -- ensure `../{short-name}/` resolves to the correct version of each sibling plugin
4. **Handle version resolution** -- use your platform's installed-plugins metadata if available
5. **Ensure safety** -- never block session initialization on symlink creation failures

---

## Integration Notes
**What this component does:** Provides a session-start hook that creates short-name symlinks for cross-plugin dependency resolution in cached/installed plugin environments, ensuring that relative path references between plugin packages work correctly.
**Capabilities needed:** Shell execution (bash script with `ln`, `jq`), file system access (symlink creation in plugin cache directory).
**Adaptation guidance:** This hook addresses a specific problem with cached plugin directory layouts. If your platform resolves cross-package references differently (e.g., through a module system, import maps, or path aliases), you may not need this hook. The script in `references/resolve-cross-plugins.sh` can serve as a reference implementation. The key requirement is that `../{package-short-name}/` relative paths must resolve from any sibling plugin's root directory.
