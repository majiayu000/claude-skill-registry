---
name: mosaic-ai-agent
description: Expert guidance for building production-ready tool-calling agents with Databricks Mosaic AI Agent Framework. Use when users need to create agents that orchestrate multiple data sources or APIs, implement LangChain-based agentic workflows, design Foundation Model-powered tool selection, optimize agent prompts and decision-making, or architect multi-tool agent systems. Covers agent architecture patterns, tool design best practices, Foundation Model integration, and common pitfalls.
---

# Mosaic AI Agent Builder

Build production-ready tool-calling agents that intelligently orchestrate data sources and APIs using Databricks Foundation Models and LangChain.

## Core Concepts

### What is a Tool-Calling Agent?

A tool-calling agent uses an LLM to:
1. Understand user intent
2. Decide which tool(s) to call
3. Execute selected tools
4. Synthesize results into a response

**Key advantage:** Dynamic routing - the LLM adapts to each query instead of following rigid logic.

### When to Use Agents vs. Direct LLM Calls

**Use agents when:**
- Query complexity varies (some need 1 tool, others need 3+)
- Tool selection depends on nuanced intent
- You need multi-step reasoning
- Tools can be composed in different ways

**Use direct LLM calls when:**
- Single, predictable tool usage
- Deterministic routing logic
- Low latency is critical
- Cost optimization is paramount

## Problem-Solution Patterns

### Problem 1: Agent Calls Wrong Tools

**Symptoms:**
- Agent uses web search instead of internal data source
- Calls inventory tool for customer behavior questions
- Skips relevant tools entirely

**Root causes:**
- Vague tool descriptions
- Overlapping tool responsibilities
- Insufficient examples in docstrings

**Solution:**

```python
# ❌ BAD - Vague description
@tool
def query_database(question: str) -> str:
    """Query the database"""
    pass

# ✅ GOOD - Specific with examples
@tool
def query_customer_behavior(question: str) -> str:
    """
    Query customer behavior analytics for purchase patterns and preferences.
    
    Use this tool when users ask about:
    - Product trends: "What products are trending?"
    - Shopping channels: "Which channels do customers prefer?"
    - Customer segments: "Which segments respond to promotions?"
    - Purchase patterns: "When do customers typically buy?"
    
    Do NOT use for:
    - Inventory levels (use query_inventory instead)
    - External market data (use web_search instead)
    """
    pass
```

**Best practices:**
- Include 3-5 concrete example questions
- Explicitly list what NOT to use the tool for
- Use domain-specific terminology
- Keep descriptions under 150 words

### Problem 2: Agent Gets Stuck in Loops

**Symptoms:**
- Calls same tool repeatedly with identical queries
- Exceeds max iterations
- Never reaches a final answer

**Root causes:**
- Tool returns errors without guidance
- Ambiguous tool outputs
- Missing synthesis instructions

**Solution:**

```python
# Configure executor with proper limits
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,  # Prevent infinite loops
    handle_parsing_errors=True,  # Gracefully handle errors
    early_stopping_method="generate"  # Force answer after max iterations
)

# Ensure tools return actionable results
@tool
def query_data(question: str) -> str:
    try:
        result = fetch_data(question)
        if not result:
            return "No data found. Try rephrasing or use a different time range."
        return result
    except Exception as e:
        return f"Query failed: {str(e)}. Consider checking data availability."
```

### Problem 3: Poor Multi-Tool Synthesis

**Symptoms:**
- Agent lists tool outputs separately without analysis
- Contradictory information not resolved
- Missing insights from combining data

**Root causes:**
- Weak system prompt
- LLM not instructed to synthesize
- Temperature too low

**Solution:**

```python
system_prompt = """You are a data analysis assistant with access to multiple tools.

CRITICAL: When you call multiple tools, you MUST:
1. Identify connections and patterns across tool results
2. Resolve any contradictions with reasoning
3. Provide unified insights, not separate summaries
4. Highlight actionable recommendations

Example of good synthesis:
"Based on customer behavior data (Tool 1), Products X and Y are trending.
However, inventory analysis (Tool 2) shows 60-day supply of both—well above
the 30-day target. This indicates overstock risk despite high demand.
Recommendation: Launch promotions to clear inventory while demand is strong."

Example of bad synthesis:
"Tool 1 says products are trending. Tool 2 says inventory is high."
"""

# Use appropriate temperature
llm = ChatDatabricks(
    endpoint="databricks-meta-llama-3-1-70b-instruct",
    temperature=0.3,  # Balance creativity and consistency
    max_tokens=2000
)
```

