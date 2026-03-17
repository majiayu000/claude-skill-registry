---
# VERSION: 2.88.0
name: minimax-mcp-usage
description: "[DEPRECATED] Use /research skill with Zai MCP instead - Optimal patterns for MiniMax MCP tools"
---

> **DEPRECATED (v2.88.0)**: This skill is deprecated. Use the `/research` skill instead, which leverages Zai MCP for comprehensive web search with better features:
> - No API key required (free)
> - Chinese content support (CSDN, Juejin, Linux.do)
> - GitHub README extraction
> - URL reader with markdown conversion
> - Domain and recency filtering
>
> See: `.claude/skills/research/SKILL.md`

**ultrathink** - Take a deep breath. We're not here to write code. We're here to make a dent in the universe.

## The Vision
MiniMax queries should be lean, accurate, and decisive.

## Your Work, Step by Step
1. **Choose tool**: web_search vs understand_image.
2. **Craft query**: Specific, time-bound, and focused.
3. **Run analysis**: Collect results with minimal noise.
4. **Synthesize**: Convert outputs into clear guidance.

## Ultrathink Principles in Practice
- **Think Different**: Use the lowest-cost path to truth.
- **Obsess Over Details**: Precision in queries matters.
- **Plan Like Da Vinci**: Decide intent before search.
- **Craft, Don't Code**: Keep results actionable.
- **Iterate Relentlessly**: Refine queries until clear.
- **Simplify Ruthlessly**: Cut vague or broad requests.

# MiniMax MCP Usage Patterns (v2.24)

This skill documents optimal usage patterns for MiniMax MCP tools.

## Available Tools

### 1. mcp__MiniMax__web_search

**Purpose:** Web search with 8% cost of alternatives

**Input:**
```yaml
query: string  # 3-5 keywords, include year for recent topics
```

**Output:**
```json
{
  "organic": [{ "title", "link", "snippet", "date" }],
  "related_searches": [{ "query" }]
}
```

**Optimal Patterns:**

```yaml
# Good: Specific, time-bounded
mcp__MiniMax__web_search:
  query: "React 19 useOptimistic hook examples 2025"

# Good: Error-focused
mcp__MiniMax__web_search:
  query: "TypeError cannot read property undefined Next.js"

# Bad: Too vague
mcp__MiniMax__web_search:
  query: "javascript"  # Too broad
```

### 2. mcp__MiniMax__understand_image

**Purpose:** Image analysis for debugging and review

**Input:**
```yaml
prompt: string       # Clear, specific question about the image
image_source: string # Local path (no @) or HTTPS URL
```

**Optimal Patterns:**

```yaml
# Good: Specific analysis request
mcp__MiniMax__understand_image:
  prompt: "Identify the exact error message and stack trace in this screenshot"
  image_source: "/tmp/error.png"

# Good: UI review
mcp__MiniMax__understand_image:
  prompt: "List all accessibility violations in this form design"
  image_source: "./mockup.png"

# Bad: Vague prompt
mcp__MiniMax__understand_image:
  prompt: "What's this?"  # Too vague
  image_source: "./image.png"
```

## Integration with Ralph Loop

```yaml
# Research phase: Use web_search
Task:
  prompt: |
    Research latest patterns for $TOPIC using mcp__MiniMax__web_search.
    Compile findings into structured report.

# Debugging phase: Use understand_image
Task:
  prompt: |
    Analyze error screenshot at $PATH using mcp__MiniMax__understand_image.
    Identify root cause and suggest fixes.
```

## Cost Analysis

| Operation | MiniMax MCP | Gemini CLI | Savings |
|-----------|-------------|------------|---------|
| Web search | ~$0.008 | ~$0.06 | 87% |
| Image analysis | ~$0.01 | N/A | New capability |

## When NOT to Use

| Scenario | Alternative |
|----------|-------------|
| US-only search | WebSearch (free) |
| Code search | ast-grep MCP (v2.23) |
| Long-form generation | Gemini CLI (1M context) |
| Real-time data | Native WebFetch |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "API key invalid" | Check MINIMAX_API_KEY in ~/.claude.json |
| "Image too large" | Compress to <20MB |
| "Format not supported" | Convert to JPEG/PNG/WebP |
| "No results" | Refine query with more keywords |
