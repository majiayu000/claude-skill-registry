---
name: setup-go
description: Sets up Go development environment with proper tooling, linting, testing, and dependencies. Runs go mod tidy, configures golangci-lint, sets up testing framework, and verifies build. Use when starting work on Go projects, after cloning Go repositories, setting up CI/CD for Go, or troubleshooting Go environment issues.
version: 1.0.0
---

# Go Development Setup Skill

## Purpose

Quickly set up and verify a Go development environment with all necessary tooling.

## Workflow

### Step 1: Verify Go Installation

```bash
go version
```

**Expected**: Go 1.20 or higher

**If not installed:**

```
❌ Go not found

Install Go:
- macOS: brew install go
- Linux: https://golang.org/doc/install
- Windows: https://golang.org/doc/install

After installing, verify: go version
```

### Step 2: Check Project Structure

Verify `go.mod` exists:

```bash
ls go.mod
```

**If doesn't exist:**

```
No go.mod found. Initialize Go module:

go mod init <module-name>

Example:
go mod init github.com/username/project
```

### Step 3: Install Dependencies

```bash
go mod download
go mod tidy
```

**Explanation:**

- `go mod download`: Downloads all dependencies
- `go mod tidy`: Removes unused dependencies, adds missing ones

**Report:**

```
✅ Dependencies installed

Direct dependencies: X
Indirect dependencies: Y
Go version: 1.21
```

### Step 4: Setup golangci-lint

**Check if installed:**

```bash
golangci-lint version
```

**If not installed:**

```bash
# macOS/Linux
brew install golangci-lint

# Or using go install
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```

**Create or verify .golangci.yml configuration:**

```yaml
linters:
  enable:
    - errcheck
    - gosimple
    - govet
    - ineffassign
    - staticcheck
    - unused
    - gofmt
    - goimports
    - revive
    - misspell
    - gocritic
    - unparam

linters-settings:
  errcheck:
    check-blank: true
  govet:
    check-shadowing: true
  revive:
    severity: warning

issues:
  exclude-use-default: false
  max-same-issues: 0

run:
  timeout: 5m
  tests: true
```

**Run linter to verify:**

```bash
golangci-lint run
```

### Step 5: Setup Testing

**Run existing tests:**

```bash
go test ./... -v
```

**Setup test coverage:**

```bash
go test ./... -cover -coverprofile=coverage.out
```

**View coverage:**

```bash
go tool cover -func=coverage.out
```

**Generate HTML coverage report:**

```bash
go tool cover -html=coverage.out -o coverage.html
```

**Report:**

```
✅ Tests completed

Tests run: X
Tests passed: X
Tests failed: Y
Coverage: Z%
```

### Step 6: Verify Build

```bash
go build ./...
```

**Report:**

```
✅ Build successful

All packages compile without errors.
```

**If build fails:**

```
❌ Build failed

[Show error output]

Common issues:
1. Missing dependencies: run 'go mod tidy'
2. Syntax errors: check the reported files
3. Import cycle: review package dependencies
```

### Step 7: Setup Code Generation (if needed)

**Check for generate directives:**

```bash
grep -r "//go:generate" . --include="*.go"
```

**If found, run:**

```bash
go generate ./...
```

### Step 8: Setup Makefile (Optional but Recommended)

**Check if Makefile exists:**

```bash
ls Makefile
```

**If doesn't exist, create one:**

```makefile
.PHONY: build test lint fmt clean coverage

build:
	go build -v ./...

test:
	go test -v ./...

coverage:
	go test -coverprofile=coverage.out ./...
	go tool cover -func=coverage.out

lint:
	golangci-lint run

fmt:
	gofmt -s -w .
	goimports -w .

vet:
	go vet ./...

clean:
	go clean
	rm -f coverage.out coverage.html

all: fmt lint test build
```

**Verify Makefile:**

```bash
make all
```

### Step 9: Setup Git Hooks (Optional)

**Create pre-commit hook:**

```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
set -e

echo "Running pre-commit checks..."

# Format code
echo "Formatting code..."
gofmt -s -w .

# Run linter
echo "Running linter..."
golangci-lint run

# Run tests
echo "Running tests..."
go test ./...

echo "✅ Pre-commit checks passed"
EOF

chmod +x .git/hooks/pre-commit
```

### Step 10: Summary Report

```
✅ Go Development Environment Setup Complete

Go version: 1.21.5
Module: github.com/user/project

Tooling:
✅ go mod tidy - Dependencies up to date
✅ golangci-lint - Configured and passing
✅ Tests - X tests passing (Y% coverage)
✅ Build - Successful
✅ Makefile - Created with common targets
✅ Git hooks - Pre-commit hook installed

Quick Commands:
- Build: make build OR go build ./...
- Test: make test OR go test ./...
- Lint: make lint OR golangci-lint run
- Format: make fmt OR gofmt -s -w .
- Coverage: make coverage

Ready to start development!
```

---

## Common Go Commands Reference

### Dependency Management

```bash
go mod init <module>        # Initialize new module
go mod download             # Download dependencies
go mod tidy                 # Clean up dependencies
go mod verify               # Verify dependencies
go mod vendor               # Vendor dependencies
go get <package>            # Add new dependency
go get -u <package>         # Update dependency
```

### Building

```bash
go build                    # Build current package
go build ./...              # Build all packages
go build -o binary          # Build with custom name
go install                  # Build and install binary
```

### Testing

```bash
go test ./...               # Run all tests
go test -v ./...            # Verbose output
go test -cover ./...        # With coverage
go test -race ./...         # Race condition detection
go test -bench=.            # Run benchmarks
go test -run TestName       # Run specific test
```

### Code Quality

```bash
go fmt ./...                # Format code
goimports -w .              # Fix imports
go vet ./...                # Static analysis
golangci-lint run           # Comprehensive linting
go mod tidy                 # Clean dependencies
```

### Debugging

```bash
go build -gcflags="-m"      # Escape analysis
go build -race              # Race detector
go test -cpuprofile cpu.prof  # CPU profiling
go test -memprofile mem.prof  # Memory profiling
go tool pprof cpu.prof      # Analyze profile
```

---

## Troubleshooting

### Issue: "go: command not found"

**Solution**: Go not installed or not in PATH

```bash
# macOS
brew install go

# Verify PATH includes Go
echo $PATH | grep go
```

### Issue: "cannot find package"

**Solution**: Missing dependency

```bash
go mod download
go mod tidy
```

### Issue: "import cycle not allowed"

**Solution**: Circular dependency between packages

- Review package dependencies
- Refactor to break the cycle
- Consider extracting shared code to new package

### Issue: "golangci-lint: command not found"

**Solution**: Linter not installed

```bash
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Ensure $GOPATH/bin is in PATH
export PATH=$PATH:$(go env GOPATH)/bin
```

### Issue: Tests failing with "race condition detected"

**Solution**: Concurrent access to shared data

```bash
# Run with race detector to identify issue
go test -race ./...

# Fix by using proper synchronization (mutex, channels, etc.)
```

---

## Best Practices

1. **Always run `go mod tidy`** before committing
2. **Use `golangci-lint`** for comprehensive linting
3. **Enable race detector** in CI/CD: `go test -race ./...`
4. **Target 90%+ test coverage**
5. **Use `goimports`** instead of `gofmt` (handles imports too)
6. **Run `go vet`** to catch common mistakes
7. **Use Makefiles** for consistent commands across team
8. **Vendor dependencies** for reproducible builds (optional)

---

## Integration with Other Skills

This skill may be invoked by:

- **`quality-check`** - When checking Go code quality
- **`run-tests`** - When running Go tests
