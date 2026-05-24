---
name: language-go
description: Go language patterns and best practices. Use when language go guidance is required.
allowed-tools:
  - Bash(go version)
  - Bash(golangci-lint)
---

## Key Execution Capabilities
### Code Validation

- Run `go build` for compilation validation
- Execute `golangci-lint` for comprehensive linting
- Run tests with `go test`
- Validate module structure and dependencies

### Tool Integration

- Use `golangci-lint` for multi-linter analysis
- Leverage `go mod` for dependency management
- Apply `go fmt` and `go vet` for formatting and validation
- Execute `go test` with coverage for testing

### Execution Context

- Process Go files from filesystem layer
- Generate structured reports with findings
- Create minimal, rule-compliant patches for violations
- Maintain separation between governance rules and execution tools

## Error Handling

This skill provides execution-layer error handling for Go code analysis:
- Compilation errors or warnings
- Linting rule violations
- Missing dependencies or tools
- Test failures or coverage issues

## Usage Notes

- Always delegate to governance rules for policy decisions
- Focus on concrete tool execution and result processing
- Provide deterministic, tool-first analysis results
- Maintain separation between rule definition and rule application