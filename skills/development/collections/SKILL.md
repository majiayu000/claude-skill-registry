---
description: Reviews Go slice and map usage for nil semantics, capacity hints, and iteration patterns. Use when reviewing collection operations, seeing slice/map initialization, or encountering nil panics.
---

# Collections

## Purpose

Establish patterns for working with slices and maps in RMS Go code. Understanding collection semantics prevents common bugs and improves performance.

## Core Principles

1. **Understand nil semantics** - Nil slices and maps behave differently
2. **Use capacity hints** - Pre-allocate when size is known
3. **Prefer range** - For iteration over index-based access
4. **Consider thread safety** - Maps are not safe for concurrent access

---

## Slices

### Nil vs Empty Slice

```go
// Nil slice - default zero value
var tasks []*Task  // nil slice
len(tasks)         // 0
cap(tasks)         // 0
tasks == nil       // true

// Empty slice - explicitly allocated
tasks := []*Task{}       // empty slice
tasks := make([]*Task, 0) // empty slice
len(tasks)                // 0
tasks == nil              // false

// Behavior difference
json.Marshal(nil)    // null
json.Marshal([]*Task{}) // []
```

### When to Use Each

```go
// DO: Use nil slice as return value when appropriate
func (s *Store) List(ctx context.Context) ([]*Task, error) {
    // Returns nil when no results - this is fine
    return nil, nil
}

// DO: Use empty slice for JSON serialization
func (h *Handler) ListTasks(w http.ResponseWriter, r *http.Request) {
    tasks, err := store.List(r.Context())
    if tasks == nil {
        tasks = []*Task{}  // Serialize as [] not null
    }
    json.NewEncoder(w).Encode(tasks)
}

// DO: Check length, not nil
if len(tasks) == 0 {
    // Works for both nil and empty
}

// DON'T: Check nil when you mean empty
if tasks == nil {  // Misses empty slices
    // ...
}
```

### Capacity Hints

```go
// DO: Pre-allocate when size is known
func convertTasks(items []*Item) []*Task {
    tasks := make([]*Task, 0, len(items))
    for _, item := range items {
        tasks = append(tasks, convertTask(item))
    }
    return tasks
}

// DO: Pre-allocate with make for known size
func getIDs(tasks []*Task) []rms.ID {
    ids := make([]rms.ID, len(tasks))
    for i, task := range tasks {
        ids[i] = task.ID
    }
    return ids
}

// DON'T: Grow slice repeatedly
func convertTasks(items []*Item) []*Task {
    var tasks []*Task  // Starts at 0 capacity
    for _, item := range items {
        tasks = append(tasks, convertTask(item))  // Multiple reallocations
    }
    return tasks
}
```

### Slice Operations

```go
// Append
tasks = append(tasks, newTask)
tasks = append(tasks, moreTasks...)

// Copy
dst := make([]*Task, len(src))
copy(dst, src)

// Delete (preserving order)
tasks = append(tasks[:i], tasks[i+1:]...)

// Delete (no order preservation, more efficient)
tasks[i] = tasks[len(tasks)-1]
tasks = tasks[:len(tasks)-1]

// Filter in place
n := 0
for _, task := range tasks {
    if task.IsValid() {
        tasks[n] = task
        n++
    }
}
tasks = tasks[:n]
```

---

## Maps

### Nil Map Behavior

```go
// Nil map - read OK, write panics
var m map[string]int  // nil
v := m["key"]         // Returns 0 (zero value), no panic
m["key"] = 1          // PANIC: assignment to nil map

// Always initialize before writing
m = make(map[string]int)
m["key"] = 1  // OK

// Or use map literal
m := map[string]int{
    "key": 1,
}
```

### Capacity Hints

```go
// DO: Hint capacity for large maps
func buildIndex(tasks []*Task) map[rms.ID]*Task {
    index := make(map[rms.ID]*Task, len(tasks))
    for _, task := range tasks {
        index[task.ID] = task
    }
    return index
}

// DON'T: No hint when size is known
func buildIndex(tasks []*Task) map[rms.ID]*Task {
    index := make(map[rms.ID]*Task)  // Grows repeatedly
    for _, task := range tasks {
        index[task.ID] = task
    }
    return index
}
```

### Comma-Ok Idiom

```go
// DO: Check existence with comma-ok
if task, ok := taskMap[id]; ok {
    // task exists
    process(task)
} else {
    // task doesn't exist
}

// DO: Distinguish zero value from missing
count, exists := counts[key]
if !exists {
    counts[key] = 1
} else {
    counts[key] = count + 1
}

// DON'T: Assume zero means missing
count := counts[key]
if count == 0 {  // Bug: 0 could be a valid value
    // ...
}
```

### Map Iteration

```go
// DO: Iterate with range
for key, value := range m {
    fmt.Printf("%s: %v\n", key, value)
}

// DO: Keys only
for key := range m {
    keys = append(keys, key)
}

// CAUTION: Iteration order is random
// If you need ordered iteration, sort keys first
keys := make([]string, 0, len(m))
for k := range m {
    keys = append(keys, k)
}
sort.Strings(keys)
for _, k := range keys {
    fmt.Printf("%s: %v\n", k, m[k])
}
```

### Safe Deletion During Iteration

