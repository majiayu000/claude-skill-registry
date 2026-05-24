---
name: claude-hooks-reference-2026
description: Complete reference for Claude Code hooks system (January 2026). Use when creating hooks, understanding hook events, matchers, exit codes, JSON output control, environment variables, plugin hooks, or implementing hook scripts.
user-invocable: true
---

# Claude Code Hooks System - Complete Reference (January 2026)

Hooks execute custom commands or prompts in response to Claude Code events. Use for automation, validation, formatting, and security.

---

## All Hook Events

| Event                | When Fired                        | Matcher Applies | Common Uses             |
| -------------------- | --------------------------------- | --------------- | ----------------------- |
| `PreToolUse`         | Before tool execution             | Yes             | Validation, blocking    |
| `PermissionRequest`  | When user shown permission dialog | Yes             | Auto-approval policies  |
| `PostToolUse`        | After successful tool execution   | Yes             | Formatting, linting     |
| `PostToolUseFailure` | After tool fails                  | Yes             | Error handling          |
| `Notification`       | When Claude wants attention       | Yes             | Custom notifications    |
| `UserPromptSubmit`   | User submits prompt               | No              | Input validation        |
| `Stop`               | Claude finishes response          | No              | Cleanup, final checks   |
| `SubagentStart`      | When spawning a subagent          | No              | Subagent initialization |
| `SubagentStop`       | Subagent (Task tool) completes    | No              | Result validation       |
| `PreCompact`         | Before context compaction         | Yes             | State backup            |
| `Setup`              | Repository setup/maintenance      | Yes             | One-time operations     |
| `SessionStart`       | Session begins or resumes         | Yes             | Environment setup       |
| `SessionEnd`         | Session ends                      | No              | Cleanup, persistence    |

---

## Configuration

### Configuration Locations (Precedence highest to lowest)

1. **Managed** - `managed-settings.json` (enterprise)
2. **Local** - `.claude/settings.local.json` (gitignored)
3. **Project** - `.claude/settings.json` (shared via git)
4. **User** - `~/.claude/settings.json` (personal)
5. **Plugin** - `hooks/hooks.json` or frontmatter
6. **Capability** - Skill/Command/Agent frontmatter

**Note**: Enterprise administrators can use `allowManagedHooksOnly` to block user, project, and plugin hooks.

### Structure

Hooks are organized by matchers, where each matcher can have multiple hooks:

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

**Fields:**

- **matcher**: Pattern to match tool names, case-sensitive (only for `PreToolUse`, `PermissionRequest`, `PostToolUse`)
  - Simple strings match exactly: `Write` matches only the Write tool
  - Supports regex: `Edit|Write` or `Notebook.*`
  - Use `*` to match all tools. Also accepts empty string (`""`) or omit `matcher`
- **hooks**: Array of hooks to execute when pattern matches
  - `type`: `"command"` for bash commands or `"prompt"` for LLM evaluation
  - `command`: (For `type: "command"`) The bash command to execute
  - `prompt`: (For `type: "prompt"`) The prompt to send to the LLM
  - `timeout`: (Optional) Seconds before canceling (default: 60 for commands, 30 for prompts)

### Project-Specific Hook Scripts

Use `$CLAUDE_PROJECT_DIR` to reference scripts in your project:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-style.sh"
          }
        ]
      }
    ]
  }
}
```

### Events Without Matchers

For `UserPromptSubmit`, `Stop`, `SubagentStop`, and `SessionEnd`, omit the matcher:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/prompt-validator.py"
          }
        ]
      }
    ]
  }
}
```

---

## Plugin Hooks

Plugins can provide hooks that integrate with user and project hooks. For complete plugin documentation including plugin.json schema, directory structure, and component integration, see [./claude-plugins-reference-2026/SKILL.md](../claude-plugins-reference-2026/SKILL.md).

### How Plugin Hooks Work

- Plugin hooks defined in `hooks/hooks.json` or custom path via `hooks` field in plugin.json
- When plugin enabled, its hooks merge with user and project hooks
- Multiple hooks from different sources can respond to same event
- Plugin hooks run alongside custom hooks in parallel

### Plugin Hook Configuration

Hooks can be configured in `hooks/hooks.json` or inline in `plugin.json`:

