---
name: kratos-new-service
description: Creates a new go-kratos microservice skeleton with clean architecture (server/service/biz/data), minimal Wire setup, HTTP + gRPC metrics, and complete project structure. Use when scaffolding new services in the brizy-go-services monorepo.
---

<objective>
Scaffold a new go-kratos microservice in the `services/` directory following clean architecture patterns. Creates minimal skeleton with:
- Single cmd entry point with main.go and Wire setup
- Clean architecture layers (server/service/biz/data) with empty implementations
- Minimal configuration (Server, Data, Metrics)
- HTTP + gRPC server setup with metrics middleware
- Complete Makefile with standard targets
- No event handlers, publishers, or subscribers
- No proto definitions (created separately)
</objective>

<quick_start>
When invoked, this skill will:
1. Ask for the service name interactively
2. Validate the name (lowercase, alphanumeric, hyphens only)
3. Create complete service skeleton in `services/{service-name}/`
4. Generate Wire dependency injection code
5. Create initial configs/config.yaml

The service will be ready to build but will need proto definitions added separately.
</quick_start>

<workflow>
## Step 1: Get and Validate Service Name

Ask the user for the service name:
```
What is the name of the new service?

Requirements:
- Lowercase letters, numbers, and hyphens only
- Must be a valid Go module name
- Will be used for directory name, module path, and service identification

Example: auth, user-management, notification-service
```

Validate the input:
- Only lowercase letters (a-z), numbers (0-9), and hyphens (-) allowed
- No consecutive hyphens
- Cannot start or end with a hyphen
- Length: 3-50 characters

If invalid, explain the issue and ask again.

## Step 2: Check for Conflicts

Verify that `services/{service-name}/` does not already exist:

```bash
ls services/{service-name} 2>/dev/null
```

If it exists, inform the user and stop. Do not overwrite existing services.

## Step 3: Create Directory Structure

Create the complete directory structure:

```bash
mkdir -p services/{service-name}/cmd/{service-name}
mkdir -p services/{service-name}/internal/biz
mkdir -p services/{service-name}/internal/data/model
mkdir -p services/{service-name}/internal/data/repo
mkdir -p services/{service-name}/internal/service
mkdir -p services/{service-name}/internal/server
mkdir -p services/{service-name}/internal/conf
mkdir -p services/{service-name}/configs
mkdir -p services/{service-name}/bin
```

## Step 4: Create Configuration Files

### 4.1 Create internal/conf/conf.proto

```protobuf
syntax = "proto3";

package conf;

option go_package = "services/{service-name}/internal/conf;conf";

import "google/protobuf/duration.proto";

message Bootstrap {
  Server server = 1;
  Data data = 2;
  Metrics metrics = 3;
}

message Server {
  message HTTP {
    string network = 1;
    string addr = 2;
    google.protobuf.Duration timeout = 3;
  }
  message GRPC {
    string network = 1;
    string addr = 2;
    google.protobuf.Duration timeout = 3;
  }
  HTTP http = 1;
  GRPC grpc = 2;
}

message Data {
  message Database {
    string driver = 1;
    string source = 2;
  }
  Database database = 1;
}

message Metrics {
  bool enabled = 1;
  string service_name = 2;
  string path = 3;
  bool include_runtime = 4;
}
```

### 4.2 Create configs/config.yaml

```yaml
server:
  http:
    addr: 0.0.0.0:8000
    timeout: 5s
  grpc:
    addr: 0.0.0.0:9000
    timeout: 5s
data:
  database:
    driver: postgres
    source: postgres://user:password@localhost:5432/{service-name}?sslmode=disable
metrics:
  enabled: true
  path: /metrics
  include_runtime: true
```

Replace `{service-name}` with the actual service name in the YAML.

## Step 5: Create Data Layer Files

### 5.1 Create internal/data/data.go

