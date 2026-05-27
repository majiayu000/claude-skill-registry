---
description: Reviews Go package structure, file organization, and internal package usage. Use when creating new packages, reviewing project layout, or seeing import cycle issues.
---

# Code Structure

## Purpose

Establish patterns for organizing Go code into packages and files. Good structure makes codebases navigable, prevents import cycles, and clarifies API boundaries.

## Core Principles

1. **Package per responsibility** - Each package has a clear purpose
2. **Flat when possible** - Avoid deep nesting without reason
3. **Internal for private** - Use `internal/` for implementation details
4. **Comments for documentation** - Package and exported symbol docs

---

## Package Organization

### Package Purpose

Each package should have a single, clear responsibility.

```
// DO: Clear responsibilities
taskcore/
├── entity/       # Domain entities (Task, Action, Assignment)
├── factory/      # Task creation logic
├── metadata/     # Metadata processing pipeline
├── converter/    # Proto/graph format conversion
└── constants/    # Type-safe enums and constants

// DON'T: Vague or grab-bag packages
taskcore/
├── util/         # What utilities?
├── common/       # Common to what?
├── helper/       # Helps with what?
└── misc/         # Miscellaneous what?
```

### Package Naming

```go
// DO: Lowercase, singular, descriptive
package task
package metadata
package converter
package factory

// DON'T: Plural, generic, or with underscores
package tasks          // Plural
package task_service   // Underscore
package util           // Generic
package common         // Vague
```

### Avoid Package Stutter

```go
// DON'T: Package name repeated in exported names
package task

type TaskService struct {}     // task.TaskService stutters
func NewTaskService() {}       // task.NewTaskService stutters

// DO: Clean names
package task

type Service struct {}         // task.Service is clean
func NewService() *Service {}  // task.NewService is clean
```

---

## Internal Packages

### Purpose

The `internal/` directory restricts imports to parent directories only.

```
project/
├── internal/           # Only importable within project/
│   ├── cache/
│   └── metrics/
├── pkg/                # Public packages
│   └── client/
└── service/
    └── task/
```

### When to Use Internal

```go
// DO: Use internal for implementation details
internal/
├── cache/        # Internal caching implementation
├── retry/        # Internal retry logic
└── validate/     # Internal validation helpers

// These can be imported by project/ packages
// but NOT by external consumers

// DON'T: Put public API in internal
internal/
└── api/          # APIs should be public for consumers
```

---

## File Organization

### File Naming

```
package_name/
├── doc.go           # Package documentation
├── types.go         # Type definitions
├── interface.go     # Interface definitions (if many)
├── service.go       # Main implementation
├── service_test.go  # Tests for service.go
├── options.go       # Functional options
└── errors.go        # Error definitions
```

### File Size Guidelines

- **Target**: 200-500 lines per file
- **Split when**: File exceeds 500 lines or has multiple responsibilities
- **Don't split**: Small packages (under 200 lines) can be single file

### Single Type Files

For complex types, consider dedicated files:

```
entity/
├── task.go           # Task type and methods
├── task_test.go
├── action.go         # Action type and methods
├── action_test.go
├── assignment.go     # Assignment type and methods
└── assignment_test.go
```

---

## Import Organization

### Standard Grouping

```go
import (
    // Standard library
    "context"
    "errors"
    "fmt"
    "time"
    
    // External packages
    "github.com/go-chi/chi/v5"
    "google.golang.org/grpc"
    
    // Internal packages
    "git.taservs.net/rms/taskcore/entity"
    "git.taservs.net/rms/taskcore/factory"
)
```

### Import Aliases

```go
// DO: Alias only when necessary
import (
    taskpb "git.taservs.net/rms/proto/task"       // Conflict resolution
    userpb "git.taservs.net/rms/proto/user"       // Conflict resolution
)

// DON'T: Unnecessary aliases
import (
    ctx "context"   // Not needed
    e "errors"      // Not needed
)
```

### Avoid Import Cycles

```go
// DON'T: Circular imports
// package a imports package b
// package b imports package a

// DO: Extract shared types to third package
// package a imports package types
// package b imports package types
```

---

## Comments and Documentation

### Package Documentation

```go
// Package task provides task management functionality for RMS.
//
// Tasks represent units of work that can be assigned, tracked, and completed.
// This package contains the core task entity, factory, and related types.
//
// Basic usage:
//
//     factory := task.NewFactory()
//     t, err := factory.Create(task.CreateParams{
//         Title:      "Review document",
//         WorkflowID: workflowID,
//     })
package task
```

### Exported Symbol Documentation

```go
// Task represents a unit of work in the RMS system.
// Tasks are created through the Factory and can be assigned to users.
type Task struct {
    // ID uniquely identifies this task.
    ID rms.ID
    
    // Title is a short description of the task.
    Title string
    
    // Status indicates the current state of the task.
    Status Status
}

// NewFactory creates a TaskFactory with the given options.
// The factory is used to create new tasks with consistent defaults.
func NewFactory(opts ...Option) *Factory {
    // ...
}

// Create creates a new task with the given parameters.
// Returns an error if validation fails.
func (f *Factory) Create(params CreateParams) (*Task, error) {
    // ...
}
```

### Comment Guidelines

```go
// DO: Explain why, not what
// processLegacy handles old-format metadata that hasn't been migrated.
// This can be removed after migration is complete (Q4 2024).
func processLegacy(meta map[string]any) {
    // ...
}

// DO: Document non-obvious behavior
// Get returns the task with the given ID.
// Returns ErrNotFound if no task exists with that ID.
func (s *Store) Get(ctx context.Context, id rms.ID) (*Task, error) {
    // ...
}

// DON'T: State the obvious
// GetID returns the task's ID.
func (t *Task) GetID() rms.ID {
    return t.ID
}
```

---

## Project Layout

### Standard Layout for Services

```
service/
├── cmd/
│   └── service/
│       └── main.go         # Entry point
├── internal/
│   ├── handler/           # HTTP/gRPC handlers
│   ├── service/           # Business logic
│   └── store/             # Data access
├── pkg/
│   └── client/            # Public client library
├── api/
│   └── proto/             # Protocol buffers
├── scripts/               # Build/deploy scripts
├── docker/
│   └── Dockerfile
├── go.mod
├── go.sum
└── README.md
```

### Standard Layout for Libraries

```
library/
├── entity/               # Domain entities
├── factory/              # Creation patterns
├── converter/            # Format conversion
├── internal/             # Private implementation
│   └── validate/
├── go.mod
├── go.sum
└── README.md
```

---

## Quick Reference

| Element | Convention |
|---------|------------|
| Package name | Lowercase, singular |
| File name | Lowercase, snake_case.go |
| Test file | *_test.go |
| Internal | Use internal/ for private packages |
| Documentation | Package doc in doc.go |
| Imports | Grouped: std, external, internal |

### Structure Checklist

- [ ] Each package has clear responsibility?
- [ ] No package stuttering?
- [ ] Internal packages for implementation details?
- [ ] Files under 500 lines?
- [ ] Imports properly grouped?
- [ ] Package documentation present?

---

## See Also

- [LAYOUT.md](./LAYOUT.md) - Reference package layouts
- [naming-convention](../naming-convention/Skill.md) - Package naming
- [declaration-practices](../declaration-practices/Skill.md) - Import organization
