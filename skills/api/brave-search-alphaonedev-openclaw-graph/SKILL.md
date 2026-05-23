---
name: brave-search
cluster: ai-apis
description: "Privacy-first web search API with filters and snippet extraction."
tags: ["ai-apis","api"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "keywords"
---

# brave-search

## Purpose
This skill provides access to Brave Search, a privacy-focused web search API that enables querying the web without tracking, while supporting filters and snippet extraction for AI-driven applications.

## When to Use
Use this when you need quick, private web searches in AI workflows, such as fetching real-time data for responses, avoiding data collection in user queries, or integrating search into tools that require filtered results (e.g., safe search for family-friendly content).

## Key Capabilities
- Perform searches with parameters like query string, result count (e.g., up to 50), and filters for safe search, language (e.g., "en-US"), and country (e.g., "US").
- Extract snippets: API returns JSON with title, URL, and description fields for each result.
- Privacy features: No user tracking; results based on Brave's index.
- Rate limiting: Up to 1000 requests per day per API key, depending on plan.

## Usage Patterns
Always authenticate requests using the $BRAVE_API_KEY environment variable. Make HTTP GET requests to the endpoint with required parameters. Structure queries as URL-encoded strings. For AI agents, integrate via HTTP clients in languages like Python or curl. Test in a loop for pagination by incrementing the 'offset' parameter (e.g., start at 0, then 10).

## Common Commands/API
Endpoint: https://api.search.brave.com/res/v1/web/search  
Authentication: Include header 'X-Subscription-Token: $BRAVE_API_KEY' (set via export BRAVE_API_KEY=your_key in your environment).  
Key parameters: q (query string), count (number of results, e.g., 10), offset (for pagination, e.g., 0), search_lang (e.g., "en"), country (e.g., "US"), safe (e.g., "active" for safe search).  
Example curl command:  
```bash
curl -H "X-Subscription-Token: $BRAVE_API_KEY" "https://api.search.brave.com/res/v1/web/search?q=AI+assistants&count=5&search_lang=en"
```  
Python snippet using requests:  
```python
import requests; import os;  
response = requests.get('https://api.search.brave.com/res/v1/web/search', headers={'X-Subscription-Token': os.environ['BRAVE_API_KEY']], params={'q': 'open source AI', 'count': 3})
```  
Config format: Store API key in .env files as BRAVE_API_KEY=your_key, and load with a library like python-dotenv.

## Integration Notes
Integrate by wrapping API calls in your AI agent's code; use async requests for non-blocking operations. For example, in OpenClaw, call this skill before generating responses that require external data. Handle config by exporting $BRAVE_API_KEY or reading from a secure vault. If combining with other AI APIs, chain this skill after tools like language models to enrich outputs (e.g., search for context, then summarize). Avoid caching results longer than 1 hour due to web content volatility.

## Error Handling
Check HTTP status codes: 200 for success, 401 for invalid API key (retry after verifying $BRAVE_API_KEY), 429 for rate limit (wait and retry with exponential backoff, e.g., 5-10 seconds). Parse JSON responses for errors like "error": "Bad request" and log details. In code, use try-except blocks:  
```python
try: response = requests.get(...)  
except requests.exceptions.RequestException as e: print(f"Error: {e}"); exit(1)
```  
For CLI, pipe output to grep for error patterns and handle failures by exiting with a non-zero code.

## Concrete Usage Examples
1. **Search for latest AI news**: Use to fetch headlines on AI topics. Command: curl -H "X-Subscription-Token: $BRAVE_API_KEY" "https://api.search.brave.com/res/v1/web/search?q=latest+AI+advancements&count=3&search_lang=en". In your agent, extract the first result's snippet and append to a response.
2. **Extract snippets for query analysis**: For a user query like "best open source tools", run: curl -H "X-Subscription-Token: $BRAVE_API_KEY" "https://api.search.brave.com/res/v1/web/search?q=best+open+source+tools&safe=active&country=US". Process the JSON to pull descriptions, then use in AI reasoning to recommend tools based on extracted data.

## Graph Relationships
- Related to: ai-apis (cluster), as it provides search capabilities for other AI tools.
- Connects with: Other search APIs in ai-apis for fallback options, or data processing skills for result analysis.
