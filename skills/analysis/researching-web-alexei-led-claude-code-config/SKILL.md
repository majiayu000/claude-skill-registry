---
name: researching-web
description: Web research via Perplexity AI. Use for technical comparisons (X vs Y), best practices, industry standards, documentation. Triggers on "research", "compare", "vs", "best practice", "which is better", "pros and cons".
context: fork
allowed-tools:
  - Task
  - Read
  - Grep
  - Glob
  - WebFetch
  - mcp__perplexity-ask__perplexity_ask
---

# Web Research with Perplexity

Two modes: **quick** (MCP direct) or **deep** (Task-based with context).

## Best For

- Technology comparisons (X vs Y)
- Best practices, industry standards
- OWASP, security guidelines
- Documentation references
- Stable technical content

## Quick Mode (Simple Queries)

Use MCP directly for fast, simple lookups:

```json
mcp__perplexity-ask__perplexity_ask({
  "messages": [{ "role": "user", "content": "Your research question" }]
})
```

## Deep Mode (Context-Aware Research)

For codebase-aware research, spawn the **perplexity-researcher** agent.

### Foreground (blocking)

```
Task(subagent_type="perplexity-researcher", prompt="Research: <topic>")
```

### Background (recommended for context efficiency)

Run in background to avoid polluting main context:

```
Task(
  subagent_type="perplexity-researcher",
  prompt="Research: <topic>",
  run_in_background=true
)
```

Retrieve results when ready:

```
TaskOutput(task_id="<agent_id>", block=true)
```

**Use background mode when:**

- Running multiple research queries in parallel
- Main task can continue while research runs
- Want to keep main context clean

### When to Use Deep Mode

- User asks "best way to do X" (needs to compare with current code)
- Researching improvements to existing code
- Need to understand if recommendations apply to current stack

## Query Formulation Tips

- Be specific: "Go 1.25 error handling best practices 2025"
- Include context: "Redis vs Memcached for session storage in Go services"
- Ask comparisons: "Pros and cons of gRPC vs REST for microservices"
- Include year: "Claude Code context optimization 2025"

## Reference Following (Deep Research)

After Perplexity returns results with citations:

1. **Review all cited URLs** in the response
2. **WebFetch top 2-3 most relevant sources** for deeper context
3. **Synthesize comprehensive answer** combining all sources

```
# After Perplexity response with citations
WebFetch(url="<cited-url-1>", prompt="Extract key details about <topic>")
WebFetch(url="<cited-url-2>", prompt="Extract implementation examples")
```

Use reference following when:

- Initial answer is high-level and needs specifics
- User asks "tell me more" or "dig deeper"
- Implementing something that needs detailed guidance

## Output Structure

```markdown
## Summary

[Key findings - 2-3 sentences]

## Details

[Organized findings by topic]

## Recommendations

[Actionable items for the project]

## Sources

- [Source](url) - [what was learned]
```
