---
name: openai-agents
description: Build AI agents with OpenAI Agents SDK, tool registration, conversation history, and stateless execution. Use when creating AI agents, registering tools, or handling conversations.
---

# OpenAI Agents SDK Integration

## Agent Initialization
```python
from openai import OpenAI
from openai.agents import Agent, Runner

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

agent = Agent(
    name="TaskAssistant",
    instructions="""You are a helpful task management assistant.
Use the provided tools to help users manage their todo list.
Always confirm actions with friendly responses.
If a user's request is ambiguous, ask for clarification.""",
    model="gpt-4o",
    tools=[]  # MCP tools registered here
)
```

## Tool Registration (from MCP)
```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["user_id", "title"]
            }
        }
    }
]
agent.tools = tools
```

## Running Agent with History
```python
async def run_agent(messages: list[dict]) -> tuple[str, list[str]]:
    """Run agent with conversation history."""
    runner = Runner(agent=agent)
    result = await runner.run(messages=messages)
    
    # Extract response
    response = result.messages[-1].content[0].text.value
    
    # Extract tool calls
    tool_calls = [
        call.function.name 
        for msg in result.messages 
        if hasattr(msg, 'tool_calls') 
        for call in msg.tool_calls
    ]
    
    return response, tool_calls
```

## Message Format
```python
messages = [
    {"role": "user", "content": "Add a task"},
    {"role": "assistant", "content": "I've added the task"},
    {"role": "user", "content": "Show my tasks"}
]
```