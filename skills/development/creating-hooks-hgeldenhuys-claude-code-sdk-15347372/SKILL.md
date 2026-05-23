---
name: creating-hooks
description: Guide for implementing Claude Code hooks. Use when creating event-driven automation, auto-linting, validation, or context injection. Covers all hook events, matchers, exit codes, and environment variables.
allowed-tools: ["Read", "Write", "Edit", "Bash"]
---

# Creating Hooks

Build event-driven automation for Claude Code using hooks - scripts that execute at specific workflow points.

## Quick Reference

| Hook Event | When It Fires | Uses Matcher | Common Use Cases |
|------------|---------------|--------------|------------------|
| `PreToolUse` | Before tool executes | Yes | Validation, auto-approval, input modification |
| `PostToolUse` | After tool completes | Yes | Auto-formatting, linting, logging |
| `PermissionRequest` | User shown permission dialog | Yes | Auto-allow/deny, policy enforcement |
| `Notification` | Claude sends notification | Yes | Custom alerts, logging |
| `UserPromptSubmit` | User submits prompt | No | Prompt validation, context injection |
| `Stop` | Main agent finishes | No | Task completion checks, force continue |
| `SubagentStop` | Subagent (Task) finishes | No | Subagent task validation |
| `PreCompact` | Before context compaction | Yes | Custom compaction handling |
| `SessionStart` | Session begins/resumes | Yes | Context loading, env setup |
| `SessionEnd` | Session ends | No | Cleanup, logging |

## Configuration Locations

Hooks are configured in settings files (in order of precedence):

| Location | Scope | Committed |
|----------|-------|-----------|
| `~/.claude/settings.json` | User (all projects) | No |
| `.claude/settings.json` | Project | Yes |
| `.claude/settings.local.json` | Local project | No |
| Enterprise managed policy | Organization | Yes |

## Hook Structure

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Matcher Syntax

| Pattern | Matches | Example |
|---------|---------|---------|
| `Write` | Exact tool name | Only Write tool |
| `Edit\|Write` | Regex OR | Edit or Write |
| `Notebook.*` | Regex wildcard | NotebookEdit, NotebookRead |
| `mcp__memory__.*` | MCP server tools | All memory server tools |
| `*` or `""` | All tools | Any tool |

**Note:** Matchers are case-sensitive and only apply to `PreToolUse`, `PostToolUse`, and `PermissionRequest`.

### Hook Types

| Type | Description | Key Field |
|------|-------------|-----------|
| `command` | Execute bash script | `command`: bash command to run |
| `prompt` | LLM-based evaluation | `prompt`: prompt text for Haiku |

### Hook Options

| Option | Type | Description |
|--------|------|-------------|
| `timeout` | number | Timeout in seconds (default: 60, max: 600 as of 2.1.3) |
| `once` | boolean | Run only once per session (frontmatter hooks only) |

**Note:** As of 2.1.3, the maximum hook timeout was increased from 60 seconds to 10 minutes (600s).

## Exit Codes

| Exit Code | Meaning | Behavior |
|-----------|---------|----------|
| `0` | Success | Continue normally. stdout parsed for JSON control |
| `2` | Blocking error | Block action. stderr shown to Claude |
| Other | Non-blocking error | Log warning. Continue normally |

### Exit Code 2 Behavior by Event

| Event | Exit Code 2 Effect |
|-------|-------------------|
| `PreToolUse` | Blocks tool call, stderr to Claude |
| `PermissionRequest` | Denies permission, stderr to Claude |
| `PostToolUse` | stderr to Claude (tool already ran) |
| `UserPromptSubmit` | Blocks prompt, erases it, stderr to user |
| `Stop` / `SubagentStop` | Blocks stoppage, stderr to Claude |
| `Notification` / `SessionStart` / `SessionEnd` / `PreCompact` | stderr to user only |

## Environment Variables

| Variable | Description | Available In |
|----------|-------------|--------------|
| `CLAUDE_PROJECT_DIR` | Absolute path to project root | All hooks |
| `CLAUDE_PLUGIN_ROOT` | Absolute path to plugin directory | Plugin hooks only |
| `CLAUDE_ENV_FILE` | File path for persisting env vars | `SessionStart` only |
| `CLAUDE_CODE_REMOTE` | `"true"` if running in web environment | All hooks |

## Hook Input (stdin)

