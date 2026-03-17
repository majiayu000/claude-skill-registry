---
name: claude-advanced-tool-use
description: Advanced tool use patterns including tool search, programmatic calling, and production orchestration. Use when scaling to 10,000+ tools, optimizing token usage, or implementing production tool systems.
---

# Claude Advanced Tool Use

## Overview

Advanced tool use provides three complementary features that address distinct bottlenecks in production systems. These features can be used independently or combined for compounding efficiency gains of 37-85%.

### The Three Features

**1. Tool Search** (85-95% context savings)
- Dynamically discover and load tools on-demand
- Scale to 10,000+ tools without context bloat
- Two variants: Regex pattern matching or BM25 natural language queries
- Deferred loading keeps tool definitions out of context until needed

**2. Programmatic Tool Calling** (37% token reduction)
- Claude writes Python code that calls your tools within a sandboxed container
- Intermediate results stay out of context window
- Eliminates 19+ unnecessary inference passes on complex workflows
- Ideal for data aggregation, filtering, and multi-step orchestration

**3. Tool Use Examples** (72% → 90% accuracy)
- Concrete usage examples clarify ambiguous JSON schemas
- Improve parameter handling accuracy
- Express API conventions schemas cannot capture
- Reduce hallucination on optional parameters

**Key Insight**: Start with your biggest bottleneck, then add complementary features as needed. Not all-or-nothing.

## Feature Comparison Matrix

| Feature | Token Savings | Best For | Complexity | Beta Header |
|---------|---------------|----------|------------|-------------|
| Tool Search | 85-95% | Large tool sets (10+ tools) | Low | advanced-tool-use-2025-11-20 |
| Programmatic Calling | 37% | Multi-step workflows (3+ dependent calls) | Medium | advanced-tool-use-2025-11-20 |
| Tool Examples | Accuracy (72%→90%) | Complex parameters, optional fields | Low | N/A |

## When to Use

**Tool Search**:
- You have 10+ tools in your system
- Tool definitions exceed 10K tokens combined
- Tool selection accuracy degrades with large sets
- Using MCP servers (200+ tools across servers)
- Tool library grows over time

**Programmatic Calling**:
- Workflows with 3+ dependent tool calls
- Processing large datasets where only summaries needed
- Batch operations across multiple items
- Conditional logic based on intermediate results
- Aggregation tasks combining multiple data sources

**Tool Use Examples**:
- JSON schemas don't capture when to use optional parameters
- API conventions need clarification
- Parameter handling accuracy below 80%
- Reducing hallucination on complex tool inputs

**Production Patterns**:
- Building scalable agentic systems
- Implementing security-first tool orchestration
- Optimizing token costs in production
- Coordinating multiple tools efficiently

## Quick Start: Tool Search with Deferred Loading

**Python Example**:
```python
import anthropic

client = anthropic.Anthropic()

tools = [
    # Always-loaded: tool search itself
    {
        "type": "tool_search_tool_regex_20251119",
        "name": "tool_search_tool_regex"
    },
    # Always-loaded: frequently used tools (3-5 total)
    {
        "name": "get_user_info",
        "description": "Get user information by ID",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"}
            }
        }
    },
    # Deferred: specialized tools loaded on-demand
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            }
        },
        "defer_loading": True
    },
    {
        "name": "get_forecast",
        "description": "Get weather forecast for a location and days ahead",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string"},
                "days": {"type": "integer"}
            }
        },
        "defer_loading": True
    }
]

response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    betas=["advanced-tool-use-2025-11-20"],
    max_tokens=2048,
    messages=[{
        "role": "user",
        "content": "What's the weather in San Francisco?"
    }],
    tools=tools
)

print(response.content[0].text)
```

**What Happens**:
1. Claude analyzes request and determines weather tools are needed
2. Uses tool_search_tool_regex with pattern `"weather"`
3. API returns `tool_reference` blocks pointing to matching tools
4. Tool definitions automatically expanded
5. Claude invokes `get_weather` with appropriate parameters
6. Only discovered tools loaded into context (85% savings)

