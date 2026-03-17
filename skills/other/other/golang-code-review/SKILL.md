---
name: golang-code-review
description: Comprehensive Go code review skill for PR reviews, architecture assessment, and test quality analysis. Use when reviewing Go code to ensure adherence to Go best practices, security standards, and project-specific patterns. Applies to full PR reviews, single file/function reviews, architecture evaluation, and test code quality checks.
---

# Golang Code Review

Perform thorough Go code reviews incorporating both external Go best practices and project-specific patterns.

## Review Process

### 1. Understand the Context

Before reviewing, gather context:
- Read the PR description or understand the change purpose
- Identify the domain/package being modified
- Check if this affects core business logic, API endpoints, or tests

### 2. Load Relevant References

Based on the review type, read appropriate references:

- **Always read**: `references/teetsh-patterns.md` for project-specific patterns
- **For general code quality**: `references/effective-go.md` for Go best practices
- **For bug prevention**: `references/common-mistakes.md` for antipatterns
- **For security-sensitive code** (auth, payments, user input, external APIs): `references/security.md`

### 3. Review Scope by Type

**Full PR Review**: Check all aspects - architecture, implementation, tests, security

**Architecture Review**: Focus on package structure, interfaces, separation of concerns, domain boundaries

**Test Review**: Focus on test quality, coverage, behavior vs implementation testing

**Single Function/File**: Focus on implementation quality, naming, error handling

### 4. Provide Structured Feedback

Organize feedback by priority:

#### Critical Issues
Security vulnerabilities, data loss risks, concurrency bugs, resource leaks

#### Important Issues
Architecture problems, missing error handling, incorrect business logic, test gaps

#### Suggestions
Code clarity, performance optimizations, idiomatic Go patterns

#### Positive Feedback
Well-designed patterns, good test coverage, clear naming

### 5. Code Examples

For each issue, provide:
- **What**: Describe the problem
- **Why**: Explain the risk or impact
- **How**: Show code example of the fix

## Key Review Areas

### Project-Specific Patterns

Check adherence to Teetsh patterns:
- Functions extracted with proper abstraction levels
- Return structs instead of multiple values for related data
- Vanilla Go testing without assertion libraries
- Behavior-driven tests checking outcomes not implementation
- Comments explain why, not what
- Multi-tenancy: school_id included in queries
- Analytics events defined in `pkg/externals/tracker/client.go`
- REST structure: domain/repo/service/handler separation

### Go Best Practices

- Proper error handling with context wrapping
- Correct concurrency patterns (goroutines, channels, mutexes)
- Interface usage: accept interfaces, return structs
- Resource management with defer
- Idiomatic naming and structure

### Security

For auth, payments, user input, external API code:
- Input validation and sanitization
- SQL injection prevention (parameterized queries)
- Proper password hashing (bcrypt)
- Secure token generation (crypto/rand)
- TLS configuration
- Authorization checks

### Testing

- Test both success and error cases
- Isolated test state (no global state)
- Behavior verification not implementation details
- Vanilla Go testing (`t.Error`, `t.Fatal`, `t.Errorf`)
- Clear test names describing what is tested

## Review Output Format

Structure your review as:

```
## Critical Issues
[Issues that must be fixed before merge]

## Important Issues
[Issues that should be fixed]

## Suggestions
[Optional improvements]

## Positive Feedback
[What was done well]
```

For each issue:
```
### [Area]: [Brief description]

**Problem**: [What's wrong and why it matters]

**Current code**:
```go
[Show problematic code]
```

**Suggested fix**:
```go
[Show corrected code]
```

**Reference**: [Link to specific pattern/practice]
```

## Example Review Snippets

### Function Design Issue
```
### Function Design: Mixed abstraction levels in GetUserData

**Problem**: Function mixes high-level flow with low-level details, making it hard to understand intent

**Current code**:
```go
func GetUserData(id int) (*User, error) {
    query := "SELECT * FROM users WHERE id = ?"
    row := db.QueryRow(query, id)
    var user User
    err := row.Scan(&user.ID, &user.Name, &user.Email)
    if err != nil {
        return nil, err
    }
    // ... more low-level operations
}
```

**Suggested fix**:
```go
func GetUserData(id int) (*User, error) {
    user, err := findUserByID(id)
    if err != nil {
        return nil, fmt.Errorf("failed to get user data: %w", err)
    }
    return user, nil
}

func findUserByID(id int) (*User, error) {
    query := "SELECT * FROM users WHERE id = ?"
    row := db.QueryRow(query, id)
    var user User
    if err := row.Scan(&user.ID, &user.Name, &user.Email); err != nil {
        return nil, err
    }
    return &user, nil
}
```

**Reference**: See `references/teetsh-patterns.md` - Function Design
```

### Testing Issue
```
### Testing: Using assertion library instead of vanilla Go

**Problem**: Project uses vanilla Go testing for better stack traces and no external dependencies

**Current code**:
```go
assert.Equal(t, expected, result)
assert.NotNil(t, user)
```

**Suggested fix**:
```go
if result != expected {
    t.Errorf("Expected %v, got %v", expected, result)
}
if user == nil {
    t.Fatal("user should not be nil")
}
```

**Reference**: See `references/teetsh-patterns.md` - Testing Patterns
```

### Security Issue
```
### Security: SQL injection vulnerability

**Problem**: User input concatenated into SQL query allows SQL injection attacks

**Current code**:
```go
query := "SELECT * FROM users WHERE email = '" + email + "'"
db.Query(query)
```

**Suggested fix**:
```go
query := "SELECT * FROM users WHERE email = $1"
db.Query(query, email)
```

**Reference**: See `references/security.md` - SQL Injection Prevention
```

## When NOT to Comment

Avoid feedback on:
- Trivial formatting issues (gofmt handles this)
- Personal style preferences not in project patterns
- Nitpicks that don't affect functionality or maintainability
- Issues already addressed in other comments

## Multi-file Review Strategy

For PRs with many files:
1. Start with architecture overview (new packages, major changes)
2. Review core business logic files first
3. Review tests for core logic
4. Review supporting files (handlers, viewmodels)
5. Summarize overall assessment

## After Review

If significant issues found:
- Summarize the most important themes
- Suggest whether changes are required before merge
- Offer to explain any patterns or practices in detail
