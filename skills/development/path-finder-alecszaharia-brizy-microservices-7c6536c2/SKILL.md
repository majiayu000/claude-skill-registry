---
name: path-finder
description: Provides correct file paths, import locations, and navigation guidance for brizy-go-services monorepo following Clean Architecture conventions and Go workspace structure. Helps locate entity files, navigate between layers (biz/data/service/server), find tests, resolve import paths, and answer "where is X located?" questions. Use when finding files, locating components, determining file paths, navigating project structure, resolving import paths, asking where files are located, or searching for entity/layer locations.
---

# Path Finder Skill

## Purpose

Navigate the brizy-go-services monorepo file structure following Clean Architecture patterns and Go workspace conventions.

## Workspace Structure

```
brizy-go-services/
├── go.work                          # Go workspace definition
├── go.work.sum                      # Workspace checksums
├── contracts/                       # Shared protobuf module
│   ├── go.mod
│   └── gen/                         # Generated code
│       └── {service}/
│           └── v1/
│               ├── {service}.pb.go
│               ├── {service}_grpc.pb.go
│               └── {service}.swagger.json
├── platform/                        # Shared utilities module
│   ├── go.mod
│   ├── events/                      # Pub/sub interfaces
│   ├── logger/                      # Watermill logger
│   ├── middleware/
│   ├── pagination/
│   └── adapters/
└── services/                        # Microservices
    └── {service}/                   # Individual service
        ├── go.mod
        ├── Makefile
        ├── cmd/
        │   ├── {service}/           # Main service
        │   │   ├── main.go
        │   │   ├── wire.go
        │   │   └── wire_gen.go
        │   └── {service}-worker/    # Optional: Event worker
        │       ├── main.go
        │       ├── wire.go
        │       └── wire_gen.go
        ├── internal/
        │   ├── biz/                 # Business logic layer
        │   │   ├── domain/          # Domain models and interfaces
        │   │   │   ├── models.go
        │   │   │   ├── interfaces.go
        │   │   │   └── errors.go
        │   │   ├── {entity}/        # Use case implementations
        │   │   │   ├── usecase.go
        │   │   │   ├── usecase_test.go
        │   │   │   └── validator.go
        │   │   ├── event/           # Optional: Event mappers
        │   │   │   ├── mapper.go
        │   │   │   ├── mapper_test.go
        │   │   │   └── topics.go
        │   │   └── provider.go
        │   ├── data/                # Data access layer
        │   │   ├── data.go
        │   │   ├── model/
        │   │   │   └── {entity}.go
        │   │   ├── repo/
        │   │   │   ├── {entity}.go
        │   │   │   └── {entity}_test.go
        │   │   ├── mq/              # Optional: Pub/sub wrappers
        │   │   │   ├── publisher.go
        │   │   │   └── subscriber.go
        │   │   └── common/
        │   │       └── transaction.go
        │   ├── handlers/            # Optional: Event handlers
        │   │   ├── provider.go
        │   │   └── {event}_handler.go
        │   ├── worker/              # Optional: Worker setup
        │   │   └── worker.go
        │   ├── service/             # Service layer (handlers)
        │   │   ├── service.go
        │   │   ├── {entity}.go
        │   │   ├── {entity}_test.go
        │   │   ├── mapper.go
        │   │   └── mapper_test.go
        │   ├── server/              # Server setup
        │   │   ├── grpc.go
        │   │   └── http.go
        │   └── conf/                # Configuration
        │       └── conf.proto
        └── configs/
            └── config.yaml
```

## Layer-Specific Paths

### Business Layer (biz)

