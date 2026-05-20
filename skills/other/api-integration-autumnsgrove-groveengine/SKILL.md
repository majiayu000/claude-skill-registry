---
name: api-integration
description: Integrate external REST APIs with proper authentication, rate limiting, error handling, and caching patterns. Use when working with external APIs, building API clients, or fetching data from third-party services.
---

# API Integration Skill

## When to Activate

Activate this skill when:
- Integrating external APIs
- Building API clients or wrappers
- Handling API authentication
- Implementing rate limiting
- Caching API responses

## Core Principles

1. **Respect rate limits** - APIs are shared resources
2. **Secure authentication** - Keys in secrets.json, never in code
3. **Handle errors gracefully** - Implement retries and backoff
4. **Cache responses** - Reduce redundant requests

## Authentication Setup

### secrets.json

```json
{
  "github_token": "ghp_your_token_here",
  "openweather_api_key": "your_key_here",
  "comment": "Never commit this file"
}
```

### Python Loading

```python
import os
import json
from pathlib import Path

def load_secrets():
    secrets_path = Path(__file__).parent / "secrets.json"
    try:
        with open(secrets_path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

secrets = load_secrets()
API_KEY = secrets.get("github_token", os.getenv("GITHUB_TOKEN", ""))

if not API_KEY:
    raise ValueError("No API key found")
```

## Request Patterns

### Basic GET (Python)

```python
import requests

def api_request(url: str, api_key: str) -> dict:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()
```

### With Retry and Backoff

```python
import time
from typing import Optional

def api_request_with_retry(
    url: str,
    api_key: str,
    max_retries: int = 3
) -> Optional[dict]:
    headers = {"Authorization": f"Bearer {api_key}"}
    wait_time = 1

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
                wait_time *= 2
            else:
                print(f"Error: HTTP {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(wait_time)
            wait_time *= 2

    return None
```

### Bash Request

```bash
#!/bin/bash
API_KEY=$(python3 -c "import json; print(json.load(open('secrets.json'))['github_token'])")

curl -s -H "Authorization: Bearer $API_KEY" \
  -H "Accept: application/json" \
  "https://api.github.com/user" | jq '.'
```

## Error Handling

```python
try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 429:
        print("Rate limited - waiting")
    elif e.response.status_code == 401:
        print("Unauthorized - check API key")
    else:
        print(f"HTTP error: {e}")
except requests.exceptions.ConnectionError:
    print("Connection error")
except requests.exceptions.Timeout:
    print("Request timeout")
```

## HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response |
| 401 | Unauthorized | Check API key |
| 403 | Forbidden | Check permissions |
| 404 | Not found | Verify endpoint |
| 429 | Rate limited | Wait and retry |
| 5xx | Server error | Retry with backoff |

## Caching

```python
import time

cache = {}
CACHE_TTL = 3600  # 1 hour

def cached_request(url: str, api_key: str) -> dict:
    now = time.time()

    if url in cache:
        data, timestamp = cache[url]
        if now - timestamp < CACHE_TTL:
            return data

    data = api_request(url, api_key)
    cache[url] = (data, now)
    return data
```

## Rate Limiting

### Check Headers

```bash
curl -I -H "Authorization: Bearer $API_KEY" "https://api.github.com/user" | grep -i rate
# x-ratelimit-limit: 5000
# x-ratelimit-remaining: 4999
```

### Implement Delays

```python
import time

def bulk_requests(urls: list, api_key: str, delay: float = 1.0):
    results = []
    for url in urls:
        result = api_request(url, api_key)
        results.append(result)
        time.sleep(delay)
    return results
```

## Pagination

```python
def fetch_all_pages(base_url: str, api_key: str) -> list:
    all_items = []
    page = 1

    while True:
        url = f"{base_url}?page={page}&per_page=100"
        data = api_request(url, api_key)

        if not data:
            break

        all_items.extend(data)
        page += 1
        time.sleep(1)  # Respect rate limits

    return all_items
```

## Best Practices

### DO ✅
- Store keys in secrets.json
- Implement retry with exponential backoff
- Cache responses when appropriate
- Respect rate limits
- Handle errors gracefully
- Log requests (without sensitive data)

### DON'T ❌
- Hardcode API keys
- Ignore rate limits
- Skip error handling
- Make requests in tight loops
- Log API keys

## API Etiquette Checklist

- [ ] Read API documentation and ToS
- [ ] Check rate limits
- [ ] Store keys securely
- [ ] Implement rate limiting
- [ ] Add error handling
- [ ] Cache appropriately
- [ ] Monitor usage

## Grove API Error Responses (MANDATORY)

When building API routes in Grove applications, **all error responses MUST use Signpost error codes**. Never return ad-hoc JSON error shapes.

```typescript
import { API_ERRORS, buildErrorJson, logGroveError } from '@autumnsgrove/groveengine/errors';
import { json } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request, locals }) => {
  if (!locals.user) {
    logGroveError('Engine', API_ERRORS.UNAUTHORIZED, { path: '/api/resource' });
    return json(buildErrorJson(API_ERRORS.UNAUTHORIZED), { status: 401 });
  }

  const body = schema.safeParse(await request.json());
  if (!body.success) {
    return json(buildErrorJson(API_ERRORS.INVALID_REQUEST_BODY), { status: 400 });
  }

  // ... business logic
};
```

Client-side, use `apiRequest()` (handles CSRF + credentials) and show toast feedback:
```typescript
import { toast } from '@autumnsgrove/groveengine/ui';

try {
  await apiRequest('/api/resource', { method: 'POST', body });
  toast.success('Created!');
} catch (err) {
  toast.error(err instanceof Error ? err.message : 'Something went wrong');
}
```

See `AgentUsage/error_handling.md` for the complete Signpost error code reference.

## Related Resources

See `AgentUsage/api_usage.md` for complete documentation including:
- Bash request patterns
- Conditional requests (ETags)
- Advanced caching strategies
- Specific API examples (GitHub, OpenWeather)
