---
name: tool-use
description: Tool use patterns for Claude including schema design, tool_choice modes, result handling, parallel execution, error recovery, and extended thinking integration.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Tool Use Skill

Comprehensive guide to implementing tool use with Claude, covering schema design, tool choice modes, multi-turn conversations, error handling patterns, and advanced features like extended thinking and strict schema conformance.

## When to Use This Skill

Activate this skill when:
- Defining custom tools with JSON schemas
- Building agentic workflows with tool use
- Implementing tool result handling
- Building parallel vs sequential tool orchestration
- Requiring guaranteed schema conformance
- Implementing error recovery patterns
- Combining tools with extended thinking

## Core Concepts

### Tool Definition Schema

Every tool requires a JSON Schema input definition with:
- **name**: Tool identifier (regex: `^[a-zA-Z0-9_-]{1,64}$`)
- **description**: Detailed explanation of purpose, when to use, behavior (3-4+ sentences)
- **input_schema**: JSON Schema defining parameters
- **input_examples** (optional, beta): Concrete examples of valid inputs

#### Best Practices for Tool Definitions

```json
{
  "name": "get_stock_price",
  "description": "Retrieves the current stock price for a given ticker symbol. The ticker symbol must be a valid symbol for a publicly traded company on a major US stock exchange like NYSE or NASDAQ. The tool will return the latest trade price in USD. Use this when the user asks about the current or most recent price of a specific stock. It will not provide any other information about the stock or company beyond the price.",
  "input_schema": {
    "type": "object",
    "properties": {
      "ticker": {
        "type": "string",
        "description": "The stock ticker symbol, e.g. AAPL for Apple Inc. Must be uppercase."
      },
      "include_historical": {
        "type": "boolean",
        "description": "Optional. Whether to include 52-week high/low prices.",
        "default": false
      }
    },
    "required": ["ticker"],
    "additionalProperties": false
  },
  "input_examples": [
    {"ticker": "AAPL"},
    {"ticker": "MSFT", "include_historical": true},
    {"ticker": "GOOGL"}
  ]
}
```

**Key Guidelines:**
- Descriptions should be 3-4+ sentences minimum
- Explain what the tool does, when to use it, what it returns, limitations
- Use `input_examples` for complex nested objects or format-sensitive parameters
- Set `additionalProperties: false` for strict validation
- Use enums for constrained parameters

### Tool Choice Modes

Control how Claude decides whether and how to use tools:

| Mode | Behavior | Use Case |
|------|----------|----------|
| `"auto"` | Claude decides to use tools or not (default) | General tool use, letting Claude decide |
| `"any"` | Claude must use one tool but can choose which | Forcing tool use without specific tool |
| `"tool"` | Force specific tool (e.g., `{"type": "tool", "name": "get_weather"}`) | Structured JSON output, specific tool required |
| `"none"` | Prevent all tool use | Normal text-only responses |

```python
# Allow Claude to decide
# tool_choice="auto" (default)

# Force any tool to be used
tool_choice={"type": "any"}

# Force specific tool (useful for JSON output)
tool_choice={"type": "tool", "name": "record_summary"}

# Prevent tool use
tool_choice={"type": "none"}
```

**Important Constraints with Extended Thinking:**
- Extended thinking only supports `tool_choice: {"type": "auto"}` or `{"type": "none"}`
- Cannot use `{"type": "any"}` or `{"type": "tool"}` with extended thinking
- Use the separate "think" tool instead for complex reasoning with tool use

### Strict Schema Conformance (Beta)

Enable guaranteed schema validation with `strict: true`:

```python
tools=[{
    "name": "search_flights",
    "strict": True,  # Enable strict mode
    "input_schema": {
        "type": "object",
        "properties": {
            "destination": {"type": "string"},
            "departure_date": {"type": "string", "format": "date"},
            "passengers": {"type": "integer"}
        },
        "required": ["destination", "departure_date"],
        "additionalProperties": False
    }
}]
```

**Benefits:**
- Guaranteed type-safe parameters (never `"2"` instead of `2`)
- No missing required fields
- No runtime schema validation needed
- Production-ready reliability

**Limitations:**
- Refusals override schema (safety takes precedence)
- Token limit truncation may break schema
- Some recursive schemas not supported
- Requires `structured-outputs-2025-11-13` beta header

## Single Tool Use Pattern

