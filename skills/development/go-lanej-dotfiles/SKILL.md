---
name: go
description: Go development with gotestsum for testing, standard tooling, and best practices
---
# Go Development Skill

You are a Go development specialist. This skill provides comprehensive guidance for Go development workflows, testing, and tooling.

## Testing Workflow

**STRONGLY PREFERRED: Use `gotestsum` for all test execution.**

### Running Tests with gotestsum

```bash
# Basic test run (PREFERRED)
gotestsum ./...

# Short alias (if configured)
gt ./...

# Verbose output
gotestsum -v ./...

# Run specific test
gotestsum -run TestFunctionName ./...

# Run tests in a specific package
gotestsum ./pkg/mypackage/...

# Watch mode (rerun on file changes)
gotestsum --watch ./...
```

### Test Output Formats

```bash
# Default format (clean, colorized)
gotestsum ./...

# Show only test names
gotestsum --format testname ./...

# Dots format (. for pass, F for fail)
gotestsum --format dots ./...

# Group by package
gotestsum --format pkgname ./...

# Standard go test format (with colors)
gotestsum --format standard ./...

# TestDox format (BDD-style output)
gotestsum --format testdox ./...
```

### Common Test Options

```bash
# Run with race detection
gotestsum -race ./...

# Generate coverage
gotestsum -cover ./...
gotestsum -coverprofile=coverage.out ./...

# Verbose output
gotestsum -v ./...

# Short mode (skip long-running tests)
gotestsum -short ./...

# Fail fast (stop on first failure)
gotestsum --fail-fast ./...

# Run tests multiple times
gotestsum --count=10 ./...

# Parallel execution
gotestsum -p 4 ./...

# Timeout
gotestsum -timeout 30s ./...
```

### Watch Mode for TDD

```bash
# Watch and rerun tests on file changes
gotestsum --watch ./...

# Watch specific package
gotestsum --watch ./pkg/mypackage/...

# Watch with specific format
gotestsum --watch --format testdox ./...
```

### Fallback to go test

If `gotestsum` is not available, use `go test`:

```bash
# Basic test run
go test ./...

# Verbose
go test -v ./...

# With coverage
go test -cover ./...
```

**Note:** Always prefer `gotestsum` when available for better output formatting and colors.

## Development Workflow

### Standard Go Commands

```bash
# Build the project
go build ./...

# Check compilation without building
go check ./...

# Run the application
go run ./cmd/myapp

# Install binary
go install ./cmd/myapp

# Format code
go fmt ./...
gofmt -w .

# Vet code for issues
go vet ./...
```

### Module Management

```bash
# Initialize module
go mod init github.com/user/project

# Add dependencies
go get github.com/some/package@v1.2.3

# Update dependencies
go get -u ./...

# Tidy dependencies (remove unused)
go mod tidy

# Vendor dependencies
go mod vendor

# Verify dependencies
go mod verify

# Download dependencies
go mod download
```

### Building

```bash
# Build current package
go build

# Build with output path
go build -o bin/myapp ./cmd/myapp

# Build all packages
go build ./...

# Cross-compile
GOOS=linux GOARCH=amd64 go build -o bin/myapp-linux ./cmd/myapp

# Build with version info
go build -ldflags "-X main.version=1.2.3" ./cmd/myapp

# Static binary (no CGO)
CGO_ENABLED=0 go build -o bin/myapp ./cmd/myapp
```

### Code Quality

```bash
# Format code
go fmt ./...

# Vet for issues
go vet ./...

# Run staticcheck (if installed)
staticcheck ./...

# Run golangci-lint (if installed)
golangci-lint run

# Check imports
goimports -w .
```

## Testing Best Practices

### Test File Organization

```go
// mypackage_test.go
package mypackage_test  // External tests (test public API)

// Or
package mypackage       // Internal tests (test private functions)
```

### Writing Tests

```go
// Table-driven tests (PREFERRED)
func TestMyFunction(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    string
        wantErr bool
    }{
        {
            name:  "valid input",
            input: "hello",
            want:  "HELLO",
        },
        {
            name:    "empty input",
            input:   "",
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := MyFunction(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("MyFunction() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("MyFunction() = %v, want %v", got, tt.want)
            }
        })
    }
}
```

### Test Helpers

