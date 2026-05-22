# API Conventions Skill

> REST API patterns for cl-n8n-mcp.

---

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/` | No | Server info |
| GET | `/health` | No | Health check |
| GET | `/stats` | API Key | Usage stats |
| POST | `/mcp` | Yes | MCP endpoint |
| DELETE | `/mcp` | Yes | Terminate session |

## Authentication

### Multi-Tenant Headers
```
x-n8n-url: https://n8n.example.com
x-n8n-key: n8n_api_key_here
```

### SaaS API Key (wrapper)
```
Authorization: Bearer n2f_xxxxxxxxxxxxx
```

## Response Format

### Success
```json
{
  "success": true,
  "data": { ... }
}
```

### Error
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded"
  }
}
```

## Rate Limit Headers

```
X-RateLimit-Limit: 50
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1704067200
```
