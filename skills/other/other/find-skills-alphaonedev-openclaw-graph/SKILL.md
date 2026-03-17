---
name: find-skills
cluster: community
description: "ClaWHub skill discovery: search by capability, category, rating, compatibility, keyword matching"
tags: ["discovery","clawhub","search","skills"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "find skills clawhub discover search capability category rating"
---

# find-skills

## Purpose
This skill enables searching and discovering skills in ClaWHub based on criteria like capabilities, categories, ratings, compatibility, and keywords. It helps users locate relevant skills efficiently for integration into AI workflows.

## When to Use
Use this skill when you need to discover available skills in ClaWHub, such as finding high-rated skills for a specific task (e.g., code generation), exploring skills by category (e.g., "productivity"), or keyword matching (e.g., "image processing"). Apply it during project setup, skill prototyping, or when expanding AI capabilities.

## Key Capabilities
- Search skills by capability (e.g., "natural language processing").
- Filter by category (e.g., "community" or "enterprise").
- Sort by rating (e.g., minimum 4.0 stars).
- Check compatibility (e.g., with OpenClaw versions >=1.5).
- Perform keyword matching on skill names, descriptions, or tags.
- Return results with metadata like ID, name, and tags.

## Usage Patterns
Invoke this skill via CLI for quick searches or integrate it into scripts for automated discovery. Use it in loops to fetch and evaluate multiple skills, or combine with other skills for dynamic workflows (e.g., search then execute). Always specify search parameters to avoid broad results; for example, combine keywords with ratings for targeted queries.

## Common Commands/API
Use the ClaWHub CLI or API for searches. Authentication requires setting the environment variable `$CLAWHUB_API_KEY` before running commands.

- **CLI Command Example**:  
  `clawhub find-skills --query "AI coding" --category "community" --min-rating 4.0 --limit 10`  
  This returns up to 10 skills matching the query with at least 4.0 rating.

- **API Endpoint Example**:  
  POST to `https://api.clawhub.com/v1/skills/search` with JSON body:  
  ```json  
  {  
    "query": "web scraping",  
    "category": "tools",  
    "minRating": 3.5,  
    "compatibility": "OpenClaw-v2"  
  }  
  ```  
  Response is a JSON array of skill objects.

- **Code Snippet for Python Integration**:  
  ```python  
  import requests  
  headers = {'Authorization': f'Bearer {os.environ.get("CLAWHUB_API_KEY")}'}  
  response = requests.post('https://api.clawhub.com/v1/skills/search', json={'query': 'data analysis'}, headers=headers)  
  ```  
  This fetches skills matching "data analysis".

- **Config Format**:  
  Store search preferences in a JSON config file (e.g., `search-config.json`):  
  ```json  
  {  
    "defaultQuery": "AI tools",  
    "defaultCategory": "community"  
  }  
  ```  
  Pass it to CLI with `--config search-config.json`.

## Integration Notes
Integrate by wrapping the API in your AI agent's code; ensure `$CLAWHUB_API_KEY` is set securely. For OpenClaw, use the skill ID from results to chain executions (e.g., call `execute-skill` next). Handle pagination in API responses by checking the `nextPageToken` field. Test integrations in a sandbox environment to verify compatibility with your agent's version.

## Error Handling
Common errors include authentication failures (HTTP 401: check `$CLAWHUB_API_KEY`), invalid queries (HTTP 400: validate parameters like `--query`), or rate limits (HTTP 429: add delays). In code, wrap API calls in try-except blocks:  
```python  
try:  
    response = requests.post(...)  
    response.raise_for_status()  
except requests.exceptions.HTTPError as e:  
    print(f"Error: {e} - Retry after checking API key.")  
```  
Log errors with details like error codes and retry up to 3 times with exponential backoff.

## Graph Relationships
- Related to: "discovery" (tag), "search" (tag), "clawhub" (cluster)
- Depends on: "clawhub-api" (for authentication and endpoints)
- Used by: "skill-execution" (for discovering skills before running)
- Conflicts with: None known
- Enhances: "community" cluster skills by providing discovery mechanisms
