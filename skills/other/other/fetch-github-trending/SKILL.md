---
name: fetch-github-trending
version: 2.0.0
description: 'Fetch trending AI/ML repositories from GitHub and store them in memory.
  Uses HTTP requests for GitHub API and memory MCP for storage and deduplication.

  '
license: MIT
allowed-tools:
- http_request
- memory/add
- memory/check_seen
- memory/mark_seen
metadata:
  domain: news
  category: collection
  requires-approval: false
  confidence: 0.75
  mcp-servers: []
---

# Fetch GitHub Trending

Fetch and store trending AI/ML repositories from GitHub with deduplication.

## When to Use

Use this skill when you need to:
- Discover trending AI/ML tools and libraries
- Find new repositories gaining traction
- Collect repos for tool spotlight sections in digests

## Instructions

### Step 1: Define Search Topics

Target these GitHub topics for AI/ML repos:
- `machine-learning`
- `deep-learning`
- `llm`
- `artificial-intelligence`
- `nlp`
- `transformers`
- `computer-vision`

### Step 2: Build GitHub Search Query

Construct a GitHub search API query:

**Query pattern:**
```
topic:machine-learning OR topic:llm language:python stars:>100 pushed:>2026-01-25
```

**Date calculation based on time range:**
- `daily`: pushed in last 1 day
- `weekly`: pushed in last 7 days
- `monthly`: pushed in last 30 days

### Step 3: Fetch from GitHub API

Use the `http_request` tool to query GitHub Search API.

**API endpoint:**
- URL: `https://api.github.com/search/repositories`
- Method: GET
- Parameters: q (query), sort (stars), order (desc), per_page (20)
- Headers: Accept: application/vnd.github.v3+json

**For each API response:**
1. Extract: full_name, description, html_url, stargazers_count, forks_count, language, topics
2. Parse created_at and pushed_at timestamps

### Step 4: Check for Duplicates

For each repository:

1. **Check if already seen:**
   - Call `memory/check_seen` with key=full_name (e.g., "owner/repo"), namespace="news/repos"
   - If seen=true, skip this repo

2. **Validate AI relevance:**
   - Repo must have at least one AI-related topic OR
   - Description mentions AI/ML keywords
   - Skip repos that don't appear AI-related

### Step 5: Store New Repositories

For each new (unseen) repository:

1. **Store in memory:**
   - Call `memory/add` with:
     - type: "document"
     - namespace: "news/repos"
     - data: {full_name, name, description, url, stars, forks, language, topics, created_at, pushed_at}
     - metadata: {fetched_at, search_topic}

2. **Mark as seen:**
   - Call `memory/mark_seen` with:
     - key: full_name
     - namespace: "news/repos"
     - ttl_seconds: 604800 (7 days)

### Step 6: Return Results

Return a summary including:
- Number of repos stored
- Number of duplicates skipped
- Topics searched
- Total matching repos found

## Tool Usage Guidance

### http_request tool
- Use for GitHub API calls
- Set appropriate headers for API version
- Handle rate limiting (60/hour unauthenticated, 5000/hour authenticated)

### memory/check_seen
- Key should be the full repo name (owner/repo format)
- Namespace: "news/repos"

### memory/add
- Store each new repo as type "document"
- Include star count for ranking

### memory/mark_seen
- Use 7-day TTL (repos trend changes weekly)

## Repository Data Schema

```json
{
  "full_name": "owner/repo-name",
  "name": "repo-name",
  "description": "A powerful LLM inference library",
  "url": "https://github.com/owner/repo-name",
  "stars": 15234,
  "forks": 1523,
  "language": "Python",
  "topics": ["llm", "inference", "machine-learning"],
  "created_at": "2025-06-15",
  "pushed_at": "2026-01-26"
}
```

## Error Handling

- If GitHub API rate limits, wait and retry or return cached results
- If API request fails, log error and continue
- Return partial results if some queries succeed

## Success Criteria

- At least one topic query succeeds
- Repos are sorted by star count
- No duplicate repos in output
- AI-relevance filter applied
