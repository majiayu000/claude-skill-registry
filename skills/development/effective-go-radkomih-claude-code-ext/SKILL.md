---
name: effective-go
description: Analyzes and refactors Go code using Effective Go principles. Use when refactoring Go code, identifying anti-patterns, improving Go idioms, or applying Go best practices.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Effective Go Skill

Comprehensive Go refactoring framework based on the official Effective Go guide and Go best practices.

## When to Use This Skill

- Refactoring Go code for idiomatic patterns
- Identifying Go-specific anti-patterns
- Improving code formatting and style
- Applying proper error handling patterns
- Optimizing concurrency patterns (goroutines, channels)
- Implementing proper naming conventions
- Analyzing interface and method design
- Reviewing receiver types (pointer vs value)

## Prerequisites

**CRITICAL**: Always load the Effective Go principles first:

```bash
Read: plugins/effective-go/resources/effective-go-principles.json
```

This JSON contains 25+ principles with definitions, code smells, and refactoring guidance including:
- Formatting (gofmt, semicolons)
- Naming (packages, interfaces, exported names)
- Control structures (if, for, switch, defer)
- Data structures (slices, maps, arrays)
- Functions (multiple returns, named returns, defer)
- Concurrency (goroutines, channels, select)
- Error handling (error vs panic, wrapping)
- Interfaces and methods (receivers, embedding)

## Refactoring Approach

### Four-Phase Strategy

#### Phase 1: Discovery & Analysis (15-20 min)

**Understand the Codebase:**
1. Identify scope (package, module, or entire project)
2. Check Go version and module structure
3. Analyze existing code patterns
4. Review dependencies and imports

**Scan for Code Smells:**
- No gofmt/goimports formatting
- Non-idiomatic naming (snake_case, wrong capitalization)
- Wrong receiver types (value when pointer needed)
- Missing error checks
- Goroutine leaks or race conditions
- Improper channel usage
- Panic in library code
- Mutable value types that should be immutable
- Large interfaces (>3 methods for non-standard libs)
- Primitive obsession (no custom types)

**Technical Exploration:**
```bash
# Check if code is gofmt'd
gofmt -l . | grep -v "vendor/"

# Find exported names that might be wrong
grep -r "^func [a-z]" --include="*.go"
grep -r "^type [a-z]" --include="*.go"

# Find potential goroutine issues
grep -r "go func" --include="*.go"
grep -r "go " --include="*.go" | grep -v "go func"

# Find error handling
grep -r "err :=" --include="*.go"
grep -r "if err" --include="*.go"

# Find panic usage
grep -r "panic(" --include="*.go"

# Find interfaces
grep -r "type.*interface" --include="*.go"
```

#### Phase 2: Strategic Refactoring Plan (10-15 min)

Based on loaded Effective Go principles:

1. **Formatting and Style**
   - Run gofmt/goimports on all files
   - Fix semicolon issues
   - Ensure proper brace placement
   - Clean up whitespace

2. **Naming Conventions**
   - Fix package names (lowercase, single-word)
   - Correct exported/unexported names
   - Apply MixedCaps/mixedCaps consistently
   - Rename interfaces (-er suffix for single-method)

3. **Prioritize Refactoring**
   - **Critical**: gofmt, data races, goroutine leaks, missing error checks
   - **High**: Wrong receivers, panic in libraries, improper channel usage
   - **Medium**: Non-idiomatic naming, primitive obsession, large interfaces
   - **Low**: Style improvements, comment formatting

#### Phase 3: Tactical Pattern Application (30-45 min)

Apply patterns systematically:

**1. Formatting**
- Run gofmt -w on all Go files
- Ensure tabs for indentation
- Fix opening brace placement
- Remove unnecessary semicolons

**2. Naming**
- Package names: short, lowercase, no underscores
- Exported names: Start with uppercase
- Unexported names: Start with lowercase
- Interfaces: Use -er suffix (Reader, Writer, Closer)
- No snake_case: Use MixedCaps or mixedCaps
- Acronyms: All caps (HTTP, URL, ID)

**3. Control Structures**
- Use guard clauses (early returns)
- Prefer for range over traditional for loops
- Use expression-less switch for if-else chains
- Apply defer for cleanup operations
- Avoid naked returns in long functions

**4. Error Handling**
- Check all errors explicitly
- Add context with fmt.Errorf and %w
- Return errors, don't panic (except in truly exceptional cases)
- Use errors.Is and errors.As for error checking
- Implement error wrapping consistently

**5. Concurrency**
- Fix goroutine leaks (ensure they can exit)
- Use channels for communication
- Apply proper channel closing (sender closes)
- Use select for multiplexing
- Avoid shared memory, prefer channels
- Add sync.WaitGroup for coordination
- Fix loop variable capture in goroutines

**6. Pointers vs Values**
- Use pointer receivers when modifying receiver
- Use pointer receivers for large structs
- Be consistent (all pointer or all value for a type)
- Use pointer receivers for types with sync.Mutex

