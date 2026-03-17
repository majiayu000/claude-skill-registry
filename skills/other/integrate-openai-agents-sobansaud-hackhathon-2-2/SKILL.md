---
name: integrate-openai-agents
description: This skill should be used when integrating OpenAI Agents SDK with FastAPI, building message arrays from database history, running agents with MCP tools, parsing tool calls, executing them, and saving conversations to the database.
---

# Integrate OpenAI Agents Skill

This skill provides guidance for integrating OpenAI Agents SDK with FastAPI for chatbot functionality.

## Purpose

Build a stateless chat endpoint that:
1. Loads conversation history from the database
2. Runs an OpenAI agent with MCP tools
3. Parses and executes tool calls
4. Returns agent responses
5. Saves the full conversation to the database

## When to Use

Use this skill when:
- Setting up the main chat API endpoint
- Integrating OpenAI Agents SDK with MCP tools
- Implementing conversation flow between user, agent, and tools
- Building chatbot backend infrastructure

## Capabilities

- **Agents SDK Integration**: Use OpenAI Agents Python SDK for agent execution
- **Message History**: Build message arrays from database conversation records
- **Tool Execution**: Parse tool calls from agent and execute via MCP
- **Conversation Persistence**: Save all messages to database after each interaction
- **Stateless Design**: Each request is independent, conversation_id links history

## Architecture

```
/api/{user_id}/chat
├── Load conversation by ID (or create new)
├── Fetch message history from DB
├── Build message array for agent
├── Run agent with MCP tools
├── Parse tool_calls from agent response
├── Execute each tool call
├── Collect tool results
├── Return final response
└── Save all messages to DB
```

## Implementation Pattern

### Chat Endpoint

```python
from openai import OpenAI
from agents import Agent, Runner

@app.post("/api/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    conversation_id = request.conversation_id or str(uuid.uuid4())

    # 1. Load conversation history
    messages = await get_conversation_messages(conversation_id)

    # 2. Build message array for agent
    message_array = build_message_array(messages, request.message)

    # 3. Run agent with tools
    agent = Agent(
        name="TaskAssistant",
        model="gpt-4",
        tools=[add_task, list_tasks, complete_task, delete_task, update_task]
    )
    result = Runner.run(agent, message_array)

    # 4. Parse and execute tool calls (if any)
    tool_outputs = []
    for tool_call in result.tool_calls:
        output = execute_tool(tool_call, user_id)
        tool_outputs.append(output)

    # 5. Save conversation to DB
    await save_conversation(conversation_id, user_id, [
        {"role": "user", "content": request.message},
        {"role": "assistant", "content": result.final_output},
        *tool_outputs
    ])

    return {"conversation_id": conversation_id, "response": result.final_output}
```

### Building Message Array

```python
def build_message_array(messages: list, user_message: str) -> list:
    """Build message array for agent from DB history."""
    message_array = []

    # Add system prompt
    message_array.append({
        "role": "system",
        "content": "You are a helpful task assistant. Use tools when needed."
    })

    # Add historical messages
    for msg in messages:
        message_array.append({
            "role": msg.role,  # "user" or "assistant"
            "content": msg.content
        })

    # Add current user message
    message_array.append({
        "role": "user",
        "content": user_message
    })

    return message_array
```

### Tool Call Execution

```python
async def execute_tool(tool_call: ToolCall, user_id: str) -> dict:
    """Execute a tool call and return structured result."""
    tool_name = tool_call.name
    tool_args = tool_call.arguments
    tool_args["user_id"] = user_id  # Inject user_id

    # Route to appropriate tool
    if tool_name == "add_task":
        result = await add_task(**tool_args)
    elif tool_name == "list_tasks":
        result = await list_tasks(**tool_args)
    # ... other tools

    return {
        "role": "assistant",
        "content": f"Tool {tool_name} executed: {result}",
        "tool_call_id": tool_call.id
    }
```

## Conversation Schema

```python
class Conversation(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str
    created_at: datetime
    updated_at: datetime

class Message(SQLModel, table=True):
    id: int = Field(primary_key=True, autoincrement=True)
    conversation_id: str = Field(foreign_key="conversation.id")
    role: str  # "user", "assistant", "tool"
    content: str
    tool_name: Optional[str] = None
    tool_call_id: Optional[str] = None
    created_at: datetime
```

## Request/Response Models

```python
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: Optional[list[dict]] = None
```

## Dependencies

```txt
openai>=1.0.0
agents>=0.1.0
```

## Verification Checklist

- [ ] Chat endpoint loads and saves conversation history
- [ ] Agent runs with MCP tools
- [ ] Tool calls are parsed and executed correctly
- [ ] User isolation enforced in all tool calls
- [ ] Conversation ID links related messages
- [ ] Response returned with proper structure
