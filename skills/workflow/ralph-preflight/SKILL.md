---
name: ralph-preflight
description: Check all MCP servers and services before workflow execution. MUST pass before any Ralph command proceeds.
triggers:
  - /ralph.preflight
  - preflight check
  - check services
---

# /ralph.preflight

Validate all required services before workflow execution.

## CRITICAL: Run Before Any Ralph Command

This command MUST pass before `/ralph.spawn`, `/ralph.integrate`, or `/ralph.cleanup`.
If pre-flight fails, the workflow is BLOCKED until issues are resolved.

## Process

1. **Check Linear MCP (REQUIRED)**

   ```
   # Attempt to list teams - if this fails, Linear is not authenticated
   mcp__plugin_linear_linear__list_teams({})
   ```

   **If empty or error**: BLOCK immediately

   ```
   # Verify floe team access
   mcp__plugin_linear_linear__get_team({"query": "floe"})
   ```

   **If no access**: BLOCK - user must fix Linear authentication

2. **Check Git (REQUIRED)**

   ```bash
   git status --porcelain
   ```

   **If fails**: BLOCK - not in a git repository

3. **Check Cognee (OPTIONAL)**

   Check if `.cognee/config.yaml` exists and `COGNEE_API_KEY` is set.

   **If unavailable**: WARN - memories will buffer locally via `.ralph/memory-buffer/`

4. **Check Memory Buffer**

   ```bash
   ls .ralph/memory-buffer/pending/*.json 2>/dev/null | wc -l
   ls .ralph/memory-buffer/failed/*.json 2>/dev/null | wc -l
   ```

   **If failed entries**: WARN - review `.ralph/memory-buffer/failed/`

5. **Check Manifest**

   Verify `.ralph/manifest.json` is valid JSON.

## Output: PASS

```
==================================================
RALPH WIGGUM PRE-FLIGHT CHECK: PASS
==================================================

[OK] linear: Connected to Linear MCP
[OK] git: Git repository valid
[OK] cognee: Cognee configuration found
[OK] manifest: Manifest valid (v1.0.0)
[OK] memory_buffer: Buffer empty - ready for use

--------------------------------------------------
Status: Ready to proceed
```

## Output: BLOCKED

```
==================================================
RALPH WIGGUM PRE-FLIGHT CHECK: BLOCKED
==================================================

[!!] linear: Linear MCP not authenticated
    Action: Re-authenticate Linear in Claude Code settings
[OK] git: Git repository valid
[??] cognee: COGNEE_API_KEY not set - using local buffer
    Action: Set COGNEE_API_KEY environment variable

--------------------------------------------------
Status: BLOCKED - Fix required issues before proceeding

Recovery:
  1. Fix the blocked service(s) above
  2. Run: /ralph.preflight to verify
  3. Resume with: /ralph.resume
```

## Linear Authentication Recovery

If Linear MCP authentication fails:

1. **Check MCP server status** in Claude Code settings
2. **Re-authenticate** if token expired
3. **Verify team access** - must have access to "floe" team
4. **Run** `/ralph.preflight` again to verify

## Cognee Degraded Mode

When Cognee is unavailable:

1. Memories are written to `.ralph/memory-buffer/pending/`
2. Format: `{timestamp}-{type}-{id}.json`
3. Auto-sync when Cognee reconnects (see `/ralph.memory-sync`)
4. No context is lost - all decisions recorded locally

## Pre-Flight Script

For programmatic access:

```bash
python .ralph/scripts/preflight.py           # Check all
python .ralph/scripts/preflight.py -s linear # Check Linear only
python .ralph/scripts/preflight.py --json    # JSON output
```

## Configuration

From `.ralph/config.yaml`:

```yaml
resilience:
  preflight_checks:
    linear: required   # BLOCK if unavailable
    cognee: optional   # WARN + continue with buffer
    git: required      # BLOCK if unavailable
```

## Related Commands

- `/ralph.spawn` - Start agents (requires preflight PASS)
- `/ralph.resume` - Resume from saved session
- `/ralph.memory-sync` - Sync buffered memories
- `/ralph.memory-status` - Check buffer status
