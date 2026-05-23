---
name: claude-agent-sdk
description: This skill should be used when building applications with the Claude Agent SDK (Python). Use for creating orchestrators with subagents, configuring agents programmatically, setting up hooks and permissions, and following SDK best practices. Trigger when implementing agentic workflows, multi-agent systems, or SDK-based automation.
---

# Claude Agent SDK

Build production-ready applications using the Claude Agent SDK for Python.

**SDK Version:** This skill targets `claude-agent-sdk>=0.1.6` (Python)

## Overview

This skill provides patterns, examples, and best practices for building SDK applications that orchestrate Claude agents.

## Quick Start

Copy the template and customize:

```bash
cp assets/sdk-template.py my-app.py
# Edit my-app.py - customize agents and workflow
chmod +x my-app.py
./my-app.py
```

The template includes proper uv script headers, agent definitions, and async patterns.

## Choosing Between query() and ClaudeSDKClient

The SDK provides two ways to interact with Claude: the `query()` function for simple one-shot tasks, and `ClaudeSDKClient` for continuous conversations.

### Quick Comparison

| Feature | `query()` | `ClaudeSDKClient` |
|---------|-----------|-------------------|
| **Conversation memory** | No - each call is independent | Yes - maintains context across queries |
| **Use case** | One-off tasks, single questions | Multi-turn conversations, complex workflows |
| **Complexity** | Simple - one function call | More setup - context manager pattern |
| **Hooks support** | No | Yes |
| **Custom tools** | No | Yes |
| **Interrupts** | No | Yes - can interrupt ongoing operations |
| **Session control** | New session each time | Single persistent session |

> **Important:** Hooks and custom tools (SDK MCP servers) are **only supported with `ClaudeSDKClient`**, not with `query()`. If you need hooks or custom tools, you must use `ClaudeSDKClient`.
>
> **Note on Async Runtimes:** The SDK works with both `asyncio` and `anyio`. The official SDK examples prefer `anyio.run()` for better async library compatibility, but `asyncio.run()` works equally well. Use whichever fits your project's async runtime.

### When to Use query()

Use `query()` for simple, independent tasks where you don't need conversation history:

```python
import anyio  # or: import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def analyze_file():
    """One-shot file analysis - no conversation needed."""
    options = ClaudeAgentOptions(
        system_prompt="You are a code analyzer",
        allowed_tools=["Read", "Grep", "Glob"],
        permission_mode="acceptEdits"
    )

    async for message in query(
        prompt="Analyze /path/to/file.py for bugs",
        options=options
    ):
        print(message)

anyio.run(analyze_file)  # or: asyncio.run(analyze_file())
```

**Best for:**

- Single analysis tasks
- Independent file operations
- Quick questions without follow-up
- Scripts that run once and exit

**Key limitation:** Each `query()` call creates a new session with no memory of previous calls.

### When to Use ClaudeSDKClient

Use `ClaudeSDKClient` when you need conversation context across multiple interactions:

```python
import anyio  # or: import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock

async def interactive_debugging():
    """Multi-turn debugging conversation with context."""
    options = ClaudeAgentOptions(
        system_prompt="You are a debugging assistant",
        allowed_tools=["Read", "Grep", "Bash"],
        permission_mode="acceptEdits"
    )

    async with ClaudeSDKClient(options=options) as client:
        # First query
        await client.query("Find all TODO comments in /path/to/project")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

        # Follow-up - Claude remembers the TODOs found above
        await client.query("Now prioritize them by complexity")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

        # Another follow-up - still in same conversation
        await client.query("Create a plan to address the top 3")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

anyio.run(interactive_debugging)  # or: asyncio.run(interactive_debugging())
```

**Best for:**

- Multi-turn conversations
- Interactive workflows
- Tasks requiring context from previous responses
- Applications with interrupt capability
- Orchestrators managing complex workflows

**Key advantage:** Claude remembers all previous queries and responses in the session.

**See:** `examples/streaming_mode.py` - Comprehensive ClaudeSDKClient examples with all patterns

### Advanced: Interrupts with ClaudeSDKClient

Only `ClaudeSDKClient` supports interrupting ongoing operations:

```python
import anyio  # or: import asyncio
from claude_agent_sdk import ClaudeSDKClient

async def interruptible_task():
    async with ClaudeSDKClient() as client:
        await client.query("Run a long analysis on /large/codebase")

        # Start processing in background
        async with anyio.create_task_group() as tg:
            tg.start_soon(process_messages, client)

            # Simulate user interrupt after 5 seconds
            await anyio.sleep(5)
            await client.interrupt()

async def process_messages(client):
    async for message in client.receive_response():
        print(message)

anyio.run(interruptible_task)  # or: asyncio.run(interruptible_task())
```

### Quick Decision Guide

**Use `query()` if:**

- Task is self-contained
- No follow-up questions needed
- Each execution is independent
- Simpler code is preferred

**Use `ClaudeSDKClient` if:**

- Need conversation memory
- Building interactive workflows
- Require interrupt capability
- Managing complex multi-step processes
- Working with orchestrators and subagents

## Core Patterns

### 1. Orchestrator with Subagents