```go
// DO: Delete during iteration is safe
for k, v := range m {
    if shouldDelete(v) {
        delete(m, k)  // Safe
    }
}

// DON'T: Add during iteration (undefined behavior)
for k := range m {
    m[k+"_copy"] = m[k]  // May or may not see new keys
}
```

---

## Thread Safety

### Maps Are Not Thread-Safe

```go
// DON'T: Concurrent map access
var cache = make(map[string]*Task)

func get(key string) *Task {
    return cache[key]  // Data race!
}

func set(key string, task *Task) {
    cache[key] = task  // Data race!
}
```

### Use sync.Map for Concurrent Access

```go
// DO: sync.Map for concurrent access
var cache sync.Map

func get(key string) (*Task, bool) {
    if v, ok := cache.Load(key); ok {
        return v.(*Task), true
    }
    return nil, false
}

func set(key string, task *Task) {
    cache.Store(key, task)
}

func getOrCreate(key string, create func() *Task) *Task {
    v, _ := cache.LoadOrStore(key, create())
    return v.(*Task)
}
```

### Mutex-Protected Map

```go
// DO: Mutex for complex operations
type TaskCache struct {
    mu    sync.RWMutex
    tasks map[rms.ID]*Task
}

func (c *TaskCache) Get(id rms.ID) (*Task, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()
    task, ok := c.tasks[id]
    return task, ok
}

func (c *TaskCache) Set(id rms.ID, task *Task) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.tasks[id] = task
}

func (c *TaskCache) GetOrSet(id rms.ID, create func() *Task) *Task {
    c.mu.Lock()
    defer c.mu.Unlock()
    
    if task, ok := c.tasks[id]; ok {
        return task
    }
    
    task := create()
    c.tasks[id] = task
    return task
}
```

---

## Common Patterns

### Grouping

```go
// Group items by key
func groupByStatus(tasks []*Task) map[Status][]*Task {
    groups := make(map[Status][]*Task)
    for _, task := range tasks {
        groups[task.Status] = append(groups[task.Status], task)
    }
    return groups
}

// Group by workflow with capacity hint
func groupByWorkflow(tasks []*Task) map[rms.ID][]*Task {
    groups := make(map[rms.ID][]*Task, len(tasks)/10)  // Estimate
    for _, task := range tasks {
        groups[task.WorkflowID] = append(groups[task.WorkflowID], task)
    }
    return groups
}
```

### Deduplication

```go
// Deduplicate slice
func uniqueIDs(ids []rms.ID) []rms.ID {
    seen := make(map[rms.ID]struct{}, len(ids))
    result := make([]rms.ID, 0, len(ids))
    
    for _, id := range ids {
        if _, ok := seen[id]; !ok {
            seen[id] = struct{}{}
            result = append(result, id)
        }
    }
    
    return result
}
```

### Set Operations

```go
// Set using map
type StringSet map[string]struct{}

func NewStringSet(values ...string) StringSet {
    s := make(StringSet, len(values))
    for _, v := range values {
        s[v] = struct{}{}
    }
    return s
}

func (s StringSet) Add(value string)    { s[value] = struct{}{} }
func (s StringSet) Remove(value string) { delete(s, value) }
func (s StringSet) Contains(value string) bool {
    _, ok := s[value]
    return ok
}
```

### Index Building

```go
// Build lookup index
func buildTaskIndex(tasks []*Task) map[rms.ID]*Task {
    index := make(map[rms.ID]*Task, len(tasks))
    for _, task := range tasks {
        index[task.ID] = task
    }
    return index
}

// Multi-index
type TaskIndices struct {
    ByID       map[rms.ID]*Task
    ByWorkflow map[rms.ID][]*Task
    ByStatus   map[Status][]*Task
}

func buildIndices(tasks []*Task) *TaskIndices {
    indices := &TaskIndices{
        ByID:       make(map[rms.ID]*Task, len(tasks)),
        ByWorkflow: make(map[rms.ID][]*Task),
        ByStatus:   make(map[Status][]*Task),
    }
    
    for _, task := range tasks {
        indices.ByID[task.ID] = task
        indices.ByWorkflow[task.WorkflowID] = append(indices.ByWorkflow[task.WorkflowID], task)
        indices.ByStatus[task.Status] = append(indices.ByStatus[task.Status], task)
    }
    
    return indices
}
```

---

## Quick Reference

| Operation | Slice | Map |
|-----------|-------|-----|
| Zero value | `nil` (safe to read) | `nil` (panics on write) |
| Initialize | `make([]T, len, cap)` | `make(map[K]V, cap)` |
| Length | `len(s)` | `len(m)` |
| Add | `s = append(s, v)` | `m[k] = v` |
| Delete | `s = append(s[:i], s[i+1:]...)` | `delete(m, k)` |
| Check exists | `i < len(s)` | `_, ok := m[k]` |
| Thread-safe | No | No (use sync.Map) |

### Checklist

- [ ] Pre-allocated with known capacity?
- [ ] Nil vs empty semantics correct for use case?
- [ ] Comma-ok used for map lookups?
- [ ] Thread safety considered?
- [ ] Range used for iteration?

---

## See Also

- [concurrency](../concurrency/Skill.md) - Thread-safe patterns
- [control-flow](../control-flow/Skill.md) - Iteration patterns