```go
package data

import (
	"github.com/go-kratos/kratos/v2/log"
	"github.com/google/wire"
	"services/{service-name}/internal/conf"
)

// ProviderSet is data providers.
var ProviderSet = wire.NewSet(
	NewData,
)

// Data encapsulates all data access dependencies.
type Data struct {
	log *log.Helper
	// db *gorm.DB - uncomment when adding GORM
}

// NewData creates a new Data instance.
func NewData(c *conf.Data, logger log.Logger) (*Data, func(), error) {
	logHelper := log.NewHelper(log.With(logger, "module", "data"))

	d := &Data{
		log: logHelper,
	}

	cleanup := func() {
		logHelper.Info("closing data resources")
	}

	return d, cleanup, nil
}
```

Replace `{service-name}` with the actual service name.

## Step 6: Create Business Logic Layer Files

### 6.1 Create internal/biz/interfaces.go

```go
package biz

// Repository interfaces will be defined here
// Example:
// type ExampleRepo interface {
// 	Save(ctx context.Context, example *Example) error
// 	FindByID(ctx context.Context, id int64) (*Example, error)
// }
```

### 6.2 Create internal/biz/biz.go

```go
package biz

import (
	"github.com/go-kratos/kratos/v2/log"
	"github.com/google/wire"
)

// ProviderSet is business logic providers.
var ProviderSet = wire.NewSet()
```

## Step 7: Create Service Layer Files

### 7.1 Create internal/service/service.go

```go
package service

import (
	"github.com/google/wire"
	"services/{service-name}/internal/biz"
)

// ProviderSet is service providers.
var ProviderSet = wire.NewSet(
	NewService,
)

// Service encapsulates business logic dependencies.
type Service struct {
	log *log.Helper
}

// NewService creates a new Service instance.
func NewService(logger log.Logger) *Service {
	return &Service{
		log: log.NewHelper(log.With(logger, "module", "service")),
	}
}
```

Replace `{service-name}` with the actual service name.

## Step 8: Create Server Layer Files

### 8.1 Create internal/server/http.go

```go
package server

import (
	"github.com/go-kratos/kratos/v2/log"
	"github.com/go-kratos/kratos/v2/middleware/logging"
	"github.com/go-kratos/kratos/v2/middleware/recovery"
	"github.com/go-kratos/kratos/v2/transport/http"
	"platform/metrics"
	"services/{service-name}/internal/conf"
	"services/{service-name}/internal/service"
)

// NewHTTPServer creates a new HTTP server.
func NewHTTPServer(
	c *conf.Server,
	logger log.Logger,
	svc *service.Service,
	metricsRegistry *metrics.Registry,
) *http.Server {
	var opts = []http.ServerOption{
		http.Middleware(
			recovery.Recovery(),
			logging.Server(logger),
			metrics.HTTPMiddleware(metricsRegistry),
		),
	}
	if c.Http.Network != "" {
		opts = append(opts, http.Network(c.Http.Network))
	}
	if c.Http.Addr != "" {
		opts = append(opts, http.Address(c.Http.Addr))
	}
	if c.Http.Timeout != nil {
		opts = append(opts, http.Timeout(c.Http.Timeout.AsDuration()))
	}
	srv := http.NewServer(opts...)

	// Register service handlers here
	// Example:
	// v1.RegisterExampleServiceHTTPServer(srv, svc)

	return srv
}
```

Replace `{service-name}` with the actual service name.

### 8.2 Create internal/server/grpc.go

```go
package server

import (
	"github.com/go-kratos/kratos/v2/log"
	"github.com/go-kratos/kratos/v2/middleware/logging"
	"github.com/go-kratos/kratos/v2/middleware/recovery"
	"github.com/go-kratos/kratos/v2/transport/grpc"
	"platform/metrics"
	"services/{service-name}/internal/conf"
	"services/{service-name}/internal/service"
)

// NewGRPCServer creates a new gRPC server.
func NewGRPCServer(
	c *conf.Server,
	logger log.Logger,
	svc *service.Service,
	metricsRegistry *metrics.Registry,
) *grpc.Server {
	var opts = []grpc.ServerOption{
		grpc.Middleware(
			recovery.Recovery(),
			logging.Server(logger),
			metrics.GRPCMiddleware(metricsRegistry),
		),
	}
	if c.Grpc.Network != "" {
		opts = append(opts, grpc.Network(c.Grpc.Network))
	}
	if c.Grpc.Addr != "" {
		opts = append(opts, grpc.Address(c.Grpc.Addr))
	}
	if c.Grpc.Timeout != nil {
		opts = append(opts, grpc.Timeout(c.Grpc.Timeout.AsDuration()))
	}
	srv := grpc.NewServer(opts...)

	// Register service handlers here
	// Example:
	// v1.RegisterExampleServiceServer(srv, svc)

	return srv
}
```

