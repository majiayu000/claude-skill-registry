---
description: Reviews Go interfaces and struct design for proper abstraction, embedding, and composition patterns. Use when designing APIs, reviewing interface definitions, or seeing type hierarchies.
---

# Struct and Interface Design

## Purpose

Establish patterns for interface and struct design in RMS Go code. Proper abstraction boundaries make code testable, maintainable, and flexible.

## Core Principles

1. **Accept interfaces, return structs** - Functions should accept abstract types and return concrete types
2. **Consumer-defined interfaces** - Define interfaces where they're used, not where they're implemented
3. **Small interfaces** - Prefer many small interfaces to few large ones
4. **Composition over inheritance** - Use embedding, not type hierarchies

---

## Accept Interfaces, Return Structs

### The Pattern

```go
// DO: Accept interface, return concrete type
func NewTaskService(store TaskStore) *TaskService {
    return &TaskService{store: store}
}

// Interface defined by consumer (this package)
type TaskStore interface {
    Get(ctx context.Context, id rms.ID) (*Task, error)
    Save(ctx context.Context, task *Task) error
}

// Concrete implementation (another package)
type SQLTaskStore struct {
    db *sql.DB
}

func (s *SQLTaskStore) Get(ctx context.Context, id rms.ID) (*Task, error) { ... }
func (s *SQLTaskStore) Save(ctx context.Context, task *Task) error { ... }
```

```go
// DON'T: Return interface
func NewTaskStore(db *sql.DB) TaskStore {  // Returns interface - harder to extend
    return &SQLTaskStore{db: db}
}
```

### Why This Matters

- **Testability**: Easy to mock dependencies via interfaces
- **Flexibility**: Callers define what they need
- **Type safety**: Concrete returns provide full access to methods

---

## Consumer-Defined Interfaces

### Define Where Used

```go
// DON'T: Define interface in implementation package
// package store
type TaskStore interface {
    Get(ctx context.Context, id rms.ID) (*Task, error)
    Save(ctx context.Context, task *Task) error
    Delete(ctx context.Context, id rms.ID) error
    List(ctx context.Context, filter Filter) ([]*Task, error)
    Count(ctx context.Context, filter Filter) (int64, error)
}

// Consumer must accept entire interface even if only using Get

// DO: Define interface in consumer package
// package service
type TaskGetter interface {
    Get(ctx context.Context, id rms.ID) (*Task, error)
}

type TaskService struct {
    getter TaskGetter  // Only needs Get
}

func (s *TaskService) Process(ctx context.Context, id rms.ID) error {
    task, err := s.getter.Get(ctx, id)
    // ...
}
```

### Interface Segregation

```go
// DO: Small, focused interfaces
type TaskReader interface {
    Get(ctx context.Context, id rms.ID) (*Task, error)
    List(ctx context.Context, filter Filter) ([]*Task, error)
}

type TaskWriter interface {
    Save(ctx context.Context, task *Task) error
    Delete(ctx context.Context, id rms.ID) error
}

// Consumers declare exactly what they need
type ReadOnlyService struct {
    store TaskReader  // Only read operations
}

type FullService struct {
    reader TaskReader
    writer TaskWriter
}

// Or combine when needed
type TaskStore interface {
    TaskReader
    TaskWriter
}
```

---

## Interface Design

### Single-Method Interfaces

Prefer small interfaces, especially single-method ones.

```go
// DO: Single-method interfaces
type Validator interface {
    Validate() error
}

type Processor interface {
    Process(ctx context.Context) error
}

type Publisher interface {
    Publish(ctx context.Context, event Event) error
}

// Any type can satisfy Validator
func (t *Task) Validate() error { ... }
func (p CreateTaskParams) Validate() error { ... }
func (u TaskUpdates) Validate() error { ... }
```

### Interface Naming

```go
// Single-method: -er suffix
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
type Validator interface { Validate() error }
type Processor interface { Process(ctx context.Context) error }

// Multi-method: descriptive noun
type TaskStore interface {
    Get(ctx context.Context, id rms.ID) (*Task, error)
    Save(ctx context.Context, task *Task) error
}

// Composed interfaces: combine names or describe role
type ReadWriter interface {
    Reader
    Writer
}

type TaskRepository interface {
    TaskReader
    TaskWriter
}
```

### Empty Interface

Avoid `interface{}` (or `any`). Use typed alternatives.

```go
// DON'T: Empty interface loses type safety
func Process(data interface{}) error
func Store(key string, value any)

// DO: Use generics (Go 1.18+)
func Process[T any](data T) error
func Store[T any](key string, value T)

// DO: Use specific types or small interfaces
func ProcessTask(task *Task) error
func ProcessEntity(entity Entity) error  // Entity is a defined interface
```

---

## Struct Design

### Field Organization

```go
// DO: Logical field grouping
type Task struct {
    // Identity
    ID         rms.ID
    WorkflowID rms.ID
    
    // Core data
    Title       string
    Description string
    Status      Status
    Priority    Priority
    
    // Relationships
    ActorID    rms.ID
    AssigneeID rms.ID
    
    // Metadata
    Metadata map[string]any
    Tags     []string
    
    // Timestamps
    CreatedAt time.Time
    UpdatedAt time.Time
    DueDate   *time.Time
}
```

### Exported vs Unexported Fields

