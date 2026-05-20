---
name: restful-api-design
description: Use nouns for resources (GET /users, not GET /getUsers) Use when designing system architecture. Architecture category skill.
metadata:
  category: Architecture
  priority: high
  is-built-in: true
  session-guardian-id: builtin_restful_api_design
---

# RESTful API Design

Use nouns for resources (GET /users, not GET /getUsers). Use HTTP methods semantically: GET for reads, POST for creation, PUT/PATCH for updates, DELETE for removal. Return appropriate status codes (201 Created, 404 Not Found, 422 Unprocessable Entity). Version your API. Use consistent naming conventions. Provide meaningful error responses with error codes and messages.