Replace `{service-name}` with the actual service name.

### 8.3 Create internal/server/server.go

```go
package server

import (
	"github.com/google/wire"
)

// ProviderSet is server providers.
var ProviderSet = wire.NewSet(
	NewHTTPServer,
	NewGRPCServer,
	NewMetricsRegistry,
)
```

### 8.4 Create internal/server/metrics.go

```go
package server

import (
	"platform/metrics"
	"services/{service-name}/internal/conf"
)

// NewMetricsRegistry creates a new metrics registry.
func NewMetricsRegistry(c *conf.Metrics) *metrics.Registry {
	if !c.Enabled {
		return nil
	}

	return metrics.NewRegistry(c.ServiceName, c.IncludeRuntime)
}
```

Replace `{service-name}` with the actual service name.

## Step 9: Create Command Layer Files

### 9.1 Create cmd/{service-name}/main.go

```go
package main

import (
	"flag"
	"os"

	"github.com/go-kratos/kratos/v2"
	"github.com/go-kratos/kratos/v2/config"
	"github.com/go-kratos/kratos/v2/config/file"
	"github.com/go-kratos/kratos/v2/log"
	"github.com/go-kratos/kratos/v2/transport/http"
	"services/{service-name}/internal/conf"
)

// go build -ldflags "-X main.Version=x.y.z"
var (
	// Name is the name of the compiled software.
	Name string = "symbol-service"
	// Version is the version of the compiled software.
	Version string = "1.0"
	// configFile is the config flag.
	configFile string

	id, _ = os.Hostname()
)

func init() {
	flag.StringVar(&configFile, "conf", "configs/config.yaml", "config path, eg: --conf config.yaml")
}

var buildInfo = build.NewBuildInfo(Name, Version)

func main() {
	flag.Parse()
	logger := log.With(log.NewStdLogger(os.Stdout),
		"ts", log.DefaultTimestamp,
		"caller", log.DefaultCaller,
		"service.name", "{service-name}",
	)

	c := config.New(
		config.WithSource(
			file.NewSource(flagconf),
		),
	)
	defer c.Close()

	if err := c.Load(); err != nil {
		panic(err)
	}

	var bc conf.Bootstrap
	if err := c.Scan(&bc); err != nil {
		panic(err)
	}

	app, cleanup, err := wireApp(buildInfo, bc.Server, bc.Data, bc.Metrics, logger)
	if err != nil {
		panic(err)
	}
	defer cleanup()

	// Start and wait for stop signal
	if err := app.Run(); err != nil {
		panic(err)
	}
}

func newApp(logger log.Logger, hs *http.Server, gs *grpc.Server) *kratos.App {
	return kratos.New(
		kratos.ID(id),
		kratos.Name(Name),
		kratos.Version(Version),
		kratos.Metadata(map[string]string{}),
		kratos.Logger(logger),
		kratos.Server(
			gs,
			hs,
		),
	)
}
```

Replace `{service-name}` with the actual service name.

### 9.2 Create cmd/{service-name}/wire.go

```go
//go:build wireinject
// +build wireinject

package main

import (
	platform_build_info "platform/build"
	platform_logger "platform/logger"
	
	"github.com/go-kratos/kratos/v2"
	"github.com/go-kratos/kratos/v2/log"
	"github.com/google/wire"
	"services/{service-name}/internal/biz"
	"services/{service-name}/internal/conf"
	"services/{service-name}/internal/data"
	"services/{service-name}/internal/server"
	"services/{service-name}/internal/service"
)

// wireApp builds the application with dependency injection.
func wireApp(*platform_build_info.ServiceBuildInfo, *conf.Data, *conf.Metrics, log.Logger) (*kratos.App, func(), error) {
	panic(wire.Build(
		platform_logger.ProviderSet,
		server.ProviderSet,
		service.ProviderSet,
		biz.ProviderSet,
		data.ProviderSet,
		newApp,
	))
}
```

