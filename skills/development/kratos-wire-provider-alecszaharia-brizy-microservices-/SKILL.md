---
name: kratos-wire-provider
description: Manages Wire dependency injection providers in go-kratos microservices. Adds constructors to ProviderSets and regenerates Wire code. Use when integrating new components into dependency injection.
---

<objective>
Add constructor functions to appropriate Wire ProviderSets and regenerate dependency injection code for go-kratos microservices.
</objective>

<quick_start>
To add a provider to the biz layer:

1. **Add to ProviderSet** in `internal/biz/biz.go`:
```go
var ProviderSet = wire.NewSet(
	NewSymbolValidator,
	NewSymbolUseCase,
	NewProductUseCase,  // Add your constructor
)
```

2. **Regenerate Wire code**:
```bash
cd services/{service-name}
make generate
```
</quick_start>

<provider_sets>
## ProviderSet Locations

**Data Layer** (`internal/data/data.go`):
- Repository implementations
- Database connection
- Transaction manager

```go
var ProviderSet = wire.NewSet(
	NewData,           // Database setup
	NewTransaction,    // Transaction manager
	repo.NewSymbolRepo,
	repo.NewProductRepo,
)
```

**Business Layer** (`internal/biz/biz.go`):
- Use cases
- Validators

```go
var ProviderSet = wire.NewSet(
	NewSymbolValidator,
	NewSymbolUseCase,
	NewProductUseCase,
)
```

**Service Layer** (`internal/service/service.go`):
- Service handlers

```go
var ProviderSet = wire.NewSet(
	NewSymbolService,
	NewProductService,
)
```

**Server Layer** (`internal/server/server.go`):
- HTTP and gRPC servers

```go
var ProviderSet = wire.NewSet(
	NewHTTPServer,
	NewGRPCServer,
)
```
</provider_sets>

<wire_process>
## Wire Generation Process

**File**: `cmd/{service}/wire.go` defines dependencies:
```go
//go:build wireinject

func InitApp(*conf.Server, *conf.Data, log.Logger) (*App, error) {
	wire.Build(
		server.ProviderSet,
		service.ProviderSet,
		biz.ProviderSet,
		data.ProviderSet,
		newApp,
	)
	return &App{}, nil
}
```

**Generated**: `cmd/{service}/wire_gen.go` (auto-generated, never edit)

**Command**: `make generate` runs:
```bash
GOWORK=off go generate ./cmd/{service}/...
```
</wire_process>

<ordering_rules>
## Provider Ordering

**Within ProviderSet**:
- Alphabetical order (recommended)
- OR grouped by functionality
- Be consistent with existing pattern

**Between ProviderSets** (in wire.Build):
1. `server.ProviderSet` (outermost layer)
2. `service.ProviderSet`
3. `biz.ProviderSet`
4. `data.ProviderSet` (innermost layer)
5. `newApp` (application constructor)
</ordering_rules>

<common_tasks>
## Common Tasks

**Add new repository**:
1. Add constructor to `data.ProviderSet`
2. Run `make generate`

**Add new use case**:
1. Add constructor to `biz.ProviderSet`
2. Run `make generate`

**Add new service handler**:
1. Add constructor to `service.ProviderSet`
2. Run `make generate`

**Troubleshooting**:
- If Wire errors, check constructor signatures match interface returns
- Ensure all dependencies are provided in ProviderSets
- Check for circular dependencies
- Run `GOWORK=off go mod tidy` if module issues
</common_tasks>

<wire_annotations>
## Wire Annotations

**Optional**: Use Wire build tags for conditional providers:
```go
//go:build wireinject
// +build wireinject
```

**Providers must**:
- Return types that match interface declarations
- Have all parameters available in dependency graph
- Not create circular dependencies
</wire_annotations>

<success_criteria>
Wire integration is successful when:
- [ ] Constructor added to appropriate ProviderSet
- [ ] Alphabetical/consistent ordering maintained
- [ ] `make generate` completes without errors
- [ ] `wire_gen.go` updated successfully
- [ ] Service compiles: `make build`
- [ ] Tests pass: `make test`
- [ ] No circular dependency errors
</success_criteria>

<error_messages>
## Common Wire Errors

**"no provider found for X"**:
→ Add constructor for X to appropriate ProviderSet

**"cycle in dependency graph"**:
→ Circular dependency detected, refactor to break cycle

**"provider returns interface but is not implemented"**:
→ Check constructor returns interface type, struct implements all methods

**"multiple providers for type"**:
→ Same type provided by multiple constructors, remove duplicate
</error_messages>