**Location**: \`services/{service}/internal/biz/\`

**Structure** (Domain-Driven Design):
- \`domain/\` - Domain models, interfaces, and errors
  - \`models.go\` - Business domain models and DTOs
  - \`interfaces.go\` - Repository and service interface definitions
  - \`errors.go\` - Domain errors (ErrSymbolNotFound) and data layer errors (ErrDataNotFound)
- \`{entity}/\` - Use case implementations per entity
  - \`usecase.go\` - Use case implementation
  - \`usecase_test.go\` - Use case tests
  - \`validator.go\` - Validation logic
- \`event/\` - Event-related code (optional)
  - \`mapper.go\` - Event payload mappers
  - \`topics.go\` - Event topic constants
- \`provider.go\` - Wire ProviderSet

**Import Paths**:
- Domain types: \`{service}/internal/biz/domain\`
- Use cases: \`{service}/internal/biz/{entity}\`
- Event mappers: \`{service}/internal/biz/event\`

**Example**:
```go
// services/symbols/internal/biz/domain/interfaces.go
package domain

import "context"

type SymbolUseCase interface {
    GetSymbol(ctx context.Context, id uint64) (*Symbol, error)
}

type SymbolRepo interface {
    FindByID(ctx context.Context, id uint64) (*Symbol, error)
}

type SymbolEventPublisher interface {
    PublishSymbolCreated(ctx context.Context, symbol *Symbol) error
}
```

### Data Layer (data)

**Location**: \`services/{service}/internal/data/\`

**Subdirectories**:
- \`model/\` - GORM entities (database models)
- \`repo/\` - Repository implementations
- \`mq/\` - Message queue publisher/subscriber wrappers (optional)
- \`common/\` - Shared data layer utilities

**File Patterns**:
- \`data.go\` - Database setup and initialization
- \`model/{entity}.go\` - GORM entity definition
- \`repo/{entity}.go\` - Repository implementation
- \`repo/{entity}_test.go\` - Repository tests
- \`mq/publisher.go\` - Event publisher wrapper (optional)
- \`mq/subscriber.go\` - Event subscriber wrapper (optional)
- \`common/transaction.go\` - Transaction utilities

**Import Paths**:
- GORM models: \`{service}/internal/data/model\`
- Repositories: \`{service}/internal/data/repo\`
- Pub/sub wrappers: \`{service}/internal/data/mq\`
- Common utilities: \`{service}/internal/data/common\`

**Example**:
```go
// services/symbols/internal/data/repo/symbol.go
package repo

import (
    "symbols/internal/biz/domain"
    "symbols/internal/data/model"
)
```

### Service Layer (service)

**Location**: \`services/{service}/internal/service/\`

**File Patterns**:
- \`service.go\` - Service struct definition
- \`{entity}.go\` - gRPC/HTTP handler implementations
- \`{entity}_test.go\` - Service handler tests
- \`mapper.go\` - DTO ↔ Domain model conversions
- \`mapper_test.go\` - Mapper tests
- \`errors.go\` - Service error mapping

**Import Path**: \`{service}/internal/service\`

**Example**:
```go
// services/symbols/internal/service/symbols.go
package service

import (
    v1 "contracts/gen/symbols/v1"
    "symbols/internal/biz/domain"
)
```

### Server Layer (server)

**Location**: \`services/{service}/internal/server/\`

**Files**:
- \`grpc.go\` - gRPC server setup
- \`http.go\` - HTTP server setup (Kratos bindings)

**Import Path**: \`{service}/internal/server\`

### Event Handlers Layer (handlers) - Optional

**Location**: \`services/{service}/internal/handlers/\`

**File Patterns**:
- \`provider.go\` - Wire ProviderSet
- \`{event}_handler.go\` - Event handler implementations
- \`{event}_handler_test.go\` - Handler tests (optional)

**Import Path**: \`{service}/internal/handlers\`

**Example**:
```go
// services/symbols/internal/handlers/lifecycle.go
package handlers

import (
    "{service}/internal/biz"
    "github.com/ThreeDotsLabs/watermill/message"
)