```go
// DO: Unexported fields with methods for controlled access
type Task struct {
    id          rms.ID     // unexported
    title       string     // unexported
    status      Status     // unexported
    createdAt   time.Time  // unexported
}

func (t *Task) ID() rms.ID       { return t.id }
func (t *Task) Title() string    { return t.title }
func (t *Task) Status() Status   { return t.status }
func (t *Task) SetTitle(s string) { t.title = s }

// DO: Exported fields for DTOs/params (data transfer)
type CreateTaskParams struct {
    Title       string  // exported for JSON/validation
    Description string
    WorkflowID  rms.ID
    ActorID     rms.ID
}
```

---

## Struct Embedding

### Composition Over Inheritance

```go
// DO: Embed for composition
type Task struct {
    ID       rms.ID
    Title    string
    Metadata // Embedded for metadata behavior
}

type Metadata struct {
    CreatedAt time.Time
    UpdatedAt time.Time
    CreatedBy rms.ID
    UpdatedBy rms.ID
}

// Task now has CreatedAt, UpdatedAt methods
task := &Task{}
task.CreatedAt = time.Now()  // Directly accessible
```

### Embedding Interfaces

```go
// DO: Embed interface for delegation
type CachingStore struct {
    TaskStore  // Embed interface
    cache      *Cache
}

func (s *CachingStore) Get(ctx context.Context, id rms.ID) (*Task, error) {
    // Check cache first
    if task, ok := s.cache.Get(id); ok {
        return task, nil
    }
    
    // Delegate to embedded store
    task, err := s.TaskStore.Get(ctx, id)
    if err != nil {
        return nil, err
    }
    
    s.cache.Set(id, task)
    return task, nil
}
```

### Avoid Deep Embedding

```go
// DON'T: Deep embedding is confusing
type Task struct {
    Entity
}

type Entity struct {
    Resource
}

type Resource struct {
    Metadata
}

// task.CreatedAt - hard to know where this comes from

// DO: Flat composition with clear field names
type Task struct {
    ID       rms.ID
    Title    string
    Entity   EntityInfo
    Metadata MetadataInfo
}

task.Metadata.CreatedAt  // Clear origin
```

---

## Type Aliases vs Type Definitions

### Type Definition (Preferred)

Creates a new, distinct type.

```go
// DO: Type definition for domain types
type TaskID string
type Priority int
type Status string

func (id TaskID) String() string { return string(id) }
func (p Priority) IsHigh() bool { return p >= 3 }

// These are different types - type safety!
var taskID TaskID = "task-123"
var otherID string = "other"
// taskID = otherID  // Compile error!
```

### Type Alias

Same type, just another name. Use sparingly.

```go
// Type alias - same underlying type
type ID = string  // ID and string are interchangeable

var id ID = "123"
var s string = id  // OK - same type

// DO: Use aliases for gradual refactoring
// Old code uses TaskID, new code uses rms.ID
type TaskID = rms.ID
```

---

## Nil Handling

### Nil Receiver Safety

```go
// DO: Handle nil receiver gracefully
func (t *Task) ID() rms.ID {
    if t == nil {
        return ""
    }
    return t.id
}

func (t *Task) IsComplete() bool {
    if t == nil {
        return false
    }
    return t.status == StatusComplete
}

// Safe to call on nil
var task *Task
fmt.Println(task.ID())         // Returns ""
fmt.Println(task.IsComplete()) // Returns false
```

### Nil Checks in Methods

```go
// DO: Check embedded/pointer fields
func (t *Task) MetadataValue(key string) any {
    if t == nil || t.Metadata == nil {
        return nil
    }
    return t.Metadata[key]
}
```

---

## Interface Satisfaction

### Compile-Time Verification

```go
// DO: Verify interface satisfaction at compile time
var _ TaskStore = (*SQLTaskStore)(nil)
var _ TaskStore = (*CachingStore)(nil)
var _ io.Reader = (*CustomReader)(nil)

// This fails at compile time if SQLTaskStore doesn't implement TaskStore
```

### Partial Interface Implementation

```go
// Embed to get partial implementation
type PartialStore struct {
    TaskStore  // Embed full interface
}

// Override only what you need
func (s *PartialStore) Get(ctx context.Context, id rms.ID) (*Task, error) {
    // Custom implementation
}

// Save, Delete, etc. delegate to embedded TaskStore
```

---

## Quick Reference

| Pattern | When to Use |
|---------|-------------|
| Accept interface | Function parameters |
| Return struct | Function return types |
| Consumer-defined | Interface location |
| Single-method | Most interfaces |
| Embedding | Composition, delegation |
| Type definition | New domain types |
| Type alias | Gradual refactoring |

### Interface Checklist

- [ ] Defined where used, not implemented?
- [ ] As small as possible?
- [ ] Named with -er suffix (if single method)?
- [ ] Satisfied by concrete types?

### Struct Checklist

- [ ] Fields logically grouped?
- [ ] Unexported fields with accessor methods?
- [ ] Embedding used appropriately?
- [ ] Nil-safe methods?

---

## See Also

- [EXAMPLES.md](./EXAMPLES.md) - Extended struct/interface examples
- [naming-convention](../naming-convention/Skill.md) - Naming patterns
- [functional-options](../functional-options/Skill.md) - Constructor patterns
