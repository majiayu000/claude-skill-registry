---
name: function-calling
description: LLM function calling and tool use patterns. Use when enabling LLMs to call external tools, defining tool schemas, implementing tool execution loops, or getting structured output from LLMs.
context: fork
agent: llm-integrator
version: 1.0.0
author: SkillForge
user-invocable: false
---

# Function Calling

Enable LLMs to use external tools and return structured data.

## When to Use

- LLM needs to call APIs or databases
- Extracting structured data from text
- Building AI agents with tool use
- Reliable JSON output from LLMs

## Basic Tool Definition (2026 Best Practice)

```python
# OpenAI format with strict mode (2026 recommended)
tools = [{
    "type": "function",
    "function": {
        "name": "search_documents",
        "description": "Search the document database for relevant content",
        "strict": True,  # ← 2026: Enables structured output validation
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results to return"
                }
            },
            "required": ["query", "limit"],  # All props required when strict
            "additionalProperties": False     # ← 2026: Required for strict mode
        }
    }
}]

# Note: With strict=True:
# - All properties must be listed in "required"
# - additionalProperties must be False
# - No "default" values (provide via code instead)
```

## Tool Execution Loop

```python
async def run_with_tools(messages: list, tools: list) -> str:
    """Execute tool calls until LLM returns final answer."""
    while True:
        response = await llm.chat(messages=messages, tools=tools)

        # Check if LLM wants to call tools
        if not response.tool_calls:
            return response.content

        # Execute each tool call
        for tool_call in response.tool_calls:
            result = await execute_tool(
                tool_call.function.name,
                json.loads(tool_call.function.arguments)
            )

            # Add tool result to conversation
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

        # Continue loop (LLM will process tool results)

async def execute_tool(name: str, args: dict) -> any:
    """Route to appropriate tool implementation."""
    tools = {
        "search_documents": search_documents,
        "get_weather": get_weather,
        "calculate": calculate,
    }
    return await tools[name](**args)
```

## Structured Output (Guaranteed JSON)

```python
from pydantic import BaseModel

class Analysis(BaseModel):
    sentiment: str
    confidence: float
    key_points: list[str]

# OpenAI structured output
response = await client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Analyze this text..."}],
    response_format=Analysis
)

analysis = response.choices[0].message.parsed  # Typed Analysis object
```

## LangChain Tool Binding

```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

@tool
def search_documents(query: str, limit: int = 5) -> list[dict]:
    """Search the document database.

    Args:
        query: Search query string
        limit: Maximum results to return
    """
    return db.search(query, limit=limit)

# Bind to model
llm_with_tools = llm.bind_tools([search_documents])

# Or with structured output
class SearchResult(BaseModel):
    query: str = Field(description="The search query used")
    results: list[str] = Field(description="Matching documents")

structured_llm = llm.with_structured_output(SearchResult)
```

## Parallel Tool Calls

```python
# OpenAI supports parallel tool calls
response = await llm.chat(
    messages=messages,
    tools=tools,
    parallel_tool_calls=True  # Default in GPT-4o
)

# Handle multiple calls in parallel
if response.tool_calls:
    results = await asyncio.gather(*[
        execute_tool(tc.function.name, json.loads(tc.function.arguments))
        for tc in response.tool_calls
    ])
```

**⚠️ 2026 Compatibility Note:**
```python
# Structured outputs with strict=True may not work with parallel_tool_calls
# If using strict mode schemas, disable parallel calls:
response = await llm.chat(
    messages=messages,
    tools=tools_with_strict_true,
    parallel_tool_calls=False  # Required for strict mode reliability
)
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Tool count | 5-15 max (more = confusion) |
| Description length | 1-2 sentences |
| Parameter validation | Use Pydantic/Zod |
| Error handling | Return error as tool result |
| **Schema mode** | **`strict: true` (2026 best practice)** |
| Output format | Structured Outputs > JSON mode |
| Parallel calls | Disable with strict mode |

## Common Mistakes

- Vague tool descriptions (LLM won't know when to use)
- No input validation (LLM sends bad params)
- Missing error handling (crashes on tool failure)
- Too many tools (LLM gets confused)

## Related Skills

- `agent-loops` - Multi-step tool use with reasoning
- `llm-streaming` - Streaming with tool calls
- `structured-output` - Complex output schemas

## Capability Details

### tool-definition
**Keywords:** tool, function, define tool, tool schema, function schema
**Solves:**
- Define tools with clear descriptions
- Create JSON schemas for tool parameters
- Document tool behavior for LLM

### tool-execution-loop
**Keywords:** execution loop, tool call, agent loop, run tool
**Solves:**
- Implement tool execution loops
- Handle multiple tool calls
- Process tool results

### structured-output
**Keywords:** structured output, JSON output, typed response, response schema
**Solves:**
- Get structured JSON from LLM
- Enforce output schemas
- Parse and validate responses

### parallel-tool-calls
**Keywords:** parallel, concurrent, multiple tools, batch tools
**Solves:**
- Execute multiple tools in parallel
- Handle concurrent tool results
- Optimize tool call latency

### strict-mode-schemas
**Keywords:** strict mode, strict schema, additionalProperties, required fields
**Solves:**
- Enforce strict JSON schemas
- Prevent extra fields in output
- Ensure schema compliance