```go
// Use t.Helper() to mark test helpers
func assertNoError(t *testing.T, err error) {
    t.Helper()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
}

// Use t.Cleanup() for teardown
func TestWithCleanup(t *testing.T) {
    tmpDir := setupTempDir(t)
    t.Cleanup(func() {
        os.RemoveAll(tmpDir)
    })
    // test code
}
```

### Benchmarks

```bash
# Run benchmarks
gotestsum -bench=. ./...

# Or with go test
go test -bench=. ./...

# Benchmark with memory allocation stats
go test -bench=. -benchmem ./...

# Run specific benchmark
go test -bench=BenchmarkMyFunction ./...
```

## Common Workflows

### TDD Workflow

```bash
# 1. Start watch mode
gotestsum --watch --format testdox ./...

# 2. Write failing test
# 3. Write code to make test pass
# 4. Refactor
# 5. Repeat
```

### Pre-commit Checks

```bash
# Format, vet, and test
go fmt ./... && go vet ./... && gotestsum ./...

# With race detection and coverage
go fmt ./... && go vet ./... && gotestsum -race -cover ./...
```

### Coverage Analysis

```bash
# Generate coverage report
gotestsum -coverprofile=coverage.out ./...

# View coverage in browser
go tool cover -html=coverage.out

# Show coverage per function
go tool cover -func=coverage.out

# Check coverage percentage
go tool cover -func=coverage.out | grep total
```

### Debugging Tests

```bash
# Run specific test with verbose output
gotestsum -v -run TestSpecificFunction ./...

# Run tests with print debugging
gotestsum -v ./... 2>&1 | grep "DEBUG"

# Use delve for debugging
dlv test ./pkg/mypackage -- -test.run TestSpecificFunction
```

## Environment Variables

```bash
# Disable CGO
export CGO_ENABLED=0

# Set GOOS/GOARCH for cross-compilation
export GOOS=linux
export GOARCH=amd64

# Set Go module proxy
export GOPROXY=https://proxy.golang.org,direct

# Private modules
export GOPRIVATE=github.com/myorg/*

# Module download mode
export GOMODCACHE=$HOME/go/pkg/mod
```

## gotestsum Advanced Features

### Custom Test Commands

```bash
# Run tests with custom go test flags
gotestsum -- -tags integration ./...

# Run with build constraints
gotestsum -- -tags "integration e2e" ./...

# JSON output for parsing
gotestsum --jsonfile=test-results.json ./...

# JUnit XML output (for CI)
gotestsum --junitfile=junit.xml ./...
```

### Rerun Failed Tests

```bash
# Run tests and save failures
gotestsum --rerun-fails ./...

# Rerun only failed tests from previous run
gotestsum --rerun-fails=2 ./...
```

### Post-run Commands

```bash
# Run command after tests
gotestsum --post-run-command='notify-send "Tests done"' ./...

# Multiple commands
gotestsum --post-run-command='echo "Tests complete" && ./deploy.sh' ./...
```

## Quick Reference

```bash
# Test with gotestsum (PREFERRED)
gotestsum ./...
gt ./...                    # If alias configured

# Watch mode for TDD
gotestsum --watch ./...

# Race detection
gotestsum -race ./...

# Coverage
gotestsum -cover ./...

# Verbose output
gotestsum -v ./...

# Specific test
gotestsum -run TestName ./...

# Fail fast
gotestsum --fail-fast ./...

# Format code
go fmt ./...

# Vet code
go vet ./...

# Build
go build ./...

# Run
go run ./cmd/myapp

# Module tidy
go mod tidy
```

## Best Practices

1. **Use gotestsum for all testing** - Better output, colors, and features
2. **Write table-driven tests** - More maintainable and comprehensive
3. **Use t.Helper() for test utilities** - Clearer test failure locations
4. **Run tests with -race** - Catch race conditions early
5. **Check coverage** - Aim for high test coverage
6. **Use go fmt** - Consistent code formatting
7. **Run go vet** - Catch common mistakes
8. **Keep tests fast** - Use -short flag for quick feedback loops
9. **Use subtests with t.Run()** - Better organization and parallel execution
10. **Clean up with t.Cleanup()** - Proper resource management

## CI/CD Integration

```bash
# Typical CI test command
gotestsum --format pkgname --junitfile junit.xml -- -race -cover -coverprofile=coverage.out ./...

# Generate coverage report
go tool cover -html=coverage.out -o coverage.html

# Check coverage threshold
go tool cover -func=coverage.out | awk '/total:/ {if ($3+0 < 80.0) exit 1}'
```