**7. Interfaces**
- Keep interfaces small (1-3 methods ideal)
- Define interfaces where used, not where implemented
- Accept interfaces, return structs
- Use empty interface sparingly

**8. Data Structures**
- Prefer slices over arrays
- Use make() with capacity hints
- Ensure maps are initialized with make()
- Use composite literals for initialization
- Apply append() correctly (assign result)

#### Phase 4: Validation & Testing (10-15 min)

**Verify Improvements:**
- [ ] All files pass gofmt check
- [ ] No exported names start with lowercase
- [ ] All errors are checked or explicitly ignored
- [ ] No goroutine leaks detected
- [ ] Channels properly closed from sender
- [ ] Receiver types are consistent and appropriate
- [ ] No panic calls in library code
- [ ] Interfaces are small and focused
- [ ] Code follows Go idioms

**Testing Strategy:**
- Run go vet on all packages
- Run golint or staticcheck
- Run go test -race to detect data races
- Use go test -cover for coverage
- Run golangci-lint for comprehensive checks

## Core Effective Go Principles Reference

### Formatting
1. **gofmt** - Standard formatting, non-negotiable
2. **Semicolons** - Automatic insertion, placement rules

### Naming
3. **Package Names** - Short, lowercase, single-word
4. **Exported Names** - Uppercase = public
5. **Interface Naming** - -er suffix for single-method
6. **MixedCaps** - No underscores in identifiers

### Control Structures
7. **Guard Clauses** - Early returns, reduced nesting
8. **For Loop Patterns** - Range, traditional, infinite
9. **Switch Statements** - No fallthrough by default
10. **Type Switch** - Handling interface types
11. **Defer** - Cleanup operations

### Functions
12. **Multiple Return Values** - Return (result, error)
13. **Named Return Values** - For documentation/defer
14. **new vs make** - Allocation primitives

