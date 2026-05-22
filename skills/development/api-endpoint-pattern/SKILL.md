---
name: api-endpoint-pattern
description: Standards for creating and organizing HTTP API endpoints using the Echo framework
---

# API Endpoint Pattern Skill

Use this skill when adding or modifying HTTP endpoints in the API.

---

## Scope

- Creating new API endpoints
- Adding new domain routers
- Modifying handler logic

---

## Router Structure

### Main Router (`internal/router/router.go`)
Initializes Echo, sets up middleware, and groups routes by domain.

### Sub-Routers (`internal/router/[domain]/router.go`)
Each domain has its own sub-router with a `Bind` function that receives an `*echo.Group` and dependencies.

```go
func Bind(e *echo.Group, db *sql.DB) *echo.Group {
    e.GET("/list", func(c echo.Context) error {
        // handler logic
    })
    return e
}
```

---

## Adding a New Endpoint

1. If introducing a new domain, create `internal/router/[domain]/router.go`.
2. Implement a `Bind(e *echo.Group, db *sql.DB) *echo.Group` function.
3. Register the sub-router in `internal/router/router.go`:
   ```go
   domainrouter.Bind(api.Group("/domain"), config.DB.Conn)
   ```
4. Implement data access logic in `internal/models/` if needed.

---

## Handler Guidelines

- **Parameter Parsing**: Use helper functions for complex query params (e.g., trader levels).
- **Dependency Injection**: Pass `*sql.DB` into `Bind`, then into handlers. Avoid globals.
- **Response Handling**:
  - Success: `c.JSON(200, data)` or `c.String(200, "OK")`
  - Error: `c.String(code, err.Error())` — log significant errors with zerolog.
- **Business Logic**: Keep handlers thin. Move complex logic to `internal/models/` or other internal packages.

---

## Conventions

- Use `e.Group()` for logical route separation.
- Use plural names for collections (`/items`, `/weapons`).
- Use query parameters for filtering and optional configuration.
- Prefer HTTP status constants for consistency, but be consistent either way.
