---
description: Reviews Go function signatures for parameter ordering, return value conventions, and receiver patterns. Use when reviewing function signatures, designing APIs, or seeing complex parameter lists.
---

# Functions and Methods

## Purpose

Establish consistent patterns for function and method signatures in RMS Go code. Well-designed function signatures make APIs intuitive and maintainable.

## Core Principles

1. **Context first** - `ctx context.Context` is always the first parameter
2. **Error last** - `error` is always the last return value
3. **Limit parameters** - Use parameter structs for 4+ arguments
4. **Consistent receivers** - Same name across all methods of a type

---

## Parameter Ordering

### Standard Order

```
func Name(ctx context.Context, id rms.ID, options ...Option) (*Result, error)
         ^                     ^          ^                    ^       ^
         |                     |          |                    |       |
         1. Context            2. IDs     3. Variadic opts     4. Data 5. Error
```

### Context Always First

```go
// DO: Context first
func (s *Service) GetTask(ctx context.Context, id rms.ID) (*Task, error)
func (s *Service) CreateTask(ctx context.Context, params CreateTaskParams) (*Task, error)
func (s *Service) List(ctx context.Context, filter TaskFilter) ([]*Task, error)

// DON'T: Context not first
func (s *Service) GetTask(id rms.ID, ctx context.Context) (*Task, error)
func CreateTask(params CreateTaskParams, ctx context.Context) (*Task, error)
```

### IDs Before Data Structures

```go
// DO: IDs before larger structures
func (s *Service) Update(ctx context.Context, id rms.ID, updates TaskUpdates) error
func (s *Service) AssignTask(ctx context.Context, taskID, assigneeID rms.ID) error

// DON'T: Data structures before IDs
func (s *Service) Update(ctx context.Context, updates TaskUpdates, id rms.ID) error
```

### Error Always Last

```go
// DO: Error last in return values
func (s *Service) Get(ctx context.Context, id rms.ID) (*Task, error)
func (s *Service) List(ctx context.Context) ([]*Task, int64, error)

// DON'T: Error not last
func (s *Service) Get(ctx context.Context, id rms.ID) (error, *Task)
```

---

## Return Values

### Named Return Values

Use named returns sparingly - primarily for documentation or defer usage.

```go
// DO: Named returns for complex functions with multiple returns
func (p *Parser) Parse(input string) (result *AST, remaining string, err error) {
    // Named returns document what each value represents
}

// DO: Named returns when defer needs to modify them
func (s *Service) ProcessWithCleanup(ctx context.Context) (err error) {
    lock := s.acquireLock()
    defer func() {
        if unlockErr := lock.Unlock(); unlockErr != nil {
            if err == nil {
                err = unlockErr
            }
        }
    }()
    // ...
}

// DON'T: Named returns for simple functions
func (t *Task) ID() (id rms.ID) {  // Unnecessary
    return t.id
}

// DO: Simple functions without named returns
func (t *Task) ID() rms.ID {
    return t.id
}
```

### Naked Returns

Avoid naked returns - they reduce clarity.

```go
// DON'T: Naked returns
func calculate(a, b int) (result int, err error) {
    result = a + b
    return  // What are we returning?
}

// DO: Explicit returns
func calculate(a, b int) (result int, err error) {
    result = a + b
    return result, nil
}

// Or without named returns
func calculate(a, b int) (int, error) {
    result := a + b
    return result, nil
}
```

### Returning Zero Values

Return explicit zero values when appropriate.

```go
// DO: Return nil explicitly for pointers
func (s *Store) Get(ctx context.Context, id rms.ID) (*Task, error) {
    if !exists {
        return nil, ErrNotFound
    }
    return task, nil
}

// DO: Return empty slice, not nil, when list has no results
func (s *Store) List(ctx context.Context) ([]*Task, error) {
    tasks := make([]*Task, 0)  // Empty slice, not nil
    // ...
    return tasks, nil
}
```

---

## Parameter Structs

### When to Use

Use parameter structs when:
- Function has 4+ parameters
- Parameters are logically grouped
- Function signature changes frequently
- Optional parameters exist

```go
// DON'T: Too many parameters
func CreateTask(
    ctx context.Context,
    title string,
    description string,
    workflowID rms.ID,
    actorID rms.ID,
    priority Priority,
    dueDate time.Time,
    metadata map[string]any,
) (*Task, error)

// DO: Parameter struct
type CreateTaskParams struct {
    Title       string
    Description string
    WorkflowID  rms.ID
    ActorID     rms.ID
    Priority    Priority
    DueDate     time.Time
    Metadata    map[string]any
}

func CreateTask(ctx context.Context, params CreateTaskParams) (*Task, error)
```

### Parameter Struct Design

```go
// DO: Validate in struct method
type CreateTaskParams struct {
    Title       string         `json:"title"`
    Description string         `json:"description,omitempty"`
    WorkflowID  rms.ID         `json:"workflowId"`
    ActorID     rms.ID         `json:"actorId"`
    Priority    Priority       `json:"priority,omitempty"`
    DueDate     *time.Time     `json:"dueDate,omitempty"`
    Metadata    map[string]any `json:"metadata,omitempty"`
}

func (p CreateTaskParams) Validate() error {
    if p.Title == "" {
        return errors.New("title is required")
    }
    if p.WorkflowID == "" {
        return errors.New("workflow ID is required")
    }
    if p.ActorID == "" {
        return errors.New("actor ID is required")
    }
    return nil
}

// Usage
func (s *Service) CreateTask(ctx context.Context, params CreateTaskParams) (*Task, error) {
    if err := params.Validate(); err != nil {
        return nil, fmt.Errorf("validate params: %w", err)
    }
    // ...
}
```

