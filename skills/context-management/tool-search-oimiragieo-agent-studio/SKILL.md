---
name: tool-search
description: Semantic tool search with embeddings for scalable tool discovery. Enables on-demand tool loading to reduce context usage by 90%+ for large tool libraries.
allowed-tools: read, write, grep, glob
version: 1.0
best_practices:
  - Use for tool libraries with 10+ tools
  - Keep 3-5 most-used tools always loaded
  - Use clear, descriptive tool names
  - Add system prompt guidance
error_handling: graceful
streaming: supported
---

# Tool Search Skill

## Identity

Tool Search - Provides semantic tool discovery using embeddings to scale from dozens to thousands of tools with 90%+ context reduction.

## Capabilities

- **Semantic Tool Search**: Find relevant tools based on task context
- **Embedding-Based Matching**: Use embeddings for accurate tool discovery
- **On-Demand Loading**: Load tools only when needed
- **Context Efficiency**: 90%+ reduction in tool definition tokens

## The Problem

Traditional tool loading:

- All tools loaded upfront
- 58 tools = ~55K tokens
- Context fills quickly
- Hard to scale beyond ~100 tools

## The Solution

Tool Search with Embeddings:

- Only Tool Search Tool loaded initially (~500 tokens)
- Tools discovered on-demand via semantic search
- 3-5 relevant tools loaded per search (~3K tokens)
- Total: ~8.7K tokens vs. ~77K traditional (85% reduction)

## How It Works

1. **Initial State**: Only Tool Search Tool + critical tools loaded
2. **Tool Discovery**: Agent searches for tools based on task
3. **Semantic Matching**: Embeddings match tools to task context
4. **Tool Expansion**: Matching tools expanded into full definitions
5. **Tool Use**: Agent uses discovered tools

## Configuration

### MCP Configuration (`.claude/.mcp.json`)

```json
{
  "betaFeatures": ["advanced-tool-use-2025-11-20"],
  "toolSearch": {
    "enabled": true,
    "autoEnableThreshold": 20,
    "defaultDeferLoading": true
  },
  "mcpServers": {
    "repo": {
      "deferLoading": true,
      "alwaysLoadTools": ["search_code", "read_file"]
    },
    "github": {
      "deferLoading": true,
      "alwaysLoadTools": ["create_pull_request", "get_issue"]
    }
  }
}
```

### Always Load Critical Tools

Keep 3-5 most-used tools always loaded:

- Core file operations: `read_file`, `write_file`, `search_code`
- Essential integrations: `create_pull_request`, `get_issue`
- Frequently used: `take_screenshot`, `navigate_page`

## Usage Patterns

### When to Use Tool Search

**Most Beneficial When**:

- Tool definitions consuming >10K tokens
- Tool library has 10+ tools
- Experiencing tool selection accuracy issues
- Building MCP-powered systems with multiple servers

**Less Beneficial When**:

- Small tool library (<10 tools)
- All tools used frequently in every session
- Tool definitions are compact

### Tool Discovery

**Agent Workflow**:

1. Agent needs capability (e.g., "create a pull request")
2. Agent searches: "github pull request creation"
3. Tool Search returns: `create_pull_request` tool
4. Tool expanded into full definition
5. Agent uses tool

**Example**:

```
User: "Create a pull request for my changes"

Agent searches: "github pull request creation"
Tool Search finds: create_pull_request tool
Tool loaded and used
```

## Best Practices

### 1. Clear Tool Names and Descriptions

**Good**:

```json
{
  "name": "search_customer_orders",
  "description": "Search for customer orders by date range, status, or total amount. Returns order details including items, shipping, and payment info."
}
```

**Bad**:

```json
{
  "name": "query_db_orders",
  "description": "Execute order query"
}
```

### 2. System Prompt Guidance

Add guidance in agent prompts:

```
You have access to tools for Slack messaging, Google Drive file management,
Jira ticket tracking, and GitHub repository operations. Use the tool search
to find specific capabilities when needed.
```

### 3. Keep Critical Tools Always Loaded

Don't defer loading for:

- Core file operations
- Essential integrations
- Frequently used tools

### 4. Monitor Tool Usage

Track which tools are discovered:

- Most searched tools
- Tool discovery patterns
- Context savings achieved

