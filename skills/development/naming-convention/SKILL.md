---
description: Enforces RMS Go naming conventions for variables, functions, interfaces, structs, and packages. Use when reviewing Go code for naming issues, creating new Go files, or encountering confusing identifier names.
---

# Naming Convention

## Purpose

Establish consistent naming across RMS Go codebases. Good names are critical for readability and maintenance.

## Core Principle

**Use MixedCaps or mixedCaps, never underscores.**

Go uses capitalization for export control:
- `ExportedName` - visible outside package
- `unexportedName` - package-private

---

## Variables

### Local Variables

Prefer short names for local variables with limited scope.

```go
// DO: Short names for narrow scope
for i, task := range tasks {
    process(task)
}

// DO: Descriptive when scope is larger
taskProcessor := NewTaskProcessor(cfg)
```

```go
// DON'T: Verbose names for tiny scope
for taskIndex, currentTask := range tasks {
    process(currentTask)
}
```

### Common Short Names

| Name | Usage |
|------|-------|
| `i`, `j`, `k` | Loop indices |
| `n` | Count or length |
| `v` | Value in range |
| `k` | Key in map iteration |
| `ctx` | Context |
| `err` | Error |
| `ok` | Boolean from comma-ok idiom |
| `t` | Testing.T |
| `b` | Testing.B (benchmarks) |

### Package-Level Variables

Use descriptive names for package-level variables.

```go
// DO: Descriptive package-level names
var (
    DefaultTimeout    = 30 * time.Second
    MaxRetryAttempts  = 3
)

// DON'T: Cryptic package-level names
var (
    defTo  = 30 * time.Second
    maxRet = 3
)
```

---

## Functions and Methods

### Function Naming

Functions should describe what they do, not how.

```go
// DO: Action-oriented names
func CreateTask(params CreateTaskParams) (*Task, error)
func ValidateMetadata(meta Metadata) error
func ParseTaskID(s string) (rms.ID, error)

// DON'T: Implementation details in name
func CreateTaskWithDatabaseInsert(params CreateTaskParams) (*Task, error)
func ValidateMetadataUsingRegex(meta Metadata) error
```

### Getters

Omit "Get" prefix for simple getters.

```go
// DO: No "Get" prefix
func (t *Task) ID() rms.ID
func (t *Task) Status() Status
func (t *Task) Priority() Priority

// DON'T: Redundant "Get" prefix
func (t *Task) GetID() rms.ID
func (t *Task) GetStatus() Status
```

**Exception**: Keep "Get" when it clarifies intent:
```go
// OK: "Get" clarifies fetching from external source
func (c *Client) GetUser(ctx context.Context, id rms.ID) (*User, error)
```

### Setters

Use "Set" prefix for setters.

```go
// DO: "Set" prefix for setters
func (t *Task) SetStatus(s Status)
func (t *Task) SetPriority(p Priority)
```

### Boolean Functions

Use `is`, `has`, `can`, `should` for boolean-returning functions.

```go
// DO: Boolean prefixes
func (t *Task) IsComplete() bool
func (t *Task) HasAssignee() bool
func (u *User) CanEdit(task *Task) bool

// DON'T: Ambiguous names
func (t *Task) Complete() bool  // Is this a getter or action?
func (t *Task) Assignee() bool  // Unclear return type
```

---

## Method Receivers

### Naming

Use short (1-2 letter) names derived from the type.

```go
// DO: Short, consistent receiver names
func (t *Task) Validate() error
func (t *Task) AddAction(a Action) error
func (t *Task) Complete() error

// DON'T: Verbose receiver names
func (task *Task) Validate() error
func (this *Task) AddAction(a Action) error
func (self *Task) Complete() error
```

### Consistency

Use the same receiver name across all methods of a type.

```go
// DO: Consistent receiver name
func (t *Task) ID() rms.ID { return t.id }
func (t *Task) Status() Status { return t.status }
func (t *Task) Priority() Priority { return t.priority }

// DON'T: Inconsistent receivers
func (t *Task) ID() rms.ID { return t.id }
func (task *Task) Status() Status { return task.status }
func (ts *Task) Priority() Priority { return ts.priority }
```

---

## Interfaces

### Single-Method Interfaces

Use `-er` suffix for single-method interfaces.

```go
// DO: -er suffix
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
type Validator interface { Validate() error }
type Processor interface { Process(ctx context.Context) error }

// DON'T: Noun names for single-method interfaces
type Validation interface { Validate() error }
type Processing interface { Process(ctx context.Context) error }
```

### Multi-Method Interfaces

Use descriptive nouns for multi-method interfaces.

```go
// DO: Descriptive noun for multi-method interface
type TaskStore interface {
    Get(ctx context.Context, id rms.ID) (*Task, error)
    Save(ctx context.Context, task *Task) error
    Delete(ctx context.Context, id rms.ID) error
}

type MetadataProcessor interface {
    Validate(meta Metadata) error
    Transform(meta Metadata) (Metadata, error)
    Normalize(meta Metadata) Metadata
}
```

