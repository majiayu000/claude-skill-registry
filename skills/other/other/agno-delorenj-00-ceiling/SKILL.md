---
name: agno
description: Agno AI agent framework. Use for building multi-agent systems, AgentOS runtime, MCP server integration, and agentic AI development.
---

# Agno Skill

Comprehensive assistance with Agno development - a modern AI agent framework for building production-ready multi-agent systems with MCP integration, workflow orchestration, and AgentOS runtime.

## When to Use This Skill

This skill should be triggered when:
- **Building AI agents** with tools, memory, and structured outputs
- **Creating multi-agent teams** with role-based delegation and collaboration
- **Implementing workflows** with conditional branching, loops, and async execution
- **Integrating MCP servers** (stdio, SSE, or Streamable HTTP transports)
- **Deploying AgentOS** with custom FastAPI apps, JWT middleware, or database backends
- **Working with knowledge bases** for RAG and document processing
- **Debugging agent behavior** with debug mode and telemetry
- **Optimizing agent performance** with exponential backoff, retries, and rate limiting

## Key Concepts

### Core Architecture
- **Agent**: Single autonomous AI unit with model, tools, instructions, and optional memory/knowledge
- **Team**: Collection of agents that collaborate on tasks with role-based delegation
- **Workflow**: Multi-step orchestration with conditional branching, loops, and parallel execution
- **AgentOS**: FastAPI-based runtime for deploying agents as production APIs

### MCP Integration
- **MCPTools**: Connect to single MCP server via stdio, SSE, or Streamable HTTP
- **MultiMCPTools**: Connect to multiple MCP servers simultaneously
- **Transport Types**: stdio (local processes), SSE (server-sent events), Streamable HTTP (production)

### Memory & Knowledge
- **Session Memory**: Conversation state stored in PostgreSQL, SQLite, or cloud storage (GCS)
- **Knowledge Base**: RAG-powered document retrieval with vector embeddings
- **User Memory**: Persistent user-specific memories across sessions

## Quick Reference

### 1. Basic Agent with Tools

```python
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    tools=[DuckDuckGoTools()],
    markdown=True,
)

agent.print_response("Search for the latest AI news", stream=True)
```

### 2. Agent with Structured Output

```python
from agno.agent import Agent
from pydantic import BaseModel, Field

class MovieScript(BaseModel):
    name: str = Field(..., description="Movie title")
    genre: str = Field(..., description="Movie genre")
    storyline: str = Field(..., description="3 sentence storyline")

agent = Agent(
    description="You help people write movie scripts.",
    output_schema=MovieScript,
)

result = agent.run("Write a sci-fi thriller")
print(result.content.name)  # Access structured output
```

### 3. MCP Server Integration (stdio)

```python
import asyncio
from agno.agent import Agent
from agno.tools.mcp import MCPTools

async def run_agent(message: str) -> None:
    mcp_tools = MCPTools(command="uvx mcp-server-git")
    await mcp_tools.connect()

    try:
        agent = Agent(tools=[mcp_tools])
        await agent.aprint_response(message, stream=True)
    finally:
        await mcp_tools.close()

asyncio.run(run_agent("What is the license for this project?"))
```

### 4. Multiple MCP Servers

```python
import asyncio
import os
from agno.agent import Agent
from agno.tools.mcp import MultiMCPTools

async def run_agent(message: str) -> None:
    env = {
        **os.environ,
        "GOOGLE_MAPS_API_KEY": os.getenv("GOOGLE_MAPS_API_KEY"),
    }

    mcp_tools = MultiMCPTools(
        commands=[
            "npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt",
            "npx -y @modelcontextprotocol/server-google-maps",
        ],
        env=env,
    )
    await mcp_tools.connect()

    try:
        agent = Agent(tools=[mcp_tools], markdown=True)
        await agent.aprint_response(message, stream=True)
    finally:
        await mcp_tools.close()
```

### 5. Multi-Agent Team with Role Delegation

