---
name: generate-endpoint
description: Generate a single API endpoint with controller action, service method, and test
argument-hint: "<verb> <path> [--entity=<name>]"
tags: [codegen, api, endpoint, backend]
user-invocable: true
---

# Generate API Endpoint

Generate a single controller action with corresponding service and repository methods.

## What To Do

1. **Add controller action** matching the HTTP verb and path
2. **Add service method** with business logic
3. **Add repository method** if data access needed
4. **Add test** for the new endpoint
5. **Update Swagger docs** with proper attributes

## Arguments
- `<verb>`: HTTP verb (GET, POST, PUT, DELETE, PATCH)
- `<path>`: Route path (e.g., /api/candidates/{id}/skills)
- `--entity=<name>`: Associated entity name