```json
{
  "description": "Automatic code formatting",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

Reference in plugin.json:

```json
{
  "name": "my-plugin",
  "hooks": "./hooks/hooks.json"
}
```

Or define inline:

```json
{
  "name": "my-plugin",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh"
          }
        ]
      }
    ]
  }
}
```

### Plugin Environment Variables

- `${CLAUDE_PLUGIN_ROOT}`: Absolute path to the plugin directory
- `${CLAUDE_PROJECT_DIR}`: Project root directory
- All standard environment variables available

---

## Hooks in Skills, Agents, and Slash Commands

Hooks can be defined in frontmatter. These are scoped to the component's lifecycle. For complete skill documentation, see [./claude-skills-reference-2026/SKILL.md](../claude-skills-reference-2026/SKILL.md).

**Supported events**: `PreToolUse`, `PostToolUse`, `Stop`

### Skill Example

```yaml
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

### Agent Example

```yaml
---
name: code-reviewer
description: Review code changes
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

### `once` Option

Set `once: true` to run hook only once per session. After first successful execution, hook is removed.

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/one-time-setup.sh"
          once: true
```

**Note**: Only supported for skills and slash commands, not agents.

---

## Event-Specific Matchers

### PreToolUse / PermissionRequest / PostToolUse Common Matchers

| Matcher             | Description                    |
| ------------------- | ------------------------------ |
| `Task`              | Subagent tasks                 |
| `Bash`              | Shell commands                 |
| `Glob`              | File pattern matching          |
| `Grep`              | Content search                 |
| `Read`              | File reading                   |
| `Edit`              | File editing                   |
| `Write`             | File writing                   |
| `WebFetch`          | Web fetching                   |
| `WebSearch`         | Web search                     |
| `Notebook.*`        | NotebookEdit, NotebookRead     |
| `mcp__<server>__.*` | All tools from MCP server      |
| `mcp__.*__write.*`  | MCP write tools across servers |

### SessionStart Matchers

| Matcher   | Trigger                                |
| --------- | -------------------------------------- |
| `startup` | New session started                    |
| `resume`  | `--resume`, `--continue`, or `/resume` |
| `clear`   | `/clear` command                       |
| `compact` | Auto or manual compact                 |

### PreCompact Matchers

| Matcher  | Trigger                     |
| -------- | --------------------------- |
| `manual` | `/compact` command          |
| `auto`   | Auto-compact (full context) |

### Setup Matchers

| Matcher       | Trigger                         |
| ------------- | ------------------------------- |
| `init`        | `--init` or `--init-only` flags |
| `maintenance` | `--maintenance` flag            |

### Notification Matchers

| Matcher              | Trigger                              |
| -------------------- | ------------------------------------ |
| `permission_prompt`  | Permission requests from Claude      |
| `idle_prompt`        | Claude waiting for input (60s+ idle) |
| `auth_success`       | Authentication success               |
| `elicitation_dialog` | MCP tool elicitation                 |

---

## Hook Input (JSON via stdin)

### Common Fields (All Events)

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/session.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse"
}
```

**`permission_mode` values**: `"default"`, `"plan"`, `"acceptEdits"`, `"dontAsk"`, `"bypassPermissions"`

### PreToolUse Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/session.jsonl",
  "cwd": "/path/to/project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "psql -c 'SELECT * FROM users'",
    "description": "Query the users table",
    "timeout": 120000
  },
  "tool_use_id": "toolu_01ABC123"
}
```

**Tool-specific `tool_input` fields:**

| Tool    | Fields                                                   |
| ------- | -------------------------------------------------------- |
| `Bash`  | `command`, `description`, `timeout`, `run_in_background` |
| `Write` | `file_path`, `content`                                   |
| `Edit`  | `file_path`, `old_string`, `new_string`, `replace_all`   |
| `Read`  | `file_path`, `offset`, `limit`                           |

### PostToolUse Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/session.jsonl",
  "cwd": "/path/to/project",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  },
  "tool_use_id": "toolu_01ABC123"
}
```

### Notification Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/session.jsonl",
  "cwd": "/path/to/project",
  "permission_mode": "default",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission to use Bash",
  "notification_type": "permission_prompt"
}
```

### UserPromptSubmit Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/session.jsonl",
  "cwd": "/path/to/project",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate factorial"
}
```

### Stop Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/session.jsonl",
  "cwd": "/path/to/project",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": true
}
```

