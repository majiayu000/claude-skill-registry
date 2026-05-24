---
name: web-search-tavily
description: "Search the web using Tavily API for high-quality, AI-optimized results with advanced filtering options. Use when you need structured search results, domain filtering, relevance scores, or AI-generated answer summaries. Requires TAVILY_API_KEY. Keywords: tavily, advanced search, filtered search, domain filtering, relevance scoring."
license: MIT
compatibility: Requires TAVILY_API_KEY environment variable and internet access
metadata:
  author: agent-skills
  version: "1.0"
---

# Web Search (Tavily API)

Search the web using Tavily's AI-optimized search API. Returns high-quality, structured results with relevance scores and optional AI-generated summaries.

**Note:** This skill requires a Tavily API key. For basic web search using the agent's built-in capability, see `web-search`.

## When to Use This Skill

Use this skill when:
- You need to find current information not in your training data
- The user asks about recent events, news, or updates
- You need to verify facts or find authoritative sources
- Research requires real-time web data
- Keywords mentioned: search, look up, find online, current, latest, news

Do NOT use this skill when:
- Information is already in your knowledge base and doesn't need verification
- The user asks about historical facts that don't change
- You're working with local files or code (use other tools)
- A more specific skill exists for the task (e.g., documentation lookup)

## Prerequisites

Before using this skill, ensure:
- **TAVILY_API_KEY** environment variable is set with a valid API key
- **Deno** is installed (for running the search script)
- **Internet access** is available

Get a Tavily API key at: https://tavily.com

## Quick Start

Run a simple search:

```bash
deno run --allow-env --allow-net=api.tavily.com scripts/search.ts "your search query"
```

Example with AI-generated answer:

```bash
deno run --allow-env --allow-net=api.tavily.com scripts/search.ts "React 19 new features" --answer
```

## Script Usage

```bash
deno run --allow-env --allow-net=api.tavily.com scripts/search.ts [options] "query"
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--answer` | Include AI-generated answer summary | false |
| `--depth <level>` | Search depth: `basic` or `advanced` | basic |
| `--results <n>` | Number of results to return | 5 |
| `--topic <type>` | Topic type: `general`, `news`, or `finance` | general |
| `--time <range>` | Time filter: `day`, `week`, `month`, or `year` | none |
| `--include <domains>` | Only include these domains (comma-separated) | none |
| `--exclude <domains>` | Exclude these domains (comma-separated) | none |
| `--raw` | Include raw page content in results | false |
| `--json` | Output as JSON (for programmatic use) | false |
| `--help` | Show help message | - |

## Search Parameters

### Topic Types

- **general** (default): Broad web search across all content types
- **news**: Prioritizes news articles and current events
- **finance**: Focuses on financial information and market data

### Search Depth

- **basic** (default): Fast search, good for most queries
- **advanced**: Deeper search with more comprehensive results (slower, higher API cost)

### Time Range

Filter results by recency:
- **day**: Last 24 hours
- **week**: Last 7 days
- **month**: Last 30 days
- **year**: Last 365 days

### Domain Filtering

Control which sites appear in results:

```bash
# Only search documentation sites
scripts/search.ts "React hooks" --include docs.react.dev,developer.mozilla.org

# Exclude social media
scripts/search.ts "AI news" --exclude twitter.com,reddit.com
```

## Output Format

### Human-Readable Output (default)

```
🔍 Search: "React 19 new features"

Found 5 results in 234ms

📝 AI Answer:
────────────────────────────────────────────────────────────
React 19 introduces several new features including...
────────────────────────────────────────────────────────────

1. React 19 Release Notes
   https://react.dev/blog/2024/04/25/react-19
   React 19 is now available on npm! This release includes...
   Score: 0.987

2. What's New in React 19
   https://example.com/react-19-features
   A comprehensive overview of React 19's new features...
   Score: 0.945
```

### JSON Output (--json)

```json
{
  "query": "React 19 new features",
  "results": [
    {
      "title": "React 19 Release Notes",
      "url": "https://react.dev/blog/2024/04/25/react-19",
      "content": "React 19 is now available on npm...",
      "score": 0.987,
      "published_date": "2024-04-25"
    }
  ],
  "answer": "React 19 introduces several new features...",
  "response_time": 234
}
```

### Result Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Page title |
| `url` | string | Source URL |
| `content` | string | Relevant excerpt from the page |
| `score` | number | Relevance score (0-1, higher is better) |
| `published_date` | string | Publication date (if available) |
| `raw_content` | string | Full page content (only with --raw) |

## Examples

### Example 1: Current Events Search

**Scenario**: Find recent news about a technology topic

```bash
scripts/search.ts "OpenAI GPT-5 announcement" --topic news --time week --answer
```

**Expected output**: Recent news articles about GPT-5, with an AI-generated summary

### Example 2: Documentation Lookup

**Scenario**: Find specific technical documentation

```bash
scripts/search.ts "Deno deploy edge functions tutorial" --depth advanced --results 10
```

**Expected output**: Comprehensive results from documentation and tutorial sites

### Example 3: Fact Verification

**Scenario**: Verify a specific claim or statistic

```bash
scripts/search.ts "world population 2024" --include un.org,worldbank.org,census.gov --json
```

**Expected output**: JSON results from authoritative sources for programmatic verification

### Example 4: Financial Research

**Scenario**: Research market information

```bash
scripts/search.ts "NVIDIA stock analysis 2024" --topic finance --answer
```

**Expected output**: Financial analysis and market data with AI summary

## Common Issues and Solutions

### Issue: "TAVILY_API_KEY environment variable is not set"

**Symptoms**: Script exits immediately with API key error

**Solution**:
1. Get an API key from https://tavily.com
2. Set the environment variable:
   ```bash
   export TAVILY_API_KEY="your-api-key-here"
   ```
3. Or run with the variable inline:
   ```bash
   TAVILY_API_KEY="your-key" deno run --allow-env --allow-net=api.tavily.com scripts/search.ts "query"
   ```

### Issue: "Invalid Tavily API key"

**Symptoms**: 401 authentication error

**Solution**:
1. Verify your API key is correct (no extra spaces)
2. Check if your API key has expired
3. Verify your Tavily account is active

### Issue: "Tavily API rate limit exceeded"

**Symptoms**: 429 error response

**Solution**:
1. Wait a moment and retry
2. Reduce request frequency
3. Consider upgrading your Tavily plan for higher limits

### Issue: No results returned

**Symptoms**: Empty results array

**Solution**:
1. Try broader search terms
2. Remove domain filters that might be too restrictive
3. Check if the topic exists online
4. Try `--depth advanced` for harder queries

## Limitations

This skill has the following limitations:
- Requires active internet connection
- API rate limits apply based on your Tavily plan
- Results depend on Tavily's index coverage
- Cannot access paywalled or login-required content
- Real-time accuracy depends on Tavily's crawling frequency
- Maximum query length and result count have API limits

## Related Skills

- **research-workflow**: For comprehensive research projects that use multiple searches with planning and synthesis