Replace `{service-name}` with the actual service name.

## Step 10: Create Build Configuration Files

### 10.1 Create go.mod

```go
module services/{service-name}

go 1.25.0

require (
    github.com/envoyproxy/protoc-gen-validate v1.3.0
    github.com/go-kratos/kratos/contrib/middleware/validate/v2 v2.0.0-20251217105121-fb8e43efb207
    github.com/go-kratos/kratos/v2 v2.9.2
    github.com/go-playground/validator/v10 v10.30.1
    github.com/google/wire v0.7.0
    github.com/gorilla/handlers v1.5.2
    github.com/stretchr/testify v1.11.1
    go.uber.org/automaxprocs v1.6.0
    google.golang.org/protobuf v1.36.11
    gorm.io/driver/mysql v1.6.0
    gorm.io/driver/sqlite v1.6.0
    gorm.io/gorm v1.31.1
)

```

Replace `{service-name}` with the actual service name.

### 10.2 Create Makefile

```makefile
GOHOSTOS:=$(shell go env GOHOSTOS)
GOPATH:=$(shell go env GOPATH)
VERSION=$(shell git describe --tags --always)

ifeq ($(GOHOSTOS), windows)
	#the `find.exe` is different from `find` in bash/shell.
	#to see https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/find.
	#changed to use git-bash.exe to run find cli or other cli friendly, caused of every developer has a Git.
	#Git_Bash= $(subst cmd\,bin\bash.exe,$(dir $(shell where git)))
	Git_Bash=$(subst \,/, $(subst cmd\,bin\bash.exe,$(dir $(shell where git))))
	INTERNAL_PROTO_FILES=$(shell $(Git_Bash) -c "find internal -name *.proto")
	API_PROTO_FILES=$(shell $(Git_Bash) -c "find api -name *.proto")
else
	INTERNAL_PROTO_FILES=$(shell find internal -name *.proto)
	API_PROTO_FILES=$(shell find api -name *.proto)
endif

.PHONY: init config api build generate all test coverage help

APP_NAME := symbols
BIN_DIR := bin

# init env
init:
	go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
	go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
	go install github.com/go-kratos/kratos/cmd/kratos/v2@latest
	go install github.com/go-kratos/kratos/cmd/protoc-gen-go-http/v2@latest
	go install github.com/google/gnostic/cmd/protoc-gen-openapi@latest
	go install github.com/google/wire/cmd/wire@latest
	go install github.com/envoyproxy/protoc-gen-validate@latest

# generate internal proto
config:
	buf dep update
	buf lint
	buf format -w
	buf generate

# build
build: service worker

service: generate
	go build -o $(BIN_DIR)/$(APP_NAME) ./cmd/$(APP_NAME)

# generate wire files
generate:
	wire ./cmd/symbols
	go mod tidy

# generate all
all:
	make config;
	make generate;

# run unit tests
test:
	go test -v -race -coverprofile=coverage.out ./internal/...

# generate coverage report
coverage:
	go test -v -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html
	@echo "Coverage report generated: coverage.html"

# show help
help:
	@echo ''
	@echo 'Usage:'
	@echo ' make [target]'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
	helpMessage = match(lastLine, /^# (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			helpMessage = substr(lastLine, RSTART + 2, RLENGTH); \
			printf "\033[36m%-22s\033[0m %s\n", helpCommand,helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

```

Replace `{service-name}` with the actual service name.

### 10.3 Create internal/conf/buf.yaml

```yaml
version: v2
modules:
  - path: internal/conf/
deps:
  - buf.build/envoyproxy/protoc-gen-validate
lint:
  use:
    - STANDARD
breaking:
  use:
    - FILE

```

### 10.4 Create internal/conf/buf.gen.yaml

```yaml
version: v2
managed:
  enabled: true

plugins:
  # Generate Go protobuf code for service configuration schema
  # Used to define strongly-typed config loaded from YAML at runtime
  - remote: buf.build/protocolbuffers/go
    out: internal/conf/gen
    opt: paths=source_relative
  # Generate validation code from protoc-gen-validate annotations
  - local: protoc-gen-validate
    out: internal/conf/gen
    opt: paths=source_relative,lang=go
inputs:
  - directory: internal/conf
```

