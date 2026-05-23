---
name: golang
description: |
  Provides idiomatic Go programming expertise and best practices. Ensures clean, efficient, and maintainable code following official Go conventions. Specializes in concurrent programming patterns, interface design, error handling strategies, and performance optimization. Masters standard library usage and ecosystem integration.
  Use when: writing Go code (.go files), designing interfaces and struct types, implementing concurrent patterns (goroutines/channels), handling errors idiomatically, writing table-driven tests, creating Go modules, optimizing performance-critical code, managing dependencies with go.mod, implementing HTTP servers and clients, working with context propagation, or designing package APIs for public libraries.
---

# Go Coding Standards

## Basic Principles

### One Function, One Responsibility

- If function name connects with "and" or "or", it's a signal to split
- If test cases are needed for each if branch, it's a signal to split

### Conditional and Loop Depth Limited to 2 Levels

- Minimize depth using early return whenever possible
- If still heavy, extract into separate functions

### Make Function Side Effects Explicit

- Example: If `getUser` also runs `updateLastAccess()`, specify it in the function name

### Convert Magic Numbers/Strings to Constants When Possible

- Declare at the top of the file where used
- Consider separating into a constants file if there are many

### Function Order by Call Order

- Follow Go's clear conventions if they exist
- Otherwise, order top-to-bottom for easy reading by call order

### Review External Libraries for Complex Implementations

- When logic is complex and tests become bloated
- If industry-standard libraries exist, use them
- When security, accuracy, or performance optimization is critical
- When platform compatibility or edge cases are numerous

### Modularization (Prevent Code Duplication and Pattern Repetition)

- Absolutely forbid code repetition
- Modularize similar patterns into reusable forms
- Allow pre-modularization if reuse is confirmed
- Avoid excessive abstraction
- Modularization levels:
  - Same file: Extract into separate function
  - Multiple files: Separate into different package
  - Multiple projects/domains: Separate into different module

### Variable and Function Names

- Clear purpose while being concise
- Forbid abbreviations outside industry standards (id, api, db, err, etc.)
- Don't repeat context from the parent scope
- Boolean variables use `is`, `has`, `should` prefixes
- Function names are verbs or verb+noun forms
- Plural rules:
  - Pure arrays/slices: "s" suffix (`users`)
  - Wrapped struct: "list" suffix (`userList`)
  - Specific data structure: Explicit (`userSet`, `userMap`)
  - Already plural words: Use as-is

### Field Order

- Alphabetically ascending by default
- Maintain consistency in usage

### Error Handling

- Error handling level: Handle where meaningful response is possible
- Error messages: Technical details for logs, actionable guidance for users
- Error classification: Distinguish between expected and unexpected errors
- Error propagation: Add context when propagating up the call stack
- Recovery vs. fast fail: Recover from expected errors with fallback
- Use %w for error chains, %v for simple logging
- Wrap internal errors not to be exposed with %v
- Never ignore return errors from functions; handle them explicitly
- Sentinel errors: For expected conditions that callers must handle, use `var ErrNotFound = errors.New("not found")`

## File Structure

### Element Order in File

1. package declaration
2. import statements (grouped)
3. Constant definitions (const)
4. Variable definitions (var)
5. Type/Interface/Struct definitions
6. Constructor functions (New\*)
7. Methods (grouped by receiver type, alphabetically ordered)
8. Helper functions (alphabetically ordered)

## Interfaces and Structs

### Interface Definition Location

- Define interfaces in the package that uses them (Accept interfaces, return structs)
- Only separate shared interfaces used by multiple packages

### Pointer Receiver Rules

- Use pointer receivers for state modification, large structs (3+ fields), or when consistency is needed
- Use value receivers otherwise

## Context Usage

### Context Parameter

- Always pass as the first parameter
- Use `context.Background()` only in main and tests

## Testing

### Testing Libraries

- Prefer standard library's if + t.Errorf over assertion libraries like testify
- Prefer manual mocking over gomock

## Forbidden Practices

### init() Functions

- Generally forbidden. Prefer explicit initialization functions

## Package Structure

### internal Package

- Actively use for libraries, use only when necessary for applications

## Recommended Libraries

- Web: Fiber
- DB: Bun, SQLBoiler (when managing migrations externally)
- Logging: slog
- CLI: cobra
- Utilities: samber/lo, golang.org/x/sync
- Configuration: koanf (viper if cobra integration needed)
- Validation: go-playground/validator/v10
- Scheduling: github.com/go-co-op/gocron
- Image processing: github.com/h2non/bimg
