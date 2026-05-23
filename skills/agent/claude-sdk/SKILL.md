---
name: Claude SDK Expert
description: Build autonomous AI agents using Claude Agent SDK with computer use, tool calling, MCP integration, and production best practices
version: 1.1.0
last_updated: 2026-01-06
external_version: "Claude Opus 4.5, Sonnet 4.5"
resources: resources/code-examples.py
---

# Claude SDK Expert Skill

## Purpose
Build autonomous AI agents using Claude Agent SDK, leveraging computer use, tool orchestration, and MCP integration for production deployments.

## SDK Overview

### Claude Agent SDK (2026)
Enables building autonomous agents that control computers, write files, run commands, and iterate on work.

**Core Philosophy:** Give Claude a computer to unlock agent effectiveness beyond chat.

## Key Capabilities

### 1. Computer Use
Claude can control a computer environment:
- File system operations (read, write, edit)
- Terminal command execution
- Iterative debugging and refinement
- Multi-step autonomous workflows

**Use Cases:** Finance agents, personal assistants, customer support, development agents, research agents

### 2. Built-in Tools

| Category | Tools |
|----------|-------|
| **Files** | Read, Write, Edit |
| **Commands** | Bash |
| **Search** | Grep, Glob |
| **Web** | WebFetch, WebSearch |

### 3. MCP Integration
Define custom tools via Model Context Protocol servers.

**Benefits:**
- Standardized tool interface
- Reusable across agents
- Enterprise data connectivity

**Popular MCP Servers:** GitHub, Slack, PostgreSQL, MongoDB, Stripe, Salesforce

## Architecture Patterns

### Pattern 1: Autonomous Task Completion
Agent completes multi-step task without intervention.
```
User Request → Analyze → Subtasks → Execute Tools → Iterate → Result
```

### Pattern 2: Human-in-the-Loop
Agent proposes actions, waits for approval.
```
Task → Plan → Human Review → Approve? → Execute → Result
```

### Pattern 3: Iterative Refinement
Agent retries on errors automatically.
```
Attempt 1 → Error → Analyze → Attempt 2 → Success
```

**See:** `resources/code-examples.py` for full implementations

## Tool Design Best Practices

### DO
- Provide tools relevant to the task
- Use clear, descriptive names
- Write detailed descriptions (Claude reads these!)
- Define strict input schemas
- Implement error handling
- Return structured outputs

### DON'T
- Give agents unnecessary tools
- Use ambiguous names ("handler", "processor")
- Skip input validation
- Return raw errors without context
- Hide side effects

**See:** `resources/code-examples.py` for good/bad tool examples

## MCP Integration

### Connecting MCP Servers
```python
mcp_config = {
    "servers": {
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")}
        }
    }
}
```

**Full example:** `resources/code-examples.py`

## Production Best Practices

### 1. Streaming
Show real-time progress to build user trust.

### 2. Error Handling
- Catch API errors, rate limits, tool failures
- Implement fallbacks and retries
- Log errors for debugging

### 3. Cost Optimization
- Use Haiku for simple tasks, Sonnet for complex
- Cache repetitive contexts
- Batch similar requests
- Monitor token usage

### 4. Security
- Restrict file/command access
- Sanitize dangerous inputs
- Audit all agent actions
- Validate tool outputs

**Implementation:** `resources/code-examples.py`

## Model Selection (January 2026)

| Model | Best For | Pricing (per M tokens) | Speed |
|-------|----------|------------------------|-------|
| **claude-opus-4-5** | Flagship reasoning, complex agents, highest accuracy | $5 in / $25 out | Slower |
| **claude-sonnet-4-5** | Best balance - coding, agents, computer use | $3 in / $15 out | Medium |
| **claude-haiku-4** | Simple tasks, format conversions, high-throughput | $0.25 in / $1.25 out | Fast |

**Note**: Opus 4.5 achieved 80.9% on SWE-bench Verified. Sonnet 4.5 supports 1M token context with beta header.

## Testing Agents

### Unit Testing
Test individual tools in isolation.

### Integration Testing
Test agent workflows with multiple tools.

### Evaluation Framework
Measure accuracy, latency, tool efficiency.

**Examples:** `resources/code-examples.py`

## Monitoring Metrics

| Metric | Description |
|--------|-------------|
| Tool Call Success Rate | % of tool invocations succeeding |
| Task Completion Rate | % of requests fully resolved |
| Average Iterations | Tool calls per task |
| Latency | Time to complete requests |
| Token Usage | Input + output tokens |
| Error Rate | % of requests with errors |

## Decision Framework

### Use Claude SDK when:
- Building on Anthropic models
- Need computer use capabilities
- Want production-ready agent framework
- Require MCP integration
- Building autonomous agents

### Consider alternatives when:
- Committed to OpenAI ecosystem → AgentKit
- Need visual agent builder → AgentKit
- Require complex state machines → LangGraph
- Want full OSS control → AutoGen/LangGraph

## Resources

**Documentation:**
- [Agent SDK Docs](https://docs.claude.com/en/api/agent-sdk)
- [Computer Use Guide](https://docs.anthropic.com/en/docs/agents/computer-use)
- [MCP Integration](https://modelcontextprotocol.io)

**GitHub:**
- [Python SDK](https://github.com/anthropics/claude-agent-sdk-python)
- [TypeScript SDK](https://github.com/anthropics/claude-agent-sdk-typescript)

## Key Principles

1. **Computer Use is Game-Changing** - Leverage file/bash capabilities fully
2. **Tools are First-Class** - Design tools as carefully as prompts
3. **MCP for Data** - Use MCP servers for enterprise connectivity
4. **Stream for UX** - Real-time feedback builds trust
5. **Security Always** - Validate inputs, restrict permissions, audit
6. **Right Model for Task** - Haiku for simple, Sonnet for complex

---

*Build powerful, autonomous agents using Claude's cutting-edge capabilities.*