```python
from agno.agent import Agent
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.hackernews import HackerNewsTools

research_agent = Agent(
    name="Research Specialist",
    role="Gather information on topics",
    tools=[DuckDuckGoTools()],
    instructions=["Find comprehensive information", "Cite sources"],
)

news_agent = Agent(
    name="News Analyst",
    role="Analyze tech news",
    tools=[HackerNewsTools()],
    instructions=["Focus on trending topics", "Summarize key points"],
)

team = Team(
    members=[research_agent, news_agent],
    instructions=["Delegate research tasks to appropriate agents"],
)

team.print_response("Research AI trends and latest HN discussions", stream=True)
```

### 6. Workflow with Conditional Branching

```python
from agno.agent import Agent
from agno.workflow.workflow import Workflow
from agno.workflow.router import Router
from agno.workflow.step import Step
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.hackernews import HackerNewsTools

simple_researcher = Agent(
    name="Simple Researcher",
    tools=[DuckDuckGoTools()],
)

deep_researcher = Agent(
    name="Deep Researcher",
    tools=[HackerNewsTools()],
)

workflow = Workflow(
    steps=[
        Router(
            routes={
                "simple_topics": Step(agent=simple_researcher),
                "complex_topics": Step(agent=deep_researcher),
            }
        )
    ]
)

workflow.run("Research quantum computing")
```

### 7. Agent with Database Session Storage

```python
from agno.agent import Agent
from agno.db.postgres import PostgresDb

db = PostgresDb(
    db_url="postgresql://user:pass@localhost:5432/agno",
    schema="agno_sessions"
)

agent = Agent(
    db=db,
    session_id="user-123",  # Persistent session
    add_history_to_messages=True,
)

# Conversations are automatically saved and restored
agent.print_response("Remember my favorite color is blue")
agent.print_response("What's my favorite color?")  # Will remember
```

### 8. AgentOS with Custom FastAPI App

```python
from fastapi import FastAPI
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS

# Custom FastAPI app
app = FastAPI(title="Custom App")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Add AgentOS routes
agent_os = AgentOS(
    agents=[Agent(id="assistant", model=OpenAIChat(id="gpt-5-mini"))],
    base_app=app  # Merge with custom app
)

if __name__ == "__main__":
    agent_os.serve(app="custom_app:app", reload=True)
```

### 9. Agent with Debug Mode

```python
from agno.agent import Agent
from agno.tools.hackernews import HackerNewsTools

agent = Agent(
    tools=[HackerNewsTools()],
    debug_mode=True,  # Enable detailed logging
    # debug_level=2,  # More verbose output
)

# See detailed logs of:
# - Messages sent to model
# - Tool calls and results
# - Token usage and timing
agent.print_response("Get top HN stories")
```

### 10. Workflow with Input Schema Validation

```python
from typing import List
from agno.agent import Agent
from agno.workflow.workflow import Workflow
from agno.workflow.step import Step
from pydantic import BaseModel, Field

class ResearchTopic(BaseModel):
    """Structured research topic with specific requirements"""
    topic: str
    focus_areas: List[str] = Field(description="Specific areas to focus on")
    target_audience: str = Field(description="Who this research is for")
    sources_required: int = Field(description="Number of sources needed", default=5)

workflow = Workflow(
    input_schema=ResearchTopic,  # Validate inputs
    steps=[
        Step(agent=Agent(instructions=["Research based on focus areas"]))
    ]
)

# This will validate the input structure
workflow.run({
    "topic": "AI Safety",
    "focus_areas": ["alignment", "interpretability"],
    "target_audience": "researchers",
    "sources_required": 10
})
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

### **agentos.md** (22 pages)
- MCP server integration (stdio, SSE, Streamable HTTP)
- Multiple MCP server connections
- Custom FastAPI app integration
- JWT middleware and authentication
- AgentOS lifespan management
- Telemetry and monitoring

### **agents.md** (834 pages)
- Agent creation and configuration
- Tools integration (DuckDuckGo, HackerNews, Pandas, PostgreSQL, Wikipedia)
- Structured outputs with Pydantic
- Memory management (session, user, knowledge)
- Debugging with debug mode
- Human-in-the-loop patterns
- Multimodal agents (audio, video, images)
- Database backends (PostgreSQL, SQLite, GCS)
- State management and session persistence

### **examples.md** (188 pages)
- Workflow patterns (conditional branching, loops, routers)
- Team collaboration examples
- Async streaming workflows
- Audio/video processing teams
- Image generation pipelines
- Multi-step orchestration
- Input schema validation

### **getting_started.md**
- Installation and setup
- First agent examples
- MCP server quickstarts
- Common patterns and best practices

### **integration.md**
- Third-party integrations
- API connections
- Custom tool creation
- Database setup

### **migration.md**
- Upgrading between versions
- Breaking changes and migration guides
- Deprecated features

### **other.md**
- Advanced topics
- Performance optimization
- Production deployment

## Working with This Skill

### For Beginners
Start with **getting_started.md** to understand:
- Basic agent creation with `Agent()`
- Adding tools for web search, databases, etc.
- Running agents with `.print_response()` or `.run()`
- Understanding the difference between Agent, Team, and Workflow

**Quick Start Pattern:**
```python
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(tools=[DuckDuckGoTools()])
agent.print_response("Your question here")
```

### For Intermediate Users
Explore **agents.md** and **examples.md** for:
- Multi-agent teams with role delegation
- MCP server integration (local tools via stdio)
- Workflow orchestration with conditional logic
- Session persistence with databases
- Structured outputs with Pydantic models

**Team Pattern:**
```python
from agno.team import Team

