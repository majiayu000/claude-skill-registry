---
name: Claude SDK Expert
description: Build autonomous AI agents using Claude Agent SDK with computer use, tool calling, MCP integration, and production best practices for Anthropic models
version: 1.0.0
---

# Claude SDK Expert Skill

## Purpose
This skill provides comprehensive guidance on building autonomous AI agents using the Claude Agent SDK (formerly Claude Code SDK), leveraging computer use capabilities, tool orchestration, and MCP integration for production deployments.

## SDK Overview

### Claude Agent SDK (2025)
The Claude Agent SDK enables building autonomous agents that can interact with computers, write files, run commands, and iterate on their work.

**Evolution:** Renamed from "Claude Code SDK" to reflect broader capabilities beyond coding.

**Core Philosophy:** Give Claude a computer to unlock agent effectiveness beyond chat-based interactions.

## Key Capabilities

### 1. Computer Use
**Revolutionary Feature:** Claude can control a computer environment to complete tasks.

**What This Enables:**
- File system operations (read, write, edit)
- Terminal command execution
- Iterative debugging and refinement
- Multi-step autonomous workflows
- Real-world task completion

**Use Cases:**
- Finance agents analyzing portfolios
- Personal assistants booking travel
- Customer support handling complex requests
- Development agents building software
- Research agents gathering and analyzing data

### 2. Built-in Tools

**File Operations:**
- `Read` - Read file contents
- `Write` - Create or overwrite files
- `Edit` - Make targeted edits to existing files

**Command Execution:**
- `Bash` - Run shell commands and scripts

**Search & Discovery:**
- `Grep` - Search file contents with regex
- `Glob` - Find files by pattern

**Web Access:**
- `WebFetch` - Retrieve and analyze web pages
- `WebSearch` - Search the internet for information

**All tools are production-tested and optimized for agent use.**

### 3. MCP Integration
**Model Context Protocol Support:** Define custom tools via MCP servers.

**Benefits:**
- Standardized tool interface
- Reusable across different agents
- Community ecosystem of MCP servers
- Enterprise data source connectivity

**Example MCP Servers:**
- GitHub, Slack, Google Drive
- PostgreSQL, MongoDB
- Stripe, Salesforce
- Custom internal APIs

## Architecture Patterns

### Pattern 1: Autonomous Task Completion
**Scenario:** Agent completes multi-step task without human intervention

**Flow:**
```
User Request
    ↓
Claude analyzes task
    ↓
Breaks into subtasks
    ↓
Executes via tools (Read, Bash, Write, etc.)
    ↓
Iterates on failures
    ↓
Returns result
```

**Example:**
```python
from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    tools=[
        {"type": "computer_use"},
        {"type": "bash"},
        {"type": "file_operations"}
    ],
    messages=[{
        "role": "user",
        "content": "Analyze the last 30 days of sales data and create a summary report"
    }]
)

# Claude autonomously:
# 1. Reads sales data files
# 2. Runs analysis scripts
# 3. Generates report
# 4. Saves to file
```

### Pattern 2: Human-in-the-Loop Approval
**Scenario:** Agent proposes actions, waits for approval before executing

**Flow:**
```
Task → Plan → Show to Human → Approve? → Execute → Result
                                ↓ No
                            Revise Plan
```

**Implementation:**
```python
# Step 1: Generate plan
plan_response = client.messages.create(
    model="claude-sonnet-4-5",
    messages=[{
        "role": "user",
        "content": "Create a plan to refactor the authentication system"
    }]
)

# Step 2: Human reviews plan
if human_approves(plan_response.content):
    # Step 3: Execute with tools
    execution_response = client.messages.create(
        model="claude-sonnet-4-5",
        tools=all_tools,
        messages=[{
            "role": "user",
            "content": f"Execute this plan: {plan_response.content}"
        }]
    )
```

### Pattern 3: Iterative Refinement
**Scenario:** Agent iterates on work based on feedback/errors

**Flow:**
```
Attempt 1 → Error → Analyze → Attempt 2 → Error → Analyze → Attempt 3 → Success
```