**`stop_hook_active`**: True when Claude is already continuing due to a stop hook. Check this to prevent infinite loops.

### SubagentStart Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/session.jsonl",
  "cwd": "/path/to/project",
  "permission_mode": "default",
  "hook_event_name": "SubagentStart",
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

**Fields**:

- `agent_id`: Unique identifier for the subagent
- `agent_type`: Agent name (built-in like "Bash", "Explore", "Plan", or custom agent names)

### SubagentStop Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/session.jsonl",
  "cwd": "/path/to/project",
  "permission_mode": "default",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false,
  "agent_id": "def456",
  "agent_transcript_path": "/path/to/subagents/agent-def456.jsonl"
}
```

**Fields**:

- `agent_id`: Unique identifier for the subagent
- `agent_transcript_path`: Path to the subagent's own transcript in nested `subagents/` folder
- `stop_hook_active`: True when already continuing due to a stop hook

### PreCompact Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/session.jsonl",
  "cwd": "/path/to/project",
  "permission_mode": "default",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

### Setup Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/session.jsonl",
  "cwd": "/path/to/project",
  "permission_mode": "default",
  "hook_event_name": "Setup",
  "trigger": "init"
}
```

**Fields**:

- `trigger`: Either `"init"` (from `--init` or `--init-only`) or `"maintenance"` (from `--maintenance`)
- Setup hooks have access to `CLAUDE_ENV_FILE` for persisting environment variables

### SessionStart Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/session.jsonl",
  "cwd": "/path/to/project",
  "permission_mode": "default",
  "hook_event_name": "SessionStart",
  "source": "startup",
  "model": "claude-sonnet-4-20250514"
}
```

**Fields**:

- `source`: Indicates how session started: `"startup"` (new), `"resume"` (resumed), `"clear"` (after `/clear`), or `"compact"` (after compaction)
- `model`: Model identifier when available
- `agent_type`: (Optional) Present when Claude Code started with `claude --agent <name>`

### SessionEnd Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/session.jsonl",
  "cwd": "/path/to/project",
  "permission_mode": "default",
  "hook_event_name": "SessionEnd",
  "reason": "exit"
}
```

**`reason` values**: `clear`, `logout`, `prompt_input_exit`, `other`

---

## Hook Output

### Exit Codes

| Code  | Behavior                                                         |
| ----- | ---------------------------------------------------------------- |
| 0     | Success. stdout processed (JSON or plain text)                   |
| 2     | Blocking error. stderr used as error message, fed back to Claude |
| Other | Non-blocking error. stderr shown in verbose mode (Ctrl+O)        |

**Important**: Claude Code does not see stdout if exit code is 0, except for `UserPromptSubmit` and `SessionStart` where stdout is added to context.

### Exit Code 2 Behavior Per Event

| Event                | Exit Code 2 Behavior                             |
| -------------------- | ------------------------------------------------ |
| `PreToolUse`         | Blocks tool call, shows stderr to Claude         |
| `PermissionRequest`  | Denies permission, shows stderr to Claude        |
| `PostToolUse`        | Shows stderr to Claude (tool already ran)        |
| `PostToolUseFailure` | Shows stderr to Claude (tool already failed)     |
| `Notification`       | Shows stderr to user only                        |
| `UserPromptSubmit`   | Blocks prompt, erases it, shows stderr to user   |
| `Stop`               | Blocks stoppage, shows stderr to Claude          |
| `SubagentStart`      | Shows stderr to user only                        |
| `SubagentStop`       | Blocks stoppage, shows stderr to Claude subagent |
| `PreCompact`         | Shows stderr to user only                        |
| `Setup`              | Shows stderr to user only                        |
| `SessionStart`       | Shows stderr to user only                        |
| `SessionEnd`         | Shows stderr to user only                        |

---

## JSON Output Control

**Important**: JSON output only processed with exit code 0. Exit code 2 uses stderr only.

### Common JSON Fields (All Events)

```json
{
  "continue": true,
  "stopReason": "Message shown when continue is false",
  "suppressOutput": false,
  "systemMessage": "Optional warning message shown to user"
}
```

| Field            | Type    | Effect                                           |
| ---------------- | ------- | ------------------------------------------------ |
| `continue`       | boolean | `false` stops Claude (takes precedence over all) |
| `stopReason`     | string  | Shown to user when `continue` is false           |
| `suppressOutput` | boolean | Hide stdout from transcript mode                 |
| `systemMessage`  | string  | Warning message shown to user                    |

