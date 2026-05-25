---
name: lifecycle-hooks
description: >-
  Behavioral rules and lifecycle event handlers for the dev-tools package.
  Defines automated behaviors that trigger at specific points in the agent workflow.
  (converted from hooks)
dependencies: []
---

# Lifecycle Hooks

This skill documents the lifecycle event handlers for the dev-tools package. These hooks define automated behaviors that trigger at specific points in the agent workflow.

## Session Start Hook

**Event:** `session_start`
**Purpose:** Cross-plugin dependency resolution for cache environments

### Behavior

When a session starts, this hook runs a script that resolves cross-package references by creating symlinks in the plugin cache directory. The script:

1. Detects whether execution is happening in a plugin cache environment (vs. local monorepo development)
2. If in cache, iterates over sibling plugin directories under the same organization
3. Strips the organization prefix to derive short names (e.g., `agent-alchemy-claude-tools` becomes `claude-tools`)
4. Creates symlinks so that relative path references between packages work correctly
5. Uses the installed plugins registry or filesystem sorting to resolve the correct version

### When This Is Needed

In the original plugin system, cross-plugin references use filesystem paths like `/../{short-name}/`. In local development (monorepo), these paths resolve naturally because sibling directories have short names. In cache environments, the extra version subdirectory and organization-prefixed names break this convention.

### Ported Context

In the ported format, this behavior may not be needed since ported files use named references (e.g., "Refer to the **deep-analysis** skill from the core-tools package") instead of filesystem paths. The script is preserved in `references/resolve-cross-plugins.sh` for environments that still need filesystem-based cross-package resolution.

### Script Reference

See **references/resolve-cross-plugins.sh** for the full implementation.

### Configuration

- **Timeout:** 10 seconds (the script should never block session start)
- **Error handling:** The script traps all errors and exits cleanly (exit 0) to never block session startup
- **Debug logging:** Set `AGENT_ALCHEMY_HOOK_DEBUG=1` to enable diagnostic logging to `$AGENT_ALCHEMY_HOOK_LOG` (default: `/tmp/agent-alchemy-hooks.log`)

## Integration Notes

**What this component does:** Defines lifecycle event handlers that run at specific workflow points, primarily handling cross-plugin dependency resolution in cache environments.

**Capabilities needed:**
- Shell command execution (to run the symlink resolution script)
- Filesystem access (to create symlinks in the plugin cache)

**Adaptation guidance:**
- In ported environments where skills reference each other by name rather than filesystem path, this hook may be unnecessary
- If your platform uses a different plugin/package resolution mechanism, adapt the symlink logic in the reference script accordingly
- The script is designed to be non-blocking: it silently exits on any error to avoid disrupting session startup
