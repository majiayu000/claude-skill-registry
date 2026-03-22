---
name: makefile-first
description: Makefile-first policy for build, test, lint, format, and verification commands. Use when running any project commands or executing tests. Do NOT use when the project has no Makefile -- check for a Makefile before applying this policy.
durability: encoded-preference
---

# Makefile-First Policy

## Core Rule

**ALWAYS use Makefile** - Never run commands directly.

## Decision Flow

```
1. Check if Makefile exists
   ├── YES → Use make targets (make test, make lint, etc.)
   └── NO → See "When Makefile Doesn't Exist"
```

## When Makefile Doesn't Exist

| Situation | Action |
|-----------|--------|
| New project (creating from scratch) | Create Makefile |
| Existing codebase | **Ask user before creating Makefile** |
| User declines | Use language-specific commands |

## Why Makefile

- Single entry point for all operations
- Self-documenting (serves as handover documentation)
- Language-agnostic interface
- Enables `make check` before every PR
- Reproducible across team members and CI/CD

## Common Targets

```bash
make help      # Show available targets
make build     # Build the project
make test      # Run unit/integration tests
make lint      # Run linter
make format    # Format code
make check     # Run all verification (lint + test + typecheck)
make e2e       # Run E2E tests
make clean     # Clean build artifacts
```

## Discovering Targets

```bash
# List available targets
make help

# Or parse Makefile directly
grep -E '^[a-zA-Z_-]+:' Makefile
```

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| Running `npm run build` directly | Use `make build` |
| Running `go test ./...` directly | Use `make test` |
| Running `pytest` directly | Use `make test` |
| Running `ruff check .` directly | Use `make lint` |

## Recommended Makefile Template

```makefile
.PHONY: build test lint format check clean

build:
	# Language-specific build command

test:
	# Language-specific test command

lint:
	# Language-specific lint command

format:
	# Language-specific format command

check: lint test
	@echo "All checks passed"

clean:
	# Clean build artifacts

help:
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'
```