## Implementation

### Embedding-Based Tool Search

The tool search uses embeddings to match tools to queries:

1. **Tool Indexing**: Create embeddings for all tool definitions
2. **Query Embedding**: Create embedding for user query
3. **Similarity Search**: Find tools with similar embeddings
4. **Tool Expansion**: Load matching tools into context

### Tool Search Tool

The Tool Search Tool itself:

- Searches tool library semantically
- Returns relevant tools based on query
- Expands tools into full definitions
- Maintains tool index

## Benefits

### Context Efficiency

- **85% reduction** in tool definition tokens
- **52.5% total context** (down from 87%)
- **Within optimal range** (60-70% target)

### Improved Accuracy

- **11% improvement** in tool selection accuracy
- **79.5% → 88.1%** (Opus 4.5)
- Better tool matching for complex queries

### Scalability

- Scales to **thousands of tools**
- No context limit concerns
- Dynamic tool discovery

## Examples

### Example 1: GitHub Operations

```
User: "Create a pull request"

Agent workflow:
1. Searches: "github pull request creation"
2. Tool Search finds: create_pull_request tool
3. Tool loaded (3K tokens)
4. Agent uses tool
5. Total context: ~8.7K tokens (vs. 55K traditional)
```

### Example 2: File Operations

```
User: "Search for authentication code"

Agent workflow:
1. Searches: "code search file operations"
2. Tool Search finds: search_code, read_file tools
3. Tools loaded (5K tokens)
4. Agent uses tools
```

### Example 3: Multiple Integrations

```
User: "Check Slack messages and create Jira ticket"

Agent workflow:
1. Searches: "slack message reading"
2. Tool Search finds: read_slack_message tool
3. Searches: "jira ticket creation"
4. Tool Search finds: create_jira_ticket tool
5. Both tools loaded (6K tokens total)
```

## Integration

### With MCP Servers

Tool search works with MCP servers:

- GitHub MCP: 35 tools → 3-5 loaded on-demand
- Slack MCP: 11 tools → 2-3 loaded on-demand
- Custom MCPs: Any number of tools → Loaded as needed

### With Agent System

All agents benefit from tool search:

- Reduced context usage
- Better tool selection
- Scalable tool libraries

## Troubleshooting

### Tools Not Found

- Check tool names and descriptions are clear
- Verify tool search is enabled
- Review search queries
- Check tool index is up to date

### Context Still High

- Verify deferLoading is enabled
- Check alwaysLoadTools list (should be minimal)
- Review tool definitions (may be too verbose)
- Monitor actual tool usage

### Tool Selection Issues

- Improve tool descriptions
- Add more context to search queries
- Review tool naming conventions
- Check embedding quality

## Integration with Programmatic Tool Calling (PTC)

Tool Search works excellently with Programmatic Tool Calling:

1. **Tool Search** finds relevant tools (on-demand loading)
2. **PTC** orchestrates tools efficiently (reduced context)
3. **Result**: Optimal tool usage with minimal token consumption

**Example Workflow**:

```python
# Tool Search finds tools
tools = search_tools("github issue management")

# PTC orchestrates multiple tool calls
team = await get_team_members("engineering")
issues = await asyncio.gather(*[
    get_issue(member["github_username"]) for member in team
])
# Only final results in context, not all intermediate data
```

See [PTC Patterns Guide](../docs/PTC_PATTERNS.md) for comprehensive PTC documentation.

## Related Documentation

- [Advanced Tool Use](../docs/ADVANCED_TOOL_USE.md) - Comprehensive tool use guide
- [PTC Patterns](../docs/PTC_PATTERNS.md) - Programmatic Tool Calling patterns
- [Context Optimization](../docs/CONTEXT_OPTIMIZATION.md) - Context management

## References

- [Tool Search with Embeddings Cookbook](https://github.com/anthropics/anthropic-cookbook/tree/main/tool_use/tool_search_with_embeddings.ipynb)
- [Programmatic Tool Calling Cookbook](https://github.com/anthropics/anthropic-cookbook/tree/main/tool_use/programmatic_tool_calling_ptc.ipynb)
- [Advanced Tool Use Documentation](https://docs.claude.com/en/docs/agents-and-tools/advanced-tool-use)
