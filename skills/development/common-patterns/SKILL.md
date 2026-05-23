---
description: Reviews common RMS Go patterns including caching, retry logic, enums, and unmarshalling. Use when implementing utility patterns, seeing repeated boilerplate, or reviewing pattern usage.
---

# Common Patterns

## Purpose

Document frequently used patterns in RMS Go code. These patterns solve common problems and should be applied consistently.

---

## Enum Pattern

### Type-Safe Enums

```go
// DO: Typed string enums
type Status string

const (
    StatusPending    Status = "PENDING"
    StatusInProgress Status = "IN_PROGRESS"
    StatusComplete   Status = "COMPLETE"
    StatusCancelled  Status = "CANCELLED"
)

func (s Status) String() string {
    return string(s)
}

func (s Status) IsValid() bool {
    switch s {
    case StatusPending, StatusInProgress, StatusComplete, StatusCancelled:
        return true
    default:
        return false
    }
}

func (s Status) IsTerminal() bool {
    return s == StatusComplete || s == StatusCancelled
}

func ParseStatus(s string) (Status, error) {
    status := Status(s)
    if !status.IsValid() {
        return "", fmt.Errorf("invalid status: %s", s)
    }
    return status, nil
}
```

### Integer Enums with iota

```go
// DO: Integer enums for ordered values
type Priority int

const (
    PriorityLow Priority = iota + 1
    PriorityMedium
    PriorityHigh
    PriorityCritical
)

func (p Priority) String() string {
    switch p {
    case PriorityLow:
        return "low"
    case PriorityMedium:
        return "medium"
    case PriorityHigh:
        return "high"
    case PriorityCritical:
        return "critical"
    default:
        return "unknown"
    }
}
```

---

## Retry Pattern

### Exponential Backoff

```go
func WithRetry[T any](ctx context.Context, op func() (T, error), opts RetryOptions) (T, error) {
    var result T
    var lastErr error
    
    for attempt := 0; attempt <= opts.MaxRetries; attempt++ {
        result, lastErr = op()
        if lastErr == nil {
            return result, nil
        }
        
        // Don't retry on non-retryable errors
        if !opts.IsRetryable(lastErr) {
            return result, lastErr
        }
        
        if attempt == opts.MaxRetries {
            break
        }
        
        // Calculate backoff
        backoff := opts.BaseDelay * time.Duration(1<<attempt)
        if backoff > opts.MaxDelay {
            backoff = opts.MaxDelay
        }
        
        select {
        case <-time.After(backoff):
        case <-ctx.Done():
            return result, ctx.Err()
        }
    }
    
    return result, fmt.Errorf("after %d retries: %w", opts.MaxRetries, lastErr)
}

type RetryOptions struct {
    MaxRetries  int
    BaseDelay   time.Duration
    MaxDelay    time.Duration
    IsRetryable func(error) bool
}

var DefaultRetryOptions = RetryOptions{
    MaxRetries: 3,
    BaseDelay:  100 * time.Millisecond,
    MaxDelay:   5 * time.Second,
    IsRetryable: func(err error) bool {
        // Retry transient errors
        return !errors.Is(err, ErrNotFound) && !errors.Is(err, ErrInvalidInput)
    },
}
```

### Usage

```go
task, err := WithRetry(ctx, func() (*Task, error) {
    return client.GetTask(ctx, id)
}, DefaultRetryOptions)
```

---

## Caching Pattern

### Simple In-Memory Cache

```go
type Cache[K comparable, V any] struct {
    mu    sync.RWMutex
    items map[K]cacheItem[V]
    ttl   time.Duration
}

type cacheItem[V any] struct {
    value     V
    expiresAt time.Time
}

func NewCache[K comparable, V any](ttl time.Duration) *Cache[K, V] {
    return &Cache[K, V]{
        items: make(map[K]cacheItem[V]),
        ttl:   ttl,
    }
}

func (c *Cache[K, V]) Get(key K) (V, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()
    
    item, ok := c.items[key]
    if !ok || time.Now().After(item.expiresAt) {
        var zero V
        return zero, false
    }
    return item.value, true
}

func (c *Cache[K, V]) Set(key K, value V) {
    c.mu.Lock()
    defer c.mu.Unlock()
    
    c.items[key] = cacheItem[V]{
        value:     value,
        expiresAt: time.Now().Add(c.ttl),
    }
}

func (c *Cache[K, V]) Delete(key K) {
    c.mu.Lock()
    defer c.mu.Unlock()
    delete(c.items, key)
}
```

### Get-Or-Set Pattern

```go
func (c *Cache[K, V]) GetOrSet(key K, fetch func() (V, error)) (V, error) {
    if v, ok := c.Get(key); ok {
        return v, nil
    }
    
    v, err := fetch()
    if err != nil {
        var zero V
        return zero, err
    }
    
    c.Set(key, v)
    return v, nil
}
```

