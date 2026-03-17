---
name: exa
description: |
  High-precision semantic search and content retrieval via Exa API. Use when: (1) Deep research requiring semantic understanding, (2) Code documentation and examples lookup, (3) Company/professional research, (4) AI-powered comprehensive research tasks, (5) URL content extraction with structured output. Triggers: "research", "find papers", "code examples", "company info", "LinkedIn profiles", "deep analysis". Differentiator: Exa excels at semantic/neural search while grok-search is better for real-time news and general web content.
---

# Exa Search

High-precision semantic search via Exa API. Standalone CLI only (no MCP dependency).

## Execution Method

Run `scripts/exa_cli.py` via Bash:

```bash
# Prerequisites: pip install httpx tenacity
# Environment: EXA_API_KEY (required), EXA_API_URL (optional, default: https://api.exa.ai)
```

## Available Tools

### Search Tools

```bash
# Basic semantic search
python scripts/exa_cli.py web_search_exa --query "emerging patterns in TypeScript" [--num-results 10] [--type auto|keyword|neural] [--livecrawl always|fallback|never]

# Advanced search with filters
python scripts/exa_cli.py web_search_advanced_exa --query "machine learning papers" \
  [--include-domains arxiv.org,github.com] [--exclude-domains medium.com] \
  [--start-date 2024-01-01] [--end-date 2024-12-31] \
  [--text] [--highlights] [--summary] [--out results.json]

# Deep search with query expansion
python scripts/exa_cli.py deep_search_exa --objective "foundations of quantum error correction" [--additional-queries "query1|query2"]

# Company research
python scripts/exa_cli.py company_research_exa --company "Anthropic" [--num-results 10]

# LinkedIn profile search
python scripts/exa_cli.py linkedin_search_exa --query "AI researchers at Stanford" [--num-results 10]
```

### Content Tools

```bash
# Extract content from URL
python scripts/exa_cli.py crawling_exa --url "https://example.com/article" \
  [--max-chars 5000] [--livecrawl always|fallback|never] \
  [--text] [--highlights] [--summary] [--out content.json]

# Get code context (documentation, examples)
python scripts/exa_cli.py get_code_context_exa --query "React useState hook examples" [--tokens-num 10000] [--out code.json]
```

### Research Tools

```bash
# Start AI research task
python scripts/exa_cli.py deep_researcher_start --instructions "Analyze the impact of LLMs on software development" [--model exa-research|exa-research-pro]
# Returns: {"taskId": "abc123", ...}

# Check research status
python scripts/exa_cli.py deep_researcher_check --task-id "abc123" [--out report.json]
# Status: running → completed | failed
```

### Configuration

```bash
# Check config and test connection
python scripts/exa_cli.py get_config_info [--no-test]
```

## Tool Capability Matrix

| Tool | Required | Optional | Output |
|------|----------|----------|--------|
| `web_search_exa` | `query` | `num-results`, `type`, `livecrawl` | Search results JSON |
| `web_search_advanced_exa` | `query` | `include-domains`, `exclude-domains`, `start-date`, `end-date`, `text`, `highlights`, `summary` | Filtered results JSON |
| `deep_search_exa` | `objective` | `additional-queries` | Expanded search results |
| `company_research_exa` | `company` | `num-results` | Company info JSON |
| `linkedin_search_exa` | `query` | `num-results` | LinkedIn profiles JSON |
| `crawling_exa` | `url` | `max-chars`, `livecrawl`, `text`, `highlights`, `summary` | Page content JSON |
| `get_code_context_exa` | `query` | `tokens-num` (1000-50000) | Code context JSON |
| `deep_researcher_start` | `instructions` | `model` | Task ID |
| `deep_researcher_check` | `task-id` | - | Status + report |

## Tool Routing Guide

### Exa vs Grok-Search

| Use Case | Recommended Tool |
|----------|------------------|
| Real-time news, current events | grok-search |
| Semantic/conceptual research | **exa** |
| Code documentation lookup | **exa** (`get_code_context_exa`) |
| Company/professional research | **exa** |
| General web content fetch | grok-search |
| Academic papers, technical docs | **exa** |
| AI-powered deep research | **exa** (`deep_researcher_*`) |

## Workflow Patterns

### Pattern 1: Quick Semantic Search
```bash
python scripts/exa_cli.py web_search_exa --query "best practices for React hooks" --num-results 5
```

### Pattern 2: Filtered Research
```bash
python scripts/exa_cli.py web_search_advanced_exa --query "transformer architecture" \
  --include-domains arxiv.org,papers.nips.cc --start-date 2023-01-01 --text --summary
```

### Pattern 3: Deep Research Task
```bash
# Start research
python scripts/exa_cli.py deep_researcher_start --instructions "Compare RAG vs fine-tuning for domain adaptation"
# Poll until completed
python scripts/exa_cli.py deep_researcher_check --task-id "<taskId>" --out research_report.json
```

## Error Handling

| Error | Recovery |
|-------|----------|
| `EXA_API_KEY not configured` | Set environment variable or use `--api-key` |
| HTTP 429 (Rate limit) | Automatic retry with exponential backoff |
| HTTP 401 (Unauthorized) | Verify API key is valid |
| Timeout | Retry or reduce `num-results` |

## Output Format

All commands output JSON to stdout. Use `--out <file>` to write to file instead.

```json
{
  "results": [
    {"title": "...", "url": "...", "text": "...", "publishedDate": "..."}
  ]
}
```