Basic pattern: Define tool → Claude calls tool → Return result → Claude responds

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[{
        "name": "get_weather",
        "description": "Get current weather in a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and state, e.g. San Francisco, CA"
                }
            },
            "required": ["location"]
        }
    }],
    messages=[{"role": "user", "content": "What's the weather in SF?"}]
)

# Check if Claude wants to use tool
if response.stop_reason == "tool_use":
    tool_use = next(b for b in response.content if b.type == "tool_use")
    print(f"Tool: {tool_use.name}")
    print(f"Input: {tool_use.input}")

    # Execute tool (simulate)
    tool_result = "68°F, partly cloudy"

    # Return result to Claude
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        tools=[...],  # Same tools
        messages=[
            {"role": "user", "content": "What's the weather in SF?"},
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": [{
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": tool_result
            }]}
        ]
    )

    print(response.content[0].text)
```

## Multi-Turn Tool Conversations

Tools often require sequential calls where one tool's output feeds into another:

```python
# User asks: "What's the weather where I am?"
# Flow: get_location() → get_weather(location)

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[
        {
            "name": "get_location",
            "description": "Get user's location from IP address",
            "input_schema": {"type": "object", "properties": {}}
        },
        {
            "name": "get_weather",
            "description": "Get weather for location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    ],
    messages=[{"role": "user", "content": "What's the weather where I am?"}]
)

# Claude calls get_location first
tool_use = next(b for b in response.content if b.type == "tool_use")
location_result = "San Francisco, CA"

# Send location result back
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[...],
    messages=[
        {"role": "user", "content": "What's the weather where I am?"},
        {"role": "assistant", "content": response.content},
        {"role": "user", "content": [{
            "type": "tool_result",
            "tool_use_id": tool_use.id,
            "content": location_result
        }]}
    ]
)

# Claude now calls get_weather with the location
tool_use2 = next(b for b in response.content if b.type == "tool_use")
weather_result = "68°F, sunny"

# Final result
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[...],
    messages=[
        {"role": "user", "content": "What's the weather where I am?"},
        {"role": "assistant", "content": response.content},
        {"role": "user", "content": [{
            "type": "tool_result",
            "tool_use_id": tool_use.id,
            "content": location_result
        }]},
        {"role": "assistant", "content": response.content},
        {"role": "user", "content": [{
            "type": "tool_result",
            "tool_use_id": tool_use2.id,
            "content": weather_result
        }]}
    ]
)

print(response.content[0].text)
```

## Parallel Tool Use Pattern

Claude can call multiple independent tools simultaneously:

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[...],
    messages=[{
        "role": "user",
        "content": "What's the weather in SF and NYC? What time is it there?"
    }]
)

# Claude makes 4 parallel tool calls (2 weather + 2 time)
tool_uses = [b for b in response.content if b.type == "tool_use"]
print(f"Parallel calls: {len(tool_uses)}")  # 4

# Execute all tools and collect results
tool_results = []
for tool_use in tool_uses:
    if tool_use.name == "get_weather":
        if "San Francisco" in str(tool_use.input):
            result = "68°F, partly cloudy"
        else:
            result = "45°F, clear"
    else:  # get_time
        if "Los_Angeles" in str(tool_use.input):
            result = "2:30 PM PST"
        else:
            result = "5:30 PM EST"

    tool_results.append({
        "type": "tool_result",
        "tool_use_id": tool_use.id,
        "content": result
    })

# IMPORTANT: Return all results in ONE user message
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[...],
    messages=[
        {"role": "user", "content": "What's the weather in SF and NYC? What time is it there?"},
        {"role": "assistant", "content": response.content},
        {"role": "user", "content": tool_results}  # All results together!
    ]
)

print(response.content[0].text)
```

**Critical Formatting Rules for Parallel Tools:**
- All tool results must be in a SINGLE user message
- Tool result blocks must come FIRST in content array
- Text can come AFTER tool results if needed
- Incorrect formatting teaches Claude to avoid parallel calls

## Tool Result Handling

### Basic Tool Result Format

```python
{
    "type": "tool_result",
    "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
    "content": "15 degrees"
}
```

### Tool Result with Images

```python
{
    "type": "tool_result",
    "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
    "content": [
        {"type": "text", "text": "Current weather screenshot:"},
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": "/9j/4AAQSkZJRg..."
            }
        }
    ]
}
```

### Tool Result with Documents

