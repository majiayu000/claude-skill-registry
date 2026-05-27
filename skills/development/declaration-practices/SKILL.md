---
description: Reviews Go variable and constant declarations for proper scope, grouping, and zero value usage. Use when reviewing declaration blocks, creating new Go packages, or seeing ungrouped imports/vars.
---

# Declaration Practices

## Purpose

Establish patterns for variable and constant declarations in RMS Go code. Proper declarations improve readability and catch errors early.

## Core Principles

1. **Minimal scope** - Declare variables as close to use as possible
2. **Logical grouping** - Group related declarations together
3. **Zero value awareness** - Understand and leverage Go's zero values
4. **Type inference** - Use `:=` for local variables when type is obvious

---

## Import Organization

### Standard Grouping

Group imports in this order, separated by blank lines:

1. Standard library
2. External packages
3. Internal packages

```go
// DO: Organized imports
import (
    "context"
    "errors"
    "fmt"
    "time"
    
    "github.com/go-chi/chi/v5"
    "google.golang.org/grpc"
    
    "git.taservs.net/rms/taskcore/entity"
    "git.taservs.net/rms/zeke/clients"
)
```

```go
// DON'T: Mixed imports
import (
    "git.taservs.net/rms/taskcore/entity"
    "context"
    "github.com/go-chi/chi/v5"
    "fmt"
    "google.golang.org/grpc"
)
```

### Import Aliases

Use aliases sparingly, only when needed for clarity or conflicts.

```go
// DO: Alias for conflict resolution
import (
    "context"
    
    taskpb "git.taservs.net/rms/proto/task"
    userpb "git.taservs.net/rms/proto/user"
)

// DO: Alias for clarity (long package path)
import (
    rmscontext "git.taservs.net/rms/common/context"
)

// DON'T: Unnecessary aliases
import (
    ctx "context"  // Not needed
    e "errors"     // Not needed
)
```

---

## Variable Declaration

### Short Declaration (`:=`)

Use for local variables when the type is obvious.

```go
// DO: Short declaration for obvious types
ctx := context.Background()
err := doSomething()
tasks := make([]*Task, 0)
count := 0
name := "default"

// DON'T: Redundant type declaration
var ctx context.Context = context.Background()
var count int = 0
```

### Explicit Type Declaration (`var`)

Use when zero value is desired or type isn't obvious.

```go
// DO: var for zero value initialization
var (
    total   int64
    results []*Result
    err     error
)

// DO: var when type isn't obvious
var timeout time.Duration = 30 * time.Second
var handler http.Handler = &CustomHandler{}

// DO: var for package-level variables
var DefaultTimeout = 30 * time.Second
```

### Declaration Grouping

Group related declarations together.

```go
// DO: Group related variables
var (
    ErrNotFound     = errors.New("not found")
    ErrInvalidInput = errors.New("invalid input")
    ErrUnauthorized = errors.New("unauthorized")
)

const (
    DefaultTimeout    = 30 * time.Second
    DefaultMaxRetries = 3
    DefaultBatchSize  = 100
)

// DON'T: Scatter related declarations
var ErrNotFound = errors.New("not found")
const DefaultTimeout = 30 * time.Second
var ErrInvalidInput = errors.New("invalid input")
const DefaultMaxRetries = 3
```

---

## Constant Declaration

### Typed Constants

Use typed constants for type safety.

```go
// DO: Typed constants
type Status string

const (
    StatusPending    Status = "PENDING"
    StatusInProgress Status = "IN_PROGRESS"
    StatusComplete   Status = "COMPLETE"
)

type Priority int

const (
    PriorityLow    Priority = 1
    PriorityMedium Priority = 2
    PriorityHigh   Priority = 3
)
```

### Untyped Constants

Use untyped constants for values that should adapt to context.

```go
// DO: Untyped constants for flexibility
const (
    KB = 1024
    MB = KB * 1024
    GB = MB * 1024
)

// Can be used with any numeric type
var size32 int32 = 10 * MB
var size64 int64 = 10 * MB

// DO: Untyped string constants
const (
    Version   = "1.0.0"
    AppName   = "taskcore"
    UserAgent = AppName + "/" + Version
)
```

### Iota for Sequential Values

```go
// DO: iota for sequential constants
type Priority int

const (
    PriorityLow Priority = iota + 1
    PriorityMedium
    PriorityHigh
    PriorityCritical
)
// PriorityLow=1, PriorityMedium=2, PriorityHigh=3, PriorityCritical=4

// DO: iota for bit flags
type Permission int

const (
    PermRead Permission = 1 << iota
    PermWrite
    PermDelete
    PermAdmin
)
// PermRead=1, PermWrite=2, PermDelete=4, PermAdmin=8
```

