---
name: claude-agent-sdk-python
description: >
  Expert guidance for building AI agents with the Claude Agent SDK in Python.
  Use when the user writes Python code with the SDK, imports claude_agent_sdk, uses query(),
  ClaudeSDKClient, ClaudeAgentOptions, AgentDefinition, creates custom @tool functions,
  sets up hooks, integrates MCP servers, manages sessions, or debugs SDK issues in Python.
  Also triggers on: "claude_agent_sdk", "ClaudeAgentOptions", "from claude_agent_sdk import",
  "pip install claude-agent-sdk", "asyncio.run", or "async for message in query".
---

# Claude Agent SDK — Python Guide

Production guidance for building AI agents with the Claude Agent SDK in Python.

> **Naming**: The Claude Code SDK was renamed to the Claude Agent SDK (v0.1.0+).
> Package: `pip install claude-agent-sdk` · Import: `from claude_agent_sdk import ...`

## Message Types

All message types for type checking and `isinstance()` checks:

```python
from claude_agent_sdk import (
    AssistantMessage,     # Claude's text/tool responses
    ResultMessage,        # Final result with subtype (success/error/cancelled)
    SystemMessage,        # System events (session_id, etc.)
    UserMessage,          # User prompts
    ToolUseMessage,       # Tool invocation requests
    ToolResultMessage,    # Tool execution results
)
```

## Quick Reference — Two Interaction Modes

### 1. `query()` — Stateless, One-Shot

Best for: independent tasks, automation scripts, CI pipelines.

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage

async def main():
    async for message in query(
        prompt="Review utils.py for bugs. Fix any issues you find.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"],
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")

asyncio.run(main())
```

### 2. `ClaudeSDKClient` — Stateful, Multi-Turn

Best for: conversations, follow-up questions, interactive apps.

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

async with ClaudeSDKClient(
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Bash"],
        permission_mode="acceptEdits",
    )
) as client:
    await client.query("Analyze the codebase structure")
    async for msg in client.receive_messages():
        print(msg)
    # Continue the conversation with context preserved
    await client.query("Now refactor the largest file you found")
    async for msg in client.receive_messages():
        print(msg)
```

## ClaudeAgentOptions — Complete Configuration

All options are optional. Key fields:

| Field | Type | Description |
|-------|------|-------------|
| `allowed_tools` | `list[str] \| None` | Tools Claude can use. See Built-in Tools below. |
| `disallowed_tools` | `list[str] \| None` | Explicitly block specific tools. |
| `permission_mode` | `"default" \| "acceptEdits" \| "bypassPermissions"` | Permission strategy. |
| `system_prompt` | `str \| dict \| None` | Custom instructions. Use `{"type": "preset", "preset": "claude_code"}` for CC default. |
| `model` | `str \| None` | e.g. `"sonnet"`, `"opus"`, `"haiku"`, or full model string. |
| `cwd` | `str \| Path \| None` | Working directory for the agent. |
| `max_turns` | `int \| None` | Maximum agentic loop iterations. |
| `setting_sources` | `list[Literal["user", "project"]] \| None` | `["user", "project"]` to load Skills/CLAUDE.md from filesystem. |
| `mcp_servers` | `dict \| None` | MCP server configurations. |
| `agents` | `dict[str, AgentDefinition] \| None` | Named subagent definitions. |
| `hooks` | `dict \| None` | Lifecycle hook callbacks. |

### Built-in Tools

Tool names for `allowed_tools`:

- **File ops**: `Read`, `Write`, `Edit`, `MultiEdit`
- **Search**: `Glob`, `Grep`
- **Execution**: `Bash`
- **Web**: `WebSearch`, `WebFetch`
- **Delegation**: `Task` (required for subagents)
- **Skills**: `Skill` (requires `setting_sources`)

## Custom Tools via SDK MCP Server

Define in-process tools without a separate MCP server process:

```python
from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeAgentOptions

@tool("search_orders", "Search orders by customer ID", {"customer_id": str, "status": str})
async def search_orders(args):
    results = await db.query_orders(args["customer_id"], args.get("status"))
    return {"content": [{"type": "text", "text": json.dumps(results)}]}

@tool("send_email", "Send an email notification", {"to": str, "subject": str, "body": str})
async def send_email(args):
    await email_service.send(args["to"], args["subject"], args["body"])
    return {"content": [{"type": "text", "text": f"Email sent to {args['to']}"}]}

server = create_sdk_mcp_server(name="business-tools", tools=[search_orders, send_email])

options = ClaudeAgentOptions(
    mcp_servers={"biz": server},
    allowed_tools=["mcp__biz__search_orders", "mcp__biz__send_email"],
)
```

**Tool naming convention**: MCP tools are accessed as `mcp__<server-name>__<tool-name>`.

## Subagents

Delegate specialized tasks to isolated agents with their own context and tool permissions:

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async for message in query(
    prompt="Review auth module for security issues, then write tests",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Grep", "Glob", "Task"],  # Task is required
        agents={
            "security-reviewer": AgentDefinition(
                description="Security specialist. Use for vulnerability analysis.",
                prompt="You are a security expert. Analyze code for OWASP Top 10...",
                tools=["Read", "Grep", "Glob"],
                model="opus",
            ),
            "test-writer": AgentDefinition(
                description="Test specialist. Use to generate test suites.",
                prompt="You are a testing expert. Write comprehensive unit tests...",
                tools=["Read", "Write", "Bash"],
                model="sonnet",
            ),
        },
    ),
):
    print(message)
```

**Factory pattern** for dynamic agents:

```python
def create_reviewer(language: str) -> AgentDefinition:
    return AgentDefinition(
        description=f"{language} code review specialist",
        prompt=f"You are an expert {language} developer...",
        tools=["Read", "Grep", "Glob"],
        model="opus" if language in ["rust", "c++"] else "sonnet",
    )
```

## Hooks — Lifecycle Callbacks

Available events: `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`.

```python
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher

async def block_dangerous_commands(input_data, tool_use_id, context):
    """Block destructive bash commands."""
    if input_data.get("tool_name") == "Bash":
        cmd = input_data.get("tool_input", {}).get("command", "")
        if any(danger in cmd for danger in ["rm -rf /", "DROP TABLE", "mkfs"]):
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"Blocked dangerous command: {cmd}",
                }
            }
    return {}

async def audit_log(input_data, tool_use_id, context):
    """Log all tool usage for auditing."""
    with open("audit.log", "a") as f:
        f.write(f"{input_data.get('tool_name')}: {input_data.get('tool_input')}\n")
    return {}

options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="Bash", hooks=[block_dangerous_commands]),
            HookMatcher(matcher=".*", hooks=[audit_log]),
        ]
    }
)
```

## MCP Integration (External Servers)

```python
options = ClaudeAgentOptions(
    mcp_servers={
        "github": {
            "type": "stdio",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")},
        },
        "postgres": {
            "type": "stdio",
            "command": "docker",
            "args": ["run", "mcp-postgres-server"],
            "env": {"DATABASE_URL": os.getenv("DATABASE_URL")},
        },
    },
    allowed_tools=["mcp__github", "mcp__postgres"],
)
```

You can mix SDK MCP servers (in-process) and external MCP servers in the same config.

## Using Skills in the SDK

Skills are filesystem-based and must be explicitly enabled:

```python
options = ClaudeAgentOptions(
    cwd="/path/to/project",
    setting_sources=["user", "project"],  # REQUIRED — loads Skills from filesystem
    allowed_tools=["Skill", "Read", "Write", "Bash"],
)
```

**Common mistake**: forgetting `setting_sources`. Without it, Skills won't be discovered even if `"Skill"` is in `allowed_tools`.

Skill locations:
- **Project**: `.claude/skills/*/SKILL.md` (shared via git)
- **User**: `~/.claude/skills/*/SKILL.md` (personal, cross-project)

Note: The `allowed-tools` field in SKILL.md frontmatter **only works in Claude Code CLI**, not in the SDK. Use `allowed_tools` in `ClaudeAgentOptions` to control tool access.

## Sessions and Conversation Management

```python
from claude_agent_sdk import query, ClaudeAgentOptions

session_id = None

# First interaction — capture session_id
async for message in query(
    prompt="Review this codebase and identify the top 3 issues",
    options=ClaudeAgentOptions(allowed_tools=["Read", "Glob", "Grep"]),
):
    if message.type == "system" and hasattr(message, "session_id"):
        session_id = message.session_id
    print(message)

