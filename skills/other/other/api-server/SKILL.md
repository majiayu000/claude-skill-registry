---
name: API Server
description: Standards for building HTTP services, REST APIs, and middleware in Golang.
metadata:
  labels: [golang, http, api, rest, middleware]
  triggers:
    files: ['cmd/server/*.go', 'internal/adapter/handler/**']
    keywords: [http server, rest api, gin, echo, middleware]
---

# Golang API Server Standards

## **Priority: P0 (CRITICAL)**

## Router Selection

- **Standard Lib (`net/http`)**: Use for simple services or when zero deps is required. Use `http.ServeMux` (Go 1.22+ has decent routing).
- **Echo (`labstack/echo`)**: Recommended for production REST APIs. Excellent middleware support, binding, and error handling.
- **Gin (`gin-gonic/gin`)**: High performance alternative.

## Guidelines

- **Graceful Shutdown**: MUST implement graceful shutdown to handle in-flight requests on termination (SIGINT/SIGTERM).
- **DTOs**: Separate Domain structs from API Request/Response structs. Map between them.
- **Middleware**: Use middleware for cross-cutting concerns (Logging, Recovery, CORS, Auth, Tracing).
- **Health Checks**: Always include `/health` and `/ready` endpoints.
- **Content-Type**: Enforce `application/json` for REST APIs.

## Middleware Pattern

- Standard: `func(next http.Handler) http.Handler`
- Echo implementation: `func(next echo.HandlerFunc) echo.HandlerFunc`

## Anti-Patterns

- **Business Logic in Handlers**: Handlers should only parse request -> call service -> format response.
- **Global Router**: Don't use global router variables. Pass router instance.

## References

- [Middleware Patterns](references/middleware-patterns.md)
- [Graceful Shutdown](references/graceful-shutdown.md)
