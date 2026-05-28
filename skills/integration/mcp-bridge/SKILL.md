---
name: mcp-bridge
description: MCP detection and unified state operations. Provides seamless integration with Control Tower MCP when available, with file-based fallback.
---

# MCP Bridge

// Project Autopilot - MCP Bridge Skill
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Core Principle:** Detect MCP availability once at command start, use unified interfaces throughout execution.

---

## MCP Configuration Detection

### Configuration File Locations

MCP configuration is checked in order of precedence:

| Scope | Path | Description |
|-------|------|-------------|
| Project | `.mcp.json` | Project-scoped, shared with team |
| User | `~/.claude.json` | User-scoped, all projects |
| User Local | `~/.claude/settings.local.json` | User local settings |

### Detection Function

```
FUNCTION detectControlTower():
    """
    Detect whether Control Tower MCP is configured and available.
    Returns detection result for use throughout command execution.
    """

    # Configuration file locations (checked in order)
    configPaths = [
        "{cwd}/.mcp.json",                    # Project scope
        "~/.claude.json",                     # User scope
        "~/.claude/settings.local.json"       # User local
    ]

    FOR each configPath IN configPaths:
        IF fileExists(configPath):
            TRY:
                config = parseJSON(readFile(configPath))

                # Check for control-tower or autopilot server entry
                IF config.mcpServers:
                    IF "control-tower" IN config.mcpServers:
                        RETURN {
                            available: true,
                            source: 'mcp',
                            serverName: 'control-tower',
                            configPath: configPath
                        }
                    IF "autopilot" IN config.mcpServers:
                        RETURN {
                            available: true,
                            source: 'mcp',
                            serverName: 'autopilot',
                            configPath: configPath
                        }
            CATCH:
                # Ignore parse errors, try next config
                CONTINUE

    # No MCP configuration found
    RETURN {
        available: false,
        source: 'local'
    }
```

### Example Detection Result

```json
// MCP Available
{
  "available": true,
  "source": "mcp",
  "serverName": "control-tower",
  "configPath": "/Users/dev/.claude.json"
}

// Local Mode
{
  "available": false,
  "source": "local"
}
```

---

## Unified State Operations

### Save Checkpoint

```
FUNCTION saveCheckpoint(state, context):
    """
    Save checkpoint via MCP if available, otherwise file-based.

    Parameters:
        state: {
            phase: string,
            task: string,
            decisions: array,
            todos: array,
            blockers: array
        }
        context: detection result from detectControlTower()
    """

    IF context.available:
        TRY:
            result = CALL_MCP "checkpoint_save" {
                project_id: context.projectId,
                execution_id: context.executionId,
                state: state,
                phase: state.phase,
                task: state.task,
                context_usage_pct: getContextUsage(),
                name: "Auto-checkpoint"
            }

            LOG "Checkpoint saved via Control Tower"
            RETURN {source: 'mcp', id: result.checkpoint_id}

        CATCH error:
            # MCP configured but failed - show clear error, don't silently fallback
            handleMCPError(error)
            THROW error
    ELSE:
        # MCP not configured - use file-based (no warning, this is expected)
        formatted = formatTransponderState(state)
        writeFile(".autopilot/TRANSPONDER.md", formatted)
        LOG "State saved locally"
        RETURN {source: 'local', path: '.autopilot/TRANSPONDER.md'}
```

### Load Checkpoint

```
FUNCTION loadCheckpoint(projectId, context):
    """
    Load latest checkpoint via MCP if available, otherwise file-based.

    Parameters:
        projectId: string (UUID for MCP, ignored for local)
        context: detection result from detectControlTower()

    Returns:
        Checkpoint state object
    """

    IF context.available:
        TRY:
            result = CALL_MCP "checkpoint_load" {
                project_id: projectId
                # checkpoint_id omitted for latest
            }

            LOG "Checkpoint loaded from Control Tower"
            RETURN {
                source: 'mcp',
                state: result.state,
                checkpoint_id: result.checkpoint_id,
                created_at: result.created_at
            }

        CATCH error:
            handleMCPError(error)
            THROW error
    ELSE:
        # Local state
        IF fileExists(".autopilot/TRANSPONDER.md"):
            content = readFile(".autopilot/TRANSPONDER.md")
            state = parseTransponderState(content)
            RETURN {source: 'local', state: state}
        ELSE:
            RETURN {source: 'local', state: null}
```

### Update Progress