type LifecycleEventHandler struct {
    logger   *log.Helper
    symbolUC biz.SymbolUseCase
}
```

### Worker Layer (worker) - Optional

**Location**: \`services/{service}/internal/worker/\`

**File Patterns**:
- \`worker.go\` - Worker lifecycle management (Start/Stop)
- \`provider.go\` - Wire ProviderSet (optional)

**Import Path**: \`{service}/internal/worker\`

**Example**:
```go
// services/symbols/internal/worker/worker.go
package worker

import (
    "github.com/ThreeDotsLabs/watermill/message"
)

func NewWorker(router *message.Router, logger log.Logger) Worker
func NewRouter(cfg *conf.Data, handlers..., logger) *message.Router
```

### Configuration

**Location**: \`services/{service}/internal/conf/\`

**Files**:
- \`conf.proto\` - Configuration protobuf schema

**Runtime Config**: \`services/{service}/configs/config.yaml\`

## Shared Modules

### Contracts (Protobuf)

**Location**: \`contracts/gen/{service}/v1/\`

**Generated Files**:
- \`{service}.pb.go\` - Protobuf messages
- \`{service}_grpc.pb.go\` - gRPC service definitions
- \`{service}_http.pb.go\` - Kratos HTTP bindings
- \`{service}.swagger.json\` - OpenAPI spec

**Import Path**: \`contracts/gen/{service}/v1\`

**Example**:
```go
import v1 "contracts/gen/symbols/v1"
```

### Platform Utilities

**Location**: \`platform/{package}/\`

**Packages**:
- \`platform/events\` - Publisher/Subscriber interfaces for event-driven architecture
- \`platform/logger\` - Structured logging with Watermill integration
- \`platform/middleware\` - Request ID middleware with context propagation
- \`platform/pagination\` - Offset-based pagination utilities
- \`platform/adapters\` - Common adapters (transformers, validators)

**Import Examples**:
```go
import "platform/events"
import "platform/logger"
import "platform/middleware"
import "platform/pagination"
```

## Path Resolution Rules

### 1. Service-Specific Code

Pattern: \`services/{service}/internal/{layer}/{file}.go\`

Examples:
- Business logic: \`services/symbols/internal/biz/symbols.go\`
- Repository: \`services/symbols/internal/data/repo/symbol.go\`
- GORM model: \`services/symbols/internal/data/model/symbol.go\`
- Service handler: \`services/symbols/internal/service/symbols.go\`

### 2. Test Files

Pattern: \`{same_path_as_implementation}_test.go\`

Examples:
- \`services/symbols/internal/biz/symbols_test.go\`
- \`services/symbols/internal/data/repo/symbol_test.go\`
- \`services/symbols/internal/service/symbols_test.go\`

### 3. Proto Definitions

**Source**: \`api/{service}/v1/{service}.proto\`
**Generated**: \`contracts/gen/{service}/v1/\`

### 4. Configuration

**Proto Schema**: \`services/{service}/internal/conf/conf.proto\`
**Runtime Config**: \`services/{service}/configs/config.yaml\`

## Quick Reference Table

| What | Path Pattern | Example |
|------|-------------|---------|
| Use case interface | \`services/{service}/internal/biz/domain/interfaces.go\` | \`services/symbols/internal/biz/domain/interfaces.go\` |
| Use case implementation | \`services/{service}/internal/biz/{entity}/usecase.go\` | \`services/symbols/internal/biz/symbol/usecase.go\` |
| Business models | \`services/{service}/internal/biz/domain/models.go\` | \`services/symbols/internal/biz/domain/models.go\` |
| Domain errors | \`services/{service}/internal/biz/domain/errors.go\` | \`services/symbols/internal/biz/domain/errors.go\` |
| Validator | \`services/{service}/internal/biz/{entity}/validator.go\` | \`services/symbols/internal/biz/symbol/validator.go\` |
| Event mappers | \`services/{service}/internal/biz/event/mapper.go\` | \`services/symbols/internal/biz/event/mapper.go\` |
| GORM entity | \`services/{service}/internal/data/model/{entity}.go\` | \`services/symbols/internal/data/model/symbol.go\` |
| Repository | \`services/{service}/internal/data/repo/{entity}.go\` | \`services/symbols/internal/data/repo/symbol.go\` |
| Service handler | \`services/{service}/internal/service/{entity}.go\` | \`services/symbols/internal/service/symbols.go\` |
| Mapper | \`services/{service}/internal/service/mapper.go\` | \`services/symbols/internal/service/mapper.go\` |
| Wire config | \`services/{service}/cmd/{service}/wire.go\` | \`services/symbols/cmd/symbols/wire.go\` |
| Main entry | \`services/{service}/cmd/{service}/main.go\` | \`services/symbols/cmd/symbols/main.go\` |
| Proto def | \`api/{service}/v1/{service}.proto\` | \`api/symbols/v1/symbols.proto\` |
| Generated proto | \`contracts/gen/{service}/v1/{service}.pb.go\` | \`contracts/gen/symbols/v1/symbols.pb.go\` |

## Import Path Patterns

### Within Same Service

```go
// From service layer to biz domain layer
import "{service}/internal/biz/domain"

