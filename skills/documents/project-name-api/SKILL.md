---
name: project-name-api
description: HTTP client for {{PROJECT_NAME}} REST API at {{API_BASE_URL}}. Use when
  making API requests, testing endpoints, handling authentication, or working with
  {{PROJECT_NAME}} API documentation.
---

---
name: {{PROJECT_NAME}}-api
description: HTTP client for {{PROJECT_NAME}} REST API at {{API_BASE_URL}}. Use when making API requests, testing endpoints, handling authentication, or working with {{PROJECT_NAME}} API documentation.
# Template version: 1.0 (2025-11-02)
---

# {{PROJECT_NAME}} API Client

<!--
TEMPLATE INSTRUCTIONS:
Replace these placeholders before using:
- {{PROJECT_NAME}}: Your project name (e.g., "myapp", "acme-platform")
- {{API_BASE_URL}}: API base URL (e.g., "https://api.example.com/v1")
- {{AUTH_METHOD}}: Authentication method (e.g., "Bearer token", "API key", "OAuth2")
- {{AUTH_HEADER}}: Auth header name (e.g., "Authorization", "X-API-Key")

After customization:
1. Update the skill name to match your project
2. Add actual endpoint documentation below
3. Add example requests/responses
4. Remove this comment block
-->

## Configuration

**Base URL**: `{{API_BASE_URL}}`
**Authentication**: {{AUTH_METHOD}} via `{{AUTH_HEADER}}` header

## Authentication

To authenticate requests:

```python
headers = {
    "{{AUTH_HEADER}}": "YOUR_TOKEN_HERE",
    "Content-Type": "application/json"
}
```

## Available Endpoints

### Example Endpoint (Replace with actual endpoints)

**GET** `/users/{id}`
- Description: Retrieve user by ID
- Parameters:
  - `id` (path, required): User ID
- Response: User object with id, name, email

```python
import requests

response = requests.get(
    f"{{API_BASE_URL}}/users/123",
    headers=headers
)
user = response.json()
```

### Add Your Endpoints Here

Document each endpoint with:
- HTTP method and path
- Description
- Parameters (path, query, body)
- Response format
- Example code

## Error Handling

Common error codes:
- 401: Invalid authentication
- 404: Resource not found
- 429: Rate limit exceeded
- 500: Server error

## Rate Limits

[Document rate limits if applicable]

## Examples

### Creating a Resource

```python
import requests

data = {
    "field1": "value1",
    "field2": "value2"
}

response = requests.post(
    f"{{API_BASE_URL}}/resources",
    headers=headers,
    json=data
)

if response.status_code == 201:
    created_resource = response.json()
    print(f"Created resource: {created_resource['id']}")
```

### Listing Resources with Pagination

```python
import requests

page = 1
all_resources = []

while True:
    response = requests.get(
        f"{{API_BASE_URL}}/resources",
        headers=headers,
        params={"page": page, "per_page": 100}
    )

    data = response.json()
    all_resources.extend(data["items"])

    if not data.get("has_more"):
        break
    page += 1
```

## Testing

To test the API connection:

```bash
curl -H "{{AUTH_HEADER}}: YOUR_TOKEN" {{API_BASE_URL}}/health
```

Expected response: `{"status": "ok"}`

## Resources

- [Add link to API documentation]
- [Add link to OpenAPI/Swagger spec if available]
- [Add link to authentication docs]