Replace `{service-name}` with the actual service name.

### 10.5 Create .gitignore

```
# Binaries
bin/

# Wire generated
wire_gen.go

# Test coverage
coverage.out
coverage.html

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

### 10.6 Create README.md

```markdown
# {Service Name}

{Brief description of what this service does}

## Architecture

This service follows clean architecture with the following layers:

- **cmd/** - Application entry point and dependency injection (Wire)
- **internal/server/** - HTTP and gRPC server setup
- **internal/service/** - Service handlers (implements proto service interfaces)
- **internal/biz/** - Business logic and use cases
- **internal/data/** - Data access layer (repositories, database)
- **internal/conf/** - Configuration protobuf definitions

## Development

### Prerequisites

```bash
make init
```

### Generate Wire Code

```bash
make generate
```

### Build

```bash
make build
```

### Run

```bash
./bin/{service-name} -conf configs/config.yaml
```

### Test

```bash
make test
```

### Coverage

```bash
make coverage
```

## Configuration

Configuration is defined in `internal/conf/conf.proto` and loaded from `configs/config.yaml`.

### Server

- HTTP server on port 8000
- gRPC server on port 9000

### Metrics

Prometheus metrics exposed at `/metrics`:
- HTTP request metrics
- gRPC request metrics
- Go runtime metrics (if enabled)

## API

Proto definitions should be added to `api/service/{service-name}/v1/` in the monorepo root.

After defining protos:
1. Run `make contracts-generate` from monorepo root
2. Import generated code in service handlers
3. Register handlers in `internal/server/http.go` and `internal/server/grpc.go`

## Adding Features

### Add a new use case

1. Define repository interface in `internal/biz/interfaces.go`
2. Create use case in `internal/biz/my_usecase.go`
3. Add to `biz.ProviderSet`
4. Implement repository in `internal/data/repo/my_repo.go`
5. Add to `data.ProviderSet`
6. Inject into service layer

### Add database

1. Uncomment GORM in `internal/data/data.go`
2. Add models in `internal/data/model/`
3. Add repositories in `internal/data/repo/`
4. Update config to include database connection
```

Replace `{Service Name}` and `{service-name}` with the actual service name.

## Step 11: Generate Wire Code

Navigate to the cmd directory and generate Wire code:

```bash
cd services/{service-name}/cmd/{service-name}
GOWORK=off go generate
```

This will create `wire_gen.go` with the dependency injection graph.

## Step 12: Verify Build

Build the service to verify everything is wired correctly:

```bash
cd services/{service-name}
make build
```

If there are any import or compilation errors, fix them before proceeding.

## Step 13: Summary

Inform the user of what was created:

```
✓ Created new service: {service-name}
✓ Location: services/{service-name}/
✓ Structure: Clean architecture with server/service/biz/data layers
✓ Config: Complete config with Server, Data, Metrics
✓ Wire: Dependency injection configured and generated
✓ Metrics: HTTP and gRPC metrics enabled
✓ Build: Makefile with all standard targets

Next steps:
1. Define proto API in api/service/{service-name}/v1/
2. Run 'make contracts-generate' from monorepo root
3. Implement service handlers in internal/service/
4. Add business logic in internal/biz/
5. Implement repositories in internal/data/

The service is ready to build and run, but needs proto definitions to be useful.
```
</workflow>

<success_criteria>
Service skeleton is complete when:

- [ ] Service name validated (lowercase, alphanumeric, hyphens only)
- [ ] No conflicts with existing services
- [ ] Complete directory structure created
- [ ] All layer files created with correct imports
- [ ] Configuration files in place (conf.proto, config.yaml)
- [ ] Wire setup complete (wire.go and wire_gen.go generated)
- [ ] Metrics registry configured in server layer
- [ ] HTTP and gRPC servers have metrics middleware
- [ ] Makefile has all standard targets
- [ ] Service builds successfully with `make build`
- [ ] All placeholder `{service-name}` replaced with actual service name
- [ ] README.md provides clear next steps
- [ ] No event handlers, publishers, or subscribers included
- [ ] No proto definitions created (user adds separately)
</success_criteria>