Define a main orchestrator that delegates work to specialized subagents.

**Critical requirements:**

- Orchestrator must use `system_prompt={"type": "preset", "preset": "claude_code"}` (provides Task tool knowledge)
- Register agents programmatically via `agents={}` parameter (SDK best practice)
- Orchestrator must include `"Task"` in `allowed_tools`
- Match agent names exactly between definition and usage

**Example:**

```python
from claude_agent_sdk import AgentDefinition, ClaudeAgentOptions

options = ClaudeAgentOptions(
    system_prompt={"type": "preset", "preset": "claude_code"},  # REQUIRED for orchestrators
    allowed_tools=["Bash", "Task", "Read", "Write"],
    agents={
        "analyzer": AgentDefinition(
            description="Analyzes code structure and patterns",
            prompt="You are a code analyzer...",
            tools=["Read", "Grep", "Glob"],
            model="sonnet"
        ),
        "fixer": AgentDefinition(
            description="Fixes identified issues",
            prompt="You are a code fixer...",
            tools=["Read", "Edit", "Bash"],
            model="sonnet"
        )
    },
    permission_mode="acceptEdits",
    model="claude-sonnet-4-5"
)
```

**See:**

- `references/agent-patterns.md` - Complete agent definition patterns
- `examples/agents.py` - Official SDK agent examples with different agent types

### 2. System Prompt Configuration

Choose the appropriate system prompt pattern:

```python
# Orchestrator (use claude_code preset) - dict format (official examples prefer this)
system_prompt={"type": "preset", "preset": "claude_code"}

# Shorthand format (equivalent, but less explicit)
system_prompt="claude_code"

# Custom behavior
system_prompt="You are a Python expert..."

# Extend preset with additional instructions
system_prompt={
    "type": "preset",
    "preset": "claude_code",
    "append": "Additional domain-specific instructions"
}
```

**Note:** The shorthand `system_prompt="claude_code"` is equivalent to `{"type": "preset", "preset": "claude_code"}`. Both are valid. Official examples prefer the dict format for explicitness.

**See:**

- `references/system-prompts.md` - Complete system prompt documentation
- `examples/system_prompt.py` - Official SDK system prompt examples

### 3. Tool Restrictions

Limit subagent tools to minimum needed:

```python
# Read-only analyzer
tools=["Read", "Grep", "Glob"]

# Code modifier
tools=["Read", "Edit", "Bash"]

# Test runner
tools=["Bash", "Read"]
```

**See:** `references/agent-patterns.md` for common tool combinations

### 4. Hooks

Intercept SDK events to control behavior:

```python
from claude_agent_sdk import HookMatcher

options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="Bash", hooks=[check_bash_command])
        ],
        "PostToolUse": [
            HookMatcher(matcher="Bash", hooks=[review_output])
        ]
    }
)
```

**See:**

- `references/hooks-guide.md` - Complete hook patterns documentation
- `examples/hooks.py` - Official SDK hook examples with all hook types

### 5. Permission Callbacks

Fine-grained control over tool usage:

```python
async def permission_callback(tool_name, input_data, context):
    # Allow read operations
    if tool_name in ["Read", "Grep", "Glob"]:
        return PermissionResultAllow()

    # Block dangerous commands
    if tool_name == "Bash" and "rm -rf" in input_data.get("command", ""):
        return PermissionResultDeny(message="Dangerous command")

    return PermissionResultAllow()

options = ClaudeAgentOptions(
    can_use_tool=permission_callback,
    permission_mode="default"
)
```

**See:**

- `references/tool-permissions.md` - Complete permission patterns and decision guide
- `examples/tool_permission_callback.py` - Official SDK permission callback example

## Workflow Templates

### Building an Orchestrator

Follow these steps to build an effective orchestrator:

**1. Define agent purposes**

- What specialized tasks need delegation?
- What tools does each agent need?
- What constraints should apply?

**2. Create agent definitions**

```python
agents={
    "agent-name": AgentDefinition(
        description="When to use this agent",
        prompt="Agent's role and behavior",
        tools=["Tool1", "Tool2"],
        model="sonnet"
    )
}
```

**3. Configure orchestrator**

```python
options = ClaudeAgentOptions(
    system_prompt={"type": "preset", "preset": "claude_code"},  # CRITICAL
    allowed_tools=["Bash", "Task", "Read", "Write"],
    agents=agents,
    permission_mode="acceptEdits"
)
```

**4. Implement workflow**

```python
async with ClaudeSDKClient(options=options) as client:
    await client.query("Use 'agent-name' to perform task")

    async for message in client.receive_response():
        # Process responses
        pass
```

**See:** `examples/basic-orchestrator.py` for complete working example

### Loading Agents from Files

While programmatic registration is recommended, agent content can be stored in markdown files:

```python
import yaml

def load_agent_definition(path: str) -> AgentDefinition:
    """Load agent from markdown file with YAML frontmatter."""
    with open(path) as f:
        content = f.read()

    parts = content.split("---")
    frontmatter = yaml.safe_load(parts[1])
    prompt = parts[2].strip()

    # Parse tools (comma-separated string or array)
    tools = frontmatter.get("tools", [])
    if isinstance(tools, str):
        tools = [t.strip() for t in tools.split(",")]

    return AgentDefinition(
        description=frontmatter["description"],
        prompt=prompt,
        tools=tools,
        model=frontmatter.get("model", "inherit")
    )

# Load and register programmatically
agent = load_agent_definition(".claude/agents/my-agent.md")
options = ClaudeAgentOptions(agents={"my-agent": agent})
```

**See:** `references/agent-patterns.md` for complete loading pattern

## Common Anti-Patterns

Avoid these common mistakes:

**❌ Missing orchestrator system prompt**

```python
# Orchestrator won't know how to use Task tool
options = ClaudeAgentOptions(agents={...})
```

**✅ Correct orchestrator configuration**

```python
options = ClaudeAgentOptions(
    system_prompt="claude_code",
    agents={...}
)
```

**❌ Mismatched agent names**

```python
agents={"investigator": AgentDefinition(...)}
await client.query("Use 'markdown-investigator'...")  # Wrong name
```

**✅ Exact name matching**

```python
agents={"investigator": AgentDefinition(...)}
await client.query("Use 'investigator'...")  # Matches
```

**❌ Tool/prompt mismatch**

```python
system_prompt="Fix bugs you find"
allowed_tools=["Read", "Grep"]  # Can't fix, only read
```

**✅ Aligned tools and behavior**

```python
system_prompt="Analyze code for bugs"
allowed_tools=["Read", "Grep", "Glob"]
```

**See:** `references/best-practices.md` for complete anti-patterns list

## Resources

### references/

In-depth documentation loaded as needed:

- `api-reference.md` - Complete Python SDK API reference (types, functions, examples)
- `agent-patterns.md` - Agent definition patterns, tool restrictions, best practices
- `subagents.md` - Comprehensive subagent patterns and SDK integration
- `system-prompts.md` - System prompt configuration (preset, custom, append)
- `hooks-guide.md` - Hook patterns for all hook types with examples
- `tool-permissions.md` - Permission callback patterns and examples
- `best-practices.md` - SDK best practices, anti-patterns, debugging tips
- `custom-tools.md` - Creating custom tools with SDK MCP servers (Python-only)
- `sessions.md` - Session management and resumption patterns (Python-only)
- `skills.md` - Using Agent Skills with the SDK (Python-only)
- `slash-commands.md` - Slash commands and custom command creation (Python-only)

### examples/

Ready-to-run code examples from official SDK:

**Getting Started:**

- `quick_start.py` - Basic query() usage and message handling (start here!)
- `basic-orchestrator.py` - Complete orchestrator with analyzer and fixer subagents

**Core Patterns:**

- `agents.py` - Programmatic agent definitions with different agent types
- `hooks.py` - Comprehensive hook patterns (PreToolUse, PostToolUse, UserPromptSubmit, etc.)
- `system_prompt.py` - System prompt patterns (preset, custom, append)
- `streaming_mode.py` - Complete ClaudeSDKClient patterns with multi-turn conversations

**Advanced Features:**

- `mcp_calculator.py` - Custom tools with SDK MCP server (in-process tool server)
- `tool_permission_callback.py` - Permission callbacks with logging and control
- `setting_sources.py` - Settings isolation and loading (user/project/local)
- `plugin_example.py` - Using plugins with the SDK (relevant for plugin marketplace!)

### assets/

Templates and validation tools:

- `sdk-template.py` - Project template with uv script headers and agent structure
- `sdk-validation-checklist.md` - Comprehensive checklist for validating SDK applications against best practices

## When to Use This Skill

Use this skill when:

- Creating new Claude Agent SDK applications
- Building orchestrators with multiple subagents
- Implementing programmatic agent definitions
- Configuring hooks or permission callbacks
- Validating/reviewing SDK code (use `assets/sdk-validation-checklist.md`)
- Migrating from filesystem agent discovery to programmatic registration
- Debugging SDK applications (agent not found, Task tool not working)
- Following SDK best practices

Do not use for:

- Claude Code slash commands or skills (different system)
- Direct API usage without SDK
- Non-Python implementations (TypeScript SDK has different patterns)

## Next Steps

### For Beginners

1. Start with `examples/quick_start.py` - Learn basic query() usage
2. Try `assets/sdk-template.py` - Template for new projects
3. Review `examples/basic-orchestrator.py` - See orchestrator pattern

### For Intermediate Users

1. Explore core patterns:
   - `examples/agents.py` - Agent definitions
   - `examples/system_prompt.py` - System prompt patterns
   - `examples/streaming_mode.py` - Multi-turn conversations
   - `examples/hooks.py` - Hook patterns

### For Advanced Users

1. Study advanced features:
   - `examples/tool_permission_callback.py` - Permission control
   - `examples/mcp_calculator.py` - Custom tools
   - `examples/setting_sources.py` - Settings management
   - `examples/plugin_example.py` - Plugin integration

### Validation & Quality

1. Validate your code with `assets/sdk-validation-checklist.md`
2. Review against best practices in `references/best-practices.md`

### Reference Documentation

1. Consult `references/` as needed for detailed patterns
