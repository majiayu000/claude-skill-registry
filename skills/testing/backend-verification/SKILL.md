---
name: backend-verification
description: Automatically runs required Go checks after any backend code changes. Ensures go vet, gofmt, and go test pass before commits. Use whenever modifying files in the backend/ directory.
---

# Backend Verification

This skill ensures all Go code changes pass required CI checks before committing.

## Required Commands

After ANY changes to Go files in `backend/`, run these commands in order:

### 1. Format Code
```bash
cd /home/user/ishkul/backend && gofmt -w .
```
Automatically formats all Go files to standard style.

### 2. Run Static Analysis
```bash
cd /home/user/ishkul/backend && go vet ./...
```
Catches common errors like:
- Printf format string issues
- Unreachable code
- Suspicious constructs

### 3. Run Tests
```bash
cd /home/user/ishkul/backend && go test ./...
```
Ensures all unit tests pass.

## Quick One-Liner

Run all checks at once:
```bash
cd /home/user/ishkul/backend && gofmt -w . && go vet ./... && go test ./...
```

## When to Use

- After creating new handlers in `internal/handlers/`
- After modifying existing Go code
- Before committing any backend changes
- After adding new packages or dependencies

## CI Integration

These checks run automatically in the CI pipeline. Running them locally first:
- Catches issues early
- Speeds up the PR review process
- Prevents failed deployments

## Common Issues

### go vet Failures
- Check for unused variables
- Verify printf format strings match arguments
- Look for unreachable code after return statements

### Test Failures
- Check test file naming: `*_test.go`
- Verify test function naming: `Test*`
- Run specific test: `go test -run TestFunctionName ./...`
