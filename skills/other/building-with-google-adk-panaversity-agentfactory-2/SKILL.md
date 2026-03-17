---
name: building-with-google-adk
description: Use when building AI agents with Google's Agent Development Kit (ADK). Triggers include creating ADK agents, Gemini-powered agents, multi-agent workflows, MCP integration with ADK, agent evaluation, workflow agents (Sequential/Parallel/Loop), Vertex AI deployment, or comparing OpenAI SDK with ADK. NOT when using other frameworks (OpenAI SDK, LangChain, CrewAI) or general LLM API calls.
---

# Building with Google ADK

Build production-grade AI agents using Google's Agent Development Kit.

## Quick Start

```bash
# Install ADK
pip install google-adk

# Or with uv (recommended)
uv add google-adk

# Create new agent project
adk create my_agent

# Run locally
adk run my_agent

# Web UI for debugging
adk web
```

---

## Environment Configuration

### Option A: Google AI Studio (Gemini API Key)

```bash
# .env
GOOGLE_API_KEY=your_gemini_api_key
```

### Option B: Vertex AI (Production)

```bash
# .env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=us-central1
```

```bash
# Authenticate with gcloud
gcloud auth application-default login
gcloud services enable aiplatform.googleapis.com
```

---

## Core Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        ADK Architecture                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   LlmAgent   │    │WorkflowAgent │    │  BaseAgent   │      │
│  │  (AI-driven) │    │(Deterministic)│   │   (Custom)   │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│         │                   │                   │               │
│         └──────────┬────────┴───────────────────┘               │
│                    ▼                                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                     Runner                               │   │
│  │  Orchestrates agent execution, handles events, state    │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│  ┌────────────────────────┴────────────────────────────────┐   │
│  │                  SessionService                          │   │
│  │  InMemory (dev) | Firestore | VertexAI (production)     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      Tools                                │  │
│  │  FunctionTool | google_search | McpToolset | AgentTool   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Agent Types

### 1. LlmAgent (AI-Driven Routing)

```python
from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="assistant",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant. Answer user questions.",
    description="Main assistant for general queries.",
    tools=[google_search]
)
```

### 2. SequentialAgent (Pipeline)

```python
from google.adk.agents import LlmAgent, SequentialAgent

researcher = LlmAgent(
    name="researcher",
    model="gemini-2.5-flash",
    instruction="Research the topic thoroughly.",
    tools=[google_search]
)

writer = LlmAgent(
    name="writer",
    model="gemini-2.5-flash",
    instruction="Write an article based on the research."
)

pipeline = SequentialAgent(
    name="content_pipeline",
    description="Research, then write.",
    sub_agents=[researcher, writer]
)
```

### 3. ParallelAgent (Concurrent Execution)

```python
from google.adk.agents import LlmAgent, ParallelAgent

fact_checker = LlmAgent(name="fact_checker", ...)
sentiment_analyzer = LlmAgent(name="sentiment", ...)

parallel_analysis = ParallelAgent(
    name="analysis",
    description="Run fact-checking and sentiment analysis in parallel.",
    sub_agents=[fact_checker, sentiment_analyzer]
)
```

### 4. LoopAgent (Iterative Refinement)

```python
from google.adk.agents import LlmAgent, LoopAgent
from google.adk.tools import exit_loop

solver = LlmAgent(
    name="solver",
    model="gemini-2.5-flash",
    instruction="Solve the problem. Call exit_loop when complete.",
    tools=[exit_loop]
)

iterative_solver = LoopAgent(
    name="iterative_solver",
    description="Iterate until solution found.",
    sub_agents=[solver],
    max_iterations=5
)
```

---

## Tools

### Function Tools (Custom Python Functions)

```python
from google.adk.tools import FunctionTool

def get_weather(city: str) -> dict:
    """Get weather for a city.

    Args:
        city: The city name to get weather for.

    Returns:
        Weather data including temperature and conditions.
    """
    # Implementation
    return {"city": city, "temp": "22°C", "condition": "Sunny"}

agent = Agent(
    name="weather_agent",
    model="gemini-2.5-flash",
    instruction="Provide weather information.",
    tools=[get_weather]  # ADK auto-wraps as FunctionTool
)
```

### Built-in Tools

```python
from google.adk.tools import google_search
from google.adk.code_executors import BuiltInCodeExecutor

agent = Agent(
    name="research_agent",
    model="gemini-2.0-flash",
    tools=[google_search],
    code_executor=BuiltInCodeExecutor()  # Enables code execution
)
```