```
FUNCTION updateProgress(projectId, executionId, phase, task, status, message, context):
    """
    Update progress via MCP if available, otherwise file-based.

    Parameters:
        projectId: string (UUID)
        executionId: string (UUID)
        phase: string (e.g., "03-api")
        task: string (e.g., "03.2")
        status: "pending" | "in_progress" | "completed" | "failed" | "skipped"
        message: string (description of progress)
        context: detection result from detectControlTower()
    """

    IF context.available:
        TRY:
            result = CALL_MCP "progress_update" {
                project_id: projectId,
                execution_id: executionId,
                phase: phase,
                task: task,
                status: status,
                message: message
            }

            # Progress update is silent (no log spam)
            RETURN {source: 'mcp', id: result.id}

        CATCH error:
            handleMCPError(error)
            THROW error
    ELSE:
        # Append to progress.md
        entry = formatProgressEntry(phase, task, status, message)
        appendFile(".autopilot/progress.md", entry)
        RETURN {source: 'local', path: '.autopilot/progress.md'}
```

### Record Activity

```
FUNCTION recordActivity(projectId, executionId, message, context):
    """
    Record activity log entry via MCP if available, otherwise file-based.

    Parameters:
        projectId: string (UUID)
        executionId: string (UUID)
        message: string (activity description)
        context: detection result from detectControlTower()
    """

    IF context.available:
        TRY:
            result = CALL_MCP "activity_log" {
                project_id: projectId,
                execution_id: executionId,
                message: message
            }

            RETURN {source: 'mcp', id: result.id}

        CATCH error:
            handleMCPError(error)
            THROW error
    ELSE:
        # Append to progress.md with timestamp
        timestamp = formatTimestamp(now())
        entry = "{timestamp} | {message}\n"
        appendFile(".autopilot/progress.md", entry)
        RETURN {source: 'local', path: '.autopilot/progress.md'}
```

### Record Cost

```
FUNCTION recordCost(projectId, executionId, model, inputTokens, outputTokens, cost, context):
    """
    Record token/cost usage via MCP if available, otherwise file-based.

    Parameters:
        projectId: string (UUID)
        executionId: string (UUID)
        model: string (e.g., "claude-sonnet-4-20250514")
        inputTokens: number
        outputTokens: number
        cost: number (USD)
        context: detection result from detectControlTower()
    """

    IF context.available:
        TRY:
            result = CALL_MCP "cost_record" {
                project_id: projectId,
                execution_id: executionId,
                model: model,
                input_tokens: inputTokens,
                output_tokens: outputTokens,
                cost: cost
            }

            RETURN {source: 'mcp', id: result.id}

        CATCH error:
            handleMCPError(error)
            THROW error
    ELSE:
        # Append to token-usage.md
        entry = formatCostEntry(model, inputTokens, outputTokens, cost)
        appendFile(".autopilot/token-usage.md", entry)
        RETURN {source: 'local', path: '.autopilot/token-usage.md'}
```

---

## Error Handling

### MCP Error Handler

```
FUNCTION handleMCPError(error):
    """
    Handle MCP errors with clear troubleshooting steps.
    Do NOT silently fallback - if MCP is configured but fails, user needs to know.
    """

    LOG ""
    LOG "Control Tower MCP unavailable."
    LOG ""
    LOG "Troubleshooting steps:"
    LOG "  1) Verify MCP server running:"
    LOG "     cd control-tower && npm run start:mcp"
    LOG ""
    LOG "  2) Check Claude Code MCP config:"
    LOG "     Run /mcp to verify control-tower server listed"
    LOG ""
    LOG "  3) Verify database connection:"
    LOG "     Ensure PostgreSQL is running"
    LOG ""
    LOG "  4) Check server logs:"
    LOG "     Look for connection errors in MCP server output"
    LOG ""

    IF error.message:
        LOG "Error details: {error.message}"
```

### Error Categories

| Error Type | Behavior | User Action |
|------------|----------|-------------|
| MCP not configured | Use local files silently | None - expected |
| MCP configured, server unreachable | Show error, halt | Start MCP server |
| MCP configured, auth failed | Show error, halt | Check API key |
| MCP configured, database error | Show error, halt | Check PostgreSQL |

---

## Output Formatting

### Source Indicator

```
FUNCTION getSourceIndicator(context):
    """
    Returns indicator text for command banner.
    """

    IF context.available:
        RETURN "Control Tower"
    ELSE:
        RETURN "Local"
```

### Banner Format

```
# With Control Tower MCP:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AUTOPILOT: TAKEOFF                               Control Tower
   Execute flight plan with wave-based parallelization
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# With local file-based state:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AUTOPILOT: TAKEOFF                                      Local
   Execute flight plan with wave-based parallelization
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Dashboard Link

```
FUNCTION showDashboardLink(projectId, context):
    """
    Show dashboard link only when Control Tower is active and projectId valid.
    """

    IF context.available AND projectId:
        # Get dashboard URL from config or use default
        dashboardUrl = context.dashboardUrl OR "http://localhost:3000"

        LOG ""
        LOG "View in dashboard: {dashboardUrl}/projects/{projectId}"
