# Project Guidelines Skill (Example)

This is an example of a project-specific skill. Use this as a template for your own projects.

Based on a Shopify embedded application with Go backend and React frontend.

---

## When to Use

Reference this skill when working on the specific project it's designed for. Project skills contain:
- Architecture overview
- File structure
- Code patterns
- Testing requirements
- Deployment workflow

---

## Architecture Overview

**Tech Stack:**
- **Frontend**: React 19 + Vite 7, TypeScript, Shopify Polaris Web Components
- **Backend**: Go 1.21+ with Fiber v3
- **Database**: PostgreSQL 17 with pgx
- **Cache**: Redis 7
- **Queue**: RabbitMQ 3.12
- **Shopify**: OAuth, GraphQL Admin API, Webhooks
- **Testing**: Vitest (frontend), Go testing (backend)

**Services:**
```
┌─────────────────────────────────────────────────────────────┐
│                    Shopify Admin (iframe)                   │
│  React 19 + Vite + Polaris Web Components + App Bridge      │
│  Deployed: Vercel / Cloud Run / Fly.io                      │
└─────────────────────────────────────────────────────────────┘
                              │ Session Token
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         Go Backend                          │
│  Fiber v3 + pgx + Redis + RabbitMQ                          │
│  Deployed: Cloud Run / Fly.io / Railway                     │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┬───────────────┐
              ▼               ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
        │PostgreSQL│   │  Redis   │   │ RabbitMQ │   │ Shopify  │
        │   17     │   │    7     │   │   3.12   │   │   API    │
        └──────────┘   └──────────┘   └──────────┘   └──────────┘
```

---

## File Structure

```
project/
├── cmd/
│   └── server/
│       └── main.go           # Application entry point
│
├── internal/
│   ├── config/               # Configuration loading
│   ├── handler/              # HTTP handlers
│   │   ├── auth.go           # OAuth handlers
│   │   ├── products.go       # Product API handlers
│   │   └── webhooks.go       # Webhook handlers
│   ├── middleware/           # Fiber middleware
│   │   ├── auth.go           # Session token validation
│   │   ├── logging.go        # Request logging
│   │   └── recovery.go       # Panic recovery
│   ├── service/              # Business logic
│   ├── repository/           # Data access (pgx)
│   ├── shopify/              # Shopify integration
│   │   ├── oauth.go          # OAuth flow
│   │   ├── graphql.go        # GraphQL client
│   │   └── webhook.go        # Webhook verification
│   └── queue/                # RabbitMQ
│       ├── producer.go       # Message publishing
│       └── consumer.go       # Worker consumers
│
├── web/                      # React frontend
│   └── src/
│       ├── pages/            # React Router pages
│       ├── components/       # React components
│       ├── hooks/            # Custom hooks (TanStack Query)
│       ├── lib/              # Utilities, API client
│       ├── queries/          # Query key factories
│       └── types/            # TypeScript definitions
│
├── migrations/               # PostgreSQL migrations
├── deploy/                   # Deployment configs
└── scripts/                  # Utility scripts
```

---

## Code Patterns

### API Response Format (Go)

```go
package handler

import (
    "github.com/gofiber/fiber/v3"
)

type ApiResponse[T any] struct {
    Success bool   `json:"success"`
    Data    T      `json:"data,omitempty"`
    Error   string `json:"error,omitempty"`
}

func RespondJSON[T any](c fiber.Ctx, status int, data T) error {
    return c.Status(status).JSON(ApiResponse[T]{
        Success: true,
        Data:    data,
    })
}

func RespondError(c fiber.Ctx, status int, err string) error {
    return c.Status(status).JSON(ApiResponse[any]{
        Success: false,
        Error:   err,
    })
}
```

### Frontend API Calls (TanStack Query)

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getSessionToken } from '@shopify/app-bridge/utilities'

// Query key factory
export const productKeys = {
  all: ['products'] as const,
  lists: () => [...productKeys.all, 'list'] as const,
  list: (filters: ProductFilters) => [...productKeys.lists(), filters] as const,
  details: () => [...productKeys.all, 'detail'] as const,
  detail: (id: string) => [...productKeys.details(), id] as const,
}

// Fetch with session token
async function fetchWithAuth<T>(endpoint: string): Promise<T> {
  const token = await getSessionToken(app)
  const response = await fetch(`/api${endpoint}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  })

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`)
  }

  const data = await response.json()
  if (!data.success) {
    throw new Error(data.error)
  }

  return data.data
}

// Hook usage
export function useProducts(filters: ProductFilters) {
  return useQuery({
    queryKey: productKeys.list(filters),
    queryFn: () => fetchWithAuth<Product[]>(`/products?${new URLSearchParams(filters)}`),
  })
}
```

### Shopify Webhook Handler (Go)

```go
package handler

import (
    "crypto/hmac"
    "crypto/sha256"
    "encoding/base64"

    "github.com/gofiber/fiber/v3"
)

