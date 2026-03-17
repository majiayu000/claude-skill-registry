---
name: go-api-gateway
description: Build the AgentStack API Gateway in Go with Fiber/Chi. Use for creating REST API endpoints, HTTP handlers, middleware, request validation, and API routing. Triggers on "build API", "create endpoint", "HTTP handler", "REST API", "API gateway", "Fiber handler", "Chi router", or when implementing spec/004-api-design.md endpoints.
---

# Go API Gateway

## Overview

Build production-grade REST API endpoints for the AgentStack platform using Go with Fiber or Chi frameworks, following the specifications in `/spec/004-api-design.md`.

## Project Structure

```
cmd/api/main.go              # Entry point
internal/api/
├── handlers/                # HTTP handlers by domain
│   ├── agents.go
│   ├── chat.go
│   ├── deployments.go
│   └── health.go
├── middleware/              # Cross-cutting concerns
│   ├── auth.go
│   ├── logging.go
│   ├── ratelimit.go
│   └── tracing.go
├── routes/                  # Route definitions
│   └── router.go
├── dto/                     # Request/Response DTOs
│   └── agents.go
└── server.go               # Server configuration
```

## Core Workflow

### Step 1: Define DTOs

Create request/response structures with validation tags:

```go
// internal/api/dto/agents.go
package dto

import "time"

type CreateAgentRequest struct {
    Name       string            `json:"name" validate:"required,min=3,max=64"`
    Framework  string            `json:"framework" validate:"required,oneof=google-adk langchain crewai"`
    Config     AgentConfig       `json:"config" validate:"required"`
    AutoDeploy bool              `json:"auto_deploy"`
}

type AgentConfig struct {
    Model        string   `json:"model" validate:"required"`
    SystemPrompt string   `json:"system_prompt"`
    Tools        []string `json:"tools"`
}

type AgentResponse struct {
    ID        string    `json:"id"`
    Name      string    `json:"name"`
    Status    string    `json:"status"`
    URLs      AgentURLs `json:"urls,omitempty"`
    CreatedAt time.Time `json:"created_at"`
}

type AgentURLs struct {
    Chat string `json:"chat,omitempty"`
}
```

### Step 2: Create Handler

```go
// internal/api/handlers/agents.go
package handlers

import (
    "github.com/gofiber/fiber/v2"
    "github.com/raphaelmansuy/agentstack/internal/api/dto"
    "github.com/raphaelmansuy/agentstack/internal/domain/agent"
)

type AgentHandler struct {
    service *agent.Service
}

func NewAgentHandler(svc *agent.Service) *AgentHandler {
    return &AgentHandler{service: svc}
}

// CreateAgent godoc
// @Summary Create a new agent
// @Tags agents
// @Accept json
// @Produce json
// @Param request body dto.CreateAgentRequest true "Agent configuration"
// @Success 201 {object} dto.AgentResponse
// @Failure 400 {object} dto.ErrorResponse
// @Router /v1/agents [post]
func (h *AgentHandler) CreateAgent(c *fiber.Ctx) error {
    var req dto.CreateAgentRequest
    if err := c.BodyParser(&req); err != nil {
        return fiber.NewError(fiber.StatusBadRequest, "Invalid request body")
    }

    // Validate request
    if err := validate.Struct(req); err != nil {
        return c.Status(fiber.StatusBadRequest).JSON(dto.ValidationError(err))
    }

    // Get project ID from context (set by auth middleware)
    projectID := c.Locals("projectID").(string)

    // Create agent
    agt, err := h.service.Create(c.Context(), projectID, agent.CreateInput{
        Name:       req.Name,
        Framework:  req.Framework,
        Config:     req.Config,
        AutoDeploy: req.AutoDeploy,
    })
    if err != nil {
        return handleDomainError(c, err)
    }

    return c.Status(fiber.StatusCreated).JSON(toAgentResponse(agt))
}

// ListAgents godoc
// @Summary List agents in project
// @Tags agents
// @Produce json
// @Param cursor query string false "Pagination cursor"
// @Param limit query int false "Items per page" default(20)
// @Success 200 {object} dto.AgentListResponse
// @Router /v1/agents [get]
func (h *AgentHandler) ListAgents(c *fiber.Ctx) error {
    projectID := c.Locals("projectID").(string)
    cursor := c.Query("cursor")
    limit := c.QueryInt("limit", 20)

    agents, nextCursor, err := h.service.List(c.Context(), projectID, cursor, limit)
    if err != nil {
        return handleDomainError(c, err)
    }

    return c.JSON(dto.AgentListResponse{
        Data:       toAgentResponses(agents),
        NextCursor: nextCursor,
    })
}
```