**Built-in:** Claude SDK naturally supports this through computer use - agents can see command outputs and adjust.

## Tool Design Best Practices

### Custom Tool Creation

**Good Tool Design:**
```python
# Clear, focused tool
{
    "name": "get_customer_orders",
    "description": "Retrieve all orders for a specific customer ID",
    "input_schema": {
        "type": "object",
        "properties": {
            "customer_id": {
                "type": "string",
                "description": "The unique customer identifier"
            },
            "since_date": {
                "type": "string",
                "description": "ISO date to filter orders from (optional)"
            }
        },
        "required": ["customer_id"]
    }
}
```

**Poor Tool Design:**
```python
# Too broad, unclear purpose
{
    "name": "do_customer_stuff",
    "description": "Does various things with customers",
    "input_schema": {
        "type": "object",
        "properties": {
            "action": {"type": "string"},
            "data": {"type": "object"}
        }
    }
}
```

### Tool Selection Principles

**DO:**
✅ Provide tools relevant to the task
✅ Use clear, descriptive names
✅ Write detailed descriptions (Claude reads these!)
✅ Define strict input schemas
✅ Implement error handling in tools
✅ Return structured, parseable outputs

**DON'T:**
❌ Give agents tools they don't need (increases confusion)
❌ Use ambiguous names like "handler" or "processor"
❌ Skip input validation
❌ Return raw error messages without context
❌ Make tools with side effects unclear

## MCP Integration Patterns

### Connecting MCP Servers

```python
# Define MCP server connection
mcp_config = {
    "servers": {
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {
                "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")
            }
        },
        "postgres": {
            "command": "docker",
            "args": ["run", "mcp-postgres-server"],
            "env": {
                "DATABASE_URL": os.getenv("DATABASE_URL")
            }
        }
    }
}

# Claude automatically discovers tools from MCP servers
response = client.messages.create(
    model="claude-sonnet-4-5",
    mcp_servers=mcp_config,
    messages=[{
        "role": "user",
        "content": "Find all GitHub issues assigned to me and update the project database"
    }]
)
# Claude uses both github and postgres MCP tools
```

### Custom MCP Server
```python
# Create custom MCP server for internal API
from mcp import Server, Tool

server = Server("internal-crm")

@server.tool()
def get_customer_data(customer_id: str):
    """Retrieve customer information from internal CRM"""
    return crm_api.get_customer(customer_id)

@server.tool()
def update_customer_notes(customer_id: str, notes: str):
    """Add notes to customer record"""
    return crm_api.update(customer_id, {"notes": notes})

# Deploy and connect to Claude
```

## Production Best Practices

### 1. Streaming for UX

**Why:** Show user progress in real-time, build trust in agent actions

```python
with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    tools=tools,
    messages=messages
) as stream:
    for event in stream:
        if event.type == "content_block_delta":
            print(event.delta.text, end="", flush=True)
        elif event.type == "tool_use":
            print(f"\nUsing tool: {event.name}")
```

### 2. Error Handling

**Robust Error Management:**
```python
try:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        tools=tools,
        messages=messages
    )
except anthropic.APIError as e:
    # Handle API errors
    log_error(f"API Error: {e}")
    return fallback_response()
except anthropic.RateLimitError:
    # Handle rate limits
    time.sleep(60)
    retry()
except Exception as e:
    # Handle tool execution errors
    log_error(f"Tool Error: {e}")
    return safe_error_message()
```

### 3. Cost Optimization

**Strategies:**
- Use Claude Haiku for simple tasks, Sonnet for complex reasoning
- Implement caching for repetitive contexts
- Batch similar requests when possible
- Limit max_tokens appropriately
- Monitor token usage via callbacks

```python
# Use appropriate model for task
simple_task_response = client.messages.create(
    model="claude-haiku-4",  # Cheaper, faster
    messages=[{"role": "user", "content": "Format this JSON"}]
)

complex_task_response = client.messages.create(
    model="claude-sonnet-4-5",  # More capable
    messages=[{"role": "user", "content": "Analyze architectural trade-offs"}]
)
```