---

## Zero Values

### Understanding Zero Values

| Type | Zero Value |
|------|------------|
| `bool` | `false` |
| Numeric | `0` |
| `string` | `""` |
| Pointer | `nil` |
| Slice | `nil` |
| Map | `nil` |
| Channel | `nil` |
| Interface | `nil` |
| Struct | All fields zero |

### Leveraging Zero Values

```go
// DO: Use zero values intentionally
type Task struct {
    ID       rms.ID
    Title    string
    Status   Status  // Zero value is ""
    Priority Priority // Zero value is 0
}

func NewTask(title string) *Task {
    return &Task{
        Title: title,
        // Status and Priority get zero values
    }
}

// DO: Check for zero value
func (t *Task) HasPriority() bool {
    return t.Priority != 0
}

// DO: Provide defaults when zero isn't appropriate
func (t *Task) EffectivePriority() Priority {
    if t.Priority == 0 {
        return PriorityMedium
    }
    return t.Priority
}
```

### Nil Slice vs Empty Slice

```go
// DO: Nil slice when "no data" is valid
func (s *Store) List(ctx context.Context) ([]*Task, error) {
    // Returns nil slice when empty
}

// DO: Empty slice for JSON serialization
func (s *Store) ListForAPI(ctx context.Context) ([]*Task, error) {
    tasks, err := s.List(ctx)
    if err != nil {
        return nil, err
    }
    if tasks == nil {
        return []*Task{}, nil  // Empty slice, serializes as []
    }
    return tasks, nil
}
```

---

## Scope Minimization

### Declare Close to Use

```go
// DO: Declare where first used
func process(ctx context.Context, items []Item) error {
    for _, item := range items {
        // result declared in loop scope
        result, err := transform(item)
        if err != nil {
            return err
        }
        
        if result.RequiresValidation {
            // validator only needed conditionally
            validator := NewValidator(item.Type)
            if err := validator.Validate(result); err != nil {
                return err
            }
        }
        
        if err := save(ctx, result); err != nil {
            return err
        }
    }
    return nil
}
```

```go
// DON'T: Declare all at top
func process(ctx context.Context, items []Item) error {
    var result *Result
    var validator *Validator
    var err error
    
    for _, item := range items {
        result, err = transform(item)
        // ...
    }
    return nil
}
```

### If with Initialization

```go
// DO: Limit scope with if-init
if err := validate(task); err != nil {
    return fmt.Errorf("validate: %w", err)
}

if task, err := store.Get(ctx, id); err != nil {
    return nil, err
} else if task == nil {
    return nil, ErrNotFound
}

// DO: Comma-ok idiom
if value, ok := cache.Get(key); ok {
    return value, nil
}

if task, ok := entity.(*Task); ok {
    return processTask(task)
}
```

---

## Package-Level Variables

### When to Use

Package-level variables should be:
- Constants or effectively constant (set once)
- Configuration loaded at startup
- Sentinel errors

```go
// DO: Package-level sentinel errors
var (
    ErrNotFound        = errors.New("not found")
    ErrAlreadyExists   = errors.New("already exists")
    ErrInvalidArgument = errors.New("invalid argument")
)

// DO: Package-level configuration
var (
    DefaultTimeout = 30 * time.Second
    MaxBatchSize   = 1000
)

// DON'T: Mutable state at package level
var currentUser *User  // Race condition risk
var taskCount int      // Race condition risk
```

### Initialization

```go
// DO: Initialize in init() if needed
var (
    logger     rms.Logger
    httpClient *http.Client
)

func init() {
    logger = rms.NewLogger("taskcore")
    httpClient = &http.Client{
        Timeout: DefaultTimeout,
    }
}

// BETTER: Initialize with function
var httpClient = newHTTPClient()

func newHTTPClient() *http.Client {
    return &http.Client{
        Timeout: DefaultTimeout,
    }
}
```

---

## Quick Reference

| Situation | Syntax |
|-----------|--------|
| Obvious type, local | `:=` |
| Zero value needed | `var x Type` |
| Explicit type needed | `var x Type = value` |
| Package-level | `var` block |
| Constants | `const` block |
| Typed enum | `type T int` + `const` |

### Declaration Checklist

- [ ] Imports grouped (std, external, internal)?
- [ ] Related vars/consts grouped together?
- [ ] Variables declared close to use?
- [ ] Zero values used intentionally?
- [ ] Package-level variables minimized?
- [ ] Types specified only when necessary?

---

## See Also

- [naming-convention](../naming-convention/Skill.md) - Variable naming
- [control-flow](../control-flow/Skill.md) - Scope reduction with if-init
- [code-structure](../code-structure/Skill.md) - Package organization
