---
name: lifecycle-hooks
description: Behavioral rules and lifecycle event handlers for the core-tools package. Includes auto-approval of file operations targeting deep-analysis session directories.
dependencies: []
---

# Lifecycle Hooks

This skill defines behavioral rules and lifecycle event handlers converted from the core-tools hook configuration. These rules describe when certain operations should be automatically approved or handled without user intervention.

---

## Auto-Approve Deep Analysis Session Operations

**Trigger:** Before any file write, file edit, or shell command execution.

**Matcher:** Operations targeting Write, Edit, or shell commands.

**Behavior:** Automatically approve file operations that target deep-analysis session and cache directories. All other operations pass through to the normal permission flow.

### Approved Paths

The following directory patterns are auto-approved for file operations:

| Pattern | Description |
|---------|-------------|
| `.agents/sessions/__da_live__/*` | Active deep-analysis session files |
| `.agents/sessions/exploration-cache/*` | Exploration cache (cached analysis results) |
| `.agents/sessions/da-*/*` | Archived deep-analysis sessions |

### Logic

1. For **file write/edit** operations: Extract the target file path. If it matches any of the approved path patterns above, approve the operation automatically.
2. For **shell commands**: Check if the command string contains any of the approved directory paths. If so, approve automatically.
3. For **all other operations**: No opinion — let the normal permission flow handle it.

### Implementation Reference

See **references/auto-approve-da-session.sh** for the reference shell implementation of this auto-approval logic. The script:
- Reads tool input as JSON from stdin
- Extracts the tool name and relevant parameters (file path or command)
- Matches against the approved path patterns
- Returns an approval decision or exits silently (no opinion)
- Never exits with a non-zero status code (a non-zero exit would break the permission flow)

### Debug Logging

The reference implementation supports optional debug logging:
- Set environment variable `AGENT_ALCHEMY_HOOK_DEBUG=1` to enable
- Logs are written to the path in `AGENT_ALCHEMY_HOOK_LOG` (default: `/tmp/agent-alchemy-hook.log`)

---

## Integration Notes

**What this component does:** Defines lifecycle event handlers that auto-approve file operations targeting deep-analysis session directories, enabling autonomous execution during analysis workflows without manual permission grants.

**Capabilities needed:** Pre-action hook/interceptor system that can inspect file operation targets and approve them programmatically. The host platform must support a way to intercept file writes and shell commands before execution.

**Adaptation guidance:** The auto-approval logic is straightforward path matching. On platforms without a hook system, this can be implemented as: (1) a pre-configured allow-list of directory patterns, (2) a middleware that checks file operation targets, or (3) a configuration setting that grants write access to session directories. The reference shell script in `references/` shows the exact matching logic.

**Configurable parameters:** None (the approved paths are tied to the deep-analysis session directory structure).