### 4. Security

**Critical Security Measures:**

**Tool Permissions:**
```python
# Restrict file access
safe_file_tools = {
    "read": {
        "allowed_paths": ["/data/public"],
        "denied_paths": ["/etc", "/secrets"]
    },
    "write": {
        "allowed_paths": ["/output"],
        "denied_paths": ["/"]
    }
}
```

**Input Sanitization:**
```python
def sanitize_bash_command(cmd: str) -> str:
    """Prevent dangerous commands"""
    dangerous = ["rm -rf", ":(){ :|:& };:", "dd if="]
    for danger in dangerous:
        if danger in cmd:
            raise SecurityError(f"Dangerous command blocked: {danger}")
    return cmd
```

**Audit Logging:**
```python
def log_agent_action(action: dict):
    """Track all agent actions for security audit"""
    audit_log.write({
        "timestamp": datetime.now(),
        "tool": action["tool_name"],
        "input": action["input"],
        "user": action["user_id"],
        "result": action["result"]
    })
```

## Performance Optimization

### Parallel Tool Calls
Claude can use multiple tools simultaneously when appropriate:

```python
# Claude automatically parallelizes when possible
response = client.messages.create(
    model="claude-sonnet-4-5",
    tools=[weather_api, stock_api, news_api],
    messages=[{
        "role": "user",
        "content": "Give me weather, stock prices, and news for San Francisco"
    }]
)
# Claude calls all 3 APIs in parallel
```

### Caching Strategies
```python
# Cache system prompts and large contexts
response = client.messages.create(
    model="claude-sonnet-4-5",
    system=[{
        "type": "text",
        "text": large_system_prompt,
        "cache_control": {"type": "ephemeral"}
    }],
    messages=messages
)
# System prompt cached for ~5 minutes
```

## Testing Agents

### Unit Testing Tools
```python
def test_customer_lookup_tool():
    """Test individual tool behavior"""
    result = get_customer_orders("CUST123")
    assert result["customer_id"] == "CUST123"
    assert isinstance(result["orders"], list)
```

### Integration Testing
```python
def test_agent_workflow():
    """Test agent using multiple tools"""
    response = client.messages.create(
        model="claude-sonnet-4-5",
        tools=[tool1, tool2, tool3],
        messages=[{
            "role": "user",
            "content": "Process order #12345"
        }]
    )

    # Verify expected tool usage
    tool_calls = extract_tool_calls(response)
    assert "verify_order" in tool_calls
    assert "process_payment" in tool_calls
```

### Evaluation Framework
```python
# Use Claude's built-in evaluation
from anthropic import Anthropic

eval_client = Anthropic()

eval_results = eval_client.evaluate(
    agent=my_agent,
    test_cases=[
        {"input": "...", "expected_output": "..."},
        # More test cases
    ],
    metrics=["accuracy", "latency", "tool_efficiency"]
)
```

## Common Patterns

### Pattern: Multi-Step Research
```python
async def research_agent(query: str):
    """Agent researches topic using multiple sources"""
    response = await client.messages.create(
        model="claude-sonnet-4-5",
        tools=[web_search, web_fetch, summarize],
        messages=[{
            "role": "user",
            "content": f"Research '{query}' and provide comprehensive summary"
        }]
    )
    # Claude: searches → fetches articles → summarizes → synthesizes
    return response.content
```

### Pattern: Code Generation & Testing
```python
def code_agent(requirements: str):
    """Agent writes and tests code"""
    response = client.messages.create(
        model="claude-sonnet-4-5",
        tools=[write_file, bash, read_file],
        messages=[{
            "role": "user",
            "content": f"Write and test code for: {requirements}"
        }]
    )
    # Claude: writes code → saves file → runs tests → fixes errors → retries
    return response.content
```