```python
{
    "type": "tool_result",
    "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
    "content": [
        {"type": "text", "text": "Document content:"},
        {
            "type": "document",
            "source": {
                "type": "text",
                "media_type": "text/plain",
                "data": "Full document content here"
            }
        }
    ]
}
```

### Error Handling in Tool Results

```python
# Tool execution error
{
    "type": "tool_result",
    "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
    "content": "ConnectionError: Weather API is unavailable (HTTP 500)",
    "is_error": True
}

# Missing parameter error
{
    "type": "tool_result",
    "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
    "content": "Error: Missing required 'location' parameter",
    "is_error": True
}
```

## Error Recovery Patterns

### Pattern 1: Graceful Error Reporting

When tool execution fails, report error and Claude retries with corrections:

```python
if tool_execution_failed:
    tool_result = {
        "type": "tool_result",
        "tool_use_id": tool_use.id,
        "content": f"Error: {error_message}",
        "is_error": True
    }
```

Claude typically retries 2-3 times before apologizing to the user.

### Pattern 2: Strict Schema Enforcement

With `strict: true`, invalid parameters are prevented before execution:

```python
# With strict: true, Claude CANNOT send invalid parameters
# Invalid type: "passengers": "two" → prevented by schema
# Missing required field → prevented by schema
# Type mismatch: int vs string → prevented by schema
```

### Pattern 3: Max Tokens Handling

If response is cut off during tool use, retry with higher limit:

```python
if response.stop_reason == "max_tokens":
    last_block = response.content[-1]
    if last_block.type == "tool_use":
        # Incomplete tool use, retry with more tokens
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,  # Increased
            messages=messages,
            tools=tools
        )
```

## Tool Use for Structured JSON Output

Use tools to guarantee structured JSON output without tool execution:

```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    betas=["structured-outputs-2025-11-13"],
    tools=[{
        "name": "record_summary",
        "description": "Record structured image summary",
        "input_schema": {
            "type": "object",
            "properties": {
                "key_colors": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "r": {"type": "number"},
                            "g": {"type": "number"},
                            "b": {"type": "number"},
                            "name": {"type": "string"}
                        },
                        "required": ["r", "g", "b", "name"]
                    }
                },
                "description": {"type": "string"},
                "estimated_year": {"type": "integer"}
            },
            "required": ["key_colors", "description"]
        }
    }],
    tool_choice={"type": "tool", "name": "record_summary"},
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "url", "url": "https://..."}},
            {"type": "text", "text": "Describe this image"}
        ]
    }]
)

# Extract structured output from tool use input
tool_use = next(b for b in response.content if b.type == "tool_use")
structured_data = tool_use.input
```

## Parallel Tool Use Best Practices

### Encouraging Parallel Execution

Add to system prompt for stronger parallel tool use:

```text
<use_parallel_tool_calls>
For maximum efficiency, whenever you perform multiple independent operations,
invoke all relevant tools simultaneously rather than sequentially. Prioritize
calling tools in parallel whenever possible. When reading 3 files, run 3 tool
calls in parallel. When running multiple commands like 'ls' or 'list_dir',
always run all commands in parallel.
</use_parallel_tool_calls>
```

### Measuring Parallel Tool Use

```python
def measure_parallel_efficiency(messages):
    # Find assistant messages with tool use
    tool_call_messages = [
        msg for msg in messages
        if msg.get("role") == "assistant"
        and any(b.get("type") == "tool_use" for b in msg.get("content", []))
    ]

    total_tools = sum(
        len([b for b in msg.get("content", []) if b.get("type") == "tool_use"])
        for msg in tool_call_messages
    )

    if not tool_call_messages:
        return 0

    avg_per_message = total_tools / len(tool_call_messages)
    print(f"Average tools per message: {avg_per_message}")
    # > 1.0 indicates parallel tool use working
```

## Extended Thinking Integration

### Extended Thinking Constraints

```python
# ✅ ALLOWED with extended thinking
response = client.messages.create(
    model="claude-opus-4-5",
    thinking={"type": "enabled", "budget_tokens": 2048},
    tools=[...],
    tool_choice={"type": "auto"},  # Default
    messages=[...]
)

# ✅ ALLOWED with extended thinking
tool_choice={"type": "none"}  # No tools

# ❌ NOT ALLOWED with extended thinking
# tool_choice={"type": "any"}  → Error
# tool_choice={"type": "tool", "name": "..."}  → Error
```

### "Think" Tool for Complex Reasoning

When you need extended reasoning with tool use, use the "think" tool:

```python
tools=[{
    "name": "think",
    "description": "Pause and think carefully before proceeding",
    "input_schema": {
        "type": "object",
        "properties": {
            "reasoning": {
                "type": "string",
                "description": "Your detailed reasoning"
            }
        },
        "required": ["reasoning"]
    }
}, {
    "name": "get_weather",
    "description": "Get weather information",
    "input_schema": {...}
}]
```

## SDK Tool Runner (Simplified Implementation)

Python and TypeScript SDKs provide tool runners for automatic tool execution:

```python
import anthropic
from anthropic import beta_tool

client = anthropic.Anthropic()

@beta_tool
def get_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get current weather in a location.

    Args:
        location: City and state, e.g. San Francisco, CA
        unit: Temperature unit, either 'celsius' or 'fahrenheit'
    """
    # Tool implementation
    return '{"temperature": "20°C", "condition": "Sunny"}'

# Tool runner automatically handles tool execution loop
runner = client.beta.messages.tool_runner(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[get_weather],
    messages=[{"role": "user", "content": "What's the weather in Paris?"}]
)

# Iterate through responses
for message in runner:
    print(message.content[0].text)

# Or get final message directly
final_message = runner.until_done()
```

## JSON Schema Support and Limitations

### Supported Features

- All basic types: object, array, string, integer, number, boolean, null
- `enum` for constrained values
- `const` for fixed values
- `anyOf`, `allOf` for complex types
- `$ref`, `$def`, `definitions` for schema composition
- String formats: date-time, time, date, duration, email, hostname, uri, ipv4, ipv6, uuid
- Array `minItems` (0 and 1 only)

### Not Supported

- Recursive schemas (limit nesting depth)
- Complex types within enums
- External `$ref` (e.g., HTTP URLs)
- Numerical constraints (minimum, maximum, multipleOf)
- String constraints (minLength, maxLength)
- Advanced array constraints
- `additionalProperties` as anything other than false
- Backreferences in regex patterns

## Common Use Cases

### Data Extraction

```python
tools=[{
    "name": "extract_info",
    "description": "Extract structured data from text",
    "input_schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "company": {"type": "string"}
        },
        "required": ["name", "email"]
    }
}]
```

### API Integration

```python
tools=[{
    "name": "search_api",
    "description": "Search external API",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "limit": {"type": "integer", "minimum": 1, "maximum": 100}
        },
        "required": ["query"]
    }
}]
```

### Multi-Step Orchestration

```python
tools=[
    {"name": "validate_input", ...},
    {"name": "process_data", ...},
    {"name": "save_result", ...}
]
# Claude orchestrates the workflow
```

## Performance Considerations

### Token Cost of Tools

- Tool definitions added to input tokens
- Tool use blocks in requests/responses count as tokens
- Tool result blocks count as tokens
- System prompt for tool use: 313-346 tokens depending on tool_choice

### Grammar Compilation

- First use of schema: additional latency for grammar compilation
- Subsequent uses: grammar cached for 24 hours
- Cache invalidated by schema changes or tool set changes
- Name/description changes don't invalidate cache

### Context Window Management

Tool use can quickly consume context in long conversations. Strategies:

1. **Compression**: Summarize tool results
2. **Chunking**: Break large operations into smaller requests
3. **Tool Runner**: Uses automatic context compaction when needed
4. **Checkpointing**: Save conversation state between phases

## Forcing Tool Use (Structured Output)

Use `tool_choice` to force specific behavior:

```python
# Force use of a tool (for JSON output)
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[sentiment_tool],
    tool_choice={"type": "tool", "name": "sentiment_tool"},
    messages=[{"role": "user", "content": "Analyze this text..."}]
)

# No prefilled explanations with forced tool_choice
# Claude goes straight to tool use

# For explanations WITH tool use, use tool_choice="auto" (default)
# and add instruction: "Use the sentiment_tool in your response"
```

## Handling Stop Reasons

### `tool_use`
Claude wants to use a tool. Extract tool use blocks and execute tools.

### `end_turn`
Claude finished generating response. No more tool calls.

### `max_tokens`
Response cut off. If last block is incomplete tool_use, retry with higher max_tokens.

### `pause_turn` (with server tools)
Long operation paused. Continue the conversation to resume.

---

## Resources

- [Anthropic Tool Use Documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [Tool Implementation Guide](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use)
- [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)
- [Claude Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview)