### Step 3: Register Routes

```go
// internal/api/routes/router.go
package routes

import (
    "github.com/gofiber/fiber/v2"
    "github.com/raphaelmansuy/agentstack/internal/api/handlers"
    "github.com/raphaelmansuy/agentstack/internal/api/middleware"
)

func SetupRoutes(app *fiber.App, deps *Dependencies) {
    // Health endpoints (no auth)
    app.Get("/health", handlers.Health)
    app.Get("/ready", handlers.Ready)

    // API v1 group
    v1 := app.Group("/v1")
    
    // Apply middleware
    v1.Use(middleware.RequestID())
    v1.Use(middleware.Logger())
    v1.Use(middleware.Tracing())
    v1.Use(middleware.Auth(deps.AuthService))
    v1.Use(middleware.RateLimit(deps.RateLimiter))

    // Agent routes
    agents := v1.Group("/agents")
    agentHandler := handlers.NewAgentHandler(deps.AgentService)
    agents.Post("/", agentHandler.CreateAgent)
    agents.Get("/", agentHandler.ListAgents)
    agents.Get("/:agentId", agentHandler.GetAgent)
    agents.Patch("/:agentId", agentHandler.UpdateAgent)
    agents.Delete("/:agentId", agentHandler.DeleteAgent)

    // Nested routes
    agents.Post("/:agentId/chat", agentHandler.Chat)
    agents.Get("/:agentId/chat/stream", agentHandler.ChatStream)
    agents.Get("/:agentId/deployments", agentHandler.ListDeployments)
    agents.Post("/:agentId/deployments", agentHandler.CreateDeployment)
}
```

### Step 4: Implement Middleware

See `references/middleware-patterns.md` for:
- Authentication middleware
- Rate limiting
- Request tracing
- Error handling

### Step 5: Add SSE Streaming

```go
// For streaming endpoints (chat, events)
func (h *AgentHandler) ChatStream(c *fiber.Ctx) error {
    c.Set("Content-Type", "text/event-stream")
    c.Set("Cache-Control", "no-cache")
    c.Set("Connection", "keep-alive")

    agentID := c.Params("agentId")
    
    c.Context().SetBodyStreamWriter(func(w *bufio.Writer) {
        for event := range h.service.StreamChat(c.Context(), agentID) {
            fmt.Fprintf(w, "event: %s\n", event.Type)
            fmt.Fprintf(w, "data: %s\n\n", event.Data)
            w.Flush()
        }
    })
    
    return nil
}
```

## Error Handling

Follow RFC 7807 Problem Details:

```go
// internal/api/dto/errors.go
type ErrorResponse struct {
    Type     string            `json:"type"`
    Title    string            `json:"title"`
    Status   int               `json:"status"`
    Detail   string            `json:"detail"`
    Instance string            `json:"instance,omitempty"`
    TraceID  string            `json:"trace_id,omitempty"`
    Errors   []ValidationError `json:"errors,omitempty"`
}

func NewError(c *fiber.Ctx, status int, title, detail string) error {
    return c.Status(status).JSON(ErrorResponse{
        Type:     errorTypeURL(status),
        Title:    title,
        Status:   status,
        Detail:   detail,
        Instance: c.Path(),
        TraceID:  c.Locals("traceID").(string),
    })
}
```

## Validation

Use go-playground/validator:

```go
import "github.com/go-playground/validator/v10"

var validate = validator.New()

func init() {
    // Custom validators
    validate.RegisterValidation("agent_name", validateAgentName)
}
```

## Testing

```go
// internal/api/handlers/agents_test.go
func TestCreateAgent(t *testing.T) {
    app := fiber.New()
    // Setup mock services
    svc := mocks.NewAgentService(t)
    handler := NewAgentHandler(svc)
    
    app.Post("/v1/agents", handler.CreateAgent)

    req := httptest.NewRequest("POST", "/v1/agents", strings.NewReader(`{
        "name": "test-agent",
        "framework": "google-adk",
        "config": {"model": "gpt-4"}
    }`))
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("X-Project-ID", "prj_test123")

    resp, _ := app.Test(req)
    assert.Equal(t, 201, resp.StatusCode)
}
```

## Resources

- `references/middleware-patterns.md` - Auth, logging, rate limiting patterns
- `references/sse-streaming.md` - Server-Sent Events implementation
- `assets/handler-template.go` - Handler boilerplate template