---

## JSON/YAML Unmarshalling

### Strict Unmarshalling

```go
// DO: Use decoder with DisallowUnknownFields
func ParseConfig(r io.Reader) (*Config, error) {
    var cfg Config
    decoder := json.NewDecoder(r)
    decoder.DisallowUnknownFields()
    
    if err := decoder.Decode(&cfg); err != nil {
        return nil, fmt.Errorf("decode config: %w", err)
    }
    return &cfg, nil
}
```

### Custom Unmarshalling

```go
type Duration time.Duration

func (d *Duration) UnmarshalJSON(b []byte) error {
    var s string
    if err := json.Unmarshal(b, &s); err != nil {
        return err
    }
    
    duration, err := time.ParseDuration(s)
    if err != nil {
        return fmt.Errorf("invalid duration: %w", err)
    }
    
    *d = Duration(duration)
    return nil
}

func (d Duration) MarshalJSON() ([]byte, error) {
    return json.Marshal(time.Duration(d).String())
}
```

### Enum Unmarshalling

```go
func (s *Status) UnmarshalJSON(b []byte) error {
    var str string
    if err := json.Unmarshal(b, &str); err != nil {
        return err
    }
    
    status := Status(str)
    if !status.IsValid() {
        return fmt.Errorf("invalid status: %s", str)
    }
    
    *s = status
    return nil
}
```

---

## Pagination Pattern

### Cursor-Based Pagination

```go
type PageParams struct {
    Limit  int
    Cursor string
}

type PageResult[T any] struct {
    Items      []T
    NextCursor string
    HasMore    bool
}

func (s *Store) List(ctx context.Context, params PageParams) (*PageResult[*Task], error) {
    limit := params.Limit
    if limit <= 0 || limit > 100 {
        limit = 50
    }
    
    // Fetch one extra to determine if there are more
    tasks, err := s.query(ctx, params.Cursor, limit+1)
    if err != nil {
        return nil, err
    }
    
    hasMore := len(tasks) > limit
    if hasMore {
        tasks = tasks[:limit]
    }
    
    var nextCursor string
    if hasMore && len(tasks) > 0 {
        nextCursor = tasks[len(tasks)-1].ID.String()
    }
    
    return &PageResult[*Task]{
        Items:      tasks,
        NextCursor: nextCursor,
        HasMore:    hasMore,
    }, nil
}
```

---

## Builder Pattern

### Fluent Builder

```go
type QueryBuilder struct {
    filters    []string
    args       []any
    orderBy    string
    limit      int
    offset     int
}

func NewQueryBuilder() *QueryBuilder {
    return &QueryBuilder{}
}

func (b *QueryBuilder) Where(condition string, args ...any) *QueryBuilder {
    b.filters = append(b.filters, condition)
    b.args = append(b.args, args...)
    return b
}

func (b *QueryBuilder) OrderBy(column string) *QueryBuilder {
    b.orderBy = column
    return b
}

func (b *QueryBuilder) Limit(n int) *QueryBuilder {
    b.limit = n
    return b
}

func (b *QueryBuilder) Build() (string, []any) {
    query := "SELECT * FROM tasks"
    
    if len(b.filters) > 0 {
        query += " WHERE " + strings.Join(b.filters, " AND ")
    }
    if b.orderBy != "" {
        query += " ORDER BY " + b.orderBy
    }
    if b.limit > 0 {
        query += fmt.Sprintf(" LIMIT %d", b.limit)
    }
    
    return query, b.args
}

// Usage
query, args := NewQueryBuilder().
    Where("status = ?", "PENDING").
    Where("priority >= ?", 3).
    OrderBy("created_at DESC").
    Limit(50).
    Build()
```

---

## Result Pattern

### Result Type for Operations

```go
type Result[T any] struct {
    Value T
    Err   error
}

func (r Result[T]) IsOK() bool {
    return r.Err == nil
}

func (r Result[T]) Unwrap() (T, error) {
    return r.Value, r.Err
}

// Channel of results
func processAll(ctx context.Context, items []Item) <-chan Result[*Task] {
    results := make(chan Result[*Task])
    
    go func() {
        defer close(results)
        for _, item := range items {
            task, err := process(ctx, item)
            select {
            case results <- Result[*Task]{Value: task, Err: err}:
            case <-ctx.Done():
                return
            }
        }
    }()
    
    return results
}
```

---

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| Enum | Type-safe constants |
| Retry | Transient failures |
| Cache | Expensive computations |
| Pagination | Large datasets |
| Builder | Complex object construction |
| Result | Channel operations with errors |

---

## See Also

- [CACHING.md](./CACHING.md) - Advanced caching patterns
- [ENUMS.md](./ENUMS.md) - Enum implementation details
- [functional-options](../functional-options/Skill.md) - Option patterns
