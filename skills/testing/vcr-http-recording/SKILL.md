---
name: vcr-http-recording
description: VCR.py HTTP recording for Python tests. Use when testing Python code making HTTP requests, recording API responses for replay, or creating deterministic tests for external services.
context: fork
agent: test-generator
version: 1.0.0
author: SkillForge
user-invocable: false
---

# VCR.py HTTP Recording

Record and replay HTTP interactions for Python tests.

## Basic Setup

```python
# conftest.py
import pytest

@pytest.fixture(scope="module")
def vcr_config():
    return {
        "cassette_library_dir": "tests/cassettes",
        "record_mode": "once",
        "match_on": ["uri", "method"],
        "filter_headers": ["authorization", "x-api-key"],
        "filter_query_parameters": ["api_key", "token"],
    }
```

## Basic Usage

```python
import pytest

@pytest.mark.vcr()
def test_fetch_user():
    response = requests.get("https://api.example.com/users/1")

    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"

@pytest.mark.vcr("custom_cassette.yaml")
def test_with_custom_cassette():
    response = requests.get("https://api.example.com/data")
    assert response.status_code == 200
```

## Async Support

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_async_api_call():
    async with AsyncClient() as client:
        response = await client.get("https://api.example.com/data")

    assert response.status_code == 200
    assert "items" in response.json()
```

## Recording Modes

```python
@pytest.fixture(scope="module")
def vcr_config():
    import os

    # CI: never record, only replay
    if os.environ.get("CI"):
        record_mode = "none"
    else:
        record_mode = "new_episodes"

    return {"record_mode": record_mode}
```

| Mode | Behavior |
|------|----------|
| `once` | Record if missing, then replay |
| `new_episodes` | Record new, replay existing |
| `none` | Never record (CI) |
| `all` | Always record (refresh) |

## Filtering Sensitive Data

```python
def filter_request_body(request):
    """Redact sensitive data from request body."""
    import json
    if request.body:
        try:
            body = json.loads(request.body)
            if "password" in body:
                body["password"] = "REDACTED"
            if "api_key" in body:
                body["api_key"] = "REDACTED"
            request.body = json.dumps(body)
        except json.JSONDecodeError:
            pass
    return request

@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": ["authorization", "x-api-key"],
        "before_record_request": filter_request_body,
    }
```

## LLM API Testing

```python
def llm_request_matcher(r1, r2):
    """Match LLM requests ignoring dynamic fields."""
    import json

    if r1.uri != r2.uri or r1.method != r2.method:
        return False

    body1 = json.loads(r1.body)
    body2 = json.loads(r2.body)

    # Ignore dynamic fields
    for field in ["request_id", "timestamp"]:
        body1.pop(field, None)
        body2.pop(field, None)

    return body1 == body2

@pytest.fixture(scope="module")
def vcr_config():
    return {
        "custom_matchers": [llm_request_matcher],
    }
```

## Cassette File Example

```yaml
# tests/cassettes/test_fetch_user.yaml
interactions:
- request:
    body: null
    headers:
      Content-Type: application/json
    method: GET
    uri: https://api.example.com/users/1
  response:
    body:
      string: '{"id": 1, "name": "John Doe"}'
    status:
      code: 200
version: 1
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Record mode | `once` for dev, `none` for CI |
| Cassette format | YAML (readable) |
| Sensitive data | Always filter headers/body |
| Custom matchers | Use for LLM APIs |

## Common Mistakes

- Committing cassettes with real API keys
- Using `all` mode in CI (makes live calls)
- Not filtering sensitive data
- Missing cassettes in git

## Related Skills

- `msw-mocking` - Frontend equivalent
- `integration-testing` - API testing patterns
- `llm-testing` - LLM-specific patterns

## Capability Details

### http-recording
**Keywords:** record HTTP, vcr.use_cassette, record mode, capture HTTP
**Solves:**
- Record HTTP interactions for replay
- Capture real API responses
- Create deterministic test fixtures

### cassette-replay
**Keywords:** replay, cassette, playback, mock replay
**Solves:**
- Replay recorded HTTP interactions
- Run tests without network access
- Ensure consistent test results

### async-support
**Keywords:** async, aiohttp, httpx async, async cassette
**Solves:**
- Record async HTTP clients
- Handle aiohttp and httpx async
- Test async API integrations

### sensitive-data-filtering
**Keywords:** filter, scrub, redact, sensitive data, before_record
**Solves:**
- Scrub API keys from cassettes
- Redact sensitive data
- Implement before_record hooks

### custom-matchers
**Keywords:** matcher, match on, request matching, custom match
**Solves:**
- Configure request matching rules
- Ignore dynamic request parts
- Match by method/host/path

### llm-api-testing
**Keywords:** LLM cassette, OpenAI recording, Anthropic recording
**Solves:**
- Record LLM API responses
- Test AI integrations deterministically
- Avoid costly API calls in tests