### Data
15. **Slices** - Dynamic sequences
16. **Maps** - Key-value storage
17. **Printing** - Format verbs (%v, %+v, %#v)
18. **Append** - Growing slices

### Initialization
19. **Composite Literals** - Inline initialization

### Methods
20. **Pointer vs Value Receivers** - When to use each

### Interfaces
21. **Interfaces** - Implicit implementation
22. **Type Assertions** - Safe conversion
23. **Embedding** - Composition over inheritance

### Concurrency
24. **Share by Communicating** - Channel-based patterns
25. **Goroutines** - Lightweight concurrency
26. **Channels** - Communication pipes
27. **Select** - Multiplexing channels

### Errors
28. **Error Handling** - Explicit error returns
29. **Panic** - Only for unrecoverable errors
30. **Recover** - Panic recovery
31. **Error Wrapping** - Adding context with %w

## Code Smell Detection Checklist

### Critical Anti-Patterns
- [ ] Code not formatted with gofmt
- [ ] Exported names starting with lowercase
- [ ] Panic used in library code
- [ ] Data races (concurrent map access, shared state)
- [ ] Goroutine leaks (no way to stop)
- [ ] Sending on closed channel

### High Priority Anti-Patterns
- [ ] Mixed pointer and value receivers on same type
- [ ] Missing error checks
- [ ] Errors ignored with _
- [ ] Improper channel closing (receiver closes, or closing nil channel)
- [ ] Loop variable captured in goroutine
- [ ] Using new() for slices, maps, channels
- [ ] Not assigning append() result

### Medium Priority Anti-Patterns
- [ ] Snake_case naming instead of MixedCaps
- [ ] Large interfaces (>5 methods)
- [ ] Missing doc comments on exported identifiers
- [ ] Using interface{} when specific type would work
- [ ] Not using defer for cleanup
- [ ] Naked returns in long functions
- [ ] Arrays when slices would be better

### Low Priority Anti-Patterns
- [ ] Inconsistent naming
- [ ] Missing String() method for custom types
- [ ] Could use type switch instead of repeated assertions
- [ ] Could use composite literal instead of new()

## Output Format

### 1. Anti-Pattern Identified
```
File: internal/service/order.go:45-78
Smell: Missing error check - result of operation ignored
Principle Violated: Error Handling
Impact: Silent failures, bugs go unnoticed
```

### 2. Effective Go Principle to Apply
```
Principle: Error Handling (from effective-go-principles.json)
Category: Errors
Key Point: Always check errors explicitly, never ignore them
When to Apply: Every function call that returns an error
```

### 3. Refactoring Steps
```
Step 1: Find all places where errors are returned
Step 2: Add explicit error checks with if err != nil
Step 3: Add context to errors with fmt.Errorf("operation failed: %w", err)
Step 4: Propagate or handle errors appropriately
Step 5: Use _ only for intentional ignoring (document why)
```

### 4. Code Example
```go
// BEFORE: Missing error check (Anti-pattern)
func processOrder(id string) *Order {
	order, _ := db.GetOrder(id) // ERROR: Ignoring error!
	return order
}

func updateUser(user *User) {
	db.Save(user) // ERROR: Not checking error!
}

// AFTER: Proper error handling (Go idiom)
func processOrder(id string) (*Order, error) {
	order, err := db.GetOrder(id)
	if err != nil {
		return nil, fmt.Errorf("getting order %s: %w", id, err)
	}
	return order, nil
}

func updateUser(user *User) error {
	if err := db.Save(user); err != nil {
		return fmt.Errorf("saving user %s: %w", user.ID, err)
	}
	return nil
}
```

### 5. Impact Assessment
**Benefits:**
- Errors are caught and handled explicitly
- Better error context for debugging
- No silent failures
- Follows Go conventions

**Metrics:**
- Improved reliability
- Better error messages
- Easier debugging
- Code passes go vet checks

## Language-Specific Patterns

### Error Handling
```go
// Good: Proper error handling with context
func loadConfig(path string) (*Config, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("reading config from %s: %w", path, err)
	}

	var cfg Config
	if err := json.Unmarshal(data, &cfg); err != nil {
		return nil, fmt.Errorf("parsing config: %w", err)
	}

	return &cfg, nil
}

// Usage
cfg, err := loadConfig("config.json")
if err != nil {
	log.Fatalf("Failed to load config: %v", err)
}
```

### Receiver Types
```go
// Good: Consistent pointer receivers
type Counter struct {
	mu    sync.Mutex
	value int
}

// Pointer receiver - modifies state
func (c *Counter) Increment() {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.value++
}

// Pointer receiver - consistency
func (c *Counter) Value() int {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.value
}

// Bad: Mixed receivers
type BadCounter struct {
	value int
}

func (c BadCounter) Increment() { // Value receiver - doesn't modify!
	c.value++ // Modifies copy
}

func (c *BadCounter) Value() int { // Pointer receiver - inconsistent
	return c.value
}
```

### Goroutines and Channels
```go
// Good: Proper goroutine coordination
func processBatch(items []Item) error {
	var wg sync.WaitGroup
	errors := make(chan error, len(items))

	for _, item := range items {
		wg.Add(1)
		item := item // Capture variable

		go func() {
			defer wg.Done()
			if err := process(item); err != nil {
				errors <- err
			}
		}()
	}

	// Wait in separate goroutine
	go func() {
		wg.Wait()
		close(errors) // Sender closes channel
	}()

	// Collect errors
	for err := range errors {
		return err // Return first error
	}

	return nil
}

// Bad: Goroutine leak
func badProcess(items []Item) {
	for _, item := range items {
		go func() {
			process(item) // Captures loop variable - BUG!
			// No coordination, no error handling, no way to stop
		}()
	}
	// Function returns immediately, goroutines may still be running
}
```

### Interfaces
```go
// Good: Small, focused interfaces
type Reader interface {
	Read(p []byte) (n int, err error)
}

type Closer interface {
	Close() error
}

type ReadCloser interface {
	Reader
	Closer
}

// Define where used, not where implemented
type DataStore interface {
	Save(data []byte) error
}

func SaveToStore(store DataStore, data []byte) error {
	return store.Save(data)
}

// Bad: Large, unfocused interface
type Database interface {
	GetUser(id string) (*User, error)
	CreateUser(u *User) error
	UpdateUser(u *User) error
	DeleteUser(id string) error
	GetOrder(id string) (*Order, error)
	CreateOrder(o *Order) error
	// ... 20+ more methods
}
```

## Best Practices

### Do
- Always run gofmt before committing
- Check all errors explicitly
- Use defer for cleanup operations
- Keep interfaces small
- Accept interfaces, return structs
- Use pointer receivers for large structs or when modifying
- Close channels from the sender side
- Use context for cancellation and timeouts
- Wrap errors with %w for error chains
- Use sync.WaitGroup to coordinate goroutines

### Don't
- Don't ignore gofmt warnings
- Don't use panic in library code
- Don't ignore errors with _
- Don't mix pointer and value receivers
- Don't capture loop variables in goroutines without copying
- Don't send on closed channels
- Don't use naked returns in long functions
- Don't create large interfaces
- Don't share memory without synchronization
- Don't use new() for slices, maps, or channels

## Resources

- **Effective Go Principles**: See `resources/effective-go-principles.json` for complete definitions
- **Checklist**: See `CHECKLIST.md` for full anti-pattern list
- **Official Guide**: https://go.dev/doc/effective_go
- **Go Code Review Comments**: https://go.dev/wiki/CodeReviewComments

## Workflow Integration

This skill can be:
- Invoked from `/go-review` command
- Used by `go-analyzer` agent for autonomous analysis
- Triggered by pre-commit hooks to check for anti-patterns
- Called from other skills for Go code improvements
