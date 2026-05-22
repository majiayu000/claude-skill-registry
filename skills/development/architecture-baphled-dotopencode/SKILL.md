---
name: architecture
description: Enforce architectural patterns and layer boundaries
category: Code Quality
---

# Skill: architecture

## What I do

I enforce clean architecture: layer separation (domain → service → repository → handler), dependency direction (inward only), and boundary rules that keep the codebase maintainable as it grows.

## When to use me

- Designing new packages, intents, or modules
- Reviewing code for layer boundary violations
- Deciding where new logic belongs (domain vs service vs handler)
- Structuring Go projects with clean dependency flow
- Diagnosing tight coupling or circular dependencies

## Core principles

1. **Dependencies point inward** — Domain knows nothing about HTTP, databases, or frameworks
2. **Layer isolation** — Each layer has a single responsibility; no layer skipping
3. **Interface boundaries** — Layers communicate through interfaces defined by the consumer
4. **Domain is king** — Business rules live in domain; everything else is infrastructure
5. **Package by feature** — Group by capability (`user/`, `order/`), not by type (`models/`, `handlers/`)

## Patterns & examples

**Layer responsibilities:**

| Layer | Responsibility | Depends on | Example |
|-------|---------------|------------|---------|
| Domain | Business rules, entities, value objects | Nothing | `User`, `Email`, validation |
| Service | Orchestration, use cases | Domain | `RegisterUser`, `PlaceOrder` |
| Repository | Data persistence (interface) | Domain | `UserRepository` interface |
| Handler | HTTP/CLI transport | Service | `POST /users` handler |
| Infrastructure | Framework adapters | Domain interfaces | GORM repo, SMTP sender |

**Dependency flow in Go:**
```go
// domain/ — no imports from other layers
type User struct {
    ID    string
    Email string
    Name  string
}

type UserRepository interface {
    Save(ctx context.Context, user *User) error
    FindByEmail(ctx context.Context, email string) (*User, error)
}

// service/ — depends only on domain
type UserService struct {
    repo domain.UserRepository  // interface, not concrete
}

func (s *UserService) Register(ctx context.Context, email, name string) error {
    user := &domain.User{Email: email, Name: name}
    return s.repo.Save(ctx, user)
}

// handler/ — depends on service
func (h *Handler) RegisterUser(w http.ResponseWriter, r *http.Request) {
    // Decode request, call service, encode response
    err := h.svc.Register(r.Context(), req.Email, req.Name)
}

// infrastructure/ — implements domain interfaces
type GORMUserRepo struct{ db *gorm.DB }
func (r *GORMUserRepo) Save(ctx context.Context, u *domain.User) error { ... }
```

**Package structure (feature-based):**
```
intent/
├── user/
│   ├── domain/       # entities, value objects, interfaces
│   ├── service/      # use cases
│   ├── repository/   # data access implementation
│   └── handler/      # HTTP handlers
├── order/
│   ├── domain/
│   ├── service/
│   └── ...
```

**Boundary validation checklist:**
- Domain imports: only stdlib (`fmt`, `errors`, `time`)
- Service imports: domain only
- Handler imports: service only (never domain directly for persistence)
- Repository imports: domain (for interfaces/entities) + infrastructure (GORM, etc.)

## Anti-patterns to avoid

- ❌ **Handler calling repository directly** — Skips business logic; service layer exists for a reason
- ❌ **Domain importing infrastructure** — Domain must not know about GORM, HTTP, or external services
- ❌ **Circular dependencies** — Package A imports B, B imports A; restructure with interfaces
- ❌ **God package** — Single `models/` package with everything; package by feature instead
- ❌ **Leaking implementation** — Returning GORM models from service layer; map to domain types

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Domain-Architecture/Architecture.md`

## Related skills

- `domain-modeling` - Designing entities and value objects in the domain layer
- `service-layer` - Orchestrating use cases in the service layer
- `design-patterns` - Patterns that support architectural boundaries
- `clean-code` - Code quality within each layer
- `modular-design` - Unit-level composability and testability within each layer
