---
name: http-client
description: 发送HTTP请求，支持所有方法、请求头、认证和响应处理。
metadata:
  short-description: HTTP请求客户端
source:
  repository: https://github.com/psf/requests
  license: Apache-2.0
---

# HTTP Client Tool

## Description
Make HTTP requests with full support for GET, POST, PUT, DELETE, headers, authentication, and file uploads.

## Trigger
- `/http` command
- User needs to make API calls
- User wants to test endpoints

## Usage

```bash
# GET request
python scripts/http_client.py GET https://api.example.com/users

# POST with JSON body
python scripts/http_client.py POST https://api.example.com/users --json '{"name": "John"}'

# With headers
python scripts/http_client.py GET https://api.example.com/data --header "Authorization: Bearer token"

# Upload file
python scripts/http_client.py POST https://api.example.com/upload --file document.pdf
```

## Tags
`http`, `api`, `rest`, `requests`, `client`

## Compatibility
- Codex: ✅
- Claude Code: ✅
