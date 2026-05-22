---
name: api-tester
description: 快速 API 测试工具，支持 GET/POST 请求、请求头、认证模式测试。触发词：测试 API、API 请求。
---

# API Tester

Test APIs quickly from CLI.

## Common Patterns

```bash
# GET request
curl -s https://api.github.com/user | jq .

# POST with JSON
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"key":"value"}' \
  https://httpbin.org/post

# With auth header
curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.example.com/data

# Check status code
curl -s -o /dev/null -w "%{http_code}" \
  https://api.example.com/health
```

## Saved Requests

Store common requests in:
`~/.config/api-tester/requests/`

## Response Validation

```bash
# Check JSON structure
curl -s ... | jq 'has("data")'

# Extract specific field
curl -s ... | jq -r '.data[0].id'
```