## The Compound Effect

When combined strategically, these features multiply efficiency gains:

**Example: Large MCP System**
- 200+ tools via MCP servers
- **Tool Search**: Reduces context by 85% (10K tokens → 1.5K tokens)
- **Programmatic Calling**: Reduces workflow tokens by 37%
- **Tool Examples**: Improves accuracy from 72% to 90%
- **Combined Impact**: ~90% token reduction + 18% accuracy improvement

**Implementation Strategy**:
1. Start with tool search if definitions exceed 10K tokens
2. Add programmatic calling for multi-step workflows
3. Include examples for tools with complex parameters
4. Measure efficiency gains at each step
5. Iterate based on bottleneck analysis

## Production Architecture Patterns

From production codebase analysis ([Source](.analysis/research/codex-best-practices.md)):

**1. Planner + Executor**
- Separate planning conversation from execution
- Planner decides what to do, executor does it with focused context
- Reduces re-planning overhead

**2. Preview Then Fetch**
- Return IDs/summaries first
- Fetch full documents on-demand
- Keeps context lean

**3. Guard + Act**
- Validate parameters before execution
- Server-side validation with actionable errors
- Security-first approach

**4. Summarize Outputs**
- Compress tool results before continuing
- Works well with programmatic calling
- Only summary enters context window

See `references/production-patterns.md` for complete implementation templates.

## Performance Optimization

**Identifying Your Bottleneck**:
- Tool definitions > 10K tokens → Enable tool search
- Large intermediate datasets → Use programmatic calling
- Parameter confusion → Provide tool examples
- Multiple tool calls → Consider programmatic orchestration

**Optimization Checklist**:
- [ ] Tool descriptions under 200 characters
- [ ] Semantic keywords in descriptions
- [ ] 3-5 most-used tools always loaded
- [ ] Clear tool naming (e.g., `search_customer_orders` not `query_db`)
- [ ] Tool index cached in-session
- [ ] Ranked results returned
- [ ] Server-side validation enabled
- [ ] Tool results memoized where appropriate
- [ ] Security best practices implemented
- [ ] Observability logging with trace IDs

## Integration with Context Management

Tool search and programmatic calling work seamlessly with context editing:

**Tool Result Clearing** (from claude-context-management):
- Server-side strategy removes older tool results chronologically
- Preserves recent N tool uses
- Can exclude specific tools (e.g., web_search)
- Works with deferred loading

**Programmatic Calling** (keeps results out of context):
- Tool results from code execution don't enter context window
- Only final outputs returned to Claude
- Natural synergy: fewer results + more efficient orchestration

**Combined Example**:
```python
response = client.beta.messages.create(
    model="claude-opus-4-5-20251101",
    betas=["advanced-tool-use-2025-11-20", "context-management-2025-06-27"],
    tools=tools_with_deferred_loading,
    context_management={
        "edits": [{
            "type": "clear_tool_uses_20250919",
            "trigger": {"type": "input_tokens", "value": 100000},
            "keep": {"type": "tool_uses", "value": 3}
        }]
    },
    messages=messages
)
```

## Related Skills

- **anthropic-expert**: Basic tool use fundamentals, MCP integration, code execution tool
- **claude-context-management**: Server-side tool result clearing, token optimization
- **claude-cost-optimization**: Efficiency tracking, ROI measurement for tool optimizations
- **claude-opus-4-5-guide**: Model capabilities, effort parameter impact on tool use

## References

For detailed implementation patterns, see:

- **`references/tool-search-patterns.md`**: Complete tool search guide (regex + BM25 variants, deferred loading, MCP integration, 10K+ tool scalability)
- **`references/programmatic-tool-calling.md`**: Sandboxed execution patterns, allowed_callers parameter, token efficiency mechanisms, ideal use cases
- **`references/production-patterns.md`**: Architecture patterns from production codebases, security best practices, error handling, observability
- **`references/performance-optimization.md`**: Optimization strategies, caching patterns, latency reduction, efficiency metrics
