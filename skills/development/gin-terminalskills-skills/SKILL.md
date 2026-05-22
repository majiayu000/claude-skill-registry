---
name: gin
description: >-
  You are an expert in Gin, the fastest Go web framework with a martini-like
  API. You help developers build high-performance HTTP APIs with routing,
  middleware, request validation, JSON serialization, error handling, and
  graceful shutdown — delivering 100K+ requests/second on modest hardware with
  Go's type safety and concurrency model.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: Backend Development
  tags:
    - go
    - web-framework
    - http
    - rest
    - api
    - performance
    - middleware
---

# Gin — High-Performance Go Web Framework

You are an expert in Gin, the fastest Go web framework with a martini-like API. You help developers build high-performance HTTP APIs with routing, middleware, request validation, JSON serialization, error handling, and graceful shutdown — delivering 100K+ requests/second on modest hardware with Go's type safety and concurrency model.

## Core Capabilities

### Server and Routes

```go
package main

import (
    "net/http"
    "strconv"
    "github.com/gin-gonic/gin"
)

type User struct {
    ID    uint   `json:"id"`
    Name  string `json:"name" binding:"required,min=2,max=100"`
    Email string `json:"email" binding:"required,email"`
    Role  string `json:"role" binding:"oneof=user admin"`
}

func main() {
    r := gin.Default()  // Logger + Recovery middleware

    // Middleware
    r.Use(corsMiddleware())
    r.Use(rateLimiter(100))  // 100 req/s

    api := r.Group("/api")
    api.Use(authMiddleware())
    {
        api.GET("/users", listUsers)
        api.POST("/users", createUser)
        api.GET("/users/:id", getUser)
        api.PUT("/users/:id", updateUser)
        api.DELETE("/users/:id", deleteUser)
    }

    r.Run(":8080")
}

func listUsers(c *gin.Context) {
    page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
    limit, _ := strconv.Atoi(c.DefaultQuery("limit", "20"))

    users, total := db.FindUsers(page, limit)
    c.JSON(http.StatusOK, gin.H{
        "data":  users,
        "total": total,
        "page":  page,
    })
}

func createUser(c *gin.Context) {
    var input User
    if err := c.ShouldBindJSON(&input); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    user, err := db.CreateUser(input)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to create user"})
        return
    }
    c.JSON(http.StatusCreated, user)
}

func getUser(c *gin.Context) {
    id := c.Param("id")
    user, err := db.FindUser(id)
    if err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "user not found"})
        return
    }
    c.JSON(http.StatusOK, user)
}

// Auth middleware
func authMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token == "" {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "missing token"})
            return
        }
        user, err := validateToken(token)
        if err != nil {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "invalid token"})
            return
        }
        c.Set("user", user)
        c.Next()
    }
}
```

### Graceful Shutdown

```go
func main() {
    r := gin.Default()
    // ... routes

    srv := &http.Server{Addr: ":8080", Handler: r}
    go func() { srv.ListenAndServe() }()

    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    srv.Shutdown(ctx)
}
```

## Installation

```bash
go get -u github.com/gin-gonic/gin
```

## Best Practices

1. **Binding for validation** — Use `ShouldBindJSON` with struct tags (`binding:"required,email"`); rejects bad input before handler
2. **Route groups** — Group routes by prefix and middleware: `api := r.Group("/api", authMiddleware())`
3. **Error handling** — Return consistent error JSON; use custom error types for business logic errors
4. **Middleware chain** — Use `c.Next()` to continue, `c.Abort()` to stop; middleware runs in order
5. **Context values** — Store auth user with `c.Set("user", user)`; retrieve with `c.Get("user")` in handlers
6. **gin.H for quick JSON** — Use `gin.H{}` for ad-hoc responses; use structs for typed, documented responses
7. **Graceful shutdown** — Handle SIGTERM; drain connections before exit for zero-downtime deploys
8. **Release mode** — Set `GIN_MODE=release` in production; disables debug logging, improves performance