```

### Dashboard Link Display Rules

| Condition | Show Link? | Reason |
|-----------|------------|--------|
| MCP available, valid projectId | Yes | Full functionality |
| MCP available, no projectId | No | Project not registered |
| Local mode | No | No dashboard in local mode |
| --local flag | No | Explicitly local mode |

---

## Flag Handling

### --local Flag

```
FUNCTION initializeStateBackend(arguments):
    """
    Initialize state backend based on MCP availability and flags.
    Called at command startup.
    """

    # Check for --local flag first
    IF "--local" IN arguments:
        LOG "Using local file-based state (--local flag)"
        RETURN {
            available: false,
            source: 'local',
            forced: true
        }

    # Detect Control Tower
    detection = detectControlTower()

    IF detection.available:
        LOG "Control Tower MCP detected"

        # Auto-register project if needed
        projectId = ensureProjectRegistered(detection)
        detection.projectId = projectId

        # Get or create execution
        executionId = getOrCreateExecution(projectId)
        detection.executionId = executionId
    ELSE:
        LOG "Using local file-based state"

    RETURN detection
```

### Ensure Project Registered

```
FUNCTION ensureProjectRegistered(context):
    """
    Ensure current project is registered with Control Tower.
    Returns projectId (existing or newly created).
    """

    # Check for existing project by path
    result = CALL_MCP "project_lookup" {
        path: getCurrentDirectory()
    }

    IF result.project_id:
        RETURN result.project_id

    # Register new project
    projectName = getProjectName()  # From package.json or directory name

    result = CALL_MCP "project_register" {
        name: projectName,
        path: getCurrentDirectory(),
        description: getProjectDescription()  # From clearance.md if exists
    }

    RETURN result.project_id
```

---

## Integration Examples

### Takeoff Command Integration

```
# At command start (Phase 0)
context = initializeStateBackend(arguments)
sourceIndicator = getSourceIndicator(context)

# Display banner with source indicator
LOG "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
LOG "AUTOPILOT: TAKEOFF                               {sourceIndicator}"
LOG "   Execute flight plan with wave-based parallelization"
LOG "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# During execution - save checkpoint
saveCheckpoint({
    phase: currentPhase,
    task: currentTask,
    decisions: recentDecisions,
    todos: pendingTodos,
    blockers: currentBlockers
}, context)

# During execution - update progress
updateProgress(
    context.projectId,
    context.executionId,
    "03-api",
    "03.2",
    "completed",
    "Created user endpoints with validation",
    context
)

# During execution - record cost
recordCost(
    context.projectId,
    context.executionId,
    "claude-sonnet-4-20250514",
    15000,
    8500,
    0.12,
    context
)

# At completion
showDashboardLink(context.projectId, context)
```

### Cockpit Command Integration

```
# At command start
context = initializeStateBackend(arguments)
sourceIndicator = getSourceIndicator(context)

# Display banner with source indicator
LOG "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
LOG "AUTOPILOT: COCKPIT                              {sourceIndicator}"
LOG "   Return to cockpit - resume flight from waypoint"
LOG "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Load checkpoint
checkpoint = loadCheckpoint(context.projectId, context)

IF checkpoint.state:
    LOG "Checkpoint loaded: Phase {checkpoint.state.phase}, Task {checkpoint.state.task}"
ELSE:
    LOG "No checkpoint found - starting fresh"

# At resume
showDashboardLink(context.projectId, context)
```

---

## State File Paths

### Local Mode Files

| File | Purpose |
|------|---------|
| `.autopilot/TRANSPONDER.md` | Session state bridge |
| `.autopilot/progress.md` | Activity log |
| `.autopilot/token-usage.md` | Cost tracking |
| `.autopilot/holding-pattern.md` | Mid-phase resume |

### MCP Mode Storage

| Tool | Data Stored |
|------|-------------|
| `checkpoint_save` | State snapshots with full context |
| `progress_update` | Phase/task progress entries |
| `activity_log` | Activity timeline |
| `cost_record` | Token/cost records |

---

## Testing Checklist

Before deploying MCP integration:

```
[ ] Test with MCP not configured → uses local files silently
[ ] Test with MCP configured and working → uses MCP
[ ] Test with MCP configured but server down → shows error, does not fallback
[ ] Test with --local flag → forces local even when MCP configured
[ ] Test dashboard link only shows when MCP active
[ ] Test source indicator displays correctly in banner
[ ] Test all commands maintain identical output format except indicator
```

---

## Quick Reference

### Detection Priority

1. `--local` flag (force local)
2. `.mcp.json` (project scope)
3. `~/.claude.json` (user scope)
4. `~/.claude/settings.local.json` (user local)
5. Fallback to local

### Operation Priority

1. If MCP available: Use MCP tools
2. If MCP fails: Show error, halt (no silent fallback)
3. If MCP not configured: Use local files (no warning)

### Source Indicators

| Mode | Indicator |
|------|-----------|
| Control Tower MCP | `Control Tower` |
| Local files | `Local` |
| Forced local (--local) | `Local` |
