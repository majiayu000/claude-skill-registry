---
name: exa-web-search
cluster: community
description: "Exa.ai semantic web search: neural search, crawl, contents extraction, highlights, date filtering"
tags: ["search","exa","semantic","web"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "exa semantic web search neural crawl contents extract highlight"
---

# exa-web-search

## Purpose
This skill enables semantic web searches using Exa.ai's neural engine, allowing for advanced querying, web crawling, content extraction, highlighting key sections, and date-based filtering. It's designed for AI agents to fetch and process web data efficiently in tasks requiring real-time or historical information retrieval.

## When to Use
Use this skill when you need to perform semantic searches beyond keyword matching, such as analyzing trends from recent articles, extracting data from crawled pages, or highlighting relevant content. Apply it in research tasks, content aggregation, or when integrating web data into AI workflows, especially if other search tools fail to capture contextual nuances.

## Key Capabilities
- Semantic search using neural networks for understanding query intent.
- Web crawling to fetch pages dynamically based on queries.
- Content extraction to pull text, images, or metadata from pages.
- Highlighting of key phrases or sections in results.
- Date filtering to limit results to a specific range, e.g., last 7 days.
- Supports pagination and result limits for scalable queries.

## Usage Patterns
Always initialize with authentication via environment variables. For CLI, run searches in a loop for batch processing. In code, use asynchronous API calls to avoid blocking. Structure queries with specific flags for precision, and parse responses to extract highlights or metadata. Test with small limits first to verify results.

## Common Commands/API
Exa.ai uses a CLI tool and REST API. Set your API key in `$EXA_API_KEY` before use.

CLI Commands:
- Basic search: `exa search --query "AI advancements" --limit 5 --date-after "2023-01-01"`
  Example snippet:
  ```
  result = subprocess.run(['exa', 'search', '--query', 'climate change'], capture_output=True)
  print(result.stdout)
  ```
- With crawling and extraction: `exa search --query "open source tools" --crawl-depth 2 --extract-content`
  Snippet:
  ```
  import subprocess
  output = subprocess.check_output(['exa', 'search', '--query', 'web frameworks', '--highlight'])
  ```

API Endpoints:
- Primary endpoint: `POST https://api.exa.ai/v1/search`
  Request body format (JSON):
  ```
  {
    "query": "machine learning",
    "limit": 10,
    "date_after": "2022-01-01",
    "crawl_depth": 1
  }
  ```
  Snippet:
  ```
  import requests
  headers = {'Authorization': f'Bearer {os.environ.get("EXA_API_KEY")}'}
  response = requests.post('https://api.exa.ai/v1/search', headers=headers, json={"query": "neural networks"})
  data = response.json()
  ```
- Error checking endpoint: `GET https://api.exa.ai/v1/status` to verify service availability.

Config Formats:
- Use a `.exa-config.json` file for persistent settings:
  ```
  {
    "default_limit": 20,
    "api_endpoint": "https://api.exa.ai/v1/search"
  }
  ```
  Load it in code: `with open('.exa-config.json') as f: config = json.load(f)`

## Integration Notes
Integrate by setting `$EXA_API_KEY` in your environment or passing it via headers. For AI agents, wrap API calls in try-except blocks and use async libraries like `aiohttp` for non-blocking operations. Combine with other skills by piping results, e.g., feed search outputs to a summarization tool. Ensure rate limits (e.g., 100 requests/min) are respected by adding delays. For clustering, reference the 'community' tag to link with related skills.

## Error Handling
Check HTTP status codes in API responses (e.g., 401 for unauthorized, access via `response.status_code`). For CLI, parse stderr for messages like "Query exceeded limits". Common errors include invalid queries (fix by validating input strings) or network issues (retry with exponential backoff). In code, use:
```
if response.status_code != 200:
    raise Exception(f"API error: {response.json().get('error')}")
```
Log errors with details like error codes and retry up to 3 times for transient failures.

## Graph Relationships
- Related to: search skills (e.g., general web search tools)
- Depends on: authentication services for API access
- Complements: data extraction skills for post-processing results
- Clusters with: community tools for semantic analysis
