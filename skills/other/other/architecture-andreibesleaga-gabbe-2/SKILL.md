---
name: middleware-design
description: Designing robust middleware chains (Auth, Rate Limiting, Logging).
role: eng-backend
triggers:
  - middleware
  - interceptor
  - pipeline
  - request lifecycle
  - rate limit
---

# middleware-design Skill

This skill guides the creation of the request processing pipeline ("The Onion Architecture").

## 1. The Standard Pipeline (Order Matters)

1.  **Request ID**: Generate `trace_id` immediately. (Before logs).
2.  **CORS**: Allow/Block origins. (Before processing).
3.  **Body Parser**: JSON/Form parsing. (Limit size to prevent DoS).
4.  **Rate Limiter**: Token Bucket algorithm. (Stop abuse cheaply).
5.  **Authentication**: Verify JWT/Session. (Who is it?).
6.  **Authorization**: Check Roles/Scopes. (Can they do it?).
7.  **Validation**: Zod/Pydantic schema check. (Is input valid?).
8.  **Controller**: Business Logic.
9.  **Error Handler**: Catch exceptions, format JSON, scrub sensitive data.

## 2. Implementation Rules
- **Fail Fast**: If Rate Limit check fails, return 429 immediately. Do not parse body.
- **Context Passing**: Pass `user` and `trace_id` via Context (Go/React) or Request Object (Express/FastAPI).
- **No Business Logic**: Middleware should be generic. Don't query `SELECT * FROM orders` in middleware.

## 3. Specific Patterns

### Rate Limiting
- **Global**: 1000 req/min/IP.
- **Route-Specific**: Login = 5 req/min/IP.
- **Storage**: Use Redis. Local memory rate limiting doesn't work in clustered apps.

### Response Interceptors
- Use for consistent response formatting.
- `data: { ... }`, `meta: { trace_id: ... }`.

### Error Handling Middleware
- **NEVER** return raw stack trace to client in Production.
- **ALWAYS** log raw stack trace to logger.
