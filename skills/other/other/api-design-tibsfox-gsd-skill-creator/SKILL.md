---
name: api-design
description: REST API design best practices. Use when designing APIs, choosing status codes, or creating endpoints.
---

# REST API Design

## Endpoint Rules

- **Nouns, not verbs:** `/users` not `/getUsers` — HTTP method is the verb
- **Plural nouns:** `/users`, `/orders` — consistent collections
- **Kebab-case:** `/user-profiles` not `/user_profiles`
- **Max 2 levels nesting:** `/users/{id}/orders` — deeper use query params
- **No trailing slashes, no extensions**

## HTTP Methods

| Method | Purpose | Idempotent |
|--------|---------|------------|
| GET | Retrieve | Yes |
| POST | Create | No |
| PUT | Replace entire resource | Yes |
| PATCH | Partial update | No |
| DELETE | Remove | Yes |

## Status Codes

| Code | Use When |
|------|----------|
| 200 | Success with body |
| 201 | Resource created (+ Location header) |
| 204 | Success, no body (DELETE) |
| 400 | Malformed request |
| 401 | Not authenticated |
| 403 | Authenticated but forbidden |
| 404 | Not found |
| 409 | Conflict (duplicate) |
| 422 | Valid syntax, invalid semantics |
| 429 | Rate limited |

## Error Format

```json
{"error": {"code": "VALIDATION_ERROR", "message": "...", "details": [], "request_id": "req_..."}}
```

## Key Rules

- Always paginate lists (cursor-based preferred, max page size enforced)
- Never expose sequential IDs — use UUIDs
- Auth credentials in headers, never URLs
- Return 400 for unknown parameters (catch typos)
- Include request_id in every response