### AgentTool (Agent as Tool)

```python
from google.adk.tools.agent_tool import AgentTool

search_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    tools=[google_search],
    instruction="You specialize in Google searches."
)

code_agent = Agent(
    name="code_agent",
    model="gemini-2.0-flash",
    code_executor=BuiltInCodeExecutor(),
    instruction="You specialize in code execution."
)

# Coordinator uses other agents as tools
root_agent = Agent(
    name="coordinator",
    model="gemini-2.0-flash",
    instruction="Delegate search tasks to search_agent, code to code_agent.",
    tools=[AgentTool(agent=search_agent), AgentTool(agent=code_agent)]
)
```

### MCP Integration

```python
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='filesystem_agent',
    instruction='Help users manage their files.',
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='npx',
                    args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
                )
            )
        )
    ]
)
```

---

## Running Agents

### Development: adk run

```bash
adk run my_agent  # Terminal chat
adk web           # Web UI with debugging
```

### Programmatic Execution

```python
from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

agent = Agent(
    name="assistant",
    model="gemini-2.5-flash",
    instruction="You are helpful."
)

runner = Runner(
    app_name="my_app",
    agent=agent,
    session_service=InMemorySessionService()
)

async def run():
    session = await runner.session_service.create_session(
        app_name="my_app",
        user_id="user123"
    )

    message = types.Content(
        role='user',
        parts=[types.Part(text="Hello!")]
    )

    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=message
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text)
```

### Simplified Debugging

```python
from google.adk.runners import InMemoryRunner

runner = InMemoryRunner(agent=agent)
await runner.run_debug("Hello!")  # Quick test
```

---

## Session & State Management

### State in Session

```python
# Access state in tool functions
from google.adk.tools.tool_context import ToolContext

def get_preference(tool_context: ToolContext) -> str:
    """Get user preference from session state."""
    return tool_context.state.get("preference", "default")

def set_preference(preference: str, tool_context: ToolContext) -> dict:
    """Set user preference in session state."""
    tool_context.state["preference"] = preference
    return {"status": "saved"}
```

### Production Session Services

```python
# Firestore for persistence
from google.adk.sessions import FirestoreSessionService

session_service = FirestoreSessionService(
    project="your-project",
    database="(default)"
)

# Vertex AI for managed deployment
from google.adk.sessions import VertexAiSessionService

session_service = VertexAiSessionService(
    project="your-project",
    location="us-central1"
)
```

---

## Guardrails & Callbacks

### Before Model Callback (Input Guardrail)

```python
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types
from typing import Optional

def block_keyword_guardrail(
    callback_context: CallbackContext,
    llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Block requests containing BLOCK keyword."""
    last_message = ""
    if llm_request.contents:
        for content in reversed(llm_request.contents):
            if content.role == 'user' and content.parts:
                last_message = content.parts[0].text or ""
                break

    if "BLOCK" in last_message.upper():
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="Request blocked by guardrail.")]
            )
        )
    return None  # Allow request to proceed

agent = Agent(
    name="guarded_agent",
    model="gemini-2.5-flash",
    instruction="You are helpful.",
    before_model_callback=block_keyword_guardrail
)
```

### Before Tool Callback (Tool Guardrail)

```python
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from typing import Optional, Dict, Any

def block_sensitive_city(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext
) -> Optional[Dict]:
    """Block weather requests for Paris."""
    if tool.name == "get_weather":
        city = args.get("city", "").lower()
        if city == "paris":
            return {
                "status": "error",
                "message": "Weather for Paris is restricted."
            }
    return None  # Allow tool execution

agent = Agent(
    name="weather_agent",
    model="gemini-2.5-flash",
    tools=[get_weather],
    before_tool_callback=block_sensitive_city
)
```

---

## Evaluation

### Create Test File (JSON)

```json
{
  "eval_set_id": "weather_agent_tests",
  "eval_cases": [
    {
      "eval_id": "basic_weather_request",
      "conversation": [
        {
          "user_content": {
            "parts": [{"text": "What's the weather in London?"}],
            "role": "user"
          },
          "final_response": {
            "parts": [{"text": "The weather in London is..."}],
            "role": "model"
          },
          "intermediate_data": {
            "tool_uses": [
              {"name": "get_weather", "args": {"city": "London"}}
            ]
          }
        }
      ],
      "session_input": {
        "app_name": "weather_agent",
        "user_id": "test_user"
      }
    }
  ]
}
```