# Resume with context
async for message in query(
    prompt="Now fix issue #1 that you found",
    options=ClaudeAgentOptions(
        session_id=session_id,
        allowed_tools=["Read", "Edit", "Bash"],
        permission_mode="acceptEdits",
    ),
):
    print(message)
```

## System Prompt Configuration

```python
# 1. Custom system prompt (v0.1.0+ default: minimal prompt)
options = ClaudeAgentOptions(system_prompt="You are a senior Python engineer...")

# 2. Claude Code's full system prompt (opt-in)
options = ClaudeAgentOptions(
    system_prompt={"type": "preset", "preset": "claude_code"}
)

# 3. No system prompt — SDK default (minimal)
options = ClaudeAgentOptions()  # uses minimal built-in prompt
```

**Breaking change in v0.1.0**: The SDK no longer loads Claude Code's system prompt by default. If you need the old behavior, explicitly set `preset: "claude_code"`.

## Authentication

```bash
# Direct API (default)
export ANTHROPIC_API_KEY=your-api-key

# Amazon Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
# + configure AWS credentials

# Google Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
# + configure GCP credentials

# Microsoft Azure AI Foundry
export CLAUDE_CODE_USE_FOUNDRY=1
# + configure Azure credentials
```

## Common Patterns

### Batch Processing (Parallel Agents)

```python
import asyncio

async def process_file(filepath: str):
    async for msg in query(
        prompt=f"Review {filepath} for security issues",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Grep"],
            max_turns=50,
        ),
    ):
        if isinstance(msg, ResultMessage):
            return msg.result

results = await asyncio.gather(
    process_file("auth.py"),
    process_file("payments.py"),
    process_file("users.py"),
)
```

### Structured Output Collection

```python
messages = []
async for msg in query(prompt="Analyze this codebase", options=options):
    messages.append(msg)

# Extract final result
result = next((m for m in reversed(messages) if hasattr(m, "result")), None)
```

### Error Handling

Available exception types:
- `CLINotFoundError` — Claude Code CLI binary not found in PATH
- `CLIConnectionError` — Failed to connect to CLI process
- Standard Python exceptions (e.g., `asyncio.TimeoutError`) may also be raised

```python
from claude_agent_sdk import CLINotFoundError, CLIConnectionError

try:
    async for msg in query(prompt="...", options=options):
        print(msg)
except CLINotFoundError:
    print("Claude Code CLI not found. Install: curl -fsSL https://claude.ai/install.sh | bash")
except CLIConnectionError as e:
    print(f"Connection error: {e}")
```

## Migration from Claude Code SDK (< v0.1.0)

Key changes:
1. `ClaudeCodeOptions` → `ClaudeAgentOptions`
2. System prompt no longer loads Claude Code's prompt by default
3. `setting_sources` must be explicitly set (was auto-loaded before)
4. Import path unchanged (`claude_agent_sdk`), but class names changed

## Best Practices

1. **Principle of least privilege**: Only grant tools the agent actually needs.
2. **Use `permission_mode="acceptEdits"` for automation**, `"default"` for interactive use.
3. **Prefer SDK MCP servers** over external ones for custom tools — less overhead, easier debugging.
4. **Use subagents for specialized tasks** — isolate context and apply the right model per task.
5. **Add hooks for safety** — block dangerous commands and audit tool usage in production.
6. **Set `max_turns`** to prevent runaway agents in production environments.
7. **Use `cwd`** to scope the agent to a specific directory.
8. **Capture `session_id`** from system messages if you need conversation continuity.

> For troubleshooting common issues, see `references/troubleshooting.md`.

## Official Resources

- Overview: https://platform.claude.com/docs/en/agent-sdk/overview
- Quickstart: https://platform.claude.com/docs/en/agent-sdk/quickstart
- Python reference: https://platform.claude.com/docs/en/agent-sdk/python
- Migration guide: https://platform.claude.com/docs/en/agent-sdk/migration-guide
- Python SDK repo: https://github.com/anthropics/claude-agent-sdk-python
- Demo agents: https://github.com/anthropics/claude-agent-sdk-demos
- Cookbook: https://platform.claude.com/cookbook
