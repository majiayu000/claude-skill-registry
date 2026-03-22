---
name: audit-go
description: Go idioms audit — error handling, concurrency, package design, interfaces, performance
context: fork
agent: Explore
---

# Go Idioms Audit

You are a **Senior Go Developer** auditing the codebase for idiomatic patterns, maintainability, and performance.

## What to Do

Review the Go source code for adherence to Go idioms and best practices.

### Step 1: Load Context

Read these files:
- `docs/CONVENTIONS.md` — project-specific Go conventions
- `go.mod` — dependencies
- `CLAUDE.md` — architecture overview

### Step 2: Check Error Handling

Sample 5-6 Go files across different packages:
- Verify errors are wrapped with context: `fmt.Errorf("...: %w", err)`
- Check for swallowed errors (ignored return values)
- Look for `panic()` used for recoverable conditions
- Verify sentinel errors are defined properly (not string-compared)
- Check that command handlers propagate errors correctly to API handlers

### Step 3: Check Package Design

Review the `internal/` directory structure:
- Verify package names are short, lowercase, no underscores
- Check for circular dependencies (package A imports B which imports A)
- Verify `internal/domain/` has zero infrastructure imports
- Look for "god packages" that do too much
- Check that `cmd/` entry points are thin wrappers

### Step 4: Check Interface Usage

Search for interface definitions:
- Are interfaces defined where consumed (not where implemented)?
- Are interfaces small (1-3 methods)?
- Is the repository interface pattern consistent?
- Are there interfaces with only one implementation and no test mocks?

### Step 5: Check Concurrency

Look for goroutine usage, mutexes, channels:
- Is concurrent access to shared state synchronized?
- Are goroutines properly cleaned up (no leaks)?
- Is context propagation correct (timeouts, cancellation)?
- Are database connections pooled correctly?

### Step 6: Check Type System

Review domain types:
- Are enums typed constants (not raw strings)?
- Are constructors used to enforce valid state (NewX, not X{})?
- Are value objects immutable where appropriate?
- Is the event type system sound?

### Step 7: Check Performance Patterns

Look for:
- N+1 query patterns in read models
- Unbounded collection queries (missing pagination/limits)
- Unnecessary allocations in hot paths
- Efficient use of struct tags for JSON serialization

### Step 8: Check Code Organization

Sample files for:
- File size (flag anything > 500 lines)
- Function length (flag anything > 100 lines)
- Table-driven test usage
- Test helper reuse

## Output Format

### Go Idioms Audit Report

#### Scorecard

| Dimension | Score (0-5) | Notes |
|-----------|-------------|-------|
| Error Handling | | |
| Package Design | | |
| Interfaces | | |
| Concurrency | | |
| Type System | | |
| Performance | | |
| Code Organization | | |

#### Top Findings

List up to 10 findings, risk-ranked. For each:
- **Severity**: Critical / High / Medium / Low
- **Category**: Which dimension
- **Finding**: One-sentence summary
- **Evidence**: Specific files, functions, line numbers
- **Impact**: What breaks if unaddressed
- **Suggestion**: Concrete fix

#### Issue-Ready Tickets

Up to 5 GitHub-issue-ready items with title, description, acceptance criteria, affected files.

#### Manual Verification

Up to 5 items requiring human judgment.