---

## Method Receivers

### Pointer vs Value Receivers

Use pointer receivers when:
- Method modifies the receiver
- Receiver is large (struct with many fields)
- Consistency - if any method needs pointer, use pointer for all

```go
// DO: Pointer receiver for mutation
func (t *Task) SetStatus(s Status) {
    t.status = s
    t.updatedAt = time.Now()
}

// DO: Pointer receiver for large structs
func (t *Task) Clone() *Task {
    return &Task{
        ID:          t.ID,
        Title:       t.Title,
        Description: t.Description,
        // ...
    }
}

// DO: Value receiver for immutable access on small types
func (s Status) String() string {
    return string(s)
}

func (p Priority) IsHigh() bool {
    return p >= PriorityHigh
}
```

### Receiver Naming

Use short (1-2 letter) names, consistent across all methods.

```go
// DO: Short, consistent receiver names
func (t *Task) ID() rms.ID           { return t.id }
func (t *Task) Status() Status       { return t.status }
func (t *Task) SetStatus(s Status)   { t.status = s }
func (t *Task) Validate() error      { /* ... */ }
func (t *Task) AddAction(a Action)   { /* ... */ }

// DON'T: Long or inconsistent names
func (task *Task) ID() rms.ID
func (this *Task) Status() Status
func (t *Task) SetStatus(s Status)
func (tsk *Task) Validate() error
```

### Avoid Self/This

```go
// DON'T: self/this are not idiomatic Go
func (self *Task) Validate() error
func (this *Task) Clone() *Task

// DO: Short type-derived name
func (t *Task) Validate() error
func (t *Task) Clone() *Task
```

---

## Variadic Functions

### Use for Optional Parameters

```go
// DO: Variadic for options
func NewTaskFactory(opts ...TaskFactoryOption) *TaskFactory {
    f := &TaskFactory{
        priority: PriorityMedium,
        status:   StatusPending,
    }
    for _, opt := range opts {
        opt(f)
    }
    return f
}

// Usage
factory := NewTaskFactory(
    WithDefaultPriority(PriorityHigh),
    WithValidator(validator),
)
```

### Variadic for Homogeneous Lists

```go
// DO: Variadic for multiple items of same type
func (t *Task) AddTags(tags ...string) {
    t.tags = append(t.tags, tags...)
}

func JoinErrors(errs ...error) error {
    return errors.Join(errs...)
}

// Usage
task.AddTags("urgent", "review-needed", "q4")
```

---

## Constructor Functions

### NewX Pattern

```go
// DO: NewX constructor
func NewTaskService(store TaskStore, opts ...ServiceOption) *TaskService {
    s := &TaskService{
        store:   store,
        logger:  defaultLogger,
        timeout: defaultTimeout,
    }
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// DO: NewX with required dependencies
func NewTaskFactory(validator Validator) *TaskFactory {
    return &TaskFactory{
        validator: validator,
        priority:  PriorityMedium,
    }
}
```

### Must Pattern for Initialization

```go
// DO: Must prefix for panic-on-error constructors
func MustNewClient(addr string) *Client {
    client, err := NewClient(addr)
    if err != nil {
        panic(fmt.Sprintf("create client: %v", err))
    }
    return client
}

// Usage in init or main
var client = MustNewClient(os.Getenv("SERVER_ADDR"))

// DON'T: Use Must in regular business logic
func process() {
    client := MustNewClient(addr)  // Dangerous! Will panic on error
}
```

---

## Function Length

### Keep Functions Focused

Functions should do one thing well.

```go
// DON'T: Function doing too much
func (s *Service) ProcessTask(ctx context.Context, id rms.ID) error {
    // Fetch task (10 lines)
    // Validate task (15 lines)
    // Transform data (20 lines)
    // Save to database (10 lines)
    // Publish event (10 lines)
    // Send notification (15 lines)
    return nil
}

// DO: Extract into focused functions
func (s *Service) ProcessTask(ctx context.Context, id rms.ID) error {
    task, err := s.fetchTask(ctx, id)
    if err != nil {
        return fmt.Errorf("fetch task: %w", err)
    }
    
    if err := s.validateTask(task); err != nil {
        return fmt.Errorf("validate: %w", err)
    }
    
    transformed := s.transformTask(task)
    
    if err := s.saveTask(ctx, transformed); err != nil {
        return fmt.Errorf("save: %w", err)
    }
    
    if err := s.publishEvent(ctx, transformed); err != nil {
        return fmt.Errorf("publish: %w", err)
    }
    
    return nil
}
```

---

## Quick Reference

| Pattern | Convention |
|---------|------------|
| Context parameter | Always first |
| Error return | Always last |
| ID parameters | Before data structures |
| 4+ parameters | Use parameter struct |
| Receiver name | 1-2 letters, consistent |
| Pointer receiver | For mutation or large structs |
| Value receiver | For small, immutable types |
| Constructor | `NewX` pattern |
| Panic constructor | `MustNewX` pattern |

### Function Checklist

- [ ] Context is first parameter?
- [ ] Error is last return value?
- [ ] Parameters under 4, or using struct?
- [ ] Receiver name is short and consistent?
- [ ] Named returns only where needed?
- [ ] No naked returns?

---

## See Also

- [EXAMPLES.md](./EXAMPLES.md) - Extended function examples
- [naming-convention](../naming-convention/Skill.md) - Function naming
- [functional-options](../functional-options/Skill.md) - Option patterns
- [struct-interface](../struct-interface/Skill.md) - Struct design