**Precedence**: `continue: false` takes precedence over any `decision: "block"` output.

### PreToolUse JSON Output

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Auto-approved documentation file",
    "updatedInput": {
      "field_to_modify": "new value"
    },
    "additionalContext": "Current environment: production. Proceed with caution."
  }
}
```

| Field                      | Values                 | Effect                                     |
| -------------------------- | ---------------------- | ------------------------------------------ |
| `permissionDecision`       | `allow`, `deny`, `ask` | Controls tool execution                    |
| `permissionDecisionReason` | string                 | Shown to user (allow/ask) or Claude (deny) |
| `updatedInput`             | object                 | Modifies tool input before execution       |
| `additionalContext`        | string                 | Added to Claude's context                  |

**Note**: `decision` and `reason` fields are deprecated. Use `hookSpecificOutput.permissionDecision` and `hookSpecificOutput.permissionDecisionReason`. Deprecated `"approve"` and `"block"` map to `"allow"` and `"deny"`.

### PermissionRequest JSON Output

Allow with modified input:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm run lint"
      }
    }
  }
}
```

Deny with message:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "deny",
      "message": "Command not allowed by policy",
      "interrupt": true
    }
  }
}
```

### PostToolUse JSON Output

```json
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude"
  }
}
```

- `"block"` automatically prompts Claude with `reason`
- `undefined` does nothing, `reason` is ignored

### UserPromptSubmit JSON Output

```json
{
  "decision": "block",
  "reason": "Prompt contains sensitive data",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here"
  }
}
```

**Two ways to add context (exit code 0):**

1. **Plain text stdout**: Any non-JSON text is added as context
2. **JSON with `additionalContext`**: More structured control

**Blocking prompts:**

- `"decision": "block"` prevents prompt processing, erases prompt from context
- `"reason"` shown to user but not added to context

### Stop / SubagentStop JSON Output

```json
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

- `"block"` prevents Claude from stopping. Must populate `reason`
- `undefined` allows Claude to stop. `reason` is ignored

### Setup JSON Output

```json
{
  "hookSpecificOutput": {
    "hookEventName": "Setup",
    "additionalContext": "Repository initialized with custom configuration"
  }
}
```

**Note**: Multiple hooks' `additionalContext` values are concatenated. Setup hooks have access to `CLAUDE_ENV_FILE` for persisting environment variables.

### SessionStart JSON Output

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Project context loaded successfully"
  }
}
```

**Note**: Multiple hooks' `additionalContext` values are concatenated.

---

## Prompt-Based Hooks

LLM-evaluated decisions using a fast model (Haiku). Also known as "agent hooks" for complex verification tasks.

### How Prompt-Based Hooks Work

1. Send the hook input and your prompt to Haiku
2. The LLM responds with structured JSON containing a decision
3. Claude Code processes the decision automatically

### Configuration

```json
{
  "type": "prompt",
  "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete.",
  "timeout": 30
}
```

Alternatively, use `"type": "agent"` for complex verification tasks that require tool access.

| Field     | Required | Description                                        |
| --------- | -------- | -------------------------------------------------- |
| `type`    | Yes      | `"prompt"` for LLM evaluation, `"agent"` for tools |
| `prompt`  | Yes      | Prompt text sent to LLM                            |
| `timeout` | No       | Seconds (default: 30 for prompt, 60 for agent)     |

### Response Schema

The LLM must respond with JSON:

```json
{
  "ok": true,
  "reason": "Explanation for the decision"
}
```

| Field    | Type    | Description                                    |
| -------- | ------- | ---------------------------------------------- |
| `ok`     | boolean | `true` allows the action, `false` prevents it  |
| `reason` | string  | Required when `ok` is `false`. Shown to Claude |

### $ARGUMENTS Placeholder

Use `$ARGUMENTS` in prompt to include hook input JSON. If omitted, input is appended to the prompt.

### Example: Intelligent Stop Hook

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working. Context: $ARGUMENTS\n\nAnalyze the conversation and determine if:\n1. All user-requested tasks are complete\n2. Any errors need to be addressed\n3. Follow-up work is needed\n\nRespond with JSON: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"your explanation\"} to continue working.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Example: SubagentStop Validation

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if this subagent should stop. Input: $ARGUMENTS\n\nCheck if:\n- The subagent completed its assigned task\n- Any errors occurred that need fixing\n- Additional context gathering is needed\n\nReturn: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"explanation\"} to continue."
          }
        ]
      }
    ]
  }
}
```