### Run Evaluation

```bash
# CLI
adk eval ./agent.py ./tests/eval_set.test.json --print_detailed_results

# Pytest integration
pytest tests/integration/
```

```python
from google.adk.evaluation.agent_evaluator import AgentEvaluator

@pytest.mark.asyncio
async def test_weather_agent():
    await AgentEvaluator.evaluate(
        agent_module="weather_agent",
        eval_dataset_file_path_or_dir="tests/weather_tests.test.json"
    )
```

---

## Deployment

### Vertex AI Agent Engine

```bash
uv run adk deploy agent_engine \
  --project=your-project-id \
  --region=us-central1 \
  --staging_bucket="gs://your-bucket" \
  --display_name="My Agent" \
  ./my_agent
```

### Cloud Run

```bash
uv run adk deploy cloud_run \
  --project=your-project-id \
  --region=us-central1 \
  --service_name=my-agent-service \
  ./my_agent
```

### Python SDK Deployment

```python
from vertexai.preview import reasoning_engines
from vertexai import agent_engines
import vertexai

vertexai.init(
    project="your-project",
    location="us-central1",
    staging_bucket="gs://your-bucket"
)

adk_app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True
)

remote_app = agent_engines.create(
    agent_engine=adk_app,
    extra_packages=["./my_agent"],
    requirements=["google-cloud-aiplatform[adk,agent_engines]"]
)
```

---

## Decision Logic

| Scenario | Pattern | Why |
|----------|---------|-----|
| Simple Q&A | Single `Agent` | Minimal overhead |
| Research → Write → Edit | `SequentialAgent` | Clear pipeline |
| Parallel analysis | `ParallelAgent` | Faster execution |
| Iterative refinement | `LoopAgent` | Convergence-based |
| Specialized routing | `Agent` with `sub_agents` | LLM-driven delegation |
| Explicit tool routing | Multiple `AgentTool` | Coordinator pattern |
| MCP server connection | `McpToolset` | Standard protocol |
| Production persistence | `VertexAiSessionService` | Managed, scalable |

---

## TaskManager Example

```python
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from typing import List, Optional

# In-memory task storage
tasks: List[dict] = []

def add_task(title: str, description: Optional[str] = None) -> dict:
    """Add a new task."""
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "completed": False
    }
    tasks.append(task)
    return {"status": "created", "task": task}

def list_tasks() -> dict:
    """List all tasks."""
    return {"tasks": tasks}

def complete_task(task_id: int) -> dict:
    """Mark a task as completed."""
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return {"status": "completed", "task": task}
    return {"status": "error", "message": f"Task {task_id} not found"}

def delete_task(task_id: int) -> dict:
    """Delete a task."""
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return {"status": "deleted", "task_id": task_id}

root_agent = Agent(
    name="task_manager",
    model="gemini-2.5-flash",
    instruction="""You are a TaskManager assistant.

Help users manage their tasks:
- Add new tasks with add_task
- List all tasks with list_tasks
- Complete tasks with complete_task
- Delete tasks with delete_task

Always confirm actions and show current task list after changes.""",
    tools=[add_task, list_tasks, complete_task, delete_task]
)
```

---

## Common Pitfalls

| Issue | Symptom | Fix |
|-------|---------|-----|
| Auth not working | 403 errors | Check `GOOGLE_API_KEY` or Vertex AI setup |
| Tools not called | Agent ignores tools | Improve instruction clarity |
| State not persisting | Data lost between runs | Use `FirestoreSessionService` |
| MCP server not connecting | Tool discovery fails | Verify absolute paths, check npx |
| Slow first request | 5+ second delay | Pre-warm session service |
| Sub-agents not used | Delegation fails | Add clear `description` to sub-agents |

---

## Verification

Run: `python3 scripts/verify.py`

Expected: `✓ building-with-google-adk valid`

## If Verification Fails

1. Check: `.env` has valid `GOOGLE_API_KEY` or Vertex AI config
2. Check: Agent has required fields (`name`, `model`, `instruction`)
3. **Stop and report** if still failing

## References

- [references/api-patterns.md](references/api-patterns.md) - API signatures and patterns
- [references/deployment-patterns.md](references/deployment-patterns.md) - Production deployment
- [Official ADK Docs](https://google.github.io/adk-docs/)
