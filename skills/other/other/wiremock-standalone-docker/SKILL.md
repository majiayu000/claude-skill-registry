---
name: wiremock-standalone-docker
description: Provides patterns and configurations for running WireMock as a standalone Docker container. Generates mock HTTP endpoints, creates stub mappings for testing, validates integration scenarios, and simulates error conditions. Use when you need to mock APIs, create a mock server, stub external services, simulate third-party APIs, or fake API responses for integration testing.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# WireMock Standalone Docker Skill

## Overview

Provides patterns for running WireMock as a standalone Docker container to mock external APIs during integration and end-to-end testing. Runs WireMock as a separate service that simulates real API behavior for testing HTTP clients, retry logic, and error handling.

## When to Use

Use when you need to:
- Mock external APIs during integration or end-to-end testing
- Simulate error conditions (timeouts, 5xx, rate limiting) without real services
- Test HTTP client configurations, retry logic, and error handling
- Create portable, reproducible test environments
- Validate API contracts before implementing the real service

## Instructions

### Step 1: Set Up Docker Compose

Create a `docker-compose.yml` with WireMock 3.5.2, port mapping, and volume mounts for mappings and files:

```yaml
version: "3.8"
services:
  wiremock:
    image: wiremock/wiremock:3.5.2
    ports:
      - "8080:8080"
    volumes:
      - ./wiremock:/home/wiremock
    command: ["--global-response-templating"]
```

### Step 2: Create Directory Structure

Create the WireMock configuration directories:

```
wiremock/
├── mappings/   # JSON stub definitions
└── __files/   # Response body files
```

### Step 3: Define API Mappings

Create JSON stub files in `wiremock/mappings/` for each scenario:

- **Success**: Return 200 with JSON body
- **Not Found**: Return 404
- **Server Error**: Return 500
- **Timeout**: Use `fixedDelayMilliseconds`
- **Rate Limit**: Return 429 with Retry-After header

### Step 4: Start WireMock

```bash
docker compose up -d
```

### Step 5: Verify WireMock is Running

```bash
curl http://localhost:8080/__admin/mappings
```

Expected: Returns empty array `{"mappings":[]}` if no stubs loaded, or your stub definitions. If you get connection refused, check that the container is running: `docker compose ps`

### Step 6: Configure HTTP Client

Point your application to `http://localhost:8080` (or `http://wiremock:8080` in Docker network) instead of the real API.

### Step 7: Test Edge Cases

Always test: 200, 400, 401, 403, 404, 429, 500, timeouts, malformed responses.

## Examples

### Example 1: Mock Successful GET Request

```json
{
  "request": { "method": "GET", "url": "/api/users/123" },
  "response": {
    "status": 200,
    "jsonBody": { "id": 123, "name": "Mario Rossi" }
  }
}
```

### Example 2: Mock Server Error

```json
{
  "request": { "method": "GET", "url": "/api/error" },
  "response": { "status": 500, "body": "Internal Server Error" }
}
```

### Example 3: Mock Timeout

```json
{
  "request": { "method": "GET", "url": "/api/slow" },
  "response": {
    "status": 200,
    "fixedDelayMilliseconds": 5000,
    "jsonBody": { "message": "delayed" }
  }
}
```

### Example 4: Docker Compose with Application

```yaml
services:
  wiremock:
    image: wiremock/wiremock:3.5.2
    ports:
      - "8080:8080"
    volumes:
      - ./wiremock:/home/wiremock

  app:
    build: .
    environment:
      - API_BASE_URL=http://wiremock:8080
    depends_on:
      - wiremock
```

## Best Practices

1. **Organize mappings by feature**: Use subdirectories like `users/`, `products/`
2. **Version control mappings**: Keep mappings in git for reproducible tests
3. **Test all error scenarios**: 401, 403, 404, 429, 500, timeouts
4. **Reset between test runs**: `curl -X POST http://localhost:8080/__admin/reset`
5. **Use descriptive file names**: `get-user-success.json`, `post-user-error.json`

## Constraints and Warnings

- Ensure port 8080 is available or map to a different port
- Configure Docker networking when running multiple containers
- Enable `--global-response-templating` for dynamic responses
- WireMock resets mappings on container restart

## Troubleshooting

**Requests don't match stubs?**
Check what WireMock received: `curl http://localhost:8080/__admin/requests` — shows unmatched requests with details about what was actually sent.

**Stub file not loading?**
Verify file location: place JSON stubs in `wiremock/mappings/` and response files in `wiremock/__files/`. Check file permissions.

**Connection refused errors?**
Run `docker compose ps` to verify the container is running. Check port conflicts with `lsof -i :8080`.

## References

See `references/` for complete examples:
- `docker-compose.yml` - Full Docker Compose configuration
- `wiremock/mappings/` - Complete stub examples for all scenarios