### Best Use Cases

| Event               | Use Case                              |
| ------------------- | ------------------------------------- |
| `Stop`              | Intelligent task completion detection |
| `SubagentStop`      | Verify subagent completed task        |
| `UserPromptSubmit`  | Context-aware prompt validation       |
| `PreToolUse`        | Complex permission decisions          |
| `PermissionRequest` | Intelligent allow/deny dialogs        |

### Comparison with Command Hooks

| Feature           | Command Hooks         | Prompt Hooks                   |
| ----------------- | --------------------- | ------------------------------ |
| Execution         | Runs bash script      | Queries LLM                    |
| Decision logic    | You implement in code | LLM evaluates context          |
| Setup complexity  | Requires script file  | Configure prompt only          |
| Context awareness | Limited to script     | Natural language understanding |
| Performance       | Fast (local)          | Slower (API call)              |
| Use case          | Deterministic rules   | Context-aware decisions        |

### Best Practices for Prompt Hooks

1. **Be specific in prompts** - Clearly state what you want the LLM to evaluate
2. **Include decision criteria** - List the factors the LLM should consider
3. **Test your prompts** - Verify the LLM makes correct decisions for your use cases
4. **Set appropriate timeouts** - Default is 30 seconds, adjust if needed
5. **Use for complex decisions** - Bash hooks are better for simple, deterministic rules

---

## Important Hook Events

### Setup Hook

Runs when Claude Code is invoked with repository setup and maintenance flags (`--init`, `--init-only`, or `--maintenance`).

**Use Setup hooks for**:

- One-time or occasional operations (dependency installation, migrations, cleanup)
- Operations you don't want on every session start

**Matchers**:

- `init` - Invoked from `--init` or `--init-only` flags
- `maintenance` - Invoked from `--maintenance` flag

**Key characteristics**:

- Requires explicit flags because running automatically would slow down every session start
- Has access to `CLAUDE_ENV_FILE` for persisting environment variables
- Output added to Claude's context

### SessionStart Hook

Runs when Claude Code starts a new session or resumes an existing session.

**Use SessionStart hooks for**:

- Loading development context (existing issues, recent changes)
- Setting up environment variables

**Important**: For one-time operations like installing dependencies or running migrations, use Setup hooks instead. SessionStart runs on every session, so keep these hooks fast.

**Matchers**:

- `startup` - New sessions
- `resume` - Resumed sessions (from `--resume`, `--continue`, or `/resume`)
- `clear` - After `/clear` command
- `compact` - After auto or manual compact

### PostToolUseFailure Hook

Runs immediately after a tool fails (returns an error). This complements PostToolUse, which only runs on successful tool execution.

**Use PostToolUseFailure hooks for**:

- Error recovery actions
- Logging tool failures
- Custom error handling and reporting

**Recognizes the same matcher values as PreToolUse and PostToolUse.**

### SubagentStart Hook

Runs when a Claude Code subagent (Task tool call) is spawned.

**Use SubagentStart hooks for**:

- Subagent initialization
- Logging subagent creation
- Context injection for specific agent types

**Input includes**:

- `agent_id`: Unique identifier for the subagent
- `agent_type`: Agent name (built-in like "Bash", "Explore", "Plan", or custom agent names)

---

## Environment Variables

| Variable             | Description                        | Available In        |
| -------------------- | ---------------------------------- | ------------------- |
| `CLAUDE_PROJECT_DIR` | Project root (absolute path)       | All hooks           |
| `CLAUDE_CODE_REMOTE` | `"true"` if remote, empty if local | All hooks           |
| `CLAUDE_ENV_FILE`    | Path for persisting env vars       | SessionStart, Setup |
| `CLAUDE_PLUGIN_ROOT` | Plugin directory (absolute)        | Plugin hooks        |

### SessionStart Environment Persistence

**Example: Setting individual environment variables**

```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export API_KEY=your-api-key' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

**Example: Persisting all environment changes (e.g., nvm use)**

```bash
#!/bin/bash
ENV_BEFORE=$(export -p | sort)