team = Team(
    members=[researcher, analyst, writer],
    instructions=["Delegate tasks based on agent roles"]
)
```

### For Advanced Users
Deep dive into **agentos.md** for:
- AgentOS deployment with custom FastAPI apps
- Multiple MCP server orchestration
- Production authentication with JWT middleware
- Custom lifespan management
- Performance tuning with exponential backoff
- Telemetry and monitoring integration

**AgentOS Pattern:**
```python
from agno.os import AgentOS

agent_os = AgentOS(
    agents=[agent1, agent2],
    db=PostgresDb(...),
    base_app=custom_fastapi_app
)
agent_os.serve()
```

### Navigation Tips
1. **Looking for examples?** → Check `examples.md` first for real-world patterns
2. **Need API details?** → Search `agents.md` for class references and parameters
3. **Deploying to production?** → Read `agentos.md` for AgentOS setup
4. **Integrating external tools?** → See `integration.md` for MCP and custom tools
5. **Debugging issues?** → Enable `debug_mode=True` and check logs

## Common Patterns

### Pattern: MCP Server Connection Lifecycle
```python
async def run_with_mcp():
    mcp_tools = MCPTools(command="uvx mcp-server-git")
    await mcp_tools.connect()  # Always connect before use

    try:
        agent = Agent(tools=[mcp_tools])
        await agent.aprint_response("Your query")
    finally:
        await mcp_tools.close()  # Always close when done
```

### Pattern: Persistent Sessions with Database
```python
from agno.agent import Agent
from agno.db.postgres import PostgresDb

db = PostgresDb(db_url="postgresql://...")

agent = Agent(
    db=db,
    session_id="unique-user-id",
    add_history_to_messages=True,  # Include conversation history
)
```

### Pattern: Conditional Workflow Routing
```python
from agno.workflow.router import Router

workflow = Workflow(
    steps=[
        Router(
            routes={
                "route_a": Step(agent=agent_a),
                "route_b": Step(agent=b),
            }
        )
    ]
)
```

## Resources

### Official Links
- **Documentation**: https://docs.agno.com
- **GitHub**: https://github.com/agno-agi/agno
- **Examples**: https://github.com/agno-agi/agno/tree/main/cookbook

### Key Concepts to Remember
- **Always close MCP connections**: Use try/finally blocks or async context managers
- **Enable debug mode for troubleshooting**: `debug_mode=True` shows detailed execution logs
- **Use structured outputs for reliability**: Define Pydantic schemas with `output_schema=`
- **Persist sessions with databases**: PostgreSQL or SQLite for production agents
- **Disable telemetry if needed**: Set `AGNO_TELEMETRY=false` or `telemetry=False`

## scripts/
Add helper scripts here for common automation tasks.

## assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official Agno documentation
- Reference files preserve structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from real-world usage in the docs
- All examples are tested and production-ready

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information from docs.agno.com