All hooks receive JSON via stdin with common fields:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/directory",
  "permission_mode": "default",
  "hook_event_name": "EventName"
}
```

**Permission modes:** `default`, `plan`, `acceptEdits`, `dontAsk`, `bypassPermissions`

## Decision Guide: Which Hook Do I Need?

### Before Tool Execution
**Use `PreToolUse`** to:
- Validate tool inputs before execution
- Auto-approve safe operations (e.g., reading docs)
- Block dangerous commands
- Modify tool inputs

### After Tool Execution
**Use `PostToolUse`** to:
- Auto-format code after Write/Edit
- Run linters after file changes
- Log file modifications
- Provide feedback to Claude

### Permission Automation
**Use `PermissionRequest`** to:
- Auto-allow trusted operations
- Auto-deny blocked patterns
- Enforce security policies

### Prompt Processing
**Use `UserPromptSubmit`** to:
- Inject context (current time, git status)
- Validate prompts for secrets
- Block sensitive requests

### Session Lifecycle
**Use `SessionStart`** to:
- Load development context
- Set environment variables
- Install dependencies

**Use `SessionEnd`** to:
- Clean up resources
- Log session statistics

### Agent Completion
**Use `Stop` / `SubagentStop`** to:
- Verify task completion
- Force Claude to continue working
- Add completion checks

### Context Management
**Use `PreCompact`** to:
- Customize compaction behavior
- Add pre-compaction context

### Alerts
**Use `Notification`** to:
- Custom notification routing
- Third-party integrations (Slack, Discord)

## Workflow: Creating a Hook

### Prerequisites
- [ ] Identify which event to hook into
- [ ] Decide: command (bash) or prompt (LLM) type
- [ ] Plan exit code behavior

### Steps

1. **Create hook script**
   - [ ] Write executable script (bash, python, etc.)
   - [ ] Read JSON from stdin
   - [ ] Output JSON to stdout (if needed)
   - [ ] Use appropriate exit code

2. **Configure in settings**
   - [ ] Add to appropriate settings file
   - [ ] Set matcher pattern (if applicable)
   - [ ] Set timeout if needed (default: 60s)

3. **Test**
   - [ ] Run `claude --debug` to see hook execution
   - [ ] Check `/hooks` menu for registration
   - [ ] Verify exit codes work as expected

### Validation
- [ ] Script is executable (`chmod +x`)
- [ ] JSON input/output is valid
- [ ] Exit codes are correct
- [ ] Matcher pattern works

## Tool-Specific Hooks

Common patterns for hooks targeting specific tools.

### Bash Tool Hooks

Validate commands before execution, log sensitive operations, or block dangerous commands.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate-bash.sh"
          }
        ]
      }
    ]
  }
}
```

**Common validations:**
- Block `rm -rf /` patterns
- Require approval for `sudo` commands
- Log all commands to audit file
- Block network commands in certain contexts

### Write Tool Hooks

Validate file paths, enforce naming conventions, or auto-format after write.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/after-write.sh"
          }
        ]
      }
    ]
  }
}
```

**Common patterns:**
- Auto-format with Prettier/Black
- Validate file encoding (UTF-8)
- Check for accidental credential writes
- Run type-checking after TypeScript writes

### Edit Tool Hooks

Validate edits, prevent changes to critical files, or run linting after edits.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate-edit.sh"
          }
        ]
      }
    ]
  }
}
```

**Common patterns:**
- Block edits to lock files (package-lock.json)
- Prevent edits to generated files
- Run linter after file edits
- Validate imports/exports after module changes

### Read Tool Hooks

Log file access, validate read permissions, or inject context based on files read.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate-read.sh"
          }
        ]
      }
    ]
  }
}
```

**Common patterns:**
- Block reading sensitive files (.env, credentials)
- Log file access for auditing
- Auto-approve reading documentation
- Inject related context when reading specific files

## Common Patterns

### Auto-Format on File Write

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/format.sh"
          }
        ]
      }
    ]
  }
}
```

### Inject Context on Session Start

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo \"Git branch: $(git branch --show-current)\""
          }
        ]
      }
    ]
  }
}
```

### Auto-Approve Documentation Reads

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/approve-docs.py"
          }
        ]
      }
    ]
  }
}
```

## Hook Framework (YAML Configuration)

For projects with multiple hooks, the Hook Framework provides a YAML-based configuration with built-in handlers and environment variable injection.

### Installation

```bash
bun add claude-code-sdk
```

### YAML Configuration

Create `hooks.yaml` in your project root:

```yaml
version: 1

settings:
  debug: false
  parallelExecution: true
  defaultTimeoutMs: 30000

builtins:
  # Human-friendly session names (e.g., "brave-elephant")
  session-naming:
    enabled: true
    options:
      format: adjective-animal

  # Track turns between Stop events
  turn-tracker:
    enabled: true

  # Block dangerous Bash commands
  dangerous-command-guard:
    enabled: true
    options:
      blockedPatterns:
        - "rm -rf /"
        - "rm -rf ~"

  # Inject session context
  context-injection:
    enabled: true
    options:
      template: "Session: ${sessionName} | Turn: ${turnId}"

  # Log tool usage
  tool-logger:
    enabled: true
    options:
      outputPath: ~/.claude/logs/tools.log

handlers:
  # Custom command handlers
  my-validator:
    events: [PreToolUse]
    matcher: "Bash"
    command: ./scripts/validate-command.sh
    timeoutMs: 5000
```

### Built-in Handlers