### Problem 4: Slow Agent Response Times

**Symptoms:**
- Queries take >30 seconds
- Users abandon before completion
- High costs from unnecessary tool calls

**Root causes:**
- Sequential tool execution
- Redundant tool calls
- No caching

**Solutions:**

**Strategy 1: Implement caching**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def query_customer_behavior_cached(question: str) -> str:
    """Cached version of customer behavior queries"""
    return query_customer_behavior(question)
```

**Strategy 2: Use streaming for better UX**
```python
# Return intermediate results to user
for step in agent_executor.stream({"input": query}):
    if "intermediate_step" in step:
        print(f"Calling tool: {step['intermediate_step'][0].tool}...")
```

**Strategy 3: Optimize tool implementation**
```python
# Ensure tools don't do unnecessary work
@tool
def query_inventory(question: str) -> str:
    # Add query caching at data source level
    # Use efficient query patterns
    # Return concise summaries, not raw data
    pass
```

## Agent Architecture Patterns

### Pattern 1: Single-Domain Agent
**Use case:** All tools access same domain (e.g., only internal DBs)

```python
tools = [
    query_sales_db,
    query_inventory_db,
    query_customer_db
]

system_prompt = """You are an internal data analyst.
All tools access company databases. Choose tools based on data domain."""
```

**Pros:** Simple, fast tool selection  
**Cons:** Can't incorporate external data

### Pattern 2: Multi-Domain Agent
**Use case:** Mix of internal and external sources

```python
tools = [
    query_internal_data,  # Genie rooms
    search_web,           # External API
    query_company_docs    # Document search
]

system_prompt = """You are an analyst with internal and external data access.

Prioritization:
1. Check internal tools first for company-specific data
2. Use external tools for market trends, events, competitor info
3. Combine sources when appropriate"""
```

**Pros:** Comprehensive answers  
**Cons:** More complex tool selection

### Pattern 3: Specialized Sub-Agents
**Use case:** Complex domains with distinct sub-workflows

```python
# Main coordinator agent
coordinator_tools = [
    delegate_to_analyst_agent,
    delegate_to_forecasting_agent,
    delegate_to_reporting_agent
]

# Each sub-agent has its own tools and expertise
# Use only when orchestration complexity justifies it
```

## Foundation Model Selection

### Model Comparison for Agents

| Model | Best For | Tradeoffs |
|-------|----------|-----------|
| **Llama 3.1 70B** | Balanced performance, cost | Good tool selection, moderate speed |
| **Llama 3.1 405B** | Complex reasoning, multiple tools | Slower, more expensive |
| **DBRX Instruct** | Fast responses, simple routing | Less sophisticated reasoning |
| **Claude Sonnet** | Excellent tool use, synthesis | Higher cost, external API |

### Configuration Guidelines

```python
# For simple agents (2-3 tools, clear boundaries)
llm = ChatDatabricks(
    endpoint="databricks-dbrx-instruct",
    temperature=0.1,
    max_tokens=1500
)

# For complex agents (5+ tools, nuanced decisions)
llm = ChatDatabricks(
    endpoint="databricks-meta-llama-3-1-70b-instruct",
    temperature=0.2,
    max_tokens=2500
)
```

## Tool Design Best Practices

### Principle 1: Single Responsibility
Each tool should do ONE thing well.

```python
# ❌ BAD - Tool does too much
@tool
def query_all_data(question: str) -> str:
    """Query any data source based on the question"""
    pass

# ✅ GOOD - Focused tools
@tool
def query_customer_behavior(question: str) -> str:
    """Query customer behavior data"""
    pass

@tool
def query_inventory_status(question: str) -> str:
    """Query inventory levels"""
    pass
```

### Principle 2: Clear Inputs/Outputs
Make tool interfaces obvious.

```python
# ❌ BAD - Ambiguous signature
@tool
def get_data(input: str) -> str:
    pass

# ✅ GOOD - Clear semantics
@tool
def query_sales_by_region(
    region: str,
    start_date: str,
    end_date: str
) -> str:
    """
    Args:
        region: Geographic region (e.g., "North America", "EMEA")
        start_date: ISO format (e.g., "2024-01-01")
        end_date: ISO format (e.g., "2024-12-31")
    
    Returns:
        Sales summary with total revenue and top products
    """
    pass