---

## Structs

### Naming

Use descriptive nouns for structs.

```go
// DO: Descriptive nouns
type Task struct { ... }
type CreateTaskParams struct { ... }
type TaskFactory struct { ... }
type MetadataProcessor struct { ... }

// DON'T: Verb-like names
type CreateTask struct { ... }
type ProcessMetadata struct { ... }
```

### Field Names

Use MixedCaps, be descriptive.

```go
// DO: Clear field names
type Task struct {
    ID          rms.ID
    Title       string
    Description string
    Status      Status
    Priority    Priority
    CreatedAt   time.Time
    UpdatedAt   time.Time
}

// DON'T: Abbreviated or unclear names
type Task struct {
    Id    rms.ID  // Should be ID (initialism)
    Ttl   string  // What is this?
    Desc  string  // Abbreviation
    Stat  Status  // Abbreviation
}
```

---

## Packages

### Package Naming Rules

1. **Lowercase only** - no underscores, no MixedCaps
2. **Short and concise** - prefer single word
3. **Singular, not plural** - `entity` not `entities`
4. **No generic names** - avoid `util`, `common`, `helper`, `misc`

```go
// DO: Good package names
package task
package metadata
package factory
package converter

// DON'T: Poor package names
package taskUtils       // No MixedCaps
package task_helpers    // No underscores
package entities        // Not plural
package common          // Too generic
```

### Package Name vs Directory

Package name should match directory name.

```
// DO
task/
└── task.go  // package task

// DON'T
tasks/
└── task.go  // package task (mismatch)
```

### Avoid Stutter

Don't repeat package name in exported identifiers.

```go
package task

// DO: No stutter
type Factory struct { ... }
func NewFactory() *Factory

// DON'T: Stutter (task.TaskFactory)
type TaskFactory struct { ... }
func NewTaskFactory() *TaskFactory
```

---

## Initialisms and Acronyms

### Rules

1. All letters in an initialism should be the same case
2. Common initialisms: `ID`, `HTTP`, `URL`, `API`, `JSON`, `XML`, `SQL`, `RPC`, `UUID`

```go
// DO: Consistent case for initialisms
type UserID string
type HTTPClient struct { ... }
type JSONAPI struct { ... }
func ParseURL(s string) (*URL, error)
func (c *Client) GetUserByID(id rms.ID) (*User, error)

// DON'T: Mixed case in initialisms
type UserId string        // Should be UserID
type HttpClient struct {}  // Should be HTTPClient
type JsonApi struct {}     // Should be JSONAPI
func ParseUrl(s string)    // Should be ParseURL
```

### Unexported Initialisms

When unexported, keep initialism lowercase at start.

```go
// DO: Lowercase initialism when unexported
var userID rms.ID
var httpClient *http.Client
func parseURL(s string) (*url.URL, error)

// DON'T: Uppercase start for unexported
var userID rms.ID  // This is correct
var userId rms.ID  // Wrong - should be userID
```

---

## Constants

### Naming

Use MixedCaps for constants. Don't use ALL_CAPS.

```go
// DO: MixedCaps constants
const MaxRetryAttempts = 3
const DefaultTimeout = 30 * time.Second
const StatusPending = "pending"

// DON'T: ALL_CAPS (not idiomatic Go)
const MAX_RETRY_ATTEMPTS = 3
const DEFAULT_TIMEOUT = 30 * time.Second
```

### Grouped Constants

Group related constants with a type.

```go
// DO: Typed constants
type Status string

const (
    StatusPending    Status = "pending"
    StatusInProgress Status = "in_progress"
    StatusComplete   Status = "complete"
)
```

---

## Quick Reference

| Element | Convention | Example |
|---------|------------|---------|
| Local variable | Short, contextual | `i`, `ctx`, `err`, `t` |
| Package variable | Descriptive | `DefaultTimeout` |
| Function | Action verb | `CreateTask`, `Validate` |
| Getter | No "Get" prefix | `func (t *Task) ID()` |
| Setter | "Set" prefix | `func (t *Task) SetStatus()` |
| Boolean func | is/has/can/should | `IsComplete()`, `HasAssignee()` |
| Receiver | 1-2 letters | `func (t *Task)` |
| Interface (1 method) | -er suffix | `Validator`, `Processor` |
| Interface (multi) | Descriptive noun | `TaskStore` |
| Struct | Noun | `Task`, `CreateTaskParams` |
| Package | Lowercase, singular | `task`, `metadata` |
| Initialism | All same case | `ID`, `HTTP`, `URL` |
| Constant | MixedCaps | `MaxRetryAttempts` |

---

## See Also

- [EXAMPLES.md](./EXAMPLES.md) - Extended naming examples
- [code-structure](../code-structure/Skill.md) - Package organization
- [declaration-practices](../declaration-practices/Skill.md) - Variable declarations
