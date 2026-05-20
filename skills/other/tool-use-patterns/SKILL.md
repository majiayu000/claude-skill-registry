---
name: tool-use-patterns
description: >
  Patterns for Claude tool use including tool definition schemas, multi-tool orchestration,
  parallel tool calls, error handling, and result formatting. Use when the user is defining
  tools for Claude, building agentic workflows with tool calling, handling tool errors, or
  implementing multi-step tool pipelines.
---

# Tool Use Patterns

Patterns for defining, orchestrating, and handling Claude tool use. Covers schemas,
multi-tool flows, parallel execution, error handling, and result formatting.

## When to Use
- User is defining tools for the Claude API
- User is building agentic loops with tool calling
- User needs parallel tool execution
- User is handling tool errors or formatting results
- User is designing multi-step tool workflows

## Core Patterns

### Tool Definition Schema

Tools are defined with a name, description, and JSON Schema for input_schema.
The description is critical -- Claude uses it to decide when to call the tool.

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a city. Use this when the user asks about weather, temperature, or forecast for a specific location.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name, e.g. 'San Francisco, CA'"
                },
                "units": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature units. Default: fahrenheit."
                }
            },
            "required": ["city"]
        }
    }
]

message = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}]
)
```

### Agentic Tool Loop

The core pattern: send a message, check if Claude wants to use tools, execute them,
return results, and repeat until Claude produces a final text response.

```python
def run_agent(user_message: str, tools: list, system: str = "") -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6-20250514",
            max_tokens=4096,
            system=system,
            tools=tools,
            messages=messages,
        )

        # Collect tool use blocks and text
        tool_results = []
        final_text = ""

        for block in response.content:
            if block.type == "tool_use":
                # Execute the tool
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result)
                })
            elif block.type == "text":
                final_text = block.text

        # If no tool calls, return the final text
        if response.stop_reason == "end_turn":
            return final_text

        # Append assistant response and tool results
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
```

### Parallel Tool Calls

Claude can call multiple tools simultaneously. Handle all tool results in a single
user message to maintain correct conversation structure.

```python
# Claude may return multiple tool_use blocks in one response
# Example: user asks "Compare weather in NYC and London"

for block in response.content:
    if block.type == "tool_use":
        # Execute each tool call
        result = execute_tool(block.name, block.input)
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,  # Must match the specific tool_use block
            "content": json.dumps(result)
        })

# Return ALL results in a single user message
messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user", "content": tool_results})
```

### Tool Error Handling

Return errors as tool results so Claude can reason about them and recover.

```python
def execute_tool(name: str, inputs: dict) -> dict:
    try:
        if name == "get_weather":
            return get_weather(**inputs)
        elif name == "search_database":
            return search_database(**inputs)
        else:
            return {"error": f"Unknown tool: {name}"}
    except ValueError as e:
        return {"error": f"Invalid input: {str(e)}"}
    except TimeoutError:
        return {"error": "Request timed out. Try again or use a different query."}
    except Exception as e:
        return {"error": f"Tool execution failed: {str(e)}"}

# Alternatively, use the is_error flag for explicit error signaling
tool_results.append({
    "type": "tool_result",
    "tool_use_id": block.id,
    "content": "City not found. Please check the spelling.",
    "is_error": True  # Tells Claude this is an error, not a valid result
})
```

### Forcing Tool Use

Control whether Claude must use a tool, can choose, or must not use tools.

```python
# Force Claude to use a specific tool
message = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "tool", "name": "get_weather"},  # Must use this tool
    messages=[{"role": "user", "content": "Tokyo forecast"}]
)

# Force Claude to use any tool (but must pick one)
tool_choice = {"type": "any"}

# Let Claude decide (default behavior)
tool_choice = {"type": "auto"}
```

### Tool Result Formatting

Structure tool results so Claude can reason about them effectively.

```python
# Good: structured, clear result
result = {
    "status": "success",
    "data": {
        "city": "Tokyo",
        "temperature": 22,
        "units": "celsius",
        "conditions": "partly cloudy",
        "humidity": 65
    }
}

# Good: include metadata for pagination or follow-up
result = {
    "status": "success",
    "results": items[:10],
    "total_count": 247,
    "has_more": True,
    "next_cursor": "abc123"
}
```

## Anti-Patterns
- Writing vague tool descriptions that do not explain WHEN to use the tool
- Not including `required` fields in the input schema
- Returning raw exception tracebacks as tool results (expose internals, confuse Claude)
- Sending tool results with mismatched `tool_use_id` (causes API error)
- Not handling the case where Claude calls multiple tools in parallel
- Using `tool_choice: {"type": "tool"}` in a loop (causes infinite tool calling)
- Putting business logic in tool descriptions instead of the system prompt
- Returning excessively large tool results (summarize or paginate instead)

## Quick Reference

| Field | Purpose |
|-------|---------|
| `name` | Tool identifier, snake_case, max 64 chars |
| `description` | When and why to use -- be specific and directive |
| `input_schema` | JSON Schema object with properties and required |
| `tool_use_id` | Links tool result back to the specific tool call |
| `is_error` | Boolean flag signaling error in tool result |
| `tool_choice` | `auto` (default), `any` (must call one), `{"type":"tool","name":"X"}` |

Conversation structure for tool use:
1. `user` message -> Claude responds with `tool_use` blocks
2. `assistant` message (Claude's response with tool_use) -> `user` message with `tool_result` blocks
3. Repeat until `stop_reason` is `end_turn`
