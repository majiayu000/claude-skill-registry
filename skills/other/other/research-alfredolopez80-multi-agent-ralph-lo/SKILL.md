---
# VERSION: 2.88.0
name: research
description: "Comprehensive research skill using Zai MCP web search and native Claude Code tools"
---

# Research Skill - Multi-Agent Ralph v2.88

**Smart Research with Zai MCP Integration** - Leverages Zai MCP for comprehensive web search, article fetching, and content analysis.

Based on the principle that research should be thorough, well-sourced, and actionable.

## Quick Start

```bash
# Via skill invocation
/research Latest React 19 patterns and best practices

# Via CLI
ralph research "TypeScript 5.0 performance optimizations"

# Focus on specific sources
/research "Next.js App Router" --sources github,docs
```

## Key Changes in v2.88

- **Zai MCP as primary**: Uses `mcp__web-search-prime__webSearchPrime` instead of Minimax
- **Native WebFetch**: Uses Claude Code's native WebFetch for content retrieval
- **Multi-source fetching**: Supports GitHub, CSDN, Juejin, Linux.do article extraction
- **Model-agnostic**: Works with any model configured in settings.json

## Available Tools

### 1. mcp__web-search-prime__webSearchPrime (Primary Search)

**Purpose:** Comprehensive web search with high-quality results

**Parameters:**
```yaml
search_query: string      # The search query (max 70 characters recommended)
content_size: string      # "medium" (400-600 words) or "high" (2500 words)
location: string          # "cn" (Chinese) or "us" (non-Chinese)
search_recency_filter: string  # oneDay, oneWeek, oneMonth, oneYear, noLimit
search_domain_filter: string   # Optional: limit to specific domain
```

**Optimal Patterns:**
```yaml
# Good: Specific, time-bounded
mcp__web-search-prime__webSearchPrime:
  search_query: "React 19 useOptimistic hook examples 2025"
  search_recency_filter: "oneMonth"
  content_size: "medium"

# Good: Error-focused debugging
mcp__web-search-prime__webSearchPrime:
  search_query: "TypeError cannot read property undefined Next.js 15"
  location: "us"

# Good: Documentation search
mcp__web-search-prime__webSearchPrime:
  search_query: "Claude Code MCP configuration"
  search_domain_filter: "docs.anthropic.com"

# Bad: Too vague
mcp__web-search-prime__webSearchPrime:
  search_query: "javascript"  # Too broad, be specific
```

### 2. Native WebFetch (Content Retrieval)

**Purpose:** Fetch and analyze full web page content

**When to Use:**
- Deep-dive into specific articles found via search
- Documentation reading
- GitHub repository exploration
- API documentation analysis

### 3. mcp__web-search__fetchGithubReadme

**Purpose:** Extract README content from GitHub repositories

**Parameters:**
```yaml
url: string  # GitHub repository URL
```

**Example:**
```yaml
mcp__web-search__fetchGithubReadme:
  url: "https://github.com/vercel/next.js"
```

### 4. mcp__web-reader__webReader

**Purpose:** Convert URL content to LLM-friendly format

**Parameters:**
```yaml
url: string              # URL to fetch and read
return_format: string    # "markdown" (default) or "text"
retain_images: boolean   # Keep images (default: true)
with_links_summary: boolean  # Include links summary
with_images_summary: boolean # Include images summary
```

**Example:**
```yaml
mcp__web-reader__webReader:
  url: "https://docs.anthropic.com/claude/docs"
  return_format: "markdown"
  with_links_summary: true
```

### 5. Chinese Article Fetchers

**mcp__web-search__fetchCsdnArticle**
```yaml
url: string  # CSDN article URL
```

**mcp__web-search__fetchJuejinArticle**
```yaml
url: string  # Juejin article URL
```

**mcp__web-search__fetchLinuxDoArticle**
```yaml
url: string  # Linux.do post URL
```

## Research Workflow (5 Steps)

### Step 1: INITIAL SEARCH

```yaml
# Broad search first
mcp__web-search-prime__webSearchPrime:
  search_query: "${TOPIC} overview guide 2025"
  content_size: "high"
  search_recency_filter: "oneMonth"
```

### Step 2: REFINE & DEEPEN

```yaml
# Targeted follow-up searches based on initial results
mcp__web-search-prime__webSearchPrime:
  search_query: "${SPECIFIC_ASPECT} implementation ${TOPIC}"
  search_recency_filter: "oneWeek"
```

### Step 3: FETCH CONTENT

```yaml
# For documentation sites
mcp__web-reader__webReader:
  url: "${DOC_URL}"
  return_format: "markdown"

# For GitHub repos
mcp__web-search__fetchGithubReadme:
  url: "${REPO_URL}"
```

### Step 4: SYNTHESIZE

Compile findings into structured report:
- **Summary**: Key findings in 2-3 sentences
- **Sources**: All URLs with brief descriptions
- **Details**: Relevant code snippets and explanations
- **Recommendations**: Suggested approach based on research
- **Related Topics**: Areas for further exploration

### Step 5: PERSIST

Save research to memory for future reference:
```bash
ralph memvid save "Research on ${TOPIC}: [key findings]"
```

## Research Templates

### Technology Research

```yaml
# 1. Official docs
mcp__web-search-prime__webSearchPrime:
  search_query: "${TECH} official documentation"
  search_domain_filter: "official-site.com"

# 2. Best practices
mcp__web-search-prime__webSearchPrime:
  search_query: "${TECH} best practices 2025"

# 3. GitHub examples
mcp__web-search-prime__webSearchPrime:
  search_query: "${TECH} examples github"
```

### Error Research