// From use case to domain layer
import "{service}/internal/biz/domain"

// From repo to model
import "{service}/internal/data/model"

// From repo to domain (for interfaces and errors)
import "{service}/internal/biz/domain"
```

### Cross-Module Imports

```go
// Platform utilities
import "platform/pagination"
import "platform/middleware"

// Generated protobuf
import v1 "contracts/gen/symbols/v1"

// GORM
import "gorm.io/gorm"

// Kratos
import "github.com/go-kratos/kratos/v2/log"
```

## Common Scenarios

### Finding Entity Files

Given entity name \`Symbol\`:
- Business model: \`services/symbols/internal/biz/domain/models.go\` (struct \`Symbol\`)
- Repository interface: \`services/symbols/internal/biz/domain/interfaces.go\` (interface \`SymbolRepo\`)
- Use case interface: \`services/symbols/internal/biz/domain/interfaces.go\` (interface \`SymbolUseCase\`)
- Use case implementation: \`services/symbols/internal/biz/symbol/usecase.go\`
- Validator: \`services/symbols/internal/biz/symbol/validator.go\`
- GORM entity: \`services/symbols/internal/data/model/symbol.go\` (struct \`Symbol\`)
- Repository implementation: \`services/symbols/internal/data/repo/symbol.go\`
- Service handler: \`services/symbols/internal/service/symbols.go\`

### Finding Tests

Same directory as implementation + \`_test.go\` suffix:
- \`services/symbols/internal/biz/symbol/usecase_test.go\`
- \`services/symbols/internal/data/repo/symbol_test.go\`
- \`services/symbols/internal/service/symbols_test.go\`
- \`services/symbols/internal/service/mapper_test.go\`

### Finding Configuration

- Schema: \`services/symbols/internal/conf/conf.proto\`
- Runtime: \`services/symbols/configs/config.yaml\`
- Wire DI: \`services/symbols/cmd/symbols/wire.go\`

## Directory Naming Conventions

- Use **singular** for: \`biz\`, \`data\`, \`service\`, \`server\`, \`conf\`
- Use **plural** for: \`services\`, \`configs\`, \`contracts\`
- Use **snake_case** for: multi-word directories (e.g., \`symbol_data\`)
- Use **lowercase** throughout

## File Naming Conventions

- Use **singular entity name**: \`symbol.go\` for GORM models and repositories
- Use **usecase.go**: for use case implementations (not entity name)
- Use **plural entity name**: \`symbols.go\` for service handlers (matches proto)
- Use **snake_case**: \`symbol_data.go\` for multi-word names
- Use **domain package**: for models, interfaces, and errors (not individual files per entity)
- Tests: \`{filename}_test.go\`