func (h *WebhookHandler) VerifyHMAC(c fiber.Ctx) bool {
    body := c.Body()

    mac := hmac.New(sha256.New, []byte(h.shopifySecret))
    mac.Write(body)
    expected := base64.StdEncoding.EncodeToString(mac.Sum(nil))

    return hmac.Equal(
        []byte(c.Get("X-Shopify-Hmac-SHA256")),
        []byte(expected),
    )
}

func (h *WebhookHandler) HandleOrderCreate(c fiber.Ctx) error {
    if !h.VerifyHMAC(c) {
        return RespondError(c, fiber.StatusUnauthorized, "Invalid HMAC")
    }

    // Publish to queue for async processing
    h.queue.Publish("orders.created", c.Body())

    return c.SendStatus(fiber.StatusOK)
}
```

### Repository Pattern (Go + pgx)

```go
package repository

import (
    "context"
    "github.com/jackc/pgx/v5/pgxpool"
)

type SessionRepository interface {
    GetByShop(ctx context.Context, shop string) (*Session, error)
    Upsert(ctx context.Context, session *Session) error
    Delete(ctx context.Context, shop string) error
}

type sessionRepo struct {
    pool *pgxpool.Pool
}

func NewSessionRepository(pool *pgxpool.Pool) SessionRepository {
    return &sessionRepo{pool: pool}
}

func (r *sessionRepo) GetByShop(ctx context.Context, shop string) (*Session, error) {
    var session Session
    err := r.pool.QueryRow(ctx, `
        SELECT id, shop, access_token, scope, created_at
        FROM sessions
        WHERE shop = $1
    `, shop).Scan(
        &session.ID,
        &session.Shop,
        &session.AccessToken,
        &session.Scope,
        &session.CreatedAt,
    )

    if err != nil {
        return nil, err
    }

    return &session, nil
}
```

---

## Testing Requirements

### Backend (Go)

```bash
# Run all tests
go test ./...

# Run with coverage
go test ./... -coverprofile=coverage.out
go tool cover -html=coverage.out

# Run specific package
go test ./internal/handler/... -v
```

**Test structure:**
```go
package handler_test

import (
    "net/http/httptest"
    "testing"

    "github.com/gofiber/fiber/v3"
)

func TestHealthCheck(t *testing.T) {
    app := fiber.New()
    h := NewHealthHandler()
    app.Get("/health", h.Handle)

    req := httptest.NewRequest("GET", "/health", nil)
    resp, err := app.Test(req, -1)
    if err != nil {
        t.Fatalf("Test request failed: %v", err)
    }

    if resp.StatusCode != fiber.StatusOK {
        t.Errorf("expected status 200, got %d", resp.StatusCode)
    }
}
```

### Frontend (Vitest)

```bash
# Run tests
cd web && npm run test

# Run with coverage
npm run test -- --coverage

# Run in watch mode
npm run test -- --watch
```

**Test structure:**
```typescript
import { render, screen } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { describe, it, expect } from 'vitest'
import { ProductList } from './ProductList'

const queryClient = new QueryClient()

describe('ProductList', () => {
  it('renders loading state', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <ProductList />
      </QueryClientProvider>
    )
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })
})
```

---

## Deployment Workflow

### Pre-Deployment Checklist

- [ ] All tests passing locally (`go test ./...` and `npm run test`)
- [ ] `go build ./...` succeeds
- [ ] `npm run build` succeeds (frontend)
- [ ] No hardcoded secrets
- [ ] Environment variables documented
- [ ] Database migrations ready

### Deployment Commands

```bash
# Build Go binary
go build -o server ./cmd/server

# Build frontend
cd web && npm run build

# Deploy to Fly.io
fly deploy

# Or deploy to Cloud Run
gcloud run deploy app --source .
```

### Environment Variables

```bash
# Backend (.env)
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379
RABBITMQ_URL=amqp://user:pass@host:5672
SHOPIFY_API_KEY=your_api_key
SHOPIFY_API_SECRET=your_api_secret
SHOPIFY_SCOPES=read_products,write_products

# Frontend (.env)
VITE_API_URL=https://api.example.com
VITE_SHOPIFY_API_KEY=your_api_key
```

---

## Critical Rules

1. **No emojis** in code, comments, or documentation
2. **Immutability** - prefer immutable data structures
3. **TDD** - write tests before implementation
4. **80% coverage** minimum
5. **Many small files** - 200-400 lines typical, 800 max
6. **No fmt.Println** in production code (use structured logging)
7. **Proper error handling** - always handle errors explicitly
8. **Input validation** with Zod (frontend) and custom validators (Go)
9. **HMAC verification** - CRITICAL for all Shopify webhooks
10. **Session token auth** - use App Bridge tokens, not OAuth for API calls

---

## Related Skills

- `coding-standards/` - General coding best practices
- `backend-patterns/` - Go API and database patterns
- `frontend-patterns/` - React and TanStack Query patterns
- `shopify-integration/` - Shopify OAuth, webhooks, GraphQL
- `queue-worker-patterns/` - RabbitMQ consumer patterns
- `tdd-workflow/` - Test-driven development methodology