### Pattern: Data Pipeline
```python
def data_pipeline_agent(source: str, destination: str):
    """Agent ETL pipeline"""
    response = client.messages.create(
        model="claude-sonnet-4-5",
        tools=[read_file, bash, postgres_insert],
        messages=[{
            "role": "user",
            "content": f"Extract data from {source}, transform it, and load to {destination}"
        }]
    )
    # Claude orchestrates full ETL
    return response.content
```

## Model Selection

### Claude Sonnet 4.5 (claude-sonnet-4-5)
**Best For:**
- Complex reasoning and analysis
- Multi-step autonomous tasks
- Code generation and debugging
- Research and synthesis
- High-stakes decisions

**Characteristics:**
- Highest capability
- Best for computer use
- More expensive
- Slower than Haiku

### Claude Haiku 4 (claude-haiku-4)
**Best For:**
- Simple, well-defined tasks
- Format conversions
- Quick classifications
- High-throughput scenarios
- Cost-sensitive applications

**Characteristics:**
- Fast responses
- Lower cost
- Good for structured tasks
- Limited complex reasoning

## Integration Examples

### With FastAPI
```python
from fastapi import FastAPI
from anthropic import Anthropic

app = FastAPI()
client = Anthropic()

@app.post("/agent/task")
async def run_agent_task(task: dict):
    response = client.messages.create(
        model="claude-sonnet-4-5",
        tools=load_tools_for_task(task),
        messages=[{
            "role": "user",
            "content": task["description"]
        }]
    )
    return {"result": response.content}
```

### With LangChain (via LangChain-Anthropic)
```python
from langchain_anthropic import ChatAnthropic
from langchain.agents import initialize_agent

llm = ChatAnthropic(model="claude-sonnet-4-5")
agent = initialize_agent(
    tools=[tool1, tool2],
    llm=llm,
    agent_type="structured-chat-zero-shot-react-description"
)
result = agent.run("Complete this task")
```

## Monitoring & Observability

### Key Metrics
- **Tool Call Success Rate** - % of tool invocations that succeed
- **Task Completion Rate** - % of user requests fully resolved
- **Average Iterations** - How many tool calls per task
- **Latency** - Time to complete requests
- **Token Usage** - Input + output tokens per request
- **Error Rate** - % of requests with errors

### Logging Best Practices
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("claude-agent")

def run_agent_with_logging(task):
    logger.info(f"Starting task: {task}")

    response = client.messages.create(
        model="claude-sonnet-4-5",
        tools=tools,
        messages=[{"role": "user", "content": task}]
    )

    logger.info(f"Tools used: {extract_tools(response)}")
    logger.info(f"Token usage: {response.usage}")

    return response
```

## Decision Framework

**Use Claude SDK when:**
- Building on Anthropic models (Claude family)
- Need computer use capabilities (file, bash, iteration)
- Want production-ready agent framework
- Require MCP integration for data sources
- Building autonomous task completion agents

**Consider alternatives when:**
- Committed to OpenAI ecosystem (use AgentKit)
- Need visual agent builder (use AgentKit)
- Require complex state machines (use LangGraph)
- Want full OSS control (use AutoGen/LangGraph)

## Resources

**Official Documentation:**
- Agent SDK Docs: https://docs.claude.com/en/api/agent-sdk
- Computer Use Guide: https://docs.anthropic.com/en/docs/agents/computer-use
- MCP Integration: https://modelcontextprotocol.io

**GitHub:**
- Python SDK: https://github.com/anthropics/claude-agent-sdk-python
- TypeScript SDK: https://github.com/anthropics/claude-agent-sdk-typescript

## Final Principles

1. **Computer Use is Game-Changing** - Leverage file/bash capabilities fully
2. **Tools are First-Class** - Design tools as carefully as prompts
3. **MCP for Data** - Use MCP servers for enterprise data connectivity
4. **Stream for UX** - Real-time feedback builds user trust
5. **Security Always** - Validate inputs, restrict permissions, audit actions
6. **Right Model for Task** - Haiku for simple, Sonnet for complex

---

*This skill ensures you build powerful, autonomous agents using Claude's cutting-edge capabilities in 2025.*