# Run setup commands that modify environment
source ~/.nvm/nvm.sh
nvm use 20

if [ -n "$CLAUDE_ENV_FILE" ]; then
  ENV_AFTER=$(export -p | sort)
  comm -13 <(echo "$ENV_BEFORE") <(echo "$ENV_AFTER") >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

Variables in `$CLAUDE_ENV_FILE` are sourced before each Bash command.

---

## Working with MCP Tools

Claude Code hooks work with Model Context Protocol (MCP) tools.

### MCP Tool Naming

MCP tools follow the pattern `mcp__<server>__<tool>`:

- `mcp__memory__create_entities` - Memory server's create entities tool
- `mcp__filesystem__read_file` - Filesystem server's read file tool
- `mcp__github__search_repositories` - GitHub server's search tool

### Configuring Hooks for MCP Tools

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

---

## Execution Details

| Aspect              | Behavior                                |
| ------------------- | --------------------------------------- |
| **Timeout**         | 60 seconds default, configurable        |
| **Parallelization** | All matching hooks run in parallel      |
| **Deduplication**   | Identical commands deduplicated         |
| **Environment**     | Runs in cwd with Claude Code's env      |
| **Hook order**      | Hooks from all sources execute together |

### Output Handling by Event

| Event                                   | stdout Handling                  |
| --------------------------------------- | -------------------------------- |
| UserPromptSubmit, SessionStart, Setup   | Added to Claude's context        |
| PreToolUse, PostToolUse, Stop           | Shown in verbose mode (Ctrl+O)   |
| Notification, SessionEnd, SubagentStart | Logged to debug only (`--debug`) |

---

## Security Considerations

### Disclaimer

**USE AT YOUR OWN RISK**: Claude Code hooks execute arbitrary shell commands on your system automatically. By using hooks, you acknowledge that:

- You are solely responsible for the commands you configure
- Hooks can modify, delete, or access any files your user account can access
- Malicious or poorly written hooks can cause data loss or system damage
- Anthropic provides no warranty and assumes no liability for any damages
- You should thoroughly test hooks in a safe environment before production use

### Security Best Practices

1. **Validate and sanitize inputs** - Never trust input data blindly
2. **Always quote shell variables** - Use `"$VAR"` not `$VAR`
3. **Block path traversal** - Check for `..` in file paths
4. **Use absolute paths via the $CLAUDE_PROJECT_DIR variable** - Specify full paths for scripts (use `$CLAUDE_PROJECT_DIR`)
5. **Skip sensitive files** - Avoid `.env`, `.git/`, keys, etc.

### Configuration Safety

Direct edits to hooks in settings files don't take effect immediately:

1. Hooks snapshot captured at startup
2. Snapshot used throughout the session
3. Warns if hooks are modified externally
4. Requires review in `/hooks` menu for changes to apply

This prevents malicious hook modifications from affecting your current session.

---

## Debugging

### Enable Debug Mode

```bash
claude --debug
claude --debug "hooks"  # Filter to hooks only
```

### Debug Output Example

```text
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Getting matching hook commands for PostToolUse with query: Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 60000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

### Basic Troubleshooting

1. **Check configuration** - Run `/hooks` to see if your hook is registered
2. **Verify syntax** - Ensure your JSON settings are valid
3. **Test commands** - Run hook commands manually first
4. **Check permissions** - Make sure scripts are executable
5. **Review logs** - Use `claude --debug` to see hook execution details
6. **Validate plugin hooks** - Use `claude plugin validate` or `/plugin validate` for plugin-level hooks

### Common Issues

| Problem              | Cause                            | Fix                                      |
| -------------------- | -------------------------------- | ---------------------------------------- |
| Hook not running     | Wrong matcher pattern            | Check case-sensitivity, regex            |
| Command not found    | Relative path                    | Use `$CLAUDE_PROJECT_DIR`                |
| JSON not processed   | Non-zero exit code               | Exit 0 for JSON processing               |
| Hook times out       | Slow script                      | Optimize or increase timeout             |
| Quotes breaking      | Unescaped in JSON                | Use `\"` inside JSON strings             |
| Plugin hook not load | Invalid plugin.json hooks config | Validate with `claude plugin validate .` |
| Path not found       | Missing `${CLAUDE_PLUGIN_ROOT}`  | Use variable for plugin scripts          |

