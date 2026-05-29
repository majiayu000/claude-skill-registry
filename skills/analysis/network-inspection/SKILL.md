---
name: network-inspection
description: Use when debugging API calls, checking network requests, inspecting HTTP traffic, finding failed requests, analyzing response data, or investigating API errors. Provides detailed request/response analysis.
---

# Network Inspection Skill

Systematic approach to analyzing network requests using Chrome DevTools MCP.

## HTTP Status Code Reference

### Success (2xx)

| Code | Meaning | Notes |
|------|---------|-------|
| 200 | OK | Standard success response |
| 201 | Created | Resource successfully created |
| 204 | No Content | Success, no body returned |

### Redirect (3xx)

| Code | Meaning | Debugging Action |
|------|---------|------------------|
| 301 | Moved Permanently | Update hardcoded URLs |
| 302 | Found (Temporary) | Check redirect logic |
| 304 | Not Modified | Cache is working correctly |

### Client Error (4xx)

| Code | Meaning | Debugging Action |
|------|---------|------------------|
| 400 | Bad Request | Check request payload/parameters |
| 401 | Unauthorized | Check auth token/session |
| 403 | Forbidden | Check permissions/roles |
| 404 | Not Found | Check URL/endpoint spelling |
| 405 | Method Not Allowed | Check HTTP method (GET/POST/etc) |
| 409 | Conflict | Check for duplicate data |
| 422 | Unprocessable Entity | Check validation errors in response |
| 429 | Too Many Requests | Implement rate limiting/retry |

### Server Error (5xx)

| Code | Meaning | Debugging Action |
|------|---------|------------------|
| 500 | Internal Server Error | Check backend logs |
| 502 | Bad Gateway | Check proxy/load balancer |
| 503 | Service Unavailable | Check server health |
| 504 | Gateway Timeout | Check backend performance |

## Network Request Analysis Workflow

### 1. List All Requests

Use Chrome DevTools MCP to list network requests:

```
Tool: mcp__chrome-devtools__list_network_requests
```

### 2. Filter by Status

Focus on failures first:

1. **5xx errors** - Server issues (highest priority)
2. **4xx errors** - Client issues (request problems)
3. **Slow requests** - Performance issues
4. **Successful requests** - Verify data is correct

### 3. Inspect Specific Request

Get detailed information:

```
Tool: mcp__chrome-devtools__get_network_request
Parameters: { "requestId": "request-id-here" }
```

### 4. Analyze Request Components

For each problematic request, examine:

- **URL** - Is the endpoint correct?
- **Method** - GET, POST, PUT, DELETE?
- **Headers** - Authorization, Content-Type?
- **Body** - Request payload format?
- **Response** - What did server return?

## Request Headers to Check

### Outgoing Request Headers

| Header | Purpose | Debug Value |
|--------|---------|-------------|
| Authorization | Auth token | Verify token format, expiry |
| Content-Type | Payload format | Match API expectation |
| Accept | Response format | `application/json` typically |
| Origin | CORS source | Check against allowed origins |
| Cookie | Session data | Verify session exists |

### Response Headers to Check

| Header | Purpose | Debug Value |
|--------|---------|-------------|
| Set-Cookie | Session management | Check cookie attributes |
| X-Request-Id | Request tracking | Use for backend log correlation |
| Content-Type | Response format | Verify expected format |
| Cache-Control | Caching policy | Check if stale data issue |
| WWW-Authenticate | Auth challenge | Details on auth failure |

## Common API Issues

### Authentication Problems

| Symptom | Possible Cause | Solution |
|---------|----------------|----------|
| 401 on all requests | Token expired | Refresh token |
| 401 on some requests | Missing token header | Check auth interceptor |
| 403 after login | Insufficient permissions | Check user roles |
| Redirect to login | Session expired | Re-authenticate |

### Data Issues

| Symptom | Possible Cause | Solution |
|---------|----------------|----------|
| Empty response | No data found | Check query parameters |
| Partial data | Pagination | Check for next page |
| Stale data | Caching | Clear cache, check headers |
| Wrong data format | API version mismatch | Check API version |

### CORS Issues

| Error | Cause | Solution |
|-------|-------|----------|
| No 'Access-Control-Allow-Origin' | Server not configured | Add CORS headers on backend |
| Preflight failed | OPTIONS request blocked | Allow OPTIONS method |
| Credentials not supported | withCredentials mismatch | Configure credentials mode |

## Performance Analysis

### Timing Breakdown

| Phase | Description | Concern Threshold |
|-------|-------------|-------------------|
| DNS Lookup | Domain resolution | > 100ms |
| Connection | TCP handshake | > 100ms |
| TLS | SSL negotiation | > 100ms |
| Request | Sending data | > 500ms |
| Waiting (TTFB) | Server processing | > 500ms |
| Response | Receiving data | Depends on payload |

### Slow Request Causes

| Phase Slow | Likely Cause | Solution |
|------------|--------------|----------|
| DNS | DNS server issues | Use faster DNS |
| Connection | Server overloaded | Scale infrastructure |
| TLS | Certificate chain | Optimize SSL config |
| Waiting | Slow backend | Optimize API/database |
| Response | Large payload | Paginate, compress |

## Debugging Report Template

```markdown
## Network Debugging Report

**URL**: [page URL]
**Date**: [timestamp]
**Total Requests**: [count]

### Summary

- Failed Requests: X (Y% failure rate)
- Slow Requests (>1s): Z
- Total Data Transferred: N MB

### Failed Requests

| Endpoint | Method | Status | Error |
|----------|--------|--------|-------|
| [URL] | [GET/POST] | [code] | [message] |

### Request Analysis

#### Request 1: [endpoint]

**Status**: [code] [status text]

**Request**:
- Method: [method]
- URL: [full URL]
- Headers:
  ```
  [relevant headers]
  ```
- Body:
  ```json
  [request body]
  ```

**Response**:
- Status: [code]
- Headers:
  ```
  [relevant headers]
  ```
- Body:
  ```json
  [response body or error]
  ```

**Analysis**: [what went wrong]

**Suggested Fix**: [recommendation]

### Performance Issues

| Endpoint | TTFB | Total Time | Issue |
|----------|------|------------|-------|
| [URL] | [ms] | [ms] | [analysis] |

### Recommendations

1. [prioritized action 1]
2. [prioritized action 2]
```

## Integration with Console Debugging

Network failures often cause console errors:

| Network Issue | Console Manifestation |
|---------------|----------------------|
| 401 Unauthorized | `Error: User not authenticated` |
| 404 Not Found | `Error: Resource not found` |
| 500 Server Error | `Error: Request failed` |
| Network offline | `TypeError: Failed to fetch` |
| CORS blocked | CORS error message |

Use `console-debugging` skill alongside for comprehensive debugging.

## Best Practices

1. **Check the obvious first** - Is the URL correct? Is the server running?
2. **Compare working vs broken** - What's different about failing requests?
3. **Test in isolation** - Use curl/Postman to eliminate frontend issues
4. **Check request order** - Are dependent requests happening in right order?
5. **Verify authentication flow** - Token refresh, session expiry?
6. **Look at full response** - Error details often in response body