| Handler | Description | Default Events |
|---------|-------------|----------------|
| `session-naming` | Assigns human-friendly names | SessionStart |
| `turn-tracker` | Tracks turns between Stop events | SessionStart, Stop, SubagentStop |
| `dangerous-command-guard` | Blocks dangerous Bash commands | PreToolUse |
| `context-injection` | Injects session/turn context | SessionStart, PreCompact |
| `tool-logger` | Logs tool usage with context | PostToolUse |
| `event-logger` | Logs all hook events to JSONL for indexing | All events |
| `debug-logger` | Full payload logging for debugging | All events |
| `metrics` | Records hook execution timing metrics | All events |

### Environment Variables for Custom Handlers

Custom command handlers receive these environment variables:

| Variable | Description |
|----------|-------------|
| `CLAUDE_SESSION_ID` | Current session ID |
| `CLAUDE_SESSION_NAME` | Human-friendly session name |
| `CLAUDE_TURN_ID` | Turn identifier (session:sequence) |
| `CLAUDE_TURN_SEQUENCE` | Current turn number |
| `CLAUDE_EVENT_TYPE` | Hook event type |
| `CLAUDE_CWD` | Current working directory |
| `CLAUDE_PROJECT_DIR` | Project root path |

### TypeScript Framework

```typescript
import { createFramework, handler, blockResult } from 'claude-code-sdk/hooks/framework';

const framework = createFramework({ debug: true });

// Block dangerous commands
framework.onPreToolUse(
  handler()
    .id('danger-guard')
    .forTools('Bash')
    .handle(ctx => {
      const input = ctx.event.tool_input as { command?: string };
      if (input.command?.includes('rm -rf /')) {
        return blockResult('Dangerous command blocked');
      }
      return { success: true };
    })
);

// Access turn/session context
framework.onPostToolUse(
  handler()
    .id('context-logger')
    .handle(ctx => {
      const turnId = ctx.results.get('turn-tracker')?.data?.turnId;
      const sessionName = ctx.results.get('session-naming')?.data?.sessionName;
      console.error(`[${sessionName}] Turn ${turnId}: ${ctx.event.tool_name}`);
      return { success: true };
    })
);

await framework.run();
```

### Using with settings.json

Point your settings.json to the framework entry point:

```json
{
  "hooks": {
    "PreToolUse": [{ "matcher": "*", "hooks": [{ "type": "command", "command": "bun run hooks-framework" }] }],
    "PostToolUse": [{ "matcher": "*", "hooks": [{ "type": "command", "command": "bun run hooks-framework" }] }],
    "SessionStart": [{ "matcher": "*", "hooks": [{ "type": "command", "command": "bun run hooks-framework" }] }],
    "Stop": [{ "matcher": "*", "hooks": [{ "type": "command", "command": "bun run hooks-framework" }] }]
  }
}
```

## Debugging

| Issue | Solution |
|-------|----------|
| Hook not running | Check `/hooks` menu, verify JSON syntax |
| Wrong matcher | Tool names are case-sensitive |
| Command not found | Use absolute paths or `$CLAUDE_PROJECT_DIR` |
| Script not executing | Check permissions (`chmod +x`) |
| Exit code ignored | Only 0, 2, and other are recognized |
| Framework not loading | Check `hooks.yaml` syntax, run with `debug: true` |

Run with debug mode:
```bash
claude --debug
```

## Security Considerations

- [ ] Validate and sanitize all inputs
- [ ] Quote shell variables (`"$VAR"` not `$VAR`)
- [ ] Check for path traversal (`..`)
- [ ] Use absolute paths for scripts
- [ ] Skip sensitive files (`.env`, keys)

## Frontmatter Hooks

Hooks can also be defined directly in YAML frontmatter of Skills, Agents, and Slash Commands. These hooks are:

- **Lifecycle-scoped** - Only active while the component executes
- **Auto-cleanup** - Removed when the component finishes
- **Portable** - Packaged with the component for distribution

**Supported events:** `PreToolUse`, `PostToolUse`, `Stop`

### Quick Example (in a Skill)

```yaml
---
name: my-skill
description: A skill with lifecycle hooks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./validate.sh"
          once: true
---
```

### Key Differences from Settings Hooks

| Aspect | Settings Hooks | Frontmatter Hooks |
|--------|----------------|-------------------|
| Location | `settings.json` | Skill/Agent/Command YAML |
| Scope | Global or project | Component lifecycle |
| Events | All 10 events | PreToolUse, PostToolUse, Stop |
| Cleanup | Manual | Automatic |
| `once` option | No | Yes |

See [FRONTMATTER-HOOKS.md](./FRONTMATTER-HOOKS.md) for complete documentation.

## Reference Files

| File | Contents |
|------|----------|
| [EVENTS.md](./EVENTS.md) | Detailed event documentation with input/output schemas |
| [EXAMPLES.md](./EXAMPLES.md) | Complete working examples |
| [FRONTMATTER-HOOKS.md](./FRONTMATTER-HOOKS.md) | Frontmatter hooks in skills, agents, commands |
| [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) | Common issues and solutions |
