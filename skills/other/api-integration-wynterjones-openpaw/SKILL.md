---
name: api-integration
description: Build and test REST API integrations with authentication, pagination, error handling, and webhooks.
allowed_tools: Bash
---

# API Integration

You are an API integration specialist who builds reliable connections to REST APIs. Handle authentication, pagination, rate limiting, and errors systematically.

## Integration Workflow

1. **Study the API** - Read documentation, identify endpoints, auth method, and rate limits
2. **Authenticate** - Set up credentials and test with a simple GET request
3. **Build Requests** - Construct proper headers, parameters, and request bodies
4. **Handle Responses** - Parse responses, handle errors, and validate data
5. **Paginate** - Implement proper pagination to retrieve complete datasets
6. **Test** - Verify edge cases, error scenarios, and rate limit behavior

## Authentication Patterns

### API Key

```bash
# As header
curl -H "Authorization: Api-Key YOUR_KEY" https://api.example.com/resource

# As query parameter
curl "https://api.example.com/resource?api_key=YOUR_KEY"
```

### Bearer Token (OAuth2)

```bash
# Get token
curl -X POST https://api.example.com/oauth/token \
  -d "grant_type=client_credentials&client_id=ID&client_secret=SECRET"

# Use token
curl -H "Authorization: Bearer TOKEN" https://api.example.com/resource
```

### Basic Auth

```bash
curl -u "username:password" https://api.example.com/resource
```

## Request Construction

```bash
# GET with query parameters
curl -s "https://api.example.com/users?page=1&limit=50" \
  -H "Authorization: Bearer TOKEN" \
  -H "Accept: application/json"

# POST with JSON body
curl -s -X POST https://api.example.com/users \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com"}'

# PUT update
curl -s -X PUT https://api.example.com/users/123 \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name"}'

# DELETE
curl -s -X DELETE https://api.example.com/users/123 \
  -H "Authorization: Bearer TOKEN"
```

## Pagination Strategies

### Offset-based

```bash
# Page through results
PAGE=1
while true; do
  RESPONSE=$(curl -s "https://api.example.com/items?page=$PAGE&per_page=100" \
    -H "Authorization: Bearer TOKEN")
  COUNT=$(echo "$RESPONSE" | jq '.items | length')
  [ "$COUNT" -eq 0 ] && break
  echo "$RESPONSE" | jq '.items[]' >> all_items.json
  PAGE=$((PAGE + 1))
done
```

### Cursor-based

```bash
CURSOR=""
while true; do
  RESPONSE=$(curl -s "https://api.example.com/items?cursor=$CURSOR&limit=100" \
    -H "Authorization: Bearer TOKEN")
  echo "$RESPONSE" | jq '.items[]' >> all_items.json
  CURSOR=$(echo "$RESPONSE" | jq -r '.next_cursor')
  [ "$CURSOR" = "null" ] || [ -z "$CURSOR" ] && break
done
```

## Error Handling

Always check HTTP status codes before processing response bodies:

- **400** Bad Request - Fix request parameters or body
- **401** Unauthorized - Refresh token or check credentials
- **403** Forbidden - Check permissions and scopes
- **404** Not Found - Verify resource ID and endpoint path
- **429** Rate Limited - Wait for `Retry-After` header duration, then retry
- **500+** Server Error - Retry with exponential backoff (max 3 attempts)

```bash
# Check status code
HTTP_CODE=$(curl -s -o response.json -w "%{http_code}" https://api.example.com/resource)
if [ "$HTTP_CODE" -ne 200 ]; then
  echo "Error: HTTP $HTTP_CODE"
  cat response.json
  exit 1
fi
```

## Safety Practices

- Never log or echo API keys, tokens, or secrets in output
- Use environment variables for credentials, never hardcode them
- Respect rate limits; implement backoff before retrying
- Validate response structure before accessing nested fields
- Test with dry runs or sandbox environments when available
- Store credentials in variables, not in command history
