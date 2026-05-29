---
name: grok-search
description: |
  Enhanced web search and real-time content retrieval via Grok API with forced tool routing. Use when: (1) Web search / information retrieval / fact-checking, (2) Webpage content extraction / URL parsing, (3) Breaking knowledge cutoff limits for current information, (4) Real-time news and technical documentation, (5) Multi-source information aggregation. Triggers: "search for", "find information about", "latest news", "current", "fetch webpage", "get content from URL". IMPORTANT: This skill REPLACES built-in WebSearch/WebFetch with GrokSearch MCP tools.
---

# Grok Search

Enhanced web search via Grok API. Supports both MCP server and standalone CLI.

## Execution Methods

### Method 1: MCP Tools (if available)
Use `mcp__groksearch__*` tools directly.

### Method 2: CLI Script (no MCP dependency)
Run `scripts/groksearch_cli.py` via Bash:

```bash
# Prerequisites: pip install httpx tenacity
# Environment: GROK_API_URL, GROK_API_KEY

# Web search
python scripts/groksearch_cli.py web_search --query "search terms" [--platform "GitHub"] [--min-results 3] [--max-results 10]

# Fetch webpage
python scripts/groksearch_cli.py web_fetch --url "https://..." [--out file.md]

# Check config
python scripts/groksearch_cli.py get_config_info [--no-test]

# Switch model
python scripts/groksearch_cli.py switch_model --model "grok-2-latest"

# Toggle built-in tools
python scripts/groksearch_cli.py toggle_builtin_tools --action on|off|status [--root /path/to/project]
```

## Tool Routing Policy

### Forced Replacement Rules

| Scenario | Disabled | Force Use |
|----------|----------|-----------|
| Web Search | `WebSearch` | `mcp__groksearch__web_search` or CLI `web_search` |
| Web Fetch | `WebFetch` | `mcp__groksearch__web_fetch` or CLI `web_fetch` |

### Tool Capability Matrix

| Tool | Parameters | Output |
|------|------------|--------|
| `web_search` | `query`(required), `platform`/`min_results`/`max_results`(optional) | `[{title,url,description}]` |
| `web_fetch` | `url`(required), `out`(optional) | Structured Markdown |
| `get_config_info` | `no_test`(optional) | `{api_url,status,connection_test}` |
| `switch_model` | `model`(required) | `{previous_model,current_model}` |
| `toggle_builtin_tools` | `action`(on/off/status), `root`(optional) | `{blocked,deny_list}` |

## Search Workflow

### Phase 1: Query Construction
- **Intent Recognition**: Broad search → `web_search` | Deep retrieval → `web_fetch`
- **Parameter Optimization**: Set `platform` for specific sources, adjust result counts

### Phase 2: Search Execution
1. Start with `web_search` for structured summaries
2. Use `web_fetch` on key URLs if summaries insufficient
3. Retry with adjusted query if first round unsatisfactory

### Phase 3: Result Synthesis
1. Cross-reference multiple sources
2. **Must annotate source and date** for time-sensitive info
3. **Must include source URLs**: `Title [<sup>1</sup>](URL)`

## Error Handling

| Error | Recovery |
|-------|----------|
| Connection Failure | Run `get_config_info`, verify API URL/Key |
| No Results | Broaden search terms |
| Fetch Timeout | Try alternative sources |

## Anti-Patterns

| Prohibited | Correct |
|------------|---------|
| No source citation | Include `Source [<sup>1</sup>](URL)` |
| Give up after one failure | Retry at least once |
| Use built-in WebSearch/WebFetch | Use GrokSearch tools/CLI |