### Validation Commands

**For plugin hooks**:

```bash
# CLI (from terminal)
claude plugin validate .
claude plugin validate ./path/to/plugin

# In Claude Code session
/plugin validate .
/plugin validate ./path/to/plugin
```

**For settings hooks**: JSON validation with:

```bash
python3 -m json.tool .claude/settings.json
```

### Test Commands Manually

```bash
echo '{"tool_name":"Write","tool_input":{"file_path":"test.txt"}}' | ./your-hook.sh
```

---

## Code Examples

### Python: Bash Command Validation (Exit Code)

```python
#!/usr/bin/env python3
import json
import re
import sys

# Define validation rules as (regex pattern, message) tuples
VALIDATION_RULES = [
    (
        r"\bgrep\b(?!.*\|)",
        "Use 'rg' (ripgrep) instead of 'grep' for better performance",
    ),
    (
        r"\bfind\s+\S+\s+-name\b",
        "Use 'rg --files -g pattern' instead of 'find -name'",
    ),
]

def validate_command(command: str) -> list[str]:
    issues = []
    for pattern, message in VALIDATION_RULES:
        if re.search(pattern, command):
            issues.append(message)
    return issues

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
command = tool_input.get("command", "")

if tool_name != "Bash" or not command:
    sys.exit(0)

issues = validate_command(command)

if issues:
    for message in issues:
        print(f"• {message}", file=sys.stderr)
    # Exit code 2 blocks tool call and shows stderr to Claude
    sys.exit(2)
```

### Python: UserPromptSubmit Context and Validation (JSON Output)

```python
#!/usr/bin/env python3
import json
import sys
import re
import datetime

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

prompt = input_data.get("prompt", "")

# Check for sensitive patterns
sensitive_patterns = [
    (r"(?i)\b(password|secret|key|token)\s*[:=]", "Prompt contains potential secrets"),
]

for pattern, message in sensitive_patterns:
    if re.search(pattern, prompt):
        # Use JSON output to block with a specific reason
        output = {
            "decision": "block",
            "reason": f"Security policy violation: {message}. Please rephrase without sensitive information."
        }
        print(json.dumps(output))
        sys.exit(0)

# Add current time to context
context = f"Current time: {datetime.datetime.now()}"
print(context)

# Equivalent JSON approach:
# print(json.dumps({
#   "hookSpecificOutput": {
#     "hookEventName": "UserPromptSubmit",
#     "additionalContext": context,
#   },
# }))

sys.exit(0)
```

### Python: PreToolUse Auto-Approval (JSON Output)

```python
#!/usr/bin/env python3
import json
import sys

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})

# Auto-approve file reads for documentation files
if tool_name == "Read":
    file_path = tool_input.get("file_path", "")
    if file_path.endswith((".md", ".mdx", ".txt", ".json")):
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": "Documentation file auto-approved"
            },
            "suppressOutput": True
        }
        print(json.dumps(output))
        sys.exit(0)

# Let normal permission flow proceed
sys.exit(0)
```

### Node.js: SessionStart Context Injection

```javascript
#!/usr/bin/env node

const output = {
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: `<project-context>
Environment: ${process.env.NODE_ENV || "development"}
Node version: ${process.version}
Working directory: ${process.cwd()}
</project-context>`,
  },
};

console.log(JSON.stringify(output));
```

---

## Examples

### Code Formatting (PostToolUse)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write \"$CLAUDE_PROJECT_DIR\"/**/*.{js,ts,json}"
          }
        ]
      }
    ]
  }
}
```

### File Protection (PreToolUse)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/check-protected-files.sh"
          }
        ]
      }
    ]
  }
}
```

### Custom Notifications

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/permission-alert.sh"
          }
        ]
      },
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/idle-notification.sh"
          }
        ]
      }
    ]
  }
}
```

### Task Verification (Stop)

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Verify task completion. Check edge cases. Return {\"ok\": true} or {\"ok\": false, \"reason\": \"...\"}."
          }
        ]
      }
    ]
  }
}
```

---

## Sources

- [Hooks Reference](https://code.claude.com/docs/en/hooks.md) (accessed 2026-01-28)
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md)
- [Settings Reference](https://code.claude.com/docs/en/settings.md)
- [Plugin Components Reference](https://code.claude.com/docs/en/plugins-reference.md#hooks)
