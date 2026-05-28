---
name: headless-cli-agents
description: Build agentic systems using Claude CLI in headless mode or the Claude Agent SDK. Use when building automation pipelines, CI/CD integrations, multi-agent orchestration, or programmatic Claude interactions. Covers CLI flags (-p, --output-format), session management (--resume, --continue), Python SDK (claude-agent-sdk), custom tools, and agent loop patterns.
---

# Headless CLI Agents

Build agentic systems using Claude Code CLI or the Claude Agent SDK.

## CLI Headless Mode

Use `-p` flag for non-interactive execution:

```bash
# Basic query
claude -p "Explain this code"

# With JSON output for parsing
claude -p "Create a REST API" --output-format json

# Streaming JSON for real-time output
claude -p "Build a CLI app" --output-format stream-json

# Restrict tools
claude -p "Stage changes" --allowedTools "Bash,Read" --permission-mode acceptEdits
```

### Output Formats

| Format | Flag | Use Case |
|--------|------|----------|
| Text | (default) | Simple scripts |
| JSON | `--output-format json` | Programmatic parsing |
| Stream JSON | `--output-format stream-json` | Real-time streaming |

JSON response includes: `session_id`, `total_cost_usd`, `duration_ms`, `num_turns`, `result`.

### Multi-Turn Sessions

```bash
# Get session ID
session_id=$(claude -p "Start review" --output-format json | jq -r '.session_id')

# Continue conversation
claude -p --resume "$session_id" "Now implement the plan"

# Or continue most recent
claude --continue "Add tests"
```

### Key Flags

| Flag | Purpose |
|------|---------|
| `-p, --print` | Non-interactive mode |
| `--output-format` | text/json/stream-json |
| `--resume, -r` | Resume by session ID |
| `--continue, -c` | Resume most recent |
| `--allowedTools` | Restrict available tools |
| `--disallowedTools` | Block specific tools |
| `--append-system-prompt` | Add custom instructions |
| `--mcp-config` | Load MCP servers from JSON |
| `--verbose` | Detailed logging |

## Python Agent SDK

```bash
pip install claude-agent-sdk
```

### Basic Usage

```python
import anyio
from claude_agent_sdk import query

async def main():
    async for message in query(prompt="What is 2 + 2?"):
        print(message)

anyio.run(main)
```

### Custom Tools (In-Process MCP)

```python
from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeSDKClient

@tool("greet", "Greet a user", {"name": str})
async def greet_user(args):
    return {"content": [{"type": "text", "text": f"Hello, {args['name']}!"}]}

server = create_sdk_mcp_server(name="my-tools", version="1.0.0", tools=[greet_user])
client = ClaudeSDKClient(mcp_servers=[server])
```

### ClaudeSDKClient Options

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

options = ClaudeAgentOptions(
    system_prompt="You are a helpful assistant",
    working_directory="/path/to/project",
    allowed_tools=["Bash", "Read", "Write"],
    permission_mode="acceptEdits"
)

client = ClaudeSDKClient(options=options)
```

## Agent Loop Pattern

Agents follow a core feedback loop:

1. **Gather Context** - Read files, search, web fetch
2. **Take Action** - Execute tools, generate code
3. **Verify Work** - Evaluate output, iterate if needed

### Subagents

Use subagents for parallel execution with isolated context. Each subagent has its own context window and returns only relevant data to parent.

### Best Practices

- Use JSON output for reliable parsing
- Check exit codes and stderr for errors
- Implement timeouts: `timeout 300 claude -p "$prompt"`
- Use session management for multi-step workflows
- Parse costs: `echo "$result" | jq -r '.total_cost_usd'`

## Integration Examples

### CI/CD Pipeline

```bash
#!/bin/bash
result=$(claude -p "Review PR diff for security issues" \
    --output-format json \
    --allowedTools "Read,Grep,WebSearch")

if echo "$result" | jq -e '.result | contains("vulnerability")' > /dev/null; then
    echo "Security issues found"
    exit 1
fi
```

### Multi-Step Workflow

```bash
# Step 1: Plan
plan_result=$(claude -p "Create implementation plan for: $TASK" --output-format json)
session_id=$(echo "$plan_result" | jq -r '.session_id')

# Step 2: Implement
claude -p --resume "$session_id" "Implement the plan"

# Step 3: Test
claude -p --resume "$session_id" "Write tests for the implementation"
```

### Rust CLI Integration

```rust
use std::process::Command;

async fn call_claude(prompt: &str) -> Result<String> {
    let output = Command::new("claude")
        .args(["-p", prompt, "--output-format", "json"])
        .output()?;

    let response: serde_json::Value = serde_json::from_slice(&output.stdout)?;
    Ok(response["result"].as_str().unwrap_or("").to_string())
}
```

## References

- [Headless Mode Docs](https://code.claude.com/docs/en/headless)
- [Agent SDK Overview](https://platform.claude.com/docs/en/api/agent-sdk/overview)
- [Claude Agent SDK Python](https://github.com/anthropics/claude-agent-sdk-python)
