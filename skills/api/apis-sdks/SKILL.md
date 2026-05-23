---
name: apis-sdks
description: Understanding APIs and building/maintaining SDKs for developer experience
sasmp_version: "1.4.0"
version: "2.0.0"
updated: "2025-01"
bonded_agent: 04-technical-writer
bond_type: SECONDARY_BOND
---

# APIs & SDKs for DevRel

Master **API design and SDK development** to improve developer experience.

## Skill Contract

### Parameters
```yaml
parameters:
  required:
    - artifact_type: enum[api_docs, sdk, code_sample, reference]
    - language: string
  optional:
    - api_spec: object
    - version: string
```

### Output
```yaml
output:
  deliverable:
    code: string
    documentation: markdown
    tests: array[TestCase]
```

## API Fundamentals

### REST API Best Practices
```
GET    /users        # List users
GET    /users/:id    # Get single user
POST   /users        # Create user
PUT    /users/:id    # Update user (full)
PATCH  /users/:id    # Update user (partial)
DELETE /users/:id    # Delete user
```

### HTTP Status Codes
| Code | Meaning | Use When |
|------|---------|----------|
| 200 | OK | Successful GET/PUT/PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Server Error | Something broke |

## SDK Design Principles

### Idiomatic Code
```python
# Python SDK - Pythonic
client = AcmeClient(api_key="...")
users = client.users.list(limit=10)

# JavaScript SDK - Modern JS
const client = new AcmeClient({ apiKey: "..." });
const users = await client.users.list({ limit: 10 });
```

### SDK Components
```
SDK
├── Authentication handling
├── Request/response serialization
├── Error handling
├── Pagination helpers
├── Rate limit handling
├── Retry logic
├── Logging/debugging
└── Type definitions
```

## API Documentation

### Essential Docs
| Section | Purpose |
|---------|---------|
| Quickstart | First API call in 5 min |
| Authentication | How to authenticate |
| Endpoints | Complete reference |
| Errors | Error codes and handling |
| Rate limits | Usage limits |
| Changelog | Version history |

### Endpoint Documentation
```markdown
## Get User

`GET /users/:id`

Returns a user by their ID.

### Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes | The user ID |

### Response
```json
{
  "id": "usr_123",
  "email": "user@example.com",
  "name": "Jane Doe"
}
```

### Errors
- `404` - User not found
- `401` - Invalid API key
```

## DevRel API Responsibilities

- Advocate for developer-friendly design
- Create and maintain SDKs
- Write API documentation
- Gather feedback on DX issues
- Support developers using APIs

## Retry Logic

```yaml
retry_patterns:
  api_error_500:
    strategy: "Exponential backoff with jitter"
    max_retries: 3

  rate_limit_429:
    strategy: "Wait for retry-after header"
    fallback: "Exponential backoff"

  timeout:
    strategy: "Retry with increased timeout"
    fallback: "Return partial data"
```

## Failure Modes & Recovery

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| API breaking change | Tests fail | Update SDK, notify users |
| SDK version mismatch | Compatibility errors | Align versions |
| Missing docs | Support tickets | Add documentation |

## Debug Checklist

```
□ API spec up to date?
□ SDK matches API version?
□ Error handling complete?
□ Rate limiting documented?
□ Authentication working?
□ Examples tested?
```

## Test Template

```yaml
test_apis_sdks:
  unit_tests:
    - test_api_endpoints:
        assert: "All endpoints respond"
    - test_sdk_methods:
        assert: "Match API capabilities"

  integration_tests:
    - test_end_to_end:
        assert: "Full flow works"
```

## Observability

```yaml
metrics:
  - sdk_downloads: integer
  - api_calls: integer
  - error_rate: float
  - latency_p99: duration
```

See `assets/` for SDK templates.
