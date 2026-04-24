---
name: claude-agent-sdk
description: Build AI agents using the Claude Agent SDK. Covers query functions,
  ClaudeSDKClient, custom tools, MCP servers, hooks, permissions, subagents, and
  browser control (Chrome extension, dev-browser skill). Use when creating
  agents, adding tools, configuring agent behavior, or automating browser tasks.
triggers:
  - claude agent sdk
  - agent sdk
  - build agent
  - create agent
  - claude sdk
  - ClaudeSDKClient
  - query function
  - custom tools
  - "@tool decorator"
  - mcp server
  - agent hooks
  - subagent
  - AgentDefinition
  - browser control
  - chrome extension
  - browser automation
  - dev browser
  - browserbase
---

<essential_principles>

## Claude Agent SDK Overview

The Claude Agent SDK gives agents the same tools that power Claude Code:
file operations, bash commands, web search, and more. Build autonomous agents
that read files, run commands, search the web, edit code, and verify their work.

### Two Ways to Query

| Function | Session | Best For |
|----------|---------|----------|
| `query()` | New each time | One-off tasks, automation |
| `ClaudeSDKClient` | Continuous | Conversations, follow-ups, hooks |

**Key Difference:** `query()` is simpler but doesn't support hooks, interrupts, or
custom tools. Use `ClaudeSDKClient` for advanced features.

### Agent Loop Pattern

Agents operate in a feedback loop:
```
gather context → take action → verify work → repeat
```

### Installation

**Python:**
```bash
uv add claude-agent-sdk
```

**TypeScript:**
```bash
npm install @anthropic-ai/claude-agent-sdk
```

**Requirements:**
- Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code`)
- `ANTHROPIC_API_KEY` environment variable set

### Quick Start

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Find and fix bugs in auth.py",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"])
    ):
        print(message)

asyncio.run(main())
```

</essential_principles>

<intake>

## What would you like to do?

1. **Create a new agent** - Build an agent from scratch
2. **Add custom tools** - Create tools with @tool decorator or MCP servers
3. **Add hooks** - Intercept tool calls for logging, validation, or modification
4. **Configure permissions** - Control what tools can do
5. **Create subagents** - Define specialized agents for parallel work
6. **Control browsers** - Chrome extension, dev-browser skill
7. **Get API reference** - Python or TypeScript SDK details

**Wait for response before proceeding.**

</intake>

<routing>

| Response | Load |
|----------|------|
| 1, "create", "new", "build" | `workflows/create-agent.md` |
| 2, "tools", "custom", "@tool" | `references/custom-tools.md` |
| 3, "hooks", "intercept" | `references/hooks.md` |
| 4, "permissions", "can_use_tool" | `references/permissions.md` |
| 5, "subagent", "parallel" | `references/subagents.md` |
| 6, "browser", "chrome", "automation" | `references/browser-control.md` |
| 7, "python", "reference" | `references/python-sdk.md` |
| 7, "typescript", "reference" | `references/typescript-sdk.md` |
| "built-in", "tools" | `references/built-in-tools.md` |
| "message", "types" | `references/message-types.md` |
| "best practices", "patterns" | `references/best-practices.md` |
| "error", "troubleshoot" | `references/troubleshooting.md` |

</routing>

<quick_reference>

## ClaudeAgentOptions (Key Fields)

```python
ClaudeAgentOptions(
    # Tools
    allowed_tools=["Read", "Write", "Bash"],  # Built-in tools to enable
    disallowed_tools=["WebSearch"],           # Tools to block

    # Prompts
    system_prompt="You are...",               # Custom system prompt
    # Or use preset: {"type": "preset", "preset": "claude_code", "append": "..."}

    # MCP Servers
    mcp_servers={"calc": my_server},          # MCP server configs

    # Permissions
    permission_mode="acceptEdits",            # default | acceptEdits | plan | bypassPermissions
    can_use_tool=my_handler,                  # Custom permission callback

    # Execution
    cwd="/path/to/project",                   # Working directory
    max_turns=10,                             # Limit iterations
    env={"API_KEY": "..."},                   # Environment variables

    # Advanced
    hooks={"PreToolUse": [...]},              # Behavior hooks
    agents={"researcher": AgentDef(...)},     # Subagents
    sandbox={"enabled": True},                # Sandbox settings
    setting_sources=["project"],              # Load .claude settings
)
```

## Built-in Tools

| Tool | Purpose |
|------|---------|
| **Read** | Read files (text, images, PDFs, notebooks) |
| **Write** | Create new files |
| **Edit** | Modify existing files with search/replace |
| **Bash** | Run terminal commands |
| **Glob** | Find files by pattern (`**/*.ts`) |
| **Grep** | Search file contents with regex |
| **WebSearch** | Search the web |
| **WebFetch** | Fetch and parse web pages |
| **Task** | Spawn subagents |
| **NotebookEdit** | Edit Jupyter notebooks |
| **TodoWrite** | Manage task lists |
| **KillShell** | Kill background shells |
| **ExitPlanMode** | Exit planning mode |

## Message Types

```python
# All messages
Message = UserMessage | AssistantMessage | SystemMessage | ResultMessage

# Content blocks in AssistantMessage
ContentBlock = TextBlock | ThinkingBlock | ToolUseBlock | ToolResultBlock
```

## Error Types

```python
from claude_agent_sdk import (
    CLINotFoundError,      # Claude Code CLI not installed
    CLIConnectionError,    # Connection failed
    ProcessError,          # CLI process failed
    CLIJSONDecodeError,    # JSON parsing failed
)
```

</quick_reference>

<thinking_config>

## Thinking & Effort Configuration

Control agent thinking depth via the effort parameter rather than prompt-level instructions like "think carefully":

| Use Case | Effort | Notes |
|----------|--------|-------|
| Quick lookups, simple edits | low | Minimal thinking overhead |
| Standard development | medium | Default for most agents |
| Complex architecture, security | high | Deeper reasoning |
| Deep research, long-horizon | max | Maximum thinking budget |

```python
# Adaptive thinking (recommended for Claude 4.6)
options = ClaudeAgentOptions(
    model="claude-opus-4-6",  # or claude-sonnet-4-6
    # Effort is controlled at the API level, not in the agent options
)
```

Avoid adding "think carefully" or "be thorough" to agent system prompts—Claude 4.6 calibrates thinking depth automatically based on task complexity.

</thinking_config>

<examples>

## Common Patterns

### File Operations Agent
```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Write", "Edit", "Glob", "Grep"],
    permission_mode="acceptEdits",
    cwd="/path/to/project"
)
```

### Code Review Agent
```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep"],  # Read-only
    system_prompt="Review code for bugs, security issues, and style"
)
```

### Research Agent
```python
options = ClaudeAgentOptions(
    allowed_tools=["WebSearch", "WebFetch", "Write"],
    max_turns=20  # Allow more iterations for research
)
```

### Interactive Chat with Tools
```python
async with ClaudeSDKClient(options) as client:
    await client.query("What files are in this directory?")
    async for msg in client.receive_response():
        print(msg)

    # Follow-up - Claude remembers context
    await client.query("Show me the largest one")
    async for msg in client.receive_response():
        print(msg)
```

</examples>