```

### Principle 3: Error Handling
Tools should fail gracefully.

```python
@tool
def query_external_api(query: str) -> str:
    try:
        response = call_api(query)
        if not response:
            return "No results found. Try a different query."
        return response
    except TimeoutError:
        return "API timeout. The service may be temporarily unavailable."
    except Exception as e:
        return f"Error: {str(e)}. Please try again or contact support."
```

## Prompt Engineering for Agents

### System Prompt Structure

```python
system_prompt = """
[Role Definition]
You are a [specific role] with access to [tools description].

[Capabilities]
Your tools allow you to:
- [Capability 1]
- [Capability 2]

[Decision Guidelines]
When selecting tools:
1. [Guideline 1]
2. [Guideline 2]

[Synthesis Instructions]
When combining tool results:
- [Instruction 1]
- [Instruction 2]

[Output Format]
Always provide:
- [Element 1]
- [Element 2]
"""
```

### Few-Shot Examples in Prompts

```python
system_prompt = """You are an analyst with customer and inventory tools.

Example 1:
User: "What products are trending?"
Reasoning: Customer behavior question → use query_customer_behavior
Action: Call query_customer_behavior("trending products")

Example 2:
User: "Trending products at risk of overstock?"
Reasoning: Needs both demand and supply data
Action: Call query_customer_behavior + query_inventory_status, then synthesize

Use this reasoning pattern for all queries."""
```

## Testing & Iteration

### Test Cases for Agent Validation

```python
test_cases = [
    # Single tool - unambiguous
    {
        "query": "What products are trending?",
        "expected_tools": ["query_customer_behavior"],
        "expected_not_called": ["query_inventory", "web_search"]
    },
    # Multi-tool - requires synthesis
    {
        "query": "Trending products at risk of overstock?",
        "expected_tools": ["query_customer_behavior", "query_inventory"],
        "tool_order": "any"
    },
    # Edge case - ambiguous query
    {
        "query": "Tell me about products",
        "expected_behavior": "ask_clarification"
    }
]
```

### Debugging with Verbose Mode

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # Shows LLM reasoning
    return_intermediate_steps=True
)

result = agent_executor.invoke({"input": "your query"})

# Inspect tool calls
for step in result['intermediate_steps']:
    tool_name = step[0].tool
    tool_input = step[0].tool_input
    tool_output = step[1]
    print(f"Tool: {tool_name}\nInput: {tool_input}\nOutput: {tool_output}\n")
```

## Common Pitfalls

### Pitfall 1: Over-Engineering
**Mistake:** Creating 20+ micro-tools  
**Fix:** Start with 3-5 tools, split only when tool descriptions exceed 200 words

### Pitfall 2: Under-Specifying Tools
**Mistake:** Assuming LLM "knows" when to use tools  
**Fix:** Explicit examples and counter-examples in docstrings

### Pitfall 3: Ignoring Latency
**Mistake:** Not optimizing for response time  
**Fix:** Profile tool execution, implement caching, consider async patterns

### Pitfall 4: No Evaluation
**Mistake:** Deploying without systematic testing  
**Fix:** Create test suite with expected tool selections (see agent-mlops skill)

## Integration with Databricks

### Using Databricks Foundation Models

```python
from langchain_community.chat_models import ChatDatabricks

llm = ChatDatabricks(
    endpoint="databricks-meta-llama-3-1-70b-instruct",
    temperature=0.1,
    max_tokens=2000
)
```

### Common Endpoints
- `databricks-meta-llama-3-1-70b-instruct` - Recommended for most agents
- `databricks-meta-llama-3-1-405b-instruct` - Complex reasoning
- `databricks-dbrx-instruct` - Fast, simple routing

## Quick Reference

**Minimum viable agent:**
```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.chat_models import ChatDatabricks
from langchain.tools import tool

@tool
def my_tool(query: str) -> str:
    """Clear description with examples"""
    return "result"

llm = ChatDatabricks(endpoint="databricks-meta-llama-3-1-70b-instruct")
agent = create_tool_calling_agent(llm, [my_tool], prompt)
executor = AgentExecutor(agent=agent, tools=[my_tool])
result = executor.invoke({"input": "user query"})
```

## Related Skills

- **genie-integration**: Integrate Genie rooms as agent tools
- **agent-mlops**: Deploy and monitor agents in production