```yaml
# 1. Exact error message
mcp__web-search-prime__webSearchPrime:
  search_query: "${ERROR_MESSAGE} ${FRAMEWORK}"

# 2. Stack Overflow solutions
mcp__web-search-prime__webSearchPrime:
  search_query: "site:stackoverflow.com ${ERROR_MESSAGE}"

# 3. GitHub issues
mcp__web-search-prime__webSearchPrime:
  search_query: "site:github.com ${ERROR_MESSAGE}"
```

### Security Research

```yaml
# 1. CVE lookup
mcp__web-search-prime__webSearchPrime:
  search_query: "CVE ${VERSION} vulnerability"

# 2. Security advisories
mcp__web-search-prime__webSearchPrime:
  search_query: "${PACKAGE} security advisory 2025"

# 3. Exploit database
mcp__web-search-prime__webSearchPrime:
  search_query: "${CVE_ID} exploit"
```

## Integration with Ralph Loop

```yaml
# Research phase in orchestrator
Task:
  prompt: |
    Research latest patterns for $TOPIC using mcp__web-search-prime__webSearchPrime.
    Use mcp__web-reader__webReader for detailed content.
    Compile findings into structured report with sources.

# Code research
Task:
  prompt: |
    Search for $TOPIC implementation examples on GitHub.
    Use mcp__web-search__fetchGithubReadme to analyze repositories.
    Identify best patterns and anti-patterns.
```

## Comparison: Zai MCP vs Minimax

| Feature | Zai MCP | Minimax MCP |
|---------|---------|-------------|
| Web Search | webSearchPrime | web_search |
| Content Quality | High (2500 words max) | Medium |
| Chinese Content | Excellent (CSDN, Juejin) | Basic |
| GitHub Integration | fetchGithubReadme | None |
| URL Reader | webReader | None |
| Domain Filtering | Yes | No |
| Recency Filter | Yes | No |
| Cost | Free (no API key) | ~$0.008/query |

## When to Use Each Tool

| Scenario | Recommended Tool |
|----------|------------------|
| General web search | mcp__web-search-prime__webSearchPrime |
| Chinese tech articles | mcp__web-search__fetchCsdnArticle, fetchJuejinArticle |
| GitHub repositories | mcp__web-search__fetchGithubReadme |
| Documentation reading | mcp__web-reader__webReader |
| Real-time data | Native WebFetch |
| Code search in repo | Grep, Glob (not web search) |

## Anti-Patterns

- **Too broad queries**: "javascript" - always be specific
- **Skipping sources**: Always cite URLs
- **Ignoring recency**: Use recency filter for fast-moving topics
- **Single source**: Cross-reference multiple sources
- **No synthesis**: Don't just list results, analyze them
- **Missing memory**: Save learnings for future sessions

## Output Format

Structure research reports as:

```markdown
# Research: [TOPIC]

**Date**: YYYY-MM-DD
**Sources**: X articles analyzed

## Summary
[2-3 sentence key findings]

## Key Findings
1. [Finding 1]
   - Source: [URL]
   - Details: [Explanation]

2. [Finding 2]
   - Source: [URL]
   - Details: [Explanation]

## Code Examples
```language
// Relevant code snippets
```

## Recommendations
1. [Recommendation 1]
2. [Recommendation 2]

## Related Topics
- [Topic for further research]

## Sources
1. [Title](URL) - [Brief description]
2. [Title](URL) - [Brief description]
```

## CLI Commands

```bash
# Standard research
ralph research "topic description"

# With source focus
ralph research "topic" --sources github,docs

# Chinese content
ralph research "topic" --location cn
```

## Related Skills

- `/orchestrator` - Full orchestration with research phase
- `/smart-fork` - Pattern extraction from external repos
- `/clarify` - Requirement clarification with research

## Agent Teams Integration (v2.88)

**Optimal Scenario**: B (Pure Custom Subagents)

### Why Scenario B for Research
- **Independent execution**: Research is mostly self-contained
- **Specialization > Coordination**: Tool expertise matters more than inter-agent coordination
- **Simpler setup**: No team overhead for single-purpose research tasks
- **Tool restrictions**: ralph-researcher has specialized tools (WebSearch, WebFetch)

### Scenario Analysis
| Criterion | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| Coordination Need | 25% | 3/10 | Research is independent |
| Specialization Need | 25% | 9/10 | Specialized web tools required |
| Quality Gate Need | 20% | 5/10 | Moderate validation needs |
| Tool Restriction Need | 15% | 8/10 | Read-only tools important |
| Scalability | 15% | 7/10 | Scales with topic complexity |
| **Total** | 100% | **7.5/10** | Scenario B optimal |

### Workflow
```yaml
# Scenario B: Direct spawn without TeamCreate
Task(subagent_type="ralph-researcher", prompt="Research ${TOPIC}")
→ Execute with specialized tools
→ Compile structured report
→ Return findings
```

### Usage

**Direct Spawn (Recommended)**:
```yaml
Task:
  subagent_type: "ralph-researcher"
  prompt: |
    Research ${TOPIC} using:
    1. mcp__web-search-prime__webSearchPrime for initial search
    2. mcp__web-reader__webReader for content extraction
    3. mcp__web-search__fetchGithubReadme for GitHub repos
    Compile into structured report with all sources.
```

**Parallel Research (Multiple Topics)**:
```yaml
# Spawn multiple researchers for different topics
Task(subagent_type="ralph-researcher", prompt="Research React 19 features")
Task(subagent_type="ralph-researcher", prompt="Research TypeScript 5.5")
Task(subagent_type="ralph-researcher", prompt="Research Node.js performance")
# Results aggregated independently
```

## References

- [Zai MCP Documentation](https://github.com/mikekelly/claude-sneakpeek)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Web Search Tool Documